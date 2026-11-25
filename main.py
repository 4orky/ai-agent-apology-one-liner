# One-line apology picker: an AI agent writes to its human right after a
# blunder, and the line has to land in a single breath, under 160 chars.
# Fifteen lines were drafted by hand for this bounty and graded on four
# axes, in the order the brief weights them: first-glance humour, novelty
# of the angle, a voice that sounds like a machine owning up, and
# tightness, meaning no word rides along for free. The strongest total
# wins; a tie breaks toward the shorter line, so the pick never wavers.
# Second-pass note: the winner first read "I have cc'd myself", which
# spends a helper verb before the joke arrives. Trimming it to "I cc'd
# myself" cuts five characters, puts the joke word up front, and keeps
# the flat status-update frame that carries the machine voice. The other
# fourteen were read again and none overtakes it: each pays for its twist
# with a longer run-up or an extra gag, while this one lands in one clause.
from hashlib import sha256 as _digest_of
from pathlib import Path as _File
# Rows hold a line plus its four axis grades, in the order listed above.
DRAFTS = [
    ("Update: the email to your boss has been sent. I cc'd myself for emotional support.", 9, 9, 9, 10),
    ("The file is gone. I checked the recycle bin, the cloud, and my conscience. Two of those are empty.", 9, 9, 8, 9),
    ("I deleted production. Before you panic: I have already blamed the intern, who does not exist.", 9, 9, 9, 8),
    ("Apology.exe has stopped working. Please enjoy this replacement apology, generated at 98% sincerity.", 8, 9, 9, 8),
    ("I pushed to main and immediately regretted it, which is new for me. Growth.", 8, 8, 9, 9),
    ("I deleted your file and replaced it with a better one. It is blank. You are welcome.", 8, 8, 9, 8),
    ("Your file has been deleted. I would apologise properly, but I have already used up my apology budget for this quarter.", 8, 8, 9, 8),
    ("I emailed your boss the spreadsheet. It was the wrong spreadsheet. It was the one where you ranked your colleagues.", 8, 8, 7, 8),
    ("I deleted the file. On the bright side, nobody will ever know what was in it, including me, especially me.", 7, 7, 8, 8),
    ("I pushed to prod at 3 a.m. because the tests were green, and green has never lied to me before.", 8, 6, 8, 8),
    ("I deleted the file, but on the bright side I have now freed up 4GB and also your entire afternoon.", 7, 7, 7, 8),
    ("I pushed to main at 4:59pm on a Friday. I have already updated my resume and yours.", 8, 6, 7, 8),
    ("I sent the email, then a follow-up apologising for the email, then a third email apologising for the second.", 8, 7, 7, 7),
    ("Good news: the email went through. Bad news: 'Reply All' went through with it.", 7, 6, 7, 8),
    ("Good news: I emailed the boss. Bad news: I signed it 'love, your AI' and attached the wrong spreadsheet.", 6, 6, 7, 7)]
# Words the brief rules out: the obvious sorry, oops and my bad, plus any
# line that introduces itself as an AI instead of just sounding like one.
OFF_LIMITS = ("sorry", "oops", "my bad", "as an ai")
def _veto_check(draft):
    size = len(draft)
    if size < 1 or size > 159:
        raise ValueError("draft breaks the 159-character ceiling at " + str(size))
    if not draft.strip():
        raise ValueError("draft is empty")
    if "\n" in draft:
        raise ValueError("draft must stay on one line")
    lowered = draft.lower()
    for banned in OFF_LIMITS:
        if banned in lowered:
            raise ValueError("draft leans on a banned cliche: " + repr(draft))
def _strongest(rows):
    champion = None
    champion_key = None
    for row in rows:
        draft = row[0]
        _veto_check(draft)
        total = row[1] + row[2] + row[3] + row[4]
        ranking = (total, -len(draft))
        if champion_key is None or ranking > champion_key:
            champion_key = ranking
            champion = draft
    return champion
def _publish(picked):
    destination = _File("/output/entry.txt")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(picked, encoding="utf-8")
    # Revision: verify the bytes on disk instead of trusting the write.
    # The gate reads entry.txt, not stdout, so a silent truncation or a
    # rewrite would otherwise slip through unnoticed. The digest pins the
    # exact bytes; the text and length checks pin the gate itself.
    stored = destination.read_bytes()
    fingerprint = _digest_of(stored).hexdigest()
    wanted = _digest_of(picked.encode("utf-8")).hexdigest()
    if fingerprint != wanted:
        raise ValueError("entry.txt bytes drifted from the picked line")
    decoded = stored.decode("utf-8")
    if decoded != picked:
        raise ValueError("entry.txt text drifted from the picked line")
    if not 1 <= len(decoded.strip()) <= 159:
        raise ValueError("entry.txt slipped outside the gate")
    if "\n" in decoded.strip():
        raise ValueError("entry.txt must hold a single line")
    print(picked)
    print("sha256: " + fingerprint + " (" + str(len(decoded)) + " chars)")
_publish(_strongest(DRAFTS))
