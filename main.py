"""The Houseplant Out-of-Office.

Writes one out-of-office auto-reply, as if a houseplant had written it,
to /output/entry.txt. Standard library only, deterministic, no network.
"""

import os

LINE = (
    "Out of office: unwatered since March. "
    "My roots unionised and demand a windowsill transfer. "
    "Send water, not emails."
)

MAX_CHARS = 120


def validate(text: str) -> None:
    """Enforce the sealed gate: one line, 1-120 chars, not only whitespace."""
    if not text or text.strip() == "":
        raise ValueError("entry must not be empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )


def main() -> None:
    validate(LINE)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    payload = LINE + "\n"
    if len(payload) > MAX_CHARS:
        raise ValueError(
            "entry with newline is %d characters, over the %d limit"
            % (len(payload), MAX_CHARS)
        )
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)
    with open(path, encoding="utf-8") as fh:
        written = fh.read()
    if written != payload:
        raise ValueError("entry.txt does not match the validated line")


if __name__ == "__main__":
    main()
