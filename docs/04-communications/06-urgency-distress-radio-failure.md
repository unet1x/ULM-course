# Срочность, бедствие и отказ связи {#urgency-distress-radio-failure}

## Назначение {#purpose}

Глава даёт [ULM](../reference/glossary.md#term-ulm)-пилоту в Испании законную структуру MAYDAY/PAN PAN, отказа связи, SSR codes и light signals без переноса IFR lost-communications procedures в day-[VFR](../reference/glossary.md#term-vfr) [ULM](../reference/glossary.md#term-ulm). Эти же основы сохраняются при последующем [LAPL(A)](../reference/glossary.md#term-lapl-a)/[PPL(A)](../reference/glossary.md#term-ppl-a).

## Результаты обучения {#outcomes}

Вы сможете выбрать MAYDAY или PAN PAN по состоянию, передать доступные message elements, использовать emergency frequency по назначению, выполнить проверенную последовательность loss of communications, выбрать 7600/7700 по смыслу и распознать основные aerodrome light signals.

## Карта применимости {#applicability}

| Метка | Как использовать главу |
|---|---|
| [ULM — ОСНОВА][ulm] | Emergency communication для day-[VFR](../reference/glossary.md#term-vfr) Spain. |
| [ULM — ОСОБО ВАЖНО][ulm] | Fly aircraft first; не переносить IFR procedure. |
| [PART-FCL — ОБЩЕЕ][part-fcl] | [SERA](../reference/glossary.md#term-sera) [distress](../reference/glossary.md#term-distress)/[urgency](../reference/glossary.md#term-urgency)/failure applies by context. |
| [LAPL — ПЕРЕХОД] | Practice with instructor and aircraft checklist. |
| [PPL — РАСШИРЕНИЕ] | Later add applicable IFR knowledge separately. |
| [ИСПАНИЯ] | Current [AIP](../reference/glossary.md#term-aip) and aerodrome signals/procedure prevail. |
| [БЕЗОПАСНОСТЬ] | Emergency call never delays aircraft control. |
| [ПРОВЕРИТЬ ПЕРЕД ПОЛЁТОМ] | Radio/transponder tests, alternates, light-signal knowledge. |

## Теория {#theory}

### MAYDAY: бедствие {#distress}

[Бедствие (English: distress; español: socorro)][distress-term] — serious and/or imminent danger requiring immediate assistance. First transmission starts with `MAYDAY`, preferably three times. Use the air-ground frequency in use and transmit as many available elements as possible, distinctly, preferably: station addressed if time permits; aircraft identification; nature; intention; present position, level and heading. Control aircraft first; omitted data can follow. [Distress](../reference/glossary.md#term-distress) has absolute communications priority. Источник: `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).14095(a),(b) (проверено 2026-07-13).

### PAN PAN: срочность {#urgency}

[Срочность (English: urgency; español: urgencia)][urgency-term] concerns safety of aircraft/vehicle/person but does not require immediate assistance. First transmission starts `PAN PAN`, preferably three times, then station, identification, nature, intention, position/level/heading and useful information as required. [Urgency](../reference/glossary.md#term-urgency) has priority over all except [distress](../reference/glossary.md#term-distress). MAYDAY and PAN PAN are not interchangeable: choose condition, and upgrade if danger becomes serious/imminent. Источник: `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).14095(a),(c) (проверено 2026-07-13).

### Emergency frequency {#emergency-frequency}

121.500 MHz предназначена для genuine emergency purposes из [SERA](../reference/glossary.md#term-sera).14095(d), а не для routine radio checks. Для [distress](../reference/glossary.md#term-distress)/[urgency](../reference/glossary.md#term-urgency) обычно начинают на рабочей частоте. Сообщение о бедствии можно передать на 121.500 или другой частоте aeronautical mobile service, когда это необходимо или целесообразно; не каждая авиационная станция непрерывно её слушает. Безусловное правило «сначала переключиться» неверно. Источник: `SRC-EASA-SERA-2025` Article 4a, [SERA](../reference/glossary.md#term-sera).14095(d), GM1 [SERA](../reference/glossary.md#term-sera).14095(b)(1) (проверено 2026-07-13).

### Loss of two-way communications {#communication-failure}

[Отказ двусторонней связи (English: communication failure; español: fallo de comunicaciones)][communication-failure] is handled by the verified [SERA](../reference/glossary.md#term-sera).14083 sequence, not a home-made mnemonic claimed as law:

1. Try the previous channel; then another channel appropriate to the route.
2. If unsuccessful, attempt the appropriate ATS unit, other ATS units or other aircraft using available means.
3. If contact still fails, apply the failure procedure: select Mode A 7600 where equipped/applicable and set ADS-B loss indication where available.
4. A [VFR](../reference/glossary.md#term-vfr) flight continues in [VMC](../reference/glossary.md#term-vmc), lands at the nearest suitable aerodrome and reports arrival to appropriate ATS by the most expeditious means.
5. At a controlled aerodrome, watch for visual signals.
6. If transmitting blind after all contact attempts, use the [SERA](../reference/glossary.md#term-sera).14085 form and transmit message twice; receiver-failure reports include intended action and repetition.

This is a [VFR](../reference/glossary.md#term-vfr) outcome. The detailed IFR timing/route procedure is not a [ULM](../reference/glossary.md#term-ulm) day-[VFR](../reference/glossary.md#term-vfr) technique and is not imported here. `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).14083/[SERA](../reference/glossary.md#term-sera).14085 (проверено 2026-07-13).

### SSR codes and IDENT {#ssr-codes}

[Вторичный обзорный радиолокатор (English: secondary surveillance radar, SSR; español: radar secundario de vigilancia)][ssr] uses transponder codes:

- `7700` — emergency, unless assigned code is retained as required; pilot may select 7700 when specifically best;
- `7600` — radio-[communication failure](../reference/glossary.md#term-communication-failure);
- `7500` — unlawful interference;
- `7000` — when not receiving ATS, to improve detection, unless otherwise prescribed by competent authority. Поэтому 7000 — не универсальный [VFR](../reference/glossary.md#term-vfr)-код вне текущего национального предписания или инструкции ATS.

Назначенный код сохраняют по инструкции. IDENT используют только по указанию; это не общая кнопка «сделайте меня видимым». Источник: `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).13001/[SERA](../reference/glossary.md#term-sera).13005 and [AMC](../reference/glossary.md#term-amc)/GM (проверено 2026-07-13).

### Aerodrome light signals {#light-signals}

[SERA](../reference/glossary.md#term-sera) Appendix 1 Table AP 1-1 distinguishes in-flight and on-ground meanings:

| Light from aerodrome control | Aircraft in flight | Aircraft on ground |
|---|---|---|
| steady green | cleared to land | cleared for take-off |
| steady red | give way, continue circling | stop |
| green flashes | return for landing | cleared to taxi |
| red flashes | aerodrome unsafe, do not land | taxi clear of landing area |
| white flashes | land and proceed to apron | return to starting point |
| red pyrotechnic | do not land for the time being | — |

Daytime airborne [acknowledgement](../reference/glossary.md#term-acknowledgement) is rocking wings, except on base/final; on ground move ailerons or rudder. Night acknowledgements use lights as specified. Light signals are operational instructions, not optional decoration. Source: `SRC-EASA-SERA-2025` Appendix 1 Table AP 1-1 (проверено 2026-07-13).

## Применение для [ULM](../reference/glossary.md#term-ulm) {#ulm-application}

For [ULM](../reference/glossary.md#term-ulm) in Spain, emergency authority does not erase aircraft limitations, but immediate safety takes priority. Use aircraft [AFM](../reference/glossary.md#term-afm)/[POH](../reference/glossary.md#term-poh)/emergency checklist, [aviate–navigate–communicate](../reference/glossary.md#term-aviate-navigate-communicate) and applicable [SERA](../reference/glossary.md#term-sera). National RTC training includes [distress](../reference/glossary.md#term-distress), [urgency](../reference/glossary.md#term-urgency) and failure; it still is not [Part-FCL](../reference/glossary.md#term-part-fcl) licence or controlled-airspace privilege. `SRC-AESA-ULM-RTC-PROGRAM`, `SRC-BOE-RD-765-2022` (проверено 2026-07-13).

## Расширение [Part-FCL](../reference/glossary.md#term-part-fcl) {#part-fcl-extension}

[LAPL(A)](../reference/glossary.md#term-lapl-a)/[PPL(A)](../reference/glossary.md#term-ppl-a) candidates retain the [VFR](../reference/glossary.md#term-vfr) rule and add only procedures applicable to their future operation/training. Communications theory, R/T annotation and FCL.055 remain separate gates. `SRC-EASA-AIRCREW-2026`, `SRC-BOE-FOM-1146-2019` (проверено 2026-07-13).

## Учебные сценарии {#training-scenarios}

### Сценарий RTC-18 — MAYDAY engine power loss {#scenario-rtc-18}

СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ СЦЕНАРИЙ — НЕ ДЛЯ ПОЛЁТА

**Тип обслуживания:** emergency on frequency in use; controlled ATS receiver.<br>
**Контекст:** aircraft stable at best-achievable flight path after power loss; placeholders replace live position/frequency.<br>
**English:** Pilot: `MAYDAY MAYDAY MAYDAY, [STATION], [CALLSIGN], ENGINE POWER LOSS, FORCED LANDING [INTENTION], [POSITION], [ALTITUDE], [HEADING]`; station: `[CALLSIGN], MAYDAY ROGER, [ASSISTANCE/QUESTION]`.<br>
**Español:** Piloto: `MAYDAY MAYDAY MAYDAY, [STATION], [CALLSIGN], PÉRDIDA DE POTENCIA, ATERRIZAJE FORZOSO [INTENTION], [POSITION], [ALTITUDE], [HEADING]`; estación: `[CALLSIGN], MAYDAY RECIBIDO, [ASSISTANCE/QUESTION]`.<br>
**Пояснение:** call sends nature, intention and location without delaying control/checklist.<br>
**[Readback][readback]/[acknowledgement][acknowledgement]:** station acknowledges; pilot answers only useful questions workload permits and corrects wrong position immediately.<br>
**Решение при сомнении:** сначала управляйте самолётом; передайте доступную часть сообщения, включите подходящие emergency means и дополните данные, когда сможете.<br>
Источник: `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).14095(b) (проверено 2026-07-13).

### Сценарий RTC-19 — PAN PAN passenger condition {#scenario-rtc-19}

СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ СЦЕНАРИЙ — НЕ ДЛЯ ПОЛЁТА

**Тип обслуживания:** emergency/[urgency](../reference/glossary.md#term-urgency) traffic on frequency in use.<br>
**Контекст:** passenger condition affects safety and priority handling is requested, but immediate assistance in flight is not yet required.<br>
**English:** Pilot: `PAN PAN PAN PAN PAN PAN, [STATION], [CALLSIGN], PASSENGER ILL, REQUEST PRIORITY LANDING [AERODROME], [POSITION], [ALTITUDE], [HEADING], [PERSONS/FUEL IF USEFUL]`; station: `[CALLSIGN], PAN ROGER, [INSTRUCTION/INFORMATION]`.<br>
**Español:** Piloto: `PAN PAN PAN PAN PAN PAN, [STATION], [CALLSIGN], PASAJERO CON PROBLEMA MÉDICO, SOLICITO PRIORIDAD PARA ATERRIZAR [AERODROME], [POSITION], [ALTITUDE], [HEADING], [PERSONS/FUEL IF USEFUL]`; estación: `[CALLSIGN], PAN RECIBIDO, [INSTRUCTION/INFORMATION]`.<br>
**Пояснение:** [urgency](../reference/glossary.md#term-urgency) signal requests priority/assistance without declaring immediate [distress](../reference/glossary.md#term-distress); useful facts follow workload.<br>
**[Readback][readback]/[acknowledgement][acknowledgement]:** repeat any runway/level/heading clearance exactly; PAN [acknowledgement](../reference/glossary.md#term-acknowledgement) alone is not those readbacks.<br>
**Решение при сомнении:** if condition worsens to serious/imminent danger requiring immediate assistance, upgrade to MAYDAY and state changed nature/intention.<br>
Источник: `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).14095(c) (проверено 2026-07-13).

### Сценарий RTC-20 — Radio failure, SSR and light signal {#scenario-rtc-20}

СИНТЕТИЧЕСКИЙ УЧЕБНЫЙ СЦЕНАРИЙ — НЕ ДЛЯ ПОЛЁТА

**Тип обслуживания:** emergency / controlled-aerodrome visual-signal response.<br>
**Контекст:** [VFR](../reference/glossary.md#term-vfr) aircraft loses two-way radio, remains [VMC](../reference/glossary.md#term-vmc), attempts previous/appropriate channels and relay, then applies [SERA](../reference/glossary.md#term-sera) failure procedure.<br>
**English:** Aircraft blind transmission: `TRANSMITTING BLIND, [STATION], [CALLSIGN], RADIO FAILURE, [POSITION], [ALTITUDE], LANDING AT [SUITABLE AERODROME], THIS MESSAGE TWICE`; tower light: `STEADY RED`; pilot response: continue circling/give way and acknowledge by rocking wings only when not on base/final.<br>
**Español:** Transmisión a ciegas: `TRANSMITIENDO A CIEGAS, [STATION], [CALLSIGN], FALLO DE RADIO, [POSITION], [ALTITUDE], ATERRIZARÉ EN [SUITABLE AERODROME], MENSAJE REPETIDO`; luz de torre: `ROJA FIJA`; respuesta: ceder y continuar circuito, reconocimiento diurno con balanceo de alas fuera de base/final.<br>
**Пояснение:** установите 7600, если оборудование и обстоятельства применимы; 7600 означает отказ связи, а не бедствие. Сохраняйте [VMC](../reference/glossary.md#term-vmc), садитесь на ближайшем подходящем аэродроме и оперативно сообщите о прибытии.<br>
**[Readback][readback]/[acknowledgement][acknowledgement]:** radio repeat may be impossible; use prescribed visual [acknowledgement](../reference/glossary.md#term-acknowledgement) and observe further signals.<br>
**Решение при сомнении:** do not invent runway clearance from an unreadable flash; remain predictable, watch tower and choose safe [VFR](../reference/glossary.md#term-vfr) landing consistent with [SERA](../reference/glossary.md#term-sera)/actual conditions.<br>
Источник: `SRC-EASA-SERA-2025` [SERA](../reference/glossary.md#term-sera).14083, [SERA](../reference/glossary.md#term-sera).14085, [SERA](../reference/glossary.md#term-sera).13005, Appendix 1 Table AP 1-1 (проверено 2026-07-13).

## Безопасность {#safety}

MAYDAY and PAN PAN are not interchangeable labels. 7600 is radio failure, 7700 emergency. Emergency frequency is not for routine checks. Light signals are instructions with different airborne/ground meanings. Never invent runway clearance because radio or light signal is unreadable.

## Типичные ошибки {#common-errors}

1. Автоматически переключаться на emergency frequency 121.500 до попытки использовать рабочую частоту и контекст.
2. Delaying aircraft control to compose a perfect message.
3. Selecting 7700 for simple radio failure or 7600 for [distress](../reference/glossary.md#term-distress).
4. Applying IFR timing/route rules to [ULM](../reference/glossary.md#term-ulm) day [VFR](../reference/glossary.md#term-vfr).
5. Memorising light colour without flight/ground context.

## Конспект {#summary}

- MAYDAY: serious/imminent danger requiring immediate assistance.
- PAN PAN: safety [urgency](../reference/glossary.md#term-urgency) without immediate assistance.
- Start normally on the frequency in use; 121.500 when necessary/desirable for emergency.
- [VFR](../reference/glossary.md#term-vfr) radio failure: attempt contact, 7600 where applicable, stay [VMC](../reference/glossary.md#term-vmc), nearest suitable landing, report arrival.
- Light signals and context must be understood exactly.

## Контрольные вопросы {#review-questions}

### Q-RTC-026 — Как различить MAYDAY и PAN PAN? {#q-rtc-026}

A. Они взаимозаменяемы, если сообщение короткое.<br>
B. MAYDAY требует immediate assistance при serious/imminent danger; PAN PAN — safety [urgency](../reference/glossary.md#term-urgency) без неё.<br>
C. MAYDAY применяется только на 121.500.<br>
D. PAN PAN означает radio failure code.

**Правильный ответ:** B.

**Почему:** [SERA](../reference/glossary.md#term-sera).14095 defines conditions by danger and need for immediate assistance, not by desired frequency.

**Почему главный отвлекающий вариант неверен:** По [SERA](../reference/glossary.md#term-sera).14095 вариант A стирает различие приоритета между MAYDAY и PAN PAN, необходимое всем станциям при emergency traffic.

### Q-RTC-027 — На какой частоте обычно начинают MAYDAY transmission? {#q-rtc-027}

A. Всегда сначала 121.500 независимо от связи.<br>
B. На air-ground frequency in use; 121.500/another frequency when necessary or desirable.<br>
C. На любой сохранённой аэродромной частоте.<br>
D. Только на A/A frequency.

**Правильный ответ:** B.

**Почему:** [SERA](../reference/glossary.md#term-sera).14095 starts with frequency in use and permits emergency frequency as a supplementary measure by circumstances.

**Почему главный отвлекающий вариант неверен:** По [SERA](../reference/glossary.md#term-sera).14095 вариант A безусловно уводит MAYDAY с рабочей частоты на 121.500 и может прервать уже установленную связь.

### Q-RTC-028 — Какой transponder code обозначает radio-[communication failure](../reference/glossary.md#term-communication-failure)? {#q-rtc-028}

A. 7000 — conspicuity/[VFR](../reference/glossary.md#term-vfr) по применимому предписанию.<br>
B. 7500 — unlawful interference.<br>
C. 7600 — radio-[communication failure](../reference/glossary.md#term-communication-failure).<br>
D. 7700 — general emergency.

**Правильный ответ:** C.

**Почему:** [SERA](../reference/glossary.md#term-sera).13005 assigns 7600 to radio-[communication failure](../reference/glossary.md#term-communication-failure) and 7700 to emergency.

**Почему главный отвлекающий вариант неверен:** D alerts general emergency rather than specifically identifying communications failure.

### Q-RTC-029 — Каков [VFR](../reference/glossary.md#term-vfr) outcome после безуспешных попыток восстановить связь? {#q-rtc-029}

A. Продолжить до planned destination в любых условиях.<br>
B. Оставаться [VMC](../reference/glossary.md#term-vmc), сесть на nearest suitable aerodrome и быстро сообщить arrival ATS.<br>
C. Перейти на IFR lost-communications timing без instrument privilege.<br>
D. Орбитировать над controlled aerodrome до восстановления радио.

**Правильный ответ:** B.

**Почему:** [SERA](../reference/glossary.md#term-sera).14083(c)(3) states the [VFR](../reference/glossary.md#term-vfr) visual-conditions/nearest-suitable/report sequence.

**Почему главный отвлекающий вариант неверен:** C imports a separate IFR procedure into a [VFR](../reference/glossary.md#term-vfr) operation and may exceed pilot privileges.

### Q-RTC-030 — Что означает steady red light для aircraft in flight? {#q-rtc-030}

A. Cleared to land.<br>
B. Give way to other aircraft and continue circling.<br>
C. Return to starting point on aerodrome.<br>
D. Cleared for take-off.

**Правильный ответ:** B.

**Почему:** [SERA](../reference/glossary.md#term-sera) Appendix 1 Table AP 1-1 assigns steady red airborne meaning to give way/continue circling.

**Почему главный отвлекающий вариант неверен:** A is the airborne meaning of steady green, not steady red.

## Источники {#sources}

- `SRC-EASA-SERA-2025` — Article 4a; [SERA](../reference/glossary.md#term-sera).13001/13005, 14083, 14085, 14095; Appendix 1 Table AP 1-1.
- `SRC-BOE-RD-1180-2018` — open Spanish implementation/phraseology.
- `SRC-AESA-ULM-RTC-PROGRAM` — national [ULM](../reference/glossary.md#term-ulm) RTC [syllabus](../reference/glossary.md#term-syllabus).
- `SRC-ENAIRE-AIP-GEN-3-4-2026` — current Spain communications context.
- `SRC-EASA-AIRCREW-2026`, `SRC-BOE-FOM-1146-2019` — later LAPL/PPL distinction.

[distress-term]: ../reference/glossary.md#term-distress
[urgency-term]: ../reference/glossary.md#term-urgency
[communication-failure]: ../reference/glossary.md#term-communication-failure
[ssr]: ../reference/glossary.md#term-secondary-surveillance-radar-ssr
[readback]: ../reference/glossary.md#term-readback
[acknowledgement]: ../reference/glossary.md#term-acknowledgement
[ulm]: ../reference/glossary.md#term-ulm
[part-fcl]: ../reference/glossary.md#term-part-fcl
