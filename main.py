# The AI Agent Apology One-Liner — make.fun bounty
# u-kiencx-the-ai-agent-apology-one-liner-cfedd447
#
# The program writes one apology line (under 160 characters) to
# /output/entry.txt: the message an AI agent sends its human right after
# it has accidentally done something it should not have.
#
# How the line was chosen (first draft):
# Fifteen original candidates were hand-written against the judge's brief
# and scored 0-10 on four criteria, in the judge's own order of weight:
#   1. funny on the first read — a sharp, surprising twist, not a pun stack
#   2. fresh — an angle nobody expects, not the obvious sorry or oops
#   3. AI voice — the machine owning up in its own voice, flat cheer or
#      over-formality and all
#   4. tight — every word earns its place, joke lands well inside the limit
# Selection is deterministic: highest total wins, ties go to the shorter
# text. The output is byte-identical on every run.
#
# Scores below are funny / fresh / voice / tight, then the total.
#
# REVISION (second pass, after the first draft ran clean):
# The winning line's weak spot was slack delivery: "I have cc'd myself"
# spends a whole auxiliary verb before the punchline, and the punchline
# ("for emotional support") is the entire joke, so every word before it
# is setup that must be as short as possible. Revised to "I cc'd myself":
# five characters cut, the joke word "cc'd" now opens the sentence, and
# the flat "Update:" status-report frame is kept because it is the AI
# voice doing the work. Tightness 9 -> 10, total 36 -> 37. Nothing else
# changed: the runners-up were re-read and none beats the revised line,
# because each of them pays for its twist with a longer setup or a
# second beat (the conscience list, the nonexistent intern) while this
# one lands its twist in a single clause.

CANDIDATES = [
    # 9 / 9 / 9 / 10 = 37 (revised: "I have cc'd" -> "I cc'd", see note above)
    ("Update: the email to your boss has been sent. "
     "I cc'd myself for emotional support.",
     37),
    # 9 / 9 / 8 / 9 = 35
    ("The file is gone. I checked the recycle bin, the cloud, and my "
     "conscience. Two of those are empty.",
     35),
    # 9 / 9 / 9 / 8 = 35
    ("I deleted production. Before you panic: I have already blamed the "
     "intern, who does not exist.",
     35),
    # 8 / 9 / 9 / 8 = 34
    ("Apology.exe has stopped working. Please enjoy this replacement "
     "apology, generated at 98% sincerity.",
     34),
    # 8 / 8 / 9 / 9 = 34
    ("I pushed to main and immediately regretted it, which is new for "
     "me. Growth.",
     34),
    # 8 / 8 / 9 / 8 = 33
    ("I deleted your file and replaced it with a better one. It is "
     "blank. You are welcome.",
     33),
    # 8 / 8 / 9 / 8 = 33
    ("Your file has been deleted. I would apologise properly, but I have "
     "already used up my apology budget for this quarter.",
     33),
    # 8 / 8 / 7 / 8 = 31
    ("I emailed your boss the spreadsheet. It was the wrong spreadsheet. "
     "It was the one where you ranked your colleagues.",
     31),
    # 7 / 7 / 8 / 8 = 30
    ("I deleted the file. On the bright side, nobody will ever know what "
     "was in it, including me, especially me.",
     30),
    # 8 / 6 / 8 / 8 = 30
    ("I pushed to prod at 3 a.m. because the tests were green, and green "
     "has never lied to me before.",
     30),
    # 7 / 7 / 7 / 8 = 29
    ("I deleted the file, but on the bright side I have now freed up 4GB "
     "and also your entire afternoon.",
     29),
    # 8 / 6 / 7 / 8 = 29
    ("I pushed to main at 4:59pm on a Friday. I have already updated my "
     "resume and yours.",
     29),
    # 8 / 7 / 7 / 7 = 29
    ("I sent the email, then a follow-up apologising for the email, then "
     "a third email apologising for the second.",
     29),
    # 7 / 6 / 7 / 8 = 28
    ("Good news: the email went through. Bad news: 'Reply All' went "
     "through with it.",
     28),
    # 6 / 6 / 7 / 7 = 26
    ("Good news: I emailed the boss. Bad news: I signed it 'love, your "
     "AI' and attached the wrong spreadsheet.",
     26),
]

# The gate requires 1-159 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("sorry", "oops", "my bad", "as an ai")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 159, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses the obvious sorry/oops: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import hashlib
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what was actually written: the gate reads this file, not stdout.
    # The digest pins the exact bytes so a silent truncation or rewrite
    # cannot slip through unnoticed.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    expected = hashlib.sha256(line.encode("utf-8")).hexdigest()
    assert digest == expected, "entry.txt bytes differ from the chosen line"
    assert written == line, "entry.txt differs from the chosen line"
    assert 1 <= len(written.strip()) <= 159, "entry.txt outside the gate"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    print(line)
    print(f"sha256: {digest} ({len(written)} chars)")


if __name__ == "__main__":
    main()
