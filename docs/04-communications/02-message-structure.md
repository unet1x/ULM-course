# Структура сообщения и контроль понимания {#message-control}

## Назначение {#purpose}

Глава учит строить короткое сообщение, различать подтверждение и обязательный повтор, а при неопределённости останавливать safety-critical действие. Для [ULM](../reference/glossary.md#term-ulm) в Испании это прежде всего навык работы вне [controlled airspace](../reference/glossary.md#term-controlled-airspace); controlled examples заранее готовят к последующему [LAPL(A)](../reference/glossary.md#term-lapl-a)/[PPL(A)](../reference/glossary.md#term-ppl-a).

## Результаты обучения {#outcomes}

Вы сможете выбрать нужные поля сообщения, повторить обязательные элементы, корректно использовать `ROGER`, `WILCO`, `AFFIRM`, `NEGATIVE`, `SAY AGAIN`, исправить ошибку и перейти к ясной нестандартной речи без выдуманной фразы.

## Карта применимости {#applicability}

| Метка | Как использовать главу |
|---|---|
| [ULM — ОСНОВА][ulm] | Точность сообщения и контроль понимания. |
| [ULM — ОСОБО ВАЖНО][ulm] | Не считать передачу разрешением пространства. |
| [PART-FCL — ОБЩЕЕ][part-fcl] | [SERA](../reference/glossary.md#term-sera) [readback](../reference/glossary.md#term-readback) rules применимы по контексту. |
| [LAPL — ПЕРЕХОД] | Практиковать с [DTO](../reference/glossary.md#term-dto) на фактическом языке R/T. |
| [PPL — РАСШИРЕНИЕ] | Добавить более сложные ATS exchanges без потери структуры. |
| [ИСПАНИЯ] | Испанские пары проверять по RCA/[AIP](../reference/glossary.md#term-aip). |
| [БЕЗОПАСНОСТЬ] | Неясное runway/level сообщение не исполняется. |
| [ПРОВЕРИТЬ ПЕРЕД ПОЛЁТОМ] | Service type, [callsign](../reference/glossary.md#term-callsign), маршрут, уровень и expected points. |

## Теория {#theory}

![Поток подготовки, классификации ответа, обязательного повтора и остановки при неопределённости](../assets/diagrams/radio-message-flow.svg)

### Каркас сообщения {#message-structure}

Сначала слушайте. Начальный вызов обычно содержит адресата, полный позывной, при необходимости тип/позицию/уровень, намерение и релевантную информацию. Последующие сообщения короче. Каждое сообщение не обязано иметь одинаковые поля: передают только нужное для текущей цели, не скрывая критичный контекст.

Шаблон мышления, а не универсальный script:

1. **Кому:** правильная станция или traffic.
2. **Кто:** полный/разрешённо сокращённый позывной.
3. **Где/на каком уровне:** когда это нужно для идентификации и конфликта.
4. **Что происходит:** факт, запрос или намерение.
5. **Что нужно:** одна ясная цель.

### Подтверждение и обязательный повтор {#mandatory-readback}

[Обязательный повтор принятого элемента (English: readback; español: colación)][readback] позволяет controller проверить точность. [Подтверждение приёма (English: acknowledgement; español: acuse de recibo)][acknowledgement] лишь показывает, что сообщение принято. `ROGER` не является полным обязательным повтором; `WILCO` означает will comply, но не заменяет повтор элементов, которые [SERA](../reference/glossary.md#term-sera) требует вернуть.

По [SERA](../reference/glossary.md#term-sera).8015(e) flight crew повторяет safety-related части ATC clearances/instructions, переданные голосом. Всегда повторяются: ATC route clearances; clearances/instructions войти на ВПП, приземлиться, взлететь, остановиться перед ВПП, пересечь, рулить и выполнить backtrack по ВПП; используемая ВПП; altimeter settings; SSR codes; level, heading и speed instructions; transition levels, когда они выданы controller или содержатся в ATIS. Остальные clearances/instructions подтверждают так, чтобы показать понимание. Controller слушает повтор и немедленно исправляет расхождение. Источник: `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).8015(e) и GM (проверено 2026-07-13).

### Слова управления диалогом {#standard-words}

| Слово | Смысл | Не означает |
|---|---|---|
| `ROGER / RECIBIDO` | сообщение принято | обязательные элементы повторены |
| `WILCO / CUMPLIRÉ` | сообщение понято и будет выполнено | автоматическое право на runway action |
| `AFFIRM / AFIRMO` | да | согласие с неясной формулировкой |
| `NEGATIVE / NEGATIVO` | нет, либо permission not granted | «я не понял» |
| `SAY AGAIN / REPITA` | повторите всё/указанную часть | «разрешение можно угадать» |
| `STANDBY / ESPERE` | ждите следующего вызова | approval или clearance |

`TAKE-OFF` используют только в формуле разрешения на взлёт или его отмены; в других контекстах — `DEPARTURE`, чтобы не создавать ложное распознавание clearance. Источники: `SRC-BOE-RD-1180-2018` Annex V, `SRC-EASA-SERA-2025` (проверено 2026-07-13).

### Исправление, повтор и fallback {#plain-language}

Если пилот оговорился: `CORRECTION / CORRECCIÓN`, затем правильный элемент. Если непонятна часть: `SAY AGAIN [ITEM] / REPITA [ELEMENTO]`. [Ясная нестандартная речь (English: plain language; español: lenguaje claro)][plain-language] используется, когда standard phraseology недостаточна: коротко опишите факт и нужную помощь. Нельзя смешивать English и español как импровизированный гибрид; лучше объявить, что не поняли, замедлить обмен и использовать один поддерживаемый язык.

## Применение для [ULM](../reference/glossary.md#term-ulm) {#ulm-application}

Национальный [ULM](../reference/glossary.md#term-ulm)/[MAF](../reference/glossary.md#term-maf)+RTC в Испании не получает через правильную фразеологию доступ в [controlled airspace](../reference/glossary.md#term-controlled-airspace). Пока не выполнено отдельное условие [Part-FCL](../reference/glossary.md#term-part-fcl) из RD 765/2022 art. 4.1(d), controlled exchanges здесь — учебная подготовка, а первичная практика выполняется в разрешённой школе/операции. Источники: `SRC-BOE-RD-765-2022`, `SRC-AESA-ULM-RTC-PROGRAM` (проверено 2026-07-13).

## Расширение [Part-FCL](../reference/glossary.md#term-part-fcl) {#part-fcl-extension}

Для [LAPL(A)](../reference/glossary.md#term-lapl-a)/[PPL(A)](../reference/glossary.md#term-ppl-a) экзамен Communications проверяет знания; Spanish/English R/T annotation требует соответствующего экзамена и двусторонней связи на [skill test](../reference/glossary.md#term-skill-test)/proficiency check; языковая оценка FCL.055 остаётся отдельной. Эти три условия не превращаются одно в другое. Источники: `SRC-EASA-AIRCREW-2026`, `SRC-BOE-FOM-1146-2019` arts. 2–4, 7–9 (проверено 2026-07-13).

## Учебные сценарии {#training-scenarios}

### Сценарий RTC-03 — Первый controlled вызов {#scenario-rtc-03}

СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ СЦЕНАРИЙ — НЕ ДЛЯ ПОЛЁТА

**Тип обслуживания:** controlled ATS; later [Part-FCL](../reference/glossary.md#term-part-fcl) training.<br>
**Контекст:** aircraft outside manoeuvring area, current station and language known.<br>
**English:** Pilot: `[STATION], [FULL CALLSIGN], [TYPE], AT [POSITION], REQUEST [INTENTION]`; station: `[FULL CALLSIGN], PASS YOUR MESSAGE`.<br>
**Español:** Piloto: `[STATION], [FULL CALLSIGN], [TYPE], EN [POSITION], SOLICITO [INTENTION]`; estación: `[FULL CALLSIGN], ADELANTE`.<br>
**Пояснение:** вызов устанавливает контакт и предлагает одну цель; он ещё не является clearance.<br>
**[Readback][readback]/[acknowledgement][acknowledgement]:** `PASS YOUR MESSAGE/ADELANTE` подтверждает готовность слушать; обязательных runway элементов пока нет.<br>
**Решение при сомнении:** если station identity или ответ неясен, запросите повтор и не начинайте movement.<br>
Источник: `SRC-BOE-RD-1180-2018` Annex V, `SRC-ENAIRE-AIP-GEN-3-4-2026` (проверено 2026-07-13).

### Сценарий RTC-04 — Непонятное safety-critical указание {#scenario-rtc-04}

СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ СЦЕНАРИЙ — НЕ ДЛЯ ПОЛЁТА

**Тип обслуживания:** controlled ATS.<br>
**Контекст:** получена неразборчивая часть runway instruction.<br>
**English:** Pilot: `[CALLSIGN], SAY AGAIN RUNWAY INSTRUCTION`; station: `[CALLSIGN], HOLD SHORT RUNWAY [RUNWAY]`; pilot: `HOLD SHORT RUNWAY [RUNWAY], [CALLSIGN]`.<br>
**Español:** Piloto: `[CALLSIGN], REPITA INSTRUCCIÓN DE PISTA`; estación: `[CALLSIGN], MANTENGA FUERA DE PISTA [RUNWAY]`; piloto: `MANTENGO FUERA DE PISTA [RUNWAY], [CALLSIGN]`.<br>
**Пояснение:** пилот не достраивает потерянное слово и получает однозначное ограничение.<br>
**[Readback][readback]/[acknowledgement][acknowledgement]:** runway hold-short instruction повторяется полностью с designator.<br>
**Решение при сомнении:** остановитесь до точки ожидания; если повтор снова неясен, сообщите `UNABLE TO UNDERSTAND / NO COMPRENDO` и ждите.<br>
Источник: `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).8015(e), `SRC-BOE-RD-1180-2018` Annex V (проверено 2026-07-13).

## Безопасность {#safety}

Неиспользованный PTT, stuck microphone и одновременные передачи могут создать «правдоподобный» обрыв. Неразборчивое runway clearance нельзя дополнять по ожиданию. `STANDBY` не является одобрением. Traffic information не является [ATC clearance](../reference/glossary.md#term-atc-clearance).

## Типичные ошибки {#common-errors}

1. Отвечать `ROGER` на clearance, требующий полного повтора.
2. Повторять только цифры, но терять действие или unit/context.
3. Считать каждое сообщение пятистрочным докладом.
4. Исправлять оговорку длинным объяснением вместо `CORRECTION`.
5. Угадывать слово из ожидаемой процедуры.

## Конспект {#summary}

- Структура зависит от цели сообщения.
- Critical ATC items повторяются точно.
- `ROGER` подтверждает приём, а не содержание обязательного повтора.
- Неясность требует `SAY AGAIN`, clarification и остановки действия.
- Standard phraseology дополняется ясной речью, когда это необходимо.

## Контрольные вопросы {#review-questions}

### Q-RTC-006 — Какой ответ достаточен на указание остановиться перед конкретной ВПП? {#q-rtc-006}

A. `ROGER` без других элементов.<br>
B. Полный повтор действия и designator ВПП с позывным.<br>
C. Только собственный позывной.<br>
D. Сообщение о предполагаемом времени вылета.

**Правильный ответ:** B.

**Почему:** [SERA](../reference/glossary.md#term-sera).8015(e) включает runway hold-short instruction в safety-related элементы обязательного повтора.

**Почему главный отвлекающий вариант неверен:** По [SERA](../reference/glossary.md#term-sera).8015(e) один `ROGER` подтверждает приём, но не показывает, какая ВПП и какое ограничение поняты.

### Q-RTC-007 — Что пилот делает, если потерял одно слово runway instruction? {#q-rtc-007}

A. Восстанавливает его из привычной процедуры.<br>
B. Просит повторить конкретный элемент и не выполняет действие до ясности.<br>
C. Выполняет наиболее вероятный вариант на малой скорости.<br>
D. Переключает язык внутри фразы без уведомления станции.

**Правильный ответ:** B.

**Почему:** Clarification до movement устраняет риск runway incursion и сохраняет однозначный контекст.

**Почему главный отвлекающий вариант неверен:** A превращает ожидание пилота в выдуманное разрешение, которого станция могла не выдавать.

### Q-RTC-008 — Каково точное значение `STANDBY`? {#q-rtc-008}

A. Запрос одобрен, начинайте действие.<br>
B. Ждите следующего вызова; разрешение ещё не выдано.<br>
C. Частота освобождена навсегда.<br>
D. Воздушное судно получило приоритет.

**Правильный ответ:** B.

**Почему:** `STANDBY` управляет очередностью связи и не содержит operational approval.

**Почему главный отвлекающий вариант неверен:** A ошибочно превращает `STANDBY`, то есть ожидание ответа, в положительное clearance.

### Q-RTC-009 — Когда уместна ясная нестандартная речь? {#q-rtc-009}

A. Всегда вместо известной standard phraseology.<br>
B. Когда стандартной формулы недостаточно, чтобы однозначно описать факт или нужную помощь.<br>
C. Только для сообщений без позывного.<br>
D. Для свободного смешивания двух языков в одном предложении.

**Правильный ответ:** B.

**Почему:** Ясная нестандартная речь ([plain language](../reference/glossary.md#term-plain-language)) закрывает смысловой пробел, сохраняя краткость и один поддерживаемый язык.

**Почему главный отвлекающий вариант неверен:** A убирает общую предсказуемую структуру даже там, где standard phraseology точна.

### Q-RTC-010 — Какие поля нужно передавать в каждом радиосообщении? {#q-rtc-010}

A. Всегда адресат, тип, маршрут, топливо, пассажиров и погоду.<br>
B. Только поля, нужные для текущей цели и однозначного понимания, сохраняя обязательные элементы.<br>
C. Одни и те же пять полей независимо от этапа полёта.<br>
D. Только позывной, потому что станция знает остальное.

**Правильный ответ:** B.

**Почему:** Message structure масштабируется по контексту: initial call обычно полнее, а последующий exchange короче.

**Почему главный отвлекающий вариант неверен:** C перегружает канал и не учитывает различие между первым вызовом, повтором и коротким report.

## Источники {#sources}

- `SRC-EASA-SERA-2025` — [SERA](../reference/glossary.md#term-sera).8015(e), [SERA](../reference/glossary.md#term-sera).14045–14075.
- `SRC-BOE-RD-1180-2018` — Annex V, open ES/EN phrase pairs.
- `SRC-ENAIRE-AIP-GEN-3-4-2026` — Spanish communication/language context.
- `SRC-BOE-RD-765-2022` — условие входа [ULM](../reference/glossary.md#term-ulm) в контролируемое пространство.
- `SRC-EASA-AIRCREW-2026`, `SRC-BOE-FOM-1146-2019` — later [Part-FCL](../reference/glossary.md#term-part-fcl) distinctions.

[readback]: ../reference/glossary.md#term-readback
[acknowledgement]: ../reference/glossary.md#term-acknowledgement
[plain-language]: ../reference/glossary.md#term-plain-language
[ulm]: ../reference/glossary.md#term-ulm
[part-fcl]: ../reference/glossary.md#term-part-fcl
