# Senior-editor diagnostic pass — Zarathustra Talmudische Ausgabe

Companion to the auto-generated `verse-audit.md`. Diagnostic only; no
fixes applied. Source: `/Volumes/X10 Pro/Zarathustra/zarathustra-pt/`,
deploy: https://zarathustra-talmudisch.netlify.app/.

## Summary

- **81 chapters** total (Vorrede + 80 numbered chapters).
- **3 522 verses** total across all chapters.
- **74/80 numbered chapters** have at least one verse with a missing or
  empty language paragraph (only 7 chapter files are clean).
- **593 verses** out of 3 522 are missing at least one of the four
  language paragraphs entirely (or have it present-but-empty).
  - Missing by language: **es = 416**, **fr = 265**, **de = 57**,
    **en = 17**.
- **461 commentary notes** across 14 streams.
  - **140** carry `_audit_flag: "weak"`; **167** scored `1` in
    `audit.json`. Only **72** of those overlap — the two records are
    **out of sync**.
- All deployed URLs return HTTP 200, the deployed `talmud.js` is
  byte-identical to the source `web/talmud.js`, and the deployed
  `commentary.json`, `chapter-nav.json`, and `ch_vorrede.ptx`
  md5-match their source counterparts.

## Bugs found (broken functionality)

### bug-1 · Hardcoded `§ 1` in the active-section breadcrumb

`web/talmud.js:505-506` always builds the right-most crumb as
`§ 1 · ${verses[idx].title}` regardless of which chapter is loaded.
Navigating to `?ch=ch-p2-12` shows the literal string `§ 1 · v10`. The
active section title is *Von der Selbst-Überwindung*, not "§ 1".
Reproduce: load any non-Vorrede chapter and observe the third crumb.
Suggested fix: drop the `§ 1` prefix outside Vorrede, or replace with
`state.navEntry?.idx` / chapter title.

### bug-2 · Verse-title rendering of `vNN` is uninformative

In the numbered chapters, each verse's `<title>` is the bare id like
`v01`, which is what `renderCenter()` puts into the `verse-mark` span
and the active-section breadcrumb. The legacy Vorrede file uses richly
titled verses such as `v.7 · In die Tiefe steigen`. Result: only the
Vorrede has a useful per-verse label; the other 80 chapters show
`v01`, `v02`, …. Not strictly a bug, but it neuters the breadcrumb
feature.

### bug-3 · `_audit_flag` is out of sync with `audit.json`

- 85 entries in `audit.json` with `score == 1` have **no** `_audit_flag:
  weak` on the corresponding commentary note (so they render at full
  opacity even though the LLM said they were poor fits). Examples:
  `(deleuze, ch-p1-07-v23)`, `(klossowski, ch-p1-16-v05)`,
  `(sanchez-meca, ch-p1-10-v21)`, `(new-cambridge, ch-p1-03-v18)`.
- 54 notes carry `_audit_flag: weak` but are **missing entirely** from
  `audit.json`. Another 14 are flagged weak but `audit.json` scored
  them 2 or 3. The flag pipeline needs to be re-run from the current
  audit.

### bug-4 · `lang=de` silently falls back to `lang=en`

`web/talmud.js:14` whitelists only `["en","fr","es"]`. Hitting
`?lang=de` delivers EN without telling the user. The lang-toggle echos
`de` back, so the active tab indicator can be wrong. Either explicitly
redirect, or accept `de` and hide the centre-right translation pane.

### Non-bug verifications

- About link (`ⓘ` → `/about.html`) returns 200 (7398 B).
- TOC drawer lists 81 entries in `chapter-nav.json`, grouped by part.
- Prev/Next on first chapter shows "Anfang" disabled; on last chapter
  shows "Ende" disabled — correct.
- Deep-linking by hash (e.g. `…#ch-p2-12-v10`) is implemented at
  `talmud.js:131-134` and works.
- The deployed `talmud.js` md5-matches `web/talmud.js`.
- `style.css:278-280` sets `.verse .de em { color: inherit; }` — the
  red-italic `<em>` bug is **gone**, both in source and deploy.
- No leftover XML escapes (`&amp;`, `&quot;`, `&#`, `&lt;`, `&gt;`)
  found in either commentary.json or any chapter `.ptx` file.

## Translation issues (per verse)

### Verses where the German paragraph is reduced to a fragment (28 cases)

DE source has been split too aggressively along em-dashes and quotation
marks. Other languages keep the verse intact. Complete list:

| Chapter | Verse | DE content | Other-lang length |
|---|---|---|---|
| ch-p2-21 | v06 | `"Und"` | ~192 chars |
| ch-p3-01 | v34 | `"Die"` | ~150 |
| ch-p3-04 | v30 | `"Ein"` | ~186 |
| ch-p3-05 | v68 | `"Aber"` | ~146 |
| ch-p3-05 | v69 | `"Und"` | ~141 |
| ch-p3-06 | v28 | `"Und"` | ~117 |
| ch-p3-06 | v34 | `"Wie"` | ~149 |
| ch-p3-08 | v34 | `"„"` | ~150 |
| ch-p3-12 | v59 | `"„"` | ~139 |
| ch-p3-12 | v146 | `"Und"` | ~187 |
| ch-p3-12 | v166 | `"Geht"` | ~141 |
| ch-p3-12 | v171 | `"Wenn"` | ~163 |
| ch-p3-12 | v202 | `"Den"` | ~116 |
| ch-p3-15 | v38 | `"Du"` | ~56 |
| ch-p4-02 | v17 | `"Höre"` | ~125 |
| ch-p4-03 | v12 | `"Wir"` | ~135 |
| ch-p4-04 | v30 | `"Dass"` | ~217 |
| ch-p4-06 | v09 | `"„"` | ~193 |
| ch-p4-07 | v10 | `"Du"` | ~144 |
| ch-p4-09 | v24 | `"Habe"` | ~65 |
| ch-p4-11 | v48 | `"—"` | ~287 |
| ch-p4-12 | v10 | `"—"` | ~251 |
| ch-p4-14 | v17 | `"„Der"` | ~394 |
| ch-p4-15 | v11 | `"Wir"` | ~172 |
| ch-p4-17 | v14 | `"Der"` | ~158 |
| ch-p4-18 | v28 | `"Ob"` | ~127 |
| ch-p4-19 | v05 | `"„War"` | ~63 |
| ch-p4-19 | v63 | `"—"` | ~222 |

### Catastrophic mis-segmentation: ch-p3-15 vv38-v51 and ch-p4-19

In *Das andere Tanzlied* (ch-p3-15, the midnight-stroll Twelve Bells):
**v41 DE** contains the *entire* twelve-line stanza glued together
("Eins! Oh Mensch! Gieb Acht! Zwei! …"), while **v42-v51 DE are
empty**. The **FR** is identical-but-shifted: the whole stanza arrives
glued at **v43** and v41/v42/v44/v45/… are blank. Only the **EN** and
**ES** streams produce one verse per bell+line pair. So this chapter
is unreadable in DE-and-FR view from v41 onward. *Das Nachtwandler-Lied*
(ch-p4-19) shows the same pattern around v05 and v60-v63.

### Off-by-one shifts (FR/ES paragraph misaligned with DE/EN)

54 candidate off-by-one shifts where the FR or ES of verse N has length
and content that better match verse N-1's DE. Top-confidence examples:

- **ch-p1-01-v02 fr**: FR text **missing**; ch-p1-01-v03 FR ("Il est
  maint fardeau pesant…") actually translates **v02 DE** ("Vieles
  Schwere giebt es dem Geiste…"), not v03 DE ("Was ist schwer?"). FR is
  shifted forward by one from v02 on.
- **ch-p1-02-v24 es**: ES missing; v25 ES translates v24 DE.
- **ch-p1-07-v13 es**: ES missing; v14 ES too short for v14 DE.
- **ch-p1-10-v07 es** ("Euren Feind sollt ihr suchen…"): ES missing,
  v08 ES carries v07's content.
- **ch-p1-14-v19 es**, **ch-p1-15-v04 es**, **ch-p1-20-v05 fr**,
  **ch-p1-20-v06 es**, **ch-p2-01-v01 es** (also has chapter-title
  contamination), **ch-p2-02-v17 es**, **ch-p2-04-v29 es**,
  **ch-p2-05-v24 es**, **ch-p2-06-v22 es**, **ch-p2-11-v01 es**,
  **ch-p2-18-v03 es**, **ch-p2-18-v26 es**, **ch-p2-19-v31 es**,
  **ch-p2-20-v39 es**, **ch-p2-20-v47 es**, **ch-p2-22-v05 es**,
  **ch-p3-02-v08 fr**, **ch-p3-04-v17 es**, **ch-p3-05-v07 es**,
  **ch-p3-08-v31 es**, **ch-p3-10-v02 es**, … (54 total).

### OCR contamination: chapter title swallowed into v01 ES (10 cases)

The Sánchez Pascual ES v01 was scraped together with the chapter
heading, then re-OCR'd. Result: v01 ES starts with the chapter title,
often followed by the first letter of the next sentence stranded:

- ch-p1-05 v01 es: `"De las alegrias y de las pasiones H ermano mío…"`
  (note `H ermano` and missing `í` in `alegrías`).
- ch-p1-15 v01 es: `"De las mil metas y de la «Única» meta M uchos
  países…"`.
- ch-p2-07 v01 es: `"De las tarántula s M ira…"` (stray `s`, `M ira`).
- ch-p2-12 v01 es: `"De la superación de si mism o V oluntad de
  verdad»…"` (missing tilde on `sí mismo`).
- ch-p3-05 v01 es: `"De la virtud empequeñecedora Cuando Zaratustra…"`.
- ch-p4-04 v01 es: `"La sanguijuela Y Zaratustra…"`.
- ch-p4-12 v01 es: `"La Cena E n este punto…"`.
- **ch-p2-01 v01 es** is the worst: `"El niño del espejo Z aratustra
  volvió a continuación a las mont…"` — section-title and verse merged
  into one 416-char paragraph containing *both* DE-aligned ("Hierauf
  gieng Zarathustra wieder zurück…") **and** the next paragraph.

### Soft-hyphen and inline page-number contamination in ES

Sánchez Pascual ES carries Unicode soft hyphen `­` (U+00AD) in 21
verses where line-wrap hyphenation from the source PDF was preserved.
Examples:

- ch-p1-22 v13 es: `…degeneración? Y siempre adivinamos de­ -`
- ch-p2-14 v09 es: `…reconoce­ -`
- ch-p2-20 v29 es: `…aversión de la vo­ ,, luntad contra el tiempo y
  su "Fue . "` (also stray `,,`).
- ch-p3-12 v07/v175/v185, ch-p3-13 v66, ch-p3-14 v30, ch-p4-03 v18,
  ch-p4-07 v32, ch-p4-09 v28, ch-p4-18 v22.

Inline footnote-marker page numbers from the print edition appear in
14 ES verses:

- ch-p1-22 v58 es: `… (I, p. 127)`
- ch-p2-10 v10 es: `…es "el señor de este mundo »191 -`
- ch-p2-19 v03 es: `…todo fue!"248`
- ch-p2-20 v34 es: `…todo es digno de perecer! 259`
- ch-p3-09 v13 es: `…tomar?"338`
- ch-p3-12 v144 es: `…parásito/393`
- ch-p4-02 v13 es: `…hombre alegre!"453`
- ch-p4-03 v27 es: `…(I-A. 460)`
- ch-p4-07 v24 es: `"…la compasión es importuna"489`
- ch-p4-07 v31 es: `…enseñó "yo - soy la verdad"490`
- ch-p4-15 v19 es: `…el animal interior"543`
- ch-p4-18 v07 es: `…Dios es espíritu"570`
- plus ch-p3-04 v21, ch-p2-20 v41.

OCR'd footnote markers that should have been stripped (the SP-Notes
stream carries the actual footnote text).

### Bottom-heavy chapters (systemic alignment problems)

| Chapter | # verses w/ a missing/empty lang | Notes |
|---|---|---|
| ch-p3-12 (Von alten und neuen Tafeln) | 81 | long "tablets" chapter |
| ch-p3-15 (Das andere Tanzlied) | 52 | midnight stanza splitting |
| ch-p4-19 (Das Nachtwandler-Lied) | 51 | same midnight stanza |
| ch-p3-16 (Die sieben Siegel) | 30 | refrain-heavy |
| ch-p4-20 (Das Zeichen) | 26 | final chapter |
| ch-p2-09 (Das Nachtlied) | 25 | poem-form |
| ch-p4-11 (Die Begrüssung) | 22 | DE em-dash splitting |
| ch-p2-22 (Die stillste Stunde) | 21 | quote-block heavy |

## Commentary mis-attributions (notes that don't fit the verse)

From `audit.json` `score == 1`. Most-clearly-bad samples:

- **ch-p0-00 v02 [lampert]**: `"Lampert: the address to the sun is the
  first of three sun-prayers that frame the work…"` — structural
  generalisation.
- **ch-p0-00 v12 [lampert]**: `"the entire Vorrede §1 is, in
  retrospect, the announcement of a tragic action…"` — broad
  chapter-context.
- **ch-p1-05-v21 [klossowski]**: `"« Man as a plurality of 'wills to
  power'…"` — generic Nietzsche metaphysics; verse is about virtues
  becoming intoxicating.
- **ch-p1-15-v14 [klossowski]** (two notes both flagged): general
  remarks on Nietzsche's "no concern for the fate of humanity"; verse
  is about the genesis of values.
- **ch-p1-20-v05 [deleuze]**: `"115. WP, II, 51: further development of
  the image of engagement and the nuptial ring."` — bare cross-ref.
- **ch-p1-20-v08 [klossowski]**: generic impulse-rhythm essay.
- **ch-p1-22-v56 [klossowski]**: `"Digression: The Eternal
  Recurrence…"` — Klossowski's essay-style aside attached to "return"
  by keyword.
- **ch-p2-04-v32 [klossowski]**: `"to teach and to learn — is the
  inverse of the soul's tonality…"` — fails to engage the verse's fire
  imagery.
- **ch-p2-07-v30 [klossowski]** (two): general ressentiment essays.
- **ch-p2-11-v19 [klossowski]**: abstract "God as maximum-state".
- **ch-p2-12-v23 [klossowski]** (two): dense aside on power and
  eternal return, attached to a verse on Wille zur Wahrheit.
- **ch-p2-12-v34 [deleuze]**: `"108. When Nietzsche spoke of the
  'aesthetic justification of existence,' on the contrary…"`.
- **ch-p2-14-v03 [deleuze]**: `"94. Two texts revisit and explain the
  themes of burden and desert: Z, II, 'On the Land of Culture'…"` —
  attached by keyword "land of culture".
- **ch-p2-18-v02 [klossowski]**: generic philological observation.
- **ch-p3-04-v29 [klossowski]**: `"« What is hereditary is not the
  illness, but the morbid state…"` — uses verse's "illness" keyword.
- **ch-p3-06-v33 [klossowski]**: general self-sovereignty essay.
- **ch-p3-10-v48 [klossowski]**: paragraph-fragment from a longer
  Klossowski piece.
- **ch-p3-12-v08 [klossowski]**: generic meaning/purpose essay.
- **ch-p3-14-v12 [klossowski]**: `"« What greater joy, O Wilhelm…"`
  — letter to friend Wilhelm; biographical anecdote attached by tone.
- **ch-p3-16-v51 [sanchez-meca]**: `"79 NF, verano-otoño de 1884, 27
  (40); MBM, aforismo 262."` — bare citation with no analysis.
- **ch-p4-04-v21 [klossowski]**: general "great men" essay.
- **ch-p4-07-v04 [sanchez-meca]**: introductory paragraph on
  Nietzsche's style, mis-attached to a verse about Zarathustra
  confronting the murderer of God.
- **ch-p4-12-v17 [klossowski]**: `"« When he felt most healthy and
  robust…"` — biographical aside; "healthy" keyword.
- **ch-p4-15-v16 [klossowski]**: general illness/health note.
- **ch-p4-19-v07 [klossowski]**: `"« Only from now on does it become
  clear to man that music is a semiological language of affects…"` —
  music-theory aside attached to a sleepwalker-song verse.
- **ch-p4-20-v14 [klossowski]**: `"It was not the understanding that
  overcame the centrifugal forces…"` — "centrifugal" keyword.

Pattern: `klossowski` and `deleuze` dominate weak attributions. The
semantic embedding picked up surface keywords (centre, periphery,
return, power, ressentiment) and attached entire essays.

`sanchez-meca` is the worst: **30 of 39 notes flagged weak (77%)**.
Reads like book-length scholia that don't pin to individual verses.
Consider thinning to the 9 strong notes, or attaching at chapter level.

## Translation quality issues in commentary text

### Klossowski FR (origin) carries OCR damage that leaked through

Selected FR text in `klossowski` has visible breakages — split words,
stray letters, double-OCR'd ligatures:

- ch-p1-03-v18 fr: `"… le corps en tan t qu'une propriété du moi…"`
  (should be `"en tant qu'une"`); `"il n 'est plus le corps"`.
- ch-p1-05-v21 fr: `"L'homme en tan t qu'une pluralité"` ×3 in note.
- ch-p2-02-v09 fr: `"…nous présupposons de 1' « esprit »…"` — `1'`
  should be `l'`.
- ch-p2-06-v26 fr: `"Le soleil d'août est sur nous, Vannée fuit, w n
  plus grand silence…"` — `Vannée` → `l'année`; `w n` → `un`.
- ch-p2-08-v25 fr: `"D 'une part Youbli et Yinconscience…"` — `Youbli`
  → `l'oubli`; `Yinconscience` → `l'inconscience`.
- ch-p2-19-v19 fr: `"Plus rien ! Alangui — m a main tremble…"` — `m a
  main` → `ma main`.
- ch-p2-20-v46 fr: `"Explicitation scientifique de VÉternel Retour 167
  l'existence)…"` — `VÉternel` → `l'Éternel`; `167` is a stranded
  page number; opening paren unmatched.
- ch-p3-03-v17 fr: repeated `letter space apostrophe` runs.
- ch-p3-12-v20 fr, ch-p4-04-v18 fr, ch-p4-07-v04 fr, ch-p4-08-v05 fr,
  ch-p4-19-v07 fr — same family.
- **Total: 50 FR origin notes in `klossowski` carry visible OCR damage.**

Gemini-Flash *cleaned up* most of this damage on the EN/ES side — the
EN/ES versions read fluently (e.g. EN: `"the year flees, a greater
silence, a greater peace"`; ES: `"el año huye, un mayor silencio, una
mayor paz"`). So FR readers actually get the *worst* version of
Klossowski. **Action:** treat EN/ES as the cleaned ground truth and
back-port a hand-cleaned FR.

### Inline page-numbers and footnote markers in Klossowski / Sánchez Meca

Footnote anchors `167`, `144`, `262`, etc. carried over from print
editions into all three language renderings. `enrichNote()` in
talmud.js already strips `p. NNN` references but **not** free-standing
trailing footnote numbers.

### Note-level `_origin` field is never set

Task brief mentions a note-level `_origin` flag. Stream metadata has
`_origin: "fr"` / `"es"`, but **zero notes** carry `_origin` at the note
level. The renderer (`talmud.js:430`) reads `stream._origin`, which is
correct — but the documentation may need an update.

## Patterns observed (systematic vs one-offs)

1. **Verse mis-segmentation across languages** is the dominant problem.
   The four source corpora used different paragraph boundaries (Leipzig
   DE em-dashes split into multiple verses; Common 1909 EN keeps blocks;
   Henri Albert FR keeps blocks; Sánchez Pascual ES sometimes follows
   DE, sometimes FR). 593 verses affected.

2. **OCR contamination is one-sided**: only the Spanish (Sánchez
   Pascual) carries soft hyphens, inline footnote-marker page numbers,
   missing accents (`alegrias`, `si mismo`), and stranded title letters
   (`H ermano`). The EN/FR/DE Urtexts are clean.

3. **DE Urtext is intermittently truncated** at quotation-mark or
   em-dash boundaries: 28 chapters have at least one DE paragraph
   reduced to a 1-4 char fragment. Part III and Part IV are worst.

4. **Vorrede has two source files** (`ch_vorrede.ptx` with 12
   hand-tuned verses, `ch_p0_00_zarathustra-s-vorrede.ptx` with 163
   auto-generated verses). The deployed UI **always** loads the
   12-verse legacy file when you click "Vorrede". No notes target the
   163-verse file. Either delete the long file or wire it up.

5. **Commentary attribution quality is heavily stream-dependent**:
   philology (0% weak), Higgins/Rosen/Gooding-Williams/crossref/Loeb
   (0%), Sánchez-Pascual-notes (19%), Deleuze (29%), sp-introduction
   (33%), New Cambridge (34%), Lampert (40%), Klossowski (40%),
   **Sánchez-Meca (77%)**. Two streams need curation: Sánchez-Meca and
   Klossowski (the latter also has the OCR damage).

6. **Audit-flag pipeline is stale**: 85 LLM-weak notes are not flagged,
   54 flagged notes are not in the audit. Re-running the flagger from
   the current `audit.json` would dim correctly.

## Recommended next actions (ranked by impact)

1. **Re-derive verse alignment across DE/EN/FR/ES.** Many chapters
   need a manual segmentation pass. Without this, 1/6 of all verses
   are broken in at least one language. Start with the worst:
   ch-p3-15, ch-p4-19, ch-p3-12, ch-p2-09, ch-p4-20, ch-p4-11.

2. **Repair the 28 truncated-to-fragment DE verses.** Caused by
   over-aggressive splitting on `—` / `„`; re-fetch the Leipzig source
   and merge them with the next paragraph.

3. **Fix the 10 chapter-title-into-v01-ES contaminations** plus the 14
   stranded-page-number ES verses and the 21 soft-hyphen ES verses.
   All are easy regex strip jobs once identified.

4. **Fix bug-1 (hardcoded `§ 1` breadcrumb).** Trivial JS one-liner
   at `web/talmud.js:505-506`.

5. **Re-sync `_audit_flag` from current `audit.json`.** Single-script
   pass: set `_audit_flag = "weak"` iff `audit.json` scored it 1,
   otherwise delete the flag. Currently 140 are flagged; should be
   167, with 85 currently missing and 54+14 to remove.

6. **Curate `sanchez-meca` stream**: 30/39 are weak. Either prune to
   the 9 strong notes, or re-attribute at chapter level.

7. **Re-OCR or hand-clean the Klossowski FR source**, then re-run the
   FR→EN/ES translation. EN/ES already look cleaner than the FR
   origin; backport that quality to FR.

8. **Strip inline footnote markers** (`\b\d{2,4}\b` adjacent to closing
   quotes) from commentary bodies. ~30 occurrences across all streams.

9. **Decide on `ch_p0_00_zarathustra-s-vorrede.ptx`**: retire the
   163-verse auto file (currently dead code on deploy) or migrate the
   12-verse legacy notes to it.

10. **Improve verse-mark titles** (bug-2): auto-generate a one-phrase
    label from the DE text, or hide the bare verse-id when no title
    is present.

11. **Either accept `lang=de` or block it** (bug-4).
