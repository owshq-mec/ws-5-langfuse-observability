#!/usr/bin/env python3
"""Copy prompt text, facilitator note, team discussion and gate from prompts/*.md into 04-prompts.html.

Run after editing any prompt: python3 presentation/sync_prompts.py
Elements opt in with data-sync="NN:field", where field is prompt, prompt:A, facilitator, discussion or gate.
A field the prompt file does not have (00 has no team discussion) leaves the element as it is.
"""
import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DECK = HERE / "04-prompts.html"
PROMPTS = HERE.parent / "prompts"


def inline(text):
    text = html.escape(" ".join(text.split()), quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)


def parse(md):
    fields = {"facilitator": inline(re.search(r"\*\*Facilitator:\*\*(.*?)\n\n", md, re.S).group(1))}
    for m in re.finditer(r"^## Prompt(?: ([A-Z]))?[^\n]*\n+```text\n(.*?)```", md, re.S | re.M):
        key = f"prompt:{m.group(1)}" if m.group(1) else "prompt"
        fields[key] = html.escape(m.group(2).rstrip("\n"), quote=False)
    discussion = re.search(r"^## Team discussion\n(.*?)(?=^## )", md, re.S | re.M)
    if discussion:
        items = [i for i in re.split(r"^- ", discussion.group(1).strip(), flags=re.M) if i.strip()]
        fields["discussion"] = "".join(f"<li>{inline(i)}</li>" for i in items)
    fields["gate"] = inline(re.search(r"^## Gate\n(.*)", md, re.S | re.M).group(1))
    return fields


def main():
    data = {p.name[:2]: parse(p.read_text()) for p in sorted(PROMPTS.glob("[0-9][0-9]-*.md"))}
    pattern = re.compile(r'(<(\w+)\b[^>]*\bdata-sync="(\d\d):([\w:]+)"[^>]*>).*?(</\2>)', re.S)
    count = 0

    def fill(m):
        nonlocal count
        value = data[m.group(3)].get(m.group(4))
        if value is None:
            return m.group(0)
        count += 1
        return m.group(1) + value + m.group(5)

    deck = pattern.sub(fill, DECK.read_text())
    DECK.write_text(deck)
    print(f"synced {count} elements from {len(data)} prompt files")


if __name__ == "__main__":
    main()
