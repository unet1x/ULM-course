# Вода, облака и видимость {#water-clouds-visibility}

## Зачем эта глава {#purpose}

Влага становится авиационной угрозой через облака, туман, осадки, ухудшение видимости и обледенение. Пилот должен понимать процесс, но принимать решение по текущим продуктам и применимым [VMC][vmc], а не по одной эмпирической формуле.

## Результаты обучения {#outcomes}

После главы вы сможете:

1. связать humidity, dew point, saturation и подъём воздуха;
2. различать десять WMO cloud genera и значимые авиационные признаки;
3. объяснить radiation, advection, upslope и evaporation fog;
4. отличать horizontal от slant visibility;
5. правильно ограничить смысл [CAVOK][cavok].

## Карта применимости {#applicability}

| Метка | Как использовать главу |
|---|---|
| [ULM — ОСНОВА][ulm] | Основной слой для day [VFR][vfr]/[VMC][vmc] в Испании. |
| [ULM — ОСОБО ВАЖНО][ulm] | Туман, низкий stratus и mountain obscuration быстро убирают путь отхода. |
| [PART-FCL — ОБЩЕЕ][part-fcl] | Физика общая для будущих [LAPL(A)][lapl]/[PPL(A)][ppl]. |
| [LAPL — ПЕРЕХОД][lapl] | Позднее свяжите облачность с Part-NCO planning. |
| [PPL — РАСШИРЕНИЕ][ppl] | Та же оценка, без предположения instrument privilege. |
| [ИСПАНИЯ] | Point reports дополняются route/area products AEMET. |
| [БЕЗОПАСНОСТЬ] | [CAVOK][cavok] не означает ясное небо или автоматическую безопасность. |
| [ПРОВЕРИТЬ ПЕРЕД ПОЛЁТОМ] | Visibility, cloud base/amount, terrain obscuration, [TREND][trend] и escape route. |

## Теория {#theory}

### Влажность, dew point и насыщение {#humidity-dew-point}

Relative humidity показывает близость воздуха к насыщению при текущей температуре. Dew point — температура, до которой воздух надо охладить при оговорённых условиях, чтобы достичь насыщения. Малый temperature–dew-point spread указывает на близость к насыщению, но сам не даёт точное время, base или тип облака. Стабильная физика: `SRC-FAA-AWH-28B-2026` (проверено 2026-07-13).

### Подъём и устойчивость {#lifting-saturation}

Воздух охлаждается при расширении во время подъёма. Подъём создают конвекция, front, orography и convergence. Если parcel достигает насыщения, конденсация образует droplets/ice при наличии подходящих nuclei. Форма и вертикальное развитие зависят от moisture и stability, поэтому одинаковый surface spread не гарантирует одинаковую облачность. Источник физики: `SRC-FAA-AWH-28B-2026` (проверено 2026-07-13).

### Десять родов облаков WMO {#cloud-genera}

International Cloud Atlas различает Cirrus, Cirrocumulus, Cirrostratus, Altocumulus, Altostratus, Nimbostratus, Stratocumulus, Stratus, Cumulus и Cumulonimbus. Это морфологическая классификация: для полёта дополнительно важны amount, base/top, vertical development, precipitation, icing/turbulence и связь с terrain. Первичный источник классификации: `SRC-WMO-CLOUD-ATLAS-2017` (проверено 2026-07-13).

### Авиационно значимая облачность {#aviation-significant-cloud}

Low BKN/OVC может создать ceiling и закрыть terrain; TCU/CB указывает на глубокую convection; embedded cloud скрывает развитие; orographic cap может обозначать влажный подъём и нисходящие процессы с lee side. Отсутствие clouds в одном report не доказывает отсутствие cloud по маршруту. Испанское кодирование: `SRC-AEMET-CODE-FORMS-2021`, `SRC-AEMET-GUIA-MET-2025` (проверено 2026-07-13).

### Туман и низкий stratus {#fog}

- radiation fog формируется при охлаждении поверхности и слабом перемешивании;
- advection fog/stratus — при переносе влажного воздуха над более холодной поверхностью;
- upslope fog — при подъёме влажного потока по рельефу;
- evaporation/steam fog — при добавлении влаги в холодный воздух над более тёплой водой.

Условия могут сочетаться и изменяться после sunrise неравномерно. «Солнце сожжёт туман» — не operational trigger. Стабильная физика: `SRC-FAA-AWH-28B-2026` (проверено 2026-07-13).

### Осадки и видимость {#precipitation-visibility}

Rain, drizzle, snow и showers отличаются процессом и влиянием. Horizontal visibility измеряется по горизонтальному обзору у поверхности; slant visibility с воздуха может быть хуже из-за солнца, haze, precipitation и контраста фона. Достаточное число в aerodrome report не гарантирует видимость рельефа на солнце или под rain shaft. Источник: `SRC-AEMET-GUIA-MET-2025` (проверено 2026-07-13).

### Ограниченный смысл [CAVOK][cavok] {#cavok}

[CAVOK][cavok] заменяет группы visibility, weather и cloud только при выполнении кодовых критериев в точке и момент наблюдения/прогноза. Он допускает облака выше порога значимости, не описывает route, terrain contrast, glare, turbulence, wave или future change outside the product. [CAVOK][cavok] не означает ясное небо или автоматическую безопасность. Кодовые критерии: `SRC-AEMET-CODE-FORMS-2021`, `SRC-AEMET-GUIA-MET-2025` (проверено 2026-07-13).

### Учебный расчёт MET-CALC-05 — приближение cloud base {#met-calc-05}

**Дано:** surface temperature 24 °C; dew point 16 °C; учебный коэффициент 400 ft/°C.

**Формула:** `approximate convective cloud base AGL ≈ (T − Td) × 400`.

**Расчёт:** `(24 − 16) × 400 = 3200 ft AGL`.

**Результат:** грубая оценка около 3200 ft AGL для хорошо перемешанного convective boundary layer.

**Решение пилота:** не использовать число для dispatch; проверить observed/forecast cloud, terrain и [TREND][trend]. Допущения — mixed layer, surface parcel и эмпирический коэффициент; это приближение не является прогнозом, фактической cloud base или значением [AFM][afm]. Источник физики: `SRC-FAA-AWH-28B-2026` (проверено 2026-07-13).

### Сценарий ESP-MET-02 — Кантабрийское побережье: advection fog и stratus {#scenario-esp-met-02}

Влажный морской поток идёт к более холодному побережью и склонам. Кантабрийский адвективный туман и стратус способны закрыть берег и повыситься по рельефу, пока inland report выглядит лучше. Это климатологическая ориентация, не прогноз; нужны route products, point observations и escape criteria. Источники: `SRC-AEMET-GUIA-MET-2025`, `SRC-AEMET-AERODROME-GUIDES` (проверено 2026-07-13).

### Сценарий ESP-MET-03 — Месета: инверсия и radiation fog {#scenario-esp-met-03}

После ясной спокойной ночи Meseta может получить surface inversion, radiation fog или low stratus в низинах. Один солнечный склон не доказывает очистку маршрута; basin visibility может сохраняться хуже. Это климатологическая ориентация, не прогноз. Источники: `SRC-AEMET-GUIA-MET-2025`, `SRC-FAA-AWH-28B-2026` (проверено 2026-07-13).

## Применение к [ULM][ulm] {#ulm-application}

Для [ULM][ulm] в Испании сравнивают law/[VMC][vmc], [AFM][afm]/[POH][poh], school/aerodrome limits и [личные минимумы (personal minima)][personal-minima]. Нет универсального лимита [ULM][ulm] по visibility или cloud base, создаваемого этим курсом. Числовая законность не делает slant visibility или terrain clearance подходящими. Источник правовой границы: `SRC-BOE-RD-765-2022` (проверено 2026-07-13).

## Расширение LAPL/PPL {#part-fcl-extension}

Будущие [LAPL(A)][lapl]/[PPL(A)][ppl] требуют связать point observations с forecast и route. Это не обучение полёту по приборам и не разрешение продолжать [VFR][vfr] в [IMC][imc]. Источники: `SRC-EASA-AIRCREW-2026`, `SRC-EASA-AIR-OPS-2026` (проверено 2026-07-13).

## Безопасность {#safety}

Если cloud/visibility лишают проверенного разворота, запасного аэродрома или визуального контакта с terrain, решение принимают до входа в сужающийся коридор. Формула dew-point spread не отменяет observation и forecast.

## Типичные ошибки {#common-errors}

1. Читать dew-point spread как точную cloud base.
2. Приравнивать [CAVOK][cavok] к clear and safe.
3. Использовать aerodrome visibility как route visibility.
4. Ожидать гарантированного рассеивания fog по времени sunrise.
5. Игнорировать slant visibility и terrain contrast.

## Краткий конспект {#summary}

- Saturation возникает через cooling или moisture addition.
- Cloud genus не исчерпывает авиационную угрозу.
- Fog mechanisms могут сочетаться.
- [CAVOK][cavok] — кодовая свёртка, не go decision.

## Контрольные вопросы {#review-questions}

### Q-MET-011 — Что показывает малый spread между температурой и dew point? {#q-met-011}

A. Воздух близок к насыщению при текущих условиях, но точная cloud base не задана.<br>
B. Гроза обязательно начнётся в течение часа.<br>
C. Horizontal visibility обязательно равна slant visibility.<br>
D. Все облака находятся ниже circuit height.

**Правильный ответ:** A.

**Почему:** Spread — индикатор близости к saturation, тогда как lifting, mixing и moisture profile определяют фактический результат.

**Почему главный отвлекающий вариант неверен:** B приписывает одному surface параметру время и convective development, которых он не содержит (`SRC-FAA-AWH-28B-2026`).

### Q-MET-012 — Как использовать классификацию WMO cloud genera в авиационном решении? {#q-met-012}

A. Дополнить genus данными amount, base/top, development, precipitation и hazards.<br>
B. Считать одинаково безопасными все облака одного рода.<br>
C. Заменить ею current report и forecast.<br>
D. Определить legal minima только по форме облака.

**Правильный ответ:** A.

**Почему:** International Cloud Atlas классифицирует morphology; operational significance требует дополнительных параметров (`SRC-WMO-CLOUD-ATLAS-2017`).

**Почему главный отвлекающий вариант неверен:** B игнорирует vertical extent, embedded convection и положение относительно terrain (`SRC-WMO-CLOUD-ATLAS-2017`).

### Q-MET-013 — Почему [CAVOK][cavok] не является самостоятельным разрешением лететь? {#q-met-013}

A. Он ограничен кодовыми критериями, точкой/периодом продукта и не описывает все route hazards.<br>
B. Он всегда означает visibility ниже 1000 m.<br>
C. Он относится только к полётам по приборам.<br>
D. Он отменяет проверку ветра и характеристик.

**Правильный ответ:** A.

**Почему:** [CAVOK][cavok] сворачивает три группы при заданных условиях, но не сообщает turbulence, route evolution или suitability (`SRC-AEMET-CODE-FORMS-2021`).

**Почему главный отвлекающий вариант неверен:** D превращает ограниченный weather code в полное dispatch decision.

### Q-MET-014 — В чём риск переноса aerodrome horizontal visibility на горный маршрут? {#q-met-014}

A. Slant view, precipitation, glare и terrain cloud могут дать существенно худшую картину.<br>
B. Aerodrome visibility измеряет только температуру.<br>
C. Terrain не влияет на cloud или contrast.<br>
D. Любая опубликованная visibility действует на всю FIR.

**Правильный ответ:** A.

**Почему:** Point measurement описывает конкретную окрестность, а visual acquisition terrain зависит от направления обзора и среды.

**Почему главный отвлекающий вариант неверен:** D игнорирует пространственную изменчивость и назначение аэродромного наблюдения (`SRC-AEMET-GUIA-MET-2025`).

### Q-MET-015 — Почему нельзя обещать рассеивание radiation fog сразу после sunrise? {#q-met-015}

A. Скорость прогрева, ветер, moisture depth и облачный экран меняются от ситуации к ситуации.<br>
B. Sunrise всегда усиливает saturation.<br>
C. Radiation fog образуется только над морем.<br>
D. После sunrise observation перестают выпускать.

**Правильный ответ:** A.

**Почему:** Fog dissipation зависит от energy and mixing balance, поэтому [TREND][trend] подтверждается текущими products (`SRC-FAA-AWH-28B-2026`).

**Почему главный отвлекающий вариант неверен:** C смешивает radiation cooling over land с advection fog mechanisms.

## Источники {#sources}

- `SRC-WMO-CLOUD-ATLAS-2017` — официальная классификация cloud genera; проверено 2026-07-13.
- `SRC-AEMET-GUIA-MET-2025`, `SRC-AEMET-CODE-FORMS-2021`, `SRC-AEMET-AERODROME-GUIDES` — кодирование и испанские продукты; проверено 2026-07-13.
- `SRC-FAA-AWH-28B-2026` — стабильная физика water, cloud, fog; проверено 2026-07-13.
- `SRC-BOE-RD-765-2022`, `SRC-EASA-AIR-OPS-2026` — раздельные эксплуатационные слои; проверено 2026-07-13.

[cavok]: ../reference/glossary.md#term-cavok
[ulm]: ../reference/glossary.md#term-ulm
[lapl]: ../reference/glossary.md#term-lapl-a
[ppl]: ../reference/glossary.md#term-ppl-a
[part-fcl]: ../reference/glossary.md#term-part-fcl
[afm]: ../reference/glossary.md#term-afm
[poh]: ../reference/glossary.md#term-poh
[vfr]: ../reference/glossary.md#term-vfr
[vmc]: ../reference/glossary.md#term-vmc
[imc]: ../reference/glossary.md#term-imc
[trend]: ../reference/glossary.md#term-trend
[personal-minima]: ../reference/glossary.md#term-personal-minima
