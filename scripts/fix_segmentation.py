#!/usr/bin/env python3
"""
Fix the catastrophic mis-segmentation of the Twelve-Bells stanza in
*Das andere Tanzlied* (ch-p3-15) and the closing reprise in
*Das Nachtwandler-Lied* (ch-p4-19).

ch-p3-15  → DE has the whole stanza glued into v41; FR glued into v43.
            EN and ES are correctly split across v41…v63 (23 segments,
            alternating bell-number / poem-line).
            Fix: re-split DE and FR into 23 segments to match EN/ES.

ch-p4-19  → DE in v71 holds the full closing reprise; EN in v72 holds
            the full closing reprise; ES is awkwardly cut between v71
            and v72. No bells in this passage.
            Fix: collapse v71/v72 into a single v71 carrying the
            complete stanza in all three languages.

Idempotent. Run from anywhere.
"""
from __future__ import annotations
import re
from pathlib import Path

PROJ = Path("/Volumes/X10 Pro/Zarathustra/zarathustra-pt")
CH   = PROJ / "source" / "chapters"

# ---- ch-p3-15: split the bells stanza ---------------------------------------
DE_BELLS = [
    "Eins!",
    "Oh Mensch! Gieb Acht!",
    "Zwei!",
    "Was spricht die tiefe Mitternacht?",
    "Drei!",
    "„Ich schlief, ich schlief—,“",
    "Vier!",
    "„Auf tiefen Traum bin ich erwacht:—“",
    "Fünf!",
    "„Die Welt ist tief,“",
    "Sechs!",
    "„Und tiefer als der Tag gedacht.“",
    "Sieben!",
    "„Tief ist ihr Weh—,“",
    "Acht!",
    "„Lust—tiefer noch als Herzeleid:“",
    "Neun!",
    "„Weh spricht: Vergeh!“",
    "Zehn!",
    "„Doch alle Lust will Ewigkeit—,“",
    "Elf!",
    "„—will tiefe, tiefe Ewigkeit!“",
    "Zwölf!",
]

FR_BELLS = [
    "Un!",
    "O homme prends garde!",
    "Deux!",
    "Que dit minuit profond?",
    "Trois!",
    "\"J'ai dormi, j'ai dormi —,\"",
    "Quatre!",
    "\"D'un rêve profond je me suis éveillé : —\"",
    "Cinq!",
    "\"Le monde est profond,\"",
    "Six!",
    "\"Et plus profond que ne pensait le jour.\"",
    "Sept!",
    "\"Profonde est sa douleur —,\"",
    "Huit!",
    "\"La joie — plus profonde que l'affliction.\"",
    "Neuf!",
    "\"La douleur dit : Passe et finis!\"",
    "Dix!",
    "\"Mais toute joie veut l'éternité —,\"",
    "Onze!",
    "\"— veut la profonde éternité!\"",
    "Douze!",
]


def _set_lang_p(txt: str, vid: str, lang: str, body: str) -> str:
    """Set or insert a <p xml:id="VID" xml:lang="LANG"> body inside the
    matching <paragraphs xml:id="VID"> block. VID is the verse id WITHOUT
    -de/-en/etc. suffix."""
    block_re = re.compile(
        rf'(<paragraphs xml:id="{re.escape(vid)}">)(.*?)(</paragraphs>)',
        re.DOTALL,
    )
    pid = f"{vid}-{lang}"
    p_re = re.compile(rf'<p xml:id="{re.escape(pid)}" xml:lang="{lang}">.*?</p>', re.DOTALL)

    def repl_block(m):
        head, mid, tail = m.group(1), m.group(2), m.group(3)
        new_p = f'<p xml:id="{pid}" xml:lang="{lang}">{body}</p>'
        if p_re.search(mid):
            mid = p_re.sub(new_p, mid)
        else:
            # insert before closing — keep before any leading whitespace of </paragraphs>
            # Place it just before the tail with consistent indentation
            indent = "\n              "
            mid = mid.rstrip() + indent + new_p + "\n    "
        return head + mid + tail

    new_txt, n = block_re.subn(repl_block, txt, count=1)
    if n == 0:
        return txt  # paragraph block not present — leave alone
    return new_txt


def fix_p3_15():
    f = CH / "ch_p3_15_das-andere-tanzlied.ptx"
    txt = f.read_text(encoding="utf-8")
    orig = txt
    # Verses v41..v63 = 23 segments
    vids = [f"ch-p3-15-v{41+i:02d}" for i in range(23)]
    for vid, body in zip(vids, DE_BELLS):
        txt = _set_lang_p(txt, vid, "de", body)
    for vid, body in zip(vids, FR_BELLS):
        txt = _set_lang_p(txt, vid, "fr", body)
    if txt != orig:
        f.write_text(txt, encoding="utf-8")
        print(f"ch-p3-15: bells stanza re-segmented across {len(vids)} verses (DE+FR)")
    else:
        print("ch-p3-15: already segmented — no change")


# ---- ch-p4-19: collapse v71/v72 into v71 ------------------------------------
P419_DE = (
    "Oh Mensch! Gieb Acht! Was spricht die tiefe Mitternacht? "
    "„Ich schlief, ich schlief—, Aus tiefem Traum bin ich erwacht:— "
    "Die Welt ist tief, Und tiefer als der Tag gedacht. "
    "Tief ist ihr Weh—, Lust—tiefer noch als Herzeleid: "
    "Weh spricht: Vergeh! Doch alle Lust will Ewigkeit "
    "will tiefe, tiefe Ewigkeit!“"
)
P419_EN = (
    "O man! Take heed! What saith deep midnight’s voice indeed? "
    "“I slept my sleep—, “From deepest dream I’ve woke, and plead:— "
    "“The world is deep, “And deeper than the day could read. "
    "“Deep is its woe—, “Joy—deeper still than grief can be: "
    "“Woe saith: Hence! Go! “But joys all want eternity—, "
    "“—Want deep, profound eternity!”"
)
P419_FR = (
    "O homme! Prends garde! Que dit minuit profond? "
    "« J'ai dormi, j'ai dormi —, d'un rêve profond je me suis éveillé : — "
    "Le monde est profond, et plus profond que ne pensait le jour. "
    "Profonde est sa douleur —, la joie — plus profonde que l'affliction : "
    "la douleur dit : Passe et finis! mais toute joie veut l'éternité —, "
    "— veut la profonde éternité! »"
)
P419_ES = (
    "¡Oh hombre! ¡Presta atención! ¿Qué dice la profunda medianoche? "
    "«Yo dormía, dormía—, De un profundo soñar me he despertado:— "
    "El mundo es profundo, Y más profundo de lo que el día ha pensado. "
    "Profundo es su dolor—, El placer—es aún más profundo que el sufrimiento: "
    "El dolor dice: ¡Pasa! Mas todo placer quiere eternidad—, "
    "—¡quiere profunda, profunda eternidad!»"
)


def fix_p4_19():
    f = CH / "ch_p4_19_das-nachtwandler-lied.ptx"
    txt = f.read_text(encoding="utf-8")
    orig = txt

    # 1) overwrite v71 in all 4 langs with the full stanza
    for lang, body in (("de", P419_DE), ("en", P419_EN),
                       ("fr", P419_FR), ("es", P419_ES)):
        txt = _set_lang_p(txt, "ch-p4-19-v71", lang, body)

    # 2) remove the v72 paragraphs block entirely (its content is now in v71)
    v72_re = re.compile(
        r'\n\s*<paragraphs xml:id="ch-p4-19-v72">.*?</paragraphs>\s*',
        re.DOTALL,
    )
    txt2 = v72_re.sub("\n", txt)

    if txt2 != orig:
        f.write_text(txt2, encoding="utf-8")
        removed_v72 = (txt != txt2)
        print(f"ch-p4-19: consolidated closing reprise into v71"
              + (" (removed v72)" if removed_v72 else ""))
    else:
        print("ch-p4-19: already consolidated — no change")


def main():
    fix_p3_15()
    fix_p4_19()


if __name__ == "__main__":
    main()
