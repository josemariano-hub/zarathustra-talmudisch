# Zarathustra verse audit

Generated: 2026-05-19 20:21:44
Scope: every verse of every chapter (81 chapters, 3510 verses parsed) — no sampling.

## 0. Executive summary

| Check | Result |
|---|---|
| Chapters parsed | 81 / 81 (XML errors: 0) |
| Verses parsed | 3510 |
| LaBSE DE↔target cosine < 0.40 (likely misalignment) | **330** flags |
| Surface / OCR / punctuation artifacts | 1136 verse-language pairs |
| Empty target while DE present | **667** verse-language pairs |
| Length-ratio out of [0.40, 2.50] | 289 |
| Commentary notes total | 461 |
| Notes with audit score=0 still in commentary | 17 |
| Notes with no audit.json entry | 80 |
| Notes flagged `_audit_flag: weak` | 140 |
| Render artifacts in note bodies | 10 |
| Live site top pages | 200 OK (/, /about.html, /talmud.html?ch=vorrede) |
| Live site talmud.html for 81 chapters | 81 / 81 = 200 |
| Live site /source/*.ptx for 81 chapters | 81 / 81 = 200 |
| Sample deeplinks | 5 / 5 = 200 |

### Critical findings (in priority order)

1. **Vorrede (ch-p0-00) DE↔EN/FR/ES verse alignment is broken.** DE has 162 verses, EN/FR/ES have 163. LaBSE flags 224 verses in this chapter alone with avg cosine ≈ 0.27 (EN 90 flags, FR 33, ES 101). Manual spot-check confirms: in DE v157 = "Als Zarathustra diess gesagt hatte…" but in EN v157 = "More dangerous have I found it…" (DE v156). The translations are real, just attached to wrong verse IDs. **Likely cause: one extra blank or misnumbered `<paragraphs>` element early in the chapter.**

2. **Systemic missing Spanish translations.** 414 ES verses are empty while DE is present. Worst offenders:
   - ch-p3-12: ES missing 48/234 (20%)
   - ch-p2-09: ES missing 25/29 (86%)
   - ch-p4-19: ES missing 19/72 (26%)
   - ch-p3-16: ES missing 13/55 (23%)
   - ch-p2-22: ES missing 12/47 (25%)
   - ch-p3-13: ES missing 12/71 (16%)
   - ch-p4-05: ES missing 11/49 (22%)
   - ch-p4-06: ES missing 11/51 (21%)
   - ch-p3-10: ES missing 10/51 (19%)
   - ch-p4-13: ES missing 10/108 (9%)
   - ch-p2-18: ES missing 9/43 (20%)
   - ch-p3-02: ES missing 9/57 (15%)

3. **`ch-p2-09` has only 4 of 29 Spanish verses populated** — essentially untranslated chapter on the Spanish reader.

4. **French and Spanish missing across many chapters** — FR missing 200+ verses across the book (worst: ch-p3-12 29 missing, ch-p4-19 29 missing, ch-p4-11 13 missing, ch-p4-20 missing 21 of 26). ES missing ~280 verses book-wide.

5. **17 commentary notes with audit verdict score=0 (not relevant) are still served** in commentary.json — they should be dropped or reassigned.

6. **80 commentary notes have no audit.json entry at all** — newly added since last audit; need first-pass review.

7. **140 notes are explicitly `_audit_flag: weak`** — concentrated in Klossowski/Deleuze streams; either improve the targeting or downgrade their visibility.

8. **OCR residue in Spanish text**: notable patterns — `<despre-cio'` (broken «desprecio»), `despierto1º` (1º suffix instead of "1"), `dormir4°`, etc. — likely originating from a single OCR'd Sánchez-Pascual edition.

9. **Trailing em-dash artifacts (`—` / ` - `)** appear in ~150 verses across DE/EN/FR/ES, especially around verse endings of paragraphs where Nietzsche's original em-dash was preserved. Many are legitimate stylistic dashes (e.g. v107 last-men quote); a smaller subset are clear truncation artifacts (lone " -" with no leading content). Recommend manual triage of those flagged at end of verse without matching DE punctuation.

10. **All live site endpoints return HTTP 200** — no infrastructure failures.

### Worst 15 LaBSE misalignments (most likely wrong-verse-pairings)
- ch-p0-00-v158 [en] sim=0.024
  - DE: Möchte ich klüger sein! Möchte ich klug von Grund aus sein, gleich meiner Schlan
  - EN: When Zarathustra had said this, he remembered the words of the saint in the fore
- ch-p3-05-v72 [es] sim=0.039
  - DE: Also sprach Zarathustra.
  - ES: En el monte de los olivos
- ch-p0-00-v34 [en] sim=0.073
  - DE: Ich lehre euch den Übermenschen. Der Mensch ist Etwas, das überwunden werden sol
  - EN: When Zarathustra arrived at the nearest town which adjoineth the forest, he foun
- ch-p0-00-v34 [es] sim=0.077
  - DE: Ich lehre euch den Übermenschen. Der Mensch ist Etwas, das überwunden werden sol
  - ES: Mas cuando Zaratustra estuvo solo, habló así a su corazón:
- ch-p0-00-v89 [es] sim=0.079
  - DE: Es ist an der Zeit, dass der Mensch sich sein Ziel stecke. Es ist an der Zeit, d
  - ES: YZaratustra habló así al pueblo:
- ch-p3-16-v52 [es] sim=0.088
  - DE: Zarathustra, Von den Mitleidigen
  - ES: ¡Ay de todos aquellos que aman y no tienen todavía una altura que esté por encim
- ch-p0-00-v146 [en] sim=0.093
  - DE: Und du, mein erster Gefährte, gehab dich wohl! Gut begrub ich dich in deinem hoh
  - EN: Fellow-creators, Zarathustra seeketh; fellow-reapers and fellow-rejoicers, Zarat
- ch-p0-00-v89 [en] sim=0.095
  - DE: Es ist an der Zeit, dass der Mensch sich sein Ziel stecke. Es ist an der Zeit, d
  - EN: And thus spake Zarathustra unto the people:
- ch-p0-00-v18 [en] sim=0.102
  - DE: Zarathustra antwortete: „Ich liebe die Menschen.“
  - EN: As in the sea hast thou lived in solitude, and it hath borne thee up. Alas, wilt
- ch-p0-00-v162 [fr] sim=0.104
  - DE: Die Reden Zarathustra's
  - FR: Et si ma sagesse m'abandonne un jour: - hélas, elle aime à s'envoler! - puisse d
- ch-p0-00-v100 [en] sim=0.105
  - DE: Ein wenig Gift ab und zu: das macht angenehme Träume. Und viel Gift zuletzt, zu 
  - EN: Turning ill and being distrustful, they consider sinful: they walk warily. He is
- ch-p0-00-v147 [fr] sim=0.112
  - DE: Aber ich scheide von dir, die Zeit ist um. Zwischen Morgenröthe und Morgenröthe 
  - FR: Des compagnons, voilà ce que cherche le créateur, de ceux qui savent aiguiser le
- ch-p0-00-v146 [es] sim=0.115
  - DE: Und du, mein erster Gefährte, gehab dich wohl! Gut begrub ich dich in deinem hoh
  - ES: Compañeros busca el creador, y colaboradores en la recolección: pues todo está e
- ch-p0-00-v60 [es] sim=0.115
  - DE: Zarathustra aber sahe das Volk an und wunderte sich. Dann sprach er also:
  - ES: ¿Dónde está el rayo que os lama con su lengua? ¿Dónde la demencia que habría que
- ch-p0-00-v107 [en] sim=0.119
  - DE: „Wir haben das Glück erfunden“—sagen die letzten Menschen und blinzeln—
  - EN: They have their little pleasures for the day, and their little pleasures for the

---

## 1. Translation-coherence defects (LaBSE DE-target cosine < 0.40)

ch-p0-00-v158 [en] sim=0.024 | possible misalignment | DE: 'Möchte ich klüger sein! Möchte ich klug von Grund aus sein, gleich meiner Schlan' | EN: 'When Zarathustra had said this, he remembered the words of the saint in the fore'
ch-p3-05-v72 [es] sim=0.039 | possible misalignment | DE: 'Also sprach Zarathustra.' | ES: 'En el monte de los olivos'
ch-p0-00-v34 [en] sim=0.073 | possible misalignment | DE: 'Ich lehre euch den Übermenschen. Der Mensch ist Etwas, das überwunden werden sol' | EN: 'When Zarathustra arrived at the nearest town which adjoineth the forest, he foun'
ch-p0-00-v34 [es] sim=0.077 | possible misalignment | DE: 'Ich lehre euch den Übermenschen. Der Mensch ist Etwas, das überwunden werden sol' | ES: 'Mas cuando Zaratustra estuvo solo, habló así a su corazón:'
ch-p0-00-v89 [es] sim=0.079 | possible misalignment | DE: 'Es ist an der Zeit, dass der Mensch sich sein Ziel stecke. Es ist an der Zeit, d' | ES: 'YZaratustra habló así al pueblo:'
ch-p3-16-v52 [es] sim=0.088 | possible misalignment | DE: 'Zarathustra, Von den Mitleidigen' | ES: '¡Ay de todos aquellos que aman y no tienen todavía una altura que esté por encim'
ch-p0-00-v146 [en] sim=0.093 | possible misalignment | DE: 'Und du, mein erster Gefährte, gehab dich wohl! Gut begrub ich dich in deinem hoh' | EN: 'Fellow-creators, Zarathustra seeketh; fellow-reapers and fellow-rejoicers, Zarat'
ch-p0-00-v89 [en] sim=0.095 | possible misalignment | DE: 'Es ist an der Zeit, dass der Mensch sich sein Ziel stecke. Es ist an der Zeit, d' | EN: 'And thus spake Zarathustra unto the people:'
ch-p0-00-v18 [en] sim=0.102 | possible misalignment | DE: 'Zarathustra antwortete: „Ich liebe die Menschen.“' | EN: 'As in the sea hast thou lived in solitude, and it hath borne thee up. Alas, wilt'
ch-p0-00-v162 [fr] sim=0.104 | possible misalignment | DE: "Die Reden Zarathustra's" | FR: "Et si ma sagesse m'abandonne un jour: - hélas, elle aime à s'envoler! - puisse d"
ch-p0-00-v100 [en] sim=0.105 | possible misalignment | DE: 'Ein wenig Gift ab und zu: das macht angenehme Träume. Und viel Gift zuletzt, zu ' | EN: 'Turning ill and being distrustful, they consider sinful: they walk warily. He is'
ch-p0-00-v147 [fr] sim=0.112 | possible misalignment | DE: 'Aber ich scheide von dir, die Zeit ist um. Zwischen Morgenröthe und Morgenröthe ' | FR: 'Des compagnons, voilà ce que cherche le créateur, de ceux qui savent aiguiser le'
ch-p0-00-v146 [es] sim=0.115 | possible misalignment | DE: 'Und du, mein erster Gefährte, gehab dich wohl! Gut begrub ich dich in deinem hoh' | ES: 'Compañeros busca el creador, y colaboradores en la recolección: pues todo está e'
ch-p0-00-v60 [es] sim=0.115 | possible misalignment | DE: 'Zarathustra aber sahe das Volk an und wunderte sich. Dann sprach er also:' | ES: '¿Dónde está el rayo que os lama con su lengua? ¿Dónde la demencia que habría que'
ch-p0-00-v107 [en] sim=0.119 | possible misalignment | DE: '„Wir haben das Glück erfunden“—sagen die letzten Menschen und blinzeln—' | EN: 'They have their little pleasures for the day, and their little pleasures for the'
ch-p0-00-v83 [en] sim=0.122 | possible misalignment | DE: 'Als Zarathustra diese Worte gesprochen hatte, sahe er wieder das Volk an und sch' | EN: 'Lo, I am a herald of the lightning, and a heavy drop out of the cloud: the light'
ch-p0-00-v36 [es] sim=0.122 | possible misalignment | DE: 'Was ist der Affe für den Menschen? Ein Gelächter oder eine schmerzliche Scham. U' | ES: 'Cuando Zaratustra llegó a la primera ciudad, situada al borde de los bosques, en'
ch-p0-00-v162 [es] sim=0.124 | possible misalignment | DE: "Die Reden Zarathustra's" | ES: 'Pero pido cosas imposibles: ¡por ello pido a mi orgullo que camine siempre junto'
ch-p0-00-v55 [en] sim=0.131 | possible misalignment | DE: 'Spracht ihr schon so? Schriet ihr schon so? Ach, dass ich euch schon so schreien' | EN: 'The hour when ye say: “What good is my pity! Is not pity the cross on which he i'
ch-p0-00-v146 [fr] sim=0.133 | possible misalignment | DE: 'Und du, mein erster Gefährte, gehab dich wohl! Gut begrub ich dich in deinem hoh' | FR: 'Des compagnons, voilà ce que cherche le créateur, des moissonneurs qui moissonne'
ch-p0-00-v26 [en] sim=0.135 | possible misalignment | DE: 'Unsre Schritte klingen ihnen zu einsam durch die Gassen. Und wie wenn sie Nachts' | EN: 'The saint laughed at Zarathustra, and spake thus: “Then see to it that they acce'
ch-p0-00-v61 [en] sim=0.136 | possible misalignment | DE: 'Der Mensch ist ein Seil, geknüpft zwischen Thier und Übermensch,—ein Seil über e' | EN: 'Zarathustra, however, looked at the people and wondered. Then he spake thus:'
ch-p0-00-v15 [en] sim=0.140 | possible misalignment | DE: 'Ja, ich erkenne Zarathustra. Rein ist sein Auge, und an seinem Munde birgt sich ' | EN: 'Then thou carriedst thine ashes into the mountains: wilt thou now carry thy fire'
ch-p4-08-v10 [es] sim=0.141 | possible misalignment | DE: '—seine grosse Trübsal: die aber heisst heute Ekel. Wer hat heute von Ekel nicht ' | ES: 'Mientras no nos convirtamos y nos hagamos como vacas no entraremos en el reino d'
ch-p4-17-v22 [es] sim=0.143 | possible misalignment | DE: '—Der Esel aber schrie dazu I-A.' | ES: '¡Amén! ¡Y alabanza y honor y sabiduría y gratitud y gloria y fortaleza a nuestro'
ch-p0-00-v100 [es] sim=0.144 | possible misalignment | DE: 'Ein wenig Gift ab und zu: das macht angenehme Träume. Und viel Gift zuletzt, zu ' | ES: 'Enfermar y desconfiar considéranlo pecaminoso: la gente camina con cuidado. ¡Un '
ch-p0-00-v26 [es] sim=0.145 | possible misalignment | DE: 'Unsre Schritte klingen ihnen zu einsam durch die Gassen. Und wie wenn sie Nachts' | ES: '«No, respondió Zaratustra, yo no doy limosnas. No soy bastante pobre para eso.»'
ch-p0-00-v147 [es] sim=0.147 | possible misalignment | DE: 'Aber ich scheide von dir, die Zeit ist um. Zwischen Morgenröthe und Morgenröthe ' | ES: 'Compañeros busca el creador, que sepan afilar sus hoces. Aniquiladores se los ll'
ch-p0-00-v15 [es] sim=0.151 | possible misalignment | DE: 'Ja, ich erkenne Zarathustra. Rein ist sein Auge, und an seinem Munde birgt sich ' | ES: 'Entonces llevabas tu ceniza a la montaña: ¿quieres hoy llevar tu fuego a los val'
ch-p3-08-v14 [fr] sim=0.152 | possible misalignment | DE: '—blase unter diese Blätter, oh Zarathustra: dass alles Welke schneller noch von ' | FR: '- 2.'
ch-p3-16-v02 [es] sim=0.152 | possible misalignment | DE: 'Wenn ich ein Wahrsager bin und voll jenes wahrsagerischen Geistes, der auf hohem' | ES: 'los siete senos (O : la canción «Si y Amém>)4 33'
ch-p0-00-v155 [en] sim=0.161 | possible misalignment | DE: 'Erkunden wollen sie, ob Zarathustra noch lebe. Wahrlich, lebe ich noch?' | EN: '“The proudest animal under the sun, and the wisest animal under the sun,—they ha'
ch-p0-00-v94 [en] sim=0.165 | possible misalignment | DE: 'Seht! Ich zeige euch den letzten Menschen.' | EN: 'Alas! There cometh the time when man will no longer give birth to any star. Alas'
ch-p0-00-v161 [fr] sim=0.167 | possible misalignment | DE: "—Also begann Zarathustra's Untergang." | FR: "Mais je demande l'impossible: je prie donc ma fierté d'accompagner toujours ma s"
ch-p0-00-v80 [es] sim=0.168 | possible misalignment | DE: 'Ich liebe Den, der freien Geistes und freien Herzes ist: so ist sein Kopf nur da' | ES: 'pasa así de buen grado por el puente.'
ch-p0-00-v150 [fr] sim=0.170 | possible misalignment | DE: 'Den Einsiedlern werde ich mein Lied singen und den Zweisiedlern; und wer noch Oh' | FR: 'Mais je me sépare de toi, te temps est passé. Entre deux aurores une nouvelle vé'
ch-p0-00-v84 [es] sim=0.173 | possible misalignment | DE: 'Muss man ihnen erst die Ohren zerschlagen, dass sie lernen, mit den Augen hören.' | ES: 'Mirad, yo soy un anunciador del rayo y una pesada gota que cae de la nube: mas e'
ch-p0-00-v104 [en] sim=0.173 | possible misalignment | DE: '„Ehemals war alle Welt irre“—sagen die Feinsten und blinzeln.' | EN: 'No shepherd, and one herd! Every one wanteth the same; every one is equal: he wh'
ch-p0-00-v97 [en] sim=0.176 | possible misalignment | DE: '„Wir haben das Glück erfunden“—sagen die letzten Menschen und blinzeln.' | EN: 'The earth hath then become small, and on it there hoppeth the last man who maket'
ch-p0-00-v39 [en] sim=0.182 | possible misalignment | DE: 'Seht, ich lehre euch den Übermenschen!' | EN: 'Even the wisest among you is only a disharmony and hybrid of plant and phantom. '
ch-p0-00-v122 [es] sim=0.182 | possible misalignment | DE: 'Ich will die Menschen den Sinn ihres Seins lehren: welcher ist der Übermensch, d' | ES: '¡En verdad, una hermosa pesca ha cobrado hoy Zaratustra! No ha pescado ni un sol'
ch-p3-05-v38 [es] sim=0.184 | possible misalignment | DE: 'Diess aber ist Feigheit: ob es schon „Tugend“ heisst.—' | ES: 'En el fondo lo que más quieren es simplemente una cosa: que nadie les haga daño.'
ch-p0-00-v109 [en] sim=0.184 | possible misalignment | DE: 'Sie verstehen mich nicht: ich bin nicht der Mund für diese Ohren.' | EN: 'And here ended the first discourse of Zarathustra, which is also called “The Pro'
ch-p0-00-v161 [es] sim=0.186 | possible misalignment | DE: "—Also begann Zarathustra's Untergang." | ES: '¡Ojalá fuera yo más inteligente! ¡Ojalá fuera yo inteligente de verdad, como mi '
ch-p0-00-v90 [en] sim=0.187 | possible misalignment | DE: 'Noch ist sein Boden dazu reich genug. Aber dieser Boden wird einst arm und zahm ' | EN: 'It is time for man to fix his goal. It is time for man to plant the germ of his '
ch-p0-00-v92 [en] sim=0.190 | possible misalignment | DE: 'Ich sage euch: man muss noch Chaos in sich haben, um einen tanzenden Stern gebär' | EN: 'Alas! there cometh the time when man will no longer launch the arrow of his long'
ch-p0-00-v62 [es] sim=0.191 | possible misalignment | DE: 'Ein gefährliches Hinüber, ein gefährliches Auf-dem-Wege, ein gefährliches Zurück' | ES: '«Ya hemos oído hablar bastante del volatinero; ahora, ¡veámoslo también!» Y todo'
ch-p2-22-v06 [es] sim=0.193 | possible misalignment | DE: 'Kennt ihr den Schrecken des Einschlafenden?—' | ES: 'Yesto es lo que ocurrió, - ¡pues tengo que deciros todo, para que vuestro corazó'
ch-p0-00-v136 [es] sim=0.194 | possible misalignment | DE: 'Sondern lebendige Gefährten brauche ich, die mir folgen, weil sie sich selber fo' | ES: 'Largo tiempo durmió Zaratustra, y no sólo la aurora pasó sobre su rostro, sino t'
ch-p0-00-v59 [es] sim=0.195 | possible misalignment | DE: 'Als Zarathustra so gesprochen hatte, schrie Einer aus dem Volke: „Wir hörten nun' | ES: '¡No vuestro pecado - vuestra moderación es lo que clama al cielo, vuestra mezqui'
ch-p0-00-v137 [en] sim=0.196 | possible misalignment | DE: 'Ein Licht gieng mir auf: nicht zum Volke rede Zarathustra, sondern zu Gefährten!' | EN: 'But I need living companions, who will follow me because they want to follow the'
ch-p0-00-v63 [es] sim=0.198 | possible misalignment | DE: 'Was gross ist am Menschen, das ist, dass er eine Brücke und kein Zweck ist: was ' | ES: 'Mas Zaratustra contempló al pueblo y se maravilló. Luego habló así:'
ch-p2-02-v13 [es] sim=0.201 | possible misalignment | DE: 'Wohl zog ich den Schluss; nun aber zieht er mich.—' | ES: 'Mas para revelaros totalmente mi corazón a vosotros, amigos: si hubiera dioses, '
ch-p0-00-v149 [fr] sim=0.205 | possible misalignment | DE: 'Den Schaffenden, den Erntenden, den Feiernden will ich mich zugesellen: den Rege' | FR: "Et toi, mon premier compagnon, repose en paix! Je t'ai bien enseveli dans ton ar"
ch-p0-00-v27 [en] sim=0.206 | possible misalignment | DE: 'Gehe nicht zu den Menschen und bleibe im Walde! Gehe lieber noch zu den Thieren!' | EN: 'The fall of our footsteps ringeth too hollow through their streets. And just as '
ch-p0-00-v27 [es] sim=0.206 | possible misalignment | DE: 'Gehe nicht zu den Menschen und bleibe im Walde! Gehe lieber noch zu den Thieren!' | ES: 'El santo se rió de Zaratustra y dijo: ¡Entonces cuida de que acepten tus tesoros'
ch-p0-00-v08 [fr] sim=0.210 | possible misalignment | DE: 'Ich muss, gleich dir, untergehen, wie die Menschen es nennen, zu denen ich hinab' | FR: 'Bénis-moi donc, oeil tranquille, qui peux voir sans envie un bonheur même sans m'
ch-p0-00-v59 [en] sim=0.211 | possible misalignment | DE: 'Als Zarathustra so gesprochen hatte, schrie Einer aus dem Volke: „Wir hörten nun' | EN: 'Lo, I teach you the Superman: he is that lightning, he is that frenzy!—'
ch-p4-14-v22 [es] sim=0.211 | possible misalignment | DE: 'Das, Das ist deine Seligkeit! Eines Panthers und Adlers Seligkeit! Eines Dichter' | ES: 'Entre rojos purpúreos:'
ch-p0-00-v150 [es] sim=0.212 | possible misalignment | DE: 'Den Einsiedlern werde ich mein Lied singen und den Zweisiedlern; und wer noch Oh' | ES: 'Pero me separo de ti, el tiempo ha pasado. Entre aurora y aurora ha venido a mí '
ch-p0-00-v92 [es] sim=0.212 | possible misalignment | DE: 'Ich sage euch: man muss noch Chaos in sich haben, um einen tanzenden Stern gebär' | ES: '¡Ay! ¡Llega el tiempo en que el hombre dejará de lanzar la flecha de su anhelo m'
ch-p0-00-v157 [es] sim=0.213 | possible misalignment | DE: 'Als Zarathustra diess gesagt hatte, gedachte er der Worte des Heiligen im Walde,' | ES: 'El animal más orgulloso debajo del sol, y el animal más inteligente debajo del s'
ch-p0-00-v113 [es] sim=0.213 | possible misalignment | DE: 'Da aber geschah Etwas, das jeden Mund stumm und jedes Auge starr machte. Inzwisc' | ES: 'Yahora me miran y se ríen: y mientras ríen, continúan odiándome. Hay hielo en su'
ch-p0-00-v58 [en] sim=0.214 | possible misalignment | DE: 'Seht, ich lehre euch den Übermenschen: der ist dieser Blitz, der ist dieser Wahn' | EN: 'Where is the lightning to lick you with its tongue? Where is the frenzy with whi'
ch-p4-01-v24 [fr] sim=0.214 | possible misalignment | DE: "Wie ferne mag solches „Ferne“ sein? was geht's mich an! Aber darum steht es mir " | FR: "Qui devra venir un jour et n'aura pas le droit de passer? Notre grand hasard, c'"
ch-p0-00-v39 [es] sim=0.215 | possible misalignment | DE: 'Seht, ich lehre euch den Übermenschen!' | ES: '¿Qué es el mono para el hombre? Una irrisión o una vergüenza dolorosa. Y justo e'
ch-p0-00-v159 [fr] sim=0.218 | possible misalignment | DE: 'Aber Unmögliches bitte ich da: so bitte ich denn meinen Stolz, dass er immer mit' | FR: 'Lorsque Zarathoustra eut ainsi parlé, il se souvint des paroles du saint dans la'
ch-p0-00-v148 [fr] sim=0.219 | possible misalignment | DE: 'Nicht Hirt soll ich sein, nicht Todtengräber. Nicht reden einmal will ich wieder' | FR: 'Des créateurs comme lui, voilà ce que cherche Zarathoustra, de ceux qui moissonn'
ch-p0-00-v148 [en] sim=0.219 | possible misalignment | DE: 'Nicht Hirt soll ich sein, nicht Todtengräber. Nicht reden einmal will ich wieder' | EN: 'But I part from thee; the time hath arrived. ‘Twixt rosy dawn and rosy dawn ther'
ch-p0-00-v62 [en] sim=0.220 | possible misalignment | DE: 'Ein gefährliches Hinüber, ein gefährliches Auf-dem-Wege, ein gefährliches Zurück' | EN: 'Man is a rope stretched between the animal and the Superman—a rope over an abyss'
ch-p0-00-v152 [es] sim=0.221 | possible misalignment | DE: 'Diess hatte Zarathustra zu seinem Herzen gesprochen, als die Sonne im Mittag sta' | ES: 'Alos creadores, a los cosechadores, a los que celebran fiestas quiero unirme: vo'
ch-p3-12-v41 [es] sim=0.224 | possible misalignment | DE: 'Also will es die Art edler Seelen: sie wollen Nichts umsonst haben, am wenigsten' | ES: 'El que no puede mandarse a sí mismo debe obedecer. ¡Y más de uno puede mandarse '
ch-p0-00-v102 [en] sim=0.227 | possible misalignment | DE: 'Man wird nicht mehr arm und reich: Beides ist zu beschwerlich. Wer will noch reg' | EN: 'One still worketh, for work is a pastime. But one is careful lest the pastime sh'
ch-p0-00-v149 [es] sim=0.227 | possible misalignment | DE: 'Den Schaffenden, den Erntenden, den Feiernden will ich mich zugesellen: den Rege' | ES: 'Ytú, primer compañero mío, ¡descansa en paz! Bien te he enterrado en tu árbol hu'
ch-p0-00-v135 [en] sim=0.228 | possible misalignment | DE: 'Ein Licht gieng mir auf: Gefährten brauche ich und lebendige,—nicht todte Gefähr' | EN: 'Long slept Zarathustra; and not only the rosy dawn passed over his head, but als'
ch-p0-00-v106 [en] sim=0.229 | possible misalignment | DE: 'Man hat sein Lüstchen für den Tag und sein Lüstchen für die Nacht: aber man ehrt' | EN: 'They are clever and know all that hath happened: so there is no end to their rai'
ch-p2-05-v25 [es] sim=0.229 | possible misalignment | DE: 'Mit ihrer Tugend wollen sie ihren Feinden die Augen auskratzen; und sie erheben ' | ES: '¡Ay, qué desagradablemente les sale de la boca la palabra «virtud»! Y cuando dic'
ch-p0-00-v147 [en] sim=0.230 | possible misalignment | DE: 'Aber ich scheide von dir, die Zeit ist um. Zwischen Morgenröthe und Morgenröthe ' | EN: 'And thou, my first companion, rest in peace! Well have I buried thee in thy holl'
ch-p0-00-v95 [en] sim=0.230 | possible misalignment | DE: '„Was ist Liebe? Was ist Schöpfung? Was ist Sehnsucht? Was ist Stern“—so fragt de' | EN: 'Lo! I show you THE LAST MAN.'
ch-p1-07-v14 [es] sim=0.231 | possible misalignment | DE: 'Muthig, unbekümmert, spöttisch, gewaltthätig—so will uns die Weisheit: sie ist e' | ES: '¿Quién de vosotros puede a la vez reír y estar elevado?'
ch-p2-12-v06 [fr] sim=0.231 | possible misalignment | DE: 'Die Unweisen freilich, das Volk,—die sind gleich dem Flusse, auf dem ein Nachen ' | FR: "Vous voulez créer un monde devant lequel vous puissiez vous agenouiller, c'est l"
ch-p0-00-v18 [es] sim=0.231 | possible misalignment | DE: 'Zarathustra antwortete: „Ich liebe die Menschen.“' | ES: 'En la soledad vivías como en el mar, y el mar te llevaba. Ay,'
ch-p0-00-v158 [es] sim=0.233 | possible misalignment | DE: 'Möchte ich klüger sein! Möchte ich klug von Grund aus sein, gleich meiner Schlan' | ES: 'Quieren averiguar si Zaratustra vive todavía. En verdad, ¿vivo yo todavía?'
ch-p0-00-v124 [en] sim=0.234 | possible misalignment | DE: "Dunkel ist die Nacht, dunkel sind die Wege Zarathustra's. Komm, du kalter und st" | EN: 'But still am I far from them, and my sense speaketh not unto their sense. To men'
ch-p4-19-v18 [es] sim=0.236 | possible misalignment | DE: 'Wehe mir! Wo ist die Zeit hin? Sank ich nicht in tiefe Brunnen? Die Welt schläft' | ES: '¡Oh hombre, presta atención!'
ch-p2-11-v02 [es] sim=0.236 | possible misalignment | DE: 'Also im Herzen beschliessend fuhr ich über das Meer.—' | ES: 'La canción de los sepukros A llí está la isla de los sepulcros, la silenciosa; a'
ch-p0-00-v109 [es] sim=0.238 | possible misalignment | DE: 'Sie verstehen mich nicht: ich bin nicht der Mund für diese Ohren.' | ES: 'Yaquí acabó el primer discurso de Zaratustra, llamado también «el prólogo»: pues'
ch-p0-00-v55 [es] sim=0.238 | possible misalignment | DE: 'Spracht ihr schon so? Schriet ihr schon so? Ach, dass ich euch schon so schreien' | ES: 'La hora en que digáis: «¡Qué importa mi virtud! Todavía no me ha puesto furioso.'
ch-p0-00-v152 [en] sim=0.238 | possible misalignment | DE: 'Diess hatte Zarathustra zu seinem Herzen gesprochen, als die Sonne im Mittag sta' | EN: 'I make for my goal, I follow my course; over the loitering and tardy will I leap'
ch-p3-08-v13 [es] sim=0.238 | possible misalignment | DE: 'Lass sie fahren und fallen, oh Zarathustra, und klage nicht! Lieber noch blase m' | ES: 'Si pudiesen de otro modo, entonces querrían también de otro modo. Las gentes de '
ch-p0-00-v23 [es] sim=0.240 | possible misalignment | DE: 'Und willst du ihnen geben, so gieb nicht mehr, als ein Almosen, und lass sie noc' | ES: 'Zaratustra respondió: «¡Qué dije amor! Lo que yo llevo a los hombres es un regal'
ch-p0-00-v155 [es] sim=0.240 | possible misalignment | DE: 'Erkunden wollen sie, ob Zarathustra noch lebe. Wahrlich, lebe ich noch?' | ES: 'Esto es lo que Zaratustra dijo a su corazón cuando el sol estaba en pleno mediod'
ch-p0-00-v65 [es] sim=0.242 | possible misalignment | DE: 'Ich liebe die grossen Verachtenden, weil sie die grossen Verehrenden sind und Pf' | ES: 'Un peligroso pasar al otro lado, un peligroso caminar, un peligroso mirar atrás,'
ch-p0-00-v154 [es] sim=0.243 | possible misalignment | DE: '„Das stolzeste Thier unter der Sonne und das klügste Thier unter der Sonne—sie s' | ES: 'Hacia mi meta quiero ir, yo continúo mi marcha; saltaré por encima de los indeci'
ch-p0-00-v141 [fr] sim=0.244 | possible misalignment | DE: 'Siehe die Gläubigen aller Glauben! Wen hassen sie am meisten? Den, der zerbricht' | FR: "C'est pour enlever beaucoup de brebis du troupeau que je suis venu. Le peuple et"
ch-p0-00-v154 [fr] sim=0.245 | possible misalignment | DE: '„Das stolzeste Thier unter der Sonne und das klügste Thier unter der Sonne—sie s' | FR: 'Zarathoustra avait dit cela à son coeur, alors que le soleil était à son midi: p'
ch-p0-00-v84 [en] sim=0.247 | possible misalignment | DE: 'Muss man ihnen erst die Ohren zerschlagen, dass sie lernen, mit den Augen hören.' | EN: 'When Zarathustra had spoken these words, he again looked at the people, and was '
ch-p0-00-v47 [en] sim=0.247 | possible misalignment | DE: 'Wahrlich, ein schmutziger Strom ist der Mensch. Man muss schon ein Meer sein, um' | EN: 'But ye, also, my brethren, tell me: What doth your body say about your soul? Is '
ch-p0-00-v121 [en] sim=0.248 | possible misalignment | DE: 'Unheimlich ist das menschliche Dasein und immer noch ohne Sinn: ein Possenreisse' | EN: 'Verily, a fine catch of fish hath Zarathustra made to-day! It is not a man he ha'
ch-p3-12-v185 [es] sim=0.248 | possible misalignment | DE: 'Wer über alte Ursprünge weise wurde, siehe, der wird zuletzt nach Quellen der Zu' | ES: 'No sólo a propagaros al mismo nivel, sino a propagaros h a \xad cia arriba - ¡a eso'
ch-p0-00-v119 [en] sim=0.248 | possible misalignment | DE: 'Inzwischen kam der Abend, und der Markt barg sich in Dunkelheit: da verlief sich' | EN: 'When Zarathustra had said this the dying one did not reply further; but he moved'
ch-p0-00-v98 [en] sim=0.248 | possible misalignment | DE: 'Sie haben die Gegenden verlassen, wo es hart war zu leben: denn man braucht Wärm' | EN: '“We have discovered happiness”—say the last men, and blink thereby.'
ch-p0-00-v138 [es] sim=0.249 | possible misalignment | DE: 'Viele wegzulocken von der Heerde—dazu kam ich. Zürnen soll mir Volk und Heerde: ' | ES: 'Compañeros de viaje vivos es lo que yo necesito, que me sigan porque quieren seg'
ch-p3-11-v37 [en] sim=0.250 | possible misalignment | DE: 'Wahrlich, ich lernte das Warten auch und von Grund aus,' | EN: 'Unhappy do I also call those who have ever to WAIT,—they are repugnant to my tas'
ch-p3-12-v86 [es] sim=0.250 | possible misalignment | DE: '—Denn Stehen-können ist ein Verdienst bei Höflingen; und alle Höflinge glauben, ' | ES: 'No el que vuestra estirpe se haya hecho cortesana en las cortes, y vosotros hayá'
ch-p0-00-v40 [es] sim=0.252 | possible misalignment | DE: 'Der Übermensch ist der Sinn der Erde. Euer Wille sage: der Übermensch sei der Si' | ES: 'Yel más sabio de vosotros es tan sólo un ser escindido, híbrido de planta y fant'
ch-p0-00-v40 [en] sim=0.252 | possible misalignment | DE: 'Der Übermensch ist der Sinn der Erde. Euer Wille sage: der Übermensch sei der Si' | EN: 'Lo, I teach you the Superman!'
ch-p2-09-v29 [es] sim=0.253 | possible misalignment | DE: 'Also sang Zarathustra.' | ES: 'La canción del baile'
ch-p0-00-v113 [en] sim=0.253 | possible misalignment | DE: 'Da aber geschah Etwas, das jeden Mund stumm und jedes Auge starr machte. Inzwisc' | EN: 'And now do they look at me and laugh: and while they laugh they hate me too. The'
ch-p0-00-v143 [es] sim=0.255 | possible misalignment | DE: 'Gefährten sucht der Schaffende, und Miterntende: denn Alles steht bei ihm reif z' | ES: '- pero ése es el creador.'
ch-p0-00-v159 [es] sim=0.255 | possible misalignment | DE: 'Aber Unmögliches bitte ich da: so bitte ich denn meinen Stolz, dass er immer mit' | ES: 'He encontrado más peligros entre los hombres que entre los animales, peligrosos '
ch-p0-00-v83 [es] sim=0.255 | possible misalignment | DE: 'Als Zarathustra diese Worte gesprochen hatte, sahe er wieder das Volk an und sch' | ES: 'Yo amo a todos aquellos que son como gotas pesadas que caen una a una de la oscu'
ch-p0-00-v102 [es] sim=0.256 | possible misalignment | DE: 'Man wird nicht mehr arm und reich: Beides ist zu beschwerlich. Wer will noch reg' | ES: 'La gente continúa trabajando, pues el trabajo es un entretenimiento. Mas procura'
ch-p0-00-v154 [en] sim=0.258 | possible misalignment | DE: '„Das stolzeste Thier unter der Sonne und das klügste Thier unter der Sonne—sie s' | EN: '“They are mine animals,” said Zarathustra, and rejoiced in his heart.'
ch-p2-09-v26 [es] sim=0.258 | possible misalignment | DE: 'Nacht ist es: nun bricht wie ein Born aus mir mein Verlangen,—nach Rede verlangt' | ES: 'Así cantó Zaratustra.'
ch-p1-02-v25 [es] sim=0.259 | possible misalignment | DE: 'Aber nicht lange mehr stehe ich dann: da liege ich schon.—' | ES: 'En verdad, con suave calzado viene a mí él, el más encantador de los ladrones, y'
ch-p0-00-v101 [en] sim=0.259 | possible misalignment | DE: 'Man arbeitet noch, denn Arbeit ist eine Unterhaltung. Aber man sorgt, dass die U' | EN: 'A little poison now and then: that maketh pleasant dreams. And much poison at la'
ch-p0-00-v161 [en] sim=0.261 | possible misalignment | DE: "—Also begann Zarathustra's Untergang." | EN: 'And if my wisdom should some day forsake me:—alas! it loveth to fly away!—may my'
ch-p0-00-v32 [es] sim=0.261 | possible misalignment | DE: 'Als Zarathustra aber allein war, sprach er also zu seinem Herzen: „Sollte es den' | ES: 'Cantando, llorando, riendo y gruñendo alabo al Dios que es mi Dios. Mas ¿qué reg'
ch-p3-12-v46 [es] sim=0.263 | possible misalignment | DE: 'Oh meine Brüder, wer ein Erstling ist, der wird immer geopfert. Nun aber sind wi' | ES: 'Goce e inocencia son, en efecto, las cosas más púdicas que existen: ninguna de l'
ch-p3-16-v02 [fr] sim=0.264 | possible misalignment | DE: 'Wenn ich ein Wahrsager bin und voll jenes wahrsagerischen Geistes, der auf hohem' | FR: "(ou: Le chant de L'Alpha et de L'Oméga)"
ch-p4-12-v16 [fr] sim=0.265 | possible misalignment | DE: 'Ich bin ein Gesetz nur für die Meinen, ich bin kein Gesetz für Alle. Wer aber zu' | FR: '"Sois de bonne humeur, répondit Zarathoustra, comme je suis de bonne humeur. Gar'
ch-p2-20-v48 [es] sim=0.266 | possible misalignment | DE: '„Es ist schwer, mit Menschen zu leben, weil Schweigen so schwer ist. Sonderlich ' | ES: '- En este momento de su discurso ocurrió que Zaratustra se detuvo de repente, y '
ch-p0-00-v99 [en] sim=0.266 | possible misalignment | DE: 'Krankwerden und Misstrauen-haben gilt ihnen sündhaft: man geht achtsam einher. E' | EN: 'They have left the regions where it is hard to live; for they need warmth. One s'
ch-p0-00-v25 [es] sim=0.267 | possible misalignment | DE: 'Der Heilige lachte über Zarathustra und sprach also: So sieh zu, dass sie deine ' | ES: '¡Y si quieres darles algo, no les des más que una limosna, y deja que además la '
ch-p0-00-v104 [es] sim=0.268 | possible misalignment | DE: '„Ehemals war alle Welt irre“—sagen die Feinsten und blinzeln.' | ES: '¡Ningún pastor y un solo rebaño! Todos quieren lo mismo, todos son iguales: quie'
ch-p4-20-v03 [fr] sim=0.268 | possible misalignment | DE: 'Und wenn sie in ihren Kammern blieben, während du schon wach bist und kommst und' | FR: "Toute joie veut l'éternité de toutes choses, elle veut du miel, du levain, une h"
ch-p0-00-v91 [en] sim=0.268 | possible misalignment | DE: 'Wehe! Es kommt die Zeit, wo der Mensch nicht mehr den Pfeil seiner Sehnsucht übe' | EN: 'Still is his soil rich enough for it. But that soil will one day be poor and exh'
ch-p4-20-v09 [fr] sim=0.269 | possible misalignment | DE: 'Aber noch fehlen mir meine rechten Menschen!“—' | FR: "Car toute joie se veut elle-même, c'est pourquoi elle veut la peine! O bonheur, "
ch-p0-00-v136 [fr] sim=0.269 | possible misalignment | DE: 'Sondern lebendige Gefährten brauche ich, die mir folgen, weil sie sich selber fo' | FR: 'Ensuite Zarathoustra marcha de nouveau pendant deux heures, se fiant à la route '
ch-p1-12-v09 [es] sim=0.271 | possible misalignment | DE: 'Umwerfen—das heisst ihm: beweisen. Toll machen—das heisst ihm: überzeugen. Und B' | ES: 'Mañana tendrá una nueva fe, y pasado mañana, otra más nueva. Sentidos rápidos ti'
ch-p4-04-v13 [es] sim=0.271 | possible misalignment | DE: 'Es gieng dir schlimm, du Unseliger, in diesem Leben: erst biss dich das Thier, u' | ES: '¡Bien! Por ahí sube el camino que lleva hasta la caverna de Zaratustra: no está '
ch-p4-18-v33 [fr] sim=0.271 | possible misalignment | DE: 'Wie doch einem jeden von euch das Herz zappelte vor Lust und Bosheit, darob, das' | FR: '"O vous tous, fols espiègles, pantins! pourquoi dissimuler et vous cacher devant'
ch-p2-04-v10 [es] sim=0.272 | possible misalignment | DE: 'Auf einem Eilande glaubten sie einst zu landen, als das Meer sie herumriss; aber' | ES: 'Pero yo sufro y he sufrido con ellos: prisioneros son para mí, y marcados. Aquel'
ch-p0-00-v121 [es] sim=0.272 | possible misalignment | DE: 'Unheimlich ist das menschliche Dasein und immer noch ohne Sinn: ein Possenreisse' | ES: 'Entretanto iba llegando el atardecer, y el mercado se ocultaba en la oscuridad: '
ch-p0-00-v160 [fr] sim=0.273 | possible misalignment | DE: 'Und wenn mich einst meine Klugheit verlässt:—ach, sie liebt es, davonzufliegen!—' | FR: 'Il faut que je sois plus sage! Que je sois rusé du fond du coeur, comme mon serp'
ch-p0-00-v158 [fr] sim=0.274 | possible misalignment | DE: 'Möchte ich klüger sein! Möchte ich klug von Grund aus sein, gleich meiner Schlan' | FR: "J'ai rencontré plus de dangers parmi les hommes que parmi les animaux. Zarathous"
ch-p1-15-v05 [es] sim=0.276 | possible misalignment | DE: 'Eine Tafel der Güter hängt über jedem Volke. Siehe, es ist seiner Überwindungen ' | ES: 'Jamás un vecino ha entendido al otro: siempre su alma se asombraba de la demenci'
ch-p0-00-v153 [es] sim=0.276 | possible misalignment | DE: '„Es sind meine Thiere!“ sagte Zarathustra und freute sich von Herzen.' | ES: 'Cantaré mi canción para los eremitas solitarios o en pareja; y a quien todavía t'
ch-p0-00-v138 [fr] sim=0.276 | possible misalignment | DE: 'Viele wegzulocken von der Heerde—dazu kam ich. Zürnen soll mir Volk und Heerde: ' | FR: "Mes yeux se sont ouverts: J'ai besoin de compagnons, de compagnons vivants, - no"
ch-p2-20-v53 [es] sim=0.277 | possible misalignment | DE: 'Aber warum redet Zarathustra anders zu seinen Schülern—als zu sich selber?“—' | ES: 'De la cordura respecto a los hombres'
ch-p3-08-v32 [es] sim=0.277 | possible misalignment | DE: '„Für einen Vater sorgt er nicht genug um seine Kinder: Menschen-Väter thun diess' | ES: 'Cinco frases sobre cosas viejas oí yo ayer por la noche junto al muro del jardín'
ch-p2-22-v45 [es] sim=0.278 | possible misalignment | DE: 'Zarathustra, vom Lesen und Schreiben.' | ES: 'Quien asciende a las montañas más altas se ríe de todas las tragedias, de las de'
ch-p0-00-v30 [es] sim=0.278 | possible misalignment | DE: 'Mit Singen, Weinen, Lachen und Brummen lobe ich den Gott, der mein Gott ist. Doc' | ES: '«¿Y qué hace el santo en el bosque?», preguntó Zaratustra.'
ch-p0-00-v44 [es] sim=0.279 | possible misalignment | DE: 'Einst blickte die Seele verächtlich auf den Leib: und damals war diese Verachtun' | ES: 'Son despreciadores de la vida, son moribundos y están,'
ch-p0-00-v63 [en] sim=0.280 | possible misalignment | DE: 'Was gross ist am Menschen, das ist, dass er eine Brücke und kein Zweck ist: was ' | EN: 'A dangerous crossing, a dangerous wayfaring, a dangerous looking-back, a dangero'
ch-p0-00-v128 [fr] sim=0.280 | possible misalignment | DE: 'Der Hunger überfällt mich, sagte Zarathustra, wie ein Räuber. In Wäldern und Süm' | FR: 'A la porte de la ville il rencontra les fossoyeurs: ils éclairèrent sa figure de'
ch-p0-00-v120 [en] sim=0.281 | possible misalignment | DE: 'Wahrlich, einen schönen Fischfang that heute Zarathustra! Keinen Menschen fieng ' | EN: 'Meanwhile the evening came on, and the market-place veiled itself in gloom. Then'
ch-p4-08-v25 [es] sim=0.281 | possible misalignment | DE: '—vor den Sträflingen des Reichthums, welche sich ihren Vortheil aus jedem Kehric' | ES: '«¿Por qué me tientas?, respondió éste. Tú mismo lo sabes mejor que yo. ¿Pues qué'
ch-p0-00-v139 [es] sim=0.282 | possible misalignment | DE: 'Hirten sage ich, aber sie nennen sich die Guten und Gerechten. Hirten sage ich: ' | ES: 'Una luz ha aparecido en mi horizonte: ¡no hable al pueblo Zaratustra, sino a com'
ch-p0-00-v94 [es] sim=0.282 | possible misalignment | DE: 'Seht! Ich zeige euch den letzten Menschen.' | ES: '¡Ay! Llega el tiempo en que el hombre no dará ya a luz ninguna estrella. ¡Ay! Ll'
ch-p0-00-v85 [es] sim=0.283 | possible misalignment | DE: 'Sie haben etwas, worauf sie stolz sind. Wie nennen sie es doch, was sie stolz ma' | ES: 'Cuando Zaratustra hubo dicho estas palabras contempló de nuevo el pueblo y calló'
ch-p0-00-v125 [en] sim=0.283 | possible misalignment | DE: 'Als Zarathustra diess zu seinem Herzen gesagt hatte, lud er den Leichnam auf sei' | EN: 'Gloomy is the night, gloomy are the ways of Zarathustra. Come, thou cold and sti'
ch-p0-00-v110 [en] sim=0.285 | possible misalignment | DE: 'Zu lange wohl lebte ich im Gebirge, zu viel horchte ich auf Bäche und Bäume: nun' | EN: '“They understand me not: I am not the mouth for these ears.'
ch-p3-02-v45 [es] sim=0.285 | possible misalignment | DE: 'Und, wahrlich, was ich sah, desgleichen sah ich nie. Einen jungen Hirten sah ich' | ES: 'un perro gritar así pidiendo socorro?'
ch-p2-04-v05 [es] sim=0.285 | possible misalignment | DE: 'Aber mein Blut ist mit dem ihren verwandt; und ich will mein Blut auch noch in d' | ES: 'Son enemigos malvados: nada es más vengativo que su humildad. Y fácilmente se en'
ch-p0-00-v43 [es] sim=0.285 | possible misalignment | DE: 'Einst war der Frevel an Gott der grösste Frevel, aber Gott starb, und damit auch' | ES: '¡Yo os conjuro, hermanos míos, permanecedfieles a la tierra y no creáis a quiene'
ch-p0-00-v88 [en] sim=0.286 | possible misalignment | DE: 'Und also sprach Zarathustra zum Volke:' | EN: 'I will speak unto them of the most contemptible thing: that, however, is THE LAS'
ch-p3-12-v70 [es] sim=0.286 | possible misalignment | DE: '„Du sollst nicht rauben! Du sollst nicht todtschlagen!“—solche Worte hiess man e' | ES: 'Oh hermanos míos, acerca de lo que son las estrellas y el futuro ha habido hasta'
ch-p0-00-v125 [es] sim=0.286 | possible misalignment | DE: 'Als Zarathustra diess zu seinem Herzen gesagt hatte, lud er den Leichnam auf sei' | ES: 'Mas todavía estoy muy lejos de ellos, y mi sentido no habla a sus sentidos. Para'
ch-p0-00-v156 [fr] sim=0.287 | possible misalignment | DE: "Gefährlicher fand ich's unter Menschen als unter Thieren, gefährlicher Wege geht" | FR: "L'animal le plus fier qu'il y ait sous le soleil et l'animal le plus rusé qu'il "
ch-p3-16-v32 [es] sim=0.287 | possible misalignment | DE: 'Wenn je mein Frohlocken rief: „die Küste schwand,—nun fiel mir die letzte Kette ' | ES: 'Si en mí hay aquel placer indagador que empuja las velas hacia lo no descubierto'
ch-p3-11-v37 [fr] sim=0.289 | possible misalignment | DE: 'Wahrlich, ich lernte das Warten auch und von Grund aus,' | FR: "J'appelle encore malheureux ceux qui sont obligés d'attendre toujours, - ils ne "
ch-p0-00-v156 [en] sim=0.289 | possible misalignment | DE: "Gefährlicher fand ich's unter Menschen als unter Thieren, gefährlicher Wege geht" | EN: 'They want to know whether Zarathustra still liveth. Verily, do I still live?'
ch-p0-00-v98 [es] sim=0.289 | possible misalignment | DE: 'Sie haben die Gegenden verlassen, wo es hart war zu leben: denn man braucht Wärm' | ES: ',, "Nosotros hemos inventado la felicidad - dicen los últimos hombres, y parpade'
ch-p0-00-v19 [es] sim=0.290 | possible misalignment | DE: 'Warum, sagte der Heilige, gieng ich doch in den Wald und die Einöde? War es nich' | ES: '¿quieres bajar a tierra? Ay, ¿quieres volver a arrastrar t ú mismo tu cuerpo?'
ch-p0-00-v128 [es] sim=0.291 | possible misalignment | DE: 'Der Hunger überfällt mich, sagte Zarathustra, wie ein Räuber. In Wäldern und Süm' | ES: 'Ala puerta de la ciudad encontró a los sepultureros: éstos iluminaron el rostro '
ch-p2-06-v27 [en] sim=0.292 | possible misalignment | DE: 'Auf dem Baume Zukunft bauen wir unser Nest; Adler sollen uns Einsamen Speise bri' | EN: 'Cast but your pure eyes into the well of my delight, my friends! How could it be'
ch-p0-00-v93 [en] sim=0.293 | possible misalignment | DE: 'Wehe! Es kommt die Zeit, wo der Mensch keinen Stern mehr gebären wird. Wehe! Es ' | EN: 'I tell you: one must still have chaos in one, to give birth to a dancing star. I'
ch-p0-00-v50 [es] sim=0.293 | possible misalignment | DE: 'Die Stunde, wo ihr sagt: „Was liegt an meinem Glücke! Es ist Armuth und Schmutz,' | ES: 'En verdad, una sucia corriente es el hombre. Es necesario ser un mar para poder '
ch-p4-07-v19 [es] sim=0.294 | possible misalignment | DE: 'Zürnst du mir, dass ich zu lange schon rede-rade-breche? Dass ich schon dir rath' | ES: '- tú has adivinado qué sentimientos experimenta el que lo mató a Él. ¡Quédate! Y'
ch-p2-06-v10 [es] sim=0.294 | possible misalignment | DE: 'Und nicht das ist der Bissen, an dem ich am meisten würgte, zu wissen, dass das ' | ES: 'Ymás de uno que vino como aniquilador y como granizada para todos los campos de '
ch-p0-00-v97 [es] sim=0.294 | possible misalignment | DE: '„Wir haben das Glück erfunden“—sagen die letzten Menschen und blinzeln.' | ES: 'La tierra se ha vuelto pequeña entonces, y sobre ella da saltos el último hombre'
ch-p0-00-v105 [es] sim=0.294 | possible misalignment | DE: 'Man ist klug und weiss Alles, was geschehn ist: so hat man kein Ende zu spotten.' | ES: '"En otro tiempo todo el mundo desvariaba\' - dicen los más sutiles, y parpadean.'
ch-p0-00-v159 [en] sim=0.294 | possible misalignment | DE: 'Aber Unmögliches bitte ich da: so bitte ich denn meinen Stolz, dass er immer mit' | EN: '“Would that I were wiser! Would that I were wise from the very heart, like my se'
ch-p0-00-v99 [es] sim=0.294 | possible misalignment | DE: 'Krankwerden und Misstrauen-haben gilt ihnen sündhaft: man geht achtsam einher. E' | ES: 'Han abandonado las comarcas donde era duro vivir: pues la gente necesita calor. '
ch-p0-00-v64 [en] sim=0.295 | possible misalignment | DE: 'Ich liebe Die, welche nicht zu leben wissen, es sei denn als Untergehende, denn ' | EN: 'What is great in man is that he is a bridge and not a goal: what is lovable in m'
ch-p0-00-v153 [fr] sim=0.295 | possible misalignment | DE: '„Es sind meine Thiere!“ sagte Zarathustra und freute sich von Herzen.' | FR: 'Je marche vers mon but, je suis ma route; je sauterai par-dessus les hésitants e'
ch-p0-00-v42 [en] sim=0.295 | possible misalignment | DE: 'Verächter des Lebens sind es, Absterbende und selber Vergiftete, deren die Erde ' | EN: 'I conjure you, my brethren, REMAIN TRUE TO THE EARTH, and believe not those who '
ch-p3-15-v41 [es] sim=0.297 | possible misalignment | DE: 'Eins! Oh Mensch! Gieb Acht! Zwei! Was spricht die tiefe Mitternacht? Drei! „Ich ' | ES: '¡ Una!'
ch-p4-18-v33 [es] sim=0.297 | possible misalignment | DE: 'Wie doch einem jeden von euch das Herz zappelte vor Lust und Bosheit, darob, das' | ES: '«¡Oh vosotros todos, vosotros pícaros, payasos! ¡Por qué os desfiguráis y os esc'
ch-p0-00-v58 [es] sim=0.297 | possible misalignment | DE: 'Seht, ich lehre euch den Übermenschen: der ist dieser Blitz, der ist dieser Wahn' | ES: '¿Habéis hablado ya así? ¿Habéis gritado ya así? ¡Ah, ojalá os hubiese yo oído ya'
ch-p0-00-v61 [es] sim=0.297 | possible misalignment | DE: 'Der Mensch ist ein Seil, geknüpft zwischen Thier und Übermensch,—ein Seil über e' | ES: 'Mirad, yo os enseño el superhombre: ¡él es ese rayo, él es esa demencia! - Cuand'
ch-p0-00-v133 [es] sim=0.298 | possible misalignment | DE: 'Darauf gieng Zarathustra wieder zwei Stunden und vertraute dem Wege und dem Lich' | ES: '«¿Quién viene a mí y a mi mal dormir?»'
ch-p0-00-v148 [es] sim=0.298 | possible misalignment | DE: 'Nicht Hirt soll ich sein, nicht Todtengräber. Nicht reden einmal will ich wieder' | ES: 'Compañeros en la creación busca Zaratustra, compañeros en la recolección y en la'
ch-p4-11-v06 [es] sim=0.298 | possible misalignment | DE: 'Doch dünkt mir, ihr taugt euch schlecht zur Gesellschaft, ihr macht einander das' | ES: '- ¡en mi propia caverna se halla sentado el hombre superior! ¡Mas de qué me admi'
ch-p0-00-v47 [es] sim=0.299 | possible misalignment | DE: 'Wahrlich, ein schmutziger Strom ist der Mensch. Man muss schon ein Meer sein, um' | ES: 'En otro tiempo el alma miraba al cuerpo con desprecio: y ese desprecio era enton'
ch-p0-00-v160 [es] sim=0.299 | possible misalignment | DE: 'Und wenn mich einst meine Klugheit verlässt:—ach, sie liebt es, davonzufliegen!—' | ES: 'Cuando Zaratustra hubo dicho esto, se acordó de las palabras del santo en el bos'
ch-p0-00-v151 [es] sim=0.300 | possible misalignment | DE: 'Zu meinem Ziele will ich, ich gehe meinen Gang; über die Zögernden und Saumselig' | ES: 'No debo ser pastor ni sepulturero. Y ni siquiera voy a volver a hablar con el pu'
ch-p3-13-v45 [es] sim=0.300 | possible misalignment | DE: '—„ach, der Mensch kehrt ewig wieder! Der kleine Mensch kehrt ewig wieder!“—' | ES: 'Mi suspirar estaba sentado sobre todos los sepulcros de los hombres y no podía p'
ch-p4-01-v07 [fr] sim=0.301 | possible misalignment | DE: 'Und als ich nach Honig begehrte, begehrte ich nur nach Köder und süssem Seime un' | FR: "Que parlais-je de sacrifier? Je gaspille ce que l'on me donne, moi le gaspilleur"
ch-p0-00-v88 [es] sim=0.302 | possible misalignment | DE: 'Und also sprach Zarathustra zum Volke:' | ES: 'Voy a hablarles de lo más despreciable: el último hombre»'
ch-p0-00-v29 [es] sim=0.304 | possible misalignment | DE: 'Der Heilige antwortete: Ich mache Lieder und singe sie, und wenn ich Lieder mach' | ES: '¡No vayas a los hombres y quédate en el bosque! ¡Es mejor que vayas incluso a lo'
ch-p0-00-v105 [en] sim=0.306 | possible misalignment | DE: 'Man ist klug und weiss Alles, was geschehn ist: so hat man kein Ende zu spotten.' | EN: '“Formerly all the world was insane,”—say the subtlest of them, and blink thereby'
ch-p0-00-v110 [es] sim=0.306 | possible misalignment | DE: 'Zu lange wohl lebte ich im Gebirge, zu viel horchte ich auf Bäche und Bäume: nun' | ES: 'No me entienden: no soy yo la boca para estos oídos.'
ch-p3-16-v32 [fr] sim=0.306 | possible misalignment | DE: 'Wenn je mein Frohlocken rief: „die Küste schwand,—nun fiel mir die letzte Kette ' | FR: 'Si je porte en moi cette joie du chercheur, cette joie qui pousse la voile vers '
ch-p0-00-v90 [es] sim=0.307 | possible misalignment | DE: 'Noch ist sein Boden dazu reich genug. Aber dieser Boden wird einst arm und zahm ' | ES: 'Es tiempo de que el hombre fije su propia meta. Es tiempo de que el hombre plant'
ch-p0-00-v91 [es] sim=0.307 | possible misalignment | DE: 'Wehe! Es kommt die Zeit, wo der Mensch nicht mehr den Pfeil seiner Sehnsucht übe' | ES: 'Todavía es bastante fértil su terreno para ello. Mas algún día ese terreno será '
ch-p4-08-v36 [es] sim=0.308 | possible misalignment | DE: 'Siehe, dorthin führt der Weg zu meiner Höhle: sei diese Nacht ihr Gast. Und rede' | ES: '- «¡Bien!, dijo Zaratustra: tú deberías ver también mis animales, mi águila y mi'
ch-p2-06-v27 [fr] sim=0.309 | possible misalignment | DE: 'Auf dem Baume Zukunft bauen wir unser Nest; Adler sollen uns Einsamen Speise bri' | FR: "Jetez donc vos purs regards dans la source de ma joie, amis! Comment s'en troubl"
ch-p3-13-v70 [es] sim=0.309 | possible misalignment | DE: 'Die Stunde kam nun, dass der Untergehende sich selber segnet. Also endet Zarathu' | ES: 'He dicho mi palabra, quedo hecho pedazos a causa de ella: así lo quiere mi suert'
ch-p3-12-v150 [fr] sim=0.310 | possible misalignment | DE: '—die umfänglichste Seele, welche am weitesten in sich laufen und irren und schwe' | FR: "Quelle est la plus haute espèce chez l'être et quelle est l'espèce la plus basse"
ch-p0-00-v140 [fr] sim=0.310 | possible misalignment | DE: 'Siehe die Guten und Gerechten! Wen hassen sie am meisten? Den, der zerbricht ihr' | FR: "Mes yeux se sont ouverts: Ce n'est pas à la foule que doit parler Zarathoustra, "
ch-p0-00-v29 [en] sim=0.311 | possible misalignment | DE: 'Der Heilige antwortete: Ich mache Lieder und singe sie, und wenn ich Lieder mach' | EN: '“And what doeth the saint in the forest?” asked Zarathustra.'
ch-p0-00-v155 [fr] sim=0.311 | possible misalignment | DE: 'Erkunden wollen sie, ob Zarathustra noch lebe. Wahrlich, lebe ich noch?' | FR: '"Ce sont mes animaux! dit Zarathoustra, et il se réjouit de tout coeur.'
ch-p0-00-v81 [en] sim=0.311 | possible misalignment | DE: 'Ich liebe alle Die, welche schwere Tropfen sind, einzeln fallend aus der dunklen' | EN: 'I love him who is of a free spirit and a free heart: thus is his head only the b'
ch-p3-15-v41 [en] sim=0.311 | possible misalignment | DE: 'Eins! Oh Mensch! Gieb Acht! Zwei! Was spricht die tiefe Mitternacht? Drei! „Ich ' | EN: 'One!'
ch-p0-00-v11 [fr] sim=0.311 | possible misalignment | DE: 'Siehe! Dieser Becher will wieder leer werden, und Zarathustra will wieder Mensch' | FR: 'Ainsi commença le déclin de Zarathoustra.'
ch-p4-19-v17 [fr] sim=0.311 | possible misalignment | DE: "—hörst du's nicht, wie sie heimlich, schrecklich, herzlich zu dir redet, die alt" | FR: 'O homme, prends garde!'
ch-p0-00-v85 [en] sim=0.313 | possible misalignment | DE: 'Sie haben etwas, worauf sie stolz sind. Wie nennen sie es doch, was sie stolz ma' | EN: 'Must one first batter their ears, that they may learn to hear with their eyes? M'
ch-p0-00-v48 [es] sim=0.313 | possible misalignment | DE: 'Seht, ich lehre euch den Übermenschen: der ist diess Meer, in ihm kann eure gros' | ES: 'Oh, también esa alma era flaca, fea y famélica: ¡y la crueldad era la voluptuosi'
ch-p0-00-v152 [fr] sim=0.315 | possible misalignment | DE: 'Diess hatte Zarathustra zu seinem Herzen gesprochen, als die Sonne im Mittag sta' | FR: 'Je veux me joindre aux créateurs, à ceux qui moissonnent et chôment: je leur mon'
ch-p0-00-v22 [es] sim=0.318 | possible misalignment | DE: 'Gieb ihnen Nichts, sagte der Heilige. Nimm ihnen lieber Etwas ab und trage es mi' | ES: 'Ahora amo a Dios: a los hombres no los amo. El hombre es para mí una cosa demasi'
ch-p3-11-v37 [es] sim=0.318 | possible misalignment | DE: 'Wahrlich, ich lernte das Warten auch und von Grund aus,' | ES: 'Desventurados llamo yo a todos aquellos que siempre tienen que aguardar, - repug'
ch-p0-00-v112 [en] sim=0.318 | possible misalignment | DE: 'Und nun blicken sie mich an und lachen: und indem sie lachen, hassen sie mich no' | EN: 'Calm is my soul, and clear, like the mountains in the morning. But they think me'
ch-p0-00-v64 [es] sim=0.319 | possible misalignment | DE: 'Ich liebe Die, welche nicht zu leben wissen, es sei denn als Untergehende, denn ' | ES: 'El hombre es una cuerda tendida entre el animal y el superhombre, - una cuerda s'
ch-p0-00-v157 [fr] sim=0.319 | possible misalignment | DE: 'Als Zarathustra diess gesagt hatte, gedachte er der Worte des Heiligen im Walde,' | FR: 'Ils ont voulu savoir si Zarathoustra vivait encore. En vérité, suis je encore en'
ch-p0-00-v120 [es] sim=0.319 | possible misalignment | DE: 'Wahrlich, einen schönen Fischfang that heute Zarathustra! Keinen Menschen fieng ' | ES: 'Cuando Zaratustra hubo dicho esto, el moribundo ya no respondió; pero movió la m'
ch-p0-00-v48 [en] sim=0.321 | possible misalignment | DE: 'Seht, ich lehre euch den Übermenschen: der ist diess Meer, in ihm kann eure gros' | EN: 'Verily, a polluted stream is man. One must be a sea, to receive a polluted strea'
ch-p0-00-v129 [en] sim=0.321 | possible misalignment | DE: 'Wunderliche Launen hat mein Hunger. Oft kommt er mir erst nach der Mahlzeit, und' | EN: '“Hunger attacketh me,” said Zarathustra, “like a robber. Among forests and swamp'
ch-p0-00-v56 [en] sim=0.323 | possible misalignment | DE: 'Nicht eure Sünde—eure Genügsamkeit schreit gen Himmel, euer Geiz selbst in eurer' | EN: 'Have ye ever spoken thus? Have ye ever cried thus? Ah! would that I had heard yo'
ch-p3-16-v39 [es] sim=0.323 | possible misalignment | DE: '—im Lachen nämlich ist alles Böse bei einander, aber heilig- und losgesprochen d' | ES: 'Si mi maldad es una maldad riente, que habita entre colinas de rosas y setos de '
ch-p4-03-v14 [es] sim=0.323 | possible misalignment | DE: '—pfui, unter dem Gesindel die Ersten zu bedeuten! Ach, Ekel! Ekel! Ekel! Was lie' | ES: 'Nosotros no somos los primeros - y, sin embargo, tenemos que pasar por tales: de'
ch-p0-00-v93 [es] sim=0.324 | possible misalignment | DE: 'Wehe! Es kommt die Zeit, wo der Mensch keinen Stern mehr gebären wird. Wehe! Es ' | ES: 'Yo os digo: es preciso tener todavía caos dentro de sí para poder dar a luz una '
ch-p4-14-v21 [es] sim=0.324 | possible misalignment | DE: 'Der du den Menschen schautest So Gott als Schaf—: Den Gott zerreissen im Mensche' | ES: 'Cuando el aire va perdiendo luminosidad, Cuando ya la hoz de la luna Se desliza '
ch-p0-00-v106 [es] sim=0.325 | possible misalignment | DE: 'Man hat sein Lüstchen für den Tag und sein Lüstchen für die Nacht: aber man ehrt' | ES: 'Hoy la gente es inteligente y sabe todo lo que ha ocurrido: así no acaba nunca d'
ch-p0-00-v57 [es] sim=0.326 | possible misalignment | DE: 'Wo ist doch der Blitz, der euch mit seiner Zunge lecke? Wo ist der Wahnsinn, mit' | ES: 'La hora en que digáis: «¡Qué importa mi compasión! ¿No es la compasión acaso la '
ch-p0-00-v123 [en] sim=0.326 | possible misalignment | DE: 'Aber noch bin ich ihnen ferne, und mein Sinn redet nicht zu ihren Sinnen. Eine M' | EN: 'I want to teach men the sense of their existence, which is the Superman, the lig'
ch-p3-13-v19 [es] sim=0.326 | possible misalignment | DE: 'Zwischen dem Ähnlichsten gerade lügt der Schein am schönsten; denn die kleinste ' | ES: 'Acada alma le pertenece un mundo distinto; para cada alma es toda otra alma un t'
ch-p3-11-v31 [es] sim=0.327 | possible misalignment | DE: 'Das tiefe Gelb und das heisse Roth: so will es mein Geschmack,—der mischt Blut z' | ES: 'Omnicontentamiento que sabe sacarle gusto a todo: ¡no es éste el mejor gusto! Yo'
ch-p0-00-v129 [es] sim=0.328 | possible misalignment | DE: 'Wunderliche Launen hat mein Hunger. Oft kommt er mir erst nach der Mahlzeit, und' | ES: 'Zaratustra no dijo ni una palabra y siguió su camino. Pero cuando llevaba andand'
ch-p0-00-v87 [en] sim=0.328 | possible misalignment | DE: 'So will ich ihnen vom Verächtlichsten sprechen: das aber ist der letzte Mensch.“' | EN: 'They dislike, therefore, to hear of ‘contempt’ of themselves. So I will appeal t'
ch-p4-19-v58 [es] sim=0.329 | possible misalignment | DE: 'Sagtet ihr jemals ja zu Einer Lust? Oh, meine Freunde, so sagtet ihr Ja auch zu ' | ES: '¿Una gota de rocío? ¿Un vapor y perfume de la eternidad? ¿No lo oís? ¿No lo oléi'
ch-p2-04-v30 [es] sim=0.330 | possible misalignment | DE: 'Blutzeichen schrieben sie auf den Weg, den sie giengen, und ihre Thorheit lehrte' | ES: 'Espíritus pequeños y almas voluminosas tenían estos pastores: pero, hermanos mío'
ch-p3-13-v39 [es] sim=0.330 | possible misalignment | DE: '„Ach dass sein Bösestes so gar klein ist! Ach dass sein Bestes so gar klein ist!' | ES: 'El gran hastío del hombre él era el que me estrangulaba y -'
ch-p0-00-v24 [en] sim=0.331 | possible misalignment | DE: '„Nein, antwortete Zarathustra, ich gebe kein Almosen. Dazu bin ich nicht arm gen' | EN: 'If, however, thou wilt give unto them, give them no more than an alms, and let t'
ch-p0-00-v46 [es] sim=0.331 | possible misalignment | DE: 'Aber auch ihr noch, meine Brüder, sprecht mir: was kündet euer Leib von eurer Se' | ES: 'En otro tiempo el delito contra Dios era el máximo delito, pero Dios ha muerto y'
ch-p0-00-v86 [en] sim=0.331 | possible misalignment | DE: 'Drum hören sie ungern von sich das Wort „Verachtung“. So will ich denn zu ihrem ' | EN: 'They have something whereof they are proud. What do they call it, that which mak'
ch-p3-10-v03 [es] sim=0.334 | possible misalignment | DE: 'Messbar für Den, der Zeit hat, wägbar für einen guten Wäger, erfliegbar für star' | ES: '¡Oh, qué pronto me llegó la aurora: me despertó con su ardor, la celosa! Celosa '
ch-p0-00-v126 [es] sim=0.335 | possible misalignment | DE: 'Am Thore der Stadt begegneten ihm die Todtengräber: sie leuchteten ihm mit der F' | ES: 'Oscura es la noche, oscuros son los caminos de Zaratustra. ¡Ven, compañero frío '
ch-p0-00-v153 [en] sim=0.335 | possible misalignment | DE: '„Es sind meine Thiere!“ sagte Zarathustra und freute sich von Herzen.' | EN: 'This had Zarathustra said to his heart when the sun stood at noontide. Then he l'
ch-p4-16-v04 [fr] sim=0.336 | possible misalignment | DE: '—das böse Spiel der ziehenden Wolken, der feuchten Schwermuth, der verhängten Hi' | FR: "Déjà le vieil enchanteur nous a prodigué ce qu'il avait de plus mauvais, et, reg"
ch-p0-00-v16 [en] sim=0.337 | possible misalignment | DE: 'Verwandelt ist Zarathustra, zum Kind ward Zarathustra, ein Erwachter ist Zarathu' | EN: 'Yea, I recognise Zarathustra. Pure is his eye, and no loathing lurketh about his'
ch-p4-15-v26 [fr] sim=0.338 | possible misalignment | DE: 'Wohlan! Seien wir wieder gut und guter Dinge! Und ob schon Zarathustra böse blic' | FR: 'Surtout quand il se montre nu. Mais que puis-je faire à ses malices, moi! Est-ce'
ch-p0-00-v140 [es] sim=0.338 | possible misalignment | DE: 'Siehe die Guten und Gerechten! Wen hassen sie am meisten? Den, der zerbricht ihr' | ES: 'Para incitar a muchos a apartarse del rebaño - para eso he venido. Pueblo y reba'
ch-p3-04-v18 [es] sim=0.338 | possible misalignment | DE: 'Und oft gelüstete mich, sie mit zackichten Blitz-Golddrähten festzuheften, dass ' | ES: '¡Prefiero estar sentado en el tonel bajo un cielo cubierto, prefiero estar senta'
ch-p0-00-v57 [en] sim=0.338 | possible misalignment | DE: 'Wo ist doch der Blitz, der euch mit seiner Zunge lecke? Wo ist der Wahnsinn, mit' | EN: 'It is not your sin—it is your self-satisfaction that crieth unto heaven; your ve'
ch-p0-00-v157 [en] sim=0.339 | possible misalignment | DE: 'Als Zarathustra diess gesagt hatte, gedachte er der Worte des Heiligen im Walde,' | EN: 'More dangerous have I found it among men than among animals; in dangerous paths '
ch-p0-00-v28 [en] sim=0.339 | possible misalignment | DE: '„Und was macht der Heilige im Walde?“ fragte Zarathustra.' | EN: 'Go not to men, but stay in the forest! Go rather to the animals! Why not be like'
ch-p0-00-v151 [fr] sim=0.339 | possible misalignment | DE: 'Zu meinem Ziele will ich, ich gehe meinen Gang; über die Zögernden und Saumselig' | FR: 'Je ne dois être ni berger, ni fossoyeur. Jamais plus je ne parlerai au peuple; p'
ch-p0-00-v139 [en] sim=0.340 | possible misalignment | DE: 'Hirten sage ich, aber sie nennen sich die Guten und Gerechten. Hirten sage ich: ' | EN: 'To allure many from the herd—for that purpose have I come. The people and the he'
ch-p3-12-v207 [es] sim=0.341 | possible misalignment | DE: 'Bei Welchen liegt die grösste Gefahr aller Menschen-Zukunft? Ist es nicht bei de' | ES: '¡Romped, destrozadme a los buenos yjustos! Oh hermanos -'
ch-p4-11-v28 [es] sim=0.342 | possible misalignment | DE: "Nun geschieht's, dass die Einsamkeit selber mürbe wird und zerbricht, einem Grab" | ES: '"¿Por qué no viene él, que se anunció hace ya tanto tiempo?, así preguntan mucho'
ch-p0-00-v82 [es] sim=0.342 | possible misalignment | DE: 'Seht, ich bin ein Verkündiger des Blitzes und ein schwerer Tropfen aus der Wolke' | ES: 'Yo amo a quien es de espíritu libre y de corazón libre: su cabeza no es así más '
ch-p0-00-v49 [en] sim=0.344 | possible misalignment | DE: 'Was ist das Grösste, das ihr erleben könnt? Das ist die Stunde der grossen Verac' | EN: 'Lo, I teach you the Superman: he is that sea; in him can your great contempt be '
ch-p0-00-v51 [es] sim=0.344 | possible misalignment | DE: 'Die Stunde, wo ihr sagt: „Was liegt an meiner Vernunft! Begehrt sie nach Wissen ' | ES: 'Mirad, yo os enseño el superhombre: él es ese mar, en él puede sumergirse vuestr'
ch-p0-00-v41 [en] sim=0.344 | possible misalignment | DE: 'Ich beschwöre euch, meine Brüder, bleibt der Erde treu und glaubt Denen nicht, w' | EN: 'The Superman is the meaning of the earth. Let your will say: The Superman SHALL '
ch-p0-00-v95 [es] sim=0.344 | possible misalignment | DE: '„Was ist Liebe? Was ist Schöpfung? Was ist Sehnsucht? Was ist Stern“—so fragt de' | ES: '¡Mirad! Yo os muestro el último hombre.'
ch-p0-00-v101 [es] sim=0.345 | possible misalignment | DE: 'Man arbeitet noch, denn Arbeit ist eine Unterhaltung. Aber man sorgt, dass die U' | ES: 'Un poco de veneno de vez en cuando: eso produce sueños agradables. Y mucho venen'
ch-p3-12-v150 [es] sim=0.345 | possible misalignment | DE: '—die umfänglichste Seele, welche am weitesten in sich laufen und irren und schwe' | ES: '¿Cuál es la especie más alta de todo ser, y cuál la más baja? El parásito es la '
ch-p0-00-v17 [es] sim=0.345 | possible misalignment | DE: 'Wie im Meere lebtest du in der Einsamkeit, und das Meer trug dich. Wehe, du will' | ES: 'Zaratustra está transformado, Zaratustra se ha convertido en un niño, Zaratustra'
ch-p0-00-v42 [es] sim=0.345 | possible misalignment | DE: 'Verächter des Lebens sind es, Absterbende und selber Vergiftete, deren die Erde ' | ES: 'El superhombre es el sentido de la tierra. Diga vuestra voluntad: jsea el superh'
ch-p4-19-v59 [fr] sim=0.346 | possible misalignment | DE: '—wolltet ihr jemals Ein Mal Zwei Mal, spracht ihr jemals „du gefällst mir, Glück' | FR: 'La douleur est aussi une joie, la malédiction est aussi une bénédiction, la nuit'
ch-p3-12-v74 [es] sim=0.346 | possible misalignment | DE: 'Diess ist mein Mitleid mit allem Vergangenen, dass ich sehe: es ist preisgegeben' | ES: '¿O fue una predicación de la muerte la que llamó santo a lo que hablaba en contr'
ch-p0-00-v35 [en] sim=0.346 | possible misalignment | DE: '„Alle Wesen bisher schufen etwas über sich hinaus: und ihr wollt die Ebbe dieser' | EN: 'I TEACH YOU THE SUPERMAN. Man is something that is to be surpassed. What have ye'
ch-p4-05-v07 [es] sim=0.347 | possible misalignment | DE: 'Haha! Mich—willst du? Mich? Mich—ganz?' | ES: '¡En vano! ¡Sigue pinchando, Cruelísimo aguijón! No, No un perro - tu caza soy ta'
ch-p4-05-v32 [es] sim=0.349 | possible misalignment | DE: 'Oh Zarathustra, Alles ist Lüge an mir; aber dass ich zerbreche—diess mein Zerbre' | ES: 'Yo he querido representar el papel de un gran hombre, y persuadí a muchos de que'
ch-p3-02-v48 [es] sim=0.349 | possible misalignment | DE: 'Den Kopf ab! Beiss zu!“—so schrie es aus mir, mein Grauen, mein Hass, mein Ekel,' | ES: '« ¡Muerde! ¡Muerde!'
ch-p0-00-v111 [en] sim=0.350 | possible misalignment | DE: 'Unbewegt ist meine Seele und hell wie das Gebirge am Vormittag. Aber sie meinen,' | EN: 'Too long, perhaps, have I lived in the mountains; too much have I hearkened unto'
ch-p0-00-v24 [es] sim=0.351 | possible misalignment | DE: '„Nein, antwortete Zarathustra, ich gebe kein Almosen. Dazu bin ich nicht arm gen' | ES: 'No les des nada, dijo el santo. Es mejor que les quites alguna cosa y que la lle'
ch-p4-07-v02 [es] sim=0.351 | possible misalignment | DE: 'An deren Worten will ich lange nun kauen gleich als an guten Körnern; klein soll' | ES: '«¡Qué buenas cosas, decía, me ha regalado este día para compensarme de haber com'
ch-p0-00-v129 [fr] sim=0.354 | possible misalignment | DE: 'Wunderliche Launen hat mein Hunger. Oft kommt er mir erst nach der Mahlzeit, und' | FR: "Zarathoustra ne répondit pas un mot et passa son chemin. Lorsqu'il eut marché pe"
ch-p2-18-v04 [es] sim=0.354 | possible misalignment | DE: 'Um die gleiche Zeit, als diese Schiffer an der Feuerinsel landeten, lief das Ger' | ES: '«¡Mirad!, dijo el viejo timonel, ¡ahí va Zaratustra al infierno!»z39_'
ch-p0-00-v107 [es] sim=0.355 | possible misalignment | DE: '„Wir haben das Glück erfunden“—sagen die letzten Menschen und blinzeln—' | ES: 'La gente tiene su pequeño placer para el día y su pequeño placer para la noche: '
ch-p0-00-v127 [en] sim=0.356 | possible misalignment | DE: 'Zarathustra sagte dazu kein Wort und gieng seines Weges. Als er zwei Stunden geg' | EN: 'At the gate of the town the grave-diggers met him: they shone their torch on his'
ch-p0-00-v124 [es] sim=0.356 | possible misalignment | DE: "Dunkel ist die Nacht, dunkel sind die Wege Zarathustra's. Komm, du kalter und st" | ES: 'Yo quiero enseñar a los hombres el sentido de su ser: ese sentido es el superhom'
ch-p0-00-v16 [es] sim=0.357 | possible misalignment | DE: 'Verwandelt ist Zarathustra, zum Kind ward Zarathustra, ein Erwachter ist Zarathu' | ES: 'Sí, reconozco a Zaratustra. Puro es su ojo, y en su boca no se oculta náusea alg'
ch-p2-04-v24 [es] sim=0.358 | possible misalignment | DE: 'Nackt möchte ich sie sehn: denn allein die Schönheit sollte Busse predigen. Aber' | ES: 'Mejores canciones tendrían que cantarme para que yo aprendiese a creer en su red'
ch-p4-19-v33 [fr] sim=0.359 | possible misalignment | DE: "—nun will sie sterben, vor Glück sterben. Ihr höheren Menschen, riecht ihr's nic" | FR: "Vieille cloche! Douce lyre! toutes les douleurs t'ont déchiré le coeur, la doule"
ch-p0-00-v122 [en] sim=0.362 | possible misalignment | DE: 'Ich will die Menschen den Sinn ihres Seins lehren: welcher ist der Übermensch, d' | EN: 'Sombre is human life, and as yet without meaning: a buffoon may be fateful to it'
ch-p4-13-v103 [es] sim=0.362 | possible misalignment | DE: 'Der den Eseln Flügel giebt, der Löwinnen melkt, gelobt sei dieser gute unbändige' | ES: 'Haced como el viento cuando se precipita desde sus cavernas de la montaña: quier'
ch-p0-00-v139 [fr] sim=0.364 | possible misalignment | DE: 'Hirten sage ich, aber sie nennen sich die Guten und Gerechten. Hirten sage ich: ' | FR: "Mais j'ai besoin de compagnons vivants qui me suivent, parce qu'ils veulent se s"
ch-p0-00-v143 [en] sim=0.364 | possible misalignment | DE: 'Gefährten sucht der Schaffende, und Miterntende: denn Alles steht bei ihm reif z' | EN: 'Companions, the creator seeketh, not corpses—and not herds or believers either. '
ch-p4-07-v22 [es] sim=0.365 | possible misalignment | DE: 'Jedweder Andere hätte mir sein Almosen zugeworfen, sein Mitleiden, mit Blick und' | ES: 'Mas en el hecho de que tú pasases a mi lado en silencio; de que te ruborizases, '
ch-p3-12-v33 [es] sim=0.365 | possible misalignment | DE: '—also, dass der ärmste Fischer noch mit goldenem Ruder rudert! Diess nämlich sah' | ES: 'Pues todavía una vez quiero ir a los hombres: jentre ellos quiero hundirme en mi'
ch-p0-00-v143 [fr] sim=0.365 | possible misalignment | DE: 'Gefährten sucht der Schaffende, und Miterntende: denn Alles steht bei ihm reif z' | FR: 'Voyez les bons et les justes! Qui haïssent-ils le plus? Celui qui brise leurs ta'
ch-p0-00-v130 [en] sim=0.366 | possible misalignment | DE: 'Und damit schlug Zarathustra an das Thor des Hauses. Ein alter Mann erschien; er' | EN: '“Strange humours hath my hunger. Often it cometh to me only after a repast, and '
ch-p1-10-v08 [es] sim=0.366 | possible misalignment | DE: 'Ihr sollt den Frieden lieben als Mittel zu neuen Kriegen. Und den kurzen Frieden' | ES: '¡Debéis buscar vuestro enemigo, debéis hacer vuestra gue-rra, y hacerla por vues'
ch-p0-00-v86 [es] sim=0.369 | possible misalignment | DE: 'Drum hören sie ungern von sich das Wort „Verachtung“. So will ich denn zu ihrem ' | ES: 'Tienen algo de lo que están orgullosos. ¿Cómo llaman a eso que los llena de orgu'
ch-p2-17-v33 [es] sim=0.369 | possible misalignment | DE: 'Und gerne geben sie sich damit als Versöhner: aber Mittler und Mischer bleiben s' | ES: 'Un soplo y un deslizarse de fantasmas me parecen a mí todos sus arpegios; ¡qué h'
ch-p0-00-v36 [en] sim=0.369 | possible misalignment | DE: 'Was ist der Affe für den Menschen? Ein Gelächter oder eine schmerzliche Scham. U' | EN: 'All beings hitherto have created something beyond themselves: and ye want to be '
ch-p0-00-v06 [fr] sim=0.370 | possible misalignment | DE: 'Ich möchte verschenken und austheilen, bis die Weisen unter den Menschen wieder ' | FR: 'Voilà pourquoi je dois descendre dans les profondeurs, comme tu fais le soir qua'
ch-p0-00-v69 [en] sim=0.371 | possible misalignment | DE: 'Ich liebe Den, welcher seine Tugend liebt: denn Tugend ist Wille zum Untergang u' | EN: 'I love him who laboureth and inventeth, that he may build the house for the Supe'
ch-p1-20-v20 [es] sim=0.371 | possible misalignment | DE: 'Jener suchte eine Magd mit den Tugenden eines Engels. Aber mit Einem Male wurde ' | ES: 'Aquél era esquivo en sus relaciones con otros, y seleccionaba al elegir. Pero de'
ch-p0-00-v35 [es] sim=0.372 | possible misalignment | DE: '„Alle Wesen bisher schufen etwas über sich hinaus: und ihr wollt die Ebbe dieser' | ES: '«¡Será posible! ¡Este viejo santo en su bosque no ha oído todavía nada de que Di'
ch-p3-03-v30 [es] sim=0.372 | possible misalignment | DE: 'Wenn ich mich dessen erst überwunden habe, dann will ich mich auch des Grösseren' | ES: '¡mas alguna vez debo encontrar la fuerza y la voz del león, que te llame arriba!'
ch-p0-00-v12 [fr] sim=0.372 | possible misalignment | DE: "—Also begann Zarathustra's Untergang." | FR: 'Zarathoustra descendit seul des montagnes, et il ne rencontra personne. Mais lor'
ch-p4-10-v28 [es] sim=0.373 | possible misalignment | DE: "Wann trinkst du diesen Tropfen Thau's, der auf alle Erden-Dinge niederfiel,—wann" | ES: '«Üh cielo por encima de mí, dijo suspirando y s e sentó derecho, ¿tú me contempl'
ch-p0-00-v135 [es] sim=0.374 | possible misalignment | DE: 'Ein Licht gieng mir auf: Gefährten brauche ich und lebendige,—nicht todte Gefähr' | ES: 'El viejo se fue y al poco volvió y ofreció a Zaratustra pan y vino. «Mal sitio e'
ch-p4-20-v06 [fr] sim=0.376 | possible misalignment | DE: 'Sie schlafen noch in meiner Höhle, ihr Traum käut noch an meinen Mitternächten. ' | FR: "O hommes supérieurs, c'est après vous qu'elle languit, la joie, l'effrénée, la b"
ch-p0-00-v130 [es] sim=0.377 | possible misalignment | DE: 'Und damit schlug Zarathustra an das Thor des Hauses. Ein alter Mann erschien; er' | ES: 'El hambre me asalta, dijo Zaratustra, como un ladrón. En medio de bosques y de c'
ch-p3-06-v28 [fr] sim=0.377 | possible misalignment | DE: 'Und muss ich mich nicht verbergen, gleich Einem, der Gold verschluckt hat,—dass ' | FR: "Silencieux ciel d'hiver à la barbe de neige, tête blanche aux yeux clairs au-des"
ch-p0-00-v140 [en] sim=0.379 | possible misalignment | DE: 'Siehe die Guten und Gerechten! Wen hassen sie am meisten? Den, der zerbricht ihr' | EN: 'Herdsmen, I say, but they call themselves the good and just. Herdsmen, I say, bu'
ch-p0-00-v20 [en] sim=0.380 | possible misalignment | DE: 'Jetzt liebe ich Gott: die Menschen liebe ich nicht. Der Mensch ist mir eine zu u' | EN: '“Why,” said the saint, “did I go into the forest and the desert? Was it not beca'
ch-p3-14-v30 [es] sim=0.380 | possible misalignment | DE: '—schon glühst du und träumst, schon trinkst du durstig an allen tiefen klingende' | ES: 'Oh alma mía, ahora te he dado todo, e incluso lo último que tenía, y todas mis m'
ch-p0-00-v137 [fr] sim=0.383 | possible misalignment | DE: 'Ein Licht gieng mir auf: nicht zum Volke rede Zarathustra, sondern zu Gefährten!' | FR: "Zarathoustra dormit longtemps et non seulement l'aurore passa sur son visage, ma"
ch-p4-20-v16 [fr] sim=0.383 | possible misalignment | DE: 'Und schon kam ihm die Erinnerung, und er begriff mit Einem Blicke Alles, was zwi' | FR: "Avez-vous maintenant appris mon chant? Avez-vous deviné ce qu'il veut dire? Eh b"
ch-p4-18-v04 [es] sim=0.383 | possible misalignment | DE: 'Und du selber, du alter Papst, wie stimmt Das mit dir selber zusammen, dass du s' | ES: '¡Todo el mundo juzgaría que vosotros, con vuestra nueva fe, sois los peores blas'
ch-p4-06-v02 [fr] sim=0.383 | possible misalignment | DE: 'Wie! Kaum bin ich jenem Zauberer entronnen: muss mir da wieder ein anderer Schwa' | FR: "Peu de temps cependant après que Zarathoustra se fut débarrassé de l'enchanteur,"
ch-p0-00-v17 [en] sim=0.384 | possible misalignment | DE: 'Wie im Meere lebtest du in der Einsamkeit, und das Meer trug dich. Wehe, du will' | EN: 'Altered is Zarathustra; a child hath Zarathustra become; an awakened one is Zara'
ch-p4-06-v02 [es] sim=0.385 | possible misalignment | DE: 'Wie! Kaum bin ich jenem Zauberer entronnen: muss mir da wieder ein anderer Schwa' | ES: 'No mucho después de haberse librado Zaratustra del mago vio de nuevo a alguien s'
ch-p0-00-v115 [es] sim=0.385 | possible misalignment | DE: '„Bei meiner Ehre, Freund, antwortete Zarathustra, das giebt es Alles nicht, wovo' | ES: 'cuando estaba ya a un solo paso detrás de él ocurrió aquella cosa horrible que h'
ch-p0-00-v13 [fr] sim=0.385 | possible misalignment | DE: 'Zarathustra stieg allein das Gebirge abwärts und Niemand begegnete ihm. Als er a' | FR: '"Il ne m\'est pas inconnu, ce voyageur; voilà bien des années qu\'il passa par ici'
ch-p3-09-v11 [es] sim=0.386 | possible misalignment | DE: "—als du sprachst: mögen mich meine Thiere führen! Gefährlicher fand ich's unter " | ES: '¡aquello era abandono!'
ch-p0-00-v37 [es] sim=0.386 | possible misalignment | DE: 'Ihr habt den Weg vom Wurme zum Menschen gemacht, und Vieles ist in euch noch Wur' | ES: 'Yo os enseño el superhombre El hombre es algo que debe ser superado. ¿Qué habéis'
ch-p3-12-v203 [fr] sim=0.388 | possible misalignment | DE: 'Die Guten nämlich—die können nicht schaffen: die sind immer der Anfang vom Ende:' | FR: "C'est le créateur qu'ils haïssent le plus: celui qui brise des tables et de viei"
ch-p4-19-v06 [es] sim=0.388 | possible misalignment | DE: 'Meine Freunde, was dünket euch? Wollt ihr nicht gleich mir zum Tode sprechen: Wa' | ES: 'Yno me basta con atestiguar esto. Merece la pena vivir en la tierra: un solo día'
ch-p0-00-v22 [en] sim=0.388 | possible misalignment | DE: 'Gieb ihnen Nichts, sagte der Heilige. Nimm ihnen lieber Etwas ab und trage es mi' | EN: 'Zarathustra answered: “What spake I of love! I am bringing gifts unto men.”'
ch-p0-00-v160 [en] sim=0.389 | possible misalignment | DE: 'Und wenn mich einst meine Klugheit verlässt:—ach, sie liebt es, davonzufliegen!—' | EN: 'But I am asking the impossible. Therefore do I ask my pride to go always with my'
ch-p0-00-v23 [en] sim=0.389 | possible misalignment | DE: 'Und willst du ihnen geben, so gieb nicht mehr, als ein Almosen, und lass sie noc' | EN: '“Give them nothing,” said the saint. “Take rather part of their load, and carry '
ch-p3-12-v222 [fr] sim=0.389 | possible misalignment | DE: 'Die Schaffenden nämlich sind hart. Und Seligkeit muss es euch dünken, eure Hand ' | FR: 'Et si votre dureté ne veut pas étinceler, et trancher, et inciser: comment pourr'
ch-p4-11-v31 [es] sim=0.392 | possible misalignment | DE: '—denn er selber ist zu dir unterwegs, der letzte Rest Gottes unter Menschen, das' | ES: 'Yel hecho de que nosotros, hombres desesperados, hayamos venido ahora a tu caver'
ch-p0-00-v116 [es] sim=0.395 | possible misalignment | DE: 'Der Mann blickte misstrauisch auf. „Wenn du die Wahrheit sprichst, sagte er dann' | ES: 'Zaratustra, en cambio, permaneció inmóvil, y justo a su lado cayó el cuerpo, mal'
ch-p3-05-v08 [es] sim=0.395 | possible misalignment | DE: 'Desselbigen Tages aber redete er seine Rede über die verkleinernde Tugend.' | ES: 'Oh, cuándo regresaré a mi patria, donde ya no tengo que agacharme - ¡donde ya no'
ch-p0-00-v28 [es] sim=0.396 | possible misalignment | DE: '„Und was macht der Heilige im Walde?“ fragte Zarathustra.' | ES: 'Nuestros pasos les suenan demasiado solitarios por sus callejas. Y cuando por la'
ch-p0-00-v38 [en] sim=0.397 | possible misalignment | DE: 'Wer aber der Weiseste von euch ist, der ist auch nur ein Zwiespalt und Zwitter v' | EN: 'Ye have made your way from the worm to man, and much within you is still worm. O'
ch-p0-00-v131 [fr] sim=0.398 | possible misalignment | DE: '„Ein Lebendiger und ein Todter, sagte Zarathustra. Gebt mir zu essen und zu trin' | FR: "Ma faim a de singuliers caprices. Souvent elle ne me vient qu'après le repas, et"
ch-p0-00-v10 [fr] sim=0.399 | possible misalignment | DE: 'Segne den Becher, welcher überfliessen will, dass das Wasser golden aus ihm flie' | FR: 'Vois! cette coupe veut se vider à nouveau et Zarathoustra veut redevenir homme."'
ch-p0-00-v119 [es] sim=0.400 | possible misalignment | DE: 'Inzwischen kam der Abend, und der Markt barg sich in Dunkelheit: da verlief sich' | ES: '«No hables así, dijo Zaratustra, tú has hecho del peligro tu profesión, en ello '
ch-p2-06-v27 [es] sim=0.400 | possible misalignment | DE: 'Auf dem Baume Zukunft bauen wir unser Nest; Adler sollen uns Einsamen Speise bri' | ES: 'Pues ésta es nuestra altura y nuestra patria: en un lugar demasiado alto y abrup'

_Total LaBSE flags: 330_

## 2. Truncation / OCR / surface residue (per verse)
ch-p0-00-v17 [es] | digit glued to letter (OCR) | Zaratustra está transformado, Zaratustra se ha convertido en un niño, Zaratustra es un despierto1º: ¿qué quieres hacer a
ch-p0-00-v32 [de] | trailing dash artifact | Als Zarathustra aber allein war, sprach er also zu seinem Herzen: „Sollte es denn möglich sein! Dieser alte Heilige hat 
ch-p0-00-v35 [es] | trailing dash artifact | «¡Será posible! ¡Este viejo santo en su bosque no ha oído todavía nada de que Dios ha muerto!» -
ch-p0-00-v58 [de] | trailing dash artifact | Seht, ich lehre euch den Übermenschen: der ist dieser Blitz, der ist dieser Wahnsinn!—
ch-p0-00-v59 [en] | trailing dash artifact | Lo, I teach you the Superman: he is that lightning, he is that frenzy!—
ch-p0-00-v82 [de] | trailing dash artifact | Seht, ich bin ein Verkündiger des Blitzes und ein schwerer Tropfen aus der Wolke: dieser Blitz aber heisst Übermensch.—
ch-p0-00-v83 [en] | trailing dash artifact | Lo, I am a herald of the lightning, and a heavy drop out of the cloud: the lightning, however, is the SUPERMAN.—
ch-p0-00-v84 [es] | trailing dash artifact | Mirad, yo soy un anunciador del rayo y una pesada gota que cae de la nube: mas ese rayo se llama superhombre. -
ch-p0-00-v87 [es] | raw < or > present | Por esto no les gusta oír, referida a ellos, la palabra <despre-cio'. Voy a hablar, pues, a su orgullo.
ch-p0-00-v107 [de] | trailing dash artifact | „Wir haben das Glück erfunden“—sagen die letzten Menschen und blinzeln—
ch-p0-00-v107 [fr] | trailing dash artifact | "Nous avons inventé le bonheur," - disent les derniers hommes, et ils clignent de l'oeil. -
ch-p0-00-v108 [en] | trailing dash artifact | “We have discovered happiness,”—say the last men, and blink thereby.—
ch-p0-00-v108 [es] | trailing dash artifact | "Nosotros hemos inventado la felicidad" - dicen los últimos hombres, y parpadean. -
ch-p0-00-v114 [es] | trailing dash artifact | Pero entonces ocurrió algo que hizo callar todas las bocas y quedar fijos todos los ojos. Entretanto, en efecto, el vola
ch-p0-00-v118 [de] | trailing dash artifact | Als Zarathustra diess gesagt hatte, antwortete der Sterbende nicht mehr; aber er bewegte die Hand, wie als ob er die Han
ch-p0-00-v120 [es] | trailing dash artifact | Cuando Zaratustra hubo dicho esto, el moribundo ya no respondió; pero movió la mano como si buscase la mano de Zaratustr
ch-p0-00-v130 [es] | digit glued to letter (OCR) | El hambre me asalta, dijo Zaratustra, como un ladrón. En medio de bosques y de ciénagas me asalta mi hambre, y en plena 
ch-p0-00-v132 [de] | trailing dash artifact | Der Alte gieng fort, kam aber gleich zurück und bot Zarathustra Brod und Wein. „Eine böse Gegend ist's für Hungernde, sa
ch-p0-00-v133 [en] | trailing dash artifact | The old man withdrew, but came back immediately and offered Zarathustra bread and wine. “A bad country for the hungry,” 
ch-p1-01-v26 [de] | trailing dash artifact | Drei Verwandlungen nannte ich euch des Geistes: wie der Geist zum Kameele ward, und zum Löwen das Kameel, und der Löwe z
ch-p1-01-v26 [en] | trailing dash artifact | Three metamorphoses of the spirit have I designated to you: how the spirit became a camel, the camel a lion, and the lio
ch-p1-01-v26 [fr] | trailing dash artifact | Je vous ai nommé trois métamorphoses de l'esprit: comment l'esprit devient chameau, comment l'esprit devient lion, et co
ch-p1-01-v26 [es] | trailing dash artifact | Tres transformaciones del espíritu os he mencionado: cómo el espíritu se convirtió en camello, y el camello en león, y e
ch-p1-02-v01 [es] | digit glued to letter (OCR) | Le habían alabado a Zaratustra un sabio que sabía hablar bien del dormir4° y de la virtud: por ello, se decía, era muy h
ch-p1-02-v25 [de] | trailing dash artifact | Aber nicht lange mehr stehe ich dann: da liege ich schon.—
ch-p1-02-v25 [en] | trailing dash artifact | But not much longer do I then stand: I already lie.—
ch-p1-02-v25 [fr] | trailing dash artifact | Mais je ne suis pas debout longtemps que déjà je m'étends. -
ch-p1-02-v34 [de] | trailing dash artifact | Selig sind diese Schläfrigen: denn sie sollen bald einnicken.—
ch-p1-02-v34 [en] | trailing dash artifact | Blessed are those drowsy ones: for they shall soon nod to sleep.—
ch-p1-02-v34 [fr] | trailing dash artifact | Bienheureux les assoupis: car ils s'endormiront bientôt. -
ch-p1-02-v34 [es] | trailing dash artifact | Bienaventurados son estos somnolientos: pues no tardarán en quedar dormidos. -
ch-p1-03-v34 [en] | trailing dash artifact | More uprightly and purely speaketh the healthy body, perfect and square-built; and it speaketh of the meaning of the ear
ch-p1-03-v34 [fr] | trailing dash artifact | Le corps sain parle avec plus de loyauté et plus de pureté, le corps complet, carré de la tête à la base: il parle du se
ch-p1-04-v22 [de] | trailing dash artifact | Ich gehe nicht euren Weg, ihr Verächter des Leibes! Ihr seid mir keine Brücken zum Übermenschen!—
ch-p1-04-v22 [en] | trailing dash artifact | I go not your way, ye despisers of the body! Ye are no bridges for me to the Superman!—
ch-p1-04-v22 [fr] | trailing dash artifact | Je ne marche pas sur votre chemin, contempteurs du corps! Vous n'êtes point pour moi des ponts vers le Surhumain! -
ch-p1-04-v22 [es] | trailing dash artifact | ¡ Yo no voy por vuestro camino, despreciadores del cuerpo! ¡Vosotros no sois para mí puentes hacia el superhombre! -
ch-p1-05-v25 [de] | trailing dash artifact | Der Mensch ist Etwas, das überwunden werden muss: und darum sollst du deine Tugenden lieben,—denn du wirst an ihnen zu G
ch-p1-05-v25 [en] | trailing dash artifact | Man is something that hath to be surpassed: and therefore shalt thou love thy virtues,—for thou wilt succumb by them.—
ch-p1-05-v25 [es] | trailing dash artifact | El hombre es algo que tiene que ser superado: y por ello tienes que amar tus virtudes, - pues perecerás a causa de ellas
ch-p1-06-v27 [de] | trailing dash artifact | Ich bin ein Geländer am Strome: fasse mich, wer mich fassen kann! Eure Krücke aber bin ich nicht.—
ch-p1-06-v27 [en] | trailing dash artifact | I am a railing alongside the torrent; whoever is able to grasp me may grasp me! Your crutch, however, I am not.—
ch-p1-06-v27 [fr] | trailing dash artifact | Je suis un garde-fou au bord du fleuve: que celui qui peut me saisir me saisisse! Je ne suis pas votre béquille. -
ch-p1-06-v27 [es] | trailing dash artifact | Yo soy un pretil junto a la corriente: ¡agárreme el que pueda agarrarme! Pero yo no soy vuestra muleta. -
ch-p1-07-v26 [en] | trailing dash artifact | Now am I light, now do I fly; now do I see myself under myself. Now there danceth a God in me.—
ch-p1-08-v35 [de] | trailing dash artifact | Aber bei meiner Liebe und Hoffnung beschwöre ich dich: wirf den Helden in deiner Seele nicht weg! Halte heilig deine höc
ch-p1-08-v35 [en] | trailing dash artifact | But by my love and hope I conjure thee: cast not away the hero in thy soul! Maintain holy thy highest hope!—
ch-p1-08-v35 [fr] | trailing dash artifact | Mais par mon amour et par mon espoir, je t'en conjure: ne jette pas loin de toi le héros qui est dans ton âme! Sanctifie
ch-p1-08-v35 [es] | trailing dash artifact | Mas por mi amor y mi esperanza te conjuro: ¡no arrojes al héroe que hay en tu alma! ¡Conserva santa tu más alta esperanz
ch-p1-09-v11 [es] | digit glued to letter (OCR) | O: extienden la mano hacia las confituras y, al hacerlo, se burlan de su niñería: penden de esa caña de paja que es su v
ch-p1-09-v12 [de] | trailing dash artifact | Ihre Weisheit lautet: „ein Thor, der leben bleibt, aber so sehr sind wir Thoren! Und das eben ist das Thörichtste am Leb
ch-p1-09-v12 [fr] | trailing dash artifact | Leur sagesse dit: "Est fou qui demeure en vie, mais nous sommes tellement fous! Et ceci est la plus grande folie de la v
ch-p1-09-v14 [de] | trailing dash artifact | Und also laute die Lehre eurer Tugend „du sollst dich selber tödten! Du sollst dich selber davonstehlen!“—
ch-p1-09-v14 [en] | trailing dash artifact | And let this be the teaching of your virtue: “Thou shalt slay thyself! Thou shalt steal away from thyself!”—
ch-p1-09-v19 [de] | trailing dash artifact | Aber sie wollen loskommen vom Leben: was schiert es sie, dass sie Andre mit ihren Ketten und Geschenken noch fester bind
ch-p1-09-v19 [en] | trailing dash artifact | But they want to be rid of life; what care they if they bind others still faster with their chains and gifts!—
ch-p1-09-v19 [fr] | trailing dash artifact | Mais ils veulent se débarrasser de la vie: que leur importe si avec leurs chaînes et leurs présents ils en attachent d'a
ch-p1-09-v19 [es] | trailing dash artifact | Pero ellos quieren librarse de la vida: ¡qué les importa el que, con sus cadenas y sus regalos, aten a otros más fuertem
ch-p1-09-v24 [en] | trailing dash artifact | Or “life eternal”; it is all the same to me—if only they pass away quickly!—
ch-p1-10-v06 [es] | trailing dash artifact | Debéis ser de aquellos cuyos ojos buscan siempre un enemigo vuestro enemigo. Y en algunos de vosotros hay un -
ch-p1-10-v24 [de] | trailing dash artifact | Ich schone euch nicht, ich liebe euch von Grund aus, meine Brüder im Kriege!—
ch-p1-10-v24 [en] | trailing dash artifact | I spare you not, I love you from my very heart, my brethren in war!—
ch-p1-10-v24 [fr] | trailing dash artifact | Je ne vous ménage point, je vous aime du fond du coeur, mes frères en la guerre! -
ch-p1-10-v24 [es] | trailing dash artifact | ¡Yo no os trato con indulgencia, yo os amo a fondo, hermanos míos en la guerra! -
ch-p1-11-v33 [de] | trailing dash artifact | Dort, wo der Staat aufhört,—so seht mir doch hin, meine Brüder! Seht ihr ihn nicht, den Regenbogen und die Brücken des Ü
ch-p1-11-v33 [en] | trailing dash artifact | There, where the state CEASETH—pray look thither, my brethren! Do ye not see it, the rainbow and the bridges of the Supe
ch-p1-11-v33 [es] | trailing dash artifact | Allí donde el Estado acaba, - ¡miradme allí, hermanos míos! ¿No veis el arco iris y los puentes del superhombre? -
ch-p1-12-v39 [de] | trailing dash artifact | Fliehe, mein Freund, in deine Einsamkeit und dorthin, wo eine rauhe, starke Luft weht. Nicht ist es dein Loos, Fliegenwe
ch-p1-12-v39 [en] | trailing dash artifact | Flee, my friend, into thy solitude—and thither, where a rough strong breeze bloweth. It is not thy lot to be a fly-flap.
ch-p1-12-v39 [fr] | trailing dash artifact | Fuis, mon ami, fuis dans ta solitude, là-haut où souffle un vent rude et fort. Ce n'est pas ta destinée d'être un chasse
ch-p1-12-v39 [es] | trailing dash artifact | Huye, amigo mío, a tu soledad y allí donde sopla un viento áspero, fuerte. No es tu destino el ser espantamoscas. -
ch-p1-13-v20 [en] | trailing dash artifact | We offered that guest harbour and heart: now it dwelleth with us—let it stay as long as it will!”—
ch-p1-15-v26 [de] | trailing dash artifact | Aber sagt mir doch, meine Brüder: wenn der Menschheit das Ziel noch fehlt, fehlt da nicht auch—sie selber noch?—
ch-p1-15-v26 [en] | trailing dash artifact | But pray tell me, my brethren, if the goal of humanity be still lacking, is there not also still lacking—humanity itself
ch-p1-15-v26 [es] | trailing dash artifact | Mas decidme, hermanos: si a la humanidad le falta todavía la meta, ¿no falta todavía también - ella misma? -
ch-p1-16-v20 [en] | trailing dash artifact | My brethren, I advise you not to neighbour-love—I advise you to furthest love!—
ch-p1-17-v35 [de] | trailing dash artifact | Mit meinen Thränen gehe in deine Vereinsamung, mein Bruder. Ich liebe Den, der über sich selber hinaus schaffen will und
ch-p1-17-v35 [en] | trailing dash artifact | With my tears, go into thine isolation, my brother. I love him who seeketh to create beyond himself, and thus succumbeth
ch-p1-17-v35 [fr] | trailing dash artifact | Va dans ta solitude avec mes larmes, ô mon frère. J'aime celui qui veut créer plus haut que lui-même et qui périt aussi.
ch-p1-17-v35 [es] | trailing dash artifact | Vete con tus lágrimas a tu soledad, hermano mío. Yo amo a quien quiere crear por encima de sí mismo y por ello perece. -
ch-p1-18-v02 [de] | trailing dash artifact | Ist es ein Schatz, der dir geschenkt? Oder ein Kind, das dir geboren wurde? Oder gehst du jetzt selber auf den Wegen der
ch-p1-18-v02 [en] | trailing dash artifact | Is it a treasure that hath been given thee? Or a child that hath been born thee? Or goest thou thyself on a thief’s erra
ch-p1-18-v08 [es] | raw < or > present | «Háblame también a mí acerca de la mujer, dijo ella; soy bastante vieja para volver a olvidarlo enseguida. >>
ch-p1-18-v27 [de] | trailing dash artifact | Des Mannes Gemüth aber ist tief, sein Strom rauscht in unterirdischen Höhlen: das Weib ahnt seine Kraft, aber begreift s
ch-p1-18-v27 [en] | trailing dash artifact | Man’s soul, however, is deep, its current gusheth in subterranean caverns: woman surmiseth its force, but comprehendeth 
ch-p1-18-v27 [fr] | trailing dash artifact | Mais l'âme de l'homme est profonde, son flot mugit dans les cavernes souterraines: la femme pressent la puissance de l'h
ch-p1-18-v33 [de] | trailing dash artifact | „Du gehst zu Frauen? Vergiss die Peitsche nicht!“—
ch-p1-18-v33 [en] | trailing dash artifact | “Thou goest to women? Do not forget thy whip!”—
ch-p1-18-v33 [fr] | trailing dash artifact | "Tu vas chez les femmes? N'oublie pas le fouet!" -
ch-p1-18-v33 [es] | trailing dash artifact | «¿Vas con mujeres? ¡No olvides el látigo!» -
ch-p1-19-v03 [de] | trailing dash artifact | Den Vernichter der Moral heissen mich die Guten und Gerechten: meine Geschichte ist unmoralisch.—
ch-p1-19-v18 [en] | trailing dash artifact | Guard against injuring the anchorite! If ye have done so, however, well then, kill him also!—
ch-p1-20-v28 [de] | trailing dash artifact | Heilig heisst mir solch ein Wille und solche Ehe.—
ch-p1-20-v28 [en] | trailing dash artifact | Holy call I such a will, and such a marriage.—
ch-p1-20-v28 [fr] | trailing dash artifact | Je sanctifie telle volonté et un tel mariage. -
ch-p1-20-v28 [es] | trailing dash artifact | Santos son entonces para mí tal voluntad y tal matrimonio. -
ch-p1-22-v09 [en] | trailing dash artifact | Verily, an appropriator of all values must such bestowing love become; but healthy and holy, call I this selfishness.—
ch-p1-22-v13 [es] | soft-hyphen U+00AD present; trailing dash artifact | Decidme, hermanos míos: ¿qué es para nosotros lo malo y lo peor? ¿No es la degeneración? Y siempre adivinamos de­ -
ch-p1-22-v26 [es] | trailing dash artifact | Aquí Zaratustra calló un rato y contempló con amor a sus discípulos. Después continuó hablando así: y su voz se había -
ch-p1-22-v54 [de] | trailing dash artifact | „Todt sind alle Götter: nun wollen wir, dass der Übermensch lebe.“—diess sei einst am grossen Mittage unser letzter Will
ch-p1-22-v54 [en] | trailing dash artifact | “DEAD ARE ALL THE GODS: NOW DO WE DESIRE THE SUPERMAN TO LIVE.”—Let this be our final will at the great noontide!—
ch-p1-22-v54 [fr] | trailing dash artifact | "Tous les dieux sont morts: nous voulons, maintenant, que le surhumain vive!" Que ceci soit un jour, au grand midi, notr
ch-p1-22-v54 [es] | trailing dash artifact | «Muertos están todos los dioses: ahora queremos que viva el superhombre.» ¡sea ésta alguna vez, en el gran mediodía, -
ch-p2-01-v09 [de] | trailing dash artifact | Verloren giengen mir meine Freunde; die Stunde kam mir, meine Verlornen zu suchen!—
ch-p2-01-v09 [en] | trailing dash artifact | Lost are my friends; the hour hath come for me to seek my lost ones!—
ch-p2-01-v09 [fr] | trailing dash artifact | J'ai perdu mes amis; l'heure est venue de chercher ceux que j'ai perdus!" -
ch-p2-01-v22 [de] | trailing dash artifact | Wie ein Schrei und ein jauchzen will ich über weite Meere hinfahren, bis ich die glückseligen Inseln finde, wo meine Fre
ch-p2-01-v22 [en] | trailing dash artifact | Like a cry and an huzza will I traverse wide seas, till I find the Happy Isles where my friends sojourn;—
ch-p2-01-v22 [fr] | trailing dash artifact | Je veux passer sur de vastes mers, comme une exclamation ou un cri de joie, jusqu'à ce que je trouves les Iles Bienheure
ch-p2-01-v24 [de] | trailing dash artifact | Und wenn ich auf mein wildestes Pferd steigen will, so hilft mir mein Speer immer am besten hinauf: der ist meines Fusse
ch-p2-01-v24 [en] | trailing dash artifact | And when I want to mount my wildest horse, then doth my spear always help me up best: it is my foot’s ever ready servant
ch-p2-01-v24 [fr] | trailing dash artifact | Et quand je veux monter sur mon coursier le plus fougueux, c'est ma lance qui m'y aide le mieux: elle est toujours prête
ch-p2-01-v33 [en] | trailing dash artifact | On the soft sward of your hearts, my friends!—on your love, would she fain couch her dearest one!—
ch-p2-01-v33 [fr] | trailing dash artifact | C'est sur la molle pelouse de vos coeurs, mes amis! - sur votre amour, qu'elle aimerait à abriter ce qu'elle a de plus c
ch-p2-02-v01 [es] | digit glued to letter (OCR) | En las is1as afortunadas L os higos caen de los árboles, son buenos y dulces; y, conforme caen, su roja piel se abre. Un
ch-p2-02-v07 [de] | trailing dash artifact | Nicht ihr vielleicht selber, meine Brüder! Aber zu Vätern und Vorfahren könntet ihr euch umschaffen des Übermenschen: un
ch-p2-02-v07 [en] | trailing dash artifact | Not perhaps ye yourselves, my brethren! But into fathers and forefathers of the Superman could ye transform yourselves: 
ch-p2-02-v07 [fr] | trailing dash artifact | Ce ne sera peut-être pas vous-mêmes, mes frères! Mais vous pourriez vous transformer en pères et en ancêtres du Surhumai
ch-p2-02-v13 [de] | trailing dash artifact | Wohl zog ich den Schluss; nun aber zieht er mich.—
ch-p2-02-v13 [en] | trailing dash artifact | Yea, I have drawn the conclusion; now, however, doth it draw me.—
ch-p2-02-v13 [fr] | trailing dash artifact | C'est moi qui ai tiré cette conséquence, en vérité; mais maintenant elle me tire moi-même.-
ch-p2-02-v18 [de] | trailing dash artifact | Alles Unvergängliche—das ist nur ein Gleichniss! Und die Dichter lügen zuviel.—
ch-p2-02-v18 [en] | trailing dash artifact | All the imperishable—that’s but a simile, and the poets lie too much.—
ch-p2-02-v34 [de] | trailing dash artifact | Des Übermenschen Schönheit kam zu mir als Schatten. Ach, meine Brüder! Was gehen mich noch—die Götter an!—
ch-p2-02-v34 [en] | trailing dash artifact | The beauty of the Superman came unto me as a shadow. Ah, my brethren! Of what account now are—the Gods to me!—
ch-p2-02-v34 [fr] | trailing dash artifact | La beauté du Surhumain m'a visité comme une ombre. Hélas, mes frères! Que m'importent encore - les Dieux! -
ch-p2-02-v34 [es] | trailing dash artifact | La belleza del superhombre llegó hasta mí como una sombra. ¡Ay, hermanos míos! ¡Qué me importan ya - los dioses! -
ch-p2-03-v26 [de] | trailing dash artifact | Dem aber, der vom Teufel besessen ist, sage ich diess Wort in's Ohr: „besser noch, du ziehest deinen Teufel gross! Auch 
ch-p2-03-v26 [en] | trailing dash artifact | To him however, who is possessed of a devil, I would whisper this word in the ear: “Better for thee to rear up thy devil
ch-p2-03-v37 [de] | trailing dash artifact | Und jüngst hörte ich ihn diess Wort sagen: „Gott ist todt; an seinem Mitleiden mit den Menschen ist Gott gestorben.“—
ch-p2-03-v37 [en] | trailing dash artifact | And lately, did I hear him say these words: “God is dead: of his pity for man hath God died.”—
ch-p2-03-v37 [fr] | trailing dash artifact | Et dernièrement je l'ai entendu dire ces mots: "Dieux est mort; c'est sa pitié des hommes qui a tué Dieux." -
ch-p2-03-v41 [de] | trailing dash artifact | Alle Schaffenden aber sind hart.—
ch-p2-03-v41 [en] | trailing dash artifact | All creators, however, are hard.—
ch-p2-03-v41 [fr] | trailing dash artifact | Cependant, tous les créateurs sont durs. -
ch-p2-03-v41 [es] | trailing dash artifact | Mas todos los creadores son duros. -
ch-p2-04-v05 [de] | trailing dash artifact | Aber mein Blut ist mit dem ihren verwandt; und ich will mein Blut auch noch in dem ihren geehrt wissen.“—
ch-p2-04-v05 [en] | trailing dash artifact | But my blood is related to theirs; and I want withal to see my blood honoured in theirs.”—
ch-p2-04-v05 [fr] | trailing dash artifact | Mais mon sang est parent du leur; et je veux que mon sang soit honoré même dans le leur." -
ch-p2-04-v08 [de] | trailing dash artifact | Aber ich leide und litt mit ihnen: Gefangene sind es mir und Abgezeichnete. Der, welchen sie Erlöser nennen, schlug sie 
ch-p2-04-v08 [en] | trailing dash artifact | But I suffer and have suffered with them: prisoners are they unto me, and stigmatised ones. He whom they call Saviour pu
ch-p2-04-v08 [fr] | trailing dash artifact | Pourtant je souffre et j'ai souffert avec eux: prisonniers, à mes yeux, ils portent la marque des réprouvés. Celui qu'il
ch-p2-04-v10 [es] | trailing dash artifact | Pero yo sufro y he sufrido con ellos: prisioneros son para mí, y marcados. Aquel a quien ellos llaman redentor los arroj
ch-p2-04-v36 [de] | trailing dash artifact | Niemals noch gab es einen Übermenschen. Nackt sah ich Beide, den grössten und den kleinsten Menschen:—
ch-p2-04-v36 [en] | trailing dash artifact | Never yet hath there been a Superman. Naked have I seen both of them, the greatest man and the smallest man:—
ch-p2-04-v36 [fr] | trailing dash artifact | Jamais encore il n'y a eu de Surhumain. Je les ai vu nus tous les deux, le plus grand et le plus petit homme: -
ch-p2-04-v37 [en] | trailing dash artifact | All-too-similar are they still to each other. Verily, even the greatest found I—all-too-human!—
ch-p2-04-v37 [es] | trailing dash artifact | Nunca ha habido todavía un superhombre. Desnudos he visto yo a ambos, al hombre más grande y al más pequeño: - Demasiado
ch-p2-05-v15 [de] | trailing dash artifact | Dass eure Tugend euer Selbst sei und nicht ein Fremdes, eine Haut, eine Bemäntelung: das ist die Wahrheit aus dem Grunde
ch-p2-05-v15 [en] | trailing dash artifact | That your virtue is your Self, and not an outward thing, a skin, or a cloak: that is the truth from the basis of your so
ch-p2-05-v15 [fr] | trailing dash artifact | Que votre vertu soit identique à votre "moi" et non pas quelque chose d'étranger, un épiderme et un manteau: voilà la vé
ch-p2-05-v31 [en] | trailing dash artifact | And many a one who cannot see men’s loftiness, calleth it virtue to see their baseness far too well: thus calleth he his
ch-p2-05-v34 [de] | trailing dash artifact | Aber nicht dazu kam Zarathustra, allen diesen Lügnern und Narren zu sagen: „was wisst ihr von Tugend! Was könntet ihr vo
ch-p2-05-v34 [en] | trailing dash artifact | But Zarathustra came not to say unto all those liars and fools: “What do YE know of virtue! What COULD ye know of virtue
ch-p2-05-v34 [fr] | trailing dash artifact | Mais Zarathoustra n'est pas venu pour dire à tous ces menteurs et à ces insensés: "Que savez-vous de la vertu? Que pourr
ch-p2-05-v36 [de] | trailing dash artifact | Müde würdet der Worte „Lohn,“ „Vergeltung,“ „Strafe,“ „Rache in der Gerechtigkeit“—
ch-p2-05-v36 [en] | trailing dash artifact | That ye might become weary of the words “reward,” “retribution,” “punishment,” “righteous vengeance.”—
ch-p2-05-v36 [fr] | trailing dash artifact | pour que vous vous fatiguiez des mots "récompense", "représailles', "punition", "vengeance dans la justice" -
ch-p2-05-v42 [de] | trailing dash artifact | So werden sie getröstet sein; und gleich ihnen sollt auch ihr, meine Freunde, eure Tröstungen haben—und neue bunte Musch
ch-p2-05-v42 [en] | trailing dash artifact | Thus will they be comforted; and like them shall ye also, my friends, have your comforting—and new speckled shells!—
ch-p2-05-v42 [fr] | trailing dash artifact | Ainsi ils seront consolés; et comme eux, vous aussi, mes amis, vous aurez vos consolations - et de nouveaux coquillages 
ch-p2-05-v42 [es] | trailing dash artifact | Así serán consolados; e igual que ellos, también vosotros, amigos míos, tendréis vuestros consuelos - ¡y nuevas conchas 
ch-p2-06-v10 [de] | trailing dash artifact | Und nicht das ist der Bissen, an dem ich am meisten würgte, zu wissen, dass das Leben selber Feindschaft nöthig hat und 
ch-p2-06-v10 [en] | trailing dash artifact | And it is not the mouthful which hath most choked me, to know that life itself requireth enmity and death and torture-cr
ch-p2-06-v10 [fr] | trailing dash artifact | Et ce n'est point là le morceau qui me fut le plus dur à avaler: la conviction que la vie elle-même a besoin d'inimitié,
ch-p2-06-v23 [de] | trailing dash artifact | Und noch muss ich lernen, bescheidener dir zu nahen: allzuheftig strömt dir noch mein Herz entgegen:—
ch-p2-06-v23 [en] | trailing dash artifact | And yet must I learn to approach thee more modestly: far too violently doth my heart still flow towards thee:—
ch-p2-06-v23 [fr] | trailing dash artifact | Il faut que j'apprenne à t'approcher plus modestement: avec trop de violence mon coeur afflue à ta rencontre: -
ch-p2-06-v32 [en] | trailing dash artifact | Verily, a strong wind is Zarathustra to all low places; and this counsel counselleth he to his enemies, and to whatever 
ch-p2-07-v36 [de] | trailing dash artifact | Wie sich göttlich hier Gewölbe und Bogen brechen, im Ringkampfe: wie mit Licht und Schatten sie wider einander streben, 
ch-p2-07-v36 [en] | trailing dash artifact | How divinely do vault and arch here contrast in the struggle: how with light and shade they strive against each other, t
ch-p2-07-v36 [fr] | trailing dash artifact | Ici les voûtes et les arceaux se brisent divinement dans la lutte: la lumière et l'ombre se combattent en un divin effor
ch-p2-07-v37 [de] | trailing dash artifact | Also sicher und schön lasst uns auch Feinde sein, meine Freunde! Göttlich wollen wir wider einander streben!—
ch-p2-07-v37 [en] | trailing dash artifact | Thus, steadfast and beautiful, let us also be enemies, my friends! Divinely will we strive AGAINST one another!—
ch-p2-07-v37 [fr] | trailing dash artifact | De même, avec notre certitude et notre beauté, soyons ennemis, nous aussi, mes amis! Assemblons divinement nos efforts l
ch-p2-07-v42 [de] | trailing dash artifact | Wahrlich, kein Dreh- und Wirbelwind ist Zarathustra; und wenn er ein Tänzer ist, nimmermehr doch ein Tarantel-Tänzer!—
ch-p2-07-v42 [en] | trailing dash artifact | Verily, no cyclone or whirlwind is Zarathustra: and if he be a dancer, he is not at all a tarantula-dancer!—
ch-p2-07-v42 [fr] | trailing dash artifact | En vérité, Zarathoustra n'est pas un tourbillon et une trombe; et s'il est danseur, ce n'est pas un danseur de tarentell
ch-p2-07-v42 [es] | trailing dash artifact | En verdad, no es Zaratustra un viento que dé vueltas, ni un remolino; y si es un bailarín, ¡nunca será un bailarín picad
ch-p2-08-v27 [es] | digit glued to letter (OCR) | Yla ceguera del ciego y su buscar y tantear deben seguir dando testimonio del p9der del sol al que miró - ¿sabíais ya es
ch-p2-08-v38 [de] | trailing dash artifact | Aber ihr Diener des Volkes, ihr berühmten Weisen,—wie könntet ihr mit mir gehn!—
ch-p2-08-v38 [en] | trailing dash artifact | But ye servants of the people, ye famous wise ones—how COULD ye go with me!—
ch-p2-08-v38 [fr] | trailing dash artifact | Mais, vous qui êtes serviteurs du peuple, sages illustres, - comment pourriez-vous venir avec moi? -
ch-p2-08-v38 [es] | trailing dash artifact | Pero vosotros servidores del pueblo, vosotros sabios famosos, - ¡cómo podríais vosotros marchar junto a mí! -
ch-p2-09-v04 [es] | trailing dash artifact | Es de noche: ahora se despiertan todas las canciones de los amantes. Y también mi alma es la canción de un amante. -
ch-p2-09-v28 [de] | trailing dash artifact | Nacht ist es: nun erst erwachen alle Lieder der Liebenden. Und auch meine Seele ist das Lied eines Liebenden.—
ch-p2-09-v28 [en] | trailing dash artifact | ‘Tis night: now do all songs of loving ones awake. And my soul also is the song of a loving one.—
ch-p2-09-v28 [fr] | trailing dash artifact | Il fait nuit: voici que s'éveillent tous les chants des amoureux. Et mon âme, elle aussi, est un chant d'amoureux.-
ch-p2-10-v09 [de] | trailing dash artifact | Ein Tanz- und Spottlied auf den Geist der Schwere, meinen allerhöchsten grossmächtigsten Teufel, von dem sie sagen, dass
ch-p2-10-v09 [en] | trailing dash artifact | A dance-song and satire on the spirit of gravity my supremest, powerfulest devil, who is said to be “lord of the world.”
ch-p2-10-v09 [fr] | trailing dash artifact | Un air de danse et une satire sur l'esprit de la lourdeur, sur ce démon très haut et tout puissant, dont ils disent qu'i
ch-p2-10-v15 [de] | trailing dash artifact | Ob ich schon euch Männern „die Tiefe“ heisse oder „die Treue“, „die Ewige“, „die Geheimnissvolle.“—
ch-p2-10-v30 [de] | trailing dash artifact | Ach, und nun machtest du wieder dein Auge auf, oh geliebtes Leben! Und in's Unergründliche schien ich mir wieder zu sink
ch-p2-10-v30 [en] | trailing dash artifact | Ah, and now hast thou again opened thine eyes, O beloved Life! And into the unfathomable have I again seemed to sink.—
ch-p2-10-v30 [fr] | trailing dash artifact | Hélas! tu rouvris alors les yeux, ô vie bien-aimée! Et il me semblait que je retombais dans l'abîme insondable. -
ch-p2-10-v30 [es] | trailing dash artifact | ¡Ay, y entonces volviste a abrir tus ojos, oh vida amada! Y en lo insondable me pareció hundirme allí de nuevo. -
ch-p2-10-v34 [de] | trailing dash artifact | Warum? Wofür? Wodurch? Wohin? Wo? Wie? Ist es nicht Thorheit, noch zu leben?—
ch-p2-10-v34 [en] | trailing dash artifact | Why? Wherefore? Whereby? Whither? Where? How? Is it not folly still to live?—
ch-p2-10-v34 [fr] | trailing dash artifact | Pourquoi? A quoi bon? De quoi? Où vas-tu? Où? Comment? N'est-ce pas folie que de vivre encore? -
ch-p2-10-v34 [es] | trailing dash artifact | ¿Por qué? ¿Para qué? ¿Con qué? ¿Hacia dónde? ¿Dónde? ¿Cómo? ¿No es tontería vivir todavía? -
ch-p2-11-v02 [de] | trailing dash artifact | Also im Herzen beschliessend fuhr ich über das Meer.—
ch-p2-11-v02 [en] | trailing dash artifact | Resolving thus in my heart, did I sail o’er the sea.—
ch-p2-11-v02 [fr] | trailing dash artifact | Ayant ainsi décidé dans mon coeur - je traversai la mer. -
ch-p2-11-v38 [de] | trailing dash artifact | Ja, noch bist du mir aller Gräber Zertrümmerer: Heil dir, mein Wille! Und nur wo Gräber sind, giebt es Auferstehungen.—
ch-p2-11-v38 [en] | trailing dash artifact | Yea, thou art still for me the demolisher of all graves: Hail to thee, my Will! And only where there are graves are ther
ch-p2-11-v38 [fr] | trailing dash artifact | Oui, tu demeures pour moi la destructrice de tous les tombeaux: salut à toi, ma volonté! Et ce n'est que là où il y a de
ch-p2-11-v38 [es] | trailing dash artifact | Sí, todavía eres tú para mí la que reduce a escombros todos los sepulcros: ¡salud a ti, voluntad mía! Y sólo donde hay s
ch-p2-11-v39 [de] | trailing dash artifact | Also sang Zarathustra.—
ch-p2-12-v16 [de] | trailing dash artifact | Diess aber ist das Dritte, was ich hörte: dass Befehlen schwerer ist, als Gehorchen. Und nicht nur, dass der Befehlende 
ch-p2-12-v16 [en] | trailing dash artifact | This, however, is the third thing which I heard—namely, that commanding is more difficult than obeying. And not only bec
ch-p2-12-v16 [fr] | trailing dash artifact | Voici ce que j'entendis en troisième lieu: commander est plus difficile qu'obéir. Car celui qui commande porte aussi le 
ch-p2-12-v35 [de] | trailing dash artifact | Vieles ist dem Lebenden höher geschätzt, als Leben selber; doch aus dem Schätzen selber heraus redet—der Wille zur Macht
ch-p2-12-v35 [en] | trailing dash artifact | Much is reckoned higher than life itself by the living one; but out of the very reckoning speaketh—the Will to Power!”—
ch-p2-12-v40 [es] | digit glued to letter (OCR) | Yquien tiene que ser un creador en el bien y en el mal2º2: en verdad, ése tiene que ser antes un aniquilador y quebranta
ch-p2-12-v41 [de] | trailing dash artifact | Also gehört das höchste Böse zur höchsten Güte: diese aber ist die schöpferische.—
ch-p2-12-v41 [en] | trailing dash artifact | Thus doth the greatest evil pertain to the greatest good: that, however, is the creating good.—
ch-p2-12-v41 [fr] | trailing dash artifact | Ainsi la plus grande malignité fait partie de la plus grande bénignité: mais cette bénignité est la bénignité du créateu
ch-p2-12-v43 [en] | trailing dash artifact | And let everything break up which—can break up by our truths! Many a house is still to be built!—
ch-p2-12-v43 [fr] | trailing dash artifact | Et que soit brisé tout ce qui peut être brisé par nos vérités! Il y a encore bien des maisons à construire! -
ch-p2-13-v35 [en] | trailing dash artifact | For this is the secret of the soul: when the hero hath abandoned it, then only approacheth it in dreams—the superhero.—
ch-p2-13-v35 [fr] | trailing dash artifact | Car ceci est le secret de l'âme: quand le héros a abandonné l'âme, c'est alors seulement que s'approche en rêve - le sup
ch-p2-14-v09 [es] | soft-hyphen U+00AD present; trailing dash artifact | ¡En verdad, no podríais llevar mejor máscara, hombres del presente, que vuestro propio rostro! ¡Quién podría reconoce­ -
ch-p2-14-v22 [de] | trailing dash artifact | Unfruchtbare seid ihr: darum fehlt es euch an Glauben. Aber wer schaffen musste, der hatte auch immer seine Wahr-Träume 
ch-p2-14-v22 [en] | trailing dash artifact | Unfruitful are ye: THEREFORE do ye lack belief. But he who had to create, had always his presaging dreams and astral pre
ch-p2-14-v22 [fr] | trailing dash artifact | Vous êtes stériles: c'est pourquoi vous manquez de foi. Mais celui qui devait créer possédait toujours ses rêves et ses 
ch-p2-14-v29 [es] | soft-hyphen U+00AD present | Pero quiero tomaros a la ligera, pues yo tengo que llevar co ­ sas pesadas; ¡y qué me importa el que escarabajos y gusan
ch-p2-14-v30 [en] | trailing dash artifact | Verily, it shall not on that account become heavier to me! And not from you, ye present-day men, shall my great wearines
ch-p2-14-v30 [fr] | trailing dash artifact | En vérité mon fardeau n'en sera pas plus lourd! Et ce n'est pas de vous, mes contemporains, que me viendra la grande fat
ch-p2-14-v34 [en] | trailing dash artifact | Unto my children will I make amends for being the child of my fathers: and unto all the future—for THIS present-day!—
ch-p2-14-v34 [fr] | trailing dash artifact | Je veux me racheter auprès de mes enfants d'avoir été le fils de mes pères: je veux racheter de tout l'avenir - ce prése
ch-p2-15-v07 [de] | trailing dash artifact | Jedes Redlichen Schritt redet; die Katze aber stiehlt sich über den Boden weg. Siehe, katzenhaft kommt der Mond daher un
ch-p2-15-v07 [en] | trailing dash artifact | Every honest one’s step speaketh; the cat however, stealeth along over the ground. Lo! cat-like doth the moon come along
ch-p2-15-v07 [fr] | trailing dash artifact | Les pas d'un homme loyal parlent; mais le chat marche à pas furtifs. Voyez, la lune s'avance, déloyale comme un chat. -
ch-p2-15-v15 [de] | trailing dash artifact | Und das heisse mir aller Dinge unbefleckte Erkenntniss, dass ich von den Dingen Nichts will: ausser dass ich vor ihnen d
ch-p2-15-v15 [en] | trailing dash artifact | And this do I call IMMACULATE perception of all things: to want nothing else from them, but to be allowed to lie before 
ch-p2-15-v15 [fr] | trailing dash artifact | "Et voici ce que j'appelle l'immaculée connaissance de toutes choses: ne rien demander aux choses que de pouvoir s'étend
ch-p2-15-v39 [en] | trailing dash artifact | And this meaneth TO ME knowledge: all that is deep shall ascend—to my height!—
ch-p2-15-v39 [fr] | trailing dash artifact | Et ceci est pour moi la connaissance: tout ce qui est profond doit monter - à ma hauteur! -
ch-p2-16-v26 [en] | trailing dash artifact | For men are NOT equal: so speaketh justice. And what I will, THEY may not will!—
ch-p2-16-v26 [fr] | trailing dash artifact | Car les hommes ne sont point égaux: ainsi parle la justice. Et ce que je veux ils n'auraient pas le droit de le vouloir!
ch-p2-17-v10 [en] | trailing dash artifact | The disciple answered: “I believe in Zarathustra.” But Zarathustra shook his head and smiled.—
ch-p2-17-v12 [es] | trailing dash artifact | Pero en el supuesto de que alguien dijera con toda seriedad que los poetas mienten demasiado: tiene razón, nosotros -
ch-p2-17-v23 [de] | trailing dash artifact | Wahrlich, immer zieht es uns hinan—nämlich zum Reich der Wolken: auf diese setzen wir unsre bunten Bälge und heissen sie
ch-p2-17-v23 [en] | trailing dash artifact | Verily, ever are we drawn aloft—that is, to the realm of the clouds: on these do we set our gaudy puppets, and then call
ch-p2-17-v24 [en] | trailing dash artifact | Are not they light enough for those chairs!—all these Gods and Supermen?—
ch-p2-17-v26 [en] | trailing dash artifact | When Zarathustra so spake, his disciple resented it, but was silent. And Zarathustra also was silent; and his eye direct
ch-p2-17-v31 [de] | trailing dash artifact | Gespenster-Hauch und -Huschen gilt mir all ihr Harfen-Klingklang; was wussten sie bisher von der Inbrunst der Töne!—
ch-p2-17-v31 [en] | trailing dash artifact | Ghost-breathing and ghost-whisking, seemeth to me all the jingle-jangling of their harps; what have they known hitherto 
ch-p2-17-v31 [fr] | trailing dash artifact | Leurs arpèges m'apparaissent comme des glissements des fuites de fantômes; que connaissaient-ils jusqu'à présent de l'ar
ch-p2-17-v33 [de] | trailing dash artifact | Und gerne geben sie sich damit als Versöhner: aber Mittler und Mischer bleiben sie mir und Halb-und-Halbe und Unreinlich
ch-p2-17-v33 [en] | trailing dash artifact | And fain would they thereby prove themselves reconcilers: but mediaries and mixers are they unto me, and half-and-half, 
ch-p2-17-v33 [fr] | trailing dash artifact | Ils aiment à se faire passer pour conciliateurs, mais ils restent toujours pour moi des gens de moyens-termes et de demi
ch-p2-17-v42 [de] | trailing dash artifact | Zuschauer will der Geist des Dichters: sollten's auch Büffel sein!—
ch-p2-17-v42 [en] | trailing dash artifact | Spectators, seeketh the spirit of the poet—should they even be buffaloes!—
ch-p2-17-v42 [fr] | trailing dash artifact | L'esprit du poète veut des spectateurs: ne fût-ce que des buffles! -
ch-p2-17-v45 [en] | trailing dash artifact | Penitents of the spirit have I seen appearing; they grew out of the poets.—
ch-p2-17-v45 [fr] | trailing dash artifact | J'ai vu venir des expiateurs de l'esprit: c'est parmi les poètes qu'ils sont nés. -
ch-p2-18-v03 [de] | trailing dash artifact | „Seht mir an! sagte der alte Steuermann, da fährt Zarathustra zur Hölle!“—
ch-p2-18-v03 [fr] | trailing dash artifact | "Voyez donc! dit le vieux pilote, voilà Zarathoustra qui va en enfer!" -
ch-p2-18-v04 [es] | digit glued to letter (OCR) | «¡Mirad!, dijo el viejo timonel, ¡ahí va Zaratustra al infierno!»z39_
ch-p2-18-v23 [de] | trailing dash artifact | Diesen Rath aber rathe ich Königen und Kirchen und Allem, was alters- und tugendschwach ist—lasst euch nur umstürzen! Da
ch-p2-18-v23 [fr] | trailing dash artifact | Mais c'est le conseil que je donne aux rois et aux Églises, et à tout ce qui s'est affaibli par l'âge et par la vertu - 
ch-p2-18-v27 [de] | trailing dash artifact | Denn er will durchaus das wichtigste Thier auf Erden sein, der Staat; und man glaubt's ihm auch.—
ch-p2-18-v27 [fr] | trailing dash artifact | Car l'État veut absolument être la bête la plus importante sur la terre; et tout le monde croit qu'il l'est." -
ch-p2-18-v35 [de] | trailing dash artifact | Als diess der Feuerhund vernahm, hielt er's nicht mehr aus, mir zuzuhören. Beschämt zog er seinen Schwanz ein, sagte auf
ch-p2-18-v35 [en] | trailing dash artifact | When the fire-dog heard this, he could no longer endure to listen to me. Abashed did he draw in his tail, said “bow-wow!
ch-p2-18-v35 [fr] | trailing dash artifact | Lorsque le chien de feu entendit ces paroles, il lui fut impossible de m'écouter davantage. Honteusement il rentra sa qu
ch-p2-18-v42 [de] | trailing dash artifact | Wozu ist es denn—höchste Zeit?“—
ch-p2-18-v42 [en] | trailing dash artifact | For what is it then—the highest time?”—
ch-p2-18-v42 [fr] | trailing dash artifact | Pour quoi peut-il être - grand temps?" -
ch-p2-18-v42 [es] | trailing dash artifact | ¿De qué - ha llegado la hora?» -
ch-p2-19-v09 [de] | trailing dash artifact | Wahrlich, zum Sterben wurden wir schon zu müde; nun wachen wir noch und leben fort—in Grabkammern!“—
ch-p2-19-v09 [es] | trailing dash artifact | En verdad, estamos demasiado cansados incluso para morir; ahora continuamos estando en vela y sobrevivimos - ¡en cámaras
ch-p2-19-v10 [en] | trailing dash artifact | Thus did Zarathustra hear a soothsayer speak; and the foreboding touched his heart and transformed him. Sorrowfully did 
ch-p2-19-v32 [de] | trailing dash artifact | Aber der eigne Schrei weckte mich auf:—und ich kam zu mir.—
ch-p2-19-v32 [en] | trailing dash artifact | But mine own crying awoke me:—and I came to myself.—
ch-p2-19-v32 [fr] | trailing dash artifact | Mais mon propre cri me réveilla: - et je revins à moi. -
ch-p2-19-v43 [de] | trailing dash artifact | Aber wie du von ihnen aufwachtest und zu dir kamst, also sollen sie selber von sich aufwachen—und zu dir kommen!“—
ch-p2-19-v43 [fr] | trailing dash artifact | Mais comme tu t'est réveillé d'eux et que tu es revenu à toi-même, ainsi ils doivent se réveiller d'eux-mêmes - et venir
ch-p2-19-v46 [en] | trailing dash artifact | The soothsayer, however, shall eat and drink at my side: and verily, I will yet show him a sea in which he can drown him
ch-p2-19-v47 [de] | trailing dash artifact | Also sprach Zarathustra. Darauf aber blickte er dem jünger, welcher den Traumdeuter abgegeben hatte, lange in's Gesicht 
ch-p2-19-v47 [en] | trailing dash artifact | Thus spake Zarathustra. Then did he gaze long into the face of the disciple who had been the dream-interpreter, and shoo
ch-p2-19-v47 [fr] | trailing dash artifact | Ainsi parlait Zarathoustra. Mais alors il regarda longtemps en plein visage le disciple qui lui avait expliqué son rêve,
ch-p2-19-v47 [es] | trailing dash artifact | Así habló Zaratustra. Luego estuvo mirando largo tiempo al rostro del discípulo que había hecho de intérprete del sueño,
ch-p2-20-v04 [es] | soft-hyphen U+00AD present | Mas, desde que estoy entre hombres, para mí lo de menos es ver: "A éste le falta un ojo, y a aquél una oreja, y a aquel 
ch-p2-20-v29 [es] | soft-hyphen U+00AD present | Esto, sí, esto solo es la venganza misma: la aversión de la vo­ ,, luntad contra el tiempo y su "Fue .
ch-p2-20-v35 [es] | digit glued to letter (OCR) | "Y la justicia misma consiste en aquella ley del tiempo según la cual tiene éste que devorar a sus propios hijos260": as
ch-p2-20-v41 [en] | trailing dash artifact | All “It was” is a fragment, a riddle, a fearful chance—until the creating Will saith thereto: “But thus would I have it.
ch-p2-20-v48 [de] | trailing dash artifact | „Es ist schwer, mit Menschen zu leben, weil Schweigen so schwer ist. Sonderlich für einen Geschwätzigen.“—
ch-p2-20-v48 [en] | trailing dash artifact | “It is difficult to live amongst men, because silence is so difficult— especially for a babbler.”—
ch-p2-20-v48 [fr] | trailing dash artifact | "Il est difficile de vivre parmi les hommes, parce qu'il est si difficile de se taire. Surtout pour un bavard." -
ch-p2-20-v48 [es] | soft-hyphen U+00AD present | - En este momento de su discurso ocurrió que Zaratustra se detuvo de repente, y semejaba del todo alguien que estuviese 
ch-p2-20-v52 [es] | trailing dash artifact | «Bien, dijo el jorobado; y con discípulos es lícito charlar de manera discipular Mas ¿por qué Zaratustra habla a sus dis
ch-p2-20-v53 [de] | trailing dash artifact | Aber warum redet Zarathustra anders zu seinen Schülern—als zu sich selber?“—
ch-p2-20-v53 [en] | trailing dash artifact | But why doth Zarathustra speak otherwise unto his pupils—than unto himself?”—
ch-p2-21-v23 [de] | trailing dash artifact | Und wenn das die rechte Tugend ist, die nicht um sich selber weiss: nun, der Eitle weiss nicht um seine Bescheidenheit!—
ch-p2-21-v23 [en] | trailing dash artifact | And if that be the true virtue which is unconscious of itself—well, the vain man is unconscious of his modesty!—
ch-p2-21-v23 [fr] | trailing dash artifact | Et si la vraie vertu est celle qui ne sait rien d'elle-même, eh bien! le vaniteux ne sait rien de sa modestie! -
ch-p2-21-v40 [de] | trailing dash artifact | Aber verkleidet will ich euch sehn, ihr Nächsten und Mitmenschen, und gut geputzt, und eitel, und würdig, als „die Guten
ch-p2-21-v40 [en] | trailing dash artifact | But disguised do I want to see YOU, ye neighbours and fellowmen, and well-attired and vain and estimable, as “the good a
ch-p2-21-v40 [fr] | trailing dash artifact | Mais je veux vous voir travestis, vous, ô hommes, mes frères et mes prochains, et bien parés, et vaniteux, et dignes, vo
ch-p2-21-v41 [en] | trailing dash artifact | And disguised will I myself sit amongst you—that I may MISTAKE you and myself: for that is my last manly prudence.—
ch-p2-21-v41 [fr] | trailing dash artifact | Et je veux être assis parmi vous, travesti moi-même, afin de vous méconnaître et de me méconnaître moi-même: car ceci es
ch-p2-22-v06 [de] | trailing dash artifact | Kennt ihr den Schrecken des Einschlafenden?—
ch-p2-22-v06 [en] | trailing dash artifact | Do ye know the terror of him who falleth asleep?—
ch-p2-22-v06 [fr] | trailing dash artifact | Connaissez-vous la terreur de celui qui s'endort? -
ch-p2-22-v10 [de] | trailing dash artifact | Dann sprach es ohne Stimme zu mir: „Du weisst es, Zarathustra?“—
ch-p2-22-v10 [en] | trailing dash artifact | Then was there spoken unto me without voice: “THOU KNOWEST IT, ZARATHUSTRA?”—
ch-p2-22-v10 [fr] | trailing dash artifact | Soudain j'entendis l'Autre qui me disait sans voix: "Tu le sais Zarathoustra." -
ch-p2-22-v12 [de] | trailing dash artifact | Da sprach es abermals ohne Stimme zu mir: „Du weisst es, Zarathustra, aber du redest es nicht!“—
ch-p2-22-v12 [en] | trailing dash artifact | Then was there once more spoken unto me without voice: “Thou knowest it, Zarathustra, but thou dost not speak it!”—
ch-p2-22-v12 [fr] | trailing dash artifact | Alors l'Autre reprit sans voix: "Tu le sais, Zarathoustra, mais tu ne le dis pas!" -
ch-p2-22-v14 [de] | trailing dash artifact | Da sprach es wieder ohne Stimme zu mir: „Du willst nicht, Zarathustra? Ist diess auch wahr? Verstecke dich nicht in dein
ch-p2-22-v14 [en] | trailing dash artifact | Then was there again spoken unto me without voice: “Thou WILT not, Zarathustra? Is this true? Conceal thyself not behind
ch-p2-22-v14 [fr] | trailing dash artifact | Alors l'Autre reprit sans voix: "Tu ne veux pas, Zarathoustra? Est-ce vrai? Ne te cache pas derrière cet air de défi!" -
ch-p2-22-v16 [de] | trailing dash artifact | Da sprach es wieder ohne Stimme zu mir: „Was liegt an dir, Zarathustra! Sprich dein Wort und zerbrich!“—
ch-p2-22-v16 [fr] | trailing dash artifact | Alors l'Autre repris sans voix: "Qu'importe de toi, Zarathoustra? Dis ta parole et brise-toi!" -
ch-p2-22-v18 [de] | trailing dash artifact | Da sprach es wieder ohne Stimme zu mir: „Was liegt an dir? Du bist mir noch nicht demüthig genug. Die Demuth hat das här
ch-p2-22-v18 [en] | trailing dash artifact | Then was there again spoken unto me without voice: “What matter about thyself? Thou art not yet humble enough for me. Hu
ch-p2-22-v20 [de] | trailing dash artifact | Da sprach es wieder ohne Stimme zu mir: „Oh Zarathustra, wer Berge zu versetzen hat, der versetzt auch Thäler und Nieder
ch-p2-22-v20 [en] | trailing dash artifact | Then was there again spoken unto me without voice: “O Zarathustra, he who hath to remove mountains removeth also valleys
ch-p2-22-v20 [fr] | trailing dash artifact | Alors l'Autre reprit sans voix: "O Zarathoustra, qui a des montagnes à déplacer, déplace aussi des vallées et des bas-fo
ch-p2-22-v22 [de] | trailing dash artifact | Da sprach es wieder ohne Stimme zu mir: „Was weisst du davon! Der Thau fällt auf das Gras, wenn die Nacht am verschwiege
ch-p2-22-v22 [en] | trailing dash artifact | Then was there again spoken unto me without voice: “What knowest thou THEREOF! The dew falleth on the grass when the nig
ch-p2-22-v22 [fr] | trailing dash artifact | Alors l'Autre reprit sans voix: "Qu'en sais-tu? La rosée tombe sur l'herbe au moment le plus silencieux de la nuit." -
ch-p2-22-v22 [es] | trailing dash artifact | Entonces algo me habló de nuevo sin voz: «¡Qué sabes tú de eso! El rocío cae sobre la hierba cuando la noche está más ca
ch-p2-22-v25 [es] | raw < or > present | Yasí me dijeron: ¡has olvidado el camino, y ahora olvidas también hasta el andar!>' Entonces algo me habló de nuevo sin 
ch-p2-22-v28 [de] | trailing dash artifact | Das ist dein Unverzeihlichstes: du hast die Macht, und du willst nicht herrschen.“—
ch-p2-22-v28 [en] | trailing dash artifact | This is thy most unpardonable obstinacy: thou hast the power, and thou wilt not rule.”—
ch-p2-22-v31 [de] | trailing dash artifact | Oh Zarathustra, du sollst gehen als ein Schatten dessen, was kommen muss: so wirst du befehlen und befehlend vorangehen.
ch-p2-22-v31 [en] | trailing dash artifact | O Zarathustra, thou shalt go as a shadow of that which is to come: thus wilt thou command, and in commanding go foremost
ch-p2-22-v31 [fr] | trailing dash artifact | O Zarathoustra, tu dois aller comme le fantôme de ce qui viendra un jour; ainsi tu commanderas et, en commandant, tu ira
ch-p2-22-v34 [de] | trailing dash artifact | Der Stolz der Jugend ist noch auf dir, spät bist du jung geworden: aber wer zum Kinde werden will, muss auch noch seine 
ch-p2-22-v34 [en] | trailing dash artifact | The pride of youth is still upon thee; late hast thou become young: but he who would become a child must surmount even h
ch-p2-22-v34 [fr] | trailing dash artifact | L'orgueil de la jeunesse est encore sur toi, tu es devenu jeune sur le tard: mais celui qui veut devenir enfant doit sur
ch-p2-22-v38 [de] | trailing dash artifact | So musst du wieder in die Einsamkeit: denn du sollst noch mürbe werden.“—
ch-p2-22-v38 [en] | trailing dash artifact | So must thou go again into solitude: for thou shalt yet become mellow.”—
ch-p2-22-v38 [fr] | trailing dash artifact | Il te faut donc retourner à la solitude, afin que ta dureté s'amollisse davantage." -
ch-p2-22-v38 [es] | trailing dash artifact | Por ello tienes que volver de nuevo a la soledad: pues debes ponerte tierno aún.» -
ch-p2-22-v42 [de] | trailing dash artifact | Ach meine Freunde! Ich hätte euch noch Etwas zu sagen, ich hätte euch noch Etwas zu geben! Warum gebe ich es nicht? Bin 
ch-p2-22-v42 [en] | trailing dash artifact | Ah, my friends! I should have something more to say unto you! I should have something more to give unto you! Why do I no
ch-p2-22-v42 [es] | trailing dash artifact | ¡Ay, amigos míos! ¡Yo tendría aún algunas cosas que deciros, yo tendría aún algunas que daros! ¿Por qué no las doy? ¿Aca
ch-p3-01-v14 [es] | digit glued to letter (OCR) | Quien siempre se ha tratado a sí mismo con mucha indulgencia acaba por enfermar a causa de ello. ¡Alabado sea lo que end
ch-p3-01-v17 [en] | trailing dash artifact | Yea! To look down upon myself, and even upon my stars: that only would I call my SUMMIT, that hath remained for me as my
ch-p3-01-v17 [fr] | trailing dash artifact | Oui! Regarder en bas sur moi-même et sur mes étoiles: ceci seul serait pour moi le sommet, ceci demeure pour moi le dern
ch-p3-01-v17 [es] | trailing dash artifact | ¡Sí! Bajar la vista hacia mí mismo e incluso hacia mis estrellas: ¡sólo esto significaría mi cumbre, esto es lo que me h
ch-p3-01-v21 [es] | soft-hyphen U+00AD present | Me encuentro ante mi montaña más alta y ante mi más lar­ , ga caminata: por eso tengo primero que descender más bajo de 
ch-p3-01-v24 [de] | trailing dash artifact | Diess Zeugniss ist in ihr Gestein geschrieben und in die Wände ihrer Gipfel. Aus dem Tiefsten muss das Höchste zu seiner
ch-p3-01-v24 [en] | trailing dash artifact | That testimony is inscribed on their stones, and on the walls of their summits. Out of the deepest must the highest come
ch-p3-01-v24 [fr] | trailing dash artifact | Ce témoignage est écrit dans leurs rochers et dans les pics de leurs sommets. C'est du plus bas que le plus haut doit at
ch-p3-01-v24 [es] | trailing dash artifact | Este testimonio está escrito en sus rocas y en las paredes de sus cumbres. Lo más alto tiene que llegar a su altura desd
ch-p3-01-v30 [de] | trailing dash artifact | Ach, dass meine Hand nicht Stärke genug hat! Gerne, wahrlich, möchte ich dich von bösen Träumen erlösen!—
ch-p3-01-v30 [en] | trailing dash artifact | Ah, that my hand hath not strength enough! Gladly, indeed, would I free thee from evil dreams!—
ch-p3-01-v30 [fr] | trailing dash artifact | Hélas! pourquoi ma main n'a-t-elle pas assez de force! Que j'aimerais vraiment te délivrer des mauvais rêves! -
ch-p3-01-v30 [es] | trailing dash artifact | ¡Ay, por qué no tendrá mi mano bastante fortaleza! ¡En verdad, me gustaría redimirte de sueños malvados! -
ch-p3-01-v34 [de] | trailing dash artifact | Die Liebe ist die Gefahr des Einsamsten, die Liebe zu Allem, wenn es nur lebt! Zum Lachen ist wahrlich meine Narrheit un
ch-p3-01-v34 [en] | trailing dash artifact | LOVE is the danger of the lonesomest one, love to anything, IF IT ONLY LIVE! Laughable, verily, is my folly and my modes
ch-p3-01-v34 [fr] | trailing dash artifact | L'amour est le danger du plus solitaire; l'amour de toute chose pourvu qu'elle soit vivante! Elles prêtent vraiment à ri
ch-p3-01-v34 [es] | trailing dash artifact | El amor es el peligro del más solitario, el amor a todas las cosas, jcon tal de que vivan! ¡De risa son, en verdad, mi n
ch-p3-02-v02 [de] | trailing dash artifact | Euch, den kühnen Suchern, Versuchern, und wer je sich mit listigen Segeln auf furchtbare Meere einschiffte,—
ch-p3-02-v02 [en] | trailing dash artifact | To you, the daring venturers and adventurers, and whoever hath embarked with cunning sails upon frightful seas,—
ch-p3-02-v02 [fr] | trailing dash artifact | A vous, chercheurs hardis et aventureux, qui que vous soyez, vous qui vous êtes embarqués avec des voiles pleines d'astu
ch-p3-02-v02 [es] | trailing dash artifact | Avosotros los audaces buscadores e indagadores, y a quienquiera que alguna vez se haya lanzado con astutas velas a mares
ch-p3-02-v04 [de] | trailing dash artifact | —denn nicht wollt ihr mit feiger Hand einem Faden nachtasten; und, wo ihr errathen könnt, da hasst ihr es, zu erschliess
ch-p3-02-v04 [en] | trailing dash artifact | —For ye dislike to grope at a thread with cowardly hand; and where ye can DIVINE, there do ye hate to CALCULATE—
ch-p3-02-v04 [fr] | trailing dash artifact | car vous ne voulez pas tâtonner d'une main peureuse le long du fil conducteur; et partout où vous pouvez deviner, vous d
ch-p3-02-v05 [de] | trailing dash artifact | euch allein erzähle ich das Räthsel, das ich sah,—das Gesicht des Einsamsten.—
ch-p3-02-v05 [en] | trailing dash artifact | To you only do I tell the enigma that I SAW—the vision of the lonesomest one.—
ch-p3-02-v05 [fr] | trailing dash artifact | c'est à vous seuls que je raconte l'énigme que j'ai vue, - la vision du plus solitaire. -
ch-p3-02-v15 [de] | trailing dash artifact | Ich stieg, ich stieg, ich träumte, ich dachte,—aber Alles drückte mich. Einem Kranken glich ich, den seine schlimme Mart
ch-p3-02-v15 [en] | trailing dash artifact | I ascended, I ascended, I dreamt, I thought,—but everything oppressed me. A sick one did I resemble, whom bad torture we
ch-p3-02-v15 [fr] | trailing dash artifact | Je montai, je montai davantage, en rêvant et en pensant, - mais tout m'oppressait. Je ressemblais à un malade que fatigu
ch-p3-02-v16 [de] | trailing dash artifact | Aber es giebt Etwas in mir, das ich Muth heisse: das schlug bisher mir jeden Unmuth todt. Dieser Muth hiess mich endlich
ch-p3-02-v16 [en] | trailing dash artifact | But there is something in me which I call courage: it hath hitherto slain for me every dejection. This courage at last b
ch-p3-02-v16 [fr] | trailing dash artifact | Mais il y a quelque chose en moi que j'appelle courage: c'est ce qui a fait faire jusqu'à présent en moi tout mouvement 
ch-p3-02-v22 [de] | trailing dash artifact | In solchem Spruche aber ist viel klingendes Spiel. Wer Ohren hat, der höre.—
ch-p3-02-v22 [en] | trailing dash artifact | In such speech, however, there is much sound of triumph. He who hath ears to hear, let him hear.—
ch-p3-02-v22 [fr] | trailing dash artifact | Dans une telle maxime, il y a beaucoup de fanfare. Que celui qui a des oreilles entende. -
ch-p3-02-v22 [es] | trailing dash artifact | En estas palabras, sin embargo, hay mucho sonido de tambor batiente. Quien tenga oídos, oiga. -
ch-p3-02-v23 [de] | trailing dash artifact | „Halt! Zwerg! sprach ich. Ich! Oder du! Ich aber bin der Stärkere von uns Beiden—: du kennst meinen abgründlichen Gedank
ch-p3-02-v23 [fr] | trailing dash artifact | "Arrête-toi! nain! dis-je. Moi ou bien toi! Mais moi je suis le plus fort de nous deux -: tu ne connais pas ma pensée la
ch-p3-02-v28 [de] | trailing dash artifact | Aber wer Einen von ihnen weiter gienge—und immer weiter und immer ferner: glaubst du, Zwerg, dass diese Wege sich ewig w
ch-p3-02-v28 [en] | trailing dash artifact | But should one follow them further—and ever further and further on, thinkest thou, dwarf, that these roads would be eter
ch-p3-02-v28 [fr] | trailing dash artifact | Mais si quelqu'un suivait l'un de ces chemins - en allant toujours plus loin: crois-tu nain, que ces chemins seraient en
ch-p3-02-v35 [de] | trailing dash artifact | Denn, was laufen kann von allen Dingen: auch in dieser langen Gasse hinaus—muss es einmal noch laufen!—
ch-p3-02-v35 [en] | trailing dash artifact | For whatever CAN run its course of all things, also in this long lane OUTWARD—MUST it once more run!—
ch-p3-02-v35 [fr] | trailing dash artifact | Car toute chose qui sait courir ne doit-elle pas suivre une seconde fois cette longue route qui monte! -
ch-p3-02-v35 [es] | trailing dash artifact | Pues cada una de las cosas que pueden correr: ¡también por esa larga calle hacia adelante - tiene que volver a correr un
ch-p3-02-v37 [en] | trailing dash artifact | —And must we not return and run in that other lane out before us, that long weird lane—must we not eternally return?”—
ch-p3-02-v40 [fr] | trailing dash artifact | c'est alors que j'entendis un chien hurler ainsi. Et je le vis aussi, le poil hérissé, le cour tendu, tremblant, au mili
ch-p3-02-v41 [de] | trailing dash artifact | —also dass es mich erbarmte. Eben nämlich gieng der volle Mond, todtschweigsam, über das Haus, eben stand er still, eine
ch-p3-02-v41 [en] | trailing dash artifact | —So that it excited my commiseration. For just then went the full moon, silent as death, over the house; just then did i
ch-p3-02-v44 [es] | trailing dash artifact | ¡Pero allíyacía por tierra un hombre! ¡Y allí! El perro saltando, con el pelo erizado, gimiendo, - ahora él me veía veni
ch-p3-02-v48 [de] | trailing dash artifact | Den Kopf ab! Beiss zu!“—so schrie es aus mir, mein Grauen, mein Hass, mein Ekel, mein Erbarmen, all mein Gutes und Schli
ch-p3-02-v48 [en] | trailing dash artifact | Its head off! Bite!”—so cried it out of me; my horror, my hatred, my loathing, my pity, all my good and my bad cried wit
ch-p3-02-v48 [fr] | trailing dash artifact | Arrache-lui la tête! Mords toujours!" - C'est ainsi que quelque chose se mit à crier en moi; mon épouvante, ma haine, mo
ch-p3-02-v53 [de] | trailing dash artifact | —Der Hirt aber biss, wie mein Schrei ihm rieth; er biss mit gutem Bisse! Weit weg spie er den Kopf der Schlange—: und sp
ch-p3-02-v53 [en] | trailing dash artifact | —The shepherd however bit as my cry had admonished him; he bit with a strong bite! Far away did he spit the head of the 
ch-p3-02-v53 [fr] | trailing dash artifact | Le berger cependant se mit à mordre comme mon cri le lui conseillait, il mordit d'un bon coup de dent! Il cracha loin de
ch-p3-02-v56 [de] | trailing dash artifact | Meine Sehnsucht nach diesem Lachen frisst an mir: oh wie ertrage ich noch zu leben! Und wie ertrüge ich's, jetzt zu ster
ch-p3-02-v56 [en] | trailing dash artifact | My longing for that laughter gnaweth at me: oh, how can I still endure to live! And how could I endure to die at present
ch-p3-02-v56 [fr] | trailing dash artifact | Le désir de ce rire me ronge: oh! comment supporterais-je de mourir maintenant! -
ch-p3-02-v56 [es] | trailing dash artifact | Mi anhelo de esa risa me devora: ¡oh, cómo soporto el vivir aún! ¡Y cómo soportaría el morir ahora! -
ch-p3-03-v15 [de] | trailing dash artifact | Erkannt und geprüft soll er werden, darauf, ob er meiner Art und Abkunft ist,—ob er eines langen Willens Herr sei, schwe
ch-p3-03-v15 [en] | trailing dash artifact | Recognised and tested shall each be, to see if he be of my type and lineage:—if he be master of a long will, silent even
ch-p3-03-v15 [fr] | trailing dash artifact | Il faut qu'il soit reconnu et éprouvé, pour que l'on sache s'il est de ma race et de mon origine, s'il est maître d'une 
ch-p3-03-v30 [de] | trailing dash artifact | Wenn ich mich dessen erst überwunden habe, dann will ich mich auch des Grösseren noch überwinden; und ein Sieg soll mein
ch-p3-03-v30 [en] | trailing dash artifact | When I shall have surmounted myself therein, then will I surmount myself also in that which is greater; and a VICTORY sh
ch-p3-03-v30 [fr] | trailing dash artifact | Quand j'aurai surmonté cela en moi, je surmonterai une plus grande chose encore, et une victoire sera le sceau de mon ac
ch-p3-03-v38 [en] | trailing dash artifact | There, already approacheth eventide: the sun sinketh. Away—my happiness!—
ch-p3-03-v38 [fr] | trailing dash artifact | Déjà le soir approche: le soleil se couche. Mon bonheur - s'en est allé! -
ch-p3-03-v38 [es] | trailing dash artifact | Ya se aproxima el anochecer: el sol se pone. ¡Vete - felicidad mía! -
ch-p3-04-v10 [de] | trailing dash artifact | Zusammen lernten wir Alles; zusammen lernten wir über uns zu uns selber aufsteigen und wolkenlos lächeln:—
ch-p3-04-v10 [en] | trailing dash artifact | Together did we learn everything; together did we learn to ascend beyond ourselves to ourselves, and to smile uncloudedl
ch-p3-04-v18 [de] | trailing dash artifact | Und oft gelüstete mich, sie mit zackichten Blitz-Golddrähten festzuheften, dass ich, gleich dem Donner, auf ihrem Kessel
ch-p3-04-v18 [en] | trailing dash artifact | And oft have I longed to pin them fast with the jagged gold-wires of lightning, that I might, like the thunder, beat the
ch-p3-04-v32 [de] | trailing dash artifact | Oh Himmel über mir, du Reiner! Hoher! Das ist mir nun deine Reinheit, dass es keine ewige Vernunft-Spinne und -Spinnenne
ch-p3-04-v32 [en] | trailing dash artifact | O heaven above me! thou pure, thou lofty heaven! This is now thy purity unto me, that there is no eternal reason-spider 
ch-p3-04-v33 [de] | trailing dash artifact | —dass du mir ein Tanzboden bist für göttliche Zufälle, dass du mir ein Göttertisch bist für göttliche Würfel und Würfels
ch-p3-04-v33 [en] | trailing dash artifact | —That thou art to me a dancing-floor for divine chances, that thou art to me a table of the Gods, for divine dice and di
ch-p3-04-v33 [fr] | trailing dash artifact | O ciel au-dessus de moi, ciel pur et haut! Ceci est maintenant pour moi ta pureté qu'il n'existe pas d'éternelles araign
ch-p3-04-v37 [de] | trailing dash artifact | Oh Himmel über mir, du Schamhafter! Glühender! Oh du mein Glück vor Sonnen-Aufgang! Der Tag kommt: so scheiden wir nun!—
ch-p3-04-v37 [en] | trailing dash artifact | O heaven above me, thou modest one! thou glowing one! O thou, my happiness before sunrise! The day cometh: so let us par
ch-p3-04-v37 [fr] | trailing dash artifact | O ciel au-dessus de moi, ciel pudique et ardent! O bonheur avant le soleil levant! Le jour vient: séparons-nous donc! -
ch-p3-04-v37 [es] | trailing dash artifact | Oh cielo por encima de mí, ¡tú pudoroso!, ¡ardiente! ¡Oh tú felicidad mía antes de la salida del sol! El día viene: ¡por
ch-p3-05-v07 [de] | trailing dash artifact | Oh wann komme ich wieder in meine Heimat, wo ich mich nicht mehr bücken muss—nicht mehr bücken muss vor den Kleinen!“—Un
ch-p3-05-v07 [en] | trailing dash artifact | Oh, when shall I arrive again at my home, where I shall no longer have to stoop—shall no longer have to stoop BEFORE THE
ch-p3-05-v36 [es] | raw < or > present | Abrazar modestamente una pequeña felicidad - ¡a esto lo llaman ellos «resignación>>! Y, al hacerlo, ya bizquean con mode
ch-p3-05-v38 [de] | trailing dash artifact | Diess aber ist Feigheit: ob es schon „Tugend“ heisst.—
ch-p3-05-v38 [en] | trailing dash artifact | That, however, is COWARDICE, though it be called “virtue.”—
ch-p3-05-v38 [fr] | trailing dash artifact | Mais c'est là de la lâcheté: bien que cela s'appelle "vertu". -
ch-p3-05-v43 [de] | trailing dash artifact | Diess aber ist—Mittelmässigkeit: ob es schon Mässigkeit heisst.—
ch-p3-05-v43 [en] | trailing dash artifact | That, however, is—MEDIOCRITY, though it be called moderation.—
ch-p3-05-v43 [fr] | trailing dash artifact | Mais c'est là - de la médiocrité: bien que cela s'appelle modération. -
ch-p3-05-v43 [es] | trailing dash artifact | Pero esto es mediocridad: aunque se llame moderación. - -
ch-p3-05-v53 [de] | trailing dash artifact | Und wahrlich, mancher Zufall kam herrisch zu mir: aber herrischer noch sprach zu ihm mein Wille,—da lag er schon bittend
ch-p3-05-v53 [en] | trailing dash artifact | And verily, many a chance came imperiously unto me: but still more imperiously did my WILL speak unto it,—then did it li
ch-p3-05-v54 [de] | trailing dash artifact | —bittend, dass er Herberge finde und Herz bei mir, und schmeichlerisch zuredend: „sieh doch; oh Zarathustra, wie nur Fre
ch-p3-05-v54 [en] | trailing dash artifact | —Imploring that it might find home and heart with me, and saying flatteringly: “See, O Zarathustra, how friend only come
ch-p3-05-v56 [de] | trailing dash artifact | Ihr werdet immer kleiner, ihr kleinen Leute! Ihr bröckelt ab, ihr Behaglichen! Ihr geht mir noch zu Grunde—
ch-p3-05-v56 [en] | trailing dash artifact | Ye ever become smaller, ye small people! Ye crumble away, ye comfortable ones! Ye will yet perish—
ch-p3-05-v64 [de] | trailing dash artifact | „Liebt immerhin euren Nächsten gleich euch,—aber seid mir erst solche, die sich selber lieben—
ch-p3-05-v64 [en] | trailing dash artifact | Love ever your neighbour as yourselves—but first be such as LOVE THEMSELVES—
ch-p3-05-v64 [es] | trailing dash artifact | «¡Amad siempre a vuestros prójimos igual que a vosotros, - pero sed primero de aquellos que a sí mismos se aman -
ch-p3-05-v65 [de] | trailing dash artifact | —mit der grossen Liebe lieben, mit der grossen Verachtung lieben!“ Also spricht Zarathustra, der Gottlose.—
ch-p3-05-v65 [en] | trailing dash artifact | —Such as love with great love, such as love with great contempt!” Thus speaketh Zarathustra the godless.—
ch-p3-05-v65 [fr] | trailing dash artifact | "Aimez toujours votre prochain comme vous-mêmes, mais soyez d'abord de ceux qui s'aiment eux-mêmes - qui s'aiment avec l
ch-p3-05-v70 [de] | trailing dash artifact | Oh gesegnete Stunde des Blitzes! Oh Geheimniss vor Mittag!—Laufende Feuer will ich einst noch aus ihnen machen und Verkü
ch-p3-05-v70 [en] | trailing dash artifact | O blessed hour of the lightning! O mystery before noontide!—Running fires will I one day make of them, and heralds with 
ch-p3-06-v14 [de] | trailing dash artifact | Sonderlich boshaft bin ich nämlich des Morgens: zur frühen Stunde, da der Eimer am Brunnen klirrt und die Rosse warm dur
ch-p3-06-v14 [en] | trailing dash artifact | For especially wicked am I in the morning: at the early hour when the pail rattleth at the well, and horses neigh warmly
ch-p3-06-v15 [de] | trailing dash artifact | Ungeduldig warte ich da, dass mir endlich der lichte Himmel aufgehe, der schneebärtige Winter-Himmel, der Greis und Weis
ch-p3-06-v15 [en] | trailing dash artifact | Impatiently do I then wait, that the clear sky may finally dawn for me, the snow-bearded winter-sky, the hoary one, the 
ch-p3-06-v19 [de] | trailing dash artifact | Ein gutes muthwilliges Ding ist auch das lange Schweigen und gleich dem Winter-Himmel blicken aus lichtem rundäugichten 
ch-p3-06-v19 [en] | trailing dash artifact | A good roguish thing is also the long silence, and to look, like the winter-sky, out of a clear, round-eyed countenance:
ch-p3-06-v26 [de] | trailing dash artifact | Sondern die Hellen, die Wackern, die Durchsichtigen—das sind mir die klügsten Schweiger: denen so tief ihr Grund ist, da
ch-p3-06-v26 [en] | trailing dash artifact | But the clear, the honest, the transparent—these are for me the wisest silent ones: in them, so PROFOUND is the depth th
ch-p3-06-v41 [de] | trailing dash artifact | Inzwischen laufe ich mit warmen Füssen kreuz und quer auf meinem Ölberge: im Sonnen-Winkel meines Ölberges singe und spo
ch-p3-06-v41 [en] | trailing dash artifact | Meanwhile do I run with warm feet hither and thither on mine olive-mount: in the sunny corner of mine olive-mount do I s
ch-p3-06-v41 [fr] | trailing dash artifact | Pendant ce temps, les pieds chauds, je cours çà et là, sur ma montagne des Oliviers; dans le coin ensoleillé de ma monta
ch-p3-06-v41 [es] | trailing dash artifact | Entretanto yo corro con pies calientes de un lado para otro en mi monte de los olivos: en el rincón soleado de mi monte 
ch-p3-07-v11 [de] | trailing dash artifact | Alle Lüste und Laster sind hier zu Hause; aber es giebt hier auch Tugendhafte, es giebt viel anstellige angestellte Tuge
ch-p3-07-v11 [en] | trailing dash artifact | All lusts and vices are here at home; but here there are also the virtuous; there is much appointable appointed virtue:—
ch-p3-07-v13 [es] | digit glued to letter (OCR) | También hay aquí mucha piedad, y mucho crédulo servilismo, y mucho adulador pasteleo ante el dios de los ejércitos31s.
ch-p3-07-v21 [de] | trailing dash artifact | Speie auf die Stadt der eingedrückten Seelen und schmalen Brüste, der spitzen Augen, der klebrigen Finger—
ch-p3-07-v21 [en] | trailing dash artifact | Spit on the city of compressed souls and slender breasts, of pointed eyes and sticky fingers—
ch-p3-07-v22 [de] | trailing dash artifact | —auf die Stadt der Aufdringlinge, der Unverschämten, der Schreib- und Schreihälse, der überheizten Ehrgeizigen:—
ch-p3-07-v22 [en] | trailing dash artifact | —On the city of the obtrusive, the brazen-faced, the pen-demagogues and tongue-demagogues, the overheated ambitious:—
ch-p3-07-v23 [de] | trailing dash artifact | —wo alles Anbrüchige, Anrüchige, Lüsterne, Düsterne, Übermürbe, Geschwürige, Verschwörerische zusammenschwärt:—
ch-p3-07-v23 [en] | trailing dash artifact | Where everything maimed, ill-famed, lustful, untrustful, over-mellow, sickly-yellow and seditious, festereth pernicious:
ch-p3-07-v23 [fr] | trailing dash artifact | Crache sur la ville des âmes déprimées et des poitrines étroites, des yeux envieux et des doigts gluants - sur la ville 
ch-p3-07-v23 [es] | trailing dash artifact | Escupe a la ciudad de las almas aplastadas y de los pechos estrechos, de los ojos afilados, de los dedos viscosos - - a 
ch-p3-07-v24 [de] | trailing dash artifact | —speie auf die grosse Stadt und kehre um!“—
ch-p3-07-v24 [en] | trailing dash artifact | —Spit on the great city and turn back!—
ch-p3-07-v25 [en] | trailing dash artifact | Here, however, did Zarathustra interrupt the foaming fool, and shut his mouth.—
ch-p3-07-v31 [de] | trailing dash artifact | Aus der Liebe allein soll mir mein Verachten und mein warnender Vogel auffliegen: aber nicht aus dem Sumpfe!—
ch-p3-07-v31 [en] | trailing dash artifact | Out of love alone shall my contempt and my warning bird take wing; but not out of the swamp!—
ch-p3-07-v31 [fr] | trailing dash artifact | C'est de l'amour seul que doit me venir le vol de mon mépris et de mon oiseau avertisseur: et non du marécage! -
ch-p3-07-v31 [es] | trailing dash artifact | Sólo del amor deben salir volando mi despreciar y mi pájaro amonestador: ¡pero no de la ciénaga! -
ch-p3-07-v33 [de] | trailing dash artifact | Was war es denn, was dich zuerst grunzen machte? Dass Niemand dir genug geschmeichelt hat:—darum setztest du dich hin zu
ch-p3-07-v33 [en] | trailing dash artifact | What was it that first made thee grunt? Because no one sufficiently FLATTERED thee:—therefore didst thou seat thyself be
ch-p3-07-v39 [de] | trailing dash artifact | Denn solche Feuersäulen müssen dem grossen Mittage vorangehn. Doch diess hat seine Zeit und sein eigenes Schicksal.—
ch-p3-07-v39 [en] | trailing dash artifact | For such pillars of fire must precede the great noontide. But this hath its time and its own fate.—
ch-p3-07-v39 [fr] | trailing dash artifact | Car il faut que de telles colonnes de feu précèdent le grand midi. Mais ceci a son temps et sa propre destinée.-
ch-p3-07-v40 [de] | trailing dash artifact | Diese Lehre aber gebe ich dir, du Narr, zum Abschiede: wo man nicht mehr lieben kann, da soll man—vorübergehn!—
ch-p3-07-v40 [en] | trailing dash artifact | This precept, however, give I unto thee, in parting, thou fool: Where one can no longer love, there should one—PASS BY!—
ch-p3-07-v40 [fr] | trailing dash artifact | Je te donne cependant cet enseignement en guise d'adieu, à toi fou: lorsqu'on ne peut plus aimer, il faut - passer! -
ch-p3-07-v40 [es] | trailing dash artifact | Esta enseñanza te doy a ti, necio, como despedida: donde no se puede continuar amando se debe - ¡pasar de largo! -
ch-p3-08-v08 [de] | trailing dash artifact | Der Rest: das sind immer die Allermeisten, der Alltag, der Überfluss, die Viel-zu-Vielen—diese alle sind feige!—
ch-p3-08-v08 [en] | trailing dash artifact | The rest: these are always the great majority, the common-place, the superfluous, the far too many—those all are cowardl
ch-p3-08-v08 [fr] | trailing dash artifact | Tout le reste: c'est toujours le plus grand nombre, ce sont les vulgaires et les superflus, ceux qui sont de trop. - Tou
ch-p3-08-v13 [de] | trailing dash artifact | Lass sie fahren und fallen, oh Zarathustra, und klage nicht! Lieber noch blase mit raschelnden Winden unter sie,—
ch-p3-08-v13 [en] | trailing dash artifact | Let them go and fall away, O Zarathustra, and do not lament! Better even to blow amongst them with rustling winds,—
ch-p3-08-v13 [fr] | trailing dash artifact | Laisse-les aller, laisse-les tomber, ô Zarathoustra, et ne te plains pas! Souffle plutôt parmi eux avec le bruissement d
ch-p3-08-v14 [de] | trailing dash artifact | —blase unter diese Blätter, oh Zarathustra: dass alles Welke schneller noch von dir davonlaufen!—
ch-p3-08-v14 [en] | trailing dash artifact | —Blow amongst those leaves, O Zarathustra, that everything WITHERED may run away from thee the faster!—
ch-p3-08-v14 [es] | trailing dash artifact | ¡Déjalas ir y caer, oh Zaratustra, y no te lamentes! Es preferible que soples entre ellas con vientos veloces, - - que s
ch-p3-08-v21 [de] | trailing dash artifact | Ich höre und rieche es: es kam ihre Stunde für Jagd und Umzug, nicht zwar für eine wilde Jagd, sondern für eine zahme la
ch-p3-08-v21 [en] | trailing dash artifact | I hear it and smell it: it hath come—their hour for hunt and procession, not indeed for a wild hunt, but for a tame, lam
ch-p3-08-v32 [de] | trailing dash artifact | „Für einen Vater sorgt er nicht genug um seine Kinder: Menschen-Väter thun diess besser!“—
ch-p3-08-v32 [en] | trailing dash artifact | “For a father he careth not sufficiently for his children: human fathers do this better!”—
ch-p3-08-v36 [de] | trailing dash artifact | „Ja! Ja! Der Glaube macht ihn selig, der Glaube an ihn. Das ist so die Art alter Leute! So geht's uns auch!“—
ch-p3-08-v36 [en] | trailing dash artifact | “Ay! Ay! Belief saveth him; belief in him. That is the way with old people! So it is with us also!”—
ch-p3-08-v36 [fr] | trailing dash artifact | "Oui, oui! La foi le sauve, la foi en lui-même. C'est l'habitude des vieilles gens! Nous sommes faits de même!" -
ch-p3-08-v43 [de] | trailing dash artifact | Das geschah, als das gottloseste Wort von einem Gotte selber ausgieng,—das Wort: „Es ist Ein Gott! Du sollst keinen ande
ch-p3-08-v43 [en] | trailing dash artifact | That took place when the unGodliest utterance came from a God himself—the utterance: “There is but one God! Thou shalt h
ch-p3-08-v44 [en] | trailing dash artifact | —An old grim-beard of a God, a jealous one, forgot himself in such wise:—
ch-p3-08-v46 [de] | trailing dash artifact | Wer Ohren hat, der höre.—
ch-p3-08-v46 [en] | trailing dash artifact | He that hath an ear let him hear.—
ch-p3-08-v46 [fr] | trailing dash artifact | Que celui qui a des oreilles pour entendre entende. -
ch-p3-08-v46 [es] | trailing dash artifact | El que tenga oídos, oiga. -
ch-p3-08-v47 [de] | trailing dash artifact | Also redete Zarathustra in der Stadt, die er liebte und welche zubenannt ist die bunte Kuh. Von hier nämlich hatte er nu
ch-p3-08-v47 [fr] | trailing dash artifact | Car de cet endroit il n'avait plus que deux jours de marche pour retourner à sa caverne, auprès de ses animaux; mais il 
ch-p3-08-v47 [es] | trailing dash artifact | Así dijo Zaratustra en la ciudad que él amaba y que se denomina «La Vaca Multicolor». Desde allí, en efecto, le faltaban
ch-p3-09-v02 [de] | trailing dash artifact | Nun drohe mir nur mit dem Finger, wie Mütter drohn, nein lächle mir zu, wie Mütter lächeln, nun sprich nur: „Und wer war
ch-p3-09-v02 [en] | trailing dash artifact | Now threaten me with the finger as mothers threaten; now smile upon me as mothers smile; now say just: “Who was it that 
ch-p3-09-v10 [de] | trailing dash artifact | Ein Anderes aber ist Verlassensein. Denn, weisst du noch, oh Zarathustra? Als damals dein Vogel über dir schrie, als du 
ch-p3-09-v10 [en] | trailing dash artifact | Another matter, however, is forsakenness. For, dost thou remember, O Zarathustra? When thy bird screamed overhead, when 
ch-p3-09-v10 [es] | trailing dash artifact | Pero otra cosa distinta es el estar abandonado. Pues ¿lo sabes aún, Zaratustra? Cuando en otro tiempo tu pájaro lanzó un
ch-p3-09-v14 [de] | trailing dash artifact | Und weisst du noch, oh Zarathustra? Als deine stillste Stunde kam und dich von dir selber forttrieb, als sie mit bösem F
ch-p3-09-v14 [en] | trailing dash artifact | And dost thou remember, O Zarathustra? When thy stillest hour came and drove thee forth from thyself, when with wicked w
ch-p3-09-v15 [de] | trailing dash artifact | —als sie dir all dein Warten und Schweigen leid machte und deinen demüthigen Muth entmuthigte: Das war Verlassenheit!“—
ch-p3-09-v15 [en] | trailing dash artifact | —When it disgusted thee with all thy waiting and silence, and discouraged thy humble courage: THAT was forsakenness!”—
ch-p3-09-v15 [fr] | trailing dash artifact | "Et te souviens-tu, ô Zarathoustra? Lorsque vint ton heure la plus silencieuse qui te chassa de toi-même, lorsqu'elle te
ch-p3-09-v43 [es] | trailing dash artifact | Cosquilleada por agudos vientos, como por vinos espumeantes, mi alma estornuda, estornuda y grita jubilosa: ¡He -
ch-p3-10-v03 [de] | trailing dash artifact | Messbar für Den, der Zeit hat, wägbar für einen guten Wäger, erfliegbar für starke Fittige, errathbar für göttliche Nüss
ch-p3-10-v03 [en] | trailing dash artifact | Measurable by him who hath time, weighable by a good weigher, attainable by strong pinions, divinable by divine nut-crac
ch-p3-10-v03 [fr] | trailing dash artifact | Mesurable pour celui qui a le temps, pesable pour un bon peseur, attingible pour les ailes vigoureuses, devinable pour d
ch-p3-10-v06 [de] | trailing dash artifact | Wie sicher schaute mein Traum auf diese endliche Welt, nicht neugierig, nicht altgierig, nicht fürchtend, nicht bittend:
ch-p3-10-v06 [en] | trailing dash artifact | How confidently did my dream contemplate this finite world, not new-fangledly, not old-fangledly, not timidly, not entre
ch-p3-10-v07 [de] | trailing dash artifact | —als ob ein voller Apfel sich meiner Hand böte, ein reifer Goldapfel, mit kühl-sanfter sammtener Haut:—so bot sich mir d
ch-p3-10-v07 [en] | trailing dash artifact | —As if a big round apple presented itself to my hand, a ripe golden apple, with a coolly-soft, velvety skin:—thus did th
ch-p3-10-v08 [de] | trailing dash artifact | —als ob ein Baum mir winke, ein breitästiger, starkwilliger, gekrümmt zur Lehne und noch zum Fussbrett für den Wegmüden:
ch-p3-10-v08 [en] | trailing dash artifact | —As if a tree nodded unto me, a broad-branched, strong-willed tree, curved as a recline and a foot-stool for weary trave
ch-p3-10-v09 [de] | trailing dash artifact | —als ob zierliche Hände mir einen Schrein entgegentrügen,—einen Schrein offen für das Entzücken schamhafter verehrender 
ch-p3-10-v09 [en] | trailing dash artifact | —As if delicate hands carried a casket towards me—a casket open for the delectation of modest adoring eyes: thus did the
ch-p3-10-v12 [de] | trailing dash artifact | Und dass ich's ihm gleich thue am Tage und sein Bestes ihm nach- und ablerne: will ich jetzt die drei bösesten Dinge auf
ch-p3-10-v12 [en] | trailing dash artifact | And that I may do the like by day, and imitate and copy its best, now will I put the three worst things on the scales, a
ch-p3-10-v12 [fr] | trailing dash artifact | Et, afin que je fasse comme lui, maintenant que c'est le jour, et pour que ce qu'il y a de meilleur me serve d'exemple: 
ch-p3-10-v15 [en] | trailing dash artifact | Well! Here is my promontory, and there is the sea—IT rolleth hither unto me, shaggily and fawningly, the old, faithful, 
ch-p3-10-v16 [de] | trailing dash artifact | Wohlauf! Hier will ich die Wage halten über gewälztem Meere: und auch einen Zeugen wähle ich, dass er zusehe,—dich, du E
ch-p3-10-v16 [en] | trailing dash artifact | Well! Here will I hold the scales over the weltering sea: and also a witness do I choose to look on—thee, the anchorite-
ch-p3-10-v16 [fr] | trailing dash artifact | Eh bien! C'est ici que je veux tenir la balance sur la mer houleuse, et je choisis aussi un témoin qui regarde, - c'est 
ch-p3-10-v17 [de] | trailing dash artifact | Auf welcher Brücke geht zum Dereinst das Jetzt? Nach welchem Zwange zwingt das Hohe sich zum Niederen? Und was heisst au
ch-p3-10-v17 [en] | trailing dash artifact | On what bridge goeth the now to the hereafter? By what constraint doth the high stoop to the low? And what enjoineth eve
ch-p3-10-v17 [es] | digit glued to letter (OCR) | ¡Adelante! Aquí quiero yo sostener la balanza sobre el arrollado mar: y también elijo un testigo para que mire, - ¡a ti,
ch-p3-10-v23 [de] | trailing dash artifact | Wollust: das grosse Gleichniss-Glück für höheres Glück und höchste Hoffnung. Vielem nämlich ist Ehe verheissen und mehr 
ch-p3-10-v23 [en] | trailing dash artifact | Voluptuousness: the great symbolic happiness of a higher happiness and highest hope. For to many is marriage promised, a
ch-p3-10-v25 [de] | trailing dash artifact | Wollust:—doch ich will Zäune um meine Gedanken haben und auch noch um meine Worte: dass mir nicht in meine Gärten die Sc
ch-p3-10-v25 [en] | trailing dash artifact | Voluptuousness:—but I will have hedges around my thoughts, and even around my words, lest swine and libertine should bre
ch-p3-10-v25 [fr] | trailing dash artifact | Volupté - cependant je veux mettre des clôtures autour de mes pensées et aussi autour de mes paroles: pour que les cocho
ch-p3-10-v33 [de] | trailing dash artifact | Dass die einsame Höhe sich nicht ewig vereinsame und selbst begnüge; dass der Berg zu Thale komme und die Winde der Höhe
ch-p3-10-v33 [en] | trailing dash artifact | That the lonesome height may not for ever remain lonesome and self-sufficing; that the mountains may come to the valleys
ch-p3-10-v35 [de] | trailing dash artifact | Und damals geschah es auch,—und wahrlich, es geschah zum ersten Male!—dass sein Wort die Selbstsucht selig pries, die he
ch-p3-10-v35 [en] | trailing dash artifact | And then it happened also,—and verily, it happened for the first time!—that his word blessed SELFISHNESS, the wholesome,
ch-p3-11-v01 [es] | digit glued to letter (OCR) | Mi boca - es del pueblo: yo hablo de un modo demasiado grosero y franco para los conejos de seda. Y aún más extraña les 
ch-p3-11-v08 [de] | trailing dash artifact | Andre Sänger giebt es freilich, denen macht das volle Haus erst ihre Kehle weide, ihre Hand gesprächig, ihr Auge ausdrüc
ch-p3-11-v08 [en] | trailing dash artifact | Other singers are there, to be sure, to whom only the full house maketh the voice soft, the hand eloquent, the eye expre
ch-p3-11-v08 [fr] | trailing dash artifact | Il y a bien aussi d'autres chanteurs qui n'ont le gosier souple, la main éloquente, l'oeil expressif et le coeur éveillé
ch-p3-11-v08 [es] | trailing dash artifact | Otros cantores hay, ciertamente, a los cuales sólo la casa llena vuélveles suave su garganta, elocuente su mano, expresi
ch-p3-11-v22 [en] | trailing dash artifact | And verily! Many a thing also that is OUR OWN is hard to bear! And many internal things in man are like the oyster—repul
ch-p3-11-v30 [de] | trailing dash artifact | Alles aber kauen und verdauen—das ist eine rechte Schweine-Art! Immer I-a sagen—das lernte allein der Esel, und wer sein
ch-p3-11-v30 [en] | trailing dash artifact | To chew and digest everything, however—that is the genuine swine-nature! Ever to say YE-A—that hath only the ass learnt,
ch-p3-11-v30 [fr] | trailing dash artifact | Mais tout mâcher et tout digérer - c'est faire comme les cochons! Dire toujours I-A, c'est ce qu'apprennent seuls l'âne 
ch-p3-11-v40 [de] | trailing dash artifact | Mit Strickleitern lernte ich manches Fenster erklettern, mit hurtigen Beinen klomm ich auf hohe Masten: auf hohen Masten
ch-p3-11-v40 [en] | trailing dash artifact | With rope-ladders learned I to reach many a window, with nimble legs did I climb high masts: to sit on high masts of per
ch-p3-11-v41 [de] | trailing dash artifact | —gleich kleinen Flammen flackern auf hohen Masten: ein kleines Licht zwar, aber doch ein grosser Trost für verschlagene 
ch-p3-11-v41 [fr] | trailing dash artifact | Avec des échelles de corde j'ai appris à escalader plus d'une fenêtre, avec des jambes agiles j'ai grimpé sur de hauts m
ch-p3-11-v42 [es] | raw < or > present | Con escalas de cuerda he aprendido yo a escalar más de una ventana, con ágiles piernas he trepado a elevados mástiles: e
ch-p3-12-v04 [de] | trailing dash artifact | Inzwischen rede ich als Einer, der Zeit hat, zu mir selber. Niemand erzählt mir Neues: so erzähle ich mir mich selber.—
ch-p3-12-v04 [fr] | trailing dash artifact | En attendant je parle comme quelqu'un qui a le temps, je me parle à moi-même. Personne ne me raconte de choses nouvelles
ch-p3-12-v04 [es] | trailing dash artifact | Esto es lo que ahora aguardo: antes tienen que llegarme, en efecto, los signos de que es mi hora, - a saber, el león rie
ch-p3-12-v07 [es] | soft-hyphen U+00AD present; trailing dash artifact | Esta somnolencia la sobresalté yo cuando enseñé: lo que es bueno y lo que es malvado, eso no lo sabe todavía nadie: ¡ex­
ch-p3-12-v15 [de] | trailing dash artifact | —hinaus in ferne Zukünfte, die kein Traum noch sah, in heissere Süden, als je sich Bildner träumten: dorthin, wo Götter 
ch-p3-12-v16 [de] | trailing dash artifact | —dass ich nämlich in Gleichnissen rede und gleich Dichtern hinke und stammle: und wahrlich, ich schäme mich, dass ich no
ch-p3-12-v16 [fr] | trailing dash artifact | Et souvent il m'a emporté bien loin, au delà des monts, vers les hauteurs, au milieu du rire: alors il m'arrivait de vol
ch-p3-12-v17 [de] | trailing dash artifact | Wo alles Werden mich Götter-Tanz und Götter-Muthwillen dünkte, und die Welt los- und ausgelassen und zu sich selber zurü
ch-p3-12-v17 [en] | trailing dash artifact | Where all becoming seemed to me dancing of Gods, and wantoning of Gods, and the world unloosed and unbridled and fleeing
ch-p3-12-v18 [de] | trailing dash artifact | —als ein ewiges Sich-fliehn und -Wiedersuchen vieler Götter, als das selige Sich-Widersprechen, Sich-Wieder-hören, Sich-
ch-p3-12-v18 [en] | trailing dash artifact | —As an eternal self-fleeing and re-seeking of one another of many Gods, as the blessed self-contradicting, recommuning, 
ch-p3-12-v19 [de] | trailing dash artifact | Wo alle Zeit mich ein seliger Hohn auf Augenblicke dünkte, wo die Nothwendigkeit die Freiheit selber war, die selig mit 
ch-p3-12-v19 [en] | trailing dash artifact | Where all time seemed to me a blessed mockery of moments, where necessity was freedom itself, which played happily with 
ch-p3-12-v20 [de] | trailing dash artifact | Wo ich auch meinen alten Teufel und Erzfeind wiederfand, den Geist der Schwere und Alles, was er schuf: Zwang, Satzung, 
ch-p3-12-v20 [en] | trailing dash artifact | Where I also found again mine old devil and arch-enemy, the spirit of gravity, and all that it created: constraint, law,
ch-p3-12-v20 [es] | trailing dash artifact | cojeo y balbuceo; ¡y en verdad, me avergüenzo de tener que ser todavía poeta! - Hacia allí donde todo devenir me pareció
ch-p3-12-v21 [de] | trailing dash artifact | Denn muss nicht dasein, über das getanzt, hinweggetanzt werde? Müssen nicht um der Leichten, Leichtesten willen—Maulwürf
ch-p3-12-v21 [en] | trailing dash artifact | For must there not be that which is danced OVER, danced beyond? Must there not, for the sake of the nimble, the nimblest
ch-p3-12-v26 [de] | trailing dash artifact | Ich lehrte sie all mein Dichten und Trachten: in Eins zu dichten und zusammen zu tragen, was Bruchstück ist am Menschen 
ch-p3-12-v26 [en] | trailing dash artifact | I taught them all MY poetisation and aspiration: to compose and collect into unity what is fragment in man, and riddle a
ch-p3-12-v29 [de] | trailing dash artifact | —Diess hiess ich ihnen Erlösung, Diess allein lehrte ich sie Erlösung heissen. -—
ch-p3-12-v29 [en] | trailing dash artifact | —This did I call redemption; this alone taught I them to call redemption.—
ch-p3-12-v29 [fr] | trailing dash artifact | - C'est ceci que j'ai appelé salut pour eux, c'est ceci seul que je leur ai enseigné à appeler salut. -
ch-p3-12-v32 [de] | trailing dash artifact | Der Sonne lernte ich Das ab, wenn sie hinabgeht, die Überreiche: Gold schüttet sie da in's Meer aus unerschöpflichem Rei
ch-p3-12-v32 [en] | trailing dash artifact | From the sun did I learn this, when it goeth down, the exuberant one: gold doth it then pour into the sea, out of inexha
ch-p3-12-v33 [de] | trailing dash artifact | —also, dass der ärmste Fischer noch mit goldenem Ruder rudert! Diess nämlich sah ich einst und wurde der Thränen nicht s
ch-p3-12-v33 [en] | trailing dash artifact | —So that the poorest fisherman roweth even with GOLDEN oars! For this did I once see, and did not tire of weeping in beh
ch-p3-12-v33 [fr] | trailing dash artifact | C'est du soleil que j'ai appris cela, quand il se couche, du soleil trop riche: il répand alors dans la mer l'or de sa r
ch-p3-12-v35 [de] | trailing dash artifact | Siehe, hier ist eine neue Tafel: aber wo sind meine Brüder, die sie mit mir zu Thale und in fleischerne Herzen tragen?—
ch-p3-12-v35 [en] | trailing dash artifact | Behold, here is a new table; but where are my brethren who will carry it with me to the valley and into hearts of flesh?
ch-p3-12-v35 [fr] | trailing dash artifact | Regardez, voici une nouvelle table: mais où sont mes frères qui la porteront avec moi dans la vallée et dans les coeurs 
ch-p3-12-v45 [de] | trailing dash artifact | Genuss und Unschuld nämlich sind die schamhaftesten Dinge: Beide wollen nicht gesucht sein. Man soll sie haben—, aber ma
ch-p3-12-v45 [en] | trailing dash artifact | For enjoyment and innocence are the most bashful things. Neither like to be sought for. One should HAVE them,—but one sh
ch-p3-12-v45 [fr] | trailing dash artifact | Car la jouissance et l'innocence sont les deux choses les plus pudiques: aucune des deux ne veut être cherchée. Il faut 
ch-p3-12-v46 [es] | trailing dash artifact | Goce e inocencia son, en efecto, las cosas más púdicas que existen: ninguna de las dos quiere ser buscada. Debemos tener
ch-p3-12-v50 [de] | trailing dash artifact | Aber so will es unsre Art; und ich liebe Die, welche sich nicht bewahren wollen. Die Untergehenden liebe ich mit meiner 
ch-p3-12-v50 [en] | trailing dash artifact | But so wisheth our type; and I love those who do not wish to preserve themselves, the down-going ones do I love with min
ch-p3-12-v50 [es] | trailing dash artifact | Pero así lo quiere nuestra especie; y yo amo a los que no quieren preservarse a sí mismos. A quienes se hunden en su oca
ch-p3-12-v59 [de] | trailing dash artifact | „Über dem Flusse ist Alles fest, alle die Werthe der Dinge, die Brücken, Begriffe, alles „Gut“ und „Böse“: das ist Alles
ch-p3-12-v59 [en] | trailing dash artifact | “OVER the stream all is stable, all the values of things, the bridges and bearings, all ‘good’ and ‘evil’: these are all
ch-p3-12-v74 [de] | trailing dash artifact | Diess ist mein Mitleid mit allem Vergangenen, dass ich sehe: es ist preisgegeben,—
ch-p3-12-v74 [en] | trailing dash artifact | It is my sympathy with all the past that I see it is abandoned,—
ch-p3-12-v79 [es] | raw < or > present | Por eso, oh hermanos míos, necesítase una nueva nobleza que sea el antagonista de toda plebe y de todo despotismo y escr
ch-p3-12-v81 [de] | trailing dash artifact | Oh meine Brüder, ich weihe und weise euch zu einem neuen Adel: ihr sollt mir Zeuger und Züchter werden und Säemänner der
ch-p3-12-v81 [en] | trailing dash artifact | O my brethren, I consecrate you and point you to a new nobility: ye shall become procreators and cultivators and sowers 
ch-p3-12-v86 [de] | trailing dash artifact | —Denn Stehen-können ist ein Verdienst bei Höflingen; und alle Höflinge glauben, zur Seligkeit nach dem Tode gehöre—Sitze
ch-p3-12-v86 [fr] | trailing dash artifact | Car savoir se tenir debout est un mérite chez les courtisans; et tous les courtisans croient que la permission d'être as
ch-p3-12-v87 [de] | trailing dash artifact | Nicht auch, dass ein Geist, den sie heilig nennen, eure Vorfahren in gelobte Länder führte, die ich nicht lobe: denn wo 
ch-p3-12-v87 [en] | trailing dash artifact | Nor even that a Spirit called Holy, led your forefathers into promised lands, which I do not praise: for where the worst
ch-p3-12-v88 [de] | trailing dash artifact | —und wahrlich, wohin dieser „heilige Geist“ auch seine Ritter führte, immer liefen bei solchen Zügen—Ziegen und Gänse un
ch-p3-12-v88 [en] | trailing dash artifact | —And verily, wherever this “Holy Spirit” led its knights, always in such campaigns did—goats and geese, and wryheads and
ch-p3-12-v88 [fr] | trailing dash artifact | Et, en vérité, quel que soit le pays où ce "Saint-Esprit" ait conduit ses chevaliers, le cortège de ses chevaliers était
ch-p3-12-v88 [es] | trailing dash artifact | - Pues poder estar de pie es un mérito entre los cortesanos: y todos los cortesanos creen que de la bienaventuranza desp
ch-p3-12-v92 [de] | trailing dash artifact | „Wozu leben? Alles ist eitel! Leben—das ist Stroh dreschen; Leben—das ist sich verbrennen und doch nicht warm werden.“—
ch-p3-12-v92 [en] | trailing dash artifact | “Why should one live? All is vain! To live—that is to thrash straw; to live—that is to burn oneself and yet not get warm
ch-p3-12-v92 [fr] | trailing dash artifact | "Pourquoi vivre? tout est vain! Vivre - c'est battre de la paille; vivre - c'est se brûler et ne pas arriver à se chauff
ch-p3-12-v93 [de] | trailing dash artifact | Solch alterthümliches Geschwätz gilt immer noch als „Weisheit“; dass es aber alt ist und dumpfig riecht, darum wird es b
ch-p3-12-v93 [en] | trailing dash artifact | Such ancient babbling still passeth for “wisdom”; because it is old, however, and smelleth mustily, THEREFORE is it the 
ch-p3-12-v93 [fr] | trailing dash artifact | Ces bavardages vieillis passent encore pour de la "sagesse"; ils sont vieux, ils sentent le renfermé, c'est pourquoi on 
ch-p3-12-v93 [es] | trailing dash artifact | «¿Para qué vivir? ¡Todo es vanidad! Vivir es trillar paja; vivir - es quemarse a sí mismo y, sin embargo, no calentarse.
ch-p3-12-v104 [de] | trailing dash artifact | An dem Besten ist noch Etwas zum Ekeln; und der Beste ist noch Etwas, das überwunden werden muss!—
ch-p3-12-v104 [en] | trailing dash artifact | In the best there is still something to loathe; and the best is still something that must be surpassed!—
ch-p3-12-v104 [fr] | trailing dash artifact | Les meilleurs ont quelque chose qui dégoûte; et le meilleur même est quelque chose qui doit être surmonté! -
ch-p3-12-v104 [es] | trailing dash artifact | Incluso en el mejor hay algo que produce náusea; ¡y el mejor es todavía algo que tiene que ser superado! -
ch-p3-12-v105 [de] | trailing dash artifact | Oh meine Brüder, es ist viel Weisheit darin, dass viel Koth in der Welt ist!—
ch-p3-12-v105 [en] | trailing dash artifact | O my brethren, there is much wisdom in the fact that much filth is in the world!—
ch-p3-12-v105 [fr] | trailing dash artifact | mes frères! il est sage qu'il y ait beaucoup de fange dans le monde! -
ch-p3-12-v105 [es] | trailing dash artifact | De tablas virjas y nuevas ¡Oh hermanos míos, hay mucha sabiduría e n el hecho de que exista mucha mierda en el mundo! -
ch-p3-12-v109 [de] | trailing dash artifact | „Und deine eigne Vernunft—die sollst du selber görgeln und würgen; denn es ist eine Vernunft von dieser Welt,—darob lern
ch-p3-12-v109 [en] | trailing dash artifact | “And thine own reason—this shalt thou thyself stifle and choke; for it is a reason of this world,—thereby wilt thou lear
ch-p3-12-v109 [fr] | trailing dash artifact | "Et ta propre raison tu devrais la ravaler et l'égorger; car cette raison est de ce monde; - ainsi tu apprendrais toi-mê
ch-p3-12-v110 [en] | trailing dash artifact | —Shatter, shatter, O my brethren, those old tables of the pious! Tatter the maxims of the world-maligners!—
ch-p3-12-v113 [de] | trailing dash artifact | Zerbrecht mir, oh meine Brüder, zerbrecht mir auch diese neue Tafel! Die Welt-Müden hängten sie hin und die Prediger des
ch-p3-12-v113 [en] | trailing dash artifact | Break up for me, O my brethren, break up also that NEW table! The weary-o’-the-world put it up, and the preachers of dea
ch-p3-12-v113 [fr] | trailing dash artifact | Brisez, ô mes frères, brisez même cette nouvelle table! Les gens fatigués du monde l'ont suspendue, les prêtres de la mo
ch-p3-12-v114 [de] | trailing dash artifact | Dass sie schlecht lernten und das Beste nicht, und Alles zu früh und Alles zu geschwind: dass sie schlecht assen, daher 
ch-p3-12-v114 [en] | trailing dash artifact | Because they learned badly and not the best, and everything too early and everything too fast; because they ATE badly: f
ch-p3-12-v133 [de] | trailing dash artifact | Aber es gehört mehr Muth dazu, ein Ende zu machen, als einen neuen Vers: das wissen alle Ärzte und Dichter.—
ch-p3-12-v133 [en] | trailing dash artifact | But more COURAGE is needed to make an end than to make a new verse: that do all physicians and poets know well.—
ch-p3-12-v133 [fr] | trailing dash artifact | Mais il faut plus de courage pour faire une fin, qu'un vers nouveau: c'est ce que savent tous les médecins et tous les p
ch-p3-12-v133 [es] | trailing dash artifact | Pero se necesita más valor para poner fin que para escribir un nuevo verso: esto lo saben todos los médicos y todos los 
ch-p3-12-v134 [de] | trailing dash artifact | Oh meine Brüder, es giebt Tafeln, welche die Ermüdung, und Tafeln, welche die Faulheit schuf, die faulige: ob sie schon 
ch-p3-12-v134 [en] | trailing dash artifact | O my brethren, there are tables which weariness framed, and tables which slothfulness framed, corrupt slothfulness: alth
ch-p3-12-v134 [fr] | trailing dash artifact | O mes frères, il y a des tables créées par la fatigue et des tables créées par la paresse, la paresse pourrie: quoiqu'el
ch-p3-12-v137 [de] | trailing dash artifact | Nun glüht die Sonne auf ihn, und die Hunde lecken nach seinem Schweisse: aber er liegt da in seinem Trotze und will lieb
ch-p3-12-v137 [en] | trailing dash artifact | Now gloweth the sun upon him, and the dogs lick at his sweat: but he lieth there in his obstinacy and preferreth to lang
ch-p3-12-v141 [de] | trailing dash artifact | Nur, meine Brüder, dass ihr die Hunde von ihm scheucht, die faulen Schleicher, und all das schwärmende Geschmeiss:—
ch-p3-12-v141 [en] | trailing dash artifact | Only, my brethren, see that ye scare the dogs away from him, the idle skulkers, and all the swarming vermin:—
ch-p3-12-v142 [de] | trailing dash artifact | —all das schwärmende Geschmeiss der „Gebildeten“ , das sich am Schweisse jedes Helden—gütlich thut!—
ch-p3-12-v142 [en] | trailing dash artifact | —All the swarming vermin of the “cultured,” that—feast on the sweat of every hero!—
ch-p3-12-v142 [fr] | trailing dash artifact | Mais chassez loin de lui, mes frères, les chiens, les paresseux sournois, et toute cette vermine grouillante: - toute la
ch-p3-12-v142 [es] | trailing dash artifact | Sólo, hermanos míos, ahuyentad de él a los perros, a los hipócritas perezosos y a todo el enjambre de sabandijas: - - a 
ch-p3-12-v143 [de] | trailing dash artifact | Ich schliesse Kreise um mich und heilige Grenzen; immer Wenigere steigen mit mir auf immer höhere Berge,—ich baue ein Ge
ch-p3-12-v143 [en] | trailing dash artifact | I form circles around me and holy boundaries; ever fewer ascend with me ever higher mountains: I build a mountain-range 
ch-p3-12-v143 [fr] | trailing dash artifact | Je trace des cercles autour de moi et de saintes frontières; il y en a toujours moins qui montent avec moi sur des monta
ch-p3-12-v149 [de] | trailing dash artifact | Die Seele nämlich, welche die längste Leiter hat und am tiefsten hinunter kann: wie sollten nicht an der die meisten Sch
ch-p3-12-v149 [en] | trailing dash artifact | For the soul which hath the longest ladder, and can go deepest down: how could there fail to be most parasites upon it?—
ch-p3-12-v150 [de] | trailing dash artifact | —die umfänglichste Seele, welche am weitesten in sich laufen und irren und schweifen kann; die nothwendigste, welche sic
ch-p3-12-v150 [en] | trailing dash artifact | —The most comprehensive soul, which can run and stray and rove furthest in itself; the most necessary soul, which out of
ch-p3-12-v151 [de] | trailing dash artifact | —die seiende Seele, welche in's Werden taucht; die habende, welche in's Wollen und Verlangen will:—
ch-p3-12-v151 [en] | trailing dash artifact | —The soul in Being, which plungeth into Becoming; the possessing soul, which SEEKETH to attain desire and longing:—
ch-p3-12-v152 [de] | trailing dash artifact | —die sich selber fliehende, die sich selber im weitesten Kreise einholt; die weiseste Seele, welcher die Narrheit am süs
ch-p3-12-v152 [en] | trailing dash artifact | —The soul fleeing from itself, which overtaketh itself in the widest circuit; the wisest soul, unto which folly speaketh
ch-p3-12-v158 [de] | trailing dash artifact | Und wen ihr nicht fliegen lehrt, den lehrt mir—schneller fallen!—
ch-p3-12-v158 [en] | trailing dash artifact | And him whom ye do not teach to fly, teach I pray you—TO FALL FASTER!—
ch-p3-12-v158 [fr] | trailing dash artifact | Et s'il y a quelqu'un à qui vous n'appreniez pas à voler, apprenez-lui du moins - à tomber plus vite! -
ch-p3-12-v158 [es] | trailing dash artifact | Ya quien no le enseñéis a volar, enseñadle - ¡a caer más deprisa! -
ch-p3-12-v162 [de] | trailing dash artifact | Dem würdigeren Feinde, oh meine Freunde, sollt ihr euch aufsparen: darum müsst ihr an Vielem vorübergehn,—
ch-p3-12-v162 [en] | trailing dash artifact | For the worthier foe, O my brethren, shall ye reserve yourselves: therefore must ye pass by many a one,—
ch-p3-12-v175 [es] | soft-hyphen U+00AD present; trailing dash artifact | Ya sólo los pájaros están por encima de él. Y cuando el hombre aprenda a volar, ¡ay!, ¡hasta qué altura volará su ra­ -
ch-p3-12-v185 [de] | trailing dash artifact | Wer über alte Ursprünge weise wurde, siehe, der wird zuletzt nach Quellen der Zukunft suchen und nach neuen Ursprüngen.—
ch-p3-12-v185 [en] | trailing dash artifact | He who hath grown wise concerning old origins, lo, he will at last seek after the fountains of the future and new origin
ch-p3-12-v185 [fr] | trailing dash artifact | Celui qui a acquis l'expérience des anciennes origines finira par chercher les sources de l'avenir et des origines nouve
ch-p3-12-v185 [es] | soft-hyphen U+00AD present | No sólo a propagaros al mismo nivel, sino a propagaros h a ­ cia arriba - ¡a eso, oh hermanos míos, ayúdeos el jardín de
ch-p3-12-v191 [de] | trailing dash artifact | Die Menschen-Gesellschaft: die ist ein Versuch, so lehre ich's,—ein langes Suchen: sie sucht aber den Befehlenden!—
ch-p3-12-v191 [en] | trailing dash artifact | Human society: it is an attempt—so I teach—a long seeking: it seeketh however the ruler!—
ch-p3-12-v193 [de] | trailing dash artifact | Oh meine Brüder! Bei Welchen liegt doch die grösste Gefahr aller Menschen-Zukunft? Ist es nicht bei den Guten und Gerech
ch-p3-12-v193 [en] | trailing dash artifact | O my brethren! With whom lieth the greatest danger to the whole human future? Is it not with the good and just?—
ch-p3-12-v194 [de] | trailing dash artifact | —als bei Denen, die sprechen und im Herzen fühlen: „wir wissen schon, was gut ist und gerecht, wir haben es auch; wehe D
ch-p3-12-v203 [de] | trailing dash artifact | Die Guten nämlich—die können nicht schaffen: die sind immer der Anfang vom Ende:-
ch-p3-12-v203 [en] | trailing dash artifact | For the good—they CANNOT create; they are always the beginning of the end:—
ch-p3-12-v205 [de] | trailing dash artifact | Die Guten—die waren immer der Anfang vom Ende.—
ch-p3-12-v205 [en] | trailing dash artifact | The good—they have always been the beginning of the end.—
ch-p3-12-v205 [fr] | trailing dash artifact | Les bons - furent toujours le commencement de la fin. -
ch-p3-12-v205 [es] | trailing dash artifact | Los buenos - han sido siempre el comienzo del final. -
ch-p3-12-v206 [de] | trailing dash artifact | Oh meine Brüder, verstandet ihr auch diess Wort? Und was ich einst sagte vom „letzten Menschen“ ?—
ch-p3-12-v206 [en] | trailing dash artifact | O my brethren, have ye also understood this word? And what I once said of the “last man”?—
ch-p3-12-v206 [fr] | trailing dash artifact | O mes frères, avez-vous aussi compris cette parole? et ce que j'ai dit un jour du "dernier homme"? -
ch-p3-12-v207 [es] | trailing dash artifact | ¡Romped, destrozadme a los buenos yjustos! Oh hermanos -
ch-p3-12-v216 [de] | trailing dash artifact | Was Vaterland! Dorthin will unser Steuer, wo unser Kinder-Land ist! Dorthinaus, stürmischer als das Meer, stürmt unsre g
ch-p3-12-v216 [en] | trailing dash artifact | What of fatherland! THITHER striveth our helm where our CHILDREN’S LAND is! Thitherwards, stormier than the sea, stormet
ch-p3-12-v216 [es] | trailing dash artifact | ¡Qué importa el país de los padres! ¡Nuestro timón quiere dirigirse hacia donde está el país de nuestros hijos! ¡Hacia a
ch-p3-12-v217 [de] | trailing dash artifact | „Warum so hart!—sprach zum Diamanten einst die Küchen-Kohle; sind wir denn nicht Nah-Verwandte?“—
ch-p3-12-v217 [en] | trailing dash artifact | “Why so hard!”—said to the diamond one day the charcoal; “are we then not near relatives?”—
ch-p3-12-v222 [de] | trailing dash artifact | Die Schaffenden nämlich sind hart. Und Seligkeit muss es euch dünken, eure Hand auf Jahrtausende zu drücken wie auf Wach
ch-p3-12-v222 [en] | trailing dash artifact | For the creators are hard. And blessedness must it seem to you to press your hand upon millenniums as upon wax,—
ch-p3-12-v224 [de] | trailing dash artifact | Diese neue Tafel, oh meine Brüder, stelle ich über euch: werdet hart!—
ch-p3-12-v224 [en] | trailing dash artifact | This new table, O my brethren, put I up over you: BECOME HARD!—
ch-p3-12-v228 [de] | trailing dash artifact | Ach, wessen Auge dunkelte nicht in dieser trunkenen Dämmerung! Ach, wessen Fuss taumelte nicht und verlernte im Siege—st
ch-p3-12-v228 [en] | trailing dash artifact | Ah, whose eye hath not bedimmed in this intoxicated twilight! Ah, whose foot hath not faltered and forgotten in victory—
ch-p3-12-v229 [de] | trailing dash artifact | —Dass ich einst bereit und reif sei im grossen Mittage: bereit und reif gleich glühendem Erze, blitzschwangrer Wolke und
ch-p3-12-v229 [en] | trailing dash artifact | —That I may one day be ready and ripe in the great noontide: ready and ripe like the glowing ore, the lightning-bearing 
ch-p3-12-v230 [de] | trailing dash artifact | —bereit zu mir selber und zu meinem verborgensten Willen: ein Bogen brünstig nach seinem Pfeile, ein Pfeil brünstig nach
ch-p3-12-v230 [en] | trailing dash artifact | —Ready for myself and for my most hidden Will: a bow eager for its arrow, an arrow eager for its star:—
ch-p3-12-v231 [de] | trailing dash artifact | —ein Stern bereit und reif in seinem Mittage, glühend, durchbohrt, selig vor vernichtenden Sonnen-Pfeilen:—
ch-p3-12-v231 [en] | trailing dash artifact | —A star, ready and ripe in its noontide, glowing, pierced, blessed, by annihilating sun-arrows:—
ch-p3-12-v233 [de] | trailing dash artifact | Oh Wille, Wende aller Noth, du meine Nothwendigkeit! Spare mich auf zu Einem grossen Siege!—
ch-p3-12-v233 [en] | trailing dash artifact | O Will, thou change of every need, MY needfulness! Spare me for one great victory!—
ch-p3-12-v233 [fr] | trailing dash artifact | O volonté! trêve de toute misère, toi ma nécessité! Réserve-moi pour une grande victoire! -
ch-p3-12-v233 [es] | trailing dash artifact | ¡Oh voluntad, viraje de toda necesidad, tú necesidad mía! ¡Resérvame para una gran victoria! - -
ch-p3-13-v01 [es] | digit glued to letter (OCR) | E conva1eciente Una mañana, no mucho tiempo después de su regreso a la caverna, Zaratustra saltó de su lecho como un loc
ch-p3-13-v22 [de] | trailing dash artifact | Wie lieblich ist alles Reden und alle Lüge der Töne! Mit Tönen tanzt unsre Liebe auf bunten Regenbögen.—
ch-p3-13-v22 [en] | trailing dash artifact | How lovely is all speech and all falsehoods of tones! With tones danceth our love on variegated rainbows.—
ch-p3-13-v22 [fr] | trailing dash artifact | Comme toute parole est douce, comme tous les mensonges des sons paraissent doux! Les sons font danser notre amour sur de
ch-p3-13-v26 [de] | trailing dash artifact | In jedem Nu beginnt das Sein; um jedes Hier rollt sich die Kugel Dort. Die Mitte ist überall. Krumm ist der Pfad der Ewi
ch-p3-13-v26 [en] | trailing dash artifact | Every moment beginneth existence, around every ‘Here’ rolleth the ball ‘There.’ The middle is everywhere. Crooked is the
ch-p3-13-v26 [fr] | trailing dash artifact | A chaque moment commence l'existence; autour de chaque ici se déploie la sphère là-bas. Le centre est partout. Le sentie
ch-p3-13-v27 [de] | trailing dash artifact | —Oh ihr Schalks-Narren und Drehorgeln! antwortete Zarathustra und lächelte wieder, wie gut wisst ihr, was sich in sieben
ch-p3-13-v27 [en] | trailing dash artifact | —O ye wags and barrel-organs! answered Zarathustra, and smiled once more, how well do ye know what had to be fulfilled i
ch-p3-13-v36 [de] | trailing dash artifact | Und ich selber—will ich damit des Menschen Ankläger sein? Ach, meine Thiere, Das allein lernte ich bisher, dass dem Mens
ch-p3-13-v36 [en] | trailing dash artifact | And I myself—do I thereby want to be man’s accuser? Ah, mine animals, this only have I learned hitherto, that for man hi
ch-p3-13-v37 [de] | trailing dash artifact | —dass alles Böseste seine beste Kraft ist und der härteste Stein dem höchsten Schaffenden; und dass der Mensch besser un
ch-p3-13-v37 [en] | trailing dash artifact | —That all that is baddest is the best POWER, and the hardest stone for the highest creator; and that man must become bet
ch-p3-13-v37 [fr] | trailing dash artifact | Et moi-même - est-ce que je veux être par là l'accusateur de l'homme? Hélas! mes animaux, le plus grand mal est nécessai
ch-p3-13-v39 [es] | trailing dash artifact | El gran hastío del hombre él era el que me estrangulaba y -
ch-p3-13-v45 [de] | trailing dash artifact | —„ach, der Mensch kehrt ewig wieder! Der kleine Mensch kehrt ewig wieder!“—
ch-p3-13-v45 [fr] | trailing dash artifact | - "Hélas! l'homme reviendra éternellement! L'homme petit reviendra éternellement!" -
ch-p3-13-v60 [de] | trailing dash artifact | Du lehrst, dass es ein grosses Jahr des Werdens giebt, ein Ungeheuer von grossem Jahre: das muss sich, einer Sanduhr gle
ch-p3-13-v60 [en] | trailing dash artifact | Thou teachest that there is a great year of Becoming, a prodigy of a great year; it must, like a sand-glass, ever turn u
ch-p3-13-v63 [de] | trailing dash artifact | Du würdest sprechen und ohne Zittern, vielmehr aufathmend vor Seligkeit: denn eine grosse Schwere und Schwüle wäre von d
ch-p3-13-v63 [en] | trailing dash artifact | Thou wouldst speak, and without trembling, buoyant rather with bliss, for a great weight and worry would be taken from t
ch-p3-13-v63 [fr] | trailing dash artifact | Tu parlerais sans trembler et tu pousserais plutôt un soupir d'allégresse: car un grand poids et une grande angoisse ser
ch-p3-13-v66 [es] | soft-hyphen U+00AD present; trailing dash artifact | Vendré otra vez, con este sol, con esta tierra, con este águila, con esta serpiente no a una vida nueva o a una vida me­
ch-p3-13-v67 [de] | trailing dash artifact | —ich komme ewig wieder zu diesem gleichen und selbigen Leben, im Grössten und auch im Kleinsten, dass ich wieder aller D
ch-p3-13-v67 [en] | trailing dash artifact | —I come again eternally to this identical and selfsame life, in its greatest and its smallest, to teach again the eterna
ch-p3-13-v70 [de] | trailing dash artifact | Die Stunde kam nun, dass der Untergehende sich selber segnet. Also endet Zarathustra's Untergang.““—
ch-p3-13-v70 [en] | trailing dash artifact | The hour hath now come for the down-goer to bless himself. Thus—ENDETH Zarathustra’s down-going.’”—
ch-p3-13-v70 [fr] | trailing dash artifact | L'heure est venue maintenant, l'heure où celui qui disparaît se bénit lui-même. Ainsi - finit le déclin de Zarathoustra.
ch-p3-14-v13 [de] | trailing dash artifact | Oh meine Seele, überreich und schwer stehst du nun da, ein Weinstock mit schwellenden Eutern und gedrängten braunen Gold
ch-p3-14-v13 [en] | trailing dash artifact | O my soul, exuberant and heavy dost thou now stand forth, a vine with swelling udders and full clusters of brown golden 
ch-p3-14-v16 [de] | trailing dash artifact | Oh meine Seele, ich gab dir Alles, und alle meine Hände sind an dich leer geworden:—und nun! Nun sagst du mir lächelnd u
ch-p3-14-v16 [en] | trailing dash artifact | O my soul, I have given thee everything, and all my hands have become empty by thee:—and now! Now sayest thou to me, smi
ch-p3-14-v17 [de] | trailing dash artifact | —hat der Geber nicht zu danken, dass der Nehmende nahm? Ist Schenken nicht eine Nothdurft? Ist Nehmen nicht—Erbarmen?“—
ch-p3-14-v17 [en] | trailing dash artifact | —Doth the giver not owe thanks because the receiver received? Is bestowing not a necessity? Is receiving not—pitying?”—
ch-p3-14-v17 [fr] | trailing dash artifact | O mon âme, je t'ai tout donné et toutes mes mains se sont dépouillées pour toi: - et maintenant! Maintenant tu me dis en
ch-p3-14-v22 [en] | trailing dash artifact | “Is not all weeping complaining? And all complaining, accusing?” Thus speakest thou to thyself; and therefore, O my soul
ch-p3-14-v25 [de] | trailing dash artifact | —singen, mit brausendem Gesange, bis alle Meere still werden, dass sie deiner Sehnsucht zuhorchen,—
ch-p3-14-v25 [en] | trailing dash artifact | —Thou wilt have to sing with passionate song, until all seas turn calm to hearken unto thy longing,—
ch-p3-14-v26 [de] | trailing dash artifact | —bis über stille sehnsüchtige Meere der Nachen schwebt, das güldene Wunder, um dessen Gold alle guten schlimmen wunderli
ch-p3-14-v26 [en] | trailing dash artifact | —Until over calm longing seas the bark glideth, the golden marvel, around the gold of which all good, bad, and marvellou
ch-p3-14-v27 [de] | trailing dash artifact | —auch vieles grosse und kleine Gethier und Alles, was leichte wunderliche Füsse hat, dass es auf veilchenblauen Pfaden l
ch-p3-14-v27 [en] | trailing dash artifact | —Also many large and small animals, and everything that hath light marvellous feet, so that it can run on violet-blue pa
ch-p3-14-v27 [fr] | trailing dash artifact | Mais si tu ne veux pas pleurer, pleurer jusqu'à l'épuisement ta mélancolie de pourpre, il faudra que tu chantes, ô mon â
ch-p3-14-v28 [de] | trailing dash artifact | —hin zu dem güldenen Wunder, dem freiwilligen Nachen und zu seinem Herrn: das aber ist der Winzer, der mit diamantenem W
ch-p3-14-v28 [en] | trailing dash artifact | —Towards the golden marvel, the spontaneous bark, and its master: he, however, is the vintager who waiteth with the diam
ch-p3-14-v28 [es] | trailing dash artifact | - cantar, con un canto rugiente, hasta que todos los mares se callen para escuchar tu anhelo, - - hasta que sobre silenc
ch-p3-14-v29 [de] | trailing dash artifact | —dein grosser Löser, oh meine Seele, der Namenlose—- dem zukünftige Gesänge erst Namen finden! Und wahrlich, schon dufte
ch-p3-14-v29 [en] | trailing dash artifact | —Thy great deliverer, O my soul, the nameless one—for whom future songs only will find names! And verily, already hath t
ch-p3-14-v30 [de] | trailing dash artifact | —schon glühst du und träumst, schon trinkst du durstig an allen tiefen klingenden Trost-Brunnen, schon ruht deine Schwer
ch-p3-14-v30 [en] | trailing dash artifact | —Already glowest thou and dreamest, already drinkest thou thirstily at all deep echoing wells of consolation, already re
ch-p3-14-v30 [es] | soft-hyphen U+00AD present; trailing dash artifact | Oh alma mía, ahora te he dado todo, e incluso lo último que tenía, y todas mis manos se han vaciado por ti: ¡el mandar­ 
ch-p3-14-v32 [de] | trailing dash artifact | Dass ich dich singen hiess, sprich nun, sprich: wer von uns hat jetzt—zu danken?—Besser aber noch: singe mir, singe, oh 
ch-p3-14-v32 [en] | trailing dash artifact | That I bade thee sing,—say now, say: WHICH of us now—oweth thanks?— Better still, however: sing unto me, sing, O my soul
ch-p3-14-v32 [fr] | trailing dash artifact | Que je t'aie dit de chanter, parle donc, parle: qui de nous deux maintenant doit dire - merci? - Mieux encore: chante po
ch-p3-14-v32 [es] | trailing dash artifact | El mandarte cantar, y ahora habla, di: ¿quién de nosotros tiene ahora - que dar las gracias? - O mejor: ¡canta para mí, 
ch-p3-15-v04 [de] | trailing dash artifact | Zwei Mal nur regtest du deine Klapper mit kleinen Händen—da schaukelte schon mein Fuss vor Tanz-Wuth.—
ch-p3-15-v04 [en] | trailing dash artifact | Twice only movedst thou thy rattle with thy little hands—then did my feet swing with dance-fury.—
ch-p3-15-v04 [fr] | trailing dash artifact | Tu jetais un regard vers mon pied fou de danse, un regard berceur, fondant, riant et interrogateur: deux fois seulement,
ch-p3-15-v22 [de] | trailing dash artifact | Du bist so arg müde? Ich trage dich hin, lass nur die Arme sinken! Und hast du Durst,—ich hätte wohl Etwas, aber dein Mu
ch-p3-15-v22 [en] | trailing dash artifact | Thou art so very weary? I carry thee thither; let just thine arm sink! And art thou thirsty—I should have something; but
ch-p3-15-v25 [de] | trailing dash artifact | Nach dem Takt meiner Peitsche sollst du mir tanzen und schrein! Ich vergass doch die Peitsche nicht?—Nein!“—
ch-p3-15-v25 [en] | trailing dash artifact | To the rhythm of my whip shalt thou dance and cry! I forget not my whip?—Not I!”—
ch-p3-15-v25 [fr] | trailing dash artifact | Tu dois danser et crier au rythme de mon fouet! Je n'ai pourtant pas oublié le fouet? - Non!" -
ch-p3-15-v31 [de] | trailing dash artifact | Wenn dir deine Weisheit einmal davonliefe, ach! da liefe dir schnell auch meine Liebe noch davon.“—
ch-p3-15-v31 [en] | trailing dash artifact | If thy Wisdom should one day run away from thee, ah! then would also my love run away from thee quickly.”—
ch-p3-15-v31 [fr] | trailing dash artifact | Si ta sagesse se sauvait une fois de toi, hélas! vite mon amour, lui aussi, se sauverait de toi." -
ch-p3-15-v31 [es] | trailing dash artifact | Si alguna vez se apartase de ti tu sabiduría, ¡ay!, entonces se apartaría de ti rápidamente también mi amor.» -
ch-p3-15-v34 [de] | trailing dash artifact | Es giebt eine alte schwere schwere Brumm-Glocke: die brummt Nachts bis zu deiner Höhle hinauf:—
ch-p3-15-v34 [en] | trailing dash artifact | There is an old heavy, heavy, booming-clock: it boometh by night up to thy cave:—
ch-p3-15-v35 [de] | trailing dash artifact | —hörst du diese Glocke Mitternachts die Stunde schlagen, so denkst du zwischen Eins und Zwölf daran—
ch-p3-15-v35 [en] | trailing dash artifact | —When thou hearest this clock strike the hours at midnight, then thinkest thou between one and twelve thereon—
ch-p3-15-v36 [de] | trailing dash artifact | —du denkst daran, oh Zarathustra, ich weiss es, dass du mich bald verlassen willst!“—
ch-p3-15-v36 [en] | trailing dash artifact | —Thou thinkest thereon, O Zarathustra, I know it—of soon leaving me!”—
ch-p3-15-v36 [fr] | trailing dash artifact | Il y a un vieux bourdon, lourd, très lourd: il sonne la nuit là-haut, jusque dans ta caverne: - quand tu entends cette c
ch-p3-15-v38 [de] | trailing dash artifact | Du weisst Das, oh Zarathustra? Das weiss Niemand.—
ch-p3-15-v38 [es] | trailing dash artifact | «¿Tú sabes eso, oh Zaratustra? Eso no lo sabe nadie.» - -
ch-p3-15-v39 [de] | trailing dash artifact | Und wir sahen uns an und blickten auf die grüne Wiese, über welche eben der kühle Abend lief, und weinten mit einander.—
ch-p3-15-v39 [en] | trailing dash artifact | And we gazed at each other, and looked at the green meadow o’er which the cool evening was just passing, and we wept tog
ch-p3-15-v39 [fr] | trailing dash artifact | Et nous nous sommes regardés, nous avons jeté nos regards sur la vertre prairie, où passait la fraîcheur du soir, et nou
ch-p3-15-v39 [es] | trailing dash artifact | Ynos miramos uno a otro y contemplamos el verde prado, sobre el cual empezaba a correr el fresco atardecer, y lloramos j
ch-p3-15-v46 [en] | trailing dash artifact | “I slept my sleep—
ch-p3-15-v48 [en] | trailing dash artifact | “From deepest dream I’ve woke and plead:—
ch-p3-15-v48 [es] | trailing dash artifact | De un profundo soñar me he despertado: -
ch-p3-15-v54 [en] | trailing dash artifact | “Deep is its woe—
ch-p3-15-v60 [en] | trailing dash artifact | “But joys all want eternity—
ch-p3-16-v02 [de] | trailing dash artifact | Wenn ich ein Wahrsager bin und voll jenes wahrsagerischen Geistes, der auf hohem Joche zwischen zwei Meeren wandelt,—
ch-p3-16-v02 [en] | trailing dash artifact | If I be a diviner and full of the divining spirit which wandereth on high mountain-ridges, ‘twixt two seas,—
ch-p3-16-v02 [es] | raw < or > present | los siete senos (O : la canción «Si y Amém>)4 33
ch-p3-16-v03 [de] | trailing dash artifact | zwischen Vergangenem und Zukünftigem als schwere Wolke wandelt,—schwülen Niederungen feind und Allem, was müde ist und n
ch-p3-16-v04 [de] | trailing dash artifact | zum Blitze bereit im dunklen Busen und zum erlösenden Lichtstrahle, schwanger von Blitzen, die Ja! sagen, Ja! lachen, zu
ch-p3-16-v04 [en] | trailing dash artifact | Ready for lightning in its dark bosom, and for the redeeming flash of light, charged with lightnings which say Yea! whic
ch-p3-16-v05 [de] | trailing dash artifact | —selig aber ist der also Schwangere! Und wahrlich, lange muss als schweres Wetter am Berge hängen, wer einst das Licht d
ch-p3-16-v05 [en] | trailing dash artifact | —Blessed, however, is he who is thus charged! And verily, long must he hang like a heavy tempest on the mountain, who sh
ch-p3-16-v05 [fr] | trailing dash artifact | Et, en vérité, il faut qu'il soit longtemps suspendu au sommet, comme un lourd orage, celui qui doit un jour allumer la 
ch-p3-16-v11 [de] | trailing dash artifact | Wenn ich je frohlockend sass, wo alte Götter begraben liegen, weltsegnend, weltliebend neben den Denkmalen alter Welt-Ve
ch-p3-16-v11 [en] | trailing dash artifact | If ever I have sat rejoicing where old Gods lie buried, world-blessing, world-loving, beside the monuments of old world-
ch-p3-16-v12 [de] | trailing dash artifact | —denn selbst Kirchen und Gottes-Gräber liebe ich, wenn der Himmel erst reinen Auges durch ihre zerbrochenen Decken blick
ch-p3-16-v12 [en] | trailing dash artifact | —For even churches and Gods’-graves do I love, if only heaven looketh through their ruined roofs with pure eyes; gladly 
ch-p3-16-v12 [fr] | trailing dash artifact | Si je me suis jamais assis plein d'allégresse, à l'endroit où sont enterrés des dieux anciens, bénissant et aimant le mo
ch-p3-16-v18 [de] | trailing dash artifact | Wenn ich je am Göttertisch der Erde mit Göttern Würfel spielte, dass die Erde bebte und brach und Feuerflüsse heraufschn
ch-p3-16-v18 [en] | trailing dash artifact | If ever I have played dice with the Gods at the divine table of the earth, so that the earth quaked and ruptured, and sn
ch-p3-16-v18 [es] | trailing dash artifact | Si alguna vez jugué a los dados con los dioses sobre la divina mesa de la tierra, de tal manera que la tierra tembló y s
ch-p3-16-v19 [de] | trailing dash artifact | —denn ein Göttertisch ist die Erde, und zitternd von schöpferischen neuen Worten und Götter-Würfen:—
ch-p3-16-v19 [fr] | trailing dash artifact | Si jamais j'ai joué aux dés avec des dieux, à la table divine de la terre, en sorte que la terre tremblait et se brisait
ch-p3-16-v25 [de] | trailing dash artifact | Wenn ich selber ein Korn bin von jenem erlösenden Salze, welches macht, dass alle Dinge im Mischkruge gut sich mischen:—
ch-p3-16-v25 [en] | trailing dash artifact | If I myself am a grain of the saving salt which maketh everything in the confection-bowl mix well:—
ch-p3-16-v26 [de] | trailing dash artifact | —denn es giebt ein Salz, das Gutes mit Bösem bindet; und auch das Böseste ist zum Würzen würdig und zum letzten Überschä
ch-p3-16-v26 [en] | trailing dash artifact | —For there is a salt which uniteth good with evil; and even the evilest is worthy, as spicing and as final over-foaming:
ch-p3-16-v26 [fr] | trailing dash artifact | Si je suis moi-même un grain de ce sable rédempteur, qui fait que toutes choses se mêlent bien dans la cruche des mixtur
ch-p3-16-v32 [de] | trailing dash artifact | Wenn je mein Frohlocken rief: „die Küste schwand,—nun fiel mir die letzte Kette ab—
ch-p3-16-v32 [en] | trailing dash artifact | If ever my rejoicing hath called out: “The shore hath vanished,—now hath fallen from me the last chain—
ch-p3-16-v33 [de] | trailing dash artifact | —das Grenzenlose braust um mich, weit hinaus glänzt mir Raum und Zeit, wohlan! wohlauf! altes Herz!“—
ch-p3-16-v33 [en] | trailing dash artifact | The boundless roareth around me, far away sparkle for me space and time,—well! cheer up! old heart!”—
ch-p3-16-v33 [fr] | trailing dash artifact | Si jamais mon allégresse s'écria: "Les côtes ont disparu - maintenant ma dernière chaîne est tombée - l'immensité sans b
ch-p3-16-v39 [de] | trailing dash artifact | —im Lachen nämlich ist alles Böse bei einander, aber heilig- und losgesprochen durch seine eigne Seligkeit:—
ch-p3-16-v39 [en] | trailing dash artifact | —For in laughter is all evil present, but it is sanctified and absolved by its own bliss:—
ch-p3-16-v40 [de] | trailing dash artifact | Und wenn Das mein A und O ist, dass alles Schwere leicht, aller Leib Tänzer, aller Geist Vogel werde: und wahrlich, Das 
ch-p3-16-v40 [en] | trailing dash artifact | And if it be my Alpha and Omega that everything heavy shall become light, every body a dancer, and every spirit a bird: 
ch-p3-16-v40 [fr] | trailing dash artifact | Et ceci est mon alpha et mon oméga, que tout ce qui est lourd devienne léger, que tout corps devienne danseur, tout espr
ch-p3-16-v45 [de] | trailing dash artifact | Wenn ich spielend in tiefen Licht-Fernen schwamm, und meiner Freiheit Vogel-Weisheit kam:—
ch-p3-16-v45 [en] | trailing dash artifact | If I have swum playfully in profound luminous distances, and if my freedom’s avian wisdom hath come to me:—
ch-p3-16-v47 [de] | trailing dash artifact | —sind alle Worte nicht für die Schweren gemacht? Lügen dem Leichten nicht alle Worte! Singe! sprich nicht mehr!“—
ch-p3-16-v47 [en] | trailing dash artifact | —Are not all words made for the heavy? Do not all words lie to the light ones? Sing! speak no more!”—
ch-p3-16-v47 [fr] | trailing dash artifact | Si j'ai nagé en me jouant dans de profonds lointains de lumière, si la sagesse d'oiseau de ma liberté est venue: - car a
ch-p4-01-v02 [de] | trailing dash artifact | „Oh Zarathustra, sagten sie, schaust du wohl aus nach deinem Glücke?“—„Was liegt am Glücke! antwortete er, ich trachte l
ch-p4-01-v02 [en] | trailing dash artifact | “O Zarathustra,” said they, “gazest thou out perhaps for thy happiness?”—“Of what account is my happiness!” answered he,
ch-p4-01-v02 [fr] | trailing dash artifact | "O Zarathoustra, dirent-ils, cherches-tu des yeux ton bonheur? - Qu'importe le bonheur, répondit-il, il y a longtemps qu
ch-p4-01-v03 [de] | trailing dash artifact | Da giengen die Thiere wieder nachdenklich um ihn herum und stellten sich dann abermals vor ihn hin. „Oh Zarathustra, sag
ch-p4-01-v03 [en] | trailing dash artifact | Then went his animals again thoughtfully around him, and placed themselves once more in front of him. “O Zarathustra,” s
ch-p4-01-v03 [fr] | trailing dash artifact | Alors ses animaux pensifs tournèrent derechef autour de lui, et de nouveau ils se placèrent devant lui. "O Zarathoustra,
ch-p4-01-v12 [en] | trailing dash artifact | —My happiness itself do I throw out into all places far and wide ‘twixt orient, noontide, and occident, to see if many h
ch-p4-01-v19 [de] | trailing dash artifact | Fieng wohl je ein Mensch auf hohen Bergen Fische? Und wenn es auch eine Thorheit ist, was ich hier oben will und treibe:
ch-p4-01-v19 [en] | trailing dash artifact | Did ever any one catch fish upon high mountains? And though it be a folly what I here seek and do, it is better so than 
ch-p4-01-v23 [de] | trailing dash artifact | Wer muss einst kommen und darf nicht vorübergehn? Unser grosser Hazar, das ist unser grosses fernes Menschen-Reich, das 
ch-p4-01-v23 [en] | trailing dash artifact | What must one day come and may not pass by? Our great Hazar, that is to say, our great, remote human-kingdom, the Zarath
ch-p4-01-v24 [fr] | trailing dash artifact | Qui devra venir un jour et n'aura pas le droit de passer? Notre grand hasard, c'est-à-dire notre grand et lointain Règne
ch-p4-02-v01 [es] | trailing dash artifact | Adía siguiente estaba sentado Zaratustra de nuevo en su piedra delante de la caverna mientras los animales andaban fuera
ch-p4-02-v05 [de] | trailing dash artifact | —„Mitleiden! antwortete der Wahrsager aus einem überströmenden Herzen und hob beide Hände empor—oh Zarathustra, ich komm
ch-p4-02-v05 [en] | trailing dash artifact | —“PITY!” answered the soothsayer from an overflowing heart, and raised both his hands aloft—“O Zarathustra, I have come 
ch-p4-02-v05 [fr] | trailing dash artifact | "Pitié!" répondit le devin d'un coeur débordant et en levant les deux mains: - "O Zarathoustra, je viens pour te faire c
ch-p4-02-v06 [de] | trailing dash artifact | Und kaum waren diese Worte gesprochen, da erscholl der Schrei abermals, und länger und ängstlicher als vorher, auch scho
ch-p4-02-v06 [en] | trailing dash artifact | And hardly had those words been uttered when there sounded the cry once more, and longer and more alarming than before—a
ch-p4-02-v06 [fr] | trailing dash artifact | A peine ces paroles avaient-elles été prononcées que le cri retentit de nouveau, plus long et plus anxieux qu'auparavant
ch-p4-02-v15 [de] | trailing dash artifact | Aber Alles ist gleich, es lohnt sich Nichts, es hilft kein Suchen, es giebt auch keine glückseligen Inseln mehr!“—
ch-p4-02-v15 [en] | trailing dash artifact | But all is alike, nothing is worth while, no seeking is of service, there are no longer any Happy Isles!”—
ch-p4-02-v15 [fr] | trailing dash artifact | Mais tout est égal, rien ne vaut la peine, en vain sont toutes les recherches, il n'y a plus d'Iles Bienheureuses!" -
ch-p4-02-v15 [es] | trailing dash artifact | ¡Pero todo es idéntico, nada merece la pena, de nada sirve buscar, ya no hay tampoco islas afortunadas!» - -
ch-p4-02-v20 [de] | trailing dash artifact | Er ist in meinem Bereiche: darin soll er mir nicht zu Schaden kommen! Und wahrlich, es giebt viele böse Thiere bei mir.“
ch-p4-02-v20 [en] | trailing dash artifact | He is in MY domain: therein shall he receive no scath! And verily, there are many evil beasts about me.”—
ch-p4-02-v20 [fr] | trailing dash artifact | Ils est dans mon domaine: je ne veux pas qu'il lui arrive malheur ici! Et, en vérité, il y a chez moi beaucoup de bêtes 
ch-p4-03-v14 [de] | trailing dash artifact | —pfui, unter dem Gesindel die Ersten zu bedeuten! Ach, Ekel! Ekel! Ekel! Was liegt noch an uns Königen!“—
ch-p4-03-v14 [en] | trailing dash artifact | —Fie, to stand for the first men among the rabble! Ah, loathing! Loathing! Loathing! What doth it now matter about us ki
ch-p4-03-v14 [fr] | trailing dash artifact | C'est de la populace que nous nous sommes détournés, de tous ces braillards et de toutes ces mouches écrivassières, pour
ch-p4-03-v18 [es] | soft-hyphen U+00AD present | Yo soy Zaratustra, que en otro tiempo dijo: "¡Qué impor­ ,, tan ya los reyes! Perdonadme que me haya alegrado cuando ,, 
ch-p4-03-v21 [de] | trailing dash artifact | Mit dem Schwerte dieses Wortes zerhaust du unsres Herzens dickste Finsterniss. Du entdecktest unsre Noth, denn siehe! Wi
ch-p4-03-v21 [en] | trailing dash artifact | With the sword of thine utterance severest thou the thickest darkness of our hearts. Thou hast discovered our distress; 
ch-p4-03-v24 [de] | trailing dash artifact | Und wenn sie gar die letzten sind und mehr Vieh als Mensch: da steigt und steigt der Pöbel im Preise, und endlich sprich
ch-p4-03-v24 [en] | trailing dash artifact | And when they are even the last men, and more beast than man, then riseth and riseth the populace in honour, and at last
ch-p4-03-v24 [fr] | trailing dash artifact | Et quand ils sont les derniers même, et plutôt des animaux que des hommes: alors la populace monte et monte en valeur, e
ch-p4-03-v25 [de] | trailing dash artifact | Was hörte ich eben? antwortete Zarathustra; welche Weisheit bei Königen! Ich bin entzückt, und, wahrlich, schon gelüstet
ch-p4-03-v25 [en] | trailing dash artifact | What have I just heard? answered Zarathustra. What wisdom in kings! I am enchanted, and verily, I have already prompting
ch-p4-03-v28 [es] | soft-hyphen U+00AD present | «¡Ay, las cosas marchan mal! ¡Ruina! ¡Ruina! ¡Nunca cayó tan bajo el mundo! Roma bajó a ser puta y burdel, El César de R
ch-p4-03-v36 [de] | trailing dash artifact | Wie sie seufzten, unsre Väter, wenn sie an der Wand blitzblanke ausgedorrte Schwerter sahen! Denen gleich dürsteten sie 
ch-p4-03-v36 [en] | trailing dash artifact | How they sighed, our fathers, when they saw on the wall brightly furbished, dried-up swords! Like those they thirsted fo
ch-p4-03-v36 [fr] | trailing dash artifact | Comme ils soupiraient, nos pères, lorsqu'ils voyaient au mur des glaives polis et inutiles! Semblables à ces glaives ils
ch-p4-04-v13 [de] | trailing dash artifact | Es gieng dir schlimm, du Unseliger, in diesem Leben: erst biss dich das Thier, und dann—trat dich der Mensch!“—
ch-p4-04-v13 [en] | trailing dash artifact | It hath gone badly with thee, thou unfortunate one, in this life: first a beast bit thee, and then—a man trod upon thee!
ch-p4-04-v16 [de] | trailing dash artifact | Oh Glück! Oh Wunder! Gelobt sei dieser Tag, der mich in diesen Sumpf lockte! Gelobt sei der beste lebendigste Schröpfkop
ch-p4-04-v16 [en] | trailing dash artifact | O happiness! O miracle! Praised be this day which enticed me into the swamp! Praised be the best, the livest cupping-gla
ch-p4-05-v03 [de] | trailing dash artifact | Triff tiefer, Triff Ein Mal noch! Zerstich, zerbrich diess Herz! Was soll diess Martern Mit zähnestumpfen Pfeilen? Was b
ch-p4-05-v03 [en] | trailing dash artifact | Smite deeper! Smite yet once more! Pierce through and rend my heart! What mean’th this torture With dull, indented arrow
ch-p4-05-v03 [fr] | trailing dash artifact | Frappe plus fort! Frappe encore une fois! Transperce, brise ce coeur! Pourquoi me tourmenter de flèches épointées? Que r
ch-p4-05-v03 [es] | trailing dash artifact | ¡Hiere más hondo, Hiere otra vez! ¡ Taladra, rompe este corazón! ¿Por qué esta tortura Con flechas embotadas? ¿Por qué v
ch-p4-05-v05 [de] | trailing dash artifact | Umsonst! Stich weiter, Grausamster Stachel! Nein, Kein Hund—dein Wild nur bin ich, Grausamster Jäger! Dein stolzester Ge
ch-p4-05-v07 [es] | trailing dash artifact | ¡En vano! ¡Sigue pinchando, Cruelísimo aguijón! No, No un perro - tu caza soy tan sólo, ¡Cruelísimo cazador! Tu más orgu
ch-p4-05-v08 [en] | trailing dash artifact | Ha! Ha! And torturest me, fool that thou art, Dead-torturest quite my pride? Give LOVE to me—who warm’th me still? Who l
ch-p4-05-v08 [fr] | trailing dash artifact | Ah! Ah! Et tu me martyrises, fou que tu es, tu tortures ma fierté? Donne-moi de l'amour. Qui me chauffe encore? qui m'ai
ch-p4-05-v10 [es] | trailing dash artifact | ¿Cómo? ¿Dinero de rescate? ¿Cuánto dinero de rescate quieres? Pide mucho - ¡te lo aconseja mi segundo orgullo! ¡Ay, ay! 
ch-p4-05-v19 [de] | trailing dash artifact | „Den Büsser des Geistes, sagte der alte Mann, den—spielte ich: du selber erfandest einst diess Wort—
ch-p4-05-v19 [en] | trailing dash artifact | “THE PENITENT IN SPIRIT,” said the old man, “it was him—I represented; thou thyself once devisedst this expression—
ch-p4-05-v21 [de] | trailing dash artifact | Und gesteh es nur ein: es währte lange, oh Zarathustra, bis du hinter meine Kunst und Lüge kamst! Du glaubtest an meine 
ch-p4-05-v21 [en] | trailing dash artifact | And just acknowledge it: it was long, O Zarathustra, before thou discoveredst my trick and lie! Thou BELIEVEDST in my di
ch-p4-05-v28 [de] | trailing dash artifact | Du erntetest den Ekel ein, als deine Eine Wahrheit. Kein Wort ist mehr an dir ächt, aber dein Mund: nämlich der Ekel, de
ch-p4-05-v28 [en] | trailing dash artifact | Thou hast reaped disgust as thy one truth. No word in thee is any longer genuine, but thy mouth is so: that is to say, t
ch-p4-05-v28 [fr] | trailing dash artifact | Tu as moissonné le dégoût comme ta seule vérité. Aucune parole n'est plus vraie chez toi, mais ta bouche est encore vrai
ch-p4-05-v32 [de] | trailing dash artifact | Oh Zarathustra, Alles ist Lüge an mir; aber dass ich zerbreche—diess mein Zerbrechen ist ächt!“—
ch-p4-05-v32 [en] | trailing dash artifact | O Zarathustra, everything is a lie in me; but that I collapse—this my collapsing is GENUINE!”—
ch-p4-05-v32 [fr] | trailing dash artifact | O Zarathoustra, chez moi tout est mensonge; mais que je me brise - cela est vrai chez moi!" -
ch-p4-05-v36 [de] | trailing dash artifact | Aber sprich, was suchst du hier in meinen Wäldern und Felsen? Und wenn du mir dich in den Weg legtest, welche Probe woll
ch-p4-05-v36 [en] | trailing dash artifact | But tell me, what seekest thou here in MY forests and rocks? And if thou hast put thyself in MY way, what proof of me wo
ch-p4-05-v37 [de] | trailing dash artifact | —wess versuchtest du mich?“—
ch-p4-05-v48 [de] | trailing dash artifact | Du suchst nach grossen Menschen, du wunderlicher Narr? Wer lehrte's dich? Ist heute dazu die Zeit? Oh du schlimmer Suche
ch-p4-05-v48 [en] | trailing dash artifact | Thou seekest for great men, thou strange fool? Who TAUGHT that to thee? Is to-day the time for it? Oh, thou bad seeker, 
ch-p4-05-v48 [fr] | trailing dash artifact | Tu cherches les grands hommes, singulier fou! Qui donc t'a enseigné à les chercher? Est-ce aujourd'hui le temps opportun
ch-p4-05-v48 [es] | trailing dash artifact | ¿Tú buscas grandes hombres, tú extraño necio? ¿Quién te ha enseñado eso? ¿Es hoy tiempo de eso? Oh tú, perverso buscador
ch-p4-06-v02 [de] | trailing dash artifact | Wie! Kaum bin ich jenem Zauberer entronnen: muss mir da wieder ein anderer Schwarzkünstler über den Weg laufen,—
ch-p4-06-v02 [en] | trailing dash artifact | What! Hardly have I escaped from that magician, and must another necromancer again run across my path,—
ch-p4-06-v04 [de] | trailing dash artifact | Aber der Teufel ist nie am Platze, wo er am Platze wäre: immer kommt er zu spät, dieser vermaledeite Zwerg und Klumpfuss
ch-p4-06-v04 [en] | trailing dash artifact | But the devil is never at the place which would be his right place: he always cometh too late, that cursed dwarf and clu
ch-p4-06-v04 [fr] | trailing dash artifact | Mais le diable n'est jamais là quand on aurait besoin de lui: toujours il arrive trop tard, ce maudit nain, ce maudit pi
ch-p4-06-v18 [de] | trailing dash artifact | Ich bin's, der gottlose Zarathustra, der da spricht: wer ist gottloser als ich, dass ich mich seiner Unterweisung freue?
ch-p4-06-v18 [en] | trailing dash artifact | It is I, the ungodly Zarathustra, who saith: ‘Who is ungodlier than I, that I may enjoy his teaching?’”—
ch-p4-06-v21 [de] | trailing dash artifact | —siehe, ich selber bin wohl von uns Beiden jetzt der Gottlosere? Aber wer könnte daran sich freuen!“—
ch-p4-06-v21 [en] | trailing dash artifact | —Lo, I myself am surely the most godless of us at present? But who could rejoice at that!”—
ch-p4-06-v23 [de] | trailing dash artifact | —dass er es sah, wie der Mensch am Kreuze hieng, und es nicht ertrug, dass die Liebe zum Menschen seine Hölle und zuletz
ch-p4-06-v23 [en] | trailing dash artifact | —That he saw how MAN hung on the cross, and could not endure it;—that his love to man became his hell, and at last his d
ch-p4-06-v23 [fr] | trailing dash artifact | - la pitié de voir l'homme suspendu à la croix, sans pouvoir supporter que l'amour pour les hommes devînt son enfer et e
ch-p4-06-v33 [de] | trailing dash artifact | Da sass er, welk, in seinem Ofenwinkel, härmte sich ob seiner schwachen Beine, weltmüde, willensmüde, und erstickte eine
ch-p4-06-v33 [en] | trailing dash artifact | There did he sit shrivelled in his chimney-corner, fretting on account of his weak legs, world-weary, will-weary, and on
ch-p4-06-v33 [fr] | trailing dash artifact | Le visage ridé, il était assis au coin du feu, se faisant des soucis à cause de la faiblesse de ses jambes, fatigué du m
ch-p4-06-v40 [es] | soft-hyphen U+00AD present | También en la piedad existe un buen gusto: éste acabó por decir "¡Fuera tal Dios! ¡Mejor ningún Dios, mejor construirse 
ch-p4-06-v45 [de] | trailing dash artifact | Lass mich deinen Gast sein, oh Zarathustra, für eine einzige Nacht! Nirgends auf Erden wird es mir jetzt wohler als bei 
ch-p4-06-v45 [en] | trailing dash artifact | Let me be thy guest, O Zarathustra, for a single night! Nowhere on earth shall I now feel better than with thee!”—
ch-p4-06-v45 [fr] | trailing dash artifact | Laisse-moi être ton hôte, ô Zarathoustra, pour une seule nuit! Nulle par sur la terre je ne me sentirai mieux qu'auprès 
ch-p4-06-v50 [de] | trailing dash artifact | Dieser alte Gott nämlich lebt nicht mehr: der ist gründlich todt.“—
ch-p4-06-v50 [en] | trailing dash artifact | For that old God liveth no more: he is indeed dead.”—
ch-p4-06-v50 [es] | trailing dash artifact | Pues ese viejo Dios no vive ya: está muerto de verdad.» -
ch-p4-07-v02 [de] | trailing dash artifact | An deren Worten will ich lange nun kauen gleich als an guten Körnern; klein soll mein Zahn sie mahlen und malmen, bis si
ch-p4-07-v02 [en] | trailing dash artifact | At their words will I now chew a long while as at good corn; small shall my teeth grind and crush them, until they flow 
ch-p4-07-v02 [fr] | trailing dash artifact | Je vais à présent remâcher longtemps leurs paroles, comme si elles étaient de bons grains; ma dent les broiera, les moud
ch-p4-07-v11 [de] | trailing dash artifact | Also sprach Zarathustra und wollte davon; aber der Unaussprechliche fasste nach einem Zipfel seines Gewandes und begann 
ch-p4-07-v11 [en] | trailing dash artifact | Thus spake Zarathustra and was about to go; but the nondescript grasped at a corner of his garment and began anew to gur
ch-p4-07-v16 [de] | trailing dash artifact | War nicht aller Erfolg bisher bei den Gut-Verfolgten? Und wer gut verfolgt, lernt leicht folgen:—ist er doch einmal—hint
ch-p4-07-v16 [en] | trailing dash artifact | Hath not all success hitherto been with the well-persecuted ones? And he who persecuteth well learneth readily to be OBS
ch-p4-07-v16 [es] | soft-hyphen U+00AD present | ¿No estuvo hasta ahora siempre el éxito de parte de los bien perseguidos? Y quien persigue bien, aprende con facilidad a
ch-p4-07-v22 [de] | trailing dash artifact | Jedweder Andere hätte mir sein Almosen zugeworfen, sein Mitleiden, mit Blick und Rede. Aber dazu—bin ich nicht Bettler g
ch-p4-07-v32 [es] | soft-hyphen U+00AD present | ¿Se ha dado nunca una respuesta más cortés a un presuntuoso? - Pero tú, oh Zaratustra, lo dejaste de lado al pasar y di­
ch-p4-07-v36 [de] | trailing dash artifact | Du selber aber—warne dich selber auch vor deinem Mitleiden! Denn Viele sind zu dir unterwegs, viele Leidende, Zweifelnde
ch-p4-07-v36 [en] | trailing dash artifact | Thou thyself, however,—warn thyself also against THY pity! For many are on their way to thee, many suffering, doubting, 
ch-p4-07-v36 [fr] | trailing dash artifact | Mais toi-même - garde-toi de ta -propre- pitié! Car il y en a beaucoup qui sont en route vers toi, beaucoup de ceux qui 
ch-p4-07-v46 [de] | trailing dash artifact | Und rede zuerst und -nächst mit meinen Thieren! Das stolzeste Thier und das klügste Thier—die möchten uns Beiden wohl di
ch-p4-07-v46 [en] | trailing dash artifact | And talk first and foremost to mine animals! The proudest animal and the wisest animal—they might well be the right coun
ch-p4-07-v46 [fr] | trailing dash artifact | Commence tout d'abord par t'entretenir avec mes animaux! L'animal le plus fier et l'animal le plus rusé - qu'ils soient 
ch-p4-07-v46 [es] | trailing dash artifact | ¡Y ante todo y sobre todo, habla con mis animales! El animal más orgulloso y el animal más inteligente - ¡ellos son sin 
ch-p4-07-v52 [de] | trailing dash artifact | Ich liebe die grossen Verachtenden. Der Mensch aber ist Etwas, das überwunden werden muss.“—
ch-p4-07-v52 [en] | trailing dash artifact | I love the great despisers. Man is something that hath to be surpassed.”—
ch-p4-07-v52 [fr] | trailing dash artifact | J'aime les hommes du grand mépris. L'homme cependant est quelque chose qui doit-être surmonté." -
ch-p4-07-v52 [es] | trailing dash artifact | Yo amo a los grandes despreciadores. Pero el hombre es algo que tiene que ser superado.» - -
ch-p4-08-v10 [de] | trailing dash artifact | —seine grosse Trübsal: die aber heisst heute Ekel. Wer hat heute von Ekel nicht Herz, Mund und Augen voll? Auch du! Auch
ch-p4-08-v10 [en] | trailing dash artifact | —His great affliction: that, however, is at present called DISGUST. Who hath not at present his heart, his mouth and his
ch-p4-08-v10 [fr] | trailing dash artifact | Et, en vérité, quand bien même l'homme gagnerait le monde entier, s'il n'apprenait pas cette seule chose, je veux dire d
ch-p4-08-v14 [de] | trailing dash artifact | „Sprich nicht von mir, du Wunderlicher! Lieblicher! sagte Zarathustra und wehrte seiner Zärtlichkeit, sprich mir erst vo
ch-p4-08-v14 [en] | trailing dash artifact | “Speak not of me, thou strange one; thou amiable one!” said Zarathustra, and restrained his affection, “speak to me firs
ch-p4-08-v26 [de] | trailing dash artifact | —vor diesem vergüldeten verfälschten Pöbel, dessen Väter Langfinger oder Aasvögel oder Lumpensammler waren, mit Weibern 
ch-p4-08-v26 [en] | trailing dash artifact | —At this gilded, falsified populace, whose fathers were pickpockets, or carrion-crows, or rag-pickers, with wives compli
ch-p4-08-v26 [fr] | trailing dash artifact | "Pourquoi me tentes-tu? Répondit celui-ci. Tu le sais encore mieux que moi. Qu'est-ce donc qui m'a poussé vers les plus 
ch-p4-08-v36 [de] | trailing dash artifact | Siehe, dorthin führt der Weg zu meiner Höhle: sei diese Nacht ihr Gast. Und rede mit meinen Thieren vom Glück der Thiere
ch-p4-08-v36 [en] | trailing dash artifact | Behold, thither leadeth the way to my cave: be to-night its guest. And talk to mine animals of the happiness of animals,
ch-p4-08-v38 [de] | trailing dash artifact | Jetzt aber nimm flugs Abschied von deinen Kühen, du Wunderlicher! Lieblicher! ob es dir schon schwer werden mag. Denn es
ch-p4-08-v38 [en] | trailing dash artifact | Now, however, take leave at once of thy kine, thou strange one! thou amiable one! though it be hard for thee. For they a
ch-p4-08-v38 [fr] | trailing dash artifact | Mais maintenant prends bien vite congé de tes vaches, homme singulier et charmant! quoi qu'il puisse t'en coûter. Car ce
ch-p4-09-v03 [de] | trailing dash artifact | Mein Schatten ruft mich? Was liegt an meinem Schatten! Mag er mir nachlaufen! ich—laufe ihm davon.“—
ch-p4-09-v28 [es] | soft-hyphen U+00AD present; trailing dash artifact | "¿Dónde está mi hogar?" Por él pregunto y busco y he bus­ -
ch-p4-09-v36 [de] | trailing dash artifact | Ich will allein laufen, dass es wieder hell um mich werde. Dazu muss ich noch lange lustig auf den Beinen sein. Des Aben
ch-p4-09-v36 [en] | trailing dash artifact | I will run alone, so that it may again become bright around me. Therefore must I still be a long time merrily upon my le
ch-p4-09-v36 [fr] | trailing dash artifact | Je veux courir seul, pour qu'il fasse de nouveau clair autour de moi. C'est pourquoi il me faut encore gaiement jouer de
ch-p4-09-v36 [es] | trailing dash artifact | Quiero correr solo, para que de nuevo vuelva a haber claridad a mi alrededor. Para ello tengo que estar todavía mucho ti
ch-p4-10-v06 [de] | trailing dash artifact | Er überredet mich, ich weiss nicht wie?, er betupft mich innewendig mit schmeichelnder Hand, er zwingt mich. Ja, er zwin
ch-p4-10-v06 [en] | trailing dash artifact | It persuadeth me, I know not how, it toucheth me inwardly with a caressing hand, it constraineth me. Yea, it constrainet
ch-p4-10-v14 [de] | trailing dash artifact | Singe nicht, du Gras-Geflügel, oh meine Seele! Flüstere nicht einmal! Sieh doch —still! der alte Mittag schläft, er bewe
ch-p4-10-v14 [en] | trailing dash artifact | Do not sing, thou prairie-bird, my soul! Do not even whisper! Lo—hush! The old noontide sleepeth, it moveth its mouth: d
ch-p4-10-v15 [de] | trailing dash artifact | —einen alten braunen Tropfen goldenen Glücks, goldenen Weins? Es huscht über ihn hin, sein Glück lacht. So—lacht ein Got
ch-p4-10-v15 [en] | trailing dash artifact | —An old brown drop of golden happiness, golden wine? Something whisketh over it, its happiness laugheth. Thus—laugheth a
ch-p4-10-v15 [fr] | trailing dash artifact | Ne chante pas, oiseau des prairies, ô mon âme! Ne murmure même pas! Regarde donc - silence! Le vieux midi dort, il remue
ch-p4-10-v21 [de] | trailing dash artifact | Still—- (und hier dehnte sich Zarathustra und fühlte, dass er schlafe.)—
ch-p4-10-v22 [de] | trailing dash artifact | Auf! sprach er zu sich selber, du Schläfer! Du Mittagsschläfer! Wohlan, wohlauf, ihr alten Beine! Zeit ist's und Überzei
ch-p4-10-v22 [en] | trailing dash artifact | “Up!” said he to himself, “thou sleeper! Thou noontide sleeper! Well then, up, ye old legs! It is time and more than tim
ch-p4-10-v22 [fr] | trailing dash artifact | "Lève-toi, se dit-il à lui-même, dormeur! Paresseux! Allons, ouf, vieilles jambes! Il est temps, il est grand temps! Il 
ch-p4-10-v24 [de] | trailing dash artifact | (Aber da schlief er schon von Neuem ein, und seine Seele sprach gegen ihn und wehrte sich und legte sich wieder hin)—„La
ch-p4-10-v24 [en] | trailing dash artifact | (But then did he fall asleep anew, and his soul spake against him and defended itself, and lay down again)—“Leave me alo
ch-p4-10-v24 [fr] | trailing dash artifact | (Mais déjà il s'endormait de nouveau, et son âme lui résistait et se défendait et se recouchait tout de son long) - "Lai
ch-p4-10-v28 [de] | trailing dash artifact | Wann trinkst du diesen Tropfen Thau's, der auf alle Erden-Dinge niederfiel,—wann trinkst du diese wunderliche Seele—
ch-p4-10-v28 [en] | trailing dash artifact | When wilt thou drink this drop of dew that fell down upon all earthly things,—when wilt thou drink this strange soul—
ch-p4-11-v08 [de] | trailing dash artifact | Vergebt mir doch, ihr Verzweifelnden, dass ich vor euch mit solch kleinen Worten rede, unwürdig, wahrlich!, solcher Gäst
ch-p4-11-v08 [en] | trailing dash artifact | Forgive me, however, ye despairing ones, for speaking such trivial words before you, unworthy, verily, of such guests! B
ch-p4-11-v20 [de] | trailing dash artifact | Der Pinie vergleiche ich, wer gleich dir, oh Zarathustra, aufwächst: lang, schweigend, hart, allein, besten biegsamsten 
ch-p4-11-v20 [en] | trailing dash artifact | To the pine do I compare him, O Zarathustra, which groweth up like thee—tall, silent, hardy, solitary, of the best, supp
ch-p4-11-v30 [de] | trailing dash artifact | Und dass wir Verzweifelnde jetzt in deine Höhle kamen und schon nicht mehr verzweifeln: ein Wahr- und Vorzeichen ist es 
ch-p4-11-v30 [en] | trailing dash artifact | And that we despairing ones have now come into thy cave, and already no longer despair:—it is but a prognostic and a pre
ch-p4-11-v31 [es] | trailing dash artifact | Yel hecho de que nosotros, hombres desesperados, hayamos venido ahora a tu caverna y ya no desesperemos: una premonición
ch-p4-11-v47 [de] | trailing dash artifact | Nicht auf euch warte ich hier in diesen Bergen, nicht mit euch darf ich zum letzten Male niedersteigen. Als Vorzeichen k
ch-p4-11-v47 [en] | trailing dash artifact | Not for you do I wait here in these mountains; not with you may I descend for the last time. Ye have come unto me only a
ch-p4-12-v16 [de] | trailing dash artifact | Ich bin ein Gesetz nur für die Meinen, ich bin kein Gesetz für Alle. Wer aber zu mir gehört, der muss von starken Knoche
ch-p4-12-v16 [en] | trailing dash artifact | I am a law only for mine own; I am not a law for all. He, however, who belongeth unto me must be strong of bone and ligh
ch-p4-12-v18 [de] | trailing dash artifact | Das Beste gehört den Meinen und mir; und giebt man's uns nicht, so nehmen wir's:—die beste Nahrung, den reinsten Himmel,
ch-p4-12-v18 [en] | trailing dash artifact | The best belongeth unto mine and me; and if it be not given us, then do we take it:—the best food, the purest sky, the s
ch-p4-12-v18 [fr] | trailing dash artifact | Ce qu'il y a de meilleur appartient aux miens et à moi, et si on ne nous le donne pas, nous nous en emparons: - la meill
ch-p4-13-v12 [de] | trailing dash artifact | Der Übermensch liegt mir am Herzen, der ist mein Erstes und Einziges,—und nicht der Mensch: nicht der Nächste, nicht der
ch-p4-13-v12 [en] | trailing dash artifact | The Superman, I have at heart; THAT is the first and only thing to me—and NOT man: not the neighbour, not the poorest, n
ch-p4-13-v12 [fr] | trailing dash artifact | Le Surhumain me tient au coeur, c'est lui qui est pour moi la chose unique, - et non point l'homme: non pas le prochain,
ch-p4-13-v24 [de] | trailing dash artifact | Wer den Abgrund sieht, aber mit Adlers-Augen, wer mit Adlers-Krallen den Abgrund fasst: Der hat Muth.—
ch-p4-13-v24 [en] | trailing dash artifact | He who seeth the abyss, but with eagle’s eyes,—he who with eagle’s talons GRASPETH the abyss: he hath courage.—
ch-p4-13-v24 [fr] | trailing dash artifact | Celui qui voit l'abîme, mais avec des yeux d'aigle, - celui qui saisit l'abîme avec des serres d'aigle: celui-là a du co
ch-p4-13-v24 [es] | trailing dash artifact | El que ve el abismo, pero con ojos de águila, el que aferra el abismo con garras de águila: ése tiene valor. - -
ch-p4-13-v27 [de] | trailing dash artifact | Das mochte gut sein für jenen Prediger der kleinen Leute, dass er litt und trug an des Menschen Sünde. Ich aber erfreue 
ch-p4-13-v27 [en] | trailing dash artifact | It may have been well for the preacher of the petty people to suffer and be burdened by men’s sin. I, however, rejoice i
ch-p4-13-v27 [fr] | trailing dash artifact | Cela pouvait être bon pour ce prédicateur des petites gens de souffrir et de porter les péchés des hommes. Mais moi, je 
ch-p4-13-v31 [de] | trailing dash artifact | Nein! Nein! Drei Mal Nein! Immer Mehr, immer Bessere eurer Art sollen zu Grunde gehn,—denn ihr sollt es immer schlimmer 
ch-p4-13-v31 [en] | trailing dash artifact | Nay! Nay! Three times Nay! Always more, always better ones of your type shall succumb,—for ye shall always have it worse
ch-p4-13-v34 [de] | trailing dash artifact | Ihr leidet mir noch nicht genug! Denn ihr leidet an euch, ihr littet noch nicht am Menschen. Ihr würdet lügen, wenn ihr'
ch-p4-13-v34 [en] | trailing dash artifact | Ye do not yet suffer enough for me! For ye suffer from yourselves, ye have not yet suffered FROM MAN. Ye would lie if ye
ch-p4-13-v35 [de] | trailing dash artifact | Es ist mir nicht genug, dass der Blitz nicht mehr schadet. Nicht ableiten will ich ihn: er soll lernen für mich—arbeiten
ch-p4-13-v35 [en] | trailing dash artifact | It is not enough for me that the lightning no longer doeth harm. I do not wish to conduct it away: it shall learn—to wor
ch-p4-13-v35 [fr] | trailing dash artifact | Pour moi vous ne souffrez pas encore assez! Car c'est de vous que vous souffrez, vous n'avez pas encore souffert de l'ho
ch-p4-13-v35 [es] | trailing dash artifact | ¡Para mí no sufrís aún bastante! Pues sufrís por vosotros, no habéis sufrido aún por el hombre. ¡Mentiríais si dijeseis 
ch-p4-13-v36 [de] | trailing dash artifact | Meine Weisheit sammlet sich lange schon gleich einer Wolke, sie wird stiller und dunkler. So thut jede Weisheit, welche 
ch-p4-13-v36 [en] | trailing dash artifact | My wisdom hath accumulated long like a cloud, it becometh stiller and darker. So doeth all wisdom which shall one day be
ch-p4-13-v36 [fr] | trailing dash artifact | Il ne me suffit pas que la foudre ne nuise plus. Je ne veux point la faire dévier, je veux qu'elle apprenne à travailler
ch-p4-13-v39 [de] | trailing dash artifact | Sonderlich, wenn sie grosse Dinge wollen! Denn sie wecken Misstrauen gegen grosse Dinge, diese feinen Falschmünzer und S
ch-p4-13-v39 [en] | trailing dash artifact | Especially when they will great things! For they awaken distrust in great things, these subtle false-coiners and stage-p
ch-p4-13-v95 [de] | trailing dash artifact | Zarathustra der Tänzer, Zarathustra der Leichte, der mit den Flügeln winkt, ein Flugbereiter, allen Vögeln zuwinkend, be
ch-p4-13-v95 [en] | trailing dash artifact | Zarathustra the dancer, Zarathustra the light one, who beckoneth with his pinions, one ready for flight, beckoning unto 
ch-p4-13-v99 [de] | trailing dash artifact | Besser aber noch närrisch sein vor Glücke als närrisch vor Unglücke, besser plump tanzen als lahm gehn. So lernt mir doc
ch-p4-13-v99 [en] | trailing dash artifact | Better, however, to be foolish with happiness than foolish with misfortune, better to dance awkwardly than walk lamely. 
ch-p4-13-v103 [de] | trailing dash artifact | Der den Eseln Flügel giebt, der Löwinnen melkt, gelobt sei dieser gute unbändige Geist, der allem Heute und allem Pöbel 
ch-p4-13-v103 [en] | trailing dash artifact | That which giveth wings to asses, that which milketh the lionesses:— praised be that good, unruly spirit, which cometh l
ch-p4-14-v08 [de] | trailing dash artifact | Euch Allen, welche Ehren ihr euch mit Worten geben mögt, ob ihr euch „die freien Geister“ nennt oder „die Wahrhaftigen“ 
ch-p4-14-v08 [en] | trailing dash artifact | Unto all of you, whatever honours ye like to assume in your names, whether ye call yourselves ‘the free spirits’ or ‘the
ch-p4-14-v11 [de] | trailing dash artifact | —gleich einem neuen wunderlichen Mummenschanze, in dem sich mein böser Geist, der schwermüthige Teufel, gefällt:—ich lie
ch-p4-14-v11 [en] | trailing dash artifact | —Like a new strange mummery in which mine evil spirit, the melancholy devil, delighteth:—I love Zarathustra, so doth it 
ch-p4-14-v11 [fr] | trailing dash artifact | Je vous connais, ô hommes supérieurs, je le connais, - je le connais aussi, ce lutin que j'aime malgré moi, ce Zarathous
ch-p4-14-v12 [de] | trailing dash artifact | Aber schon fällt der mich an und zwingt mich, dieser Geist der Schwermuth, dieser Abend-Dämmerungs-Teufel: und, wahrlich
ch-p4-14-v12 [en] | trailing dash artifact | But already doth IT attack me and constrain me, this spirit of melancholy, this evening-twilight devil: and verily, ye h
ch-p4-14-v17 [fr] | trailing dash artifact | "Le prétendant de la vérité? toi? - ainsi se moquaient-ils - Non! Poète seulement! Une bête rusée, sauvage, rampante, qu
ch-p4-14-v18 [en] | trailing dash artifact | HE—of truth the wooer? Not still, stiff, smooth and cold, Become an image, A godlike statue, Set up in front of temples,
ch-p4-14-v18 [es] | trailing dash artifact | No silencioso, rígido, liso, frío, Convertido en imagen, En columna de Dios, No colocado delante de templos, Como guardi
ch-p4-14-v20 [es] | trailing dash artifact | Así, De águila, de pantera Son los anhelos del poeta, Son tus anhelos bajo miles de máscaras, ¡Tú necio! ¡Tú poeta! Tú q
ch-p4-14-v21 [de] | trailing dash artifact | Der du den Menschen schautest So Gott als Schaf—: Den Gott zerreissen im Menschen Wie das Schaf im Menschen, Und zerreis
ch-p4-14-v21 [en] | trailing dash artifact | Even thus, Eaglelike, pantherlike, Are the poet’s desires, Are THINE OWN desires ‘neath a thousand guises, Thou fool! Th
ch-p4-14-v21 [fr] | trailing dash artifact | Toi qui vis l'homme, tel Dieu, comme un agneau -: Déchirer Dieu dans l'homme, comme l'agneau dans l'homme, rire_ en le d
ch-p4-14-v22 [de] | trailing dash artifact | Das, Das ist deine Seligkeit! Eines Panthers und Adlers Seligkeit! Eines Dichters und Narren Seligkeit!“—
ch-p4-14-v22 [en] | trailing dash artifact | THAT, THAT is thine own blessedness! Of a panther and eagle—blessedness! Of a poet and fool—the blessedness!—
ch-p4-14-v23 [en] | trailing dash artifact | In evening’s limpid air, What time the moon’s sickle, Green, ‘twixt the purple-glowings, And jealous, steal’th forth: —O
ch-p4-14-v23 [fr] | trailing dash artifact | Dans l'air clarifié, quand déjà le croissant de la lune glisse ses rayons verts, envieusement, parmi la pourpre du couch
ch-p4-14-v23 [es] | trailing dash artifact | - Hostil al día, A cada paso secretamente Segando inclinadas praderas de rosas, Hasta que éstas caen, Se hunden pálidas 
ch-p4-15-v03 [de] | trailing dash artifact | Wehe allen freien Geistern, welche nicht vor solchen Zauberern auf der Hut sind! Dahin ist es mit ihrer Freiheit: du leh
ch-p4-15-v03 [en] | trailing dash artifact | Alas, to all free spirits who are not on their guard against SUCH magicians! It is all over with their freedom: thou tea
ch-p4-15-v11 [de] | trailing dash artifact | Wir suchen Verschiednes auch hier oben, ihr und ich. Ich nämlich suche mehr Sicherheit, desshalb kam ich zu Zarathustra.
ch-p4-15-v11 [en] | trailing dash artifact | We SEEK different things even here aloft, ye and I. For I seek more SECURITY; on that account have I come to Zarathustra
ch-p4-15-v13 [de] | trailing dash artifact | —mehr Schauder, mehr Gefahr, mehr Erdbeben. Euch gelüstet, fast dünkt mich's so, vergebt meinem Dünkel, ihr höheren Mens
ch-p4-15-v13 [en] | trailing dash artifact | —More horror, more danger, more earthquake. Ye long (it almost seemeth so to me—forgive my presumption, ye higher men)—
ch-p4-15-v18 [de] | trailing dash artifact | Solche lange alte Furcht, endlich fein geworden, geistlich, geistig—heute, dünkt mich, heisst sie: Wissenschaft.“—
ch-p4-15-v18 [en] | trailing dash artifact | Such prolonged ancient fear, at last become subtle, spiritual and intellectual—at present, me thinketh, it is called SCI
ch-p4-15-v18 [fr] | trailing dash artifact | Cette longue et vieille crainte, enfin affinée et spiritualisée, - aujourd'hui il me semble qu'elle s'appelle Science." 
ch-p4-16-v03 [de] | trailing dash artifact | Diese Könige mögen wohl vor uns noch gute Miene machen: das lernten Die nämlich von uns Allen heute am Besten! Hätten si
ch-p4-16-v03 [en] | trailing dash artifact | Those kings may well put on a good air before us still: for that have THEY learned best of us all at present! Had they h
ch-p4-16-v09 [de] | trailing dash artifact | Es sei denn,—es sei denn—, oh vergieb eine alte Erinnerung! Vergieb mir ein altes Nachtisch-Lied, das ich einst unter Tö
ch-p4-16-v09 [en] | trailing dash artifact | Unless it be,—unless it be—, do forgive an old recollection! Forgive me an old after-dinner song, which I once composed 
ch-p4-16-v12 [de] | trailing dash artifact | Ihr glaubt es nicht, wie artig sie dasassen, wenn sie nicht tanzten, tief, aber ohne Gedanken, wie kleine Geheimnisse, w
ch-p4-16-v12 [en] | trailing dash artifact | Ye would not believe how charmingly they sat there, when they did not dance, profound, but without thoughts, like little
ch-p4-16-v22 [de] | trailing dash artifact | Oh weint mir nicht, Weiche Herzen! Weint mir nicht, ihr Dattel-Herzen! Milch-Busen! Ihr Süssholz-Herz- Beutelchen! Weine
ch-p4-18-v04 [de] | trailing dash artifact | Und du selber, du alter Papst, wie stimmt Das mit dir selber zusammen, dass du solchergestalt einen Esel hier als Gott a
ch-p4-18-v04 [en] | trailing dash artifact | And thou thyself, thou old pope, how is it in accordance with thee, to adore an ass in such a manner as God?”—
ch-p4-18-v08 [fr] | trailing dash artifact | Mon vieux coeur saute et bondit de ce qu'il y ait encore quelque chose à adorer sur la terre. Pardonne, ô Zarathoustra, 
ch-p4-18-v22 [es] | soft-hyphen U+00AD present; trailing dash artifact | ¿No le gusta a un sabio perfecto caminar por los caminos más torcidos? La evidencia lo enseña, oh Zaratustra, ¡tu evi­ -
ch-p4-18-v33 [de] | trailing dash artifact | Wie doch einem jeden von euch das Herz zappelte vor Lust und Bosheit, darob, dass ihr endlich einmal wieder wurdet wie d
ch-p4-18-v33 [en] | trailing dash artifact | How the hearts of all of you convulsed with delight and wickedness, because ye had at last become again like little chil
ch-p4-18-v36 [es] | soft-hyphen U+00AD present; trailing dash artifact | Ciertamente: mientras no os hagáis como niños pequeños no entraréis en aquel reino de los cielos (Y Zaratustra señaló co
ch-p4-18-v38 [de] | trailing dash artifact | Und noch einmal hob Zarathustra an zu reden. „Oh meine neuen Freunde, sprach er,—ihr Wunderlichen, ihr höheren Menschen,
ch-p4-18-v38 [en] | trailing dash artifact | And once more began Zarathustra to speak. “O my new friends,” said he,— “ye strange ones, ye higher men, how well do ye 
ch-p4-19-v01 [de] | trailing dash artifact | Inzwischen aber war Einer nach dem Andern hinaus getreten, in's Freie und in die kühle nachdenkliche Nacht; Zarathustra 
ch-p4-19-v01 [en] | trailing dash artifact | Meanwhile one after another had gone out into the open air, and into the cool, thoughtful night; Zarathustra himself, ho
ch-p4-19-v01 [fr] | trailing dash artifact | Mais pendant qu'il parlait, ils étaient tous sortis l'un après l'autre, en plein air et dans la nuit fraîche et pensive;
ch-p4-19-v06 [de] | trailing dash artifact | Meine Freunde, was dünket euch? Wollt ihr nicht gleich mir zum Tode sprechen: War Das—das Leben? Um Zarathustra's Willen
ch-p4-19-v06 [en] | trailing dash artifact | My friends, what think ye? Will ye not, like me, say unto death: ‘Was THAT—life? For the sake of Zarathustra, well! Once
ch-p4-19-v06 [fr] | trailing dash artifact | Mes amis, que vous en semble? Ne voulez-vous pas, comme moi, dire à la mort: "Est-ce là la vie, eh bien, pour l'amour de
ch-p4-19-v07 [es] | digit glued to letter (OCR) | "¿Esto era - la vida?" quiero decirle yo a la muerte. '¡Bien! ¡Otra vez!58P' Amigos míos, ¿qué os parece? ¿No queréis vo
ch-p4-19-v09 [es] | soft-hyphen U+00AD present | Mas Zaratustra, mientras esto ocurría con el más feo de los hombres, estaba allí como un borracho: su mirada se apagaba,
ch-p4-19-v12 [de] | trailing dash artifact | Ihr höheren Menschen, es geht gen Mitternacht: da will ich euch Etwas in die Ohren sagen, wie jene alte Glocke es mir in
ch-p4-19-v12 [en] | trailing dash artifact | Ye higher men, it is getting on to midnight: then will I say something into your ears, as that old clock-bell saith it i
ch-p4-19-v15 [de] | trailing dash artifact | Still! Still! Da hört sich Manches, das am Tage nicht laut werden darf; nun aber, bei kühler Luft, da auch aller Lärm eu
ch-p4-19-v15 [en] | trailing dash artifact | Hush! Hush! Then is there many a thing heard which may not be heard by day; now however, in the cool air, when even all 
ch-p4-19-v18 [de] | trailing dash artifact | Wehe mir! Wo ist die Zeit hin? Sank ich nicht in tiefe Brunnen? Die Welt schläft—
ch-p4-19-v18 [en] | trailing dash artifact | Woe to me! Whither hath time gone? Have I not sunk into deep wells? The world sleepeth—
ch-p4-19-v18 [fr] | trailing dash artifact | Malheur à moi! Où a passé le temps? Ne suis-je pas tombé dans des puits profonds? Le monde dort -
ch-p4-19-v20 [de] | trailing dash artifact | Nun starb ich schon. Es ist dahin. Spinne, was spinnst du um mich? Willst du Blut? Ach! Ach! der Thau fällt, die Stunde 
ch-p4-19-v20 [en] | trailing dash artifact | Already have I died. It is all over. Spider, why spinnest thou around me? Wilt thou have blood? Ah! Ah! The dew falleth,
ch-p4-19-v28 [de] | trailing dash artifact | Ihr höheren Menschen, erlöst doch die Gräber, weckt die Leichname auf! Ach, was gräbt noch der Wurm? Es naht, es naht di
ch-p4-19-v28 [en] | trailing dash artifact | Ye higher men, free the sepulchres, awaken the corpses! Ah, why doth the worm still burrow? There approacheth, there app
ch-p4-19-v31 [de] | trailing dash artifact | Du alte Glocke, du süsse Leier! Jeder Schmerz riss dir in's Herz, Vaterschmerz, Väterschmerz, Urväterschmerz, deine Rede
ch-p4-19-v31 [en] | trailing dash artifact | Thou old clock-bell, thou sweet lyre! Every pain hath torn thy heart, father-pain, fathers’-pain, forefathers’-pain; thy
ch-p4-19-v40 [de] | trailing dash artifact | Oh Welt, du willst mich? Bin ich dir weltlich? Bin ich dir geistlich? Bin ich dir göttlich? Aber Tag und Welt, ihr seid 
ch-p4-19-v40 [en] | trailing dash artifact | O world, thou wantest ME? Am I worldly for thee? Am I spiritual for thee? Am I divine for thee? But day and world, ye ar
ch-p4-19-v43 [de] | trailing dash artifact | Gottes Weh ist tiefer, du wunderliche Welt! Greife nach Gottes Weh, nicht nach mir! Was bin ich! Eine trunkene süsse Lei
ch-p4-19-v43 [en] | trailing dash artifact | God’s woe is deeper, thou strange world! Grasp at God’s woe, not at me! What am I! A drunken sweet lyre,—
ch-p4-19-v43 [es] | trailing dash artifact | ¡El dolor de Dios es más profundo, oh mundo extraño! ¡Tiende tus manos hacia el dolor de Dios, no hacia mí! ¡Qué soy yo!
ch-p4-19-v52 [de] | trailing dash artifact | —sehnsüchtig nach Fernerem, Höherem, Hellerem. „Ich will Erben, so spricht Alles, was leidet, ich will Kinder, ich will 
ch-p4-19-v52 [en] | trailing dash artifact | —Longing for the further, the higher, the brighter. “I want heirs,” so saith everything that suffereth, “I want children
ch-p4-19-v52 [fr] | trailing dash artifact | La douleur dit: "Passe! va-t'en douleur!" Mais tout ce qui souffre veut vivre, pour mûrir, pour devenir joyeux et plein 
ch-p4-19-v56 [de] | trailing dash artifact | Ein Tropfen Thau's? Ein Dunst und Duft der Ewigkeit? Hört ihr's nicht? Riecht ihr's nicht? Eben ward meine Welt vollkomm
ch-p4-19-v56 [en] | trailing dash artifact | Or a drop of dew? Or a fume and fragrance of eternity? Hear ye it not? Smell ye it not? Just now hath my world become pe
ch-p4-19-v58 [de] | trailing dash artifact | Sagtet ihr jemals ja zu Einer Lust? Oh, meine Freunde, so sagtet ihr Ja auch zu allem Wehe. Alle Dinge sind verkettet, v
ch-p4-19-v58 [en] | trailing dash artifact | Said ye ever Yea to one joy? O my friends, then said ye Yea also unto ALL woe. All things are enlinked, enlaced and enam
ch-p4-19-v60 [de] | trailing dash artifact | —Alles von neuem, Alles ewig, Alles verkettet, verfädelt, verliebt, oh so liebtet ihr die Welt,—
ch-p4-19-v60 [en] | trailing dash artifact | —All anew, all eternal, all enlinked, enlaced and enamoured, Oh, then did ye LOVE the world,—
ch-p4-19-v62 [de] | trailing dash artifact | Alle Lust will aller Dinge Ewigkeit, will Honig, will Hefe, will trunkene Mitternacht, will Gräber, will Gräber-Thränen-
ch-p4-19-v62 [en] | trailing dash artifact | All joy wanteth the eternity of all things, it wanteth honey, it wanteth lees, it wanteth drunken midnight, it wanteth g
ch-p4-19-v62 [fr] | trailing dash artifact | Avez-vous jamais approuvé une joie? O mes amis, alors vous avez aussi approuvé toutes les douleurs. Toutes les choses so
ch-p4-19-v63 [de] | trailing dash artifact | —was will nicht Lust! sie ist durstiger, herzlicher, hungriger, schrecklicher, heimlicher als alles Weh, sie will sich, 
ch-p4-19-v63 [en] | trailing dash artifact | —WHAT doth not joy want! it is thirstier, heartier, hungrier, more frightful, more mysterious, than all woe: it wanteth 
ch-p4-19-v64 [de] | trailing dash artifact | —sie will Liebe, sie will Hass, sie ist überreich, schenkt, wirft weg, bettelt, dass Einer sie nimmt, dankt dem Nehmende
ch-p4-19-v64 [en] | trailing dash artifact | —It wanteth love, it wanteth hate, it is over-rich, it bestoweth, it throweth away, it beggeth for some one to take from
ch-p4-20-v06 [es] | trailing dash artifact | Ellos duermen todavía en mi caverna, sus sueños siguen rumiando mis mediasnoches. El oído que me escuche a mí, -
ch-p4-20-v09 [de] | trailing dash artifact | Aber noch fehlen mir meine rechten Menschen!“—
ch-p4-20-v09 [en] | trailing dash artifact | But still do I lack my proper men!”—
ch-p4-20-v09 [es] | trailing dash artifact | ¡Pero todavía me faltan mis hombres adecuados!» -
ch-p4-20-v13 [de] | trailing dash artifact | Zu dem Allen sprach Zarathustra nur Ein Wort: „meine Kinder sind nahe, meine Kinder“—, dann wurde er ganz stumm. Sein He
ch-p4-20-v13 [en] | trailing dash artifact | When all this went on Zarathustra spake only a word: “MY CHILDREN ARE NIGH, MY CHILDREN”—, then he became quite mute. Hi
ch-p4-20-v17 [de] | trailing dash artifact | Oh ihr höheren Menschen, von eurer Noth war's ja, dass gestern am Morgen jener alte Wahrsager mir wahrsagte,—
ch-p4-20-v17 [en] | trailing dash artifact | O ye higher men, YOUR distress was it that the old soothsayer foretold to me yester-morn,—
ch-p4-20-v20 [de] | trailing dash artifact | —Und noch ein Mal versank Zarathustra in sich und setzte sich wieder auf den grossen Stein nieder und sann nach. Plötzli
ch-p4-20-v20 [en] | trailing dash artifact | —And once more Zarathustra became absorbed in himself, and sat down again on the big stone and meditated. Suddenly he sp
ch-p4-20-v23 [de] | trailing dash artifact | Wohlan! Der Löwe kam, meine Kinder sind nahe, Zarathustra ward reif, meine Stunde kam:—
ch-p4-20-v23 [en] | trailing dash artifact | Well! The lion hath come, my children are nigh, Zarathustra hath grown ripe, mine hour hath come:—
ch-p4-20-v24 [de] | trailing dash artifact | Dies ist mein Morgen, mein Tag hebt an: herauf nun, herauf, du grosser Mittag!“—
ch-p4-20-v24 [en] | trailing dash artifact | This is MY morning, MY day beginneth: ARISE NOW, ARISE, THOU GREAT NOONTIDE!”—
ch-p4-20-v24 [es] | trailing dash artifact | ¡Bien! El león ha llegado, mis hijos están cerca, Zaratustra está ya maduro, mi hora ha llegado: - Ésta es mi mañana, mi

### Empty translations (DE present, target empty)
ch-p1-01-v02 [fr] | EMPTY while DE non-empty | DE: Vieles Schwere giebt es dem Geiste, dem starken, tragsamen Geiste, dem Ehrfurcht
ch-p1-02-v18 [es] | EMPTY while DE non-empty | DE: Sehr gefallen mir auch die Geistig-Armen: sie fördern den Schlaf. Selig sind die
ch-p1-02-v24 [es] | EMPTY while DE non-empty | DE: Wahrlich, auf weichen Sohlen kommt er mir, der liebste der Diebe, und stiehlt mi
ch-p1-03-v05 [es] | EMPTY while DE non-empty | DE: Diese Welt, die ewig unvollkommene, eines ewigen Widerspruches Abbild und unvoll
ch-p1-03-v31 [es] | EMPTY while DE non-empty | DE: Wahrlich nicht an Hinterwelten und erlösende Blutstropfen: sondern an den Leib g
ch-p1-07-v12 [es] | EMPTY while DE non-empty | DE: Wer von euch kann zugleich lachen und erhoben sein?
ch-p1-07-v13 [es] | EMPTY while DE non-empty | DE: Wer auf den höchsten Bergen steigt, der lacht über alle Trauer-Spiele und Trauer
ch-p1-07-v16 [es] | EMPTY while DE non-empty | DE: Das Leben ist schwer zu tragen: aber so thut mir doch nicht so zärtlich! Wir sin
ch-p1-07-v18 [es] | EMPTY while DE non-empty | DE: Es ist wahr: wir lieben das Leben, nicht, weil wir an's Leben, sondern weil wir 
ch-p1-07-v19 [es] | EMPTY while DE non-empty | DE: Es ist immer etwas Wahnsinn in der Liebe. Es ist aber immer auch etwas Vernunft 
ch-p1-08-v03 [es] | EMPTY while DE non-empty | DE: Aber der Wind, den wir nicht sehen, der quält und biegt ihn, wohin er will. Wir 
ch-p1-08-v36 [en] | EMPTY while DE non-empty | DE: Also sprach Zarathustra.
ch-p1-08-v36 [fr] | EMPTY while DE non-empty | DE: Also sprach Zarathustra.
ch-p1-08-v36 [es] | EMPTY while DE non-empty | DE: Also sprach Zarathustra.
ch-p1-09-v13 [es] | EMPTY while DE non-empty | DE: „Das Leben ist nur Leiden“ —so sagen Andre und lügen nicht: so sorgt doch, dass 
ch-p1-09-v14 [es] | EMPTY while DE non-empty | DE: Und also laute die Lehre eurer Tugend „du sollst dich selber tödten! Du sollst d
ch-p1-10-v07 [es] | EMPTY while DE non-empty | DE: Euren Feind sollt ihr suchen, euren Krieg sollt ihr führen und für eure Gedanken
ch-p1-12-v08 [es] | EMPTY while DE non-empty | DE: Morgen hat er einen neuen Glauben und übermorgen einen neueren. Rasche Sinne hat
ch-p1-13-v13 [es] | EMPTY while DE non-empty | DE: Und auch diess Gleichniss gebe ich euch: nicht Wenige, die ihren Teufel austreib
ch-p1-13-v14 [es] | EMPTY while DE non-empty | DE: Wem die Keuschheit schwer fällt, dem ist sie zu widerrathen: dass sie nicht der 
ch-p1-14-v19 [es] | EMPTY while DE non-empty | DE: Bist du reine Luft und Einsamkeit und Brod und Arznei deinem Freunde? Mancher ka
ch-p1-15-v04 [es] | EMPTY while DE non-empty | DE: Nie verstand ein Nachbar den andern: stets verwunderte sich seine Seele ob des N
ch-p1-15-v11 [es] | EMPTY while DE non-empty | DE: „Vater und Mutter ehren und bis in die Wurzel der Seele hinein ihnen zu Willen s
ch-p1-15-v14 [es] | EMPTY while DE non-empty | DE: Werthe legte erst der Mensch in die Dinge, sich zu erhalten,—er schuf erst den D
ch-p1-18-v02 [es] | EMPTY while DE non-empty | DE: Ist es ein Schatz, der dir geschenkt? Oder ein Kind, das dir geboren wurde? Oder
ch-p1-18-v05 [fr] | EMPTY while DE non-empty | DE: Als ich heute allein meines Weges gieng, zur Stunde, wo die Sonne sinkt, begegne
ch-p1-18-v27 [es] | EMPTY while DE non-empty | DE: Des Mannes Gemüth aber ist tief, sein Strom rauscht in unterirdischen Höhlen: da
ch-p1-18-v29 [es] | EMPTY while DE non-empty | DE: Seltsam ist's, Zarathustra kennt wenig die Weiber, und doch hat er über sie Rech
ch-p1-19-v10 [es] | EMPTY while DE non-empty | DE: Ich mag eure kalte Gerechtigkeit nicht; und aus dem Auge eurer Richter blickt mi
ch-p1-20-v05 [fr] | EMPTY while DE non-empty | DE: Ich will, dass dein Sieg und deine Freiheit sich nach einem Kinde sehne. Lebendi
ch-p1-20-v06 [es] | EMPTY while DE non-empty | DE: Über dich sollst du hinausbauen. Aber erst musst du mir selber gebaut sein, rech
ch-p1-20-v11 [es] | EMPTY while DE non-empty | DE: Ach, diese Armuth der Seele zu Zweien! Ach, dieser Schmutz der Seele zu Zweien! 
ch-p1-20-v19 [es] | EMPTY while DE non-empty | DE: Jener war spröde im Verkehre und wählte wählerisch. Aber mit Einem Male verdarb 
ch-p1-20-v25 [es] | EMPTY while DE non-empty | DE: Über euch hinaus sollt ihr einst lieben! So lernt erst lieben! Und darum musstet
ch-p1-21-v10 [es] | EMPTY while DE non-empty | DE: Aber dem Kämpfenden gleich verhasst wie dem Sieger ist euer grinsender Tod, der 
ch-p1-21-v27 [es] | EMPTY while DE non-empty | DE: Wäre er doch in der Wüste geblieben und ferne von den Guten und Gerechten! Viell
ch-p1-21-v35 [es] | EMPTY while DE non-empty | DE: Wahrlich, ein Ziel hatte Zarathustra, er warf seinen Ball: nun seid ihr Freunde 
ch-p1-22-v09 [es] | EMPTY while DE non-empty | DE: Wahrlich, zum Räuber an allen Werthen muss solche schenkende Liebe werden; aber 
ch-p1-22-v44 [es] | EMPTY while DE non-empty | DE: Der Mensch der Erkenntniss muss nicht nur seine Feinde lieben, sondern auch sein
ch-p1-22-v45 [es] | EMPTY while DE non-empty | DE: Man vergilt einem Lehrer schlecht, wenn man immer nur der Schüler bleibt. Und wa
ch-p1-22-v48 [es] | EMPTY while DE non-empty | DE: Ihr hattet euch noch nicht gesucht: da fandet ihr mich. So thun alle Gläubigen; 
ch-p1-22-v57 [en] | EMPTY while DE non-empty | DE: Zarathustra, von der schenkenden Tugend
ch-p1-22-v57 [fr] | EMPTY while DE non-empty | DE: Zarathustra, von der schenkenden Tugend
ch-p1-22-v57 [es] | EMPTY while DE non-empty | DE: Zarathustra, von der schenkenden Tugend
ch-p2-01-v01 [es] | EMPTY while DE non-empty | DE: Hierauf gieng Zarathustra wieder zurück in das Gebirge und in die Einsamkeit sei
ch-p2-01-v07 [es] | EMPTY while DE non-empty | DE: Wahrlich, allzugut verstehe ich des Traumes Zeichen und Mahnung: meine Lehre ist
ch-p2-01-v08 [es] | EMPTY while DE non-empty | DE: Meine Feinde sind mächtig worden und haben meiner Lehre Bildniss entstellt, also
ch-p2-01-v22 [es] | EMPTY while DE non-empty | DE: Wie ein Schrei und ein jauchzen will ich über weite Meere hinfahren, bis ich die
ch-p2-01-v24 [es] | EMPTY while DE non-empty | DE: Und wenn ich auf mein wildestes Pferd steigen will, so hilft mir mein Speer imme
ch-p2-02-v07 [es] | EMPTY while DE non-empty | DE: Nicht ihr vielleicht selber, meine Brüder! Aber zu Vätern und Vorfahren könntet 
ch-p2-02-v12 [es] | EMPTY while DE non-empty | DE: Aber dass ich euch ganz mein Herz offenbare, ihr Freunde: wenn es Götter gäbe, w
ch-p2-02-v17 [es] | EMPTY while DE non-empty | DE: Böse heisse ich's und menschenfeindlich: all diess Lehren vom Einen und Vollen u
ch-p2-03-v26 [es] | EMPTY while DE non-empty | DE: Dem aber, der vom Teufel besessen ist, sage ich diess Wort in's Ohr: „besser noc
ch-p2-03-v28 [es] | EMPTY while DE non-empty | DE: Es ist schwer, mit Menschen zu leben, weil Schweigen so schwer ist.
ch-p2-03-v37 [es] | EMPTY while DE non-empty | DE: Und jüngst hörte ich ihn diess Wort sagen: „Gott ist todt; an seinem Mitleiden m
ch-p2-04-v02 [es] | EMPTY while DE non-empty | DE: „Hier sind Priester: und wenn es auch meine Feinde sind, geht mir still an ihnen
ch-p2-04-v04 [es] | EMPTY while DE non-empty | DE: Böse Feinde sind sie: Nichts ist rachsüchtiger als ihre Demuth. Und leicht besud
ch-p2-04-v08 [es] | EMPTY while DE non-empty | DE: Aber ich leide und litt mit ihnen: Gefangene sind es mir und Abgezeichnete. Der,
ch-p2-04-v09 [es] | EMPTY while DE non-empty | DE: In Banden falscher Werthe und Wahn-Worte! Ach dass Einer sie noch von ihrem Erlö
ch-p2-04-v18 [fr] | EMPTY while DE non-empty | DE: Und erst wenn der reine Himmel wieder durch zerbrochne Decken blickt, und hinab 
ch-p2-04-v19 [fr] | EMPTY while DE non-empty | DE: Sie nannten Gott, was ihnen widersprach und wehe that: und wahrlich, es war viel
ch-p2-04-v23 [es] | EMPTY while DE non-empty | DE: Bessere Lieder müssten sie mir singen, dass ich an ihren Erlöser glauben lerne: 
ch-p2-04-v29 [es] | EMPTY while DE non-empty | DE: Kleine Geister und umfängliche Seelen hatten diese Hirten: aber, meine Brüder, w
ch-p2-04-v36 [es] | EMPTY while DE non-empty | DE: Niemals noch gab es einen Übermenschen. Nackt sah ich Beide, den grössten und de
ch-p2-05-v15 [es] | EMPTY while DE non-empty | DE: Dass eure Tugend euer Selbst sei und nicht ein Fremdes, eine Haut, eine Bemäntel
ch-p2-05-v22 [es] | EMPTY while DE non-empty | DE: Wahrlich, an Diesen habe ich meine Lust: wo ich solche Uhren finde, werde ich si
ch-p2-05-v24 [es] | EMPTY while DE non-empty | DE: Ach, wie übel ihnen das Wort „Tugend“ aus dem Munde läuft! Und wenn sie sagen: „
ch-p2-05-v36 [es] | EMPTY while DE non-empty | DE: Müde würdet der Worte „Lohn,“ „Vergeltung,“ „Strafe,“ „Rache in der Gerechtigkei
ch-p2-06-v09 [es] | EMPTY while DE non-empty | DE: Und Mancher, der wie ein Vernichter daher kam und wie ein Hagelschlag allen Fruc
ch-p2-06-v22 [es] | EMPTY while DE non-empty | DE: Fast zu heftig strömst du mir, Quell der Lust! Und oft leerst du den Becher wied
ch-p2-06-v33 [en] | EMPTY while DE non-empty | DE: Also sprach Zarathustra.
ch-p2-06-v33 [fr] | EMPTY while DE non-empty | DE: Also sprach Zarathustra.
ch-p2-06-v33 [es] | EMPTY while DE non-empty | DE: Also sprach Zarathustra.
ch-p2-07-v35 [es] | EMPTY while DE non-empty | DE: Dass Kampf und Ungleiches auch noch in der Schönheit sei und Krieg um Macht und 
ch-p2-07-v36 [es] | EMPTY while DE non-empty | DE: Wie sich göttlich hier Gewölbe und Bogen brechen, im Ringkampfe: wie mit Licht u
ch-p2-07-v38 [es] | EMPTY while DE non-empty | DE: Wehe! Da biss mich selber die Tarantel, meine alte Feindin! Göttlich sicher und 
ch-p2-09-v02 [es] | EMPTY while DE non-empty | DE: Nacht ist es: nun erst erwachen alle Lieder der Liebenden. Und auch meine Seele 
ch-p2-09-v03 [es] | EMPTY while DE non-empty | DE: Ein Ungestilltes, Unstillbares ist in mir; das will laut werden. Eine Begierde n
ch-p2-09-v05 [es] | EMPTY while DE non-empty | DE: Ach, dass ich dunkel wäre und nächtig! Wie wollte ich an den Brüsten des Lichts 
ch-p2-09-v06 [es] | EMPTY while DE non-empty | DE: Und euch selber wollte ich noch segnen, ihr kleinen Funkelsterne und Leuchtwürme
ch-p2-09-v07 [es] | EMPTY while DE non-empty | DE: Aber ich lebe in meinem eignen Lichte, ich trinke die Flammen in mich zurück, di
ch-p2-09-v08 [es] | EMPTY while DE non-empty | DE: Ich kenne das Glück des Nehmenden nicht; und oft träumte mir davon, dass Stehlen
ch-p2-09-v09 [es] | EMPTY while DE non-empty | DE: Das ist meine Armuth, dass meine Hand niemals ausruht vom Schenken; das ist mein
ch-p2-09-v10 [es] | EMPTY while DE non-empty | DE: Oh Unseligkeit aller Schenkenden! Oh Verfinsterung meiner Sonne! Oh Begierde nac
ch-p2-09-v11 [es] | EMPTY while DE non-empty | DE: Sie nehmen von mir: aber rühre ich noch an ihre Seele? Eine Kluft ist zwischen G
ch-p2-09-v12 [es] | EMPTY while DE non-empty | DE: Ein Hunger wächst aus meiner Schönheit: wehethun möchte ich Denen, welchen ich l
ch-p2-09-v13 [es] | EMPTY while DE non-empty | DE: Die Hand zurückziehend, wenn sich schon ihr die Hand entgegenstreckt; dem Wasser
ch-p2-09-v14 [es] | EMPTY while DE non-empty | DE: Solche Rache sinnt meine Fülle aus; solche Tücke quillt aus meiner Einsamkeit.
ch-p2-09-v15 [es] | EMPTY while DE non-empty | DE: Mein Glück im Schenken erstarb im Schenken, meine Tugend wurde ihrer selber müde
ch-p2-09-v16 [es] | EMPTY while DE non-empty | DE: Wer immer schenkt, dessen Gefahr ist, dass er die Scham verliere; wer immer aust
ch-p2-09-v17 [es] | EMPTY while DE non-empty | DE: Mein Auge quillt nicht mehr über vor der Scham der Bittenden; meine Hand wurde z
ch-p2-09-v18 [es] | EMPTY while DE non-empty | DE: Wohin kam die Thräne meinem Auge und der Flaum meinem Herzen? Oh Einsamkeit alle
ch-p2-09-v19 [es] | EMPTY while DE non-empty | DE: Viel Sonnen kreisen im öden Räume: zu Allem, was dunkel ist, reden sie mit ihrem
ch-p2-09-v20 [es] | EMPTY while DE non-empty | DE: Oh diess ist die Feindschaft des Lichts gegen Leuchtendes, erbarmungslos wandelt
ch-p2-09-v21 [es] | EMPTY while DE non-empty | DE: Unbillig gegen Leuchtendes im tiefsten Herzen: kalt gegen Sonnen,—also wandelt j
ch-p2-09-v22 [es] | EMPTY while DE non-empty | DE: Einem Sturme gleich fliegen die Sonnen ihre Bahnen, das ist ihr Wandeln. Ihrem u
ch-p2-09-v23 [es] | EMPTY while DE non-empty | DE: Oh, ihr erst seid es, ihr Dunklen, ihr Nächtigen, die ihr Wärme schafft aus Leuc
ch-p2-09-v24 [es] | EMPTY while DE non-empty | DE: Ach, Eis ist um mich, meine Hand verbrennt sich an Eisigem! Ach, Durst ist in mi
ch-p2-09-v25 [es] | EMPTY while DE non-empty | DE: Nacht ist es: ach dass ich Licht sein muss! Und Durst nach Nächtigem! Und Einsam
ch-p2-09-v27 [es] | EMPTY while DE non-empty | DE: Nacht ist es: nun reden lauter alle springenden Brunnen. Und auch meine Seele is
ch-p2-09-v28 [es] | EMPTY while DE non-empty | DE: Nacht ist es: nun erst erwachen alle Lieder der Liebenden. Und auch meine Seele 
ch-p2-10-v09 [es] | EMPTY while DE non-empty | DE: Ein Tanz- und Spottlied auf den Geist der Schwere, meinen allerhöchsten grossmäc
ch-p2-11-v01 [es] | EMPTY while DE non-empty | DE: „Dort ist die Gräberinsel, die schweigsame; dort sind auch die Gräber meiner Jug
ch-p2-11-v05 [es] | EMPTY while DE non-empty | DE: Immer noch bin ich der Reichste und Bestzubeneidende—ich der Einsamste! Denn ich
ch-p2-12-v16 [es] | EMPTY while DE non-empty | DE: Diess aber ist das Dritte, was ich hörte: dass Befehlen schwerer ist, als Gehorc
ch-p2-12-v35 [es] | EMPTY while DE non-empty | DE: Vieles ist dem Lebenden höher geschätzt, als Leben selber; doch aus dem Schätzen
ch-p2-12-v41 [es] | EMPTY while DE non-empty | DE: Also gehört das höchste Böse zur höchsten Güte: diese aber ist die schöpferische
ch-p2-12-v44 [en] | EMPTY while DE non-empty | DE: Also sprach Zarathustra.
ch-p2-12-v44 [fr] | EMPTY while DE non-empty | DE: Also sprach Zarathustra.
ch-p2-13-v09 [es] | EMPTY while DE non-empty | DE: Und ihr sagt mir, Freunde, dass nicht zu streiten sei über Geschmack und Schmeck
ch-p2-14-v12 [es] | EMPTY while DE non-empty | DE: Alle Zeiten und Völker blicken bunt aus euren Schleiern; alle Sitten und Glauben
ch-p2-14-v22 [es] | EMPTY while DE non-empty | DE: Unfruchtbare seid ihr: darum fehlt es euch an Glauben. Aber wer schaffen musste,
ch-p2-14-v30 [es] | EMPTY while DE non-empty | DE: Wahrlich, es soll mir darob nicht schwerer werden! Und nicht aus euch, ihr Gegen
ch-p2-14-v35 [en] | EMPTY while DE non-empty | DE: Also sprach Zarathustra.
ch-p2-14-v35 [fr] | EMPTY while DE non-empty | DE: Also sprach Zarathustra.
ch-p2-15-v02 [es] | EMPTY while DE non-empty | DE: Aber ein Lügner war er mir mit seiner Schwangerschaft; und eher noch will ich an
ch-p2-15-v07 [es] | EMPTY while DE non-empty | DE: Jedes Redlichen Schritt redet; die Katze aber stiehlt sich über den Boden weg. S
ch-p2-15-v15 [es] | EMPTY while DE non-empty | DE: Und das heisse mir aller Dinge unbefleckte Erkenntniss, dass ich von den Dingen 
ch-p2-16-v15 [es] | EMPTY while DE non-empty | DE: Gute Uhrwerke sind sie: nur sorge man, sie richtig aufzuziehn! Dann zeigen sie o
ch-p2-17-v14 [es] | EMPTY while DE non-empty | DE: Und wer von uns Dichtern hätte nicht seinen Wein verfälscht? Manch giftiger Misc
ch-p2-17-v23 [es] | EMPTY while DE non-empty | DE: Wahrlich, immer zieht es uns hinan—nämlich zum Reich der Wolken: auf diese setze
ch-p2-17-v31 [es] | EMPTY while DE non-empty | DE: Gespenster-Hauch und -Huschen gilt mir all ihr Harfen-Klingklang; was wussten si
ch-p2-17-v32 [es] | EMPTY while DE non-empty | DE: Sie sind mir auch nicht reinlich genug: sie trüben Alle ihr Gewässer, dass es ti
ch-p2-17-v42 [es] | EMPTY while DE non-empty | DE: Zuschauer will der Geist des Dichters: sollten's auch Büffel sein!—
ch-p2-18-v01 [es] | EMPTY while DE non-empty | DE: Es giebt eine Insel im Meere—unweit den glückseligen Inseln Zarathustra's—auf we
ch-p2-18-v03 [es] | EMPTY while DE non-empty | DE: „Seht mir an! sagte der alte Steuermann, da fährt Zarathustra zur Hölle!“—
ch-p2-18-v05 [es] | EMPTY while DE non-empty | DE: Also entstand eine Unruhe; nach drei Tagen aber kam zu dieser Unruhe die Geschic
ch-p2-18-v06 [es] | EMPTY while DE non-empty | DE: Und diess ist die Erzählung von Zarathustra's Gespräch mit dem Feuerhunde.
ch-p2-18-v13 [es] | EMPTY while DE non-empty | DE: Höchstens für den Bauchredner der Erde halt' ich dich: und immer, wenn ich Umstu
ch-p2-18-v18 [es] | EMPTY while DE non-empty | DE: Nicht um die Erfinder von neuem Lärme: um die Erfinder von neuen Werthen dreht s
ch-p2-18-v23 [es] | EMPTY while DE non-empty | DE: Diesen Rath aber rathe ich Königen und Kirchen und Allem, was alters- und tugend
ch-p2-18-v26 [es] | EMPTY while DE non-empty | DE: Gleich dir selber ist der Staat ein Heuchelhund; gleich dir redet er gern mit Ra
ch-p2-18-v29 [fr] | EMPTY while DE non-empty | DE: Endlich wurde er stiller, und sein Keuchen liess nach; sobald er aber stille war
ch-p2-18-v35 [es] | EMPTY while DE non-empty | DE: Als diess der Feuerhund vernahm, hielt er's nicht mehr aus, mir zuzuhören. Besch
ch-p2-19-v02 [es] | EMPTY while DE non-empty | DE: Eine Lehre ergieng, ein Glauben lief neben ihr: „Alles ist leer, Alles ist gleic
ch-p2-19-v31 [es] | EMPTY while DE non-empty | DE: Grässlich erschrak ich darob: es warf mich nieder. Und ich schrie vor Grausen, w
ch-p2-19-v42 [es] | EMPTY while DE non-empty | DE: Wahrlich, sie selber träumtest du, deine Feinde: das war dein schwerster Traum!
ch-p2-20-v39 [es] | EMPTY while DE non-empty | DE: Es sei denn, dass der Wille endlich sich selber erlöste und Wollen zu Nicht-Woll
ch-p2-20-v47 [es] | EMPTY while DE non-empty | DE: —Aber an dieser Stelle seiner Rede geschah es, dass Zarathustra plötzlich innehi
ch-p2-21-v05 [es] | EMPTY while DE non-empty | DE: An den Menschen klammert sich mein Wille, mit Ketten binde ich mich an den Mensc
ch-p2-21-v08 [es] | EMPTY while DE non-empty | DE: Ich sitze am Thorwege für jeden Schelm und frage: wer will mich betrügen?
ch-p2-21-v27 [es] | EMPTY while DE non-empty | DE: Zwar, wie eure Weisesten mir nicht gar so weise erschienen: so fand ich auch der
ch-p2-21-v40 [es] | EMPTY while DE non-empty | DE: Aber verkleidet will ich euch sehn, ihr Nächsten und Mitmenschen, und gut geputz
ch-p2-22-v05 [es] | EMPTY while DE non-empty | DE: Und so geschah's,—denn Alles muss ich euch sagen, dass euer Herz sich nicht verh
ch-p2-22-v12 [es] | EMPTY while DE non-empty | DE: Da sprach es abermals ohne Stimme zu mir: „Du weisst es, Zarathustra, aber du re
ch-p2-22-v14 [es] | EMPTY while DE non-empty | DE: Da sprach es wieder ohne Stimme zu mir: „Du willst nicht, Zarathustra? Ist diess
ch-p2-22-v15 [es] | EMPTY while DE non-empty | DE: Und ich weinte und zitterte wie ein Kind und sprach: „Ach, ich wollte schon, abe
ch-p2-22-v17 [es] | EMPTY while DE non-empty | DE: Und ich antwortete: „Ach, ist es mein Wort? Wer bin ich? Ich warte des Würdigere
ch-p2-22-v18 [es] | EMPTY while DE non-empty | DE: Da sprach es wieder ohne Stimme zu mir: „Was liegt an dir? Du bist mir noch nich
ch-p2-22-v20 [es] | EMPTY while DE non-empty | DE: Da sprach es wieder ohne Stimme zu mir: „Oh Zarathustra, wer Berge zu versetzen 
ch-p2-22-v24 [es] | EMPTY while DE non-empty | DE: Und so sprachen sie zu mir: „du verlerntest den Weg, nun verlernst du auch das G
ch-p2-22-v28 [es] | EMPTY while DE non-empty | DE: Das ist dein Unverzeihlichstes: du hast die Macht, und du willst nicht herrschen
ch-p2-22-v30 [es] | EMPTY while DE non-empty | DE: Da sprach es wieder wie ein Flüstern zu mir: „Die stillsten Worte sind es, welch
ch-p2-22-v31 [es] | EMPTY while DE non-empty | DE: Oh Zarathustra, du sollst gehen als ein Schatten dessen, was kommen muss: so wir
ch-p2-22-v34 [es] | EMPTY while DE non-empty | DE: Der Stolz der Jugend ist noch auf dir, spät bist du jung geworden: aber wer zum 
ch-p2-22-v35 [fr] | EMPTY while DE non-empty | DE: Und ich besann mich lange und zitterte. Endlich aber sagte ich, was ich zuerst s
ch-p2-22-v44 [fr] | EMPTY while DE non-empty | DE: „Ihr seht nach Oben, wenn ihr nach Erhebung verlangt. Und ich sehe hinab, weil i
ch-p2-22-v45 [en] | EMPTY while DE non-empty | DE: Zarathustra, vom Lesen und Schreiben.
ch-p2-22-v45 [fr] | EMPTY while DE non-empty | DE: Zarathustra, vom Lesen und Schreiben.
ch-p3-01-v03 [es] | EMPTY while DE non-empty | DE: Und was mir nun auch noch als Schicksal und Erlebniss komme,—ein Wandern wird da
ch-p3-01-v13 [es] | EMPTY while DE non-empty | DE: Wer sich stets viel geschont hat, der kränkelt zuletzt an seiner vielen Schonung
ch-p3-01-v21 [fr] | EMPTY while DE non-empty | DE: Vor meinem höchsten Berge stehe ich und vor meiner längsten Wanderung: darum mus
ch-p3-02-v04 [es] | EMPTY while DE non-empty | DE: —denn nicht wollt ihr mit feiger Hand einem Faden nachtasten; und, wo ihr errath
ch-p3-02-v05 [es] | EMPTY while DE non-empty | DE: euch allein erzähle ich das Räthsel, das ich sah,—das Gesicht des Einsamsten.—
ch-p3-02-v08 [fr] | EMPTY while DE non-empty | DE: Stumm über höhnischem Geklirr von Kieseln schreitend, den Stein zertretend, der 
ch-p3-02-v15 [es] | EMPTY while DE non-empty | DE: Ich stieg, ich stieg, ich träumte, ich dachte,—aber Alles drückte mich. Einem Kr
ch-p3-02-v16 [es] | EMPTY while DE non-empty | DE: Aber es giebt Etwas in mir, das ich Muth heisse: das schlug bisher mir jeden Unm
ch-p3-02-v23 [es] | EMPTY while DE non-empty | DE: „Halt! Zwerg! sprach ich. Ich! Oder du! Ich aber bin der Stärkere von uns Beiden
ch-p3-02-v28 [es] | EMPTY while DE non-empty | DE: Aber wer Einen von ihnen weiter gienge—und immer weiter und immer ferner: glaubs
ch-p3-02-v37 [es] | EMPTY while DE non-empty | DE: —und wiederkommen und in jener anderen Gasse laufen, hinaus, vor uns, in dieser 
ch-p3-02-v41 [es] | EMPTY while DE non-empty | DE: —also dass es mich erbarmte. Eben nämlich gieng der volle Mond, todtschweigsam, 
ch-p3-02-v53 [es] | EMPTY while DE non-empty | DE: —Der Hirt aber biss, wie mein Schrei ihm rieth; er biss mit gutem Bisse! Weit we
ch-p3-03-v03 [fr] | EMPTY while DE non-empty | DE: Des Nachmittags fand ich zum ersten Male einst meine Freunde, des Nachmittags au
ch-p3-03-v11 [fr] | EMPTY while DE non-empty | DE: Und wahrlich! Wo solche Bäume bei einander stehn, da sind glückselige Inseln!
ch-p3-03-v15 [es] | EMPTY while DE non-empty | DE: Erkannt und geprüft soll er werden, darauf, ob er meiner Art und Abkunft ist,—ob
ch-p3-04-v10 [fr] | EMPTY while DE non-empty | DE: Zusammen lernten wir Alles; zusammen lernten wir über uns zu uns selber aufsteig
ch-p3-04-v10 [es] | EMPTY while DE non-empty | DE: Zusammen lernten wir Alles; zusammen lernten wir über uns zu uns selber aufsteig
ch-p3-04-v17 [es] | EMPTY while DE non-empty | DE: Lieber will ich noch unter verschlossnem Himmel in der Tonne sitzen, lieber ohne
ch-p3-04-v18 [fr] | EMPTY while DE non-empty | DE: Und oft gelüstete mich, sie mit zackichten Blitz-Golddrähten festzuheften, dass 
ch-p3-04-v32 [fr] | EMPTY while DE non-empty | DE: Oh Himmel über mir, du Reiner! Hoher! Das ist mir nun deine Reinheit, dass es ke
ch-p3-04-v32 [es] | EMPTY while DE non-empty | DE: Oh Himmel über mir, du Reiner! Hoher! Das ist mir nun deine Reinheit, dass es ke
ch-p3-04-v33 [es] | EMPTY while DE non-empty | DE: —dass du mir ein Tanzboden bist für göttliche Zufälle, dass du mir ein Göttertis
ch-p3-05-v07 [es] | EMPTY while DE non-empty | DE: Oh wann komme ich wieder in meine Heimat, wo ich mich nicht mehr bücken muss—nic
ch-p3-05-v16 [es] | EMPTY while DE non-empty | DE: Und jüngst riss ein Weib sein Kind an sich, das zu mir wollte: „nehmt die Kinder
ch-p3-05-v25 [fr] | EMPTY while DE non-empty | DE: Wohl lernen auch sie auf ihre Art Schreiten und Vorwärts-Schreiten: das heisse i
ch-p3-05-v32 [es] | EMPTY while DE non-empty | DE: „Ich diene, du dienst, wir dienen“ —so betet hier auch die Heuchelei der Herrsch
ch-p3-05-v37 [es] | EMPTY while DE non-empty | DE: Sie wollen im Grunde einfältiglich Eins am meisten: dass ihnen Niemand wehe thue
ch-p3-05-v47 [es] | EMPTY while DE non-empty | DE: Und wenn ich rufe: „Flucht allen feigen Teufeln in euch, die gerne winseln und H
ch-p3-05-v53 [fr] | EMPTY while DE non-empty | DE: Und wahrlich, mancher Zufall kam herrisch zu mir: aber herrischer noch sprach zu
ch-p3-05-v53 [es] | EMPTY while DE non-empty | DE: Und wahrlich, mancher Zufall kam herrisch zu mir: aber herrischer noch sprach zu
ch-p3-05-v54 [es] | EMPTY while DE non-empty | DE: —bittend, dass er Herberge finde und Herz bei mir, und schmeichlerisch zuredend:
ch-p3-05-v56 [fr] | EMPTY while DE non-empty | DE: Ihr werdet immer kleiner, ihr kleinen Leute! Ihr bröckelt ab, ihr Behaglichen! I
ch-p3-05-v56 [es] | EMPTY while DE non-empty | DE: Ihr werdet immer kleiner, ihr kleinen Leute! Ihr bröckelt ab, ihr Behaglichen! I
ch-p3-05-v64 [fr] | EMPTY while DE non-empty | DE: „Liebt immerhin euren Nächsten gleich euch,—aber seid mir erst solche, die sich 
ch-p3-05-v65 [es] | EMPTY while DE non-empty | DE: —mit der grossen Liebe lieben, mit der grossen Verachtung lieben!“ Also spricht 
ch-p3-05-v70 [fr] | EMPTY while DE non-empty | DE: Oh gesegnete Stunde des Blitzes! Oh Geheimniss vor Mittag!—Laufende Feuer will i
ch-p3-06-v14 [fr] | EMPTY while DE non-empty | DE: Sonderlich boshaft bin ich nämlich des Morgens: zur frühen Stunde, da der Eimer 
ch-p3-06-v14 [es] | EMPTY while DE non-empty | DE: Sonderlich boshaft bin ich nämlich des Morgens: zur frühen Stunde, da der Eimer 
ch-p3-06-v15 [fr] | EMPTY while DE non-empty | DE: Ungeduldig warte ich da, dass mir endlich der lichte Himmel aufgehe, der schneeb
ch-p3-06-v15 [es] | EMPTY while DE non-empty | DE: Ungeduldig warte ich da, dass mir endlich der lichte Himmel aufgehe, der schneeb
ch-p3-06-v19 [fr] | EMPTY while DE non-empty | DE: Ein gutes muthwilliges Ding ist auch das lange Schweigen und gleich dem Winter-H
ch-p3-06-v19 [es] | EMPTY while DE non-empty | DE: Ein gutes muthwilliges Ding ist auch das lange Schweigen und gleich dem Winter-H
ch-p3-06-v26 [es] | EMPTY while DE non-empty | DE: Sondern die Hellen, die Wackern, die Durchsichtigen—das sind mir die klügsten Sc
ch-p3-06-v27 [fr] | EMPTY while DE non-empty | DE: Du schneebärtiger schweigender Winter-Himmel, du rundäugichter Weisskopf über mi
ch-p3-06-v34 [fr] | EMPTY while DE non-empty | DE: Wie könnten sie mein Glück ertragen, wenn ich nicht Unfälle und Winter-Nöthe und
ch-p3-06-v35 [fr] | EMPTY while DE non-empty | DE: —wenn ich mich nicht selbst ihres Mitleids erbarmte—des Mitleids dieser Neidbold
ch-p3-07-v02 [fr] | EMPTY while DE non-empty | DE: „Oh Zarathustra, hier ist die grosse Stadt: hier hast du Nichts zu suchen und Al
ch-p3-07-v03 [fr] | EMPTY while DE non-empty | DE: Warum wolltest du durch diesen Schlamm waten? Habe doch Mitleiden mit deinem Fus
ch-p3-07-v05 [fr] | EMPTY while DE non-empty | DE: Hier verwesen alle grossen Gefühle: hier dürfen nur klapperdürre Gefühlchen klap
ch-p3-07-v06 [fr] | EMPTY while DE non-empty | DE: Riechst du nicht schon die Schlachthäuser und Garküchen des Geistes? Dampft nich
ch-p3-07-v08 [fr] | EMPTY while DE non-empty | DE: Hörst du nicht, wie der Geist hier zum Wortspiel wurde? Widriges Wort-Spülicht b
ch-p3-07-v11 [fr] | EMPTY while DE non-empty | DE: Alle Lüste und Laster sind hier zu Hause; aber es giebt hier auch Tugendhafte, e
ch-p3-07-v11 [es] | EMPTY while DE non-empty | DE: Alle Lüste und Laster sind hier zu Hause; aber es giebt hier auch Tugendhafte, e
ch-p3-07-v21 [fr] | EMPTY while DE non-empty | DE: Speie auf die Stadt der eingedrückten Seelen und schmalen Brüste, der spitzen Au
ch-p3-07-v21 [es] | EMPTY while DE non-empty | DE: Speie auf die Stadt der eingedrückten Seelen und schmalen Brüste, der spitzen Au
ch-p3-07-v22 [fr] | EMPTY while DE non-empty | DE: —auf die Stadt der Aufdringlinge, der Unverschämten, der Schreib- und Schreihäls
ch-p3-07-v22 [es] | EMPTY while DE non-empty | DE: —auf die Stadt der Aufdringlinge, der Unverschämten, der Schreib- und Schreihäls
ch-p3-07-v24 [fr] | EMPTY while DE non-empty | DE: —speie auf die grosse Stadt und kehre um!“—
ch-p3-07-v24 [es] | EMPTY while DE non-empty | DE: —speie auf die grosse Stadt und kehre um!“—
ch-p3-07-v33 [fr] | EMPTY while DE non-empty | DE: Was war es denn, was dich zuerst grunzen machte? Dass Niemand dir genug geschmei
ch-p3-07-v33 [es] | EMPTY while DE non-empty | DE: Was war es denn, was dich zuerst grunzen machte? Dass Niemand dir genug geschmei
ch-p3-08-v03 [es] | EMPTY while DE non-empty | DE: Noch jüngst sah ich sie in der Frühe auf tapferen Füssen hinauslaufen: aber ihre
ch-p3-08-v09 [es] | EMPTY while DE non-empty | DE: Wer meiner Art ist, dem werden auch die Erlebnisse meiner Art über den Weg laufe
ch-p3-08-v12 [es] | EMPTY while DE non-empty | DE: Könnten sie anders, so würden sie auch anders wollen. Halb- und Halbe verderben 
ch-p3-08-v21 [fr] | EMPTY while DE non-empty | DE: Ich höre und rieche es: es kam ihre Stunde für Jagd und Umzug, nicht zwar für ei
ch-p3-08-v21 [es] | EMPTY while DE non-empty | DE: Ich höre und rieche es: es kam ihre Stunde für Jagd und Umzug, nicht zwar für ei
ch-p3-08-v31 [es] | EMPTY while DE non-empty | DE: Fünf Worte von alten Sachen hörte ich gestern Nachts an der Garten-Mauer: die ka
ch-p3-08-v36 [es] | EMPTY while DE non-empty | DE: „Ja! Ja! Der Glaube macht ihn selig, der Glaube an ihn. Das ist so die Art alter
ch-p3-08-v43 [fr] | EMPTY while DE non-empty | DE: Das geschah, als das gottloseste Wort von einem Gotte selber ausgieng,—das Wort:
ch-p3-08-v43 [es] | EMPTY while DE non-empty | DE: Das geschah, als das gottloseste Wort von einem Gotte selber ausgieng,—das Wort:
ch-p3-08-v44 [fr] | EMPTY while DE non-empty | DE: —ein alter Grimm-Bart von Gott, ein eifersüchtiger vergass sich also:
ch-p3-08-v44 [es] | EMPTY while DE non-empty | DE: —ein alter Grimm-Bart von Gott, ein eifersüchtiger vergass sich also:
ch-p3-09-v02 [fr] | EMPTY while DE non-empty | DE: Nun drohe mir nur mit dem Finger, wie Mütter drohn, nein lächle mir zu, wie Mütt
ch-p3-09-v02 [es] | EMPTY while DE non-empty | DE: Nun drohe mir nur mit dem Finger, wie Mütter drohn, nein lächle mir zu, wie Mütt
ch-p3-09-v08 [es] | EMPTY while DE non-empty | DE: Hier kommen alle Dinge liebkosend zu deiner Rede und schmeicheln dir: denn sie w
ch-p3-09-v11 [fr] | EMPTY while DE non-empty | DE: —als du sprachst: mögen mich meine Thiere führen! Gefährlicher fand ich's unter 
ch-p3-09-v12 [fr] | EMPTY while DE non-empty | DE: Und weisst du noch, oh Zarathustra? Als du auf deiner Insel sassest, unter leere
ch-p3-09-v14 [fr] | EMPTY while DE non-empty | DE: Und weisst du noch, oh Zarathustra? Als deine stillste Stunde kam und dich von d
ch-p3-09-v14 [es] | EMPTY while DE non-empty | DE: Und weisst du noch, oh Zarathustra? Als deine stillste Stunde kam und dich von d
ch-p3-09-v15 [es] | EMPTY while DE non-empty | DE: —als sie dir all dein Warten und Schweigen leid machte und deinen demüthigen Mut
ch-p3-09-v36 [es] | EMPTY while DE non-empty | DE: Sonderlich Die, welche sich „die Guten“ heissen, fand ich als die giftigsten Fli
ch-p3-09-v38 [fr] | EMPTY while DE non-empty | DE: Mich selber verbergen und meinen Reichthum—das lernte ich da unten: denn jeden f
ch-p3-09-v38 [es] | EMPTY while DE non-empty | DE: Mich selber verbergen und meinen Reichthum—das lernte ich da unten: denn jeden f
ch-p3-10-v02 [es] | EMPTY while DE non-empty | DE: Oh dass zu früh mir die Morgenröthe kam: die glühte mich wach, die Eifersüchtige
ch-p3-10-v06 [fr] | EMPTY while DE non-empty | DE: Wie sicher schaute mein Traum auf diese endliche Welt, nicht neugierig, nicht al
ch-p3-10-v06 [es] | EMPTY while DE non-empty | DE: Wie sicher schaute mein Traum auf diese endliche Welt, nicht neugierig, nicht al
ch-p3-10-v07 [fr] | EMPTY while DE non-empty | DE: —als ob ein voller Apfel sich meiner Hand böte, ein reifer Goldapfel, mit kühl-s
ch-p3-10-v08 [es] | EMPTY while DE non-empty | DE: —als ob ein Baum mir winke, ein breitästiger, starkwilliger, gekrümmt zur Lehne 
ch-p3-10-v09 [fr] | EMPTY while DE non-empty | DE: —als ob zierliche Hände mir einen Schrein entgegentrügen,—einen Schrein offen fü
ch-p3-10-v10 [fr] | EMPTY while DE non-empty | DE: —nicht Räthsel genug, um Menschen-Liebe davon zu scheuchen, nicht Lösung genug, 
ch-p3-10-v10 [es] | EMPTY while DE non-empty | DE: —nicht Räthsel genug, um Menschen-Liebe davon zu scheuchen, nicht Lösung genug, 
ch-p3-10-v12 [es] | EMPTY while DE non-empty | DE: Und dass ich's ihm gleich thue am Tage und sein Bestes ihm nach- und ablerne: wi
ch-p3-10-v16 [es] | EMPTY while DE non-empty | DE: Wohlauf! Hier will ich die Wage halten über gewälztem Meere: und auch einen Zeug
ch-p3-10-v23 [fr] | EMPTY while DE non-empty | DE: Wollust: das grosse Gleichniss-Glück für höheres Glück und höchste Hoffnung. Vie
ch-p3-10-v24 [es] | EMPTY while DE non-empty | DE: —Vielem, das fremder sich ist, als Mann und Weib:—und wer begriff es ganz, wie f
ch-p3-10-v25 [es] | EMPTY while DE non-empty | DE: Wollust:—doch ich will Zäune um meine Gedanken haben und auch noch um meine Wort
ch-p3-10-v29 [es] | EMPTY while DE non-empty | DE: Herrschsucht: vor deren Blick der Mensch kriecht und duckt und fröhnt und niedri
ch-p3-10-v33 [fr] | EMPTY while DE non-empty | DE: Dass die einsame Höhe sich nicht ewig vereinsame und selbst begnüge; dass der Be
ch-p3-10-v35 [fr] | EMPTY while DE non-empty | DE: Und damals geschah es auch,—und wahrlich, es geschah zum ersten Male!—dass sein 
ch-p3-10-v35 [es] | EMPTY while DE non-empty | DE: Und damals geschah es auch,—und wahrlich, es geschah zum ersten Male!—dass sein 
ch-p3-10-v36 [fr] | EMPTY while DE non-empty | DE: —aus mächtiger Seele, zu welcher der hohe Leib gehört, der schöne, sieghafte, er
ch-p3-11-v19 [es] | EMPTY while DE non-empty | DE: Und wir—wir schleppen treulich, was man uns mitgiebt, auf harten Schultern und ü
ch-p3-11-v22 [fr] | EMPTY while DE non-empty | DE: Und wahrlich! Auch manches Eigene ist schwer zu tragen! Und viel Inwendiges am M
ch-p3-11-v22 [es] | EMPTY while DE non-empty | DE: Und wahrlich! Auch manches Eigene ist schwer zu tragen! Und viel Inwendiges am M
ch-p3-11-v29 [es] | EMPTY while DE non-empty | DE: Allgenügsamkeit, die Alles zu schmecken weiss: das ist nicht der beste Geschmack
ch-p3-11-v30 [es] | EMPTY while DE non-empty | DE: Alles aber kauen und verdauen—das ist eine rechte Schweine-Art! Immer I-a sagen—
ch-p3-11-v36 [en] | EMPTY while DE non-empty | DE: Unselig heisse ich auch Die, welche immer warten müssen,—die gehen mir wider den
ch-p3-11-v36 [fr] | EMPTY while DE non-empty | DE: Unselig heisse ich auch Die, welche immer warten müssen,—die gehen mir wider den
ch-p3-11-v36 [es] | EMPTY while DE non-empty | DE: Unselig heisse ich auch Die, welche immer warten müssen,—die gehen mir wider den
ch-p3-11-v40 [fr] | EMPTY while DE non-empty | DE: Mit Strickleitern lernte ich manches Fenster erklettern, mit hurtigen Beinen klo
ch-p3-11-v40 [es] | EMPTY while DE non-empty | DE: Mit Strickleitern lernte ich manches Fenster erklettern, mit hurtigen Beinen klo
ch-p3-11-v41 [es] | EMPTY while DE non-empty | DE: —gleich kleinen Flammen flackern auf hohen Masten: ein kleines Licht zwar, aber 
ch-p3-11-v44 [fr] | EMPTY while DE non-empty | DE: Ein Versuchen und Fragen war all mein Gehen:—und wahrlich, auch antworten muss m
ch-p3-12-v01 [fr] | EMPTY while DE non-empty | DE: Hier sitze ich und warte, alte zerbrochene Tafeln um mich und auch neue halb bes
ch-p3-12-v03 [es] | EMPTY while DE non-empty | DE: Dess warte ich nun: denn erst müssen mir die Zeichen kommen, dass es meine Stund
ch-p3-12-v14 [fr] | EMPTY while DE non-empty | DE: Und oft riss sie mich fort und hinauf und hinweg und mitten im Lachen: da flog i
ch-p3-12-v15 [fr] | EMPTY while DE non-empty | DE: —hinaus in ferne Zukünfte, die kein Traum noch sah, in heissere Süden, als je si
ch-p3-12-v15 [es] | EMPTY while DE non-empty | DE: —hinaus in ferne Zukünfte, die kein Traum noch sah, in heissere Süden, als je si
ch-p3-12-v16 [es] | EMPTY while DE non-empty | DE: —dass ich nämlich in Gleichnissen rede und gleich Dichtern hinke und stammle: un
ch-p3-12-v17 [fr] | EMPTY while DE non-empty | DE: Wo alles Werden mich Götter-Tanz und Götter-Muthwillen dünkte, und die Welt los-
ch-p3-12-v18 [fr] | EMPTY while DE non-empty | DE: —als ein ewiges Sich-fliehn und -Wiedersuchen vieler Götter, als das selige Sich
ch-p3-12-v18 [es] | EMPTY while DE non-empty | DE: —als ein ewiges Sich-fliehn und -Wiedersuchen vieler Götter, als das selige Sich
ch-p3-12-v19 [es] | EMPTY while DE non-empty | DE: Wo alle Zeit mich ein seliger Hohn auf Augenblicke dünkte, wo die Nothwendigkeit
ch-p3-12-v20 [fr] | EMPTY while DE non-empty | DE: Wo ich auch meinen alten Teufel und Erzfeind wiederfand, den Geist der Schwere u
ch-p3-12-v21 [fr] | EMPTY while DE non-empty | DE: Denn muss nicht dasein, über das getanzt, hinweggetanzt werde? Müssen nicht um d
ch-p3-12-v21 [es] | EMPTY while DE non-empty | DE: Denn muss nicht dasein, über das getanzt, hinweggetanzt werde? Müssen nicht um d
ch-p3-12-v22 [es] | EMPTY while DE non-empty | DE: Dort war's auch, wo ich das Wort „Übermensch“ vom Wege auflas, und dass der Mens
ch-p3-12-v23 [fr] | EMPTY while DE non-empty | DE: —dass der Mensch eine Brücke sei und kein Zweck: sich selig preisend ob seines M
ch-p3-12-v24 [fr] | EMPTY while DE non-empty | DE: —das Zarathustra-Wort vom grossen Mittage, und was sonst ich über den Menschen a
ch-p3-12-v25 [es] | EMPTY while DE non-empty | DE: Wahrlich, auch neue Sterne liess ich sie sehn sammt neuen Nächten; und über Wolk
ch-p3-12-v26 [fr] | EMPTY while DE non-empty | DE: Ich lehrte sie all mein Dichten und Trachten: in Eins zu dichten und zusammen zu
ch-p3-12-v28 [es] | EMPTY while DE non-empty | DE: Das Vergangne am Menschen zu erlösen und alles „Es war“ umzuschauen, bis der Wil
ch-p3-12-v29 [es] | EMPTY while DE non-empty | DE: —Diess hiess ich ihnen Erlösung, Diess allein lehrte ich sie Erlösung heissen. -
ch-p3-12-v31 [es] | EMPTY while DE non-empty | DE: Denn noch Ein Mal will ich zu den Menschen: unter ihnen will ich untergehen, ste
ch-p3-12-v32 [fr] | EMPTY while DE non-empty | DE: Der Sonne lernte ich Das ab, wenn sie hinabgeht, die Überreiche: Gold schüttet s
ch-p3-12-v32 [es] | EMPTY while DE non-empty | DE: Der Sonne lernte ich Das ab, wenn sie hinabgeht, die Überreiche: Gold schüttet s
ch-p3-12-v40 [es] | EMPTY while DE non-empty | DE: Wer sich nicht befehlen kann, der soll gehorchen. Und Mancher kann sich befehlen
ch-p3-12-v45 [es] | EMPTY while DE non-empty | DE: Genuss und Unschuld nämlich sind die schamhaftesten Dinge: Beide wollen nicht ge
ch-p3-12-v59 [es] | EMPTY while DE non-empty | DE: „Über dem Flusse ist Alles fest, alle die Werthe der Dinge, die Brücken, Begriff
ch-p3-12-v69 [es] | EMPTY while DE non-empty | DE: Oh meine Brüder, über Sterne und Zukunft ist bisher nur gewähnt, nicht gewusst w
ch-p3-12-v73 [es] | EMPTY while DE non-empty | DE: Oder war es eine Predigt des Todes, dass heilig hiess, was allem Leben widerspra
ch-p3-12-v74 [fr] | EMPTY while DE non-empty | DE: Diess ist mein Mitleid mit allem Vergangenen, dass ich sehe: es ist preisgegeben
ch-p3-12-v81 [fr] | EMPTY while DE non-empty | DE: Oh meine Brüder, ich weihe und weise euch zu einem neuen Adel: ihr sollt mir Zeu
ch-p3-12-v81 [es] | EMPTY while DE non-empty | DE: Oh meine Brüder, ich weihe und weise euch zu einem neuen Adel: ihr sollt mir Zeu
ch-p3-12-v85 [es] | EMPTY while DE non-empty | DE: Nicht, dass euer Geschlecht an Höfen höfisch wurde, und ihr lerntet, bunt, einem
ch-p3-12-v87 [es] | EMPTY while DE non-empty | DE: Nicht auch, dass ein Geist, den sie heilig nennen, eure Vorfahren in gelobte Län
ch-p3-12-v92 [es] | EMPTY while DE non-empty | DE: „Wozu leben? Alles ist eitel! Leben—das ist Stroh dreschen; Leben—das ist sich v
ch-p3-12-v109 [es] | EMPTY while DE non-empty | DE: „Und deine eigne Vernunft—die sollst du selber görgeln und würgen; denn es ist e
ch-p3-12-v113 [es] | EMPTY while DE non-empty | DE: Zerbrecht mir, oh meine Brüder, zerbrecht mir auch diese neue Tafel! Die Welt-Mü
ch-p3-12-v114 [fr] | EMPTY while DE non-empty | DE: Dass sie schlecht lernten und das Beste nicht, und Alles zu früh und Alles zu ge
ch-p3-12-v115 [es] | EMPTY while DE non-empty | DE: —ein verdorbener Magen ist nämlich ihr Geist: der räth zum Tode! Denn wahrlich, 
ch-p3-12-v134 [es] | EMPTY while DE non-empty | DE: Oh meine Brüder, es giebt Tafeln, welche die Ermüdung, und Tafeln, welche die Fa
ch-p3-12-v137 [fr] | EMPTY while DE non-empty | DE: Nun glüht die Sonne auf ihn, und die Hunde lecken nach seinem Schweisse: aber er
ch-p3-12-v137 [es] | EMPTY while DE non-empty | DE: Nun glüht die Sonne auf ihn, und die Hunde lecken nach seinem Schweisse: aber er
ch-p3-12-v141 [fr] | EMPTY while DE non-empty | DE: Nur, meine Brüder, dass ihr die Hunde von ihm scheucht, die faulen Schleicher, u
ch-p3-12-v141 [es] | EMPTY while DE non-empty | DE: Nur, meine Brüder, dass ihr die Hunde von ihm scheucht, die faulen Schleicher, u
ch-p3-12-v143 [es] | EMPTY while DE non-empty | DE: Ich schliesse Kreise um mich und heilige Grenzen; immer Wenigere steigen mit mir
ch-p3-12-v145 [es] | EMPTY while DE non-empty | DE: Schmarotzer: das ist ein Gewürm, ein kriechendes, geschmiegtes, das fett werden 
ch-p3-12-v148 [fr] | EMPTY while DE non-empty | DE: Was ist die höchste Art alles Seienden und was die geringste? Der Schmarotzer is
ch-p3-12-v148 [es] | EMPTY while DE non-empty | DE: Was ist die höchste Art alles Seienden und was die geringste? Der Schmarotzer is
ch-p3-12-v149 [fr] | EMPTY while DE non-empty | DE: Die Seele nämlich, welche die längste Leiter hat und am tiefsten hinunter kann: 
ch-p3-12-v149 [es] | EMPTY while DE non-empty | DE: Die Seele nämlich, welche die längste Leiter hat und am tiefsten hinunter kann: 
ch-p3-12-v151 [fr] | EMPTY while DE non-empty | DE: —die seiende Seele, welche in's Werden taucht; die habende, welche in's Wollen u
ch-p3-12-v151 [es] | EMPTY while DE non-empty | DE: —die seiende Seele, welche in's Werden taucht; die habende, welche in's Wollen u
ch-p3-12-v152 [fr] | EMPTY while DE non-empty | DE: —die sich selber fliehende, die sich selber im weitesten Kreise einholt; die wei
ch-p3-12-v152 [es] | EMPTY while DE non-empty | DE: —die sich selber fliehende, die sich selber im weitesten Kreise einholt; die wei
ch-p3-12-v161 [es] | EMPTY while DE non-empty | DE: Ich sollt nur Feinde haben, die zu hassen sind, aber nicht Feinde zum Verachten:
ch-p3-12-v162 [fr] | EMPTY while DE non-empty | DE: Dem würdigeren Feinde, oh meine Freunde, sollt ihr euch aufsparen: darum müsst i
ch-p3-12-v163 [es] | EMPTY while DE non-empty | DE: —sonderlich an vielem Gesindel, das euch in die Ohren lärmt von Volk und Völkern
ch-p3-12-v184 [es] | EMPTY while DE non-empty | DE: Nicht nur fort euch zu pflanzen, sondern hinauf—dazu, oh meine Brüder, helfe euc
ch-p3-12-v192 [fr] | EMPTY while DE non-empty | DE: —ein Versuch, oh meine Brüder! Und kein „Vertrag“! Zerbrecht, zerbrecht mir solc
ch-p3-12-v192 [es] | EMPTY while DE non-empty | DE: —ein Versuch, oh meine Brüder! Und kein „Vertrag“! Zerbrecht, zerbrecht mir solc
ch-p3-12-v193 [fr] | EMPTY while DE non-empty | DE: Oh meine Brüder! Bei Welchen liegt doch die grösste Gefahr aller Menschen-Zukunf
ch-p3-12-v193 [es] | EMPTY while DE non-empty | DE: Oh meine Brüder! Bei Welchen liegt doch die grösste Gefahr aller Menschen-Zukunf
ch-p3-12-v197 [es] | EMPTY while DE non-empty | DE: Oh meine Brüder, den Guten und Gerechten sah Einer einmal in's Herz, der da spra
ch-p3-12-v202 [fr] | EMPTY while DE non-empty | DE: Den Schaffenden hassen sie am meisten: den, der Tafeln bricht und alte Werthe, d
ch-p3-12-v202 [es] | EMPTY while DE non-empty | DE: Den Schaffenden hassen sie am meisten: den, der Tafeln bricht und alte Werthe, d
ch-p3-12-v203 [es] | EMPTY while DE non-empty | DE: Die Guten nämlich—die können nicht schaffen: die sind immer der Anfang vom Ende:
ch-p3-12-v217 [es] | EMPTY while DE non-empty | DE: „Warum so hart!—sprach zum Diamanten einst die Küchen-Kohle; sind wir denn nicht
ch-p3-12-v221 [fr] | EMPTY while DE non-empty | DE: Und wenn eure Härte nicht blitzen und scheiden und zerschneiden will: wie könnte
ch-p3-12-v221 [es] | EMPTY while DE non-empty | DE: Und wenn eure Härte nicht blitzen und scheiden und zerschneiden will: wie könnte
ch-p3-12-v224 [es] | EMPTY while DE non-empty | DE: Diese neue Tafel, oh meine Brüder, stelle ich über euch: werdet hart!—
ch-p3-12-v228 [fr] | EMPTY while DE non-empty | DE: Ach, wessen Auge dunkelte nicht in dieser trunkenen Dämmerung! Ach, wessen Fuss 
ch-p3-12-v228 [es] | EMPTY while DE non-empty | DE: Ach, wessen Auge dunkelte nicht in dieser trunkenen Dämmerung! Ach, wessen Fuss 
ch-p3-12-v229 [fr] | EMPTY while DE non-empty | DE: —Dass ich einst bereit und reif sei im grossen Mittage: bereit und reif gleich g
ch-p3-12-v229 [es] | EMPTY while DE non-empty | DE: —Dass ich einst bereit und reif sei im grossen Mittage: bereit und reif gleich g
ch-p3-12-v231 [fr] | EMPTY while DE non-empty | DE: —ein Stern bereit und reif in seinem Mittage, glühend, durchbohrt, selig vor ver
ch-p3-12-v231 [es] | EMPTY while DE non-empty | DE: —ein Stern bereit und reif in seinem Mittage, glühend, durchbohrt, selig vor ver
ch-p3-12-v232 [fr] | EMPTY while DE non-empty | DE: —eine Sonne selber und ein unerbittlicher Sonnen-Wille, zum Vernichten bereit im
ch-p3-12-v232 [es] | EMPTY while DE non-empty | DE: —eine Sonne selber und ein unerbittlicher Sonnen-Wille, zum Vernichten bereit im
ch-p3-13-v15 [es] | EMPTY while DE non-empty | DE: Kam wohl eine neue Erkenntniss zu dir, eine saure, schwere? Gleich angesäuertem 
ch-p3-13-v18 [es] | EMPTY while DE non-empty | DE: Zu jeder Seele gehört eine andre Welt; für jede Seele ist jede andre Seele eine 
ch-p3-13-v21 [es] | EMPTY while DE non-empty | DE: Sind nicht den Dingen Namen und Töne geschenkt, dass der Mensch sich an den Ding
ch-p3-13-v26 [es] | EMPTY while DE non-empty | DE: In jedem Nu beginnt das Sein; um jedes Hier rollt sich die Kugel Dort. Die Mitte
ch-p3-13-v27 [fr] | EMPTY while DE non-empty | DE: —Oh ihr Schalks-Narren und Drehorgeln! antwortete Zarathustra und lächelte wiede
ch-p3-13-v27 [es] | EMPTY while DE non-empty | DE: —Oh ihr Schalks-Narren und Drehorgeln! antwortete Zarathustra und lächelte wiede
ch-p3-13-v36 [fr] | EMPTY while DE non-empty | DE: Und ich selber—will ich damit des Menschen Ankläger sein? Ach, meine Thiere, Das
ch-p3-13-v38 [es] | EMPTY while DE non-empty | DE: Nicht an diess Marterholz war ich geheftet, dass ich weiss: der Mensch ist böse,
ch-p3-13-v44 [es] | EMPTY while DE non-empty | DE: Mein Seufzen sass auf allen Menschen-Gräbern und konnte nicht mehr aufstehn; mei
ch-p3-13-v46 [es] | EMPTY while DE non-empty | DE: Nackt hatte ich einst Beide gesehn, den grössten Menschen und den kleinsten Mens
ch-p3-13-v60 [fr] | EMPTY while DE non-empty | DE: Du lehrst, dass es ein grosses Jahr des Werdens giebt, ein Ungeheuer von grossem
ch-p3-13-v60 [es] | EMPTY while DE non-empty | DE: Du lehrst, dass es ein grosses Jahr des Werdens giebt, ein Ungeheuer von grossem
ch-p3-13-v63 [es] | EMPTY while DE non-empty | DE: Du würdest sprechen und ohne Zittern, vielmehr aufathmend vor Seligkeit: denn ei
ch-p3-13-v64 [es] | EMPTY while DE non-empty | DE: „Nun sterbe und schwinde ich, würdest du sprechen, und im Nu bin ich ein Nichts.
ch-p3-13-v66 [fr] | EMPTY while DE non-empty | DE: Ich komme wieder, mit dieser Sonne, mit dieser Erde, mit diesem Adler, mit diese
ch-p3-13-v67 [fr] | EMPTY while DE non-empty | DE: —ich komme ewig wieder zu diesem gleichen und selbigen Leben, im Grössten und au
ch-p3-13-v69 [es] | EMPTY while DE non-empty | DE: Ich sprach mein Wort, ich zerbreche an meinem Wort: so will es mein ewiges Loos 
ch-p3-14-v13 [fr] | EMPTY while DE non-empty | DE: Oh meine Seele, überreich und schwer stehst du nun da, ein Weinstock mit schwell
ch-p3-14-v13 [es] | EMPTY while DE non-empty | DE: Oh meine Seele, überreich und schwer stehst du nun da, ein Weinstock mit schwell
ch-p3-14-v16 [fr] | EMPTY while DE non-empty | DE: Oh meine Seele, ich gab dir Alles, und alle meine Hände sind an dich leer geword
ch-p3-14-v16 [es] | EMPTY while DE non-empty | DE: Oh meine Seele, ich gab dir Alles, und alle meine Hände sind an dich leer geword
ch-p3-14-v17 [es] | EMPTY while DE non-empty | DE: —hat der Geber nicht zu danken, dass der Nehmende nahm? Ist Schenken nicht eine 
ch-p3-14-v22 [fr] | EMPTY while DE non-empty | DE: „Ist alles Weinen nicht ein Klagen? Und alles Klagen nicht ein Anklagen?“ Also r
ch-p3-14-v22 [es] | EMPTY while DE non-empty | DE: „Ist alles Weinen nicht ein Klagen? Und alles Klagen nicht ein Anklagen?“ Also r
ch-p3-14-v23 [fr] | EMPTY while DE non-empty | DE: —in stürzende Thränen ausschütten all dein Leid über deine Fülle und über all di
ch-p3-14-v24 [es] | EMPTY while DE non-empty | DE: Aber willst du nicht weinen, nicht ausweinen deine purpurne Schwermuth, so wirst
ch-p3-14-v25 [fr] | EMPTY while DE non-empty | DE: —singen, mit brausendem Gesange, bis alle Meere still werden, dass sie deiner Se
ch-p3-14-v26 [fr] | EMPTY while DE non-empty | DE: —bis über stille sehnsüchtige Meere der Nachen schwebt, das güldene Wunder, um d
ch-p3-14-v26 [es] | EMPTY while DE non-empty | DE: —bis über stille sehnsüchtige Meere der Nachen schwebt, das güldene Wunder, um d
ch-p3-14-v27 [es] | EMPTY while DE non-empty | DE: —auch vieles grosse und kleine Gethier und Alles, was leichte wunderliche Füsse 
ch-p3-14-v28 [fr] | EMPTY while DE non-empty | DE: —hin zu dem güldenen Wunder, dem freiwilligen Nachen und zu seinem Herrn: das ab
ch-p3-14-v29 [fr] | EMPTY while DE non-empty | DE: —dein grosser Löser, oh meine Seele, der Namenlose—- dem zukünftige Gesänge erst
ch-p3-14-v29 [es] | EMPTY while DE non-empty | DE: —dein grosser Löser, oh meine Seele, der Namenlose—- dem zukünftige Gesänge erst
ch-p3-14-v30 [fr] | EMPTY while DE non-empty | DE: —schon glühst du und träumst, schon trinkst du durstig an allen tiefen klingende
ch-p3-15-v02 [fr] | EMPTY while DE non-empty | DE: —einen goldenen Kahn sah ich blinken auf mächtigen Gewässern, einen sinkenden, t
ch-p3-15-v09 [fr] | EMPTY while DE non-empty | DE: Ich fürchte dich Nahe, ich liebe dich Ferne; deine Flucht lockt mich, dein Suche
ch-p3-15-v18 [fr] | EMPTY while DE non-empty | DE: Jetzt neben mir! Und geschwind, du boshafte Springerin! Jetzt hinauf! Und hinübe
ch-p3-15-v22 [es] | EMPTY while DE non-empty | DE: Du bist so arg müde? Ich trage dich hin, lass nur die Arme sinken! Und hast du D
ch-p3-15-v34 [fr] | EMPTY while DE non-empty | DE: Es giebt eine alte schwere schwere Brumm-Glocke: die brummt Nachts bis zu deiner
ch-p3-15-v34 [es] | EMPTY while DE non-empty | DE: Es giebt eine alte schwere schwere Brumm-Glocke: die brummt Nachts bis zu deiner
ch-p3-15-v35 [fr] | EMPTY while DE non-empty | DE: —hörst du diese Glocke Mitternachts die Stunde schlagen, so denkst du zwischen E
ch-p3-15-v35 [es] | EMPTY while DE non-empty | DE: —hörst du diese Glocke Mitternachts die Stunde schlagen, so denkst du zwischen E
ch-p3-15-v41 [fr] | EMPTY while DE non-empty | DE: Eins! Oh Mensch! Gieb Acht! Zwei! Was spricht die tiefe Mitternacht? Drei! „Ich 
ch-p3-16-v01 [fr] | EMPTY while DE non-empty | DE: (Oder: das Ja- und Amen-Lied)
ch-p3-16-v01 [es] | EMPTY while DE non-empty | DE: (Oder: das Ja- und Amen-Lied)
ch-p3-16-v03 [fr] | EMPTY while DE non-empty | DE: zwischen Vergangenem und Zukünftigem als schwere Wolke wandelt,—schwülen Niederu
ch-p3-16-v04 [es] | EMPTY while DE non-empty | DE: zum Blitze bereit im dunklen Busen und zum erlösenden Lichtstrahle, schwanger vo
ch-p3-16-v05 [es] | EMPTY while DE non-empty | DE: —selig aber ist der also Schwangere! Und wahrlich, lange muss als schweres Wette
ch-p3-16-v10 [fr] | EMPTY while DE non-empty | DE: Wenn mein Hohn je vermoderte Worte zerblies, und ich wie ein Besen kam den Kreuz
ch-p3-16-v10 [es] | EMPTY while DE non-empty | DE: Wenn mein Hohn je vermoderte Worte zerblies, und ich wie ein Besen kam den Kreuz
ch-p3-16-v12 [es] | EMPTY while DE non-empty | DE: —denn selbst Kirchen und Gottes-Gräber liebe ich, wenn der Himmel erst reinen Au
ch-p3-16-v18 [fr] | EMPTY while DE non-empty | DE: Wenn ich je am Göttertisch der Erde mit Göttern Würfel spielte, dass die Erde be
ch-p3-16-v19 [es] | EMPTY while DE non-empty | DE: —denn ein Göttertisch ist die Erde, und zitternd von schöpferischen neuen Worten
ch-p3-16-v25 [fr] | EMPTY while DE non-empty | DE: Wenn ich selber ein Korn bin von jenem erlösenden Salze, welches macht, dass all
ch-p3-16-v25 [es] | EMPTY while DE non-empty | DE: Wenn ich selber ein Korn bin von jenem erlösenden Salze, welches macht, dass all
ch-p3-16-v26 [es] | EMPTY while DE non-empty | DE: —denn es giebt ein Salz, das Gutes mit Bösem bindet; und auch das Böseste ist zu
ch-p3-16-v31 [fr] | EMPTY while DE non-empty | DE: Wenn jene suchende Lust in mir ist, die nach Unentdecktem die Segel treibt, wenn
ch-p3-16-v31 [es] | EMPTY while DE non-empty | DE: Wenn jene suchende Lust in mir ist, die nach Unentdecktem die Segel treibt, wenn
ch-p3-16-v33 [es] | EMPTY while DE non-empty | DE: —das Grenzenlose braust um mich, weit hinaus glänzt mir Raum und Zeit, wohlan! w
ch-p3-16-v38 [fr] | EMPTY while DE non-empty | DE: Wenn meine Bosheit eine lachende Bosheit ist, heimisch unter Rosenhängen und Lil
ch-p3-16-v38 [es] | EMPTY while DE non-empty | DE: Wenn meine Bosheit eine lachende Bosheit ist, heimisch unter Rosenhängen und Lil
ch-p3-16-v40 [es] | EMPTY while DE non-empty | DE: Und wenn Das mein A und O ist, dass alles Schwere leicht, aller Leib Tänzer, all
ch-p3-16-v45 [fr] | EMPTY while DE non-empty | DE: Wenn ich spielend in tiefen Licht-Fernen schwamm, und meiner Freiheit Vogel-Weis
ch-p3-16-v45 [es] | EMPTY while DE non-empty | DE: Wenn ich spielend in tiefen Licht-Fernen schwamm, und meiner Freiheit Vogel-Weis
ch-p3-16-v46 [fr] | EMPTY while DE non-empty | DE: —so aber spricht Vogel-Weisheit: „Siehe, es giebt kein Oben, kein Unten! Wirf di
ch-p3-16-v51 [fr] | EMPTY while DE non-empty | DE: Ach, wo in der Welt geschahen grössere Thorheiten, als bei den Mitleidigen? Und 
ch-p3-16-v52 [en] | EMPTY while DE non-empty | DE: Zarathustra, Von den Mitleidigen
ch-p3-16-v52 [fr] | EMPTY while DE non-empty | DE: Zarathustra, Von den Mitleidigen
ch-p4-01-v03 [es] | EMPTY while DE non-empty | DE: Da giengen die Thiere wieder nachdenklich um ihn herum und stellten sich dann ab
ch-p4-01-v06 [fr] | EMPTY while DE non-empty | DE: Was opfern! Ich verschwende, was mir geschenkt wird, ich Verschwender mit tausen
ch-p4-01-v08 [fr] | EMPTY while DE non-empty | DE: —nach dem besten Köder, wie er Jägern und Fischfängern noththut. Denn wenn die W
ch-p4-01-v13 [es] | EMPTY while DE non-empty | DE: Bis sie, anbeissend an meine spitzen verborgenen Haken, hinauf müssen in meine H
ch-p4-01-v19 [fr] | EMPTY while DE non-empty | DE: Fieng wohl je ein Mensch auf hohen Bergen Fische? Und wenn es auch eine Thorheit
ch-p4-01-v19 [es] | EMPTY while DE non-empty | DE: Fieng wohl je ein Mensch auf hohen Bergen Fische? Und wenn es auch eine Thorheit
ch-p4-01-v23 [fr] | EMPTY while DE non-empty | DE: Wer muss einst kommen und darf nicht vorübergehn? Unser grosser Hazar, das ist u
ch-p4-01-v23 [es] | EMPTY while DE non-empty | DE: Wer muss einst kommen und darf nicht vorübergehn? Unser grosser Hazar, das ist u
ch-p4-01-v24 [es] | EMPTY while DE non-empty | DE: Wie ferne mag solches „Ferne“ sein? was geht's mich an! Aber darum steht es mir 
ch-p4-02-v06 [es] | EMPTY while DE non-empty | DE: Und kaum waren diese Worte gesprochen, da erscholl der Schrei abermals, und läng
ch-p4-02-v12 [es] | EMPTY while DE non-empty | DE: Aber wenn du auch vor mir tanzen wolltest und alle deine Seitensprünge springen:
ch-p4-02-v20 [es] | EMPTY while DE non-empty | DE: Er ist in meinem Bereiche: darin soll er mir nicht zu Schaden kommen! Und wahrli
ch-p4-02-v28 [en] | EMPTY while DE non-empty | DE: Also sprach Zarathustra.
ch-p4-02-v28 [fr] | EMPTY while DE non-empty | DE: Also sprach Zarathustra.
ch-p4-03-v05 [es] | EMPTY while DE non-empty | DE: Lieber, wahrlich, unter Einsiedlern und Ziegenhirten als mit unserm vergoldeten 
ch-p4-03-v12 [es] | EMPTY while DE non-empty | DE: Wir sind nicht die Ersten—und müssen es doch bedeuten: dieser Betrügerei sind wi
ch-p4-03-v13 [fr] | EMPTY while DE non-empty | DE: Dem Gesindel giengen wir aus dem Wege, allen diesen Schreihälsen und Schreib-Sch
ch-p4-03-v13 [es] | EMPTY while DE non-empty | DE: Dem Gesindel giengen wir aus dem Wege, allen diesen Schreihälsen und Schreib-Sch
ch-p4-03-v21 [fr] | EMPTY while DE non-empty | DE: Mit dem Schwerte dieses Wortes zerhaust du unsres Herzens dickste Finsterniss. D
ch-p4-03-v21 [es] | EMPTY while DE non-empty | DE: Mit dem Schwerte dieses Wortes zerhaust du unsres Herzens dickste Finsterniss. D
ch-p4-03-v22 [es] | EMPTY while DE non-empty | DE: —den Menschen, der höher ist als wir: ob wir gleich Könige sind. Ihm führen wir 
ch-p4-03-v24 [es] | EMPTY while DE non-empty | DE: Und wenn sie gar die letzten sind und mehr Vieh als Mensch: da steigt und steigt
ch-p4-03-v25 [fr] | EMPTY while DE non-empty | DE: Was hörte ich eben? antwortete Zarathustra; welche Weisheit bei Königen! Ich bin
ch-p4-03-v25 [es] | EMPTY while DE non-empty | DE: Was hörte ich eben? antwortete Zarathustra; welche Weisheit bei Königen! Ich bin
ch-p4-03-v32 [es] | EMPTY while DE non-empty | DE: Wir müssen ihn hören, ihn, der lehrt „ihr sollt den Frieden lieben als Mittel zu
ch-p4-03-v35 [es] | EMPTY while DE non-empty | DE: Wenn die Schwerter durcheinander liefen gleich rothgefleckten Schlangen, da wurd
ch-p4-04-v03 [fr] | EMPTY while DE non-empty | DE: Wie ein Wanderer, der von fernen Dingen träumt, unversehens auf einsamer Strasse
ch-p4-04-v12 [es] | EMPTY while DE non-empty | DE: Wohlan! Dort hinauf geht der Weg zu Zarathustra's Höhle: die ist nicht fern,—wil
ch-p4-04-v16 [es] | EMPTY while DE non-empty | DE: Oh Glück! Oh Wunder! Gelobt sei dieser Tag, der mich in diesen Sumpf lockte! Gel
ch-p4-04-v19 [fr] | EMPTY while DE non-empty | DE: Lieber Nichts wissen, als Vieles halb wissen! Lieber ein Narr sein auf eigne Fau
ch-p4-05-v05 [es] | EMPTY while DE non-empty | DE: Umsonst! Stich weiter, Grausamster Stachel! Nein, Kein Hund—dein Wild nur bin ic
ch-p4-05-v06 [en] | EMPTY while DE non-empty | DE: Wie? Lösegeld? Was willst du Lösegelds? Verlange Viel—das räth mein Stolz! Und r
ch-p4-05-v06 [es] | EMPTY while DE non-empty | DE: Wie? Lösegeld? Was willst du Lösegelds? Verlange Viel—das räth mein Stolz! Und r
ch-p4-05-v08 [es] | EMPTY while DE non-empty | DE: Haha! Und marterst mich, Narr, der du bist, Zermarterst meinen Stolz? Gieb Liebe
ch-p4-05-v09 [fr] | EMPTY while DE non-empty | DE: Davon! Da floh er selber, Mein letzter einziger Genoss, Mein grosser Feind, Mein
ch-p4-05-v09 [es] | EMPTY while DE non-empty | DE: Davon! Da floh er selber, Mein letzter einziger Genoss, Mein grosser Feind, Mein
ch-p4-05-v10 [en] | EMPTY while DE non-empty | DE: —Nein! Komm zurück, Mit allen deinen Martern! Zum Letzten aller Einsamen Oh komm
ch-p4-05-v18 [fr] | EMPTY while DE non-empty | DE: Du Pfau der Pfauen, du Meer der Eitelkeit, was spieltest du vor mir, du schlimme
ch-p4-05-v18 [es] | EMPTY while DE non-empty | DE: Du Pfau der Pfauen, du Meer der Eitelkeit, was spieltest du vor mir, du schlimme
ch-p4-05-v21 [fr] | EMPTY while DE non-empty | DE: Und gesteh es nur ein: es währte lange, oh Zarathustra, bis du hinter meine Kuns
ch-p4-05-v21 [es] | EMPTY while DE non-empty | DE: Und gesteh es nur ein: es währte lange, oh Zarathustra, bis du hinter meine Kuns
ch-p4-05-v27 [es] | EMPTY while DE non-empty | DE: Ich errathe dich wohl: du wurdest der Bezauberer Aller, aber gegen dich hast du 
ch-p4-05-v31 [es] | EMPTY while DE non-empty | DE: Einen grossen Menschen wollte ich vorstellen und überredete Viele: aber diese Lü
ch-p4-05-v36 [fr] | EMPTY while DE non-empty | DE: Aber sprich, was suchst du hier in meinen Wäldern und Felsen? Und wenn du mir di
ch-p4-05-v36 [es] | EMPTY while DE non-empty | DE: Aber sprich, was suchst du hier in meinen Wäldern und Felsen? Und wenn du mir di
ch-p4-05-v37 [es] | EMPTY while DE non-empty | DE: —wess versuchtest du mich?“—
ch-p4-05-v39 [es] | EMPTY while DE non-empty | DE: Oh Zarathustra, ich suche einen Ächten, Rechten, Einfachen, Eindeutigen, einen M
ch-p4-06-v01 [fr] | EMPTY while DE non-empty | DE: Nicht lange aber, nachdem Zarathustra sich von dem Zauberer losgemacht hatte, sa
ch-p4-06-v01 [es] | EMPTY while DE non-empty | DE: Nicht lange aber, nachdem Zarathustra sich von dem Zauberer losgemacht hatte, sa
ch-p4-06-v03 [es] | EMPTY while DE non-empty | DE: —irgend ein Hexenmeister mit Handauflegen, ein dunkler Wunderthäter von Gottes G
ch-p4-06-v08 [es] | EMPTY while DE non-empty | DE: Ich suchte den letzten frommen Menschen, einen Heiligen und Einsiedler, der alle
ch-p4-06-v19 [es] | EMPTY while DE non-empty | DE: Also sprach Zarathustra und durchbohrte mit seinen Blicken die Gedanken und Hint
ch-p4-06-v20 [fr] | EMPTY while DE non-empty | DE: „Wer ihn am meisten liebte und besass, der hat ihn nun am meisten auch verloren 
ch-p4-06-v20 [es] | EMPTY while DE non-empty | DE: „Wer ihn am meisten liebte und besass, der hat ihn nun am meisten auch verloren 
ch-p4-06-v22 [es] | EMPTY while DE non-empty | DE: „Du dientest ihm bis zuletzt, fragte Zarathustra nachdenklich, nach einem tiefen
ch-p4-06-v23 [es] | EMPTY while DE non-empty | DE: —dass er es sah, wie der Mensch am Kreuze hieng, und es nicht ertrug, dass die L
ch-p4-06-v28 [es] | EMPTY while DE non-empty | DE: Meine Liebe diente ihm lange Jahre, mein Wille gierig allem seinen Willen nach. 
ch-p4-06-v30 [es] | EMPTY while DE non-empty | DE: Wer ihn als einen Gott der Liebe preist, denkt nicht hoch genug von der Liebe se
ch-p4-06-v33 [es] | EMPTY while DE non-empty | DE: Da sass er, welk, in seinem Ofenwinkel, härmte sich ob seiner schwachen Beine, w
ch-p4-06-v45 [es] | EMPTY while DE non-empty | DE: Lass mich deinen Gast sein, oh Zarathustra, für eine einzige Nacht! Nirgends auf
ch-p4-07-v09 [es] | EMPTY while DE non-empty | DE: „Ich erkenne dich wohl, sprach er mit einer erzenen Stimme: du bist der Mörder G
ch-p4-07-v11 [fr] | EMPTY while DE non-empty | DE: Also sprach Zarathustra und wollte davon; aber der Unaussprechliche fasste nach 
ch-p4-07-v11 [es] | EMPTY while DE non-empty | DE: Also sprach Zarathustra und wollte davon; aber der Unaussprechliche fasste nach 
ch-p4-07-v15 [fr] | EMPTY while DE non-empty | DE: Sie verfolgen mich: nun bist du meine letzte Zuflucht. Nicht mit ihrem Hasse, ni
ch-p4-07-v16 [fr] | EMPTY while DE non-empty | DE: War nicht aller Erfolg bisher bei den Gut-Verfolgten? Und wer gut verfolgt, lern
ch-p4-07-v17 [es] | EMPTY while DE non-empty | DE: —ihr Mitleid ist's, vor dem ich flüchte und dir zuflüchte. Oh Zarathustra, schüt
ch-p4-07-v18 [es] | EMPTY while DE non-empty | DE: —du erriethest, wie Dem zu Muthe ist, welcher ihn tödtete. Bleib! Und willst du 
ch-p4-07-v19 [fr] | EMPTY while DE non-empty | DE: Zürnst du mir, dass ich zu lange schon rede-rade-breche? Dass ich schon dir rath
ch-p4-07-v21 [es] | EMPTY while DE non-empty | DE: Dass du aber an mir vorübergiengst, schweigend; dass du erröthetest, ich sah es 
ch-p4-07-v24 [fr] | EMPTY while DE non-empty | DE: Mit Noth kam ich heraus aus dem Gedräng der Mitleidigen,—dass ich den Einzigen f
ch-p4-07-v34 [fr] | EMPTY while DE non-empty | DE: Du schämst dich an der Scham des grossen Leidenden; und wahrlich, wenn du sprich
ch-p4-07-v36 [es] | EMPTY while DE non-empty | DE: Du selber aber—warne dich selber auch vor deinem Mitleiden! Denn Viele sind zu d
ch-p4-08-v08 [es] | EMPTY while DE non-empty | DE: So wir nicht umkehren und werden wie die Kühe, so kommen wir nicht in das Himmel
ch-p4-08-v09 [fr] | EMPTY while DE non-empty | DE: Und wahrlich, wenn der Mensch auch die ganze Welt gewönne und lernte das Eine ni
ch-p4-08-v09 [es] | EMPTY while DE non-empty | DE: Und wahrlich, wenn der Mensch auch die ganze Welt gewönne und lernte das Eine ni
ch-p4-08-v14 [fr] | EMPTY while DE non-empty | DE: „Sprich nicht von mir, du Wunderlicher! Lieblicher! sagte Zarathustra und wehrte
ch-p4-08-v14 [es] | EMPTY while DE non-empty | DE: „Sprich nicht von mir, du Wunderlicher! Lieblicher! sagte Zarathustra und wehrte
ch-p4-08-v24 [fr] | EMPTY while DE non-empty | DE: „Was versuchst du mich? antwortete dieser. Du weisst es selber besser noch als i
ch-p4-08-v24 [es] | EMPTY while DE non-empty | DE: „Was versuchst du mich? antwortete dieser. Du weisst es selber besser noch als i
ch-p4-08-v25 [fr] | EMPTY while DE non-empty | DE: —vor den Sträflingen des Reichthums, welche sich ihren Vortheil aus jedem Kehric
ch-p4-08-v26 [es] | EMPTY while DE non-empty | DE: —vor diesem vergüldeten verfälschten Pöbel, dessen Väter Langfinger oder Aasvöge
ch-p4-08-v32 [fr] | EMPTY while DE non-empty | DE: „Du erriethst mich gut, antwortete der freiwillige Bettler, mit erleichtertem He
ch-p4-08-v35 [es] | EMPTY while DE non-empty | DE: „- Wohlan! sagte Zarathustra: du solltest auch meine Thiere sehn, meinen Adler u
ch-p4-08-v36 [fr] | EMPTY while DE non-empty | DE: Siehe, dorthin führt der Weg zu meiner Höhle: sei diese Nacht ihr Gast. Und rede
ch-p4-08-v37 [es] | EMPTY while DE non-empty | DE: —bis ich selber heimkomme. Denn jetzt ruft ein Nothschrei Mich eilig weg von dir
ch-p4-09-v20 [es] | EMPTY while DE non-empty | DE: Ach, wohin kam mir alles Gute und alle Scham und aller Glaube an die Guten! Ach,
ch-p4-10-v05 [es] | EMPTY while DE non-empty | DE: Kein Auge drückt er mir zu, die Seele lässt er mir wach. Leicht ist er, wahrlich
ch-p4-10-v06 [fr] | EMPTY while DE non-empty | DE: Er überredet mich, ich weiss nicht wie?, er betupft mich innewendig mit schmeich
ch-p4-10-v14 [fr] | EMPTY while DE non-empty | DE: Singe nicht, du Gras-Geflügel, oh meine Seele! Flüstere nicht einmal! Sieh doch 
ch-p4-10-v14 [es] | EMPTY while DE non-empty | DE: Singe nicht, du Gras-Geflügel, oh meine Seele! Flüstere nicht einmal! Sieh doch 
ch-p4-10-v15 [es] | EMPTY while DE non-empty | DE: —einen alten braunen Tropfen goldenen Glücks, goldenen Weins? Es huscht über ihn
ch-p4-10-v22 [es] | EMPTY while DE non-empty | DE: Auf! sprach er zu sich selber, du Schläfer! Du Mittagsschläfer! Wohlan, wohlauf,
ch-p4-10-v24 [es] | EMPTY while DE non-empty | DE: (Aber da schlief er schon von Neuem ein, und seine Seele sprach gegen ihn und we
ch-p4-10-v27 [es] | EMPTY while DE non-empty | DE: „Oh Himmel über mir, sprach er seufzend und setzte sich aufrecht, du schaust mir
ch-p4-10-v28 [fr] | EMPTY while DE non-empty | DE: Wann trinkst du diesen Tropfen Thau's, der auf alle Erden-Dinge niederfiel,—wann
ch-p4-11-v04 [fr] | EMPTY while DE non-empty | DE: „Ihr Verzweifelnden! Ihr Wunderlichen! Ich hörte also euren Nothschrei? Und nun 
ch-p4-11-v05 [fr] | EMPTY while DE non-empty | DE: —in meiner eignen Höhle sitzt er, der höhere Mensch! Aber was wundere ich mich! 
ch-p4-11-v05 [es] | EMPTY while DE non-empty | DE: —in meiner eignen Höhle sitzt er, der höhere Mensch! Aber was wundere ich mich! 
ch-p4-11-v08 [fr] | EMPTY while DE non-empty | DE: Vergebt mir doch, ihr Verzweifelnden, dass ich vor euch mit solch kleinen Worten
ch-p4-11-v08 [es] | EMPTY while DE non-empty | DE: Vergebt mir doch, ihr Verzweifelnden, dass ich vor euch mit solch kleinen Worten
ch-p4-11-v15 [fr] | EMPTY while DE non-empty | DE: „Daran, oh Zarathustra, wie du uns Hand und Gruss botest, erkennen wir dich als 
ch-p4-11-v20 [fr] | EMPTY while DE non-empty | DE: Der Pinie vergleiche ich, wer gleich dir, oh Zarathustra, aufwächst: lang, schwe
ch-p4-11-v21 [fr] | EMPTY while DE non-empty | DE: —zuletzt aber hinausgreifend mit starken grünen Ästen nach seiner Herrschaft, st
ch-p4-11-v21 [es] | EMPTY while DE non-empty | DE: —zuletzt aber hinausgreifend mit starken grünen Ästen nach seiner Herrschaft, st
ch-p4-11-v27 [es] | EMPTY while DE non-empty | DE: „Warum kommt er nicht, der sich so lange ankündigte? also fragen Viele; verschla
ch-p4-11-v30 [fr] | EMPTY while DE non-empty | DE: Und dass wir Verzweifelnde jetzt in deine Höhle kamen und schon nicht mehr verzw
ch-p4-11-v30 [es] | EMPTY while DE non-empty | DE: Und dass wir Verzweifelnde jetzt in deine Höhle kamen und schon nicht mehr verzw
ch-p4-11-v31 [fr] | EMPTY while DE non-empty | DE: —denn er selber ist zu dir unterwegs, der letzte Rest Gottes unter Menschen, das
ch-p4-11-v35 [fr] | EMPTY while DE non-empty | DE: („Deutsch und deutlich? Dass Gott erbarm! sagte hier der König zur Linken, bei S
ch-p4-11-v35 [es] | EMPTY while DE non-empty | DE: („Deutsch und deutlich? Dass Gott erbarm! sagte hier der König zur Linken, bei S
ch-p4-11-v43 [fr] | EMPTY while DE non-empty | DE: Eure Schultern drückt manche Last, manche Erinnerung; manch schlimmer Zwerg hock
ch-p4-11-v47 [fr] | EMPTY while DE non-empty | DE: Nicht auf euch warte ich hier in diesen Bergen, nicht mit euch darf ich zum letz
ch-p4-11-v47 [es] | EMPTY while DE non-empty | DE: Nicht auf euch warte ich hier in diesen Bergen, nicht mit euch darf ich zum letz
ch-p4-11-v49 [fr] | EMPTY while DE non-empty | DE: —Nein! Nein! Drei Mal Nein! Auf Andere warte ich hier in diesen Bergen und will 
ch-p4-11-v49 [es] | EMPTY while DE non-empty | DE: —Nein! Nein! Drei Mal Nein! Auf Andere warte ich hier in diesen Bergen und will 
ch-p4-11-v52 [es] | EMPTY while DE non-empty | DE: Sprecht mir doch von meinen Gärten, von meinen glückseligen Inseln, von meiner n
ch-p4-11-v53 [fr] | EMPTY while DE non-empty | DE: Diess Gastgeschenk erbitte ich mir von eurer Liebe, dass ihr mir von meinen Kind
ch-p4-12-v15 [fr] | EMPTY while DE non-empty | DE: „Sei guter Dinge, antwortete ihm Zarathustra, wie ich es bin. Bleibe bei deiner 
ch-p4-12-v16 [es] | EMPTY while DE non-empty | DE: Ich bin ein Gesetz nur für die Meinen, ich bin kein Gesetz für Alle. Wer aber zu
ch-p4-13-v12 [es] | EMPTY while DE non-empty | DE: Der Übermensch liegt mir am Herzen, der ist mein Erstes und Einziges,—und nicht 
ch-p4-13-v25 [es] | EMPTY while DE non-empty | DE: „Der Mensch ist böse“ —so sprachen mir zum Troste alle Weisesten. Ach, wenn es h
ch-p4-13-v27 [es] | EMPTY while DE non-empty | DE: Das mochte gut sein für jenen Prediger der kleinen Leute, dass er litt und trug 
ch-p4-13-v31 [fr] | EMPTY while DE non-empty | DE: Nein! Nein! Drei Mal Nein! Immer Mehr, immer Bessere eurer Art sollen zu Grunde 
ch-p4-13-v31 [es] | EMPTY while DE non-empty | DE: Nein! Nein! Drei Mal Nein! Immer Mehr, immer Bessere eurer Art sollen zu Grunde 
ch-p4-13-v34 [fr] | EMPTY while DE non-empty | DE: Ihr leidet mir noch nicht genug! Denn ihr leidet an euch, ihr littet noch nicht 
ch-p4-13-v34 [es] | EMPTY while DE non-empty | DE: Ihr leidet mir noch nicht genug! Denn ihr leidet an euch, ihr littet noch nicht 
ch-p4-13-v38 [es] | EMPTY while DE non-empty | DE: Wollt Nichts über euer Vermögen: es giebt eine schlimme Falschheit bei Solchen, 
ch-p4-13-v39 [fr] | EMPTY while DE non-empty | DE: Sonderlich, wenn sie grosse Dinge wollen! Denn sie wecken Misstrauen gegen gross
ch-p4-13-v84 [es] | EMPTY while DE non-empty | DE: Der—liebte nicht genug: sonst hätte er auch uns geliebt, die Lachenden! Aber er 
ch-p4-13-v95 [fr] | EMPTY while DE non-empty | DE: Zarathustra der Tänzer, Zarathustra der Leichte, der mit den Flügeln winkt, ein 
ch-p4-13-v95 [es] | EMPTY while DE non-empty | DE: Zarathustra der Tänzer, Zarathustra der Leichte, der mit den Flügeln winkt, ein 
ch-p4-13-v99 [fr] | EMPTY while DE non-empty | DE: Besser aber noch närrisch sein vor Glücke als närrisch vor Unglücke, besser plum
ch-p4-13-v99 [es] | EMPTY while DE non-empty | DE: Besser aber noch närrisch sein vor Glücke als närrisch vor Unglücke, besser plum
ch-p4-13-v102 [es] | EMPTY while DE non-empty | DE: Dem Winde thut mir gleich, wenn er aus seinen Berghöhlen stürzt: nach seiner eig
ch-p4-13-v103 [fr] | EMPTY while DE non-empty | DE: Der den Eseln Flügel giebt, der Löwinnen melkt, gelobt sei dieser gute unbändige
ch-p4-14-v06 [fr] | EMPTY while DE non-empty | DE: Und schon, ihr höheren Menschen—dass ich euch mit diesem Lob- und Schmeichel-Nam
ch-p4-14-v06 [es] | EMPTY while DE non-empty | DE: Und schon, ihr höheren Menschen—dass ich euch mit diesem Lob- und Schmeichel-Nam
ch-p4-14-v08 [fr] | EMPTY while DE non-empty | DE: Euch Allen, welche Ehren ihr euch mit Worten geben mögt, ob ihr euch „die freien
ch-p4-14-v08 [es] | EMPTY while DE non-empty | DE: Euch Allen, welche Ehren ihr euch mit Worten geben mögt, ob ihr euch „die freien
ch-p4-14-v10 [fr] | EMPTY while DE non-empty | DE: Ich kenne euch, ihr höheren Menschen, ich kenne ihn,—ich kenne auch diesen Unhol
ch-p4-14-v10 [es] | EMPTY while DE non-empty | DE: Ich kenne euch, ihr höheren Menschen, ich kenne ihn,—ich kenne auch diesen Unhol
ch-p4-14-v11 [es] | EMPTY while DE non-empty | DE: —gleich einem neuen wunderlichen Mummenschanze, in dem sich mein böser Geist, de
ch-p4-14-v12 [fr] | EMPTY while DE non-empty | DE: Aber schon fällt der mich an und zwingt mich, dieser Geist der Schwermuth, diese
ch-p4-14-v13 [es] | EMPTY while DE non-empty | DE: —macht nur die Augen auf!—es gelüstet ihn, nackt zu kommen, ob männlich, ob weib
ch-p4-14-v20 [en] | EMPTY while DE non-empty | DE: Also Adlerhaft, pantherhaft Sind des Dichters Sehnsüchte, Sind deine Sehnsüchte 
ch-p4-15-v03 [fr] | EMPTY while DE non-empty | DE: Wehe allen freien Geistern, welche nicht vor solchen Zauberern auf der Hut sind!
ch-p4-15-v03 [es] | EMPTY while DE non-empty | DE: Wehe allen freien Geistern, welche nicht vor solchen Zauberern auf der Hut sind!
ch-p4-15-v11 [fr] | EMPTY while DE non-empty | DE: Wir suchen Verschiednes auch hier oben, ihr und ich. Ich nämlich suche mehr Sich
ch-p4-15-v11 [es] | EMPTY while DE non-empty | DE: Wir suchen Verschiednes auch hier oben, ihr und ich. Ich nämlich suche mehr Sich
ch-p4-15-v12 [fr] | EMPTY while DE non-empty | DE: —heute, wo Alles wackelt, wo alle Erde bebt. Ihr aber, wenn ich eure Augen sehe,
ch-p4-15-v12 [es] | EMPTY while DE non-empty | DE: —heute, wo Alles wackelt, wo alle Erde bebt. Ihr aber, wenn ich eure Augen sehe,
ch-p4-15-v14 [fr] | EMPTY while DE non-empty | DE: —euch gelüstet nach dem schlimmsten gefährlichsten Leben, das mir am meisten Fur
ch-p4-15-v14 [es] | EMPTY while DE non-empty | DE: —euch gelüstet nach dem schlimmsten gefährlichsten Leben, das mir am meisten Fur
ch-p4-15-v16 [es] | EMPTY while DE non-empty | DE: Furcht nämlich—das ist des Menschen Erb- und Grundgefühl; aus der Furcht erklärt
ch-p4-15-v17 [es] | EMPTY while DE non-empty | DE: Die Furcht nämlich vor wildem Gethier—die wurde dem Menschen am längsten angezüc
ch-p4-15-v25 [fr] | EMPTY while DE non-empty | DE: Sonderlich nämlich, wenn er sich nackend zeigt. Aber was kann ich für seine Tück
ch-p4-16-v02 [fr] | EMPTY while DE non-empty | DE: Schon gab uns jener alte Zauberer von seinem Schlimmsten zum Besten, und siehe d
ch-p4-16-v03 [fr] | EMPTY while DE non-empty | DE: Diese Könige mögen wohl vor uns noch gute Miene machen: das lernten Die nämlich 
ch-p4-16-v03 [es] | EMPTY while DE non-empty | DE: Diese Könige mögen wohl vor uns noch gute Miene machen: das lernten Die nämlich 
ch-p4-16-v09 [es] | EMPTY while DE non-empty | DE: Es sei denn,—es sei denn—, oh vergieb eine alte Erinnerung! Vergieb mir ein alte
ch-p4-16-v12 [fr] | EMPTY while DE non-empty | DE: Ihr glaubt es nicht, wie artig sie dasassen, wenn sie nicht tanzten, tief, aber 
ch-p4-16-v12 [es] | EMPTY while DE non-empty | DE: Ihr glaubt es nicht, wie artig sie dasassen, wenn sie nicht tanzten, tief, aber 
ch-p4-16-v21 [en] | EMPTY while DE non-empty | DE: Diese schönste Luft trinkend, Mit Nüstern geschwellt gleich Bechern, Ohne Zukunf
ch-p4-17-v21 [es] | EMPTY while DE non-empty | DE: Amen! Und Lob und Ehre und Weisheit und Dank und Preis und Stärke sei unserm Got
ch-p4-18-v01 [en] | EMPTY while DE non-empty | DE: An dieser Stelle der Litanei aber konnte Zarathustra sich nicht länger bemeister
ch-p4-18-v01 [fr] | EMPTY while DE non-empty | DE: An dieser Stelle der Litanei aber konnte Zarathustra sich nicht länger bemeister
ch-p4-18-v01 [es] | EMPTY while DE non-empty | DE: An dieser Stelle der Litanei aber konnte Zarathustra sich nicht länger bemeister
ch-p4-18-v03 [es] | EMPTY while DE non-empty | DE: Jeder würde urtheilen, ihr wäret mit eurem neuen Glauben die ärgsten Gottesläste
ch-p4-18-v08 [es] | EMPTY while DE non-empty | DE: Mein altes Herz springt und hüpft darob, dass es auf Erden noch Etwas anzubeten 
ch-p4-18-v32 [fr] | EMPTY while DE non-empty | DE: „Oh ihr Schalks-Narren allesammt, ihr Possenreisser! Was verstellt und versteckt
ch-p4-18-v32 [es] | EMPTY while DE non-empty | DE: „Oh ihr Schalks-Narren allesammt, ihr Possenreisser! Was verstellt und versteckt
ch-p4-18-v38 [fr] | EMPTY while DE non-empty | DE: Und noch einmal hob Zarathustra an zu reden. „Oh meine neuen Freunde, sprach er,
ch-p4-18-v38 [es] | EMPTY while DE non-empty | DE: Und noch einmal hob Zarathustra an zu reden. „Oh meine neuen Freunde, sprach er,
ch-p4-18-v39 [fr] | EMPTY while DE non-empty | DE: —seit ihr wieder fröhlich wurdet! Ihr seid wahrlich Alle aufgeblüht: mich dünkt,
ch-p4-18-v39 [es] | EMPTY while DE non-empty | DE: —seit ihr wieder fröhlich wurdet! Ihr seid wahrlich Alle aufgeblüht: mich dünkt,
ch-p4-19-v04 [es] | EMPTY while DE non-empty | DE: Und dass ich so viel bezeuge, ist mir noch nicht genug. Es lohnt sich auf der Er
ch-p4-19-v05 [es] | EMPTY while DE non-empty | DE: „War Das—das Leben?“ will ich zum Tode sprechen. „Wohlan! Noch Ein Mal!“
ch-p4-19-v08 [fr] | EMPTY while DE non-empty | DE: Zarathustra aber, als sich diess mit dem hässlichsten Menschen zutrug, stand da,
ch-p4-19-v08 [es] | EMPTY while DE non-empty | DE: Zarathustra aber, als sich diess mit dem hässlichsten Menschen zutrug, stand da,
ch-p4-19-v12 [fr] | EMPTY while DE non-empty | DE: Ihr höheren Menschen, es geht gen Mitternacht: da will ich euch Etwas in die Ohr
ch-p4-19-v12 [es] | EMPTY while DE non-empty | DE: Ihr höheren Menschen, es geht gen Mitternacht: da will ich euch Etwas in die Ohr
ch-p4-19-v13 [fr] | EMPTY while DE non-empty | DE: —so heimlich, so schrecklich, so herzlich, wie jene Mitternachts-Glocke zu mir e
ch-p4-19-v15 [fr] | EMPTY while DE non-empty | DE: Still! Still! Da hört sich Manches, das am Tage nicht laut werden darf; nun aber
ch-p4-19-v15 [es] | EMPTY while DE non-empty | DE: Still! Still! Da hört sich Manches, das am Tage nicht laut werden darf; nun aber
ch-p4-19-v20 [fr] | EMPTY while DE non-empty | DE: Nun starb ich schon. Es ist dahin. Spinne, was spinnst du um mich? Willst du Blu
ch-p4-19-v20 [es] | EMPTY while DE non-empty | DE: Nun starb ich schon. Es ist dahin. Spinne, was spinnst du um mich? Willst du Blu
ch-p4-19-v21 [fr] | EMPTY while DE non-empty | DE: —die Stunde, wo mich fröstelt und friert, die fragt und fragt und fragt: „wer ha
ch-p4-19-v23 [fr] | EMPTY while DE non-empty | DE: —die Stunde naht: oh Mensch, du höherer Mensch, gieb Acht! diese Rede ist für fe
ch-p4-19-v27 [es] | EMPTY while DE non-empty | DE: Ihr flogt nicht hoch genug: nun stammeln die Gräber „erlöst doch die Todten! War
ch-p4-19-v28 [fr] | EMPTY while DE non-empty | DE: Ihr höheren Menschen, erlöst doch die Gräber, weckt die Leichname auf! Ach, was 
ch-p4-19-v31 [fr] | EMPTY while DE non-empty | DE: Du alte Glocke, du süsse Leier! Jeder Schmerz riss dir in's Herz, Vaterschmerz, 
ch-p4-19-v31 [es] | EMPTY while DE non-empty | DE: Du alte Glocke, du süsse Leier! Jeder Schmerz riss dir in's Herz, Vaterschmerz, 
ch-p4-19-v32 [fr] | EMPTY while DE non-empty | DE: —reif gleich goldenem Herbste und Nachmittage, gleich meinem Einsiedlerherzen - 
ch-p4-19-v32 [es] | EMPTY while DE non-empty | DE: —reif gleich goldenem Herbste und Nachmittage, gleich meinem Einsiedlerherzen - 
ch-p4-19-v34 [fr] | EMPTY while DE non-empty | DE: —ein Duft und Geruch der Ewigkeit, ein rosenseliger, brauner Gold-Wein-Geruch vo
ch-p4-19-v34 [es] | EMPTY while DE non-empty | DE: —ein Duft und Geruch der Ewigkeit, ein rosenseliger, brauner Gold-Wein-Geruch vo
ch-p4-19-v40 [fr] | EMPTY while DE non-empty | DE: Oh Welt, du willst mich? Bin ich dir weltlich? Bin ich dir geistlich? Bin ich di
ch-p4-19-v40 [es] | EMPTY while DE non-empty | DE: Oh Welt, du willst mich? Bin ich dir weltlich? Bin ich dir geistlich? Bin ich di
ch-p4-19-v41 [fr] | EMPTY while DE non-empty | DE: —habt klügere Hände, greift nach tieferem Glücke, nach tieferem Unglücke, greift
ch-p4-19-v43 [fr] | EMPTY while DE non-empty | DE: Gottes Weh ist tiefer, du wunderliche Welt! Greife nach Gottes Weh, nicht nach m
ch-p4-19-v45 [fr] | EMPTY while DE non-empty | DE: Dahin! Dahin! Oh Jugend! Oh Mittag! Oh Nachmittag! Nun kam Abend und Nacht und M
ch-p4-19-v50 [fr] | EMPTY while DE non-empty | DE: „Was vollkommen ward, alles Reife—will sterben!“ so redest du. Gesegnet, gesegne
ch-p4-19-v50 [es] | EMPTY while DE non-empty | DE: „Was vollkommen ward, alles Reife—will sterben!“ so redest du. Gesegnet, gesegne
ch-p4-19-v51 [es] | EMPTY while DE non-empty | DE: Weh spricht: „Vergeh! Weg, du Wehe!“ Aber Alles, was leidet, will leben, dass es
ch-p4-19-v56 [es] | EMPTY while DE non-empty | DE: Ein Tropfen Thau's? Ein Dunst und Duft der Ewigkeit? Hört ihr's nicht? Riecht ih
ch-p4-19-v57 [fr] | EMPTY while DE non-empty | DE: Schmerz ist auch eine Lust, Fluch ist auch ein Segen, Nacht ist auch eine Sonne,
ch-p4-19-v57 [es] | EMPTY while DE non-empty | DE: Schmerz ist auch eine Lust, Fluch ist auch ein Segen, Nacht ist auch eine Sonne,
ch-p4-19-v58 [fr] | EMPTY while DE non-empty | DE: Sagtet ihr jemals ja zu Einer Lust? Oh, meine Freunde, so sagtet ihr Ja auch zu 
ch-p4-19-v60 [fr] | EMPTY while DE non-empty | DE: —Alles von neuem, Alles ewig, Alles verkettet, verfädelt, verliebt, oh so liebte
ch-p4-19-v60 [es] | EMPTY while DE non-empty | DE: —Alles von neuem, Alles ewig, Alles verkettet, verfädelt, verliebt, oh so liebte
ch-p4-19-v61 [fr] | EMPTY while DE non-empty | DE: —ihr Ewigen, liebt sie ewig und allezeit: und auch zum Weh sprecht ihr: vergeh, 
ch-p4-19-v62 [es] | EMPTY while DE non-empty | DE: Alle Lust will aller Dinge Ewigkeit, will Honig, will Hefe, will trunkene Mitter
ch-p4-19-v63 [fr] | EMPTY while DE non-empty | DE: —was will nicht Lust! sie ist durstiger, herzlicher, hungriger, schrecklicher, h
ch-p4-19-v64 [fr] | EMPTY while DE non-empty | DE: —sie will Liebe, sie will Hass, sie ist überreich, schenkt, wirft weg, bettelt, 
ch-p4-19-v64 [es] | EMPTY while DE non-empty | DE: —sie will Liebe, sie will Hass, sie ist überreich, schenkt, wirft weg, bettelt, 
ch-p4-19-v65 [fr] | EMPTY while DE non-empty | DE: —so reich ist Lust, dass sie nach Wehe durstet, nach Hölle, nach Hass, nach Schm
ch-p4-19-v66 [fr] | EMPTY while DE non-empty | DE: Ihr höheren Menschen, nach euch sehnt sie sich, die Lust, die unbändige, selige,
ch-p4-19-v67 [fr] | EMPTY while DE non-empty | DE: Denn alle Lust will sich selber, drum will sie auch Herzeleid! Oh Glück, oh Schm
ch-p4-19-v67 [es] | EMPTY while DE non-empty | DE: Denn alle Lust will sich selber, drum will sie auch Herzeleid! Oh Glück, oh Schm
ch-p4-19-v68 [fr] | EMPTY while DE non-empty | DE: —Lust will aller Dinge Ewigkeit, will tiefe, tiefe Ewigkeit!
ch-p4-19-v69 [fr] | EMPTY while DE non-empty | DE: Lerntet ihr nun mein Lied? Erriethet ihr, was es will? Wohlan! Wohlauf! Ihr höhe
ch-p4-19-v70 [fr] | EMPTY while DE non-empty | DE: Singt mir nun selber das Lied, dess Name ist „Noch ein Mal“, dess Sinn ist „in a
ch-p4-19-v71 [en] | EMPTY while DE non-empty | DE: Oh Mensch! Gieb Acht! Was spricht die tiefe Mitternacht? „Ich schlief, ich schli
ch-p4-19-v71 [fr] | EMPTY while DE non-empty | DE: Oh Mensch! Gieb Acht! Was spricht die tiefe Mitternacht? „Ich schlief, ich schli
ch-p4-20-v01 [fr] | EMPTY while DE non-empty | DE: Des Morgens aber nach dieser Nacht sprang Zarathustra von seinem Lager auf, gürt
ch-p4-20-v02 [fr] | EMPTY while DE non-empty | DE: „Du grosses Gestirn, sprach er, wie er einstmal gesprochen hatte, du tiefes Glüc
ch-p4-20-v04 [fr] | EMPTY while DE non-empty | DE: Wohlan! sie schlafen noch, diese höheren Menschen, während ich wach bin: das sin
ch-p4-20-v05 [fr] | EMPTY while DE non-empty | DE: Zu meinem Werke will ich, zu meinem Tage: aber sie verstehen nicht, was die Zeic
ch-p4-20-v07 [fr] | EMPTY while DE non-empty | DE: —Diess hatte Zarathustra zu seinem Herzen gesprochen, als die Sonne aufgieng: da
ch-p4-20-v08 [fr] | EMPTY while DE non-empty | DE: Mein Adler ist wach und ehrt gleich mir die Sonne. Mit Adlers-Klauen greift er n
ch-p4-20-v10 [fr] | EMPTY while DE non-empty | DE: Also sprach Zarathustra; da aber geschah es, dass er sich plötzlich wie von unzä
ch-p4-20-v11 [fr] | EMPTY while DE non-empty | DE: „Was geschieht mir?“ dachte Zarathustra in seinem erstaunten Herzen und liess si
ch-p4-20-v12 [fr] | EMPTY while DE non-empty | DE: „Das Zeichen kommt,“ sprach Zarathustra und sein Herz verwandelte sich. Und in W
ch-p4-20-v13 [fr] | EMPTY while DE non-empty | DE: Zu dem Allen sprach Zarathustra nur Ein Wort: „meine Kinder sind nahe, meine Kin
ch-p4-20-v14 [fr] | EMPTY while DE non-empty | DE: Diess Alles dauerte eine lange Zeit, oder eine kurze Zeit: denn, recht gesproche
ch-p4-20-v15 [fr] | EMPTY while DE non-empty | DE: Zarathustra selber aber, betäubt und fremd, erhob sich von seinem Sitze, sah um 
ch-p4-20-v17 [fr] | EMPTY while DE non-empty | DE: Oh ihr höheren Menschen, von eurer Noth war's ja, dass gestern am Morgen jener a
ch-p4-20-v17 [es] | EMPTY while DE non-empty | DE: Oh ihr höheren Menschen, von eurer Noth war's ja, dass gestern am Morgen jener a
ch-p4-20-v18 [fr] | EMPTY while DE non-empty | DE: —zu eurer Noth wollte er mich verfuhren und versuchen: oh Zarathustra, sprach er
ch-p4-20-v18 [es] | EMPTY while DE non-empty | DE: —zu eurer Noth wollte er mich verfuhren und versuchen: oh Zarathustra, sprach er
ch-p4-20-v19 [fr] | EMPTY while DE non-empty | DE: Zu meiner letzten Sünde? rief Zarathustra und lachte zornig über sein eigenes Wo
ch-p4-20-v20 [fr] | EMPTY while DE non-empty | DE: —Und noch ein Mal versank Zarathustra in sich und setzte sich wieder auf den gro
ch-p4-20-v20 [es] | EMPTY while DE non-empty | DE: —Und noch ein Mal versank Zarathustra in sich und setzte sich wieder auf den gro
ch-p4-20-v22 [fr] | EMPTY while DE non-empty | DE: Mein Leid und mein Mitleiden—was liegt daran! Trachte ich denn nach Glücke? Ich 
ch-p4-20-v23 [fr] | EMPTY while DE non-empty | DE: Wohlan! Der Löwe kam, meine Kinder sind nahe, Zarathustra ward reif, meine Stund
ch-p4-20-v23 [es] | EMPTY while DE non-empty | DE: Wohlan! Der Löwe kam, meine Kinder sind nahe, Zarathustra ward reif, meine Stund
ch-p4-20-v24 [fr] | EMPTY while DE non-empty | DE: Dies ist mein Morgen, mein Tag hebt an: herauf nun, herauf, du grosser Mittag!“—
ch-p4-20-v25 [fr] | EMPTY while DE non-empty | DE: Also sprach Zarathustra und verliess seine Höhle, glühend und stark, wie eine Mo
ch-p4-20-v25 [es] | EMPTY while DE non-empty | DE: Also sprach Zarathustra und verliess seine Höhle, glühend und stark, wie eine Mo

_Total surface findings: 1136; empties: 667_


## 2b. Length-ratio defects (target much shorter/longer than DE)
ch-p0-00-v12 [fr] ratio=7.62 | length ratio out of bounds | Zarathoustra descendit seul des montagnes, et il ne rencontra personne. Mais lorsqu'il arriva dans l
ch-p0-00-v18 [en] ratio=2.98 | length ratio out of bounds | As in the sea hast thou lived in solitude, and it hath borne thee up. Alas, wilt thou now go ashore?
ch-p0-00-v19 [en] ratio=0.32 | length ratio out of bounds | Zarathustra answered: “I love mankind.”
ch-p0-00-v20 [es] ratio=0.32 | length ratio out of bounds | Zaratustra respondió: «Yo amo a los hombres.»
ch-p0-00-v25 [en] ratio=0.39 | length ratio out of bounds | “No,” replied Zarathustra, “I give no alms. I am not poor enough for that.”
ch-p0-00-v26 [es] ratio=0.40 | length ratio out of bounds | «No, respondió Zaratustra, yo no doy limosnas. No soy bastante pobre para eso.»
ch-p0-00-v28 [es] ratio=3.61 | length ratio out of bounds | Nuestros pasos les suenan demasiado solitarios por sus callejas. Y cuando por las noches, estando en
ch-p0-00-v31 [es] ratio=0.38 | length ratio out of bounds | El santo respondió: Hago canciones y las canto, y, al hacerlas, río, lloro y gruño: así alabo a Dios
ch-p0-00-v39 [en] ratio=3.24 | length ratio out of bounds | Even the wisest among you is only a disharmony and hybrid of plant and phantom. But do I bid you bec
ch-p0-00-v39 [es] ratio=10.03 | length ratio out of bounds | ¿Qué es el mono para el hombre? Una irrisión o una vergüenza dolorosa. Y justo eso es lo que el homb
ch-p0-00-v40 [en] ratio=0.32 | length ratio out of bounds | Lo, I teach you the Superman!
ch-p0-00-v41 [es] ratio=0.20 | length ratio out of bounds | ¡Mirad, yo os enseño el superhombre!
ch-p0-00-v44 [es] ratio=0.29 | length ratio out of bounds | Son despreciadores de la vida, son moribundos y están,
ch-p0-00-v59 [en] ratio=0.27 | length ratio out of bounds | Lo, I teach you the Superman: he is that lightning, he is that frenzy!—
ch-p0-00-v60 [en] ratio=3.68 | length ratio out of bounds | When Zarathustra had thus spoken, one of the people called out: “We have now heard enough of the rop
ch-p0-00-v80 [es] ratio=0.25 | length ratio out of bounds | pasa así de buen grado por el puente.
ch-p0-00-v89 [en] ratio=0.31 | length ratio out of bounds | And thus spake Zarathustra unto the people:
ch-p0-00-v89 [es] ratio=0.23 | length ratio out of bounds | YZaratustra habló así al pueblo:
ch-p0-00-v94 [en] ratio=3.95 | length ratio out of bounds | Alas! There cometh the time when man will no longer give birth to any star. Alas! There cometh the t
ch-p0-00-v94 [es] ratio=3.90 | length ratio out of bounds | ¡Ay! Llega el tiempo en que el hombre no dará ya a luz ninguna estrella. ¡Ay! Llega el tiempo del ho
ch-p0-00-v95 [en] ratio=0.26 | length ratio out of bounds | Lo! I show you THE LAST MAN.
ch-p0-00-v95 [es] ratio=0.36 | length ratio out of bounds | ¡Mirad! Yo os muestro el último hombre.
ch-p0-00-v97 [en] ratio=2.62 | length ratio out of bounds | The earth hath then become small, and on it there hoppeth the last man who maketh everything small. 
ch-p0-00-v97 [es] ratio=2.76 | length ratio out of bounds | La tierra se ha vuelto pequeña entonces, y sobre ella da saltos el último hombre, que todo lo empequ
ch-p0-00-v108 [en] ratio=0.17 | length ratio out of bounds | “We have discovered happiness,”—say the last men, and blink thereby.—
ch-p0-00-v108 [es] ratio=0.20 | length ratio out of bounds | "Nosotros hemos inventado la felicidad" - dicen los últimos hombres, y parpadean. -
ch-p0-00-v109 [en] ratio=6.26 | length ratio out of bounds | And here ended the first discourse of Zarathustra, which is also called “The Prologue”: for at this 
ch-p0-00-v109 [es] ratio=6.14 | length ratio out of bounds | Yaquí acabó el primer discurso de Zaratustra, llamado también «el prólogo»: pues en este punto el gr
ch-p0-00-v113 [en] ratio=0.08 | length ratio out of bounds | And now do they look at me and laugh: and while they laugh they hate me too. There is ice in their l
ch-p0-00-v113 [es] ratio=0.06 | length ratio out of bounds | Yahora me miran y se ríen: y mientras ríen, continúan odiándome. Hay hielo en su reír.
ch-p0-00-v114 [en] ratio=3.56 | length ratio out of bounds | Then, however, something happened which made every mouth mute and every eye fixed. In the meantime, 
ch-p0-00-v115 [es] ratio=2.71 | length ratio out of bounds | cuando estaba ya a un solo paso detrás de él ocurrió aquella cosa horrible que hizo callar todas las
ch-p0-00-v119 [en] ratio=0.38 | length ratio out of bounds | When Zarathustra had said this the dying one did not reply further; but he moved his hand as if he s
ch-p0-00-v120 [en] ratio=3.46 | length ratio out of bounds | Meanwhile the evening came on, and the market-place veiled itself in gloom. Then the people disperse
ch-p0-00-v121 [es] ratio=3.51 | length ratio out of bounds | Entretanto iba llegando el atardecer, y el mercado se ocultaba en la oscuridad: el pueblo se dispers
ch-p0-00-v125 [en] ratio=0.16 | length ratio out of bounds | Gloomy is the night, gloomy are the ways of Zarathustra. Come, thou cold and stiff companion! I carr
ch-p0-00-v125 [fr] ratio=0.27 | length ratio out of bounds | Quand Zarathoustra eut dit cela à son coeur, il chargea le cadavre sur ses épaules et se mit en rout
ch-p0-00-v125 [es] ratio=0.15 | length ratio out of bounds | Mas todavía estoy muy lejos de ellos, y mi sentido no habla a sus sentidos. Para los hombres yo soy 
ch-p0-00-v126 [es] ratio=0.25 | length ratio out of bounds | Oscura es la noche, oscuros son los caminos de Zaratustra. ¡Ven, compañero frío y rígido! Te llevaré
ch-p0-00-v127 [fr] ratio=0.37 | length ratio out of bounds | Après avoir dit ces choses, l'homme disparut; et Zarathoustra continua son chemin par les rues obscu
ch-p0-00-v127 [es] ratio=3.34 | length ratio out of bounds | Cuando Zaratustra hubo dicho esto a su corazón, cargó el cadáver sobre sus espaldas y se puso en cam
ch-p0-00-v128 [fr] ratio=4.07 | length ratio out of bounds | A la porte de la ville il rencontra les fossoyeurs: ils éclairèrent sa figure de leur flambeau, reco
ch-p0-00-v128 [es] ratio=3.99 | length ratio out of bounds | Ala puerta de la ciudad encontró a los sepultureros: éstos iluminaron el rostro de Zaratustra con la
ch-p0-00-v132 [en] ratio=0.35 | length ratio out of bounds | “A living man and a dead one,” said Zarathustra. “Give me something to eat and drink, I forgot it du
ch-p0-00-v132 [fr] ratio=0.35 | length ratio out of bounds | En parlant ainsi, Zarathoustra frappa à la porte de la maison. Un vieil homme parut aussitôt: il por
ch-p0-00-v132 [es] ratio=0.22 | length ratio out of bounds | Ymientras decía esto, Zaratustra llamó a la puerta de la casa. Un hombre viejo apareció; traía la lu
ch-p0-00-v133 [fr] ratio=0.38 | length ratio out of bounds | "Un vivant et un mort, dit Zarathoustra. Donnez-moi à manger et à boire, j'ai oublié de le faire pen
ch-p0-00-v133 [es] ratio=0.07 | length ratio out of bounds | «¿Quién viene a mí y a mi mal dormir?»
ch-p0-00-v135 [en] ratio=2.69 | length ratio out of bounds | Long slept Zarathustra; and not only the rosy dawn passed over his head, but also the morning. At la
ch-p0-00-v135 [es] ratio=7.71 | length ratio out of bounds | El viejo se fue y al poco volvió y ofreció a Zaratustra pan y vino. «Mal sitio es éste para hambrien
ch-p0-00-v136 [fr] ratio=4.83 | length ratio out of bounds | Ensuite Zarathoustra marcha de nouveau pendant deux heures, se fiant à la route et à la clarté des é
ch-p0-00-v136 [es] ratio=3.26 | length ratio out of bounds | Largo tiempo durmió Zaratustra, y no sólo la aurora pasó sobre su rostro, sino también la mañana ent
ch-p0-00-v137 [fr] ratio=3.17 | length ratio out of bounds | Zarathoustra dormit longtemps et non seulement l'aurore passa sur son visage, mais encore le matin. 
ch-p0-00-v143 [es] ratio=0.15 | length ratio out of bounds | - pero ése es el creador.
ch-p0-00-v152 [en] ratio=0.34 | length ratio out of bounds | I make for my goal, I follow my course; over the loitering and tardy will I leap. Thus let my on-goi
ch-p0-00-v153 [en] ratio=4.71 | length ratio out of bounds | This had Zarathustra said to his heart when the sun stood at noontide. Then he looked inquiringly al
ch-p0-00-v154 [fr] ratio=3.30 | length ratio out of bounds | Zarathoustra avait dit cela à son coeur, alors que le soleil était à son midi: puis il interrogea le
ch-p0-00-v155 [es] ratio=5.44 | length ratio out of bounds | Esto es lo que Zaratustra dijo a su corazón cuando el sol estaba en pleno mediodía: entonces se puso
ch-p0-00-v161 [en] ratio=3.00 | length ratio out of bounds | And if my wisdom should some day forsake me:—alas! it loveth to fly away!—may my pride then fly with
ch-p0-00-v162 [fr] ratio=5.13 | length ratio out of bounds | Et si ma sagesse m'abandonne un jour: - hélas, elle aime à s'envoler! - puisse du moins ma fierté vo
ch-p0-00-v162 [es] ratio=4.30 | length ratio out of bounds | Pero pido cosas imposibles: ¡por ello pido a mi orgullo que camine siempre junto a mi inteligencia!
ch-p1-02-v25 [es] ratio=2.98 | length ratio out of bounds | En verdad, con suave calzado viene a mí él, el más encantador de los ladrones, y me roba mis pensami
ch-p1-03-v06 [es] ratio=2.62 | length ratio out of bounds | Este mundo, eternamente imperfecto, imagen, e imagen imperfecta, de una contradicción eterna - un eb
ch-p1-07-v15 [es] ratio=3.27 | length ratio out of bounds | Quien asciende a las montañas más altas se ríe de todas las tragedias, de las del teatro y de las de
ch-p1-07-v20 [es] ratio=2.57 | length ratio out of bounds | Es verdad: nosotros amamos la vida no porque estemos habituados a vivir, sino porque estamos habitua
ch-p1-09-v12 [es] ratio=2.56 | length ratio out of bounds | Su sabiduría dice: «¡tonto es el que continúa viviendo, mas también nosotros somos así de tontos! ¡Y
ch-p1-13-v15 [es] ratio=5.44 | length ratio out of bounds | Ytambién os propongo esta parábola: no pocos que quisieron expulsar a su demonio fueron a parar ello
ch-p1-15-v15 [es] ratio=2.80 | length ratio out of bounds | Para conservarse, el hombre empezó implantando valores en las cosas, - ¡él fue el primero en crear u
ch-p1-18-v06 [fr] ratio=3.05 | length ratio out of bounds | Tandis que, solitaire, je suivais aujourd'hui mon chemin, à l'heure où décline le soleil, j'ai renco
ch-p1-18-v30 [es] ratio=3.17 | length ratio out of bounds | ¡Es extraño, Zaratustra conoce poco a las mujeres, y, sin embargo, tiene razón sobre ellas! ¿Ocurre 
ch-p1-19-v11 [es] ratio=2.57 | length ratio out of bounds | No me gusta vuestra fría justicia; y desde los ojos de vuestros jueces me miran siempre el verdugo y
ch-p1-20-v07 [fr] ratio=2.67 | length ratio out of bounds | Tu dois construire plus haut que toi-même. Mais il faut d'abord que tu sois construit toi-même, carr
ch-p1-20-v12 [es] ratio=2.59 | length ratio out of bounds | ¡Ay, esa pobreza de alma entre dos! ¡Ay, esa suciedad de alma entre dos! ¡Ay, ese lamentable bienest
ch-p1-20-v21 [es] ratio=2.86 | length ratio out of bounds | Aquél otro buscaba una criada que tuviese las virtudes de un ángel. Pero de una sola vez se convirti
ch-p1-21-v11 [es] ratio=3.39 | length ratio out of bounds | Tanto al combatiente como al victorioso les resulta odiosa esa vuestra gesticuladora muerte que se a
ch-p1-22-v56 [en] ratio=0.29 | length ratio out of bounds | “—and only when ye have all denied me, will I return unto you.
ch-p2-01-v02 [es] ratio=4.59 | length ratio out of bounds | El niño del espejo Z aratustra volvió a continuación a las montañas y a la soledad de su caverna y s
ch-p2-01-v09 [es] ratio=3.83 | length ratio out of bounds | En verdad, demasiado bien comprendo el signo y la adver-tencia del sueño: ¡mi doctrina está en pelig
ch-p2-02-v08 [es] ratio=2.61 | length ratio out of bounds | ¡Acaso no vosotros mismos, hermanos míos! Pero podríais transformaros en padres y antepasados del su
ch-p2-02-v13 [es] ratio=2.88 | length ratio out of bounds | Mas para revelaros totalmente mi corazón a vosotros, amigos: si hubiera dioses, ¡cómo soportaría yo 
ch-p2-04-v11 [es] ratio=2.69 | length ratio out of bounds | ¡En cadenas de falsos valores y de palabras ilusas! ¡Ay, si alguien los redimiese de su redentor! En
ch-p2-04-v37 [es] ratio=2.51 | length ratio out of bounds | Nunca ha habido todavía un superhombre. Desnudos he visto yo a ambos, al hombre más grande y al más 
ch-p2-06-v26 [en] ratio=0.37 | length ratio out of bounds | A summer on the loftiest height, with cold fountains and blissful stillness: oh, come, my friends, t
ch-p2-06-v26 [fr] ratio=0.40 | length ratio out of bounds | Un été dans les plus grandes hauteurs, avec de froides sources et une bienheureuse tranquillité: ven
ch-p2-06-v26 [es] ratio=0.39 | length ratio out of bounds | Un verano en lo más alto, con fuentes frías y silencio bienaventurado: ¡oh, venid, amigos míos, para
ch-p2-07-v37 [es] ratio=5.58 | length ratio out of bounds | Que existen lucha y desigualdad incluso en la belleza, y guerra por el poder y por el sobrepoder: es
ch-p2-09-v26 [es] ratio=0.24 | length ratio out of bounds | Así cantó Zaratustra.
ch-p2-10-v10 [es] ratio=2.66 | length ratio out of bounds | Una canción de baile y de mofa contra el espíritu de la pesadez, mi supremo y más poderoso diablo, d
ch-p2-11-v02 [es] ratio=3.45 | length ratio out of bounds | La canción de los sepukros A llí está la isla de los sepulcros, la silenciosa; allí están también lo
ch-p2-11-v06 [es] ratio=2.68 | length ratio out of bounds | Aún continúo siendo el más rico y el más digno de envidia - ¡yo el más solitario! Pues yo os tuve a 
ch-p2-14-v31 [es] ratio=4.04 | length ratio out of bounds | ¡En verdad, no por ello me ha de pesar más! Y no de vosotros, hombres del presente, debe llegarme a 
ch-p2-17-v15 [es] ratio=2.72 | length ratio out of bounds | ¿Y quién de entre nosotros los poetas no ha adulterado su propio vino? Más de una venenosa mixtura h
ch-p2-17-v24 [es] ratio=3.17 | length ratio out of bounds | En verdad, siempre somos arrastrados hacia lo alto - es decir, hacia el reino de las nubes: sobre és
ch-p2-18-v04 [es] ratio=0.28 | length ratio out of bounds | «¡Mirad!, dijo el viejo timonel, ¡ahí va Zaratustra al infierno!»z39_
ch-p2-18-v07 [es] ratio=7.87 | length ratio out of bounds | Por los mismos días en que estos marineros habían desembarcado en la isla de fuego se difundió el ru
ch-p2-18-v14 [es] ratio=2.61 | length ratio out of bounds | Alo sumo te considero el ventrílocuo de la tierra: y siempre que he oído hablar a los demonios de la
ch-p2-18-v24 [es] ratio=2.96 | length ratio out of bounds | Éste es el consejo que doy a los reyes y a las Iglesias y a todo lo que es débil por edad y por virt
ch-p2-18-v30 [fr] ratio=2.80 | length ratio out of bounds | Enfin, il finit par se taire et ses hoquets diminuèrent; mais dès qu'il se fut tu, je dis en riant: 
ch-p2-20-v48 [es] ratio=3.53 | length ratio out of bounds | - En este momento de su discurso ocurrió que Zaratustra se detuvo de repente, y semejaba del todo al
ch-p2-21-v28 [es] ratio=3.15 | length ratio out of bounds | Es cierto que así como vuestros sapientísimos no me parecen tan sabios, así también encontré que la 
ch-p2-22-v06 [es] ratio=2.93 | length ratio out of bounds | Yesto es lo que ocurrió, - ¡pues tengo que deciros todo, para que vuestro corazón no se endurezca co
ch-p2-22-v19 [es] ratio=3.17 | length ratio out of bounds | Entonces algo me habló de nuevo sin voz: «¡Qué importas tú, Zaratustra! ¡ Di tu palabra y hazte peda
ch-p2-22-v32 [es] ratio=8.53 | length ratio out of bounds | Entonces algo me habló de nuevo como un susurro: «Las palabras más silenciosas son las que traen la 
ch-p2-22-v35 [es] ratio=2.63 | length ratio out of bounds | El orgullo de la juventud está todavía sobre ti, tarde te has hecho joven: pero el que quiere conver
ch-p2-22-v44 [en] ratio=0.36 | length ratio out of bounds | “Ye look aloft when ye long for exaltation, and I look downward because I am exalted.
ch-p2-22-v45 [es] ratio=2.95 | length ratio out of bounds | Quien asciende a las montañas más altas se ríe de todas las tragedias, de las del teatro y de las de
ch-p3-01-v04 [es] ratio=2.60 | length ratio out of bounds | Ysea cual sea mi destino, sean cuales sean las vivencias que aún haya yo de experimentar, - siempre 
ch-p3-01-v14 [es] ratio=3.18 | length ratio out of bounds | Quien siempre se ha tratado a sí mismo con mucha indulgencia acaba por enfermar a causa de ello. ¡Al
ch-p3-02-v06 [es] ratio=2.67 | length ratio out of bounds | - pues no queréis, con mano cobarde, seguir a tientas un hilo; y allí donde podéis adivinar, odiáis 
ch-p3-02-v17 [es] ratio=4.42 | length ratio out of bounds | Yo subía, subía, soñaba, pensaba, - mas todo me oprimía. Me asemejaba a un enfermo al que su terribl
ch-p3-02-v42 [es] ratio=2.84 | length ratio out of bounds | - de tal modo que me dio lástima. Pues justo en aquel momento la luna llena, con un silencio de muer
ch-p3-02-v45 [es] ratio=0.19 | length ratio out of bounds | un perro gritar así pidiendo socorro?
ch-p3-02-v48 [es] ratio=0.12 | length ratio out of bounds | « ¡Muerde! ¡Muerde!
ch-p3-02-v49 [es] ratio=2.76 | length ratio out of bounds | ¡Arráncale la cabeza! ¡Muerde!» - éste fue el grito que de mí se escapó, mi horror, mi odio, mi náus
ch-p3-03-v29 [es] ratio=0.39 | length ratio out of bounds | Bastante terrible ha sido ya siempre para mí tu pesadez:
ch-p3-03-v34 [fr] ratio=0.37 | length ratio out of bounds | En vérité, je me méfie de votre beauté maligne!
ch-p3-04-v34 [es] ratio=4.27 | length ratio out of bounds | Oh cielo por encima de mí, ¡tú puro!, ¡elevado! Ésta es para mí tu pureza, ¡que no existe ninguna et
ch-p3-05-v08 [es] ratio=3.23 | length ratio out of bounds | Oh, cuándo regresaré a mi patria, donde ya no tengo que agacharme - ¡donde ya no tengo que agacharme
ch-p3-05-v55 [es] ratio=4.32 | length ratio out of bounds | Yen verdad, más de un azar llegó hasta mí con aire señorial: pero más señorialmente aún le habló mi 
ch-p3-05-v57 [es] ratio=2.62 | length ratio out of bounds | ¡Vosotros os volvéis cada vez más pequeños, gentes pequeñas! ¡Vosotros os hacéis migajas, oh cómodos
ch-p3-06-v16 [fr] ratio=4.93 | length ratio out of bounds | Car c'est surtout le matin que je suis méchant: à la première heure, quand les seaux grincent à la f
ch-p3-06-v16 [es] ratio=5.03 | length ratio out of bounds | Especialmente maligno soy, ciertamente, por la mañana: a una hora temprana, cuando el cubo rechina e
ch-p3-06-v36 [fr] ratio=3.48 | length ratio out of bounds | Comment sauraient-ils supporter mon bonheur si je ne mettais autour de mon bonheur des accidents et 
ch-p3-07-v04 [fr] ratio=4.46 | length ratio out of bounds | "O Zarathoustra, c'est ici qu'est la grande ville: tu n'as rien à y chercher et tout à y perdre. Pou
ch-p3-07-v23 [fr] ratio=3.42 | length ratio out of bounds | Crache sur la ville des âmes déprimées et des poitrines étroites, des yeux envieux et des doigts glu
ch-p3-07-v23 [es] ratio=3.76 | length ratio out of bounds | Escupe a la ciudad de las almas aplastadas y de los pechos estrechos, de los ojos afilados, de los d
ch-p3-07-v34 [fr] ratio=2.53 | length ratio out of bounds | Qu'était-ce donc qui te fit grogner ainsi? Personne ne te flattait assez: - c'est pourquoi tu t'es a
ch-p3-07-v34 [es] ratio=2.55 | length ratio out of bounds | ¿Qué fue, pues, lo que te llevó a gruñir? El que nadie te haya adulado bastante: - por eso te pusist
ch-p3-08-v05 [es] ratio=2.55 | length ratio out of bounds | En verdad, algunos de ellos levantaron en otro tiempo las piernas como un bailarín, a ellos hízoles 
ch-p3-08-v14 [fr] ratio=0.04 | length ratio out of bounds | - 2.
ch-p3-08-v45 [fr] ratio=2.85 | length ratio out of bounds | C'est ce qui arriva lorsqu'un dieu prononça lui-même la parole la plus impie, - la parole: "Il n'y a
ch-p3-08-v45 [es] ratio=2.58 | length ratio out of bounds | Esto ocurrió cuando la palabra más atea de todas fue pronunciada por un dios mismo, - la palabra: «¡
ch-p3-09-v03 [fr] ratio=3.17 | length ratio out of bounds | Maintenant menace-moi du doigt, ainsi qu'une mère menace, et souris-moi comme sourit une mère, dis-m
ch-p3-09-v03 [es] ratio=3.16 | length ratio out of bounds | Pero ahora amenázame tan sólo con el dedo, como amenazan las madres, ahora sonríeme como sonríen las
ch-p3-09-v11 [es] ratio=0.17 | length ratio out of bounds | ¡aquello era abandono!
ch-p3-09-v15 [fr] ratio=2.55 | length ratio out of bounds | "Et te souviens-tu, ô Zarathoustra? Lorsque vint ton heure la plus silencieuse qui te chassa de toi-
ch-p3-09-v16 [es] ratio=4.27 | length ratio out of bounds | ¿Y lo sabes todavía, oh Zaratustra? Cuando llegó tu hora más silenciosa y te arrastró lejos de ti mi
ch-p3-09-v39 [fr] ratio=2.99 | length ratio out of bounds | Me cacher moi-même et ma richesse - voilà ce que j'ai appris à faire là-bas: car j'ai trouvé chacun 
ch-p3-09-v39 [es] ratio=4.95 | length ratio out of bounds | Aquien vive entre los buenos la compasión le enseña a mentir. La compasión vicia el aire a todas las
ch-p3-10-v08 [fr] ratio=5.24 | length ratio out of bounds | Avec quelle certitude mon rêve a regardé ce monde fini! Ce n'était de sa part ni curiosité, ni indis
ch-p3-10-v09 [es] ratio=3.61 | length ratio out of bounds | - así se me ofrecía el mundo: - - como si un árbol me hiciera señas, un árbol de amplio ra-maje, de 
ch-p3-10-v13 [es] ratio=2.66 | length ratio out of bounds | Ypara proceder durante el día como él, y para seguirlo e imitarlo en lo mejor de él: quiero yo ahora
ch-p3-10-v23 [es] ratio=2.61 | length ratio out of bounds | Voluptuosidad: la gran felicidad que sirve de símbolo a toda felicidad más alta y a la suprema esper
ch-p3-10-v24 [fr] ratio=3.19 | length ratio out of bounds | Volupté - c'est la plus grande félicité symbolique pour le bonheur et l'espoir supérieur. Car il y a
ch-p3-10-v34 [fr] ratio=2.58 | length ratio out of bounds | Que la hauteur solitaire ne s'esseule pas éternellement et ne se contente pas de soi; que la montagn
ch-p3-10-v36 [es] ratio=2.57 | length ratio out of bounds | Yentonces ocurrió también, - ¡y, en verdad, ocurrió por vez primera! - que su palabra llamó bienaven
ch-p3-10-v37 [fr] ratio=2.82 | length ratio out of bounds | Et c'est alors qu'il arriva aussi - et, en vérité, ce fut pour la première fois! - que sa parole fit
ch-p3-11-v23 [fr] ratio=2.54 | length ratio out of bounds | Et, en vérité! bien des choses qui vous sont propres sont aussi lourdes à porter! Et l'intérieur de 
ch-p3-11-v23 [es] ratio=2.74 | length ratio out of bounds | ¡Y en verdad! ¡También algunas cosas propias son una carga pesada! ¡Y muchas de las cosas que reside
ch-p3-11-v32 [es] ratio=3.05 | length ratio out of bounds | Pero masticar y digerir todo - ¡ésa es realmente cosa propia de cerdos! Decir siempre sí - ¡esto lo 
ch-p3-11-v37 [en] ratio=3.05 | length ratio out of bounds | Unhappy do I also call those who have ever to WAIT,—they are repugnant to my taste—all the toll-gath
ch-p3-11-v37 [fr] ratio=3.56 | length ratio out of bounds | J'appelle encore malheureux ceux qui sont obligés d'attendre toujours, - ils ne sont pas à mon goût,
ch-p3-11-v37 [es] ratio=3.25 | length ratio out of bounds | Desventurados llamo yo a todos aquellos que siempre tienen que aguardar, - repugnan a mi gusto: todo
ch-p3-11-v42 [es] ratio=4.04 | length ratio out of bounds | Con escalas de cuerda he aprendido yo a escalar más de una ventana, con ágiles piernas he trepado a 
ch-p3-11-v45 [fr] ratio=2.93 | length ratio out of bounds | Essayer et interroger, ce fut là toute ma façon de marcher: - et, en vérité, il faut aussi apprendre
ch-p3-12-v16 [fr] ratio=3.65 | length ratio out of bounds | Et souvent il m'a emporté bien loin, au delà des monts, vers les hauteurs, au milieu du rire: alors 
ch-p3-12-v19 [fr] ratio=5.69 | length ratio out of bounds | Où tout devenir me semblait danses et malices divines, où le monde déchaîné et effréné se réfugiait 
ch-p3-12-v20 [es] ratio=5.84 | length ratio out of bounds | cojeo y balbuceo; ¡y en verdad, me avergüenzo de tener que ser todavía poeta! - Hacia allí donde tod
ch-p3-12-v22 [fr] ratio=3.26 | length ratio out of bounds | C'est là aussi que j'ai ramassé sur ma route le mot de "Surhumain" et cette doctrine: l'homme est qu
ch-p3-12-v30 [es] ratio=4.29 | length ratio out of bounds | Aredimir lo pasado en el hombre y a transformar mediante su creación todo «Fue», hasta que la volunt
ch-p3-12-v34 [es] ratio=3.45 | length ratio out of bounds | Del sol he aprendido esto, cuando se hunde él, el inmensamente rico: entonces es cuando derrama oro 
ch-p3-12-v88 [es] ratio=3.95 | length ratio out of bounds | - Pues poder estar de pie es un mérito entre los cortesanos: y todos los cortesanos creen que de la 
ch-p3-12-v110 [es] ratio=2.57 | length ratio out of bounds | «Y tu propia razón - a ésa tú mismo debes agarrarla del cuello y estrangularla; pues es una razón de
ch-p3-12-v114 [es] ratio=3.82 | length ratio out of bounds | ¡Rompedme, oh hermanos míos, rompedme también esta nueva tabla! Los cansados del mundo la han colgad
ch-p3-12-v144 [es] ratio=4.08 | length ratio out of bounds | Yo trazo e n torno a m í círculos y fronteras sagradas; cada vez es menor el número de quienes conmi
ch-p3-12-v153 [fr] ratio=4.29 | length ratio out of bounds | Car l'âme qui a la plus longue échelle et qui peut descendre le plus bas: comment ne porterait-elle 
ch-p3-12-v153 [es] ratio=4.22 | length ratio out of bounds | El alma, en efecto, que posee la escala más larga y que más profundo puede descender: ¿cómo no iban 
ch-p3-12-v162 [es] ratio=3.65 | length ratio out of bounds | Debéis tener sólo enemigos que haya que odiar, pero no enemigos que haya que despreciar: es necesari
ch-p3-12-v163 [fr] ratio=3.00 | length ratio out of bounds | Il faut vous réserver pour un ennemi plus digne, ô mes amis: c'est pourquoi il y en a beaucoup devan
ch-p3-12-v204 [es] ratio=2.61 | length ratio out of bounds | Al creador es al que más odian: a quien rompe tablas y viejos valores, al quebrantador - llámanlo de
ch-p3-12-v230 [fr] ratio=4.81 | length ratio out of bounds | Hélas! quel oeil ne s'est pas obscurci dans cette ivresse de crépuscule? Hélas! quel pied n'a pas tr
ch-p3-12-v230 [es] ratio=4.82 | length ratio out of bounds | ¡Ay, a quién no se le oscurecieron los ojos en ese crepúsculo ebrio! ¡Ay, a quién no le vaciló el pi
ch-p3-13-v28 [fr] ratio=2.53 | length ratio out of bounds | - "O espiègles que vous êtes, ô serinettes! Répondit Zarathoustra en souriant de nouveau, comme vous
ch-p3-13-v28 [es] ratio=3.48 | length ratio out of bounds | En cada instante comienza el ser; en torno a todo '�quí" gira la esfera '�llá". El centro está en to
ch-p3-13-v36 [es] ratio=2.89 | length ratio out of bounds | Yo mismo - ¿quiero ser con esto el acusador del hombre? Ay, animales míos, esto es lo único que he a
ch-p3-13-v37 [fr] ratio=2.71 | length ratio out of bounds | Et moi-même - est-ce que je veux être par là l'accusateur de l'homme? Hélas! mes animaux, le plus gr
ch-p3-13-v45 [es] ratio=2.73 | length ratio out of bounds | Mi suspirar estaba sentado sobre todos los sepulcros de los hombres y no podía ponerse de pie; mi su
ch-p3-13-v65 [es] ratio=2.86 | length ratio out of bounds | Hablarías sin temblar, antes bien dando un aliviador suspiro de bienaventuranza: ¡pues una gran pesa
ch-p3-13-v67 [es] ratio=0.18 | length ratio out of bounds | jor o a una vida semejante:
ch-p3-13-v68 [fr] ratio=3.63 | length ratio out of bounds | Je reviendrai avec ce soleil, avec cette terre, avec cet aigle, avec ce serpent - non pas pour une v
ch-p3-14-v14 [fr] ratio=2.56 | length ratio out of bounds | O mon âme, tu es là maintenant, lourde et pleine d'abondance, un cep de vigne aux mamelles gonflées,
ch-p3-14-v17 [fr] ratio=2.90 | length ratio out of bounds | O mon âme, je t'ai tout donné et toutes mes mains se sont dépouillées pour toi: - et maintenant! Mai
ch-p3-14-v18 [es] ratio=3.55 | length ratio out of bounds | Oh alma mía, te he dado todo, y todas mis manos se han vaciado por ti: - ¡y ahora! Ahora me dices, s
ch-p3-14-v27 [fr] ratio=8.50 | length ratio out of bounds | Mais si tu ne veux pas pleurer, pleurer jusqu'à l'épuisement ta mélancolie de pourpre, il faudra que
ch-p3-14-v28 [es] ratio=6.31 | length ratio out of bounds | - cantar, con un canto rugiente, hasta que todos los mares se callen para escuchar tu anhelo, - - ha
ch-p3-14-v31 [es] ratio=0.25 | length ratio out of bounds | te cantar, mira, esto era mi última cosa!
ch-p3-15-v18 [es] ratio=0.39 | length ratio out of bounds | ¡Ahora, a mi lado! ¡Y rápido, maligna saltadora!
ch-p3-15-v20 [fr] ratio=2.84 | length ratio out of bounds | Ah! regarde comme je suis étendu! regarde, pétulante, comme j'implore ta grâce! J'aimerais bien à su
ch-p3-15-v36 [fr] ratio=3.28 | length ratio out of bounds | Il y a un vieux bourdon, lourd, très lourd: il sonne la nuit là-haut, jusque dans ta caverne: - quan
ch-p3-15-v36 [es] ratio=3.49 | length ratio out of bounds | Hay una vieja, pesada, pesada campana retumbante: ella retumba por la noche y su sonido asciende has
ch-p3-15-v41 [en] ratio=0.01 | length ratio out of bounds | One!
ch-p3-15-v41 [es] ratio=0.02 | length ratio out of bounds | ¡ Una!
ch-p3-16-v02 [fr] ratio=0.33 | length ratio out of bounds | (ou: Le chant de L'Alpha et de L'Oméga)
ch-p3-16-v04 [fr] ratio=3.23 | length ratio out of bounds | Si je suis un devin et plein de cet esprit divinatoire qui chemine sur une haute crête entre deux me
ch-p3-16-v06 [es] ratio=3.86 | length ratio out of bounds | dispuesta en su oscuro seno a lanzar el rayo y el redentor resplandor, grávida de rayos que dicen ¡s
ch-p3-16-v13 [es] ratio=4.03 | length ratio out of bounds | Si alguna vez me senté jubiloso allí donde yacen enterrados viejos dioses, bendiciendo al mundo, ama
ch-p3-16-v19 [fr] ratio=2.75 | length ratio out of bounds | Si jamais j'ai joué aux dés avec des dieux, à la table divine de la terre, en sorte que la terre tre
ch-p3-16-v27 [es] ratio=2.81 | length ratio out of bounds | Si yo mismo soy un grano de aquella sal redentora que hace que todas las cosas se mezclen bien en aq
ch-p3-16-v34 [es] ratio=2.60 | length ratio out of bounds | Si alguna vez mi júbilo gritó: «La costa ha desaparecido, - ahora ha caído mi última cadena - - lo i
ch-p3-16-v41 [es] ratio=3.05 | length ratio out of bounds | - dentro de la risa, en efecto, se congrega todo lo malvado, pero santificado y absuelto por su prop
ch-p3-16-v47 [fr] ratio=4.02 | length ratio out of bounds | Si j'ai nagé en me jouant dans de profonds lointains de lumière, si la sagesse d'oiseau de ma libert
ch-p3-16-v51 [en] ratio=0.35 | length ratio out of bounds | Ah, where in the world have there been greater follies than with the pitiful? And what in the world 
ch-p3-16-v51 [es] ratio=0.39 | length ratio out of bounds | Ay, ¿en qué lugar del mundo se han cometido tonterías mayores que entre los compasivos? ¿Y qué cosa 
ch-p3-16-v52 [es] ratio=3.06 | length ratio out of bounds | ¡Ay de todos aquellos que aman y no tienen todavía una altura que esté por encima de su compasión!
ch-p4-01-v04 [es] ratio=2.60 | length ratio out of bounds | - «Sí, animales míos, respondió él, acertado es vuestro consejo y conforme a mi corazón: ¡hoy quiero
ch-p4-01-v09 [fr] ratio=3.42 | length ratio out of bounds | Et lorsque j'ai demandé du miel, c'était une amorce que je demandais, des ruches dorées et douces et
ch-p4-01-v25 [es] ratio=3.44 | length ratio out of bounds | ¿Quién tiene que venir un día, y no le será lícito pasar de largo? Nuestro gran Hazar, es decir, nue
ch-p4-02-v01 [fr] ratio=0.27 | length ratio out of bounds | Le lendemain Zarathoustra était de nouveau assis sur sa pierre devant la caverne, tandis que ses ani
ch-p4-02-v03 [es] ratio=0.23 | length ratio out of bounds | «Bienvenido seas, dijo Zaratustra, tú adivino de la gran fatiga, no debe ser en vano el que en otro 
ch-p4-02-v04 [es] ratio=2.94 | length ratio out of bounds | - «¿Un viejo alegre?, respondió el adivino moviendo la cabeza: quien quiera que seas o quieras ser, 
ch-p4-02-v07 [es] ratio=3.81 | length ratio out of bounds | - «¡Compasión!, respondió el adivino con el corazón rebosante, y alzó las dos manos - ¡oh Zaratustra
ch-p4-03-v14 [fr] ratio=3.68 | length ratio out of bounds | C'est de la populace que nous nous sommes détournés, de tous ces braillards et de toutes ces mouches
ch-p4-03-v15 [es] ratio=3.14 | length ratio out of bounds | De la chusma hemos escapado, de todos esos vocingleros y moscardones que escriben, del hedor de los 
ch-p4-03-v23 [es] ratio=3.19 | length ratio out of bounds | Con la espada de esa palabra has desgarrado la más densa tiniebla de nuestro corazón. Has descubiert
ch-p4-03-v26 [es] ratio=3.43 | length ratio out of bounds | Ycuando incluso son los últimos, y más animales que hombres: entonces la plebe sube y sube de precio
ch-p4-03-v38 [es] ratio=3.14 | length ratio out of bounds | «¡Bien!, dijo, hacia allá sigue el camino, allá se encuentra la caverna de Zaratustra; ¡y este día d
ch-p4-04-v04 [fr] ratio=2.69 | length ratio out of bounds | Comme un voyageur qui rêve de choses lointaines, sur une route solitaire, se heurte par mégarde à un
ch-p4-05-v07 [es] ratio=8.32 | length ratio out of bounds | ¡En vano! ¡Sigue pinchando, Cruelísimo aguijón! No, No un perro - tu caza soy tan sólo, ¡Cruelísimo 
ch-p4-05-v10 [es] ratio=5.98 | length ratio out of bounds | ¿Cómo? ¿Dinero de rescate? ¿Cuánto dinero de rescate quieres? Pide mucho - ¡te lo aconseja mi segund
ch-p4-05-v37 [fr] ratio=6.96 | length ratio out of bounds | Mais, dis-moi, que cherches-tu ici dans mes forêts et parmi mes rochers. Et si c'est pour moi que tu
ch-p4-05-v38 [es] ratio=3.41 | length ratio out of bounds | Mas dime, ¿qué buscas tú aquí en mis bosques y entre mis rocas? Y cuando te colocaste en mi camino, 
ch-p4-06-v02 [fr] ratio=3.69 | length ratio out of bounds | Peu de temps cependant après que Zarathoustra se fut débarrassé de l'enchanteur, il vit de nouveau q
ch-p4-06-v02 [es] ratio=3.40 | length ratio out of bounds | No mucho después de haberse librado Zaratustra del mago vio de nuevo a alguien sentado junto al cami
ch-p4-06-v24 [es] ratio=4.43 | length ratio out of bounds | - mira, ¿no soy yo ahora, de nosotros dos, el más ateo? ¡Mas quién podría alegrarse de eso!» - - «Tú
ch-p4-06-v31 [es] ratio=2.56 | length ratio out of bounds | Él era un Dios escondido, lleno de secretos. En verdad, no supo procurarse un hijo más que por camin
ch-p4-07-v12 [fr] ratio=2.86 | length ratio out of bounds | Ainsi parlait Zarathoustra et il se disposait à passer son chemin: mais l'être innommable saisit un 
ch-p4-07-v18 [fr] ratio=3.74 | length ratio out of bounds | Les plus beaux succès ne furent-ils pas jusqu'ici pour ceux qui furent le mieux persécutés? Et celui
ch-p4-07-v20 [fr] ratio=2.60 | length ratio out of bounds | M'en veux-tu de ce que, depuis trop longtemps, j'écorche ainsi mes mots? De ce que déjà je te donne 
ch-p4-07-v20 [es] ratio=2.75 | length ratio out of bounds | ¿Estás irritado conmigo porque hace ya mucho tiempo que hablo y chapurreo? ¿De que yo te dé consejos
ch-p4-08-v10 [fr] ratio=2.71 | length ratio out of bounds | Et, en vérité, quand bien même l'homme gagnerait le monde entier, s'il n'apprenait pas cette seule c
ch-p4-08-v11 [es] ratio=2.61 | length ratio out of bounds | Y, en verdad, si el hombre conquistase el mundo entero y no aprendiese esa única cosa, el rumiar: ¡d
ch-p4-08-v26 [fr] ratio=3.04 | length ratio out of bounds | "Pourquoi me tentes-tu? Répondit celui-ci. Tu le sais encore mieux que moi. Qu'est-ce donc qui m'a p
ch-p4-08-v27 [es] ratio=3.42 | length ratio out of bounds | - ¿los forzados de la riqueza, que recogen su ganancia de todas las barreduras, con ojos fríos, con 
ch-p4-08-v33 [fr] ratio=3.27 | length ratio out of bounds | "Tu m'as bien deviné, répondit le mendiant volontaire, le coeur allégé. J'aime le miel, et je mâchon
ch-p4-09-v21 [es] ratio=2.55 | length ratio out of bounds | ¡Ay, dónde se me han ido todo el bien y toda la vergüenza y toda la fe en los buenos! ¡Ay, dónde se 
ch-p4-10-v15 [fr] ratio=2.55 | length ratio out of bounds | Ne chante pas, oiseau des prairies, ô mon âme! Ne murmure même pas! Regarde donc - silence! Le vieux
ch-p4-10-v16 [es] ratio=3.05 | length ratio out of bounds | ¡No cantes, ave de los prados, oh alma mía! ¡No susurres si-quiera! Mira - ¡silencio!, e l viejo med
ch-p4-11-v07 [fr] ratio=2.62 | length ratio out of bounds | Il me semble pourtant que vous vous entendez très mal, vos coeurs se rendent moroses les uns les aut
ch-p4-11-v20 [es] ratio=0.40 | length ratio out of bounds | Al pino comparo yo al que crece como tú, oh Zaratustra:
ch-p4-11-v22 [fr] ratio=3.86 | length ratio out of bounds | Je le compare à un pin, ô Zarathoustra, celui qui grandit comme toi: élancé, silencieux, dur, solita
ch-p4-11-v22 [es] ratio=3.23 | length ratio out of bounds | largo, silencioso, duro, solo, hecho de la mejor y más flexible leña, soberano, - - y, en fin, exten
ch-p4-11-v32 [fr] ratio=4.08 | length ratio out of bounds | Et que nous nous soyons venus vers ta caserne, nous autres hommes qui désespérions et qui déjà ne dé
ch-p4-11-v32 [es] ratio=2.58 | length ratio out of bounds | - pues también él está e n camino hacia ti, el último resto de Dios entre los hombres, es decir: tod
ch-p4-11-v36 [fr] ratio=2.74 | length ratio out of bounds | ("Allemand et clairement?" Que Dieu ait pitié! dit alors à part lui le roi de gauche; on voit qu'il 
ch-p4-11-v48 [fr] ratio=3.01 | length ratio out of bounds | Ce n'est pas vous que j'attends ici dans ces montagnes, ce n'est pas avec vous que je descendrai ver
ch-p4-11-v48 [es] ratio=2.73 | length ratio out of bounds | No es a vosotros a quienes aguardo yo aquí en estas montañas, no es con vosotros con quienes me es l
ch-p4-12-v17 [es] ratio=2.56 | length ratio out of bounds | Yo soy una ley únicamente para los míos, no soy una ley para todos. Mas quien me pertenece tiene que
ch-p4-13-v26 [es] ratio=2.52 | length ratio out of bounds | «El hombre es malvado» - así me dijeron, para consolarme, los más sabios. ¡Ay, si eso fuera hoy verd
ch-p4-13-v32 [fr] ratio=3.23 | length ratio out of bounds | Non! Non! Trois fois non! Il faut qu'il en périsse toujours plus et toujours des meilleurs de votre 
ch-p4-13-v32 [es] ratio=2.78 | length ratio out of bounds | ¡No! ¡No! ¡Tres veces no! Deben perecer cada vez más, cada vez mejores de vuestra especie, - pues vo
ch-p4-13-v100 [fr] ratio=2.64 | length ratio out of bounds | Il vaut mieux encore être fou de bonheur que fou de malheur, il vaut mieux danser lourdement que de 
ch-p4-13-v100 [es] ratio=2.76 | length ratio out of bounds | Pero es mejor estar loco de felicidad que estarlo de infelicidad, es mejor bailar torpemente que cam
ch-p4-13-v104 [fr] ratio=2.57 | length ratio out of bounds | Celui qui donne des ailes aux ânes et qui trait les lionnes, qu'il soit loué, cet esprit bon et indo
ch-p4-14-v12 [es] ratio=4.56 | length ratio out of bounds | Yo os conozco a vosotros, hombres superiores, yo lo conozco a él, - yo conozco también a ese espírit
ch-p4-14-v20 [es] ratio=3.43 | length ratio out of bounds | Así, De águila, de pantera Son los anhelos del poeta, Son tus anhelos bajo miles de máscaras, ¡Tú ne
ch-p4-14-v22 [es] ratio=0.21 | length ratio out of bounds | Entre rojos purpúreos:
ch-p4-15-v13 [fr] ratio=6.10 | length ratio out of bounds | Nous cherchons des choses différentes, là-haut aussi, vous et moi. Car moi je cherche plus de certit
ch-p4-15-v13 [es] ratio=5.49 | length ratio out of bounds | Buscamo$ también cosas distintas aquí arriba, vosotros y yo. Yo busco, en efecto, más seguridad, por
ch-p4-16-v04 [es] ratio=2.80 | length ratio out of bounds | Estos reyes, sin duda, siguen poniendo ante nosotros buena cara: ¡ esto es lo que ellos, en efecto, 
ch-p4-16-v05 [fr] ratio=3.36 | length ratio out of bounds | Il me semble pourtant que ces rois font bonne figure devant nous; car, parmi nous tous, ce sont eux 
ch-p4-16-v13 [fr] ratio=2.88 | length ratio out of bounds | Vous ne vous doutez pas combien elles étaient charmantes, lorsqu'elles ne dansaient pas, assises ave
ch-p4-16-v13 [es] ratio=2.52 | length ratio out of bounds | No podréis creer de qué modo tan gracioso se estaban sentadas, cuando no bailaban, profundas, pero s
ch-p4-16-v22 [en] ratio=3.69 | length ratio out of bounds | This the finest air drinking, With nostrils out-swelled like goblets, Lacking future, lacking rememb
ch-p4-16-v23 [es] ratio=0.24 | length ratio out of bounds | jRugir una vez más aún, Rugir moralmente! jComo león moral Rugir ante las hijas del desierto!
ch-p4-17-v22 [es] ratio=3.71 | length ratio out of bounds | ¡Amén! ¡Y alabanza y honor y sabiduría y gratitud y gloria y fortaleza a nuestro Dios por los siglos
ch-p4-18-v34 [fr] ratio=2.78 | length ratio out of bounds | Le coeur de chacun de vous tressaillait pourtant de joie et de méchanceté, parce que vous êtes enfin
ch-p4-18-v34 [es] ratio=2.52 | length ratio out of bounds | ¡Cómo se os agitaba, sin embargo, el corazón a cada uno de vosotros de placer y de maldad por habero
ch-p4-18-v37 [es] ratio=0.28 | length ratio out of bounds | remos el reino de la tierra.»
ch-p4-18-v40 [fr] ratio=2.91 | length ratio out of bounds | Et de nouveau Zarathoustra commença à parler. "O mes nouveaux amis, dit-il, - hommes singuliers, vou
ch-p4-18-v40 [es] ratio=3.02 | length ratio out of bounds | Yde nuevo comenzó Zaratustra a hablar. «¡Oh, mis nuevos amigos, dijo, - vosotros gente extraña, homb
ch-p4-19-v14 [fr] ratio=3.24 | length ratio out of bounds | O hommes supérieurs, il est près de minuit: je veux donc vous dire quelque chose à l'oreille, quelqu
ch-p4-19-v16 [fr] ratio=3.53 | length ratio out of bounds | Silence! Silence! On entend bien des choses qui n'osent pas se dire de jour; mais maintenant que l'a
ch-p4-19-v17 [fr] ratio=0.17 | length ratio out of bounds | O homme, prends garde!
ch-p4-19-v18 [es] ratio=0.35 | length ratio out of bounds | ¡Oh hombre, presta atención!
ch-p4-19-v21 [es] ratio=2.65 | length ratio out of bounds | Ya he muerto. Todo ha terminado. Araña, ¿por qué tejes tu tela a mi alrededor? ¿Quieres sangre? ¡Ay!
ch-p4-19-v22 [fr] ratio=5.47 | length ratio out of bounds | Déjà je suis mort. C'en est fait. Araignée, pourquoi tisses-tu ta toile autour de moi? Veux-tu du sa
ch-p4-19-v33 [fr] ratio=2.70 | length ratio out of bounds | Vieille cloche! Douce lyre! toutes les douleurs t'ont déchiré le coeur, la douleur du père, la doule
ch-p4-19-v33 [es] ratio=3.62 | length ratio out of bounds | ¡Vieja campana, dulce lira! Todo dolor te ha desgarrado el corazón, el dolor del padre, el dolor de 
ch-p4-19-v35 [fr] ratio=3.31 | length ratio out of bounds | - maintenant il veut mourir, mourir de bonheur. O hommes supérieurs, ne le sentez-vous pas? Secrètem
ch-p4-19-v42 [fr] ratio=3.35 | length ratio out of bounds | O monde, tu me veux? Suis-je mondain pour toi? Suis-je religieux? Suis-je devin pour toi? Mais jour 
ch-p4-19-v53 [es] ratio=3.41 | length ratio out of bounds | El dolor dice: «¡Pasa! ¡Fuera tú, dolor!» Mas todo lo que sufre quiere vivir, para volverse maduro y
ch-p4-19-v59 [es] ratio=2.61 | length ratio out of bounds | ¿Habéis dicho sí alguna vez a un solo placer? Oh amigos míos, entonces dijisteis sí también a todo d
ch-p4-19-v62 [fr] ratio=3.85 | length ratio out of bounds | Avez-vous jamais approuvé une joie? O mes amis, alors vous avez aussi approuvé toutes les douleurs. 
ch-p4-19-v65 [es] ratio=3.03 | length ratio out of bounds | más hambriento, más terrible, más misterioso que todo sufrimiento, se quiere a sí mismo, muerde el c
ch-p4-19-v68 [es] ratio=4.65 | length ratio out of bounds | Pues todo placer se quiere a sí mismo, ¡por eso quiere también sufrimiento! ¡Oh felicidad, oh dolor!
ch-p4-20-v03 [fr] ratio=5.45 | length ratio out of bounds | Toute joie veut l'éternité de toutes choses, elle veut du miel, du levain, une heure de minuit plein
ch-p4-20-v09 [fr] ratio=5.30 | length ratio out of bounds | Car toute joie se veut elle-même, c'est pourquoi elle veut la peine! O bonheur, ô douleur! Oh brise-
ch-p4-20-v13 [es] ratio=0.09 | length ratio out of bounds | Atodos ellos Zaratustra les dijo tan sólo una única frase:
ch-p4-20-v19 [es] ratio=2.72 | length ratio out of bounds | Oh vosotros hombres superiores, vuestra necesidad fue la que aquel viejo adivino me vaticinó ayer po

_Total length-ratio findings: 289_


## 3. Commentary mis-fits and audit-cache analysis
_Total notes in commentary.json: 461_

### 3a. Notes with audit score=0 still present in commentary.json (17)
ch-p4-01-v02 [klossowski] | audit_score=0 | The note provides biographical reflections on Nietzsche's adolescence and later thoughts on tragedy and the divine, which have no discernible connection to the verse's central theme of Zarathustra dis
ch-p1-03-v35 [sanchez-pascual-notes] | audit_score=0 | The note is a cross-reference to other parts of the text and does not illuminate the meaning, imagery, or specific words of this particular verse.
ch-p1-07-v15 [sanchez-pascual-notes] | audit_score=0 | The note provides a biblical reference that has no apparent connection to the content or themes of the verse (difficulty of life, pride, and resignation).
ch-p1-21-v31 [sanchez-pascual-notes] | audit_score=0 | The note discusses "the Hebrew Jesus" and "anachronism," concepts that have no textual basis or direct connection to any word, image, or idea present in this specific verse.
ch-p2-02-v26 [sanchez-pascual-notes] | audit_score=0 | The note discusses "Zarathustra's shadow," which is a distinct concept from "Willing emancipates" and the doctrine of will and freedom presented in the verse. There is no connection.
ch-p2-17-v44 [sanchez-pascual-notes] | audit_score=0 | The note is a cross-reference to another note and provides no direct illumination or commentary on the verse's content.
ch-p4-05-v20 [sanchez-pascual-notes] | audit_score=0 | The note discusses a linguistic play between *versuchen* and *suchen*, but neither of these words, nor any derivative, appears in the verse. Therefore, it does not illuminate any specific word, image,
ch-p4-06-v27 [sanchez-pascual-notes] | audit_score=0 | The note introduces the concept of a "hidden God," which is not mentioned or implied in the verse. The verse focuses on the pope's self-proclaimed enlightenment, not on a specific attribute of God.
ch-p4-06-v40 [sanchez-pascual-notes] | audit_score=0 | The commentary discusses "Töpfe und Geschöpfe" and a biblical allusion to man made from clay, but these words or the concept of creation from clay are not present in this specific verse.
ch-p4-13-v11 [sanchez-pascual-notes] | audit_score=0 | The note introduces the concept of an "inner animal" and related references (*The Gay Science*, Romans 7:22, Pauline man), claiming it is "mentioned here by Zarathustra." This concept is not present i
ch-p4-17-v11 [sanchez-pascual-notes] | audit_score=0 | The note is a cross-reference and does not illuminate the content of the verse itself.
ch-p4-18-v18 [sanchez-pascual-notes] | audit_score=0 | The note merely provides a page reference to another section of the book without offering any commentary or explanation related to the verse itself.
ch-p4-18-v18 [sanchez-pascual-notes] | audit_score=0 | The note merely provides a page reference to another section of the book without offering any commentary or explanation related to the verse itself.
ch-p4-20-v07 [sanchez-pascual-notes] | audit_score=0 | The note claims Zarathustra "claims for himself 'the obedient ear'," but this phrase ("das gehorchende Ohr") does not appear in the verse. The note's premise is therefore unfounded regarding this spec
ch-p3-06-v17 [new-cambridge] | audit_score=0 | The note discusses Wagner's philosophical evolution, specifically his learning from Feuerbach and his later "will to teach." This bears no plausible connection to the verse's inquiry about the origin 
ch-p2-22-v19 [sp-introduction] | audit_score=0 | The note is a general appraisal of *Thus Spoke Zarathustra* as a literary masterpiece, not an illumination of the specific verse about humility, heights, and valleys.
ch-p4-03-v03 [sp-introduction] | audit_score=0 | The note describes Nietzsche's personal experience and the genesis of a philosophical idea, which is unrelated to the king's commentary on a goat-herd or anchorite living among rocks and trees and the

### 3b. Notes with no audit.json entry (80)
ch-p1-07-v14 [klossowski] | NO_AUDIT
ch-p1-08-v13 [klossowski] | NO_AUDIT
ch-p1-18-v01 [klossowski] | NO_AUDIT
ch-p2-15-v39 [klossowski] | NO_AUDIT
ch-p2-16-v26 [klossowski] | NO_AUDIT
ch-p3-01-v05 [klossowski] | NO_AUDIT
ch-p3-08-v35 [klossowski] | NO_AUDIT
ch-p2-09-v21 [deleuze] | NO_AUDIT
ch-p2-10-v36 [sanchez-meca] | NO_AUDIT
ch-p2-07-v30 [sanchez-meca] | NO_AUDIT
ch-p1-05-v21 [sanchez-meca] | NO_AUDIT
ch-p1-06-v21 [sanchez-meca] | NO_AUDIT
ch-p1-08-v21 [sanchez-meca] | NO_AUDIT
ch-p1-09-v21 [sanchez-meca] | NO_AUDIT
ch-p1-14-v21 [sanchez-meca] | NO_AUDIT
ch-p1-14-v21 [sanchez-meca] | NO_AUDIT
ch-p1-16-v21 [sanchez-meca] | NO_AUDIT
ch-p1-17-v21 [sanchez-meca] | NO_AUDIT
ch-p1-18-v21 [sanchez-meca] | NO_AUDIT
ch-p2-05-v21 [sanchez-meca] | NO_AUDIT
ch-p2-09-v21 [sanchez-meca] | NO_AUDIT
ch-p2-10-v21 [sanchez-meca] | NO_AUDIT
ch-p2-11-v21 [sanchez-meca] | NO_AUDIT
ch-p2-16-v21 [sanchez-meca] | NO_AUDIT
ch-p2-19-v21 [sanchez-meca] | NO_AUDIT
ch-p2-21-v21 [sanchez-meca] | NO_AUDIT
ch-p3-06-v21 [sanchez-meca] | NO_AUDIT
ch-p3-09-v21 [sanchez-meca] | NO_AUDIT
ch-p3-15-v21 [sanchez-meca] | NO_AUDIT
ch-p4-02-v21 [sanchez-meca] | NO_AUDIT
ch-p4-08-v21 [sanchez-meca] | NO_AUDIT
ch-p4-09-v21 [sanchez-meca] | NO_AUDIT
ch-p4-10-v21 [sanchez-meca] | NO_AUDIT
ch-p4-10-v21 [sanchez-meca] | NO_AUDIT
ch-p4-11-v21 [sanchez-meca] | NO_AUDIT
ch-p4-16-v21 [sanchez-meca] | NO_AUDIT
ch-p1-19-v02 [sanchez-pascual-notes] | NO_AUDIT
ch-p1-02-v34 [sanchez-pascual-notes] | NO_AUDIT
ch-p1-07-v08 [sanchez-pascual-notes] | NO_AUDIT
ch-p1-08-v26 [sanchez-pascual-notes] | NO_AUDIT
ch-p1-08-v12 [sanchez-pascual-notes] | NO_AUDIT
ch-p1-13-v03 [sanchez-pascual-notes] | NO_AUDIT
ch-p1-14-v27 [sanchez-pascual-notes] | NO_AUDIT
ch-p1-15-v21 [sanchez-pascual-notes] | NO_AUDIT
ch-p1-20-v10 [sanchez-pascual-notes] | NO_AUDIT
ch-p2-01-v03 [sanchez-pascual-notes] | NO_AUDIT
ch-p2-04-v31 [sanchez-pascual-notes] | NO_AUDIT
ch-p2-08-v39 [sanchez-pascual-notes] | NO_AUDIT
ch-p2-16-v25 [sanchez-pascual-notes] | NO_AUDIT
ch-p2-16-v24 [sanchez-pascual-notes] | NO_AUDIT
ch-p2-18-v02 [sanchez-pascual-notes] | NO_AUDIT
ch-p2-18-v36 [sanchez-pascual-notes] | NO_AUDIT
ch-p2-18-v10 [sanchez-pascual-notes] | NO_AUDIT
ch-p2-19-v46 [sanchez-pascual-notes] | NO_AUDIT
ch-p2-20-v06 [sanchez-pascual-notes] | NO_AUDIT
ch-p2-21-v42 [sanchez-pascual-notes] | NO_AUDIT
ch-p2-21-v42 [sanchez-pascual-notes] | NO_AUDIT
ch-p3-03-v11 [sanchez-pascual-notes] | NO_AUDIT
ch-p3-04-v29 [sanchez-pascual-notes] | NO_AUDIT
ch-p3-07-v01 [sanchez-pascual-notes] | NO_AUDIT
ch-p3-09-v05 [sanchez-pascual-notes] | NO_AUDIT
ch-p3-14-v28 [sanchez-pascual-notes] | NO_AUDIT
ch-p3-15-v36 [sanchez-pascual-notes] | NO_AUDIT
ch-p4-01-v25 [sanchez-pascual-notes] | NO_AUDIT
ch-p4-02-v10 [sanchez-pascual-notes] | NO_AUDIT
ch-p4-05-v11 [sanchez-pascual-notes] | NO_AUDIT
ch-p4-07-v29 [sanchez-pascual-notes] | NO_AUDIT
ch-p4-13-v46 [sanchez-pascual-notes] | NO_AUDIT
ch-p4-18-v26 [sanchez-pascual-notes] | NO_AUDIT
ch-p4-19-v07 [sanchez-pascual-notes] | NO_AUDIT
ch-p1-19-v01 [new-cambridge] | NO_AUDIT
ch-p2-03-v36 [new-cambridge] | NO_AUDIT
ch-p2-04-v32 [new-cambridge] | NO_AUDIT
ch-p2-05-v30 [new-cambridge] | NO_AUDIT
ch-p2-14-v22 [new-cambridge] | NO_AUDIT
ch-p2-15-v15 [new-cambridge] | NO_AUDIT
ch-p2-18-v05 [new-cambridge] | NO_AUDIT
ch-p4-12-v20 [new-cambridge] | NO_AUDIT
ch-p4-15-v19 [new-cambridge] | NO_AUDIT
ch-p1-02-v32 [sp-introduction] | NO_AUDIT


## 4. Weak attributions (_audit_flag=weak): 140

### 4a. Per-chapter count of weak notes
- ch-p0-00: 2 weak notes
- ch-p1-01: 1 weak notes
- ch-p1-02: 1 weak notes
- ch-p1-04: 1 weak notes
- ch-p1-05: 4 weak notes
- ch-p1-06: 1 weak notes
- ch-p1-07: 4 weak notes
- ch-p1-08: 3 weak notes
- ch-p1-09: 1 weak notes
- ch-p1-11: 2 weak notes
- ch-p1-12: 1 weak notes
- ch-p1-13: 1 weak notes
- ch-p1-14: 3 weak notes
- ch-p1-15: 4 weak notes
- ch-p1-16: 1 weak notes
- ch-p1-17: 2 weak notes
- ch-p1-18: 1 weak notes
- ch-p1-19: 2 weak notes
- ch-p1-20: 2 weak notes
- ch-p1-21: 1 weak notes
- ch-p1-22: 3 weak notes
- ch-p2-01: 1 weak notes
- ch-p2-02: 1 weak notes
- ch-p2-03: 1 weak notes
- ch-p2-04: 2 weak notes
- ch-p2-05: 1 weak notes
- ch-p2-07: 1 weak notes
- ch-p2-09: 2 weak notes
- ch-p2-10: 2 weak notes
- ch-p2-11: 2 weak notes
- ch-p2-12: 4 weak notes
- ch-p2-14: 1 weak notes
- ch-p2-15: 1 weak notes
- ch-p2-16: 3 weak notes
- ch-p2-18: 2 weak notes
- ch-p2-19: 2 weak notes
- ch-p2-20: 1 weak notes
- ch-p2-21: 3 weak notes
- ch-p2-22: 1 weak notes
- ch-p3-01: 2 weak notes
- ch-p3-03: 2 weak notes
- ch-p3-04: 2 weak notes
- ch-p3-06: 2 weak notes
- ch-p3-07: 2 weak notes
- ch-p3-08: 2 weak notes
- ch-p3-09: 2 weak notes
- ch-p3-10: 1 weak notes
- ch-p3-12: 1 weak notes
- ch-p3-13: 2 weak notes
- ch-p3-14: 2 weak notes
- ch-p3-15: 1 weak notes
- ch-p3-16: 3 weak notes
- ch-p4-01: 1 weak notes
- ch-p4-02: 2 weak notes
- ch-p4-03: 2 weak notes
- ch-p4-04: 5 weak notes
- ch-p4-05: 3 weak notes
- ch-p4-07: 3 weak notes
- ch-p4-08: 1 weak notes
- ch-p4-09: 2 weak notes
- ch-p4-10: 3 weak notes
- ch-p4-11: 3 weak notes
- ch-p4-12: 2 weak notes
- ch-p4-13: 1 weak notes
- ch-p4-15: 2 weak notes
- ch-p4-16: 1 weak notes
- ch-p4-17: 3 weak notes
- ch-p4-18: 3 weak notes
- ch-p4-19: 4 weak notes
- ch-p4-20: 3 weak notes

### 4b. audit.json score=1 entries (loose fit): 167
- klossowski: 39
- sanchez-pascual-notes: 36
- new-cambridge: 32
- deleuze: 31
- sanchez-meca: 15
- sp-introduction: 12
- lampert: 2

### 4c. All weak notes (full list)
ch-p0-00-v02 [lampert] | weak | The note identifies this verse's address to the sun as the first in a series that frames the work, which is a structural observation, but it does not engage with the specific content or unique ideas o
ch-p0-00-v12 [lampert] | weak | The commentary discusses the role of the entire Vorrede §1 as a prelude to the work's broader narrative arc, rather than illuminating the specific meaning or function of this concluding verse itself.
ch-p1-05-v21 [klossowski] | weak | The commentary discusses general Nietzschean themes of "Wills to Power" and the "plurality of impulses/passions" as "fictitious units." While this could be broadly related to virtues, it does not spec
ch-p1-15-v14 [klossowski] | weak | The note discusses the general genesis of images, words, and concepts, which is a broader philosophical topic. It does not engage with the specific ideas of "values" (Werthe), "human significance" (Me
ch-p1-15-v14 [klossowski] | weak | The note offers a broad interpretation of Nietzsche's view on humanity, individuality, and his "artistic" perspective, drawing on general Nietzschean themes like "individual achievements" and "soverei
ch-p1-20-v08 [klossowski] | weak | The note discusses the dynamics of "impulses" and their "rhythm," which has thematic resonance with "first movement" or "rolling wheel," but it does not directly engage the verse's specific call to *c
ch-p1-22-v56 [klossowski] | weak | The note immediately jumps to "Eternal Recurrence," a broader Nietzschean theme, interpreting "return" in the verse. However, it fails to engage with the specific conditions of this return ("when ye h
ch-p2-04-v32 [klossowski] | weak | The note discusses "teaching and learning" broadly but fails to engage with the verse's specific imagery of "fire" and the contrast between external proof and the internal origin ("one's own burning")
ch-p2-07-v30 [klossowski] | weak | The note discusses "ressentiment," the "rabble," and the "debasement" of "selection" and "privilege," which touches upon general Nietzschean themes of values and social hierarchies (as mentioned in "G
ch-p2-11-v19 [klossowski] | weak | The note delves into abstract concepts of "God" as a "maximum-state" or "evolution of the Will to Power" and "eternal circular movement." While these are core Nietzschean ideas, they do not specifical
ch-p2-12-v23 [klossowski] | weak | The note discusses general societal power dynamics and historical movements, touching on "power" which is in the verse. However, it does not engage with the specific imagery or mechanism of "surrender
ch-p2-12-v23 [klossowski] | weak | The note is a dense philosophical discussion connecting "power" and "life" to "will to power," "eternal return," and theories of energy and biology. While these are broad Nietzschean themes and "power
ch-p2-18-v02 [klossowski] | weak | The note takes "es ist Zeit!" as a general starting point for discussing Nietzsche's broader themes of time, interpretation, and language, rather than engaging with the specific narrative context of t
ch-p3-03-v17 [klossowski] | weak | The note, a personal reflection from Nietzsche, discusses struggles with pain, the need for solitude for "sublime impulses," and recovery. While this provides a general biographical context for Nietzs
ch-p3-04-v29 [klossowski] | weak | The commentary addresses a broader Nietzschean theme of critiquing traditional values as weakness, which aligns generally with Zarathustra's rejection of "rationality" and 'a Will'. However, it does n
ch-p3-06-v33 [klossowski] | weak | The commentary discusses broader themes of self-sovereignty and rejection of societal forms, which are general Nietzschean themes. It does not engage with the specific idea of embracing "Zufall" (chan
ch-p3-10-v48 [klossowski] | weak | The note discusses general Nietzschean concepts like the Will to Power, sickness/health, and purpose, which are broadly relevant to Zarathustra's critique of morality. However, it does not engage with
ch-p3-12-v08 [klossowski] | weak | The note briefly touches on "giving sense and purpose to existence" and "transvaluation of values" which are broadly related to the verse's theme of creating good and bad. However, it quickly pivots t
ch-p3-14-v12 [klossowski] | weak | The note is a poetic passage evoking joy, friendship, and nature. While it shares a general poetic tone with the verse, it does not engage with the verse's specific imagery of the soul being nurtured 
ch-p4-04-v21 [klossowski] | weak | The note discusses broad Nietzschean themes like ethics, "great men," and human achievement, but does not engage with the specific epistemological concepts of "a handbreadth of basis" or "nothing grea
ch-p4-12-v17 [klossowski] | weak | The commentary discusses Nietzsche's personal health experiences, using the word "healthy" which is present in the verse ("gesund und heil"). However, it provides biographical context rather than illu
ch-p4-15-v16 [klossowski] | weak | The commentary discusses general themes of illness, force, and spirit's attempts, which are too broad to specifically illuminate the verse's core ideas of "fear" as the origin of "original sin, origin
ch-p4-19-v07 [klossowski] | weak | The note discusses semiological language of affects and philosophers' impulses in a general, theoretical way. While the verse describes strong emotional reactions (laughter, tears, dancing, transforma
ch-p4-20-v14 [klossowski] | weak | The note's concepts of "centrifugal forces" and "circular movement" around a "center" might broadly relate to themes in Zarathustra, but they do not directly illuminate the specific actions or imagery
ch-p4-01-v02 [klossowski] | weak | The commentary discusses general themes of growth and maturation in Nietzsche's life and thought. While "ripening" is a theme in the verse, the commentary does not engage with the specific imagery of 
ch-p1-07-v14 [klossowski] | weak | The commentary introduces "will to power" and the idea of philosophers as "impostors/embellishers," which are broader Nietzschean themes. However, it does not directly engage with the specific imagery
ch-p1-08-v13 [klossowski] | weak | The note discusses general themes of internal struggle ("véhémence de mes oscillations intérieures"), the arduousness of a journey ("passim dans laquelle ma vie se trouve engagée"), and the reception 
ch-p2-15-v39 [klossowski] | weak | The commentary discusses general Nietzschean themes like will to power, eternal recurrence, forgetting, loss of identity, and the death of God. While these are central to *Zarathustra*, they do not en
ch-p2-16-v26 [klossowski] | weak | The commentary discusses general Nietzschean themes like will to power, eternal recurrence, forgetting, loss of identity, and the death of God. While these are central to *Zarathustra*, they do not en
ch-p3-01-v05 [klossowski] | weak | The note discusses the concept of Eternal Return and the individual self, which is a broader theme in Zarathustra. However, it does not engage with the specific imagery of "wandering" (Wandern) and "m
ch-p1-01-v22 [deleuze] | weak | The note discusses general Nietzschean themes related to the critique of Christianity, the death of God, and reactive forces. While these are broadly related to the verse's theme of challenging "Thou 
ch-p1-05-v25 [deleuze] | weak | The note offers broad Nietzschean concepts (e.g., 'Man is reactive becoming', 'higher man') that relate to general themes of overcoming man, but it does not engage with the specific paradoxical instru
ch-p1-12-v08 [deleuze] | weak | The note offers very general Nietzschean philosophical themes ("Pluralism," "religion," "reactive forces," "nihilism") which do not specifically engage with the verse's unique imagery or precise descr
ch-p1-15-v14 [deleuze] | weak | The verse explicitly discusses man assigning "values" (Werte), creating "significance" (Sinn), and being the "valuator" (der Schätzende). The note, while related to Nietzsche's broader themes of human
ch-p1-20-v05 [deleuze] | weak | The verse speaks of "victory and freedom long[ing] for a child" and building "living monuments." The commentary references "betrothal and the nuptial ring." While marriage can lead to children, the no
ch-p2-02-v09 [deleuze] | weak | The note discusses broader Nietzschean themes like the ascetic ideal, knowledge, morality, and religion, and values "superior to life." While these are generally related to Nietzsche's philosophy, the
ch-p2-12-v34 [deleuze] | weak | The note discusses "affirming life" and art, which is a broad Nietzschean theme, but it does not engage with the specific distinction made in the verse between "Will to Life" and "Will to Power."
ch-p2-14-v03 [deleuze] | weak | The note identifies a chapter, "On the Land of Culture," which shares a key phrase with the verse ("land of culture"). However, it then explains the *themes* of that chapter ("the burden and the deser
ch-p3-04-v29 [deleuze] | weak | The note lists broad philosophical concepts (sense, force, pluralism, interpretation, higher degrees) that relate to Nietzsche's overall thought and might broadly connect to a critique of rationality,
ch-p3-13-v37 [deleuze] | weak | The note about "the best of your kind must perish" touches upon a general theme of destruction but does not directly illuminate the specific paradoxical claims of the verse, such as "all that is badde
ch-p3-16-v51 [deleuze] | weak | The verse states that God died specifically from "pity for humankind." While the note discusses the broader theme of "the death of God" and its connection to reactive nihilism and reactive man, it doe
ch-p4-03-v04 [deleuze] | weak | The note correctly identifies the chapter and speaker but then introduces an image ("long ears of the rabble") from a different chapter ("On the Higher Man") that does not illuminate the specific disc
ch-p4-04-v01 [deleuze] | weak | The note discusses broader themes and specific events from other parts of Zarathustra related to "the demon" or "spirit of gravity" and overcoming. It does not engage with the specific imagery of Zara
ch-p4-04-v18 [deleuze] | weak | The note provides a thematic parallel from *Untimely Meditations* regarding private vs. public thinkers. While potentially related to the character's type, it does not engage with the specific phrasin
ch-p4-05-v17 [deleuze] | weak | The note's discussion of "appearance" as "repeated reality" is a tenuous and abstract connection to Zarathustra's accusation of "stage-player from the heart" and being "false." The subsequent discussi
ch-p4-09-v28 [deleuze] | weak | The note lists general Nietzschean philosophical concepts ("eternal recurrence," "Heraclitus," "becoming"), some of which use the word "eternal" (ewiges) as does the verse. However, the note does not 
ch-p4-19-v21 [deleuze] | weak | The verse asks "Who hath sufficient courage for it?" while the note introduces the broader concept of "Wille zur Macht" (Will to Power). While courage can be related to will, the note doesn't specific
ch-p4-20-v14 [deleuze] | weak | The note extensively discusses the abstract concept of "the higher man" and Nietzsche's critique, and quotes a "cry" that is not in this verse. Although the verse mentions "the higher men," the note d
ch-p1-11-v20 [deleuze] | weak | The note discusses the self-destruction of "justice," which is a broader Nietzschean theme. While the verse describes the State as leading to the "slow suicide of all" and thus shares a theme of self-
ch-p2-09-v21 [deleuze] | weak | The note discusses major Nietzschean themes (eternal recurrence, nihilism, transmutation of the negative, reactive forces) which are central to *Also sprach Zarathustra* as a whole. However, it does n
ch-p3-16-v51 [sanchez-meca] | weak | The verse focuses on the "follies of the pitiful" and connects pity to suffering and the death of God. The note provides general Nietzschean references and quotes from BGE that discuss passions, cultu
ch-p4-07-v04 [sanchez-meca] | weak | The note discusses Nietzsche's challenging thought and his aim to hold a "mirror" to the reader, questioning modern man's satisfaction. While one could *very loosely* interpret Zarathustra's "black me
ch-p1-19-v01 [sanchez-meca] | weak | While the note uses the central imagery of "serpent" and "bite," it explicitly refers to a different scene ("when the shepherd bites and spits it out," "Thought is only such a bite") and its interpret
ch-p2-10-v36 [sanchez-meca] | weak | The note discusses Dionysianism, music, and tragedy, which are general Nietzschean themes that might broadly relate to "dance" in the verse. However, it entirely misses the core concept of the verse: 
ch-p1-05-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p1-06-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p1-08-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p1-09-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p1-14-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p1-14-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p1-16-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p1-17-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p1-18-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p2-05-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p2-09-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p2-10-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p2-11-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p2-16-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p2-19-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p2-21-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p3-06-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p3-09-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p3-15-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p4-02-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p4-08-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p4-09-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p4-10-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p4-10-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p4-11-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p4-16-v21 [sanchez-meca] | weak | The note discusses general Nietzschean themes like the sublimation of instincts, the will to power, and the interplay between spirit and force. While these concepts are broadly relevant to Zarathustra
ch-p1-04-v09 [sanchez-pascual-notes] | weak | The note refers to a passage in *Beyond Good and Evil* that discusses self-despising and self-valuation. This does not plausibly illuminate the specific content of the given verse, which describes the
ch-p1-07-v23 [sanchez-pascual-notes] | weak | The note introduces "God is spirit" and a later criticism of it. While the verse uses the word "spirit" ("Geist der Schwere"), the note's reference does not directly illuminate the specific concept of
ch-p1-07-v21 [sanchez-pascual-notes] | weak | The note provides structural information, stating that this verse (along with preceding paragraphs) functions as a motto for the third part of the work. While this highlights the verse's importance in
ch-p1-07-v21 [sanchez-pascual-notes] | weak | The note refers to a future event where a "teaching" from this verse will be recalled, engaging with the verse's content in a meta-narrative way, but it does not illuminate the specific words, images,
ch-p1-08-v12 [sanchez-pascual-notes] | weak | The note refers to other sections where "this same thought" (presumably the need for purification or spiritual development) is developed. This is a broader thematic connection rather than an engagemen
ch-p1-13-v03 [sanchez-pascual-notes] | weak | The note refers to a biblical passage on chastity, but the specific nuance of Nietzsche's verse—warning *against* chastity if difficult because it leads to "filth and lust of soul"—is not illuminated 
ch-p1-14-v27 [sanchez-pascual-notes] | weak | The note makes a very broad claim about condensing Greek doctrine on friendship, which does not plausibly illuminate the *specific* and gendered characteristics ("injustice and blindness," "surprise a
ch-p1-15-v12 [sanchez-pascual-notes] | weak | The note identifies "another people" as the Jewish people and cites Exodus 20:12 regarding honoring parents. While this relates to fidelity, it does not specifically illuminate the verse's unique phra
ch-p1-17-v20 [sanchez-pascual-notes] | weak | The note is a mere cross-reference to another section of the work. It does not provide any commentary or engagement with the specific content or meaning of this verse.
ch-p1-21-v31 [sanchez-pascual-notes] | weak | While the verse mentions "death," the note introduces the concept of "the sting of death," which is not present in this specific verse. It then contrasts this with "the sting of freedom" from a differ
ch-p1-22-v29 [sanchez-pascual-notes] | weak | The note claims a "paraphrase, reversing the meaning" of a biblical verse but does not engage with specific words, images, or ideas unique to *this verse* to demonstrate how such a reversal is perform
ch-p2-01-v34 [sanchez-pascual-notes] | weak | The note discusses the broader theme of "wild wisdom" associated with Zarathustra's character throughout the book, rather than illuminating the specific, titular phrase "Also sprach Zarathustra" in th
ch-p2-12-v10 [sanchez-pascual-notes] | weak | The allusion to *The Ship of Fools* is very general and does not specifically illuminate the unique elements or the core message of the verse, particularly the contrast between the river and the Will 
ch-p2-16-v25 [sanchez-pascual-notes] | weak | The note is a cross-reference to a broader theme ("On the Virtuous") but does not engage with the specific metaphor of "clockworks," their winding, or their "modest noise" used in *this* verse.
ch-p2-19-v46 [sanchez-pascual-notes] | weak | The note discusses the identification of a "soothsayer" with real-world figures (Schopenhauer, Dühring), but the given verse does not mention a "soothsayer" and instead focuses on the effect of "laugh
ch-p2-21-v42 [sanchez-pascual-notes] | weak | The note only cross-references the phrase "first sagacity concerning men" without illuminating the content or meaning of the specific prudence described in this verse (allowing oneself to be deceived)
ch-p2-21-v42 [sanchez-pascual-notes] | weak | The note only cross-references the repetition of the reproach "Why still rattle, ye rattle-snakes?" without illuminating its specific meaning or context within this particular verse.
ch-p3-03-v11 [sanchez-pascual-notes] | weak | The verse mentions finding friends in the afternoon, at the hour when light becomes stiller. The commentary simply provides cross-references to other chapters ("Of the Tree on the Mountain" and "Of th
ch-p3-07-v01 [sanchez-pascual-notes] | weak | The note points to a "similar scene" involving Jesus and Jerusalem in Luke, which is a general thematic parallel (prophet/figure encountering a city). However, it does not illuminate the specific warn
ch-p3-08-v14 [sanchez-pascual-notes] | weak | The note refers to specific characters and events from a different section of the book. While these events relate to Zarathustra's broader journey of leaving behind old forms, the note does not explic
ch-p3-08-v32 [sanchez-pascual-notes] | weak | The note alludes to Matthew 18:3, which speaks of becoming like children to enter heaven. While both the verse and the note mention "children" and implicitly a divine "father," the note does not illum
ch-p3-09-v05 [sanchez-pascual-notes] | weak | The note provides general cross-references to other sections of the book where similar themes might appear but does not engage with any specific word, image, or idea unique to this particular verse.
ch-p3-13-v23 [sanchez-pascual-notes] | weak | The note refers to a different specific section of the work (tightrope walker), providing a general thematic connection to Zarathustra's philosophy but not directly illuminating the specific imagery o
ch-p3-14-v28 [sanchez-pascual-notes] | weak | The commentary introduces a complex interpretation involving Dionysus, Ariadne, vines, and pruning hooks, and alludes to Revelation. However, none of these specific images or direct allusions are pres
ch-p4-02-v10 [sanchez-pascual-notes] | weak | The note merely points to a chapter titled "The Soothsayer," which is the character in the verse. It does not illuminate any specific dialogue, imagery, or unique idea present in this particular verse
ch-p4-04-v18 [sanchez-pascual-notes] | weak | The note is a general cross-reference and does not engage with the specific words, images, or ideas present in this verse.
ch-p4-05-v11 [sanchez-pascual-notes] | weak | Similar to pair [1], this is a general cross-reference and offers no specific illumination of the rich imagery ("peacock of peacocks," "sea of vanity," "evil magician") or concepts in this particular 
ch-p4-07-v10 [sanchez-pascual-notes] | weak | The note refers to a broader theme of "God as witness" in Nietzsche's work, but does not deeply engage with the specific psychological dynamic of the ugliest man's inability to endure being seen and h
ch-p4-13-v56 [sanchez-pascual-notes] | weak | The note connects to the work's subtitle, which hints at a broader theme of Zarathustra's audience and his critique of common morality versus self-seeking. This theme is present in the verse, but the 
ch-p4-17-v11 [sanchez-pascual-notes] | weak | The note provides a cross-reference to other sections of the work but does not engage with or explain the specific words, images, or ideas present in this particular verse (e.g., "virile food," "flatu
ch-p4-17-v02 [sanchez-pascual-notes] | weak | The note discusses the beginning of a narrative section ("The Feast of the Ass"), which provides broader context but does not specifically engage with or illuminate the unique words or ideas ("distres
ch-p4-18-v18 [sanchez-pascual-notes] | weak | The note refers to a general biblical concept (God's eternality) but does not specifically engage with the verse's unique phrasing regarding God appearing "most worthy of belief in this form" or the s
ch-p4-18-v26 [sanchez-pascual-notes] | weak | The note is a cross-reference to an earlier section. It does not engage with the specific commands or ideas in this verse, only points to a broader theme or event.
ch-p4-19-v02 [sanchez-pascual-notes] | weak | The note is a cross-reference to an earlier section. It does not illuminate the specific event described in this verse – the Ugliest Man's unique and moving utterance.
ch-p4-19-v57 [sanchez-pascual-notes] | weak | The note is a cross-reference to another chapter. It does not engage with the specific paradoxical statements or the concluding command and warning in this particular verse.
ch-p2-20-v06 [new-cambridge] | weak | The note discusses the general human instinct for self-preservation, which is a broad theme but does not engage with the specific imagery of the "big ear," "envious face," or "bloated soul" unique to 
ch-p4-04-v01 [new-cambridge] | weak | The note discusses Nietzsche's general philosophical project, pessimism, and the themes of *The Birth of Tragedy*, without engaging with the specific narrative of Zarathustra accidentally stepping on 
ch-p4-05-v01 [new-cambridge] | weak | The note discusses Schopenhauer's philosophical perspectives and general Nietzschean themes from *The Birth of Tragedy*, mentioning "in the voice of Zarathustra" generally. However, it does not engage
ch-p4-07-v04 [new-cambridge] | weak | The note discusses the Schopenhauerian theme of cosmic insignificance and feeling reduced to nothing, which can broadly relate to existential dread or a feeling of being overwhelmed, potentially conne
ch-p4-11-v01 [new-cambridge] | weak | The note discusses Nietzsche's own reading and perception of *Also sprach Zarathustra* as a whole work, but it does not engage with the specific content of this verse, which describes Zarathustra hear
ch-p4-11-v01 [new-cambridge] | weak | The commentary provides a general introduction to *Also sprach Zarathustra* as a work, discussing its significance and Nietzsche's view of it. It does not engage with the specific events or imagery de
ch-p4-17-v20 [new-cambridge] | weak | The note discusses how ancient Greeks explained "disturbance in the head" or "atrocity" by attributing it to gods. While the verse calls the higher men "toll" (mad/crazy), the note offers a general, e
ch-p4-18-v28 [new-cambridge] | weak | The commentary raises general philosophical questions pertinent to Nietzsche's work, but it does not engage with the specific question or terms ("HE," "liveth," "dead") presented in this particular ve
ch-p1-05-v04 [new-cambridge] | weak | The verse speaks of the ineffable and nameless quality of an inner experience of 'pain and sweetness' and 'hunger of the bowels'. The note discusses the sublimation of 'joy in cruelty' and adorning it
ch-p1-11-v13 [new-cambridge] | weak | The note addresses "perversity of the mind" and the "antichrist," which broadly aligns with the "monster" claiming divine authority. However, the specific error critiqued in the note (world having onl
ch-p1-22-v29 [new-cambridge] | weak | The note introduces the concept of 'da capo' (eternal recurrence), which relates to affirming one's life in general. While the verse also mentions "life," its specific focus is on bringing "flown-away
ch-p3-16-v40 [new-cambridge] | weak | The note explains the "will to power" as a fundamental philosophical concept. While "will to power" is a core Nietzschean theme that could underpin Zarathustra's ultimate goal, the note does not engag
ch-p4-10-v01 [new-cambridge] | weak | The note discusses ressentiment and noble/slave morality, a broad Nietzschean theme relevant to *Zarathustra* generally, but it does not engage with any specific words, images, or actions described in
ch-p4-20-v14 [new-cambridge] | weak | The commentary discusses broader Nietzschean themes like truthfulness, vanity, and "homo natura," which might relate to the overall context of *Zarathustra* or the "higher men" generally. However, it 
ch-p1-19-v01 [new-cambridge] | weak | The commentary discusses general themes of Zarathustra's "teachings" and the "overman" concept, which are broad themes of the work, but it does not engage with the specific narrative of the snake bite
ch-p2-03-v36 [new-cambridge] | weak | The note introduces "will to power," which is a broad theme in Nietzsche's work, including *Zarathustra*. However, it does not engage with the specific imagery or paradoxical statement of the verse ab
ch-p2-04-v32 [new-cambridge] | weak | The note discusses Nietzsche's general views on truth and truthfulness, referencing 'Truth and Lying,' which is a broad theme. The verse, however, focuses on the origin and authenticity of a "Lehre" (
ch-p2-18-v05 [new-cambridge] | weak | The note discusses Nietzsche's critique of the "will as cause" and the "inner world" being full of phantoms. The verse describes the disciples' internal "Besorgniss und Sehnsucht" (worry and longing).
ch-p3-07-v01 [new-cambridge] | weak | The note provides general background information about *Thus Spoke Zarathustra* and its main character, Zarathustra, but does not engage with any specific details, events, or characters (like the "foa
ch-p4-12-v20 [new-cambridge] | weak | The note discusses Nietzsche's own self-perception of cleverness from *Ecce Homo*. While the verse mentions a "wise man" being "clever" and "not an ass," the note does not engage with the specific wor
ch-p4-15-v19 [new-cambridge] | weak | The note quotes from *The Birth of Tragedy* and discusses Silenic wisdom, which is a broader Nietzschean theme about the nature of existence and suffering, linked by the shared motif of "laughter." Ho
ch-p3-01-v01 [sp-introduction] | weak | The note describes Nietzsche's biographical circumstances, including his climbs in Rapallo. While the verse also features Zarathustra climbing a mountain and recalling past wandering, the note does no
ch-p2-22-v19 [sp-introduction] | weak | The note discusses the meta-textual importance and literary value of *Also sprach Zarathustra* as a whole work, quoting Nietzsche's self-assessment. It does not engage with the specific content, emoti
ch-p4-03-v03 [sp-introduction] | weak | The note describes Nietzsche's personal experience of inspiration near a specific rock, relating to the genesis of *Also sprach Zarathustra* as a whole. It does not engage with the specific content of
ch-p1-02-v32 [sp-introduction] | weak | The verse critiques the "wise men of the professorial chairs" whose wisdom is "sleep without dreams." The note speaks from the perspective of "us" as "masters of the greatest doctrine." While it doesn


## 5. Render artifacts in note bodies
ch-p4-20-v14 [klossowski] [es] | very long (1505 chars) :: No fue el entendimiento lo que superó las fuerzas centrífugas para comunicarlas; estas fuerzas mismas se comunicaron un día, en Sils-Maria, bajo la fo
ch-p4-09-v16 [sanchez-pascual-notes] [en] | very long (2361 chars) :: «With you I have yearned for everything forbidden»: Zarathustra's "shadow" applies to itself Ovid's formula (Amores 3, 4, 17): *nitimur in vetitum*, w
ch-p4-09-v16 [sanchez-pascual-notes] [fr] | very long (2476 chars) :: «Avec toi j'ai aspiré à tout l'interdit»: l'«ombre» de Zarathoustra s'applique à elle-même la formule d'Ovide (3 *Amours*, 4, 17): *nitimur in vetitum
ch-p4-09-v16 [sanchez-pascual-notes] [es] | very long (2381 chars) :: «Contigo he aspirado a todo lo prohibido»: la «sombra» de Zaratustra se aplica a sí misma la fórmula de Ovidio (3 Amores, 4, 1 7): nitimur n i vetitum
ch-p4-18-v26 [sanchez-pascual-notes] [fr] | very short (29 chars) :: Voir ci-dessus, L'éveil, § 1.
ch-p3-02-v01 [new-cambridge] [fr] | very long (1677 chars) :: La Deuxième partie se poursuit avec des observations critiques sur divers types – entre autres, les « poètes » (« Des poètes »), les « prêtres » (« De
ch-p3-02-v01 [new-cambridge] [es] | very long (1574 chars) :: parte ii La Parte II continúa con observaciones críticas sobre varios tipos –entre otros, ‘poetas’ (‘De los poetas’), ‘sacerdotes’ (‘De los sacerdotes
ch-p1-01-v22 [new-cambridge] [fr] | very long (1572 chars) :: alors nous trouverons comme le fruit le plus mûr sur son arbre l'individu souverain, l'individu ne ressemblant qu'à lui-même, à nouveau libre de la mo
ch-p1-01-v22 [new-cambridge] [es] | very long (1586 chars) :: entonces encontraremos como el fruto más maduro en su árbol al individuo soberano, el individuo que se asemeja solo a sí mismo, libre de nuevo de la m
ch-p1-19-v01 [new-cambridge] [fr] | very long (1555 chars) :: notes 1. Zarathoustra ne présente pas de grandes « doctrines », même si c'est ainsi que l'œuvre a le plus souvent été lue (Stegmaier 2000: 204–5). Nie

_Total render-artifact findings: 10_


## 6. Functionality smoke tests

### Top pages
- https://zarathustra-talmudisch.netlify.app/ :: OK
- https://zarathustra-talmudisch.netlify.app/about.html :: OK
- https://zarathustra-talmudisch.netlify.app/talmud.html?ch=vorrede :: OK

### Chapters (talmud.html)
- 81/81 OK

### Source .ptx files
- 81/81 OK

### Sample deeplinks
- https://zarathustra-talmudisch.netlify.app/talmud.html?ch=ch-p1-01#v05 :: 200
- https://zarathustra-talmudisch.netlify.app/talmud.html?ch=ch-p2-01#v10 :: 200
- https://zarathustra-talmudisch.netlify.app/talmud.html?ch=ch-p3-01#v01 :: 200
- https://zarathustra-talmudisch.netlify.app/talmud.html?ch=ch-p4-01#v20 :: 200
- https://zarathustra-talmudisch.netlify.app/talmud.html?ch=vorrede#v05 :: 200


## 7. Side coverage by chapter
_Sides used in commentary: ['bottom', 'inner', 'outer']_
- ch-p1-08: total=5 {'bottom': 0, 'inner': 4, 'outer': 1} | missing sides: ['bottom']
- ch-p1-14: total=3 {'bottom': 0, 'inner': 3, 'outer': 0} | missing sides: ['bottom', 'outer'] | ALL notes weak-flagged
- ch-p1-16: total=3 {'bottom': 0, 'inner': 2, 'outer': 1} | missing sides: ['bottom']
- ch-p1-17: total=4 {'bottom': 0, 'inner': 2, 'outer': 2} | missing sides: ['bottom']
- ch-p2-05: total=3 {'bottom': 1, 'inner': 2, 'outer': 0} | missing sides: ['outer']
- ch-p2-06: total=2 {'bottom': 0, 'inner': 1, 'outer': 1} | missing sides: ['bottom']
- ch-p2-09: total=4 {'bottom': 0, 'inner': 3, 'outer': 1} | missing sides: ['bottom']
- ch-p2-10: total=3 {'bottom': 1, 'inner': 2, 'outer': 0} | missing sides: ['outer']
- ch-p2-11: total=5 {'bottom': 0, 'inner': 2, 'outer': 3} | missing sides: ['bottom']
- ch-p2-16: total=6 {'bottom': 0, 'inner': 4, 'outer': 2} | missing sides: ['bottom']
- ch-p2-17: total=3 {'bottom': 0, 'inner': 2, 'outer': 1} | missing sides: ['bottom']
- ch-p2-19: total=3 {'bottom': 0, 'inner': 2, 'outer': 1} | missing sides: ['bottom']
- ch-p2-21: total=5 {'bottom': 1, 'inner': 4, 'outer': 0} | missing sides: ['outer']
- ch-p3-09: total=7 {'bottom': 0, 'inner': 5, 'outer': 2} | missing sides: ['bottom']
- ch-p3-12: total=13 {'bottom': 0, 'inner': 9, 'outer': 4} | missing sides: ['bottom']
- ch-p3-15: total=5 {'bottom': 0, 'inner': 3, 'outer': 2} | missing sides: ['bottom']
- ch-p3-16: total=3 {'bottom': 1, 'inner': 1, 'outer': 1} | ALL notes weak-flagged
- ch-p4-02: total=4 {'bottom': 0, 'inner': 3, 'outer': 1} | missing sides: ['bottom']
- ch-p4-08: total=6 {'bottom': 0, 'inner': 5, 'outer': 1} | missing sides: ['bottom']
- ch-p4-09: total=6 {'bottom': 0, 'inner': 3, 'outer': 3} | missing sides: ['bottom']
- ch-p4-10: total=3 {'bottom': 1, 'inner': 2, 'outer': 0} | missing sides: ['outer'] | ALL notes weak-flagged
- ch-p4-15: total=3 {'bottom': 1, 'inner': 0, 'outer': 2} | missing sides: ['inner']
- ch-p4-16: total=5 {'bottom': 0, 'inner': 4, 'outer': 1} | missing sides: ['bottom']


## 8. Recommended fixes (ranked by impact)

1. **Fix Vorrede (ch-p0-00) verse numbering drift.** DE has 162 verses, EN/FR/ES have 163. Spot-check shows EN/FR/ES are shifted by +1 starting around v06 (FR) and v155+ (EN). The cleanest fix is to align all four languages on the German verse boundaries (one extra `<paragraphs>` block in EN/FR/ES needs to be merged into a neighboring verse). Until fixed, every Vorrede commentary note targeting v06+ is attached to the wrong sentence in EN/FR/ES UIs. Affected: 224 LaBSE-flagged verse-language pairs.

2. **Backfill missing Spanish translations.** 414 ES verses are empty book-wide. Highest priority: `ch-p2-09` (25 of 29 missing — chapter unreadable in ES), `ch-p3-12` (48 missing), `ch-p4-19` (19 missing), `ch-p3-16` (13 missing). If the user has a complete Sánchez-Pascual edition, re-extract these chapters; otherwise mark the ES tab as "partial" for those chapters in the UI.

3. **Backfill missing French translations.** ~200 FR verses empty. Worst: `ch-p3-12`, `ch-p4-19`, `ch-p4-11`, `ch-p3-10`, `ch-p3-14`, `ch-p4-20`.

4. **Drop or relabel commentary notes with audit_score=0 (17 notes).** These were judged irrelevant in audit.json but remain visible in commentary.json. Either delete them or re-target.

5. **Audit the 80 notes with no audit.json entry.** Likely added after the last LLM audit pass — schedule a re-run.

6. **Triage 140 `_audit_flag: weak` notes.** Per-stream concentration: Klossowski and Deleuze are heaviest. Consider marking them as "associative" rather than "exegetical" in the UI, or hide behind a toggle.

7. **Clean OCR artifacts in ES verses.** Specific known patterns to grep:
   - `1º` / `1°` / `4°` glued to letters (`despierto1º`, `dormir4°`)
   - `<…'` broken brackets like `<despre-cio'`
   - `Asi ` (no accent) where `Así` is expected
   - Soft hyphen `U+00AD` in mid-word (`consolado-res`)

8. **Decide policy on trailing em-dashes.** Many `—` are intentional (Nietzsche's signature punctuation). But verses ending bare ` - ` with no leading content are real truncations. Build a one-shot script: flag any verse where target language ends with a dash but DE doesn't, or vice-versa.

9. **No HTML/render-engine artifacts found in note bodies of consequence** (10 flags, mostly `<em>` or `<i>` tags which are likely legitimate). Verify the renderer interprets these as HTML; if not, escape them.

10. **No broken endpoints on the live site.** All 81 chapters + Vorrede + about + deeplinks return 200. No action needed unless content rerouting is planned.

11. **No side-coverage gaps**: all 81 chapters have notes on at least one side; check report Section 7 for chapters with `missing sides` that may benefit from cross-stream balancing (most chapters have only inner+outer; bottom is rarely used outside ch-p1-01).
