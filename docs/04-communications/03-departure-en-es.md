# Вылет: English и español {#departure-en-es}

## Назначение {#purpose}

Эта глава разбирает controlled departure от taxi request до frequency change. Для первоначального [ULM](../reference/glossary.md#term-ulm)/[MAF](../reference/glossary.md#term-maf) в Испании сценарии служат подготовкой и не отменяют ограничение [controlled airspace](../reference/glossary.md#term-controlled-airspace); практическое выполнение требует применимых [Part-FCL](../reference/glossary.md#term-part-fcl) privileges, оборудования и actual clearance. Позже блок прямо используется в [LAPL(A)](../reference/glossary.md#term-lapl-a)/[PPL(A)](../reference/glossary.md#term-ppl-a) training.

## Результаты обучения {#outcomes}

Вы сможете отличить taxi information от clearance, разобрать conditional clearance, полностью повторить runway instruction, распознать защищённое слово `TAKE-OFF` и сообщить departure без превращения self-announcement в разрешение.

## Карта применимости {#applicability}

| Метка | Как использовать главу |
|---|---|
| [ULM — ОСНОВА][ulm] | Понимать runway safety и local aerodrome procedure. |
| [ULM — ОСОБО ВАЖНО][ulm] | Controlled examples не расширяют national licence. |
| [PART-FCL — ОБЩЕЕ][part-fcl] | Практика ATC departure для будущей лицензии. |
| [LAPL — ПЕРЕХОД] | Отрабатывать в [DTO](../reference/glossary.md#term-dto) с instructor. |
| [PPL — РАСШИРЕНИЕ] | Добавить complex ground routing и controlled departures. |
| [ИСПАНИЯ] | Использовать актуальные AD/[AIP](../reference/glossary.md#term-aip) phraseology и layout. |
| [БЕЗОПАСНОСТЬ] | Не пересекать/занимать ВПП без понятного clearance. |
| [ПРОВЕРИТЬ ПЕРЕД ПОЛЁТОМ] | Runway, holding points, hotspots, [NOTAM](../reference/glossary.md#term-notam), frequency. |

## Теория {#theory}

### Controlled departure как последовательность {#controlled-departure}

[ATC][atc] разделяет этапы: start-up, taxi, holding point, runway entry/crossing, line-up, take-off, departure and transfer. Наличие одного clearance не разрешает следующий этап. Taxi clearance не включает runway crossing, если это не выражено ясно. Runway designator и действие повторяют.

В Spanish и English допускаются только опубликованные/context-appropriate формы. Таблицы ниже — синтетические placeholders, не local procedure. Текущие [AIP](../reference/glossary.md#term-aip) España, [NOTAM](../reference/glossary.md#term-notam), chart, AD instructions и ATS direction имеют приоритет. Источники: `SRC-BOE-RD-1180-2018` Annex V, `SRC-ENAIRE-AIP-GEN-3-4-2026` (проверено 2026-07-13).

### Условное разрешение {#conditional-clearance}

Conditional clearance содержит: traffic identification, condition, clearance и краткое повторение condition. Пилот должен видеть указанный traffic и однозначно понимать, к кому относится condition. Примерная логика: `BEHIND [TRAFFIC], LINE UP BEHIND`; español: `DETRÁS DE [TRÁFICO], ALINEE DETRÁS`. Если traffic не identified, сообщите `NEGATIVE CONTACT / TRÁFICO NO A LA VISTA` и не действуйте. [SERA](../reference/glossary.md#term-sera).8015(e) требует повторить runway-related instruction, включая condition. Источник: `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).8015(e), `SRC-BOE-RD-1180-2018` Annex V (проверено 2026-07-13).

### Защищённое слово {#takeoff-word}

`TAKE-OFF / DESPEGUE` применяют только в take-off clearance или его cancellation. В других сообщениях говорят `DEPARTURE / SALIDA`. Эта дисциплина снижает риск принять fragment за clearance.

## Применение для [ULM](../reference/glossary.md#term-ulm) {#ulm-application}

[ULM](../reference/glossary.md#term-ulm)+[MAF](../reference/glossary.md#term-maf)+RTC без [Part-FCL](../reference/glossary.md#term-part-fcl) licence эквивалентной категории/класса недостаточны для [controlled airspace](../reference/glossary.md#term-controlled-airspace) с 1 апреля 2026. Эти exchanges изучаются сейчас, чтобы позже не переучиваться, но не дают права выполнить controlled departure. Источники: `SRC-BOE-RD-765-2022` art. 4.1(d), `SRC-BOE-RD-182-2026` art. 3 и disposición final 2.2 (проверено 2026-07-13).

## Расширение [Part-FCL](../reference/glossary.md#term-part-fcl) {#part-fcl-extension}

В [LAPL(A)](../reference/glossary.md#term-lapl-a)/[PPL(A)](../reference/glossary.md#term-ppl-a) training instructor связывает phraseology с actual aerodrome chart, clearances и workload. Communications exam, R/T annotation и FCL.055 остаются отдельными gates; national RTC не переносится автоматически. `SRC-EASA-AIRCREW-2026`, `SRC-BOE-FOM-1146-2019` (проверено 2026-07-13).

## Учебные сценарии {#training-scenarios}

### Сценарий RTC-05 — Taxi request {#scenario-rtc-05}

СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ СЦЕНАРИЙ — НЕ ДЛЯ ПОЛЁТА

**Тип обслуживания:** controlled ATS, ground/tower as published.<br>
**Контекст:** aircraft at `[PARKING]`, current information received, ready to taxi.<br>
**English:** Pilot: `[STATION], [CALLSIGN], AT [PARKING], INFORMATION [LETTER], REQUEST TAXI`; station: `[CALLSIGN], TAXI TO HOLDING POINT [POINT] RUNWAY [RUNWAY] VIA [ROUTE]`; pilot: `TAXI TO HOLDING POINT [POINT] RUNWAY [RUNWAY] VIA [ROUTE], [CALLSIGN]`.<br>
**Español:** Piloto: `[STATION], [CALLSIGN], EN [PARKING], INFORMACIÓN [LETTER], SOLICITO RODAJE`; estación: `[CALLSIGN], RUEDE A PUNTO DE ESPERA [POINT] PISTA [RUNWAY] VÍA [ROUTE]`; piloto: `RUEDE A PUNTO DE ESPERA [POINT] PISTA [RUNWAY] VÍA [ROUTE], [CALLSIGN]`.<br>
**Пояснение:** route заканчивается at holding point; runway crossing не подразумевается.<br>
**[Readback][readback]/[acknowledgement][acknowledgement]:** повторяются route, holding point и runway designator.<br>
**Решение при сомнении:** остановитесь в безопасном месте и запросите `SAY AGAIN TAXI ROUTE / REPITA RUTA DE RODAJE`.<br>
Источник: `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).8015(e), `SRC-BOE-RD-1180-2018` Annex V (проверено 2026-07-13).

### Сценарий RTC-06 — Conditional line-up {#scenario-rtc-06}

СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ СЦЕНАРИЙ — НЕ ДЛЯ ПОЛЁТА

**Тип обслуживания:** controlled ATS.<br>
**Контекст:** pilot visual with specified landing traffic at holding point.<br>
**English:** Station: `[CALLSIGN], BEHIND LANDING [TRAFFIC], LINE UP RUNWAY [RUNWAY] BEHIND`; pilot: `BEHIND LANDING [TRAFFIC], LINE UP RUNWAY [RUNWAY] BEHIND, [CALLSIGN]`.<br>
**Español:** Estación: `[CALLSIGN], DETRÁS DEL [TRAFFIC] EN ATERRIZAJE, ALINEE PISTA [RUNWAY] DETRÁS`; piloto: `DETRÁS DEL [TRAFFIC] EN ATERRIZAJE, ALINEO PISTA [RUNWAY] DETRÁS, [CALLSIGN]`.<br>
**Пояснение:** condition исполняется только после identified traffic passes; это не take-off clearance.<br>
**[Readback][readback]/[acknowledgement][acknowledgement]:** traffic, condition, runway и line-up action повторяются полностью.<br>
**Решение при сомнении:** при потере visual contact оставайтесь before runway и сообщите `NEGATIVE CONTACT / TRÁFICO NO A LA VISTA`.<br>
Источник: `SRC-BOE-RD-1180-2018` Annex V, `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).8015(e) (проверено 2026-07-13).

### Сценарий RTC-07 — Line-up без взлёта {#scenario-rtc-07}

СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ СЦЕНАРИЙ — НЕ ДЛЯ ПОЛЁТА

**Тип обслуживания:** controlled ATS.<br>
**Контекст:** no conditional traffic; only runway entry and line-up are issued.<br>
**English:** Station: `[CALLSIGN], LINE UP AND WAIT RUNWAY [RUNWAY]`; pilot: `LINE UP AND WAIT RUNWAY [RUNWAY], [CALLSIGN]`.<br>
**Español:** Estación: `[CALLSIGN], ALINEE Y MANTENGA PISTA [RUNWAY]`; piloto: `ALINEO Y MANTENGO PISTA [RUNWAY], [CALLSIGN]`.<br>
**Пояснение:** пилот входит и ждёт; take-off ещё не разрешён.<br>
**[Readback][readback]/[acknowledgement][acknowledgement]:** действие и runway designator повторяются.<br>
**Решение при сомнении:** если слышен только fragment, hold short и запросите полное указание; не создавайте clearance самостоятельно.<br>
Источник: `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).8015(e), `SRC-BOE-RD-1180-2018` Annex V (проверено 2026-07-13).

### Сценарий RTC-08 — Take-off clearance {#scenario-rtc-08}

СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ СЦЕНАРИЙ — НЕ ДЛЯ ПОЛЁТА

**Тип обслуживания:** controlled ATS.<br>
**Контекст:** aircraft lined up, runway and aircraft checks complete.<br>
**English:** Station: `[CALLSIGN], RUNWAY [RUNWAY] CLEARED FOR TAKE-OFF [WIND]`; pilot: `RUNWAY [RUNWAY] CLEARED FOR TAKE-OFF, [CALLSIGN]`.<br>
**Español:** Estación: `[CALLSIGN], PISTA [RUNWAY] AUTORIZADO A DESPEGAR [WIND]`; piloto: `PISTA [RUNWAY] AUTORIZADO A DESPEGAR, [CALLSIGN]`.<br>
**Пояснение:** exact protected phrase authorises take-off, subject to pilot-in-command safety decision.<br>
**[Readback][readback]/[acknowledgement][acknowledgement]:** runway и clearance wording повторяются; wind information не превращает unsafe take-off в обязанность.<br>
**Решение при сомнении:** если runway/clearance unreadable or conditions unsafe, remain/stop as safely possible and say `UNABLE / IMPOSIBLE` with reason if time permits.<br>
Источник: `SRC-BOE-RD-1180-2018` Annex V exact ES/EN pair, `SRC-EASA-SERA-2025` (проверено 2026-07-13).

### Сценарий RTC-09 — Departure report и transfer {#scenario-rtc-09}

СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ СЦЕНАРИЙ — НЕ ДЛЯ ПОЛЁТА

**Тип обслуживания:** controlled ATS.<br>
**Контекст:** airborne, clear of immediate runway environment, reporting point assigned.<br>
**English:** Pilot: `[CALLSIGN], PASSING [POINT], [ALTITUDE], DEPARTURE [DIRECTION]`; station: `[CALLSIGN], CONTACT [NEXT STATION] [FREQUENCY]`; pilot: `CONTACT [NEXT STATION] [FREQUENCY], [CALLSIGN]`.<br>
**Español:** Piloto: `[CALLSIGN], PASANDO [POINT], [ALTITUDE], SALIDA [DIRECTION]`; estación: `[CALLSIGN], CONTACTE [NEXT STATION] [FREQUENCY]`; piloto: `CONTACTO [NEXT STATION] [FREQUENCY], [CALLSIGN]`.<br>
**Пояснение:** report locates aircraft; transfer assigns a new channel.<br>
**[Readback][readback]/[acknowledgement][acknowledgement]:** repeat next station/frequency; any level restriction remains in force until changed.<br>
**Решение при сомнении:** request frequency again before switching; if no contact after correct attempts, return to previous frequency when practicable and follow applicable procedure.<br>
Источник: `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).14060–14065, `SRC-ENAIRE-AIP-GEN-3-4-2026` (проверено 2026-07-13).

## Безопасность {#safety}

Self-announced `TAKING OFF` на A/A не является [ATC clearance](../reference/glossary.md#term-atc-clearance) и не должен копировать protected controlled phrase. В controlled ATS только однозначное clearance permits take-off; [PIC](../reference/glossary.md#term-pic) всё равно может отказаться, если runway, traffic или aircraft condition unsafe.

## Типичные ошибки {#common-errors}

1. Считать taxi clearance разрешением пересечь runway.
2. Повторить conditional clearance без visual identification traffic.
3. Принять line-up за take-off clearance.
4. Использовать `TAKE-OFF` в обычном departure request.
5. Переключиться на нерасслышанную частоту.

## Конспект {#summary}

- Каждый departure stage имеет отдельное разрешение.
- Conditional clearance требует identified traffic и полного повтора.
- `LINE UP AND WAIT` не разрешает взлёт.
- Только `CLEARED FOR TAKE-OFF / AUTORIZADO A DESPEGAR` — controlled take-off pair.
- Dynamic local data всегда проверяются перед полётом.

## Контрольные вопросы {#review-questions}

### Q-RTC-011 — Что разрешает taxi clearance до holding point ВПП? {#q-rtc-011}

A. Руление по указанному маршруту до holding point, но не пересечение ВПП без ясного указания.<br>
B. Пересечение любой ВПП по кратчайшему пути.<br>
C. Line-up и take-off, если traffic не виден.<br>
D. Выбор любой taxiway после начала движения.

**Правильный ответ:** A.

**Почему:** Taxi route имеет явный предел; runway crossing является отдельным safety-related instruction.

**Почему главный отвлекающий вариант неверен:** B добавляет runway authority, которой в clearance до holding point нет.

### Q-RTC-012 — Как действовать при conditional line-up, если указанное traffic не найдено визуально? {#q-rtc-012}

A. Выполнить условие по времени.<br>
B. Оставаться вне ВПП и сообщить negative contact.<br>
C. Следовать за любым похожим самолётом.<br>
D. Сократить condition при повторе.

**Правильный ответ:** B.

**Почему:** Conditional clearance опирается на однозначно identified traffic; без него condition не может безопасно сработать.

**Почему главный отвлекающий вариант неверен:** A нарушает условие conditional line-up: visual identification указанного traffic нельзя заменять предположением о последовательности.

### Q-RTC-013 — Что означает `LINE UP AND WAIT RUNWAY [RUNWAY]`? {#q-rtc-013}

A. Войти, выстроиться и ждать дальнейшего clearance.<br>
B. Взлететь без дополнительного сообщения.<br>
C. Пересечь ВПП и продолжить руление.<br>
D. Сообщить только departure direction.

**Правильный ответ:** A.

**Почему:** Line-up instruction разрешает runway entry/alignment, но protected take-off clearance отсутствует.

**Почему главный отвлекающий вариант неверен:** B смешивает два разных runway actions и пропускает обязательное take-off clearance.

### Q-RTC-014 — Почему слово `TAKE-OFF` ограничено clearance/cancellation? {#q-rtc-014}

A. Чтобы fragment обычного сообщения не был ошибочно принят за разрешение взлёта.<br>
B. Потому что departure reports запрещены после взлёта.<br>
C. Чтобы пилот не сообщал направление выхода.<br>
D. Потому что слово используется только в météo reports.

**Правильный ответ:** A.

**Почему:** Protected wording делает take-off clearance заметным и отличает его от `DEPARTURE` context.

**Почему главный отвлекающий вариант неверен:** B не связан с word discipline: departure report остаётся нормальной частью exchange.

### Q-RTC-015 — Имеет ли пилот право отказаться от выданного take-off clearance? {#q-rtc-015}

A. Нет, clearance отменяет ответственность [PIC](../reference/glossary.md#term-pic).<br>
B. Да, если aircraft/runway/traffic condition делает взлёт небезопасным; сообщить unable.<br>
C. Только после начала разбега.<br>
D. Только если изменена частота.

**Правильный ответ:** B.

**Почему:** [ATC clearance](../reference/glossary.md#term-atc-clearance) не отменяет safety decision pilot-in-command и состояние конкретного самолёта.

**Почему главный отвлекающий вариант неверен:** A ошибочно передаёт controller полномочия и ответственность [PIC](../reference/glossary.md#term-pic) за готовность aircraft и безопасное выполнение take-off clearance.

## Источники {#sources}

- `SRC-BOE-RD-1180-2018` — Annex V controlled ES/EN phrase pairs.
- `SRC-EASA-SERA-2025` — [SERA](../reference/glossary.md#term-sera).8015(e), communications transfer.
- `SRC-ENAIRE-AIP-GEN-3-4-2026` — dynamic Spanish communications context.
- `SRC-BOE-RD-765-2022`, `SRC-BOE-RD-182-2026` — условие входа [ULM](../reference/glossary.md#term-ulm) в контролируемое пространство.
- `SRC-EASA-AIRCREW-2026`, `SRC-BOE-FOM-1146-2019` — later LAPL/PPL radio gates.

[atc]: ../reference/glossary.md#term-air-traffic-control-atc
[readback]: ../reference/glossary.md#term-readback
[acknowledgement]: ../reference/glossary.md#term-acknowledgement
[ulm]: ../reference/glossary.md#term-ulm
[part-fcl]: ../reference/glossary.md#term-part-fcl
