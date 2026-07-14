# Семейства ROTAX: архитектура и поиск точного документа {#rotax-operation}

## Назначение {#purpose}

Название «ROTAX» не является моделью и не задаёт процедуру. Глава учит сначала идентифицировать двигатель, установку и контролируемую документацию, затем строить только качественное сравнение. Источник актуальности — официальный каталог документов (locator, `SRC-ROTAX-TECH-DOCS`); GU09, Conocimiento General de la Aeronave, pp. 33–39, на p. 33 задаёт экзаменационный объём (`SRC-AESA-ULM-LEARNING-OBJECTIVES-GU09-ED01`).

> **УЧЕБНАЯ СХЕМА — НЕ ЧЕК-ЛИСТ.** Иерархия: применимое право/[AIP](../reference/glossary.md#term-aip)/[NOTAM](../reference/glossary.md#term-notam)/AD → самолётные [AFM](../reference/glossary.md#term-afm)/[POH](../reference/glossary.md#term-poh) как точные документы самолёта, [дополнение к руководству по лётной эксплуатации (English: aircraft flight manual supplement; español: suplemento al manual de vuelo)](../reference/glossary.md#term-aircraft-flight-manual-supplement), [эксплуатационная табличка (English: placard; español: letrero o placa)](../reference/glossary.md#term-placard) и [самолётная контрольная карта (English: aircraft checklist; español: lista de comprobación de la aeronave)](../reference/glossary.md#term-aircraft-checklist) → точное [руководство по эксплуатации изготовителя (English: Operator's Manual; español: manual del operador; OM)](../reference/glossary.md#term-operators-manual-om) двигателя, винта и оборудования, применимые [SB](../reference/glossary.md#term-service-bulletin-sb)/[SI](../reference/glossary.md#term-service-instruction-si) и область применимости (effectivity) → программа и записи технического обслуживания → общий справочник → курс. Инструктор проверяет, что выбран документ именно установленного двигателя.

## Результаты обучения {#outcomes}

- качественно отличать карбюраторный 912 от 912 i с впрыском;
- не переносить турбонаддув, [конденсаторно-разрядное зажигание (English: capacitor-discharge ignition; español: encendido por descarga capacitiva; CDI)](../reference/glossary.md#term-capacitor-discharge-ignition-cdi) или архитектуру каналов [электронной системы управления двигателем (EMS)](../reference/glossary.md#term-engine-management-system-ems) на каждую модель;
- прочитать номер документа, издание и редакцию, модель и вариант, серийный номер и применимость, а также контроль языка;
- объяснить роли [OM](../reference/glossary.md#term-operators-manual-om), [руководства по установке (English: Installation Manual; español: manual de instalación; IM)](../reference/glossary.md#term-installation-manual-im) и [руководства по линейному техобслуживанию (English: Maintenance Manual Line; español: manual de mantenimiento en línea; MML)](../reference/glossary.md#term-maintenance-manual-line-mml);
- остановить подготовку при конфликте документов.

## Карта применимости {#applicability}

| Метка | Что изучать |
|---|---|
| [ULM — ОСНОВА][ulm] | Порядок работы с документами двигателя установленного [MAF](../reference/glossary.md#term-maf) |
| [ULM — ОСОБО ВАЖНО][ulm] | Не использовать «процедуру ROTAX вообще» |
| [PART-FCL — ОБЩЕЕ][part-fcl] | Объём по силовой установке и электросистеме в §§8.1–8.2 |
| [LAPL — ПЕРЕХОД] | Новый тип означает новые [AFM](../reference/glossary.md#term-afm)/[POH](../reference/glossary.md#term-poh) и документацию двигателя |
| [PPL — РАСШИРЕНИЕ] | Более широкий парк, но та же дисциплина проверки применимости документов |
| [ИСПАНИЯ] | Национальный режим обслуживания [ULM](../reference/glossary.md#term-ulm) не заменяется [Part-ML](../reference/glossary.md#term-part-ml) |
| [БЕЗОПАСНОСТЬ] | Нет универсальных RPM, рабочей жидкости, действия по предупреждению или процедуры опробования |
| [ПРОВЕРИТЬ ПЕРЕД ПОЛЁТОМ] | Модель, вариант, серийный номер, редакция, AD/[SB](../reference/glossary.md#term-service-bulletin-sb)/[SI](../reference/glossary.md#term-service-instruction-si), дополнение и записи |

## Теория {#theory}

### Безопасная общая архитектура {#family-architecture}

Проверенные семейства имеют горизонтально-оппозитную четырёхцилиндровую четырёхтактную основу, но не каждое другое свойство общее. В применимых вариантах встречаются жидкостно охлаждаемые головки и воздушно охлаждаемые цилиндры, смазка с сухим картером (dry-sump lubrication) и понижающий редуктор (reduction gearbox). Эти признаки всё равно сверяют с точной моделью и установкой.

Карбюраторный 912 (912 carburetted) использует карбюраторы, тогда как 912 i использует впрыск топлива (fuel injection) с электронным управлением. Семейства 914, 915 i и 916 i имеют турбонаддув согласно проверенным руководствам; не каждый ROTAX турбирован. Для применимых двигателей серии i электронная система управления двигателем (English: [engine management system (EMS)](../reference/glossary.md#term-engine-management-system-ems); español: sistema de gestión del motor) может иметь резервные каналы. Двойное [CDI](../reference/glossary.md#term-capacitor-discharge-ignition-cdi) или два контура зажигания и резервные каналы EMS — не одно и то же: они различаются функциями, входными и выходными сигналами и индикацией.

### Пять вопросов перед чтением значения {#exact-document-workflow}

1. **Что установлено?** Регистрация и конфигурация самолёта, модель и вариант двигателя.
2. **К какому серийному номеру и области применимости относится файл?** Название серии недостаточно.
3. **Какой статус документа?** Номер, издание, редакция и дата документа, а также текущие [SB](../reference/glossary.md#term-service-bulletin-sb)/[SI](../reference/glossary.md#term-service-instruction-si)/AD.
4. **Какой документ определяет действие на самолёте?** [AFM](../reference/glossary.md#term-afm)/[POH](../reference/glossary.md#term-poh), дополнение и контрольная карта, согласованные с [OM](../reference/glossary.md#term-operators-manual-om) двигателя.
5. **Какой язык и единицы контролируют?** ROTAX указывает: английский оригинал и метрические единицы `SI` (English: International System of Units; español: Sistema Internacional de Unidades) имеют приоритет; перевод и пересчёт не должны менять смысл.

Если два значения не совпадают, пилот не усредняет и не выбирает удобное: он останавливает подготовку и разрешает конфликт через эксплуатанта, специалиста по обслуживанию и инструктора, используя текущие одобренные данные (approved data).

### Проверенные снимки [OM](../reference/glossary.md#term-operators-manual-om) {#verified-om-snapshots}

| Семейство | Контрольная копия, проверенная 13.07.2026 | Разрешённое использование в курсе |
|---|---|---|
| Карбюраторный 912 | [OM-912](../reference/glossary.md#term-operators-manual-om) Edition 4 Rev.2; нижний колонтитул 01.06.2025, каталог 15.07.2025 (`SRC-ROTAX-OM-912-ED4-R2`) | Документ и применимость; качественная карбюраторная архитектура |
| 912 i | [OM-912 i](../reference/glossary.md#term-operators-manual-om) Edition 2 Rev.2; нижний колонтитул 01.09.2025, каталог 06.10.2025 (`SRC-ROTAX-OM-912I-ED2-R2`) | Документ и применимость; контекст впрыска и EMS |
| 914 | [OM-914](../reference/glossary.md#term-operators-manual-om) Edition 3 Rev.0, 01.08.2019 (`SRC-ROTAX-OM-914-ED3-R0`) | Контекст семейства с турбонаддувом, но не действующее значение для другого двигателя |
| 915 i A/C24 | [OM-915 i A/C24](../reference/glossary.md#term-operators-manual-om) Edition 0 Rev.4, 01.09.2022 (`SRC-ROTAX-OM-915I-ED0-R4`) | Качественное описание архитектуры впрыска, турбонаддува и EMS |
| 916 i A/C24 | [OM-916 i A/C24](../reference/glossary.md#term-operators-manual-om) Edition 0 Rev.1, 01.12.2023 (`SRC-ROTAX-OM-916I-ED0-R1`) | Качественное описание архитектуры впрыска, турбонаддува и EMS |

Перед реальным использованием каждую контрольную копию (snapshot) повторно находят через официальный каталог по точной модели или варианту, серийному номеру и области применимости: прямая ссылка не доказывает, что файл всё ещё действует для данного двигателя.

Отдельная ловушка измерений: в [OM-912 i](../reference/glossary.md#term-operators-manual-om) на PDF p. 77 расход топлива (fuel flow) описан как величина, вычисляемая ECU. Такое вычисленное значение само по себе не доказывает остаток в баках и не задаёт продолжительность полёта (endurance). Для полётного планирования и сверки используют данные производителя самолёта, установленное и допущенное измерение и текущий [AFM](../reference/glossary.md#term-afm)/[POH](../reference/glossary.md#term-poh); применимость подтверждает `SRC-ROTAX-OM-912I-ED2-R2`.

### [IM](../reference/glossary.md#term-installation-manual-im) и [MML](../reference/glossary.md#term-maintenance-manual-line-mml): не пилотская инструкция {#im-mml-boundary}

Проверенные контрольные копии для границы ролей (`SRC-ROTAX-IM-MML-ROLE-2026`):

- 912 [IM](../reference/glossary.md#term-installation-manual-im) Issue 3 Rev.1 и [MML](../reference/glossary.md#term-maintenance-manual-line-mml) Issue 4 Rev.2, 01.06.2025;
- 912 i [IM](../reference/glossary.md#term-installation-manual-im) Issue 2 Rev.1, 01.02.2020, и [MML](../reference/glossary.md#term-maintenance-manual-line-mml) Issue 2 Rev.2, 01.05.2023;
- 914 [IM](../reference/glossary.md#term-installation-manual-im) Issue 3 Rev.0, 01.08.2019, и [MML](../reference/glossary.md#term-maintenance-manual-line-mml) Issue 3 Rev.0, 01.03.2024;
- 915 i [IM](../reference/glossary.md#term-installation-manual-im) Issue 0 Rev.5, 01.02.2024, и [MML](../reference/glossary.md#term-maintenance-manual-line-mml) Issue 0 Rev.3, 01.05.2025;
- 916 i [IM](../reference/glossary.md#term-installation-manual-im)/[MML](../reference/glossary.md#term-maintenance-manual-line-mml) Issue 0 Rev.2, 01.12.2025.

[IM](../reference/glossary.md#term-installation-manual-im) предназначен для работ изготовителя или установщика (manufacturer/installer) в установленном объёме. [MML](../reference/glossary.md#term-maintenance-manual-line-mml) не превращает владельца или пилота в специалиста по обслуживанию: требуются компетентность, знание типа, инструменты, условия, полномочия и применимые ограничения ROTAX/iRMT. Здесь эти файлы подтверждают границу ролей, а не описывают выполнение работы.

### SCN-AGK-03 — Предупреждение канала EMS (lane) или признак неисправности зажигания? {#scn-agk-03}

**Признаки:** на самолёте с двигателем серии i появляется индикация канала EMS либо двигатель работает необычно.

**Конкурирующие объяснения:** датчик или входной сигнал, канал EMS, электропитание, проводка или установка, сама индикация, отдельная проблема зажигания или сгорания.

**Граница безопасного решения:** не называть канал «магнето», не выполнять повторные сбросы и применить точную самолётную процедуру при ненормальной ситуации.

**Точный документ:** дополнение к [AFM](../reference/glossary.md#term-afm)/[POH](../reference/glossary.md#term-poh) и контрольная карта; точный [OM](../reference/glossary.md#term-operators-manual-om) и текущие [SB](../reference/glossary.md#term-service-bulletin-sb)/[SI](../reference/glossary.md#term-service-instruction-si)/AD для модели, варианта, серийного номера и области применимости; инструктаж преподавателя.

**Почему это не чек-лист:** логика каналов, разрешённый сброс, оставшееся резервирование и решение о посадке различаются между установками.

## Применение к [ULM](../reference/glossary.md#term-ulm)/[MAF](../reference/glossary.md#term-maf) {#ulm-application}

Школа [ULM](../reference/glossary.md#term-ulm) должна показать ученику документы именно борта. Хорошая проверка — ученик может от регистрации, обозначения типа, серийного номера самолёта или изготовителя и таблички двигателя дойти до применимого раздела [AFM](../reference/glossary.md#term-afm), редакции [OM](../reference/glossary.md#term-operators-manual-om) и статуса записей. GU09 pp. 33–39 определяет объём [MAF](../reference/glossary.md#term-maf); строки только для DCG, автожира или вертолёта не добавляются.

## Расширение [Part-FCL](../reference/glossary.md#term-part-fcl) {#part-fcl-extension}

Теория LAPL и PPL использует общую [программу](../reference/glossary.md#term-syllabus) «Общие знания о воздушном судне» (Aircraft General Knowledge; `SRC-EASA-AIRCREW-2026`, §§8.1–8.2). Переход не отменяет ознакомление с новым типом (type familiarisation). [Part-ML](../reference/glossary.md#term-part-ml)/[Part-NCO](../reference/glossary.md#term-part-nco) определяются лётной годностью и операцией, а не тем, что пилот получил LAPL или PPL.

## Безопасность {#safety}

Частота вращения (RPM), продолжительность, холостой ход, падение при проверке магнето или канала, температуры и давления, октановое число и этанол, масло и охлаждающая жидкость, свеча и зазор, прогрев, запуск и охлаждение, момент редуктора, интервал или TBO, расход, напряжение и ток, шаг и инерция винта, проверка масла и действие по предупреждению не имеют универсального значения для всех ROTAX.

## Частые ошибки {#common-errors}

1. «Все 912 карбюраторные» — 912 i использует впрыск.
2. «Каждый ROTAX имеет турбонаддув» — неверно.
3. «Двойное [CDI](../reference/glossary.md#term-capacitor-discharge-ignition-cdi) равно двум каналам EMS» — функции не тождественны.
4. «Одна проверка магнето или канала подходит всем» — нет.
5. «Последний скачанный PDF управляет самолётом» — одобрение самолёта и применимость важнее.

## Итог {#summary}

Безопасная техническая грамотность — это не память о числе, а воспроизводимый путь к точным, текущим и одобренным данным. Общее сравнение семейств помогает читать систему, но никогда не подменяет конкретную установку.

## Контрольные вопросы {#review-questions}

### Q-AGK-011 — Что отличает 912 i от карбюраторного 912 на уровне курса? {#q-agk-011}

A. 912 i использует архитектуру впрыска и EMS, а карбюраторное семейство — карбюраторы.<br>
B. Каждый 912 i обязательно установлен на самолёте сферы [Part-FCL](../reference/glossary.md#term-part-fcl).<br>
C. Карбюраторный 912 всегда имеет турбонаддув.<br>
D. Между ними нет различий в документации и индикации.

**Правильный ответ:** A.

**Почему:** 912 i использует впрыск и EMS, тогда как проверенное карбюраторное семейство 912 применяет карбюраторы; определяющей всё равно остаётся точная установка.

**Почему главный отвлекающий вариант неверен:** C без основания приписывает турбонаддув всему карбюраторному семейству 912.

### Q-AGK-012 — Что проверяют до применения значения для двигателя? {#q-agk-012}

A. Только совпадение названия семейства в заголовке руководства.<br>
B. Модель, вариант, серийный номер и применимость; редакцию, самолётный документ и текущие AD/[SB](../reference/glossary.md#term-service-bulletin-sb)/[SI](../reference/glossary.md#term-service-instruction-si).<br>
C. Значение на похожем самолёте школы.<br>
D. Среднее между [OM](../reference/glossary.md#term-operators-manual-om) и старой контрольной картой.

**Правильный ответ:** B.

**Почему:** Значение применимо лишь к идентифицированной конфигурации и контролируемому набору документов.

**Почему главный отвлекающий вариант неверен:** D предлагает усреднить конфликтующие значения [OM](../reference/glossary.md#term-operators-manual-om) и контрольной карты вместо проверки модели, применимости и одобренной иерархии.

### Q-AGK-013 — Почему [CDI](../reference/glossary.md#term-capacitor-discharge-ignition-cdi) и канал EMS не тождественны? {#q-agk-013}

A. [CDI](../reference/glossary.md#term-capacitor-discharge-ignition-cdi) относится к контуру зажигания, а канал EMS может управлять более широкими функциями и входами.<br>
B. Двойное [CDI](../reference/glossary.md#term-capacitor-discharge-ignition-cdi) также управляет всеми функциями впрыска и всеми входами EMS.<br>
C. Канал EMS лишь дублирует искру зажигания и не использует других входов или выходов.<br>
D. Наличие двух индикаций каналов исключает отдельную двухконтурную архитектуру зажигания.

**Правильный ответ:** A.

**Почему:** [CDI](../reference/glossary.md#term-capacitor-discharge-ignition-cdi) относится к зажиганию, а канал EMS управляет более широким набором входных и выходных сигналов двигателя; их резервирование не тождественно.

**Почему главный отвлекающий вариант неверен:** B смешивает резервирование контура искрового зажигания с более широкой функцией электронного управления двигателем.

### Q-AGK-014 — Для кого прежде всего предназначен [IM](../reference/glossary.md#term-installation-manual-im)? {#q-agk-014}

A. Для работ изготовителя или установщика в пределах установленного объёма и компетентности.<br>
B. Для самостоятельного ремонта любым пилотом на стоянке.<br>
C. Для пилота как основной источник эксплуатационных ограничений и действий на установленном самолёте.<br>
D. Для замены обычных процедур самолётного [AFM](../reference/glossary.md#term-afm).

**Правильный ответ:** A.

**Почему:** [Installation Manual](../reference/glossary.md#term-installation-manual-im) описывает специализированную роль и не создаёт полномочий пилота на работу.

**Почему главный отвлекающий вариант неверен:** C ошибочно превращает [Installation Manual](../reference/glossary.md#term-installation-manual-im) в основной пилотский источник эксплуатационных ограничений и действий; ими управляют применимые самолётные [AFM](../reference/glossary.md#term-afm)/[POH](../reference/glossary.md#term-poh), дополнения, таблички и контрольная карта.

### Q-AGK-015 — Что делать при конфликте [OM](../reference/glossary.md#term-operators-manual-om) и самолётной контрольной карты? {#q-agk-015}

A. Выбрать более удобное значение.<br>
B. Усреднить оба значения.<br>
C. Остановиться и разрешить вопрос применимости через [AFM](../reference/glossary.md#term-afm)/[POH](../reference/glossary.md#term-poh), организацию, специалиста по обслуживанию и текущие данные.<br>
D. Считать [OM](../reference/glossary.md#term-operators-manual-om) двигателя автоматически главным для действия на самолёте.

**Правильный ответ:** C.

**Почему:** Одобрение на уровне самолёта и точную применимость нужно согласовать; пилот не исправляет конфликт арифметикой.

**Почему главный отвлекающий вариант неверен:** D ошибочно позволяет отдельному руководству двигателя разрешать действие на всём самолёте.

## Источники {#sources}

- `SRC-AESA-ULM-LEARNING-OBJECTIVES-GU09-ED01` — Conocimiento General de la Aeronave, pp. 33–39; здесь p. 33.
- `SRC-EASA-AIRCREW-2026` — §§8.1–8.2.
- `SRC-ROTAX-TECH-DOCS` — official locator.
- `SRC-ROTAX-OM-912-ED4-R2`, `SRC-ROTAX-OM-912I-ED2-R2`, `SRC-ROTAX-OM-914-ED3-R0`, `SRC-ROTAX-OM-915I-ED0-R4`, `SRC-ROTAX-OM-916I-ED0-R1` — exact snapshots and pinpoints in registry.
- `SRC-ROTAX-IM-MML-ROLE-2026` — role boundary and exact verified editions.
- `SRC-ROTAX-IM-912-ED3-R1`, `SRC-ROTAX-MML-912-ED4-R2` — точные снимки 912 [IM](../reference/glossary.md#term-installation-manual-im)/[MML](../reference/glossary.md#term-maintenance-manual-line-mml) и контрольные места границы ролей.
- `SRC-ROTAX-IM-912I-ED2-R1`, `SRC-ROTAX-MML-912I-ED2-R2` — точные снимки 912 i [IM](../reference/glossary.md#term-installation-manual-im)/[MML](../reference/glossary.md#term-maintenance-manual-line-mml) и контрольные места границы ролей.
- `SRC-ROTAX-IM-914-ED3-R0`, `SRC-ROTAX-MML-914-ED3-R0` — точные снимки 914 [IM](../reference/glossary.md#term-installation-manual-im)/[MML](../reference/glossary.md#term-maintenance-manual-line-mml) и контрольные места границы ролей.
- `SRC-ROTAX-IM-915I-ED0-R5`, `SRC-ROTAX-MML-915I-ED0-R3` — точные снимки 915 i [IM](../reference/glossary.md#term-installation-manual-im)/[MML](../reference/glossary.md#term-maintenance-manual-line-mml) и контрольные места границы ролей.
- `SRC-ROTAX-IM-916I-ED0-R2`, `SRC-ROTAX-MML-916I-ED0-R2` — точные снимки 916 i [IM](../reference/glossary.md#term-installation-manual-im)/[MML](../reference/glossary.md#term-maintenance-manual-line-mml) и контрольные места границы ролей.

[ulm]: ../reference/glossary.md#term-ulm
[part-fcl]: ../reference/glossary.md#term-part-fcl
