# Esborranys en català — Airbus i Planet, com a UPC Space Program

Versió en català dels dos correus, escrits per ser enviats per membres de
l'**associació d'estudiants UPC Space Program** (Universitat Politècnica de
Catalunya). Cada correu fa referència a una **fotografia adjunta de l'altre globus**
com a exemple del vehicle i de la càrrega útil. Placeholders: `[NOM]` del
destinatari, `[SIGNATURA]` de qui envia, i la foto per adjuntar.

**Nota important abans d'enviar.** Aquests textos han de sortir signats per qui
realment els envia — membres de l'associació — i si el vol és una col·laboració amb
Zero 2 Infinity, val la pena dir-ho en una línia (com fa l'esborrany) en lloc
d'ometre-ho: una tasca de bona voluntat concedida a estudiants es converteix en un
problema de reputació si després sembla que era una empresa. La transparència no
costa res i protegeix el favor.

---

## A. Airbus — Pléiades Neo

> **Assumpte:** Sol·licitud d'adquisició a 30 cm — recuperació de la càrrega útil d'un globus estratosfèric prop de Burgos

Hola [NOM],

Som estudiants del **UPC Space Program**, l'associació aeroespacial d'estudiants de
la Universitat Politècnica de Catalunya. El 12 d'agost vam perdre la càrrega útil
d'un dels nostres globus estratosfèrics, i creiem que Pléiades Neo la pot trobar.

El vol va sortir de Villadiego (Burgos) el 12 d'agost de 2026 a les 18:23 UTC. Una
fallada de bateria va acabar la telemetria a 22.205 m i el sistema de seguretat va
alliberar el globus; la càrrega va aterrar suaument sota paracaigudes, de nit, i la
ràdio no va tornar a parlar. La nostra reconstrucció del descens (camps de vent GFS,
calibrada amb l'ascens registrat i comprovada fora de mostra) situa l'aterratge en
una **caixa de 38 km²** als páramos al nord de Villadiego, amb una caixa del 90% de
139 km². Adjuntem una fotografia de l'altre globus de l'associació perquè es vegi
exactament quin tipus de vehicle i de càrrega útil estem buscant.

La bona notícia per a la imatgeria: el paracaigudes de 84 polzades va quedar
enganxat al tren de vol, així que l'objectiu no és només l'esfera blanca de
porexpan de 0,70 m — és una **vela taronja de 2,13 m** estesa sobre el rostoll. A
30 cm són 7 píxels de diàmetre, al costat del dipol brillant-més-ombra de l'esfera.
Hem fet els números abans d'escriure-us: la detecció té molt de marge, i la
discriminació que ens preocupava (les bales d'ensitjat blanques d'1,2–1,5 m) ara
juga doblement a favor nostre: la vela és més gran que qualsevol bala, i és
taronja — una ràtio vermell/blau sobre el producte multiespectral la separa
categòricament del plàstic blanc (ràtio ≈ 1) i del sòl sec (≈ 1,5–2). Les 6 bandes
VNIR a 30 cm són gairebé ideals per a aquest filtre, i per això us ho demanem a
vosaltres específicament.

El que ens funcionaria:

- 1 × escena d'arxiu sobre l'AOI, la més recent disponible abans del 12/08/2026
- 1–2 × adquisicions programades després d'aquesta data (qualsevol passada després
  de les 21:00 UTC del 12 d'agost és vàlida — la càrrega no s'ha mogut)
- ≤15° fora del nadir, ≤5% de núvols, PAN lliurat per separat del producte
  pansharpened

AOI (WGS84): **caixa del 50%: 42,63156–42,69375 N, 3,89968–3,81511 O (38 km²)**;
caixa del 90%: 42,60287–42,72243 N, 3,93869–3,77610 O (139 km²).

Sabem que això queda per sota dels vostres mínims de programació, i per això
preguntem si pot sortir com a col·lecció d'avaluació o de bona voluntat — una sola
passada sobre un corredor ibèric existent. A canvi, la història és tota vostra:
publicarem el mètode de detecció i la recuperació, amb la imatgeria acreditada a
Airbus, tant si la trobem com si no. Per a una associació d'estudiants, "imatgeria
de 30 cm recupera una càrrega útil estratosfèrica perduda" és un cas d'estudi que
s'escriu sol — i per a nosaltres seria una col·laboració que recordaríem tota la
carrera. El vol es va fer en col·laboració amb Zero 2 Infinity, que ens dona suport
tècnic.

Una cosa que val la pena remarcar: la càrrega és a terra des del 12 d'agost i la
zona és en plena collita — l'exposició es degrada setmana a setmana. Si això és
possible, com més aviat millor.

Us podem enviar la nota de viabilitat completa — radiometria, geometria d'ombres,
anàlisi de confusors — més l'AOI en GeoJSON i l'informe d'investigació del vol.

Gràcies pel vostre temps,

[SIGNATURA]
UPC Space Program — Universitat Politècnica de Catalunya

---

## B. Planet — SkySat, Pelican, PlanetScope

> **Assumpte:** Trobar un paracaigudes taronja prop de Burgos — sol·licitud de tasking, i una pregunta sobre Pelican

Hola [NOM],

Una petició poc habitual, i creiem que genuïnament interessant més enllà del favor.

Som estudiants del **UPC Space Program**, l'associació aeroespacial d'estudiants de
la Universitat Politècnica de Catalunya. El 12 d'agost de 2026 vam volar un globus
estratosfèric des de Villadiego (Burgos); una fallada d'alimentació va acabar la
telemetria a 22 km i el sistema de seguretat va alliberar el globus. La nostra
reconstrucció calibrada del descens dona una **caixa primària de 38 km²** (90%:
139 km²) sobre camps al nord del punt de llançament — caixes exactes més avall.
Adjuntem una fotografia de l'altre globus de l'associació com a exemple del vehicle
i de la càrrega útil que busquem.

L'objectiu és millor del que semblava quan ho vam modelar per primer cop. El
paracaigudes de 84 polzades va quedar enganxat, així que el que cal trobar és una
**vela taronja de 2,13 m** sobre rostoll — uns 3 píxels a la cel·la real de 0,72 m
de SkySat, cosa que converteix SkySat de "veu un bri no identificable" en un sensor
candidat de debò, amb l'esfera de 0,70 m i la seva ombra com a indici confirmatori
al costat. La nostra preocupació residual era separar la vela de les bales
d'ensitjat d'1,2–1,5 m; s'ha dissolt dues vegades: la vela és més gran, i és
taronja — una ràtio de bandes vermell/blau marca el teixit taronja a ≈ 4–6 contra
≈ 1 del plàstic blanc de bala i ≈ 1,5–2 del sòl sec, així que el filtre de color
tanca el problema fins i tot a la cel·la grossa de SkySat.

Dues preguntes, doncs:

1. **Hi ha Pelican disponible per a això?** A 40 cm la vela fa més de 5 píxels i el
   filtre de mida és decisiu; un objectiu de mida, posició i data conegudes a terra
   és un objecte de validació poc freqüent per a un sensor nou.
2. **Si SkySat és l'opció realista**, podríem tenir una o dues adquisicions després
   del 12/08/2026 (qualsevol passada després de les 21:00 UTC d'aquell dia és
   vàlida — res no s'ha mogut), més l'escena d'arxiu més recent d'abans d'aquesta
   data? La línia base d'arxiu elimina tot el que ja era als camps; qualsevol cosa
   nova, brillant i de ~2 m és candidata. Sobre 38 km², la nostra estimació és una
   llista curta que es revisa en un dia de cotxe.

A banda — el nostre accés a PlanetScope podria cobrir l'AOI les setmanes del
voltant? No per detectar: a 3 m la vela no arriba a un píxel. Però és ideal per
saber quins camps s'han llaurat i quan, i per triar dates de tasking sense núvols.

AOI (WGS84): **caixa del 50%: 42,63156–42,69375 N, 3,89968–3,81511 O (38 km²)**;
caixa del 90%: 42,60287–42,72243 N, 3,93869–3,77610 O (139 km²).

Sabem que això queda per sota dels vostres mínims i preguntem per condicions
d'avaluació o de bona voluntat. A canvi: publicació completa del mètode i del
resultat, imatgeria acreditada a Planet, i una validació neta de detecció d'objectes
petits al món real que no és ni un aparcament ni un contenidor. El vol es va fer en
col·laboració amb Zero 2 Infinity, que ens dona suport tècnic.

El temps compta — la càrrega és a terra des del 12 d'agost i la collita avança.

Gràcies,

[SIGNATURA]
UPC Space Program — Universitat Politècnica de Catalunya

---

## Notes d'ús

- **La foto adjunta fa la feina de credibilitat emocional**: un globus real, una
  càrrega real, estudiants reals. El paràgraf tècnic fa la de credibilitat dura.
  Totes dues calen.
- **Qui signa ha de ser qui envia.** I la línia sobre la col·laboració amb Z2I es
  queda: un favor concedit amb informació completa és un favor que es pot repetir.
- **Els números no es tradueixen a la baixa.** Les caixes WGS84, els píxels i les
  ràtios són idèntics als esborranys en anglès (`outreach_drafts.md`) — si un
  lector tècnic compara versions, han de quadrar.
- Versió anglesa de referència amb tota l'argumentació: `outreach_drafts.md`.
