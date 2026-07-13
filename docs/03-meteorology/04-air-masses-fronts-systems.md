# Воздушные массы, фронты и барические системы {#air-masses-fronts-systems}

## Зачем эта глава {#purpose}

Synoptic picture помогает не собирать аэродромные reports как несвязанные точки. Оно показывает, почему меняются ветер, облачность и осадки и где прогноз наиболее неопределён. Но textbook front model — только концептуальная схема, не готовый forecast.

## Результаты обучения {#outcomes}

После главы вы сможете:

1. объяснить source region и modification воздушной массы;
2. различить warm, cold, occluded и stationary front;
3. связать low/high, trough/ridge и pressure gradient с потоком;
4. отделить conceptual cyclone model от реальной атмосферы;
5. использовать испанские patterns только как климатологическую ориентацию.

## Карта применимости {#applicability}

| Метка | Как использовать главу |
|---|---|
| [ULM — ОСНОВА][ulm] | Основной synoptic layer для [ULM][ulm] в Испании. |
| [ULM — ОСОБО ВАЖНО][ulm] | Раннее распознавание front/system сохраняет варианты возврата. |
| [PART-FCL — ОБЩЕЕ][part-fcl] | Теория общая для [LAPL(A)][lapl]/[PPL(A)][ppl]. |
| [LAPL — ПЕРЕХОД][lapl] | Будущий route briefing опирается на тот же масштаб. |
| [PPL — РАСШИРЕНИЕ][ppl] | Добавится более формальная эксплуатационная оценка источников. |
| [ИСПАНИЯ] | Климатические patterns не заменяют AEMET forecast. |
| [БЕЗОПАСНОСТЬ] | Front может быть размытым, волнистым, медленным или не совпасть с textbook cross-section. |
| [ПРОВЕРИТЬ ПЕРЕД ПОЛЁТОМ] | Current chart, movement, timing, confidence и локальные observations. |

## Теория {#theory}

### Воздушная масса: происхождение и изменение {#air-masses}

Air mass приобретает свойства над source region, но меняется при движении над более тёплой/холодной или сухой/влажной поверхностью. Heating снизу увеличивает instability и mixing; cooling снизу стабилизирует низкий слой и может поддержать fog/stratus. Поэтому название происхождения — начало анализа, не полный forecast. Стабильная физика: `SRC-FAA-AWH-28B-2026` (проверено 2026-07-13).

### Четыре типа front {#fronts}

- warm front: тёплый воздух продвигается над отступающим холодным;
- cold front: более холодный воздух продвигается под тёплый;
- stationary front: ни одна масса не вытесняет другую заметно;
- occluded front: cold-front sector догоняет warm-front structure, формируя сложную трёхмерную границу.

Slope, speed, moisture и stability определяют реальную ширину cloud/precipitation. Не предполагайте одну последовательность облаков для каждого случая. Стабильная физика: `SRC-FAA-AWH-28B-2026` (проверено 2026-07-13).

### Low, high, trough и ridge {#pressure-systems}

Low — область относительно низкого давления, high — высокого; trough/ridge — вытянутые области пониженного/повышенного pressure pattern. Wind возникает из баланса pressure-gradient, Coriolis, friction и curvature effects. Close isobars обычно указывают более сильный pressure gradient, но surface wind дополнительно изменяют terrain и stability. Стабильная физика: `SRC-FAA-AWH-28B-2026` (проверено 2026-07-13).

### Conceptual model и real atmosphere {#conceptual-versus-forecast}

Textbook wave cyclone объясняет отношения low, warm/cold fronts и sectors. Реальный front может деформироваться, разделиться, замедлиться или взаимодействовать с mountains/convection. Схема ниже оригинальна и прямо помечена как conceptual; она не является forecast.

![Концептуальные модели front и pressure; не прогноз](../assets/diagrams/fronts-and-pressure.svg)

### Испанские patterns: только ориентация {#spain-climatological-patterns}

Atlantic fronts чаще влияют на запад/север, Mediterranean lows способны давать влажный easterly flow, а subtropical high часто определяет крупномасштабный режим. Это климатология не является прогнозом конкретного дня. Canarias, Meseta, побережья и горы требуют отдельных route products и point data. Доступ к продуктам: `SRC-AEMET-GUIA-MET-2025`, `SRC-ENAIRE-AIP-GEN-3-5-2026` (проверено 2026-07-13).

### Пошаговое чтение synoptic chart {#synoptic-reading}

1. Отметьте valid time и источник.
2. Найдите pressure centres, fronts, troughs/ridges.
3. Определите движение и expected timing относительно полёта.
4. Оцените gradient, air-mass source/modification и terrain interaction.
5. Проверьте гипотезу по reports, forecasts, radar/satellite/lightning.
6. Запишите uncertainty и trigger отмены/разворота.

## Применение к [ULM][ulm] {#ulm-application}

Для испанского [ULM][ulm] synoptic analysis служит ранним фильтром. Он не создаёт универсального weather limit и не заменяет применимые [VMC][vmc], [AFM][afm]/[POH][poh], аэродромные и личные пределы. Operational source динамический: `SRC-AEMET-GUIA-MET-2025`, проверено 2026-07-13, но каждый вылет требует текущего выпуска.

## Расширение LAPL/PPL {#part-fcl-extension}

В будущем слое [LAPL(A)][lapl]/[PPL(A)][ppl] Part-NCO требует latest available meteorological information для route/destination at estimated time of use. Это не автоматическая норма национального [ULM][ulm]. Источник: NCO.OP.160 в `SRC-EASA-AIR-OPS-2026` (Revision 24, March 2026; проверено 2026-07-13).

## Безопасность {#safety}

Не летите к front только потому, что один report ещё good. Timing error, embedded convection и terrain могут убрать retreat path. Если фактическое развитие опережает forecast, новый факт важнее прежнего плана.

## Типичные ошибки {#common-errors}

1. Принимать front symbol за точную стену погоды.
2. Ожидать textbook cloud sequence без проверки.
3. Считать high pressure синонимом good visibility.
4. Использовать climatology как day forecast.
5. Читать только destination, не движение системы.

## Краткий конспект {#summary}

- Air mass изменяется по пути.
- Front type не задаёт единственный weather sequence.
- Synoptic model строит гипотезу, reports/forecasts её проверяют.
- Climatology помогает ожидать, но не dispatch.

## Контрольные вопросы {#review-questions}

### Q-MET-016 — Почему название воздушной массы недостаточно для прогноза маршрута? {#q-met-016}

A. Свойства изменяются над новой поверхностью и под действием mixing, terrain и systems.<br>
B. Название содержит только аэродромный позывной.<br>
C. Воздушные массы не имеют температуры или влажности.<br>
D. Modification прекращается сразу после выхода из source region.

**Правильный ответ:** A.

**Почему:** Heating/cooling and moisture exchange меняют stability и low-level weather после ухода из source region (`SRC-FAA-AWH-28B-2026`).

**Почему главный отвлекающий вариант неверен:** D отрицает непрерывный surface exchange и evolution атмосферы (`SRC-FAA-AWH-28B-2026`).

### Q-MET-017 — Что означает stationary front для пилота? {#q-met-017}

A. Граница перемещается мало, но weather вдоль неё всё равно развивается.<br>
B. Ветер и осадки полностью отсутствуют.<br>
C. Front исчез из прогноза и больше не требует контроля.<br>
D. Любой маршрут параллельно границе автоматически безопасен.

**Правильный ответ:** A.

**Почему:** Малое displacement не отменяет cloud, precipitation, waves или local movement along the boundary.

**Почему главный отвлекающий вариант неверен:** B смешивает скорость перемещения границы с интенсивностью weather processes (`SRC-FAA-AWH-28B-2026`).

### Q-MET-018 — Как использовать близко расположенные isobars на surface chart? {#q-met-018}

A. Как признак сильного pressure gradient, затем учесть friction, stability и terrain.<br>
B. Как точную crosswind component для каждой ВПП.<br>
C. Как доказательство отсутствия gusts.<br>
D. Как замену актуальному wind report.

**Правильный ответ:** A.

**Почему:** Isobar spacing сообщает крупномасштабный gradient, но local surface flow формируется дополнительными процессами.

**Почему главный отвлекающий вариант неверен:** B пытается получить локальную составляющую без направления ВПП и local wind (`SRC-FAA-AWH-28B-2026`).

### Q-MET-019 — Почему conceptual front diagram нельзя использовать как forecast? {#q-met-019}

A. Реальные systems трёхмерны, меняются и требуют valid operational products.<br>
B. Diagram не содержит названия учебной главы.<br>
C. Любой front существует только на поверхности.<br>
D. Forecast всегда повторяет textbook shape без отклонений.

**Правильный ответ:** A.

**Почему:** Conceptual model объясняет relations, а timing/location/intensity приходят из current forecast and observations.

**Почему главный отвлекающий вариант неверен:** D уничтожает uncertainty и игнорирует deformation реальных systems (`SRC-FAA-AWH-28B-2026`).

### Q-MET-020 — Как безопасно использовать климатологический pattern для Испании? {#q-met-020}

A. Сформировать вопросы к briefing и проверить их текущими products.<br>
B. Принять pattern за forecast конкретного дня.<br>
C. Отменить проверку route после совпадения сезона.<br>
D. Назначить из него универсальный wind limit для [ULM][ulm].

**Правильный ответ:** A.

**Почему:** Climatology даёт предварительное ожидание, но decision требует valid-time AEMET/[AIP][aip] information.

**Почему главный отвлекающий вариант неверен:** B подменяет вероятностную многолетнюю картину конкретным состоянием атмосферы.

## Источники {#sources}

- `SRC-FAA-AWH-28B-2026` — стабильная физика air masses, fronts и wave-cyclone model; проверено 2026-07-13.
- `SRC-AEMET-GUIA-MET-2025` — испанские chart/products; проверено 2026-07-13.
- `SRC-ENAIRE-AIP-GEN-3-5-2026` — динамическая метеослужба Испании; проверено 2026-07-13.
- `SRC-EASA-AIR-OPS-2026` — будущий Part-NCO layer; проверено 2026-07-13.

[ulm]: ../reference/glossary.md#term-ulm
[lapl]: ../reference/glossary.md#term-lapl-a
[ppl]: ../reference/glossary.md#term-ppl-a
[part-fcl]: ../reference/glossary.md#term-part-fcl
[afm]: ../reference/glossary.md#term-afm
[poh]: ../reference/glossary.md#term-poh
[vmc]: ../reference/glossary.md#term-vmc
[aip]: ../reference/glossary.md#term-aip
