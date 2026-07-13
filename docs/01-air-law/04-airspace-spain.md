# Воздушное пространство Испании: классы, зоны и аэродромы

## Зачем нужна эта глава

Цвет на moving map не является разрешением. Пилот должен понимать вертикальные и горизонтальные границы, класс, обслуживающий орган, активность временной зоны и собственные полномочия. Схема этой главы концептуальна; текущую структуру даёт только официальная AIS.

## Результаты обучения

Ученик сможет:

- описать классы A–G без принятия схемы за карту Испании;
- отличить controlled и uncontrolled airspace;
- распознать CTR/TMA/CTA и вертикальную границу;
- объяснить prohibited, restricted и danger areas;
- применить особое ограничение национальной лицензии [ULM][ulm].

## Карта применимости

| Метка | Как использовать главу |
|---|---|
| [ULM — ОСНОВА][ulm] | Планируйте первоначальные полёты вне [controlled airspace][controlled-airspace]. |
| [ULM — ОСОБО ВАЖНО][ulm] | Низкая масса не даёт исключения из границ или активных зон. |
| [PART-FCL — ОБЩЕЕ][part-fcl] | Классы и ATS services входят в общий последующий syllabus. |
| [LAPL — ПЕРЕХОД][lapl] | Лицензия должна сочетаться с radio/language и aircraft capability. |
| [PPL — РАСШИРЕНИЕ][ppl] | Углубляйте clearance, [flight plan][flight-plan] и controlled-aerodrome procedures. |
| [ИСПАНИЯ] | Текущая структура публикуется в [AIP][aip] España ENR/AD. |
| [БЕЗОПАСНОСТЬ] | Ошибка на 100 ft или в единице высоты может стать infringement. |
| [ПРОВЕРИТЬ ПЕРЕД ПОЛЁТОМ] | Границы, часы активности и [NOTAM][notam] меняются. |

## Класс — это набор услуг и требований {#norm-airspace-classes}

Классы [SERA][sera] A–G концептуально задают допуск IFR/[VFR][vfr], требования [ATC clearance][atc-clearance], separation и traffic information:

| Класс | [VFR][vfr] | Общая идея обслуживания |
|---|---|---|
| A | не допускается | только IFR, все под ATC и separated |
| B | допускается | IFR и [VFR][vfr] под ATC, все separated |
| C | допускается | IFR separated от IFR/[VFR][vfr]; [VFR][vfr] separated от IFR и получает traffic information о [VFR][vfr] |
| D | допускается | IFR separated от IFR; [VFR][vfr] получает traffic information, separation от другого [VFR][vfr] не гарантируется |
| E | допускается | IFR под ATC и separated от IFR; [VFR][vfr] обычно не требует clearance класса, traffic information насколько практически возможно |
| F | допускается | advisory service для IFR; flight information service по запросу |
| G | допускается | неконтролируемое пространство; flight information service по запросу |

Это учебное сравнение [SERA][sera], а не утверждение, что все классы используются в каждом районе Испании. Реальный класс и требования берутся из текущего [AIP][aip]/chart. Источники: `SRC-EASA-SERA-2025`, `SRC-ENAIRE-AIP-ESPANA` (проверено 13.07.2026).

![Концептуальное вертикальное устройство воздушного пространства, не навигационная карта](../assets/diagrams/airspace-structure.svg)

## Вертикальные и горизонтальные элементы

- **CTR — control zone:** [controlled airspace][controlled-airspace] от поверхности вокруг аэродрома.
- **CTA — control area:** [controlled airspace][controlled-airspace], начинающееся выше установленной нижней границы.
- **TMA — terminal control area:** control area для потоков к нескольким/крупным аэродромам.
- **Airway:** установленный коридор [controlled airspace][controlled-airspace].
- **FIR:** большой район flight information and alerting services; это не один класс от земли до верхней границы.

Читая подпись границы, всегда расшифруйте reference: AMSL, AGL/SFC или flight level. Нарисуйте вертикальный профиль маршрута с terrain, lower/upper limits и плановой высотой. Не сравнивайте FL с altitude без учёта pressure setting.

## [Controlled airspace][controlled-airspace] и национальный [ULM][ulm] {#norm-controlled-access}

Испанский [ULM][ulm] может входить в [controlled airspace][controlled-airspace] только если aircraft имеет подходящее оборудование **и** пилот имеет и реализует действующую эквивалентную лицензию [Part-FCL][part-fcl] нужной категории/класса. Дополнительно выполняются требования radio/language, [flight plan][flight-plan] при применимости и получается [ATC clearance][atc-clearance]. Национальные лицензия [ULM][ulm]/[MAF][maf] и [radiofonista (RTC)][rtc] без соответствующей лицензии [Part-FCL][part-fcl] недостаточны. Источники: `SRC-BOE-RD-765-2022`, `SRC-BOE-RD-182-2026` (art. 4.4; проверено 13.07.2026).

Практическое правило первоначального этапа: планируйте маршрут в допустимом uncontrolled airspace и оставляйте навигационный буфер. Если маршрут требует controlled entry, это не задача обычных полномочий национального [MAF][maf].

## Controlled и uncontrolled aerodrome

**Controlled aerodrome** имеет aerodrome control service для aerodrome traffic. Пилот выполняет clearance/instructions и опубликованные процедуры. **Uncontrolled aerodrome** не означает «без правил»: действуют опубликованный circuit, local procedures, приоритеты, runway state, самоинформация и ответственность [PIC][pic] за separation/decision.

Для использования конкретного аэродрома [ULM][ulm] проверьте:

1. допускает ли аэродром эту категорию;
2. требуется ли PPR;
3. часы работы и контакт;
4. полосу, поверхность, уклон и ограничения;
5. circuit/noise procedures;
6. текущие [NOTAM][notam] и local notices;
7. топливо, стоянку и аварийное обеспечение.

Запись площадки в ENR 5.5 не является сама по себе разрешением её использовать. Источник: `SRC-ENAIRE-AIP-ESPANA` (ENR 5.5; состояние реестра проверено 13.07.2026, перед полётом перепроверить).

## Prohibited, restricted и danger areas {#norm-special-use-airspace}

- **P — prohibited area:** полёт запрещён в опубликованных пределах, кроме прямо установленного исключения.
- **R — restricted area:** полёт ограничен условиями, временем или разрешением, опубликованными для зоны.
- **D — danger area:** в определённое время могут происходить опасные для полёта виды деятельности; статус, характер активности и безопасное решение проверяются по публикации.

Также встречаются временно segregated/reserved areas, военные зоны, природоохранные и иные ограничения. Код зоны без vertical limits и периода активности неполон. Источник: `SRC-ENAIRE-AIP-ESPANA` (ENR 5 и текущие supplements/[NOTAM][notam]; проверено 13.07.2026).

### Алгоритм проверки зоны

1. Запишите identifier.
2. Найдите lateral limits.
3. Расшифруйте lower/upper limits и reference.
4. Определите schedule и способ activation.
5. Прочитайте controlling authority/contact.
6. Проверьте [AIP][aip] [SUP][aip-sup], [AIC][aic] и [NOTAM][notam].
7. Нанесите безопасный lateral/vertical buffer.
8. Подготовьте diversion, если статус нельзя подтвердить.

## Ошибка moving map

База GNSS может быть просрочена, упрощать геометрию, скрывать вертикальную границу или неверно отображать временную активацию. Используйте её для awareness и cross-check, но не как источник [ATC clearance][atc-clearance]. Сравнивайте дату базы с действующим AIRAC и официальным briefing.

## Безопасность

Плановая линия, касающаяся границы, не оставляет места для ветра, навигационной погрешности и нагрузки пилота. Буфер выбирается осознанно с учётом условий и не используется для уменьшения установленного separation или обязательного маршрута.

При сомнении в позиции: не продолжайте к предполагаемой границе, стабилизируйте полёт, определите положение несколькими средствами, запросите помощь при наличии возможности и выполните заранее подготовленный diversion.

## Типичные ошибки

1. Считать класс G «пространством без правил».
2. Читать только горизонтальную границу зоны.
3. Путать altitude, height и flight level.
4. Принимать [radiofonista (RTC)][rtc] за controlled-entry privilege.
5. Считать P/R/D тремя словами с одинаковым юридическим эффектом.
6. Использовать moving map вместо текущего AIS briefing.

## Краткий конспект

- Класс определяет услуги и требования, а не только цвет.
- Реальную структуру даёт текущий [AIP][aip] España.
- Национальный [MAF][maf] сам по себе не допускает controlled entry.
- Uncontrolled aerodrome всё равно имеет правила и риски.
- Для любой зоны нужны lateral, vertical и temporal limits.
- Схема курса — концептуальная, не навигационная.

## Контрольные вопросы

### Q-LAW-013 — Что означает класс G?

A. Пространство без правил и ответственности.<br>
B. Uncontrolled airspace с применимыми правилами и flight information service по запросу.<br>
C. Только IFR.<br>
D. Автоматически закрытая зона.

**Правильный ответ:** B.

**Почему:** Отсутствие ATC separation service не отменяет [SERA][sera], [VMC minima][vmc] и ответственность пилота.

**Почему главный отвлекающий вариант неверен:** A подменяет «неконтролируемое» словом «нерегулируемое».

### Q-LAW-014 — Достаточна ли national [MAF][maf] + RTC для controlled entry?

A. Да, всегда.<br>
B. Нет; нужны подходящий aircraft, реализуемая эквивалентная [Part-FCL][part-fcl] licence и остальные условия.<br>
C. Да, если зона видна.<br>
D. Да, без clearance ночью.

**Правильный ответ:** B.

**Почему:** RD 765/2022 прямо связывает исключение с aircraft и европейскими полномочиями.

**Почему главный отвлекающий вариант неверен:** A смешивает radio qualification с licence/airspace privilege.

### Q-LAW-015 — Какие три измерения нужны для проверки зоны?

A. Цвет, название и размер шрифта.<br>
B. Горизонтальные, вертикальные и временные пределы.<br>
C. Только координата центра.<br>
D. Только верхняя граница.

**Правильный ответ:** B.

**Почему:** Aircraft может быть вне зоны только при одновременном соблюдении всех применимых измерений.

**Почему главный отвлекающий вариант неверен:** C ничего не говорит о форме, высоте и активности.

### Q-LAW-016 — Является ли схема в этой главе текущей картой Испании?

A. Да, для навигации.<br>
B. Нет, это концептуальная модель; нужен текущий официальный AIS.<br>
C. Да, если нет ветра.<br>
D. Только для ночи.

**Правильный ответ:** B.

**Почему:** Схема намеренно не содержит реальных границ, частот или AIRAC date.

**Почему главный отвлекающий вариант неверен:** A превращает объясняющую иллюстрацию в небезопасный навигационный документ.

## Источники

- `SRC-EASA-SERA-2025` — классификация и ATS context.
- `SRC-BOE-RD-765-2022`, `SRC-BOE-RD-182-2026` — controlled-airspace boundary для [ULM][ulm].
- `SRC-ENAIRE-AIP-ESPANA` — фактическая структура Испании и ENR/AD.

[ulm]: ../reference/glossary.md#term-ulm
[maf]: ../reference/glossary.md#term-maf
[lapl]: ../reference/glossary.md#term-lapl-a
[ppl]: ../reference/glossary.md#term-ppl-a
[part-fcl]: ../reference/glossary.md#term-part-fcl
[sera]: ../reference/glossary.md#term-sera
[vfr]: ../reference/glossary.md#term-vfr
[aip]: ../reference/glossary.md#term-aip
[notam]: ../reference/glossary.md#term-notam
[pic]: ../reference/glossary.md#term-pic
[rtc]: ../reference/glossary.md#term-radiofonista-rtc
[controlled-airspace]: ../reference/glossary.md#term-controlled-airspace
[atc-clearance]: ../reference/glossary.md#term-atc-clearance
[aip-sup]: ../reference/glossary.md#term-aip-sup
[aic]: ../reference/glossary.md#term-aic
[flight-plan]: ../reference/glossary.md#term-flight-plan
[vmc]: ../reference/glossary.md#term-vmc
