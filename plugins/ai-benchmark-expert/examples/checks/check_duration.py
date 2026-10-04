"""Hidden acceptance check for the `parse-duration` task (runs in the model's workdir)."""
import sys

sys.path.insert(0, ".")
from duration import parse_duration  # noqa: E402

OK = {"45s": 45, "2h": 7200, "1h30m": 5400, "1h 5m 3s": 3903, "90m": 5400, "0s": 0,
      " 3m ": 180, "1H2M": 3720, "10h0m1s": 36001}
BAD = ["", "5x", "h", "-1m", "1.5h", "1m1h", "1h1h", "3", "m5"]

failed = []
for text, want in OK.items():
    try:
        got = parse_duration(text)
    except Exception as e:  # noqa: BLE001
        got = f"raised {type(e).__name__}"
    if got != want:
        failed.append(f"parse_duration({text!r}): want {want}, got {got!r}")
for text in BAD:
    try:
        got = parse_duration(text)
        failed.append(f"parse_duration({text!r}): want ValueError, got {got!r}")
    except ValueError:
        pass
    except Exception as e:  # noqa: BLE001
        failed.append(f"parse_duration({text!r}): want ValueError, got {type(e).__name__}")
print("\n".join(failed) or "all cases pass")
sys.exit(1 if failed else 0)
