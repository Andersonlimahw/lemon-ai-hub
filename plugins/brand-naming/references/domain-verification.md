# Domain verification

## ⚠️ Transactional verification is a mandatory gate

This runs on funnel survivors **before** red team, not after. A name that
scores 49/50 but has no available domain wastes the rest of the sprint —
reverse the order and this cost disappears. No candidate advances past
this gate on `UNKNOWN` or `NOT VERIFIED` status; that status means
demote, never promote.

### Protocol

**`.com.br` (Registro.br):**

```bash
# 1. WHOIS
whois -h whois.registro.br NAME.com.br
# "No match." -> AVAILABLE
# "domain: NAME.COM.BR" -> REGISTERED, read the status field
# timeout/error -> try RDAP next

# 2. RDAP (if WHOIS failed)
curl -s https://rdap.registro.br/domain/NAME.com.br | jq '.status'
# 404 -> AVAILABLE
# ["active"] / ["serverUpdateProhibited"] etc -> REGISTERED
# network error -> NOT VERIFIED
```

**`.com` and other gTLDs (registry WHOIS / RDAP):**

```bash
# 1. WHOIS
whois NAME.com
# "No match for..." -> AVAILABLE
# "Domain Name: NAME.COM" -> REGISTERED, note registrar + creation date
# timeout -> try RDAP next

# 2. RDAP (if WHOIS failed)
curl -s https://rdap.verisign.com/com/v1/domain/NAME.com | jq '.status'
# 404 -> AVAILABLE
# ["active"] or a registrar field present -> REGISTERED
# network error -> NOT VERIFIED
```

A timeout on one method is not evidence of anything — retry with the
other method once. Only after **both** WHOIS and RDAP fail or time out
does the candidate become `NOT VERIFIED`. It stays out of the finalist
track until re-verified; it does not default to "likely free".

### Decision matrix

| `.com.br` | `.com` | Action |
|---|---|---|
| AVAILABLE | AVAILABLE | Advance to red team |
| AVAILABLE | PARKED, buy-out under budget | Advance, note the cost |
| AVAILABLE | ACTIVE / REGISTERED | Advance with caution, flag the risk |
| NOT VERIFIED | any | Demote — do not promote to finalist |
| REGISTERED | any | Discard |

`check_domains.py` reduces a longlist to survivors fast; it is never the
gate itself — WHOIS or RDAP is. Absence of NS delegation is not proof of
availability: investor-held and parked domains are often registered with
no delegation.

## Never invent availability

This is the most common way a naming report becomes worthless. Every domain
claim must be backed by a real RDAP or WHOIS lookup, or an equivalent
retrieved page. If you could not verify it, write `UNKNOWN`.

## Classification

| Status | Meaning | Evidence required |
|---|---|---|
| `AVAILABLE` | No registration record | RDAP 404 / WHOIS "No match" |
| `REGISTERED-PARKED` | Registered, no real site | RDAP record + parked page |
| `ACTIVE` | Registered and in real use | RDAP record + live site |
| `FOR SALE` | Listed on a marketplace | Marketplace listing URL |
| `UNKNOWN` | Could not verify | Say so explicitly |

## Clarify the rule before you funnel

"The `.com` must be acquirable" is ambiguous and the interpretation changes
which names can win. Confirm which one the user means:

1. **Unregistered only** — brutal. Nearly every short, pronounceable
   Romance or English word is already registered. Expect the surviving set
   to be obscure and unattractive; free `.com` on a short word usually
   signals that the word is unappealing, not that you found an opening.
2. **Free or parked / for sale** — realistic. Opens the field
   substantially. Budget for an aftermarket purchase.
3. **Not actively used by a similar company** — the brand-risk rule. A
   parked `.com` is tolerable; a `.com` running an active technology
   company is disqualifying.

Most sophisticated briefs mean (2) combined with (3).

## TLDs to check

```
NAME.com    NAME.ai     NAME.dev
NAME.io     NAME.tech   + the relevant ccTLD (e.g. NAME.com.br)
```

## RDAP endpoints

RDAP returns structured JSON and is the authoritative source.

| TLD | Endpoint |
|---|---|
| `.com` / `.net` | `https://rdap.verisign.com/com/v1/domain/NAME.com` |
| `.com.br` | `https://rdap.registro.br/domain/NAME.com.br` |
| `.dev` / `.app` | `https://pubapi.registry.google/rdap/domain/NAME.dev` |
| `.io` / `.ai` | `https://rdap.identitydigital.services/rdap/domain/NAME.io` |
| `.tech` | `https://rdap.radix.host/rdap/domain/NAME.tech` |
| any | resolve the base from `https://data.iana.org/rdap/dns.json` |

A `404` means no registration record. A `200` returns registration date,
registrar, status flags and nameservers.

**Only trust a `404` from the authoritative registry server.** A generic
redirector such as `rdap.org` answers `404` for TLDs it cannot route — for
`.io` it returns `404` even for `google.io`. Reading that as `AVAILABLE`
is exactly the invented-availability failure this file exists to prevent.
Resolve the endpoint from the IANA bootstrap; if no server is published for
the TLD, the answer is `UNKNOWN`, not `AVAILABLE`.

## DNS pre-filter

Full RDAP on a large longlist is slow. Use absence of NS delegation as a
cheap pre-filter, then confirm survivors with RDAP.

`scripts/check_domains.py` does both. Important caveats:

- **No NS does not mean available.** Domains held by investors are often
  registered with no delegation. Always confirm with RDAP.
- **NS present does mean registered.** This direction is reliable, so it is
  safe to use for elimination.
- Expect false positives on well-known brands whose resolver behaviour is
  unusual — sanity-check the script against a few domains you know are
  taken before trusting a run.

## Handles

Check the handle on the platforms the company will actually use, and record
them the same way. An unavailable handle is a minor issue with known
workarounds (`getNAME`, `NAMEhq`, `withNAME`); an unavailable `.com` owned
by a competitor is not.

## Decision rule

A domain is never sufficient to approve a name. Strategic fit and
distinctiveness are independent gates. Do not let an available domain
promote a weak name — that inversion is how naming sprints fail.
