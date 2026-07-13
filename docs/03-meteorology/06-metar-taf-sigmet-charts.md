# [METAR][metar], [TAF][taf], warnings и карты Испании {#metar-taf-sigmet-charts}

## Зачем эта глава {#purpose}

Продукт читают через четыре вопроса: кто выпустил, для какого места/района, на какое время и что он не описывает. Декодирование — только начало: пилот связывает point observation, forecast, warnings, area charts и [TREND][trend].

## Результаты обучения {#outcomes}

После главы вы сможете:

1. отличить observation от forecast и UTC issue/validity times;
2. разобрать [METAR][metar], [SPECI][speci], [TREND][trend] и [TAF][taf];
3. интерпретировать BECMG, FM, TEMPO, PROB30/40, AMD и COR;
4. назвать роль [SIGMET][sigmet], [AIRMET][airmet], [GAMET][gamet], SWL, radar/satellite/lightning;
5. собрать данные через [AMA][ama] без превращения архивного примера в live weather.

## Карта применимости {#applicability}

| Метка | Как использовать главу |
|---|---|
| [ULM — ОСНОВА][ulm] | Основной briefing layer для [ULM][ulm] в Испании. |
| [ULM — ОСОБО ВАЖНО][ulm] | Point report никогда не заменяет route picture. |
| [PART-FCL — ОБЩЕЕ][part-fcl] | Codes входят в будущую теорию [LAPL(A)][lapl]/[PPL(A)][ppl]. |
| [LAPL — ПЕРЕХОД][lapl] | Part-NCO [AMC][amc] treatment показан только как future layer. |
| [PPL — РАСШИРЕНИЕ][ppl] | Применяется та же discipline source/time/validity. |
| [ИСПАНИЯ] | Авторитетны current AEMET/[ENAIRE][enaire] products and [AIP][aip]. |
| [БЕЗОПАСНОСТЬ] | Archived guide/example/screenshot не является текущей погодой. |
| [ПРОВЕРИТЬ ПЕРЕД ПОЛЁТОМ] | Issue time, validity, amendments, route coverage и next update. |

## Теория {#theory}

### UTC, station, observation и forecast {#source-time-validity}

Сначала определите product name, station/FIR/area, issue time в UTC, observation time или validity period, затем age at estimated use. [METAR][metar]/[SPECI][speci] сообщают observed aerodrome conditions; [TAF][taf] прогнозирует аэродром на validity period. [METAR][metar] не описывает весь маршрут. [TAF][taf] не является обещанием: это best forecast with change/probability groups. Источники: `SRC-AEMET-GUIA-MET-2025` pp. 18–31, `SRC-ENAIRE-AIP-GEN-3-5-2026` §§3.1–3.3 (проверено 2026-07-13).

### [METAR][metar], [SPECI][speci] и [TREND][trend] {#metar-speci-trend}

[METAR][metar] — routine report, [SPECI][speci] — selected special report after specified significant change, а [TREND][trend] — short landing forecast appended to a report where provided. [SPECI][speci] не является исправлением [TAF][taf]; COR corrects an issued message, whereas [SPECI][speci] reports new observed conditions. AUTO warns that automatic observation and missing/limited elements need attention. Источники: `SRC-AEMET-CODE-FORMS-2021`, `SRC-ENAIRE-AIP-GEN-3-5-2026` (проверено 2026-07-13).

### [TAF][taf] и change groups {#taf-change-groups}

- FM starts a new prevailing forecast from the stated time;
- BECMG describes a transition during a period to new prevailing conditions;
- TEMPO describes temporary fluctuations under code limits;
- PROB30/PROB40 expresses probability of specified conditions;
- AMD is an amendment; COR corrects an error.

TEMPO нельзя игнорировать как «не prevailing». PROB30 нельзя считать пренебрежимо малой: probability and consequence enter the decision. Future Part-NCO [AMC][amc] contains specific planning treatment for certain TEMPO/PROB30/40 groups; it is not a blanket safety permission to ignore them. Sources: `SRC-AEMET-GUIA-MET-2025` pp. 26–31; future-layer [AMC1][amc] NCO.OP.160 in `SRC-EASA-AIR-OPS-2026` (проверено 2026-07-13).

### [SIGMET][sigmet], [AIRMET][airmet], [GAMET][gamet] и SWL {#sigmet-airmet-gamet}

[SIGMET][sigmet] warns of specified en-route phenomena of operational significance; [AIRMET][airmet] addresses specified lower-level phenomena not already included as applicable; [GAMET][gamet] is a low-level area forecast; SWL visualises significant low-level weather. Each has area, validity, criteria and limitations. Отсутствие [SIGMET][sigmet] не означает отсутствие опасности. Источники: `SRC-AEMET-GUIA-MET-2025` pp. 39–57, `SRC-ENAIRE-AIP-GEN-3-5-2026` §§3.6, 8 (проверено 2026-07-13).

### V1/V5: применяем текущий [AIP][aip] {#v1-v5-discrepancy}

Текущий [AIP][aip] España GEN 3.5 §3.6.2 определяет на low-level chart `V1` как видимость ниже 1000 м, а `V5` — как видимость 1000–5000 м. Guía MET p. 52 содержит apparent contrary typo for V1; этот курс её не воспроизводит. Operational priority — current [AIP][aip]: `SRC-ENAIRE-AIP-GEN-3-5-2026` WEF 11.06.2026 (проверено 2026-07-13); discrepancy recorded in source audit.

### Radar, satellite и lightning {#radar-satellite-lightning}

Radar shows returned energy influenced by precipitation/type/range/blockage; satellite senses radiance in selected bands; lightning network locates discharges with its own detection limits. Overlay times may differ. Use animation and timestamps, never assume coloured pixel equals cloud clearance or turbulence intensity. Spanish access and product context: `SRC-AEMET-GUIA-MET-2025` pp. 50–60 (проверено 2026-07-13).

### [AMA][ama] и dynamic operational sources {#ama}

[AMA][ama], AEMET aviation pages and [AIP][aip] are dynamic operational sources. Before flight record retrieval time, product issue/validity, next update and any missing layer. Архивный снимок не является текущей погодой; a guide illustration is not dispatch data. Область [AMA][ama]: `SRC-AEMET-GUIA-MET-2025` pp. 58–60 and `SRC-ENAIRE-AIP-GEN-3-5-2026` §9.1 (проверено 2026-07-13).

![Синтетический декодер observation, forecast и change groups; не текущая погода](../assets/diagrams/metar-taf-decoder.svg)

## Десять синтетических декодирований {#synthetic-decodes}

### Синтетический пример MET-DEC-01 — обычное наблюдение {#met-dec-01}

**СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ ПРИМЕР — НЕ ДЛЯ ПОЛЁТА**

**Код:** `METAR LEZZ 131000Z 24008KT 9999 FEW030 22/12 Q1018 NOSIG=`

**Разбор:** fictional station LEZZ; observation 13-го в 10:00 UTC; wind 240°/8 kt; visibility 10 km or more; few cloud at 3000 ft aerodrome level; T/Td 22/12 °C; [QNH][qnh] 1018 hPa; no significant [TREND][trend] change.

**Решение пилота:** это point/time observation; дополнить route forecast, warnings, wind aloft and [TREND][trend].

### Синтетический пример MET-DEC-02 — порыв {#met-dec-02}

**СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ ПРИМЕР — НЕ ДЛЯ ПОЛЁТА**

**Код:** `METAR LEZZ 131030Z 29014G26KT 9999 SCT025 24/14 Q1014=`

**Разбор:** mean 14 kt from 290°, gust 26 kt; visibility at least 10 km; SCT at 2500 ft; [QNH][qnh] 1014 hPa.

**Решение пилота:** calculate mean/gust components, check crosswind/runway/terrain and apply the most restrictive limit plus margin.

### Синтетический пример MET-DEC-03 — variable direction {#met-dec-03}

**СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ ПРИМЕР — НЕ ДЛЯ ПОЛЁТА**

**Код:** `METAR LEZZ 131100Z VRB04KT 8000 NSC 20/16 Q1016=`

**Разбор:** direction variable at 4 kt; 8 km visibility; no significant cloud reported under code criteria; T/Td 20/16 °C; [QNH][qnh] 1016 hPa.

**Решение пилота:** VRB does not guarantee steady flow; inspect runway reports, local circulations and ожидаемое изменение.

### Синтетический пример MET-DEC-04 — [CAVOK][cavok] trap {#met-dec-04}

**СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ ПРИМЕР — НЕ ДЛЯ ПОЛЁТА**

**Код:** `METAR LEZZ 131130Z 08018KT CAVOK 30/09 Q1009=`

**Разбор:** wind 080°/18 kt; [CAVOK][cavok] replaces visibility/weather/cloud groups under code criteria; hot/dry surface; low [QNH][qnh]. It says nothing about route wave, gust exposure, performance or future change.

**Решение пилота:** do not equate [CAVOK][cavok] with clear/safe; assess wind, terrain, [density altitude][density-altitude] and route products.

### Синтетический пример MET-DEC-05 — low visibility, weather и cloud {#met-dec-05}

**СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ ПРИМЕР — НЕ ДЛЯ ПОЛЁТА**

**Код:** `METAR LEZZ 131200Z 02006KT 1800 -RA BR BKN004 OVC009 12/11 Q1021=`

**Разбор:** 1800 m visibility, light rain, mist, BKN 400 ft and OVC 900 ft aerodrome level, near-saturated air.

**Решение пилота:** conditions remove visual margin; do not use one aerodrome report to infer a passable route.

### Синтетический пример MET-DEC-06 — AUTO и missing data {#met-dec-06}

**СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ ПРИМЕР — НЕ ДЛЯ ПОЛЁТА**

**Код:** `METAR LEZZ 131230Z AUTO /////KT //// // ////// 18/17 Q////=`

**Разбор:** automatic report; slashes mark unavailable wind, visibility/weather, cloud and pressure elements; temperature/dew point alone remain.

**Решение пилота:** missing is unknown, not favourable; obtain alternative/current official layers or delay/cancel.

### Синтетический пример MET-DEC-07 — special report и [TREND][trend] {#met-dec-07}

**СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ ПРИМЕР — НЕ ДЛЯ ПОЛЁТА**

**Код:** `SPECI LEZZ 131300Z 25020G32KT 3000 TSRA BKN012CB 19/17 Q1008 BECMG AT1330 9999 NSW SCT020=`

**Разбор:** [SPECI][speci] records significant observed deterioration with thunderstorm rain, CB and gust; appended [TREND][trend] forecasts improvement around 13:30 UTC to 10 km or more, no significant weather, SCT 2000 ft.

**Решение пилота:** [SPECI][speci] is not a [TAF][taf] correction and [TREND][trend] is not certainty; current thunderstorm exposure drives delay.

### Синтетический пример MET-DEC-08 — BECMG и FM {#met-dec-08}

**СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ ПРИМЕР — НЕ ДЛЯ ПОЛЁТА**

**Код:** `TAF LEZZ 131100Z 1312/1321 22008KT 9999 SCT030 BECMG 1314/1316 28015G25KT FM131800 32010KT CAVOK=`

**Разбор:** [TAF][taf] valid 12–21 UTC; initial prevailing conditions; gradual transition 14–16 UTC to gusty northwesterly; from 18 UTC a new prevailing group with [CAVOK][cavok].

**Решение пилота:** plan each estimated-use window and uncertainty through BECMG; do not apply the final group early.

### Синтетический пример MET-DEC-09 — TEMPO {#met-dec-09}

**СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ ПРИМЕР — НЕ ДЛЯ ПОЛЁТА**

**Код:** `TAF LEZZ 131100Z 1312/1320 18010KT 9999 SCT025 TEMPO 1314/1318 3000 SHRA BKN012TCU=`

**Разбор:** prevailing reportable conditions are better, but temporary 14–18 UTC deterioration includes 3000 m, showers and BKN TCU at 1200 ft.

**Решение пилота:** TEMPO cannot be ignored; compare flight/escape timing and consequence, then delay/reroute/cancel if margin is inadequate.

### Синтетический пример MET-DEC-10 — probability, amendment и correction {#met-dec-10}

**СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ ПРИМЕР — НЕ ДЛЯ ПОЛЁТА**

**Код:** `TAF AMD LEZZ 131200Z 1312/1321 09012KT 9999 SCT020 PROB30 TEMPO 1315/1318 2000 TSRA BKN008CB PROB40 1318/1320 4000 SHRA BKN012`; `TAF COR` would identify correction of an issued error.

**Разбор:** AMD replaces/amends forecast content; 30% probability of temporary thunderstorm deterioration in one window; 40% probability of specified later deterioration; COR has a different editorial purpose.

**Решение пилота:** neither PROB30 nor PROB40 is negligible by definition; combine probability, severity, alternatives and later updates.

## Применение к [ULM][ulm] {#ulm-application}

For Spanish [ULM][ulm], build a multi-layer picture: current [METAR][metar]/[SPECI][speci], [TAF][taf]/[TREND][trend], [GAMET][gamet]/SWL, [AIRMET][airmet]/[SIGMET][sigmet], radar/satellite/lightning and aerodrome/local information. No single decoded message establishes a universal go condition. Sources: `SRC-ENAIRE-AIP-GEN-3-5-2026`, `SRC-AEMET-GUIA-MET-2025` (проверено 2026-07-13).

## Расширение LAPL/PPL {#part-fcl-extension}

Future [LAPL(A)][lapl]/[PPL(A)][ppl] Part-NCO layer uses latest information for route/destination at expected time and [AMC][amc] treatment of change groups. This is explicitly future-licence material, not automatically the national [ULM][ulm] rule. Source: NCO.OP.160 and [AMC1][amc]/GM1/GM2 in `SRC-EASA-AIR-OPS-2026` (проверено 2026-07-13).

## Безопасность {#safety}

Before every operational use, refresh dynamic [AIP][aip]/AEMET/[AMA][ama], confirm validity and note unavailable data. Static examples above and archived screenshots are invalid for flight.

## Типичные ошибки {#common-errors}

1. Reading [METAR][metar] as route weather.
2. Treating [TAF][taf] as a promise.
3. Ignoring TEMPO/PROB30.
4. Calling [SPECI][speci] a [TAF][taf] correction.
5. Treating no-[SIGMET][sigmet] as no hazard.

## Краткий конспект {#summary}

- Observation, forecast and warning answer different questions.
- Change groups are time-structured uncertainty, not footnotes.
- Dynamic products must be current for estimated use.
- A decoded code is not a complete briefing.

## Контрольные вопросы {#review-questions}

### Q-MET-026 — Что первым проверяют перед декодированием weather message? {#q-met-026}

A. Source/place, issue or observation time, validity and age at estimated use.<br>
B. Только последнюю группу pressure.<br>
C. Совпадает ли message с желаемым планом.<br>
D. Длину строки без пробелов.

**Правильный ответ:** A.

**Почему:** Product meaning depends on who/where/when; stale or out-of-area data can be decoded correctly but applied wrongly (`SRC-AEMET-GUIA-MET-2025`).

**Почему главный отвлекающий вариант неверен:** B ignores spatial and temporal validity, without which pressure alone cannot support dispatch.

### Q-MET-027 — Чем [SPECI][speci] отличается от COR? {#q-met-027}

A. [SPECI][speci] reports selected significant observed change; COR corrects an issued-message error.<br>
B. [SPECI][speci] always forecasts seven days; COR observes wind.<br>
C. Они полностью взаимозаменяемы.<br>
D. COR отменяет все current observations.

**Правильный ответ:** A.

**Почему:** The code forms separate special observation from editorial correction (`SRC-AEMET-CODE-FORMS-2021`).

**Почему главный отвлекающий вариант неверен:** C erases the observation/correction distinction and can corrupt chronology (`SRC-AEMET-CODE-FORMS-2021`).

### Q-MET-028 — Почему TEMPO нельзя автоматически игнорировать? {#q-met-028}

A. Temporary deterioration may overlap the flight and have high consequence despite not being prevailing.<br>
B. TEMPO always means permanent improvement.<br>
C. TEMPO applies only after forecast validity ends.<br>
D. It is a station identifier without weather meaning.

**Правильный ответ:** A.

**Почему:** Planning compares time window, probability treatment, consequence and escape options; future [AMC][amc] nuance is not blanket permission.

**Почему главный отвлекающий вариант неверен:** B reverses temporary group meaning and removes the stated adverse conditions.

### Q-MET-029 — Что означает `V1` на current Spanish low-level chart? {#q-met-029}

A. Visibility below 1000 m.<br>
B. Visibility above 10 km.<br>
C. Wind exactly 1 kt.<br>
D. Cloud base exactly 1000 ft.

**Правильный ответ:** A.

**Почему:** [AIP][aip] España GEN 3.5 §3.6.2 defines `V1 < 1000 m`; its current definition controls over the apparent Guía typo (`SRC-ENAIRE-AIP-GEN-3-5-2026`).

**Почему главный отвлекающий вариант неверен:** D changes a visibility category into a cloud-base value and even changes units.

### Q-MET-030 — Как использовать archived [AMA][ama] screenshot from a lesson? {#q-met-030}

A. Only to learn interface/product structure; retrieve current valid data for flight.<br>
B. As current weather until colours visibly change.<br>
C. As route clearance after checking station name.<br>
D. As replacement for issue and validity time.

**Правильный ответ:** A.

**Почему:** [AMA][ama] is dynamic; archived imagery has a historical timestamp and no operational currency.

**Почему главный отвлекающий вариант неверен:** B ignores timestamp/validity and could apply obsolete hazards or improvements (`SRC-AEMET-GUIA-MET-2025`).

## Источники {#sources}

- `SRC-AEMET-GUIA-MET-2025` — pp. 18–60 product explanations; examples not live; checked 2026-07-13.
- `SRC-AEMET-CODE-FORMS-2021` — official compact code forms; cross-checked with current [AIP][aip]; checked 2026-07-13.
- `SRC-ENAIRE-AIP-GEN-3-5-2026` — current Spanish service/product area and V1/V5; dynamic; checked 2026-07-13.
- `SRC-EASA-AIR-OPS-2026` — NCO.OP.160/[AMC][amc] future layer; checked 2026-07-13.
- `SRC-ICAO-ANNEX3-2025` — edition metadata only; not used to infer unverified Spanish implementation; checked 2026-07-13.

[metar]: ../reference/glossary.md#term-metar
[taf]: ../reference/glossary.md#term-taf
[speci]: ../reference/glossary.md#term-speci
[trend]: ../reference/glossary.md#term-trend
[sigmet]: ../reference/glossary.md#term-sigmet
[airmet]: ../reference/glossary.md#term-airmet
[gamet]: ../reference/glossary.md#term-gamet
[ama]: ../reference/glossary.md#term-aeronautical-meteorological-self-service-ama
[cavok]: ../reference/glossary.md#term-cavok
[qnh]: ../reference/glossary.md#term-qnh
[density-altitude]: ../reference/glossary.md#term-density-altitude
[ulm]: ../reference/glossary.md#term-ulm
[lapl]: ../reference/glossary.md#term-lapl-a
[ppl]: ../reference/glossary.md#term-ppl-a
[part-fcl]: ../reference/glossary.md#term-part-fcl
[aip]: ../reference/glossary.md#term-aip
[enaire]: ../reference/glossary.md#term-enaire
[amc]: ../reference/glossary.md#term-amc
