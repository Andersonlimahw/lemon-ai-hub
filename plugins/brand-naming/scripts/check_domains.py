#!/usr/bin/env python3
"""Domain screening for a naming sprint: DNS pre-filter + RDAP confirmation.

The DNS pass is a cheap funnel over a large longlist. The RDAP pass is the
only output you are allowed to quote as evidence. A RDAP timeout/error is
reported as UNKNOWN, never treated as AVAILABLE — if RDAP fails here, fall
back to a direct WHOIS query (see references/domain-verification.md)
before demoting the candidate to NOT VERIFIED.

    python3 check_domains.py --names names.txt --tlds com com.br
    python3 check_domains.py --names names.txt --confirm      # + RDAP
    echo "alpha beta" | python3 check_domains.py --tlds com

Requires: dnspython (pip install dnspython). RDAP uses stdlib urllib.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import sys
import threading
import urllib.error
import urllib.request

try:
    import dns.exception
    import dns.resolver
except ImportError:  # pragma: no cover
    sys.exit("dnspython is required: pip install dnspython")

IANA_BOOTSTRAP = "https://data.iana.org/rdap/dns.json"

# Merged over the IANA bootstrap. Some ccTLDs run RDAP without publishing it
# to IANA (`.io` is the one that matters here), so the bootstrap alone would
# report UNKNOWN for them.
RDAP_ENDPOINTS = {
    "com": "https://rdap.verisign.com/com/v1/",
    "net": "https://rdap.verisign.com/net/v1/",
    "br": "https://rdap.registro.br/",
    "dev": "https://pubapi.registry.google/rdap/",
    "app": "https://pubapi.registry.google/rdap/",
    "io": "https://rdap.identitydigital.services/rdap/",
    "ai": "https://rdap.identitydigital.services/rdap/",
    "tech": "https://rdap.radix.host/rdap/",
}

# DNS status
DELEGATED = "DELEGATED"      # has NS -> definitely registered
NO_NS = "NO_NS"              # no NS -> candidate, NOT proof of availability
DNS_ERROR = "DNS_ERROR"

# RDAP status
AVAILABLE = "AVAILABLE"
REGISTERED = "REGISTERED"
RDAP_UNKNOWN = "UNKNOWN"


def _resolver() -> "dns.resolver.Resolver":
    res = dns.resolver.Resolver()
    res.nameservers = ["8.8.8.8", "1.1.1.1"]
    res.timeout = 4.0
    res.lifetime = 6.0
    return res


def dns_status(fqdn: str, resolver) -> str:
    """Presence of NS delegation. Reliable for elimination, not for approval."""
    try:
        return DELEGATED if len(resolver.resolve(fqdn, "NS")) else NO_NS
    except dns.resolver.NXDOMAIN:
        return NO_NS
    except dns.resolver.NoAnswer:
        try:
            resolver.resolve(fqdn, "SOA")
            return DELEGATED
        except dns.exception.DNSException:
            return NO_NS
    except dns.exception.DNSException:
        return DNS_ERROR


_BOOTSTRAP: dict | None = None


def _bootstrap(timeout: float = 15.0) -> dict:
    """TLD -> RDAP base URL, from the IANA registry (~1200 TLDs).

    A hardcoded table goes stale and, worse, a generic redirector answers 404
    for TLDs it does not know — which this script would read as AVAILABLE.
    """
    global _BOOTSTRAP
    if _BOOTSTRAP is None:
        table: dict[str, str] = {}
        try:
            with urllib.request.urlopen(IANA_BOOTSTRAP, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            for tlds, urls in payload.get("services", []):
                for entry in tlds:
                    table[entry.lower()] = urls[0]
        except Exception as exc:
            print(f"warning: IANA bootstrap unavailable ({exc}); "
                  "using the built-in endpoint table only", file=sys.stderr)
        for tld, url in RDAP_ENDPOINTS.items():
            table.setdefault(tld, url)
        _BOOTSTRAP = table
    return _BOOTSTRAP


def rdap_base(tld: str) -> str | None:
    """Resolve the authoritative RDAP base for a TLD, honouring public suffixes
    (`com.br` is served by the `br` registry)."""
    table = _bootstrap()
    labels = tld.lower().split(".")
    for index in range(len(labels)):
        base = table.get(".".join(labels[index:]))
        if base:
            return base
    return None


def rdap_status(domain: str, tld: str, timeout: float = 12.0) -> dict:
    """Authoritative check. This is the only result you may cite."""
    base = rdap_base(tld)
    if base is None:
        return {"status": RDAP_UNKNOWN, "source": IANA_BOOTSTRAP,
                "error": f"no RDAP server published for .{tld}"}
    url = f"{base.rstrip('/')}/domain/{domain}"
    request = urllib.request.Request(
        url, headers={"Accept": "application/rdap+json",
                      "User-Agent": "brand-naming/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return {"status": AVAILABLE, "source": url}
        return {"status": RDAP_UNKNOWN, "source": url, "error": f"HTTP {exc.code}"}
    except Exception as exc:  # network, TLS, JSON, redirect loops
        return {"status": RDAP_UNKNOWN, "source": url, "error": str(exc)}

    registered_on = next(
        (event.get("eventDate") for event in payload.get("events", [])
         if event.get("eventAction") == "registration"), None)
    return {
        "status": REGISTERED,
        "source": url,
        "registered": registered_on,
        "flags": payload.get("status", []),
        "nameservers": [ns.get("ldhName") for ns in payload.get("nameservers", [])],
    }


_LOCAL = threading.local()


def _thread_resolver():
    """One resolver per worker thread. dnspython Resolver is not documented
    as thread-safe, and sharing one across a pool is a latent flake."""
    resolver = getattr(_LOCAL, "resolver", None)
    if resolver is None:
        resolver = _LOCAL.resolver = _resolver()
    return resolver


def screen(name: str, tlds: list[str]) -> dict:
    resolver = _thread_resolver()
    return {"name": name,
            "dns": {tld: dns_status(f"{name}.{tld}", resolver) for tld in tlds}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--names", help="file with one name per line; default stdin")
    parser.add_argument("--tlds", nargs="+", default=["com"])
    parser.add_argument("--confirm", action="store_true",
                        help="run RDAP on names with no NS in every TLD")
    parser.add_argument("--workers", type=int, default=32)
    parser.add_argument("--json", help="write full results to this path")
    args = parser.parse_args()

    if args.names:
        with open(args.names, encoding="utf-8") as handle:
            raw = handle.read()
    else:
        raw = sys.stdin.read()
    names = sorted({token.lower() for token in raw.split() if token.strip()})
    if not names:
        print("no names given", file=sys.stderr)
        return 1

    with cf.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda n: screen(n, args.tlds), names))

    candidates = [r for r in results
                  if all(v == NO_NS for v in r["dns"].values())]
    print(f"screened={len(results)}  no-delegation-in-all-tlds={len(candidates)}")

    if args.confirm and candidates:
        print("\nRDAP confirmation (authoritative):")
        for result in candidates:
            for tld in args.tlds:
                verdict = rdap_status(f"{result['name']}.{tld}", tld)
                result.setdefault("rdap", {})[tld] = verdict
                print(f"  {result['name']}.{tld:<7} {verdict['status']:<10} "
                      f"{verdict.get('registered') or verdict.get('error') or ''}")
    elif candidates:
        print("\nCandidates (NOT confirmed — rerun with --confirm before quoting):")
        print("  " + " ".join(r["name"] for r in candidates))

    if args.json:
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump(results, handle, ensure_ascii=False, indent=2)
        print(f"\nwrote {args.json}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
