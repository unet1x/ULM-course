# Испанское метеорологическое [решение go/no-go][go-no-go] {#spain-go-no-go}

## Зачем эта глава {#purpose}

Знание погоды становится безопасностью только через воспроизводимое решение. Worksheet ниже ведёт от определения вылета к явным GO / DELAY / REROUTE / CANCEL и к заранее записанным in-flight triggers.

## Результаты обучения {#outcomes}

После главы вы сможете:

1. построить briefing от synoptic scale к route и point data;
2. применить наиболее строгую из law, aircraft, school/aerodrome и personal границ;
3. учесть terrain, coast/islands, [density altitude][density-altitude] и uncertainty;
4. записать departure и airborne decision gates;
5. документировать источник, time, validity и missing data.

## Карта применимости {#applicability}

| Метка | Как использовать главу |
|---|---|
| [ULM — ОСНОВА][ulm] | Итоговый Spanish [ULM][ulm] workflow этого модуля. |
| [ULM — ОСОБО ВАЖНО][ulm] | GO требует запаса и escape route, не только legal weather. |
| [PART-FCL — ОБЩЕЕ][part-fcl] | Framework переносится в будущие [LAPL(A)][lapl]/[PPL(A)][ppl]. |
| [LAPL — ПЕРЕХОД][lapl] | Part-NCO duties остаются future layer. |
| [PPL — РАСШИРЕНИЕ][ppl] | Та же decision discipline с иной mission complexity. |
| [ИСПАНИЯ] | [ULM][ulm] scenarios ограничены Испанией; foreign operation не преподаётся. |
| [БЕЗОПАСНОСТЬ] | DELAY/CANCEL — нормальный outcome, а не failure. |
| [ПРОВЕРИТЬ ПЕРЕД ПОЛЁТОМ] | Refresh dynamic [AIP][aip]/AEMET/[AMA][ama] непосредственно для time of use. |

## Теория {#theory}

### Иерархия ограничений {#weather-limit-hierarchy}

Dispatch uses the most restrictive applicable law/[VMC][vmc], current [AFM][afm]/[POH][poh], aerodrome/school limits and pre-agreed [личные минимумы (personal minima)][personal-minima], plus margin for uncertainty/[TREND][trend]. [Личные минимумы (personal minima)][personal-minima] may be stricter, never looser. Нет универсального лимита [ULM][ulm] по ветру, порывам, crosswind, visibility, cloud base, turbulence, icing или thunderstorm distance. Испанская operational boundary: `SRC-BOE-RD-765-2022`; product sources: `SRC-ENAIRE-AIP-GEN-3-5-2026`, `SRC-AEMET-GUIA-MET-2025` (проверено 2026-07-13).

### Девятишаговый worksheet {#weather-worksheet}

### Шаг 1 — определить полёт {#weather-step-1}

Запишите departure/destination, route, terrain, planned heights, UTC window, payload, daylight, alternates и точки, где возможна посадка. Без defined flight невозможно понять validity и spatial coverage.

### Шаг 2 — выписать hard limits {#weather-step-2}

Отдельно выпишите law/[VMC][vmc], [AFM][afm]/[POH][poh], runway/aerodrome и school restrictions. Не держите числа «в голове» и не превращайте recommendation в aircraft limit.

### Шаг 3 — применить [личные минимумы (personal minima)][personal-minima] {#weather-step-3}

Добавьте заранее согласованные более строгие границы по wind/gust, crosswind, visibility/cloud, terrain, [недавнему опыту (recency)][recency] and type experience. Не смягчайте их после появления passenger pressure.

### Шаг 4 — построить synoptic big picture {#weather-step-4}

Определите air mass, fronts, pressure systems, broad wind/moisture and expected movement. Запишите главный uncertainty: timing, location, intensity или model disagreement.

### Шаг 5 — пройти весь route {#weather-step-5}

Проверьте [GAMET][gamet]/SWL, [AIRMET][airmet]/[SIGMET][sigmet], wind/temperature aloft, terrain/coast/island effects и route escape. [METAR][metar] не описывает весь маршрут.

### Шаг 6 — проверить point products {#weather-step-6}

Сопоставьте current [METAR][metar]/[SPECI][speci], [TAF][taf]/[TREND][trend], aerodrome warnings and local guía. Отметьте issue/observation time, validity, AMD/COR и missing data.

### Шаг 7 — оценить performance {#weather-step-7}

С текущими pressure/temperature/wind and mass use [AFM][afm]/[POH][poh] for take-off, climb, cruise and landing. Classroom [density altitude][density-altitude] only flags [TREND][trend]; it is not dispatch performance.

### Шаг 8 — добавить uncertainty и [TREND][trend] {#weather-step-8}

Сравните successive observations, forecast confidence, radar/satellite/lightning animation and update cycle. Запас увеличивают при fast development, sparse stations, terrain, coast/islands или missing data.

### Шаг 9 — выбрать outcome и triggers {#weather-step-9}

Запишите одно: **GO**, **DELAY**, **REROUTE** или **CANCEL**. Затем задайте точные наблюдаемые triggers: задержка запуска до нового выпуска; уход на alternate при заданном ухудшении; разворот до terrain-рубежа; посадка на выбранной площадке/аэродроме при потере margin. Trigger должен наступать до потери безопасного варианта.

### Матрица результата {#decision-matrix}

| Outcome | Когда выбирать |
|---|---|
| GO | Все limits соблюдены, margin устойчив к plausible change, escape routes доступны. |
| DELAY | Ожидается ближайший update/проход явления, а ожидание сохраняет options. |
| REROUTE | Alternative route materially reduces exposure и остаётся в limits. |
| CANCEL | Limit violated, data insufficient, [TREND][trend] adverse или safe escape absent. |

### Route versus point reports {#route-versus-point}

Point report answers «что наблюдалось здесь и сейчас», route product — «что ожидается в районе/слое/периоде». Оба имеют limits. Checkpoint reassessment repeats steps 5–9 with current position and remaining options; original GO does not persist automatically.

### Coast, islands and terrain {#terrain-coast-islands}

Coastlines can support breeze/convergence/fog; islands add windward/lee contrast; Meseta basins favour inversions; mountain routes add wave/rotor/obscuration. These are prompts to inspect data, not forecasts or universal regional rules. Aerodrome guide remains site-specific. Sources: `SRC-AEMET-AERODROME-GUIDES`, `SRC-AEMET-GUIA-MET-2025` (проверено 2026-07-13).

### Worked decision example {#worked-decision-example}

**Flight:** morning local [ULM][ulm] route near rising terrain, return before afternoon breeze.

**Evidence:** valid area forecast suggests later convection; current point reports good; one route segment lacks convenient landing options; temperature raises [density altitude][density-altitude].

**Decision:** GO only if updated data remain within hard/personal limits and turn-back trigger is reached before cloud develops over the ridge; otherwise DELAY or REROUTE. The scenario is synthetic and not for flight. Sources of method: `SRC-AEMET-GUIA-MET-2025`, `SRC-EASA-EGAST-GA2` (проверено 2026-07-13).

## Применение к [ULM][ulm] {#ulm-application}

This worksheet is written for Spanish national [ULM][ulm] operations. It neither grants international privilege nor teaches foreign procedures. Day [VFR][vfr]/[VMC][vmc] legality remains necessary but not sufficient; current aircraft/manual and pilot margins govern suitability. Source: `SRC-BOE-RD-765-2022` (проверено 2026-07-13).

## Расширение LAPL/PPL {#part-fcl-extension}

For future [LAPL(A)][lapl]/[PPL(A)][ppl], NCO.OP.160 requires latest available meteorological information for route/destination at expected use and GM supports continual reassessment. This duty belongs to future Part-NCO operation, not automatically to current national [ULM][ulm]. Source: `SRC-EASA-AIR-OPS-2026` Revision 24 (проверено 2026-07-13).

## Безопасность {#safety}

A forecast improvement does not create an obligation to depart. If missing/contradictory data prevent a margin demonstration, CANCEL is supported by evidence. After take-off, reassess at checkpoints and execute a trigger without renegotiating it under pressure.

## Типичные ошибки {#common-errors}

1. Проверять only destination point.
2. Оценивать law after [личные минимумы (personal minima)][personal-minima], not before.
3. Forget issue/validity/time zone.
4. Write «turn back if bad» instead of observable trigger.
5. Treat original GO as permission for the whole flight.

## Краткий конспект {#summary}

- Define flight before fetching products.
- Apply most restrictive limit plus uncertainty margin.
- Combine synoptic, route, point and performance layers.
- Make outcome and airborne triggers explicit.

## Контрольные вопросы {#review-questions}

### Q-MET-031 — Какой предел применяется, если personal minimum строже [AFM][afm] и law? {#q-met-031}

A. Строгий personal minimum, поскольку он не расширяет обязательные пределы.<br>
B. Более мягкий aircraft limit, потому что он опубликован.<br>
C. Среднее арифметическое трёх значений.<br>
D. Предел выбирается пассажиром после briefing.

**Правильный ответ:** A.

**Почему:** The most restrictive applicable boundary preserves both mandatory compliance and pre-agreed pilot margin (`SRC-BOE-RD-765-2022`).

**Почему главный отвлекающий вариант неверен:** B ignores the pilot's deliberately stricter рубеж and reduces margin after planning (`SRC-BOE-RD-765-2022`).

### Q-MET-032 — Почему worksheet начинает с определения полёта? {#q-met-032}

A. Route, UTC window, terrain and alternatives determine which products and validity matter.<br>
B. Weather sources одинаковы для любой точки и времени.<br>
C. Это позволяет не проверять aircraft performance.<br>
D. Destination name автоматически задаёт весь route.

**Правильный ответ:** A.

**Почему:** Without intended space/time/use, a current product may still be irrelevant to the actual segment.

**Почему главный отвлекающий вариант неверен:** D collapses route hazards and alternatives into a single point label.

### Q-MET-033 — Когда DELAY является самостоятельным безопасным outcome? {#q-met-033}

A. Когда ожидание нового выпуска или прохода явления сохраняет options и margins.<br>
B. Только если cancellation legally prohibited.<br>
C. Когда pilot хочет скрыть limit exceedance.<br>
D. Когда old screenshot looks better than current data.

**Правильный ответ:** A.

**Почему:** Delay changes estimated-use time and can avoid uncertainty/exposure without forcing a premature GO.

**Почему главный отвлекающий вариант неверен:** D selects obsolete evidence to justify departure and violates source-time discipline (`SRC-AEMET-GUIA-MET-2025`).

### Q-MET-034 — Каким должен быть airborne turn-back trigger? {#q-met-034}

A. Observable, reached before loss of safe turning space or visual margin.<br>
B. «Когда станет совсем плохо» без location or condition.<br>
C. Negotiated only after entering narrowing terrain.<br>
D. Based solely on passenger schedule.

**Правильный ответ:** A.

**Почему:** A pre-defined observable trigger makes action earlier than option loss and resists continuation bias.

**Почему главный отвлекающий вариант неверен:** B delays recognition and gives no repeatable decision boundary (`SRC-EASA-EGAST-GA2`).

### Q-MET-035 — Что делать, если point reports хороши, но route data отсутствуют и terrain leaves no escape? {#q-met-035}

A. DELAY/REROUTE/CANCEL until route uncertainty and escape are acceptable.<br>
B. Infer route weather from nearest point and depart.<br>
C. Treat no data as no hazard.<br>
D. Replace missing evidence with climatology.

**Правильный ответ:** A.

**Почему:** Sparse evidence plus constrained terrain prevents demonstration of margin; point observations do not cover the route.

**Почему главный отвлекающий вариант неверен:** B extrapolates beyond spatial coverage and ignores the no-escape consequence (`SRC-AEMET-GUIA-MET-2025`).

## Источники {#sources}

- `SRC-BOE-RD-765-2022` — Spanish [ULM][ulm] boundary; checked 2026-07-13.
- `SRC-AEMET-GUIA-MET-2025`, `SRC-AEMET-AERODROME-GUIDES` — workflow/products and site-specific orientation; checked 2026-07-13.
- `SRC-ENAIRE-AIP-GEN-3-5-2026` — dynamic Spanish meteorological service; checked 2026-07-13.
- `SRC-EASA-AIR-OPS-2026` — future Part-NCO route-weather duty; checked 2026-07-13.
- `SRC-EASA-EGAST-GA2` — decision pedagogy, not legal minima; checked 2026-07-13.

[metar]: ../reference/glossary.md#term-metar
[taf]: ../reference/glossary.md#term-taf
[speci]: ../reference/glossary.md#term-speci
[trend]: ../reference/glossary.md#term-trend
[sigmet]: ../reference/glossary.md#term-sigmet
[airmet]: ../reference/glossary.md#term-airmet
[gamet]: ../reference/glossary.md#term-gamet
[ama]: ../reference/glossary.md#term-aeronautical-meteorological-self-service-ama
[density-altitude]: ../reference/glossary.md#term-density-altitude
[ulm]: ../reference/glossary.md#term-ulm
[lapl]: ../reference/glossary.md#term-lapl-a
[ppl]: ../reference/glossary.md#term-ppl-a
[part-fcl]: ../reference/glossary.md#term-part-fcl
[afm]: ../reference/glossary.md#term-afm
[poh]: ../reference/glossary.md#term-poh
[vfr]: ../reference/glossary.md#term-vfr
[vmc]: ../reference/glossary.md#term-vmc
[aip]: ../reference/glossary.md#term-aip
[recency]: ../reference/glossary.md#term-recency
[personal-minima]: ../reference/glossary.md#term-personal-minima
[go-no-go]: ../reference/glossary.md#term-go-no-go
