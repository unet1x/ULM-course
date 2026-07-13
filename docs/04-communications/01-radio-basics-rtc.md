# Основы радио и испанская RTC {#radio-basics-rtc}

## Назначение {#purpose}

Эта глава даёт [ULM](../reference/glossary.md#term-ulm)-пилоту в Испании базовую дисциплину авиационной речи и отделяет четыре разных «контрольных условия»: лицензию пилота, национальную отметку [radiofonista (RTC)][rtc], радиооборудование воздушного судна и разрешение/процедуру конкретной операции. Позже те же навыки используются при переходе к [LAPL(A)](../reference/glossary.md#term-lapl-a) или [PPL(A)](../reference/glossary.md#term-ppl-a), но без обещания автоматического зачёта.

## Результаты обучения {#outcomes}

После главы вы сможете:

1. описать модель «сформировать — передать — принять — подтвердить»;
2. объяснить ограничения VHF, дисциплину частоты и технику микрофона;
3. произнести алфавит, числа, десятичную точку и время;
4. правильно начать работу с позывным;
5. выполнить учебные radio check и смену частоты.

## Карта применимости {#applicability}

| Метка | Как использовать главу |
|---|---|
| [ULM — ОСНОВА][ulm] | Навык связи для полётов [ULM](../reference/glossary.md#term-ulm) в Испании. |
| [ULM — ОСОБО ВАЖНО][ulm] | RTC, оборудование и пространство проверяются раздельно. |
| [PART-FCL — ОБЩЕЕ][part-fcl] | Позже применяются [Part-FCL](../reference/glossary.md#term-part-fcl) Communications и языковые требования. |
| [LAPL — ПЕРЕХОД] | Уточнить у [DTO](../reference/glossary.md#term-dto)/[AESA](../reference/glossary.md#term-aesa) оформление R/T для [LAPL(A)](../reference/glossary.md#term-lapl-a). |
| [PPL — РАСШИРЕНИЕ] | Та же основа нужна для [PPL(A)](../reference/glossary.md#term-ppl-a), включая более широкий сценарный диапазон. |
| [ИСПАНИЯ] | Язык и служба берутся из текущего [AIP](../reference/glossary.md#term-aip) España. |
| [БЕЗОПАСНОСТЬ] | Если сообщение непонятно, действие не угадывают. |
| [ПРОВЕРИТЬ ПЕРЕД ПОЛЁТОМ] | [AIP](../reference/glossary.md#term-aip), [NOTAM](../reference/glossary.md#term-notam), AD instructions, частоту и исправность радио. |

## Теория {#theory}

### Модель связи {#communication-model}

Пилот сначала формирует одну цель сообщения, выбирает правильную станцию и слушает канал. Затем нажимает PTT, делает короткую паузу, говорит обычным темпом, отпускает PTT и слушает ответ. Приём завершён лишь когда смысл понятен и выполнен требуемый повтор или подтверждение. Одновременные передачи маскируют друг друга; длинный монолог блокирует канал.

[Авиационная радиотелефонная связь (English: radiotelephony, R/T; español: radiotelefonía)][radiotelephony] — голосовая связь, но сама она не создаёт эксплуатационных полномочий. Национальная RTC по RD 123/2015 arts. 12–13 получается после одобренного курса и проверок. Руководство [AESA](../reference/glossary.md#term-aesa) `A-DLA-URTC-01 v1.0` указывает castellano qualification и минимальную программу 20 h theory + 10 h ground practice + 1 h flight. Источники: `SRC-BOE-RD-123-2015`, `SRC-AESA-ULM-RTC-PROGRAM` (проверено 2026-07-13).

### Ограничения VHF {#vhf-limitations}

Авиационная VHF-связь в основном распространяется в пределах радиовидимости. Высота антенн, рельеф, экранирование конструкцией, удаление, состояние антенны и взаимные помехи меняют качество. Громкий сигнал не доказывает близость, а тишина не означает отсутствия движения. Если связь ухудшается, пилот не продолжает safety-critical действие на догадке.

### Дисциплина канала и микрофон {#frequency-discipline}

- слушайте до передачи и не перебивайте срочный обмен;
- держите микрофон на рекомендованном изготовителем расстоянии;
- говорите ровно, не кричите и не «съедайте» первые слоги;
- используйте короткие стандартные фразы, а при недостатке — ясное пояснение;
- поддерживайте [прослушивание рабочей частоты (English: listening watch; español: escucha permanente)][listening-watch], когда этого требует операция;
- после смены частоты проверьте индикацию active/standby.

Частоты и аэродромные процедуры динамичны. Сохранённая частота не гарантирует актуальность: перед полётом нужны текущие [AIP](../reference/glossary.md#term-aip) España, [NOTAM](../reference/glossary.md#term-notam), карта и local aerodrome instructions. [AIP](../reference/glossary.md#term-aip)/[NOTAM](../reference/glossary.md#term-notam) и местные аэродромные инструкции сверяют перед полётом. `SRC-ENAIRE-AIP-GEN-3-4-2026`, `SRC-ENAIRE-AIP-ESPANA` (проверено 2026-07-13).

### Алфавит, числа и время {#alphabet-numbers-time}

| Буква | Слово | Буква | Слово | Буква | Слово |
|---|---|---|---|---|---|
| A | ALFA | J | JULIETT | S | SIERRA |
| B | BRAVO | K | KILO | T | TANGO |
| C | CHARLIE | L | LIMA | U | UNIFORM |
| D | DELTA | M | MIKE | V | VICTOR |
| E | ECHO | N | NOVEMBER | W | WHISKEY |
| F | FOXTROT | O | OSCAR | X | X-RAY |
| G | GOLF | P | PAPA | Y | YANKEE |
| H | HOTEL | Q | QUEBEC | Z | ZULU |
| I | INDIA | R | ROMEO |  |  |

Цифры произносят раздельно по установленной авиационной форме; decimal — `DECIMAL`, español — `COMA` по опубликованной испанской процедуре. Высота, направление, частота, [QNH](../reference/glossary.md#term-qnh) и время требуют особого внимания к контексту и единицам. Время передают в минутах текущего часа, если контекст однозначен, либо полной группой; `UTC`/local time не смешивают. Точные pronunciation tables сверяются с [SERA](../reference/glossary.md#term-sera).14015 и текущим [AIP](../reference/glossary.md#term-aip), а не переписываются по памяти. Источники: `SRC-EASA-SERA-2025`, `SRC-ENAIRE-AIP-GEN-3-4-2026` (проверено 2026-07-13).

### Позывные и названия станций {#callsigns}

[Позывной (English: callsign; español: distintivo de llamada)][callsign] идентифицирует воздушное судно. Полный позывной используется при первом контакте. Пилот переходит к допустимому сокращению только после того, как наземная станция сама сократила его. При сомнении или похожих позывных возвращаются к полной форме.

Суффикс станции показывает функцию: `TOWER/TORRE`, `GROUND/RODAJE`, `APPROACH/APROXIMACIÓN`, `INFORMATION/INFORMACIÓN`, `RADIO/RADIO`. Название не заменяет проверку типа обслуживания: [диспетчерское обслуживание (English: air traffic control, ATC; español: control de tránsito aéreo)][atc], [аэродромное полётно-информационное обслуживание (English: aerodrome flight information service, AFIS; español: servicio de información de vuelo de aeródromo)][afis] и [связь «воздух—воздух» (English: air-to-air, A/A; español: aire-aire)][air-to-air] имеют разные полномочия.

### Язык и точность {#language-use}

[SERA](../reference/glossary.md#term-sera).14015 регулирует язык air-ground communications; [AIP](../reference/glossary.md#term-aip) España GEN 3.4 публикует испанскую реализацию. Нельзя обещать English на каждой ground station. English и español не смешивают произвольно в одной формуле: выбирают язык, поддерживаемый станцией и полномочиями пилота, а непонятное уточняют. Источники: `SRC-EASA-SERA-2025`, `SRC-ENAIRE-AIP-GEN-3-4-2026` (проверено 2026-07-13).

## Применение для [ULM](../reference/glossary.md#term-ulm) {#ulm-application}

Для [ULM](../reference/glossary.md#term-ulm)/[MAF](../reference/glossary.md#term-maf) в Испании национальная RTC разрешает радиотелефонную связь в авиационной полосе в пределах её условий, но не заменяет лицензию, исправное/разрешённое оборудование или operational clearance. С 1 апреля 2026 [ULM](../reference/glossary.md#term-ulm) в контролируемом пространстве требует подходящего оборудования и пилота, который имеет и вправе реализовать действующую [Part-FCL](../reference/glossary.md#term-part-fcl) licence эквивалентной категории/класса. [ULM](../reference/glossary.md#term-ulm) + [MAF](../reference/glossary.md#term-maf) + RTC недостаточны для контролируемого пространства. См. [границу пространства](../01-air-law/04-airspace-spain.md#norm-controlled-access). Источники: `SRC-BOE-RD-765-2022` art. 4.1(d), `SRC-BOE-RD-182-2026` (проверено 2026-07-13).

## Расширение [Part-FCL](../reference/glossary.md#term-part-fcl) {#part-fcl-extension}

При будущем [LAPL(A)](../reference/glossary.md#term-lapl-a)/[PPL(A)](../reference/glossary.md#term-ppl-a) отдельно закрываются: теоретический экзамен Communications, испанская отметка R/T для castellano или English и [языковая отметка (English: language proficiency endorsement; español: anotación de competencia lingüística)][language-endorsement] по FCL.055. Экзамен Communications не является оценкой FCL.055. Национальная RTC не даёт автоматического зачёта [Part-FCL](../reference/glossary.md#term-part-fcl) Communications или R/T. Минимум для применимой языковой отметки — operational Level 4. Источники: `SRC-EASA-AIRCREW-2026` FCL.055/FCL.120/FCL.215, `SRC-BOE-FOM-1146-2019` arts. 3–4, 7–9 (проверено 2026-07-13).

## Учебные сценарии {#training-scenarios}

### Сценарий RTC-01 — Проверка радио {#scenario-rtc-01}

СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ СЦЕНАРИЙ — НЕ ДЛЯ ПОЛЁТА

**Тип обслуживания:** controlled ATS, наземная станция.<br>
**Контекст:** стоянка, разрешённая местной процедурой radio check; частота уже проверена по current [AIP](../reference/glossary.md#term-aip).<br>
**English:** Pilot: `[STATION] [CALLSIGN], RADIO CHECK [FREQUENCY]`; station: `[CALLSIGN], READABILITY FOUR`.<br>
**Español:** Piloto: `[STATION] [CALLSIGN], PRUEBA RADIO [FREQUENCY]`; estación: `[CALLSIGN], LE RECIBO CUATRO`.<br>
**Пояснение:** запрос проверяет слышимость, а не разрешает руление или вылет.<br>
**[Readback][readback]/[acknowledgement][acknowledgement]:** полный повтор readability не является обязательным runway [readback](../reference/glossary.md#term-readback); коротко подтвердите приём по контексту.<br>
**Решение при сомнении:** при слабой/отсутствующей связи остановите подготовку, проверьте volume, squelch, active frequency, plugs и питание; не занимайте manoeuvring area.<br>
Источник: `SRC-BOE-RD-1180-2018`, Annex V (проверено 2026-07-13).

### Сценарий RTC-02 — Смена частоты {#scenario-rtc-02}

СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ СЦЕНАРИЙ — НЕ ДЛЯ ПОЛЁТА

**Тип обслуживания:** controlled ATS.<br>
**Контекст:** диспетчер передаёт следующий канал; `[FREQUENCY]` — переменная, не operational data.<br>
**English:** Station: `[CALLSIGN], CONTACT [NEXT STATION] [FREQUENCY]`; pilot: `CONTACT [NEXT STATION] [FREQUENCY], [CALLSIGN]`.<br>
**Español:** Estación: `[CALLSIGN], CONTACTE [NEXT STATION] [FREQUENCY]`; piloto: `CONTACTO [NEXT STATION] [FREQUENCY], [CALLSIGN]`.<br>
**Пояснение:** пилот подтверждает назначенную частоту, перестраивается и слушает до вызова.<br>
**[Readback][readback]/[acknowledgement][acknowledgement]:** повторите частоту и позывной; это не подтверждение нового clearance.<br>
**Решение при сомнении:** если цифры неясны, оставайтесь на текущем канале и запросите `SAY AGAIN FREQUENCY / REPITA FRECUENCIA` до переключения.<br>
Источник: `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).8015(e), `SRC-ENAIRE-AIP-GEN-3-4-2026` (проверено 2026-07-13).

## Безопасность {#safety}

Никакая тренировочная формула не заменяет current [AIP](../reference/glossary.md#term-aip), [NOTAM](../reference/glossary.md#term-notam), карту, aerodrome instructions и указания ATS. Radio check не создаёт права движения. При непонятном safety-critical сообщении не действуйте: попросите повтор/уточнение и остановитесь до ясности.

## Типичные ошибки {#common-errors}

1. Начинать передачу, не послушав канал.
2. Сокращать позывной до того, как это сделала станция.
3. Считать сохранённую частоту текущей.
4. Принимать название `RADIO` за доказательство ATC service.
5. Свободно смешивать English и español вместо ясного запроса.

## Конспект {#summary}

- Сначала слушайте, затем передавайте одну цель.
- VHF зависит от радиовидимости и оборудования.
- Полный позывной нужен на первом контакте.
- Частота и служба всегда проверяются по текущим данным.
- RTC, оборудование, лицензия и operational permission — разные условия.

## Контрольные вопросы {#review-questions}

### Q-RTC-001 — Что лучше всего описывает завершённый цикл радиосвязи перед действием пилота? {#q-rtc-001}

A. Передать сообщение и сразу выполнить ожидаемое действие.<br>
B. Сформировать цель, послушать, передать, понять ответ и выполнить требуемое подтверждение.<br>
C. Дважды повторить всё сообщение независимо от ответа станции.<br>
D. Оставаться в эфире до тех пор, пока станция не прервёт передачу.

**Правильный ответ:** B.

**Почему:** Цикл связи включает проверку канала, смысл ответа и требуемое подтверждение до действия; одна передача не доказывает взаимопонимание.

**Почему главный отвлекающий вариант неверен:** A опасен тем, что ожидаемое действие может отличаться от фактического ответа или вообще не быть разрешено.

### Q-RTC-002 — Когда пилот может сократить позывной воздушного судна? {#q-rtc-002}

A. Сразу после первого собственного вызова.<br>
B. Только когда наземная станция первой использовала допустимое сокращение.<br>
C. После взлёта независимо от формы ответа.<br>
D. Всегда, если на частоте мало движения.

**Правильный ответ:** B.

**Почему:** Полная форма на первом контакте защищает от mistaken identity; переход к сокращению инициирует станция.

**Почему главный отвлекающий вариант неверен:** A преждевременно сокращает идентификатор до установления однозначного контакта.

### Q-RTC-003 — Что означает тишина на частоте неконтролируемого аэродрома? {#q-rtc-003}

A. Другого движения нет и можно входить без осмотра.<br>
B. Радиообмен не слышен; визуальный поиск и соблюдение процедуры всё равно обязательны.<br>
C. Частота обязательно неверна.<br>
D. Всем воздушным судам выдано разрешение на посадку.

**Правильный ответ:** B.

**Почему:** Самолёт может не иметь радио, быть на другой частоте, иметь отказ или быть перекрыт одновременной передачей; lookout остаётся основой.

**Почему главный отвлекающий вариант неверен:** A нарушает правило визуального поиска: тишина на частоте неконтролируемого аэродрома не доказывает отсутствия traffic.

### Q-RTC-004 — Что необходимо проверить перед использованием сохранённой аэродромной частоты? {#q-rtc-004}

A. Только заряд гарнитуры.<br>
B. Текущие [AIP](../reference/glossary.md#term-aip)/[NOTAM](../reference/glossary.md#term-notam) и аэродромные инструкции для даты и операции.<br>
C. Совпадает ли частота со старой фотографией панели.<br>
D. Использовал ли её другой пилот в прошлом месяце.

**Правильный ответ:** B.

**Почему:** Частоты и local procedures динамичны; официальные текущие данные определяют применимый канал перед полётом.

**Почему главный отвлекающий вариант неверен:** C не подтверждает дату, amendment или operational status сохранённого значения.

### Q-RTC-005 — Что сама по себе национальная RTC [ULM](../reference/glossary.md#term-ulm) разрешает в 2026 году? {#q-rtc-005}

A. Автоматический вход [ULM](../reference/glossary.md#term-ulm) в [controlled airspace](../reference/glossary.md#term-controlled-airspace).<br>
B. Необходимую авиационную радиосвязь в пределах отметки, но не расширение пространства или [Part-FCL](../reference/glossary.md#term-part-fcl) privileges.<br>
C. Автоматическую English language endorsement Level 4.<br>
D. Замену требований к радиооборудованию воздушного судна.

**Правильный ответ:** B.

**Почему:** RD 123/2015 определяет национальную RTC как радиотелефонную habilitación; RD 765/2022 art. 4.1(d) отдельно ограничивает controlled-airspace operation [ULM](../reference/glossary.md#term-ulm).

**Почему главный отвлекающий вариант неверен:** A игнорирует отдельные требования [Part-FCL](../reference/glossary.md#term-part-fcl) licence и оборудования, действующие с 01.04.2026.

## Источники {#sources}

- `SRC-BOE-RD-123-2015` — arts. 12–13, national [ULM](../reference/glossary.md#term-ulm) RTC.
- `SRC-AESA-ULM-RTC-PROGRAM` — A-DLA-URTC-01 v1.0, §§3, 6, 8.
- `SRC-BOE-RD-765-2022` и `SRC-BOE-RD-182-2026` — [ULM](../reference/glossary.md#term-ulm) operational boundary с 01.04.2026.
- `SRC-EASA-SERA-2025` — [SERA](../reference/glossary.md#term-sera).14015 и [SERA](../reference/glossary.md#term-sera).8015(e).
- `SRC-ENAIRE-AIP-GEN-3-4-2026` — language/service data; dynamic.
- `SRC-BOE-FOM-1146-2019` и `SRC-EASA-AIRCREW-2026` — later [Part-FCL](../reference/glossary.md#term-part-fcl) R/T/language gates.

[rtc]: ../reference/glossary.md#term-radiofonista-rtc
[radiotelephony]: ../reference/glossary.md#term-radiotelephony-rt
[listening-watch]: ../reference/glossary.md#term-listening-watch
[callsign]: ../reference/glossary.md#term-callsign
[atc]: ../reference/glossary.md#term-air-traffic-control-atc
[afis]: ../reference/glossary.md#term-aerodrome-flight-information-service-afis
[air-to-air]: ../reference/glossary.md#term-air-to-air-aa
[language-endorsement]: ../reference/glossary.md#term-language-proficiency-endorsement
[readback]: ../reference/glossary.md#term-readback
[acknowledgement]: ../reference/glossary.md#term-acknowledgement
[ulm]: ../reference/glossary.md#term-ulm
[part-fcl]: ../reference/glossary.md#term-part-fcl
