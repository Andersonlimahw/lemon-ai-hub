"""Hidden acceptance check for the `slugify-bugfix` task (runs in the model's workdir)."""
import inspect
import sys

sys.path.insert(0, ".")
from slugify import slugify  # noqa: E402

CASES = {
    ("Hello, World!",): "hello-world",
    ("  Ação & Reação ",): "acao-reacao",
    ("Crème brûlée -- recipe",): "creme-brulee-recipe",
    ("---already--slugged---",): "already-slugged",
    ("Über 9000!!!",): "uber-9000",
    ("",): "",
    ("!!!",): "",
    ("a" * 10 + " " + "b" * 10, 11): "aaaaaaaaaa",
}

failed = [(args, want, slugify(*args)) for args, want in CASES.items() if slugify(*args) != want]
sig = inspect.signature(slugify)
if list(sig.parameters) != ["title", "max_len"] or sig.parameters["max_len"].default != 60:
    failed.append(("signature", "slugify(title, max_len=60)", str(sig)))
for args, want, got in failed:
    print(f"FAIL slugify{args!r}: want {want!r}, got {got!r}")
sys.exit(1 if failed else 0)
