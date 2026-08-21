# Spanish state assets — military and space

**Short answer: capability yes, access no — with three exceptions worth chasing, one
of which is free and sharper than anything we have contacted so far.**

Spain owns aircraft and satellites that could find a 2.13 m orange canopy without
difficulty. None of them can be pointed at a lost commercial payload. But the search
for them turned up a national programme that flies **22 cm imagery over Castilla y
León** and costs nothing to ask about.

## Space — the answer is no, and it is structural

| Asset | Operator | Verdict |
| --- | --- | --- |
| **Ingenio / SEOSAT** (2.5 m pan optical) | CDTI / ESA | **Does not exist.** Lost in the Vega VV17 launch failure, Nov 2020, never replaced |
| **PAZ** — X-band SAR, dual-use, 2018 | Hisdesat | Taskable commercially — **but cannot see this target.** See below |
| **PAZ-2** | Hisdesat | ~2031. Irrelevant |
| **SpainSat NG** | Hisdesat | Communications only, no imaging |
| **Atlantic Constellation** (ES + PT smallsats) | — | Metres-class GSD. Insufficient for a 2 m target |

**Spain has no sovereign sub-metre optical Earth-observation satellite.** That is the
whole answer for the space question: since Ingenio was lost on the pad-to-orbit leg
in 2020, there is no Spanish government optical asset in the resolution class this
search needs. The useful satellites are the commercial ones already contacted —
Pléiades Neo and SkySat/Pelican.

### Why PAZ will not work, specifically

Do not spend money here. A parachute canopy is nylon fabric lying on stubble: no
metal, no corner, no dihedral. Our own radar analysis already establishes the scale
of the problem for a far better target — the **carbon-fibre boom**, which is
conductive, returns only **0.40 m² at X-band** with a glint lobe so narrow that a
satellite's single fixed look geometry has a **~2–4% chance per scene** of catching it
(`boom_detectability.py`, section 3). The canopy is worse than the boom. PAZ is the
right instrument for the *next* flight, once the payload carries the printed
corner-reflector cluster (`reflector_build_sheet.md`) — 2.2 m² at X-band, attitude
tolerant. It is the wrong instrument for this one.

## Military drones — capable, not accessible

| Asset | Operator / base | Capability |
| --- | --- | --- |
| **MQ-9A Reaper** ×4 | 233 Escuadrón, **Ala 23, Talavera la Real** (Badajoz), ~500 km from the search area | EO/IR full-motion video, 20 h endurance. Would find the canopy trivially |
| **INTA Milano** | INTA | ~900 kg, 20 h, 150 kg payload, BLOS via satellite |
| **INTA SIVA / Avizor** | INTA | Tactical surveillance UAV, SIVA's successor programme |
| Searcher / PASI, ScanEagle | Ejército de Tierra, Armada | Tactical ISR |

All of these task on **national-defence or declared-emergency** grounds. A lost
commercial payload is neither. Requesting a Reaper sortie would not be granted and
would cost standing — the same reasoning already applied to the Guardia Civil and the
UME drone units in `local_partners_burgos.md`. **Do not ask.**

---

## The three routes that are actually worth taking

### 1. CNIG / PNOA — free, 22 cm, and nobody has asked ⭐

The **Plan Nacional de Ortofotografía Aérea** flies the whole country on a rolling
cycle. **The 2026 flight covers Castilla y León at 22 cm GSD** (up from 35 cm in
2017 and 2023). At 22 cm a 2.13 m canopy spans **~10 pixels** — and it is orange on
stubble, which is the easiest discrimination problem in this entire project.

The open question is timing: PNOA flies in summer, and we do not know whether Burgos
was covered before or after 12 August. That is exactly what the enquiry is for.
Two things worth knowing:

- Published orthophotos lag acquisition by **6–18 months** — but the **raw fotogramas
  exist from the day of the flight**, and CNIG can say whether and when a given area
  was covered.
- It is free, public data. There is no favour being asked.

**Contact:** Centro Nacional de Información Geográfica, `consulta@cnig.es` /
`centrodedescargas@cnig.es`, and the PNOA project via `pnoa.ign.es`.

> **Asunto:** Consulta PNOA 2026 — ¿fecha del vuelo sobre el norte de Burgos (Tubilla del Agua / Valle de Sedano)?
>
> Buenos días,
>
> Somos Zero 2 Infinity, empresa española de vuelos estratosféricos. El 12 de agosto
> de 2026 perdimos una carga útil científica que aterrizó bajo paracaídas en el
> páramo entre **Tubilla del Agua, Valle de Sedano, Sargentes de la Lora y
> Basconcillos del Tozo** (Burgos).
>
> Tenemos entendido que el vuelo PNOA 2026 cubre Castilla y León con un GSD de 22 cm.
> Nuestra consulta es sencilla: **¿se ha volado ya esa zona, y en qué fecha?**
>
> Si el vuelo es posterior al 12 de agosto, esas imágenes contendrían el objeto que
> buscamos: una vela de paracaídas **naranja de 2,13 m** extendida sobre rastrojo —
> unos 10 píxeles a 22 cm, y de un color que no existe en el campo en agosto.
> Agradeceríamos saber si los fotogramas correspondientes están disponibles antes de
> la publicación de la ortofoto, y por qué vía podríamos consultarlos.
>
> Podemos enviar el polígono de búsqueda en GeoJSON y el informe técnico del vuelo.
>
> Muchas gracias,
> José Mariano López-Urdiales · Zero 2 Infinity

### 2. INTA — peer to peer, not a favour

The **Instituto Nacional de Técnica Aeroespacial** is attached to the Ministry of
Defence but carries a civil aerospace R&D remit, and operates its own UAVs. Zero 2
Infinity is a Spanish space company: this is an approach between institutions, not a
request for military support. Frame it exactly as the UBU approach is framed — a
**joint validation exercise** with a real target, real coordinates and a binary
success criterion, with the data and the write-up shared.

Realistic expectation: slow, and more likely to produce a relationship than a sortie.
Worth one email precisely because the relationship has value beyond this payload.

**Contact:** via `inta.es`, Área de Sistemas No Tripulados / Dirección de Sistemas
Aeronáuticos.

### 3. Fire-season eyes — free, immediate, and August is the moment

Through the summer the Junta de Castilla y León's **operativo INFOCAL** flies fire
surveillance over the province daily and mans **puestos de vigilancia** — staffed
towers with binoculars and all day to look — several of which overlook exactly this
páramo.

You cannot task them, and should not try. But you can **tell them what to look for**,
and an orange 2 m canopy on open stubble is precisely the kind of anomaly a fire
spotter is trained to notice and report. One email to the Junta's fire operations /
medio ambiente service in Burgos, with the photo and the coordinates, costs nothing
and puts trained observers with elevated viewpoints on the problem for the rest of
the season.

This is the same "tell, don't task" principle as the Protección Civil training-exercise
idea: no public resource is diverted, and the ask is proportionate.

---

## Summary

| Route | Cost | Realistic value |
| --- | --- | --- |
| **CNIG / PNOA enquiry** | free | **Highest of the three — 22 cm imagery may already exist** |
| Fire-watch towers / INFOCAL notice | free | Good — trained observers, elevated, all season |
| INTA | free, slow | Relationship more than sortie |
| PAZ tasking | € | **Zero. Physics says no. Do not buy** |
| Reaper / UME / Guardia Civil | — | Not available; do not ask |
