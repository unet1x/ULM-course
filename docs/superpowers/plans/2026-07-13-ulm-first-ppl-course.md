# ULM-first PPL(A) Theory Course Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Создать и опубликовать проверяемый русскоязычный курс, который последовательно готовит ученика в Испании сначала к ULM/MAF, а затем расширяет те же темы до PPL(A) Part-FCL.

**Architecture:** Курс строится как статический сайт MkDocs и одновременно остаётся читаемым прямо на GitHub. Каждая предметная область разбивается на ULM-основу, блок «ULM — особо важно» и PPL-расширение; источники, оригинальные термины, вопросы и SVG проверяются автоматическим валидатором. Исследование нормативных источников выполняется параллельно отдельными агентами, но изменения учебника вносятся последовательно, чтобы не конфликтовали навигация, глоссарий и реестр источников.

**Tech Stack:** Markdown, SVG 1.1, Python 3 standard library, MkDocs 1.6.1, Material for MkDocs 9.7.6, GitHub Actions.

## Global Constraints

- Основной маршрут: ULM/MAF в Испании сначала; PPL(A) — встроенное последующее расширение.
- Нормативная дата: 13 июля 2026 года.
- Базовые ULM-нормы: Real Decreto 123/2015 в редакции после Real Decreto 182/2026; Real Decreto 765/2022 в редакции, действующей с 1 апреля 2026 года; Real Decreto 141/2025.
- Базовые PPL-нормы: EASA Easy Access Rules for Aircrew от 24 февраля 2026 года и применимые положения Regulation (EU) No 1178/2011, включая изменения Regulation (EU) 2025/134.
- Изменяемое правило публикуется только с прямой ссылкой на первичный официальный источник и датой проверки.
- Объяснения пишутся по-русски; профессиональные термины сохраняются в канонической English или español форме.
- Первое употребление термина содержит русское объяснение и устойчивый якорь; каждое последующее употребление ссылается на исходное объяснение или глоссарий.
- Все главы используют метки `[ULM — ОСНОВА]`, `[ULM — ОСОБО ВАЖНО]`, `[ОБА]`, `[PPL — РАСШИРЕНИЕ]`, `[ИСПАНИЯ]`, `[МЕЖДУНАРОДНЫЙ ПОЛЁТ]`, `[БЕЗОПАСНОСТЬ]`, `[ПРОВЕРИТЬ ПЕРЕД ПОЛЁТОМ]` по назначению.
- Числовые ограничения конкретного самолёта не обобщаются; AFM/POH конкретного борта имеет приоритет.
- Закрытые банки вопросов и защищённые изображения не копируются; вопросы и SVG создаются заново.
- Стороннее изображение допускается только с проверенной лицензией и записью об атрибуции; по умолчанию создаётся оригинальный SVG.
- Каждый содержательный модуль завершается конспектом, типичными ошибками, задачами, объяснёнными ответами и источниками.
- Ветка реализации: `codex/ulm-first-course`; перед работой создать изолированное рабочее дерево через `superpowers:using-git-worktrees`.
- Лицензия учебного текста и оригинальных схем: Creative Commons Attribution-ShareAlike 4.0 International; служебные скрипты распространяются на тех же условиях для простоты репозитория.

---

## File Map

### Repository and build

- `README.md` — назначение, ULM-first маршрут, чтение на GitHub, локальная сборка, предупреждения.
- `LICENSE` — полный текст CC BY-SA 4.0.
- `CONTRIBUTING.md` — правила источников, терминов, схем и обновлений.
- `requirements.txt` — точные версии MkDocs и темы.
- `mkdocs.yml` — навигация, русская локаль, расширения Markdown и тема.
- `.github/workflows/docs.yml` — проверка и сборка сайта.
- `scripts/validate_course.py` — единая точка автоматической проверки.
- `tests/test_course.py` — проверки структуры, ссылок, источников, терминов, изображений и вопросов.

### Course

- `docs/index.md` — вход в курс и предупреждения.
- `docs/00-start/` — порядок обучения, лицензия, медицина, организации подготовки, план занятий.
- `docs/01-air-law/` — ULM-нормы Испании, Part-FCL, SERA, пространство, AIP/NOTAM.
- `docs/02-human-performance/` — физиология, восприятие, принятие решений.
- `docs/03-meteorology/` — теория, опасности, продукты и go/no-go.
- `docs/04-communications/` — RTC, English/español phraseology, аварийная связь.
- `docs/05-navigation/` — карты, расчёт пути, radio navigation, GNSS, маршрут.
- `docs/06-principles-of-flight/` — аэродинамика, устойчивость, stall/spin, винт и ULM-особенности.
- `docs/07-aircraft-general-knowledge/` — планер, двигатель, Rotax, системы, приборы, BRS.
- `docs/08-performance-planning/` — W&B, performance, fuel planning, расчётные примеры.
- `docs/09-operational-procedures/` — SOP, ground operations, circuit, emergencies.
- `docs/10-flight-preparation/` — briefing, flight plan, документы и полные сценарии.
- `docs/11-international-ulm/` — модель допуска, Франция, Португалия, международный checklist.
- `docs/12-exam-preparation/` — тематические тесты и пробные экзамены.
- `docs/reference/` — glossary, abbreviations, formulas, checklists и templates.
- `docs/sources/official-sources.json` — машиночитаемый реестр источников.
- `docs/sources/official-sources.md` — реестр для читателя и журнал проверки.
- `docs/assets/diagrams/` — оригинальные SVG.

### Research evidence

- `docs/sources/audit-spain-2026.md` — проверка ULM, PPL, SERA, AIP и экзаменационных процедур Испании.
- `docs/sources/audit-technical.md` — карта EASA syllabus и технических официальных пособий.
- `docs/sources/audit-cross-border.md` — правила Франции и Португалии для иностранного ULM.

---

### Task 1: Research evidence pack

**Files:**
- Create: `docs/sources/audit-spain-2026.md`
- Create: `docs/sources/audit-technical.md`
- Create: `docs/sources/audit-cross-border.md`

**Interfaces:**
- Consumes: утверждённая спецификация и Global Constraints этого плана.
- Produces: проверенные утверждения, прямые URL, дата редакции, дата доступа, границы применимости и список спорных мест для всех последующих задач.

- [ ] **Step 1: Dispatch three independent source auditors in parallel**

Первый аудитор проверяет BOE, AESA, ENAIRE/AIP España, AEMET и Part-FCL практику Испании. Второй сопоставляет девять предметов EASA с официальными техническими пособиями FAA/EASA и руководствами производителей. Третий проверяет DGAC/DSAC France и ANAC Portugal для испанского ULM/MAF. Каждый работает только в своём audit-файле и не редактирует учебные главы.

- [ ] **Step 2: Require an evidence row for every rule**

Каждая строка аудита содержит:

```markdown
| ID | Утверждение | Первичный источник | Редакция/дата | Проверено | Ограничение применения |
|---|---|---|---|---|---|
| ES-ULM-LIC-001 | ... | https://official.example/... | 2026-03-12 | 2026-07-13 | Только лицензия ULM, España |
```

- [ ] **Step 3: Verify the known 2026 amendments explicitly**

Проверить и записать без пересказа по памяти:

- `https://www.boe.es/eli/es/rd/2015/02/27/123/con`;
- `https://www.boe.es/eli/es/rd/2026/03/11/182`;
- `https://www.boe.es/eli/es/rd/2022/09/20/765/con`;
- `https://www.boe.es/eli/es/rd/2025/02/25/141`;
- EASA Easy Access Rules for Aircrew от 24 февраля 2026 года;
- Regulation (EU) 2025/134, применяемый с 18 февраля 2026 года;
- французскую страницу `Aéronefs étrangers`, обновлённую в 2025 году;
- португальский Decreto-Lei n.º 283/2007 и действующие страницы ANAC.

- [ ] **Step 4: Run evidence checks**

Run:

```bash
rg -n '^\| [A-Z]{2,}-[A-Z0-9-]+-[0-9]{3} \|' docs/sources/audit-*.md
rg -n '2026-07-13|2026-03-12|2026-04-01' docs/sources/audit-*.md
```

Expected: все три audit-файла содержат evidence rows и даты; отсутствуют правила без официального URL.

- [ ] **Step 5: Commit**

```bash
git add docs/sources/audit-spain-2026.md docs/sources/audit-technical.md docs/sources/audit-cross-border.md
git commit -m "docs: audit 2026 aviation sources"
```

### Task 2: Site foundation and validation harness

**Files:**
- Modify: `.gitignore`
- Create: `README.md`
- Create: `LICENSE`
- Create: `CONTRIBUTING.md`
- Create: `requirements.txt`
- Create: `mkdocs.yml`
- Create: `docs/index.md`
- Create: `scripts/validate_course.py`
- Create: `tests/test_course.py`
- Create: `.github/workflows/docs.yml`

**Interfaces:**
- Consumes: audit-файлы Task 1.
- Produces: собираемый сайт и команда `python3 scripts/validate_course.py`, используемая всеми последующими задачами.

- [ ] **Step 1: Write failing repository-structure tests**

Добавить в `tests/test_course.py` проверки существования `README.md`, `mkdocs.yml`, `docs/index.md`, `docs/sources`, отсутствия `TBD`/`TODO`/`FIXME`, корректных локальных Markdown-ссылок и alt-текста у изображений. Каталог `docs/reference` создаётся и начинает проверяться в Task 3. Использовать только `unittest`, `pathlib`, `re`, `json` и `urllib.parse` standard library.

```python
class CourseStructureTests(unittest.TestCase):
    def test_required_entry_points_exist(self):
        for path in ("README.md", "mkdocs.yml", "docs/index.md"):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_no_incomplete_markers(self):
        forbidden = re.compile(r"\b(?:TBD|TODO|FIXME)\b")
        for path in markdown_files():
            self.assertIsNone(forbidden.search(path.read_text(encoding="utf-8")), path)
```

- [ ] **Step 2: Run tests and confirm the expected failure**

Run: `python3 -m unittest tests.test_course -v`

Expected: FAIL because the entry files and course directories do not yet exist.

- [ ] **Step 3: Create the minimal complete foundation**

`requirements.txt` contains exactly:

```text
mkdocs==1.6.1
mkdocs-material==9.7.6
```

`mkdocs.yml` starts with Russian locale, Material theme, search, navigation sections that already exist, and Markdown extensions `admonition`, `attr_list`, `footnotes`, `md_in_html`, `tables`, `toc` with permalinks. `docs/index.md` states ULM-first order, educational limitations, regulatory date and quick links. `README.md` gives GitHub reading and build commands. Existing `.worktrees/` remains in `.gitignore`; add `site/`, `__pycache__/`, `*.pyc` and `.venv/`.

- [ ] **Step 4: Implement the validator entry point**

`scripts/validate_course.py` runs `unittest` and, when `mkdocs` is available, `python -m mkdocs build --strict`. It returns a non-zero exit status on either failure and never downloads packages itself.

- [ ] **Step 5: Add continuous verification**

`.github/workflows/docs.yml` uses Python 3.13, installs `requirements.txt`, runs `python scripts/validate_course.py`, then uploads the built `site/` artifact. It does not publish until the repository owner enables GitHub Pages.

- [ ] **Step 6: Verify**

Run:

```bash
python3 -m unittest tests.test_course -v
python3 scripts/validate_course.py
```

Expected: PASS; if MkDocs is not installed locally, the validator reports a clear SKIP for build while unit tests still pass.

- [ ] **Step 7: Commit**

```bash
git add .gitignore README.md LICENSE CONTRIBUTING.md requirements.txt mkdocs.yml docs/index.md scripts/validate_course.py tests/test_course.py .github/workflows/docs.yml
git commit -m "feat: scaffold ULM-first course site"
```

### Task 3: Source registry and linked terminology system

**Files:**
- Create: `docs/sources/official-sources.json`
- Create: `docs/sources/official-sources.md`
- Create: `docs/reference/terms.json`
- Create: `docs/reference/glossary.md`
- Create: `docs/reference/abbreviations.md`
- Modify: `tests/test_course.py`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: audit rows from Task 1.
- Produces: source IDs in the form `SRC-...`, term IDs in the form `term-...`, and reference-style links required by all content tasks.

- [ ] **Step 1: Write failing registry tests**

Tests require the new `docs/reference` directory; each source record must have `id`, `authority`, `title`, `url`, `edition`, `checked`, `scope`; each `checked` value equals `2026-07-13`; each URL uses HTTPS and an official domain. Each term record requires `id`, `canonical`, `english`, `spanish`, `russian`, `definition`, `anchor`, `defined_in`.

- [ ] **Step 2: Run the registry tests and confirm failure**

Run: `python3 -m unittest tests.test_course.CourseRegistryTests -v`

Expected: FAIL because registries do not exist.

- [ ] **Step 3: Populate the official source registry**

At minimum include EASA Aircrew 2026, EUR-Lex 1178/2011 and 2025/134, BOE RD 123/2015 consolidated, RD 182/2026, RD 765/2022 consolidated, RD 141/2025, AESA ULM procedure, ENAIRE AIP España, AEMET aviation, DGAC foreign aircraft and ANAC Portugal ultraleves. `official-sources.md` renders the same records for a human reader and explains the source hierarchy.

- [ ] **Step 4: Populate the initial glossary**

Start with terms required in every module: `ULM`, `MAF`, `PPL(A)`, `Part-FCL`, `SERA`, `AIP`, `NOTAM`, `AFM`, `POH`, `PIC`, `VFR`, `VMC`, `IMC`, `angle of attack`, `stall`, `load factor`, `MTOM`, `centre of gravity`, `METAR`, `TAF`, `QNH`, `flight plan`, `radiofonista (RTC)`. Each detailed definition has `<a id="term-slug"></a>` and English/español distinctions.

- [ ] **Step 5: Enforce repeated-term links**

Extend `tests/test_course.py` so each manifest term after its declared definition is written as `[canonical term][term-slug]` or an inline link ending in `#term-slug`. Ignore code fences, URL destinations and the term's own definition line.

- [ ] **Step 6: Verify and commit**

Run: `python3 scripts/validate_course.py`

Expected: PASS with valid JSON, unique IDs, stable anchors and no broken term links.

```bash
git add docs/sources docs/reference tests/test_course.py mkdocs.yml
git commit -m "feat: add verified sources and terminology"
```

### Task 4: ULM-first roadmap and Spanish air law

**Files:**
- Create: `docs/00-start/01-how-to-study.md`
- Create: `docs/00-start/02-ulm-to-ppl-roadmap.md`
- Create: `docs/00-start/03-medical-training-exams.md`
- Create: `docs/01-air-law/01-regulatory-system.md`
- Create: `docs/01-air-law/02-ulm-licence-maf.md`
- Create: `docs/01-air-law/03-rules-of-air.md`
- Create: `docs/01-air-law/04-airspace-spain.md`
- Create: `docs/01-air-law/05-aip-notam-occurrence-reporting.md`
- Create: `docs/01-air-law/06-ppl-extension.md`
- Create: `docs/assets/diagrams/airspace-structure.svg`
- Create: `docs/assets/diagrams/ulm-to-ppl-roadmap.svg`
- Modify: `docs/reference/glossary.md`
- Modify: `docs/reference/terms.json`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: `SRC-BOE-*`, `SRC-AESA-*`, `SRC-EASA-*`, `SRC-ENAIRE-*` and linked terms.
- Produces: точные текущие требования ULM/MAF, учебный порядок и правовую основу, на которую ссылаются все главы.

- [ ] **Step 1: Add failing navigation and source-citation tests**

Tests require all files listed above in `mkdocs.yml`, at least one source ID per normative subsection, visible applicability table in every file and no statement that ULM has automatic Part-FCL recognition.

- [ ] **Step 2: Write the ULM-first start modules**

Cover age, medical, school, theory, practical training, solo, skill test, application, MAF privileges, RTC, recency/revalidation rules, logbook and the transition from ULM to PPL. Every number is taken from the 2026 consolidated law and cited next to the statement.

- [ ] **Step 3: Write air-law modules**

Explain ICAO/EU/Spain hierarchy, EASA vs Annex I/national ULM, SERA rules, right-of-way, VFR/VMC, Spanish airspace, controlled/uncontrolled aerodromes, restricted/prohibited/danger areas, AIP/AIP SUP/AIC/NOTAM and occurrence reporting. Put PPL-only depth after the ULM foundation.

- [ ] **Step 4: Draw the two SVGs**

`airspace-structure.svg` shows conceptual classes and vertical elements without pretending to be a current chart. `ulm-to-ppl-roadmap.svg` shows ULM training, licence, experience and later DTO/ATO PPL route. Both have `<title>`, `<desc>`, high-contrast labels and no raster data.

- [ ] **Step 5: Add questions and explained answers**

At least 30 original questions across the start and air-law files, IDs `Q-START-001...` and `Q-LAW-001...`. Every answer explains why the correct option applies and why the main distractor is wrong.

- [ ] **Step 6: Verify and commit**

Run: `python3 scripts/validate_course.py`

Expected: PASS; all legal statements cite 2026 sources and all new terms link to the glossary.

```bash
git add docs/00-start docs/01-air-law docs/assets/diagrams docs/reference mkdocs.yml tests/test_course.py
git commit -m "feat: add ULM roadmap and Spanish air law"
```

### Task 5: Human performance and aeronautical decision-making

**Files:**
- Create: `docs/02-human-performance/01-physiology.md`
- Create: `docs/02-human-performance/02-vision-hearing-orientation.md`
- Create: `docs/02-human-performance/03-stress-fatigue-medication.md`
- Create: `docs/02-human-performance/04-adm-tem-communication.md`
- Create: `docs/assets/diagrams/hypoxia-response.svg`
- Create: `docs/assets/diagrams/decision-loop.svg`
- Modify: `docs/reference/glossary.md`
- Modify: `docs/reference/terms.json`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: EASA syllabus, official aeromedical material and course terminology.
- Produces: IMSAFE/personal-minima/TEM framework reused by meteorology and flight preparation.

- [ ] **Step 1: Add failing coverage tests**

Require anchors for hypoxia, hyperventilation, carbon monoxide, spatial disorientation, fatigue, medication, alcohol, stress, IMSAFE, situational awareness, TEM and external pressure.

- [ ] **Step 2: Write the four modules in ULM-first order**

Explain mechanisms, recognition, prevention and immediate safe action. Highlight ULM exposure to noise, vibration, cold, turbulence and limited passive protection. PPL extensions cover higher-altitude and longer-duration decision contexts without adding IR training.

- [ ] **Step 3: Add scenarios and diagrams**

Include at least eight go/no-go or continue/divert scenarios and 24 original questions. Diagrams must not give medical treatment advice beyond official first-response guidance.

- [ ] **Step 4: Verify and commit**

Run: `python3 scripts/validate_course.py`

```bash
git add docs/02-human-performance docs/assets/diagrams docs/reference mkdocs.yml tests/test_course.py
git commit -m "feat: add human performance theory"
```

### Task 6: Meteorology for light ULM operations and PPL extension

**Files:**
- Create: `docs/03-meteorology/01-atmosphere-pressure-temperature.md`
- Create: `docs/03-meteorology/02-wind-turbulence-mountain-coast.md`
- Create: `docs/03-meteorology/03-water-clouds-visibility.md`
- Create: `docs/03-meteorology/04-air-masses-fronts-systems.md`
- Create: `docs/03-meteorology/05-hazards-thunderstorm-icing.md`
- Create: `docs/03-meteorology/06-metar-taf-sigmet-charts.md`
- Create: `docs/03-meteorology/07-spain-go-no-go.md`
- Create: `docs/assets/diagrams/fronts-and-pressure.svg`
- Create: `docs/assets/diagrams/thunderstorm-hazards.svg`
- Create: `docs/assets/diagrams/metar-taf-decoder.svg`
- Modify: `docs/reference/glossary.md`
- Modify: `docs/reference/terms.json`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: AEMET products, EASA syllabus, official aviation weather handbooks.
- Produces: weather decision inputs used in Tasks 10–12.

- [ ] **Step 1: Add failing meteorology coverage and calculation tests**

Require pressure/temperature/density, lapse rates with stated assumptions, QNH/QFE/standard setting, wind, gusts, turbulence, sea breeze, mountain wave/rotor, cloud families, fog, fronts, thunderstorms, icing, METAR/SPECI/TAF/SIGMET and Spanish forecast sources.

- [ ] **Step 2: Write theory and worked examples**

Every calculation shows given data, formula, units, substitution, result and operational interpretation. Clearly separate teaching approximations from official values. ULM boxes treat gust factor, crosswind, thermals, rotor and low inertia conservatively.

- [ ] **Step 3: Write product decoding and decisions**

Add at least ten fully decoded synthetic METAR/TAF examples, six Spanish regional scenarios and 35 original questions. Synthetic examples are labeled as such; live weather is never presented as valid for a future flight.

- [ ] **Step 4: Draw and verify diagrams**

Run SVG/XML parsing tests plus `python3 scripts/validate_course.py`.

- [ ] **Step 5: Commit**

```bash
git add docs/03-meteorology docs/assets/diagrams docs/reference mkdocs.yml tests/test_course.py
git commit -m "feat: add ULM-focused meteorology"
```

### Task 7: Communications, RTC and bilingual phraseology

**Files:**
- Create: `docs/04-communications/01-radio-basics-rtc.md`
- Create: `docs/04-communications/02-message-structure.md`
- Create: `docs/04-communications/03-departure-en-es.md`
- Create: `docs/04-communications/04-enroute-arrival-en-es.md`
- Create: `docs/04-communications/05-uncontrolled-aerodrome.md`
- Create: `docs/04-communications/06-urgency-distress-radio-failure.md`
- Create: `docs/assets/diagrams/radio-message-flow.svg`
- Modify: `docs/reference/glossary.md`
- Modify: `docs/reference/terms.json`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: Spanish RTC rules, SERA/ICAO phraseology, AIP España communication procedures.
- Produces: reusable bilingual call scripts for flight scenarios.

- [ ] **Step 1: Add failing phraseology coverage tests**

Require aviation alphabet, numbers, time, callsigns, readback items, departure, position report, joining, landing, uncontrolled aerodrome, MAYDAY, PAN PAN, radio failure, transponder codes and light signals.

- [ ] **Step 2: Write phraseology modules**

Each exchange contains English transmission, Spanish transmission where used in Spain, Russian explanation of intent, and a note identifying what must be read back. Do not invent a universal phrase when official phraseology differs by context.

- [ ] **Step 3: Add interactive study scripts**

Include 20 complete call-and-response scenarios, 30 original questions and blank practice cards in `docs/reference/checklists-radio.md`.

- [ ] **Step 4: Verify and commit**

Run: `python3 scripts/validate_course.py`

```bash
git add docs/04-communications docs/reference docs/assets/diagrams mkdocs.yml tests/test_course.py
git commit -m "feat: add RTC and bilingual phraseology"
```

### Task 8: Navigation and flight-log calculations

**Files:**
- Create: `docs/05-navigation/01-earth-time-directions.md`
- Create: `docs/05-navigation/02-charts-airspace.md`
- Create: `docs/05-navigation/03-heading-track-wind.md`
- Create: `docs/05-navigation/04-dead-reckoning-flight-log.md`
- Create: `docs/05-navigation/05-vor-dme-adf-ppl.md`
- Create: `docs/05-navigation/06-gnss-and-cross-check.md`
- Create: `docs/05-navigation/07-lost-diversion-border.md`
- Create: `docs/assets/diagrams/wind-triangle.svg`
- Create: `docs/assets/diagrams/vor-geometry.svg`
- Create: `docs/assets/diagrams/sample-route.svg`
- Create: `docs/reference/templates-flight-log.md`
- Modify: `docs/reference/glossary.md`
- Modify: `docs/reference/terms.json`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: airspace, weather and communication modules.
- Produces: navigation calculations and flight-log template used by performance and international scenarios.

- [ ] **Step 1: Add failing formula and worked-example tests**

Require units and formulas for time-distance-speed, fuel, wind correction, groundspeed, magnetic/true/compass conversion and 1-in-60 rule. Tests check that each worked example contains `Дано`, `Формула`, `Расчёт`, `Результат`, `Решение пилота`.

- [ ] **Step 2: Write the seven modules**

Teach visual navigation and dead reckoning first for ULM. Put VOR/DME/ADF depth in `[PPL — РАСШИРЕНИЕ]`. Treat GNSS as monitored navigation, include database/RAIM or integrity limitations at PPL-VFR level, and never imply that a moving map authorizes entry into airspace.

- [ ] **Step 3: Add calculation set and route scenario**

Include 20 worked calculations, 35 original questions and one synthetic cross-country flight log. Charts are conceptual and visibly marked `НЕ ДЛЯ НАВИГАЦИИ`.

- [ ] **Step 4: Verify and commit**

Run: `python3 scripts/validate_course.py`

```bash
git add docs/05-navigation docs/reference docs/assets/diagrams mkdocs.yml tests/test_course.py
git commit -m "feat: add navigation and flight-log theory"
```

### Task 9: Principles of flight with ULM-specific handling risks

**Files:**
- Create: `docs/06-principles-of-flight/01-flow-forces-moments.md`
- Create: `docs/06-principles-of-flight/02-lift-drag-polar.md`
- Create: `docs/06-principles-of-flight/03-stability-controls.md`
- Create: `docs/06-principles-of-flight/04-stall-spin-load-factor.md`
- Create: `docs/06-principles-of-flight/05-propeller-effects.md`
- Create: `docs/06-principles-of-flight/06-ulm-low-inertia-gusts.md`
- Create: `docs/assets/diagrams/four-forces.svg`
- Create: `docs/assets/diagrams/angle-of-attack.svg`
- Create: `docs/assets/diagrams/drag-polar.svg`
- Create: `docs/assets/diagrams/three-axis-stability.svg`
- Create: `docs/assets/diagrams/vn-envelope.svg`
- Modify: `docs/reference/glossary.md`
- Modify: `docs/reference/terms.json`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: official PPL syllabus and recognized aerodynamics handbooks.
- Produces: aerodynamic concepts referenced by performance, procedures and emergencies.

- [ ] **Step 1: Add failing concept-coverage tests**

Require angle of attack, boundary layer at PPL level, lift/drag, induced/parasitic drag, stability around three axes, controls, flap effects, stall, spin awareness, load factor, maneuvering/gust envelope and propeller asymmetric effects.

- [ ] **Step 2: Write theory without false simplifications**

Explain Bernoulli and momentum descriptions as compatible views, avoid claiming equal transit time, distinguish stall from low airspeed, and distinguish spin awareness from unauthorized self-training. ULM emphasis covers low inertia, gust response and energy management.

- [ ] **Step 3: Add diagrams, scenarios and questions**

At least six energy-management scenarios and 35 original questions. Every SVG distinguishes conceptual relationships from type-specific numbers.

- [ ] **Step 4: Verify and commit**

Run: `python3 scripts/validate_course.py`

```bash
git add docs/06-principles-of-flight docs/assets/diagrams docs/reference mkdocs.yml tests/test_course.py
git commit -m "feat: add principles of flight"
```

### Task 10: Aircraft general knowledge, Rotax and safety systems

**Files:**
- Create: `docs/07-aircraft-general-knowledge/01-airframe-controls-loads.md`
- Create: `docs/07-aircraft-general-knowledge/02-piston-engine.md`
- Create: `docs/07-aircraft-general-knowledge/03-rotax-operation.md`
- Create: `docs/07-aircraft-general-knowledge/04-fuel-oil-cooling-ignition.md`
- Create: `docs/07-aircraft-general-knowledge/05-propeller-electrical.md`
- Create: `docs/07-aircraft-general-knowledge/06-pitot-static-instruments.md`
- Create: `docs/07-aircraft-general-knowledge/07-avionics-transponder-elt.md`
- Create: `docs/07-aircraft-general-knowledge/08-maintenance-preflight-brs.md`
- Create: `docs/assets/diagrams/four-stroke-cycle.svg`
- Create: `docs/assets/diagrams/fuel-system.svg`
- Create: `docs/assets/diagrams/electrical-system.svg`
- Create: `docs/assets/diagrams/pitot-static.svg`
- Create: `docs/assets/diagrams/brs-decision-boundary.svg`
- Modify: `docs/reference/glossary.md`
- Modify: `docs/reference/terms.json`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: official Rotax operator manuals for named engine families and generic PPL technical syllabus.
- Produces: system knowledge for preflight, performance and emergency procedures.

- [ ] **Step 1: Add failing safety-boundary tests**

Require every Rotax, BRS and maintenance section to carry a visible AFM/POH/operator-manual priority warning and prohibit uncited numeric limits.

- [ ] **Step 2: Write generic aircraft knowledge**

Cover structures, loads, controls, four-stroke engines, carburetion/injection, carb icing, lubrication, cooling, dual ignition, propellers, electrical system, pitot-static and flight instruments, glass cockpit basics, radio/transponder and ELT/PLB.

- [ ] **Step 3: Write ULM-specific system modules**

Explain Rotax architecture and operational differences only where supported by official manuals; use no universal temperature, RPM or fluid value. Explain BRS capabilities, limitations, arming and decision boundaries only generically, directing the reader to the installed system manual.

- [ ] **Step 4: Add preflight examples and questions**

Include a generic ULM walk-around logic, fault-recognition cases and 40 original questions. Do not present a generic checklist as approval for a specific aircraft.

- [ ] **Step 5: Verify and commit**

Run: `python3 scripts/validate_course.py`

```bash
git add docs/07-aircraft-general-knowledge docs/assets/diagrams docs/reference mkdocs.yml tests/test_course.py
git commit -m "feat: add aircraft and ULM systems theory"
```

### Task 11: Mass, balance, performance and fuel planning

**Files:**
- Create: `docs/08-performance-planning/01-mass-balance.md`
- Create: `docs/08-performance-planning/02-takeoff-climb-landing.md`
- Create: `docs/08-performance-planning/03-density-altitude.md`
- Create: `docs/08-performance-planning/04-fuel-range-endurance.md`
- Create: `docs/08-performance-planning/05-ulm-worked-example.md`
- Create: `docs/08-performance-planning/06-ppl-worked-example.md`
- Create: `docs/assets/diagrams/mass-balance.svg`
- Create: `docs/assets/diagrams/performance-factors.svg`
- Create: `docs/reference/formulas.md`
- Modify: `docs/reference/glossary.md`
- Modify: `docs/reference/terms.json`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: navigation formulas, weather density concepts and aircraft manual priority rule.
- Produces: completed planning calculations for Tasks 12 and 13.

- [ ] **Step 1: Add failing calculation-format tests**

Require SI and aviation units, conversions, assumptions, rounding rule and operational conclusion for every worked calculation. Require synthetic aircraft data to be labeled `УЧЕБНЫЕ ДАННЫЕ — НЕ ДЛЯ ПОЛЁТА`.

- [ ] **Step 2: Write mass-and-balance and performance theory**

Cover mass, arm, moment, centre of gravity, envelope, takeoff/landing factors, runway surface/slope/wind/temperature/obstacle, climb, cruise, range, endurance and reserve logic. ULM emphasis explains payload sensitivity and small margin consequences.

- [ ] **Step 3: Add two complete worked dossiers**

One synthetic ULM and one synthetic SEP PPL example each include loading, CG, takeoff, landing, climb, cruise, fuel, alternate and go/no-go decision. Use deliberately fictional performance tables to prevent operational misuse.

- [ ] **Step 4: Add 30 questions, verify and commit**

Run: `python3 scripts/validate_course.py`

```bash
git add docs/08-performance-planning docs/assets/diagrams docs/reference mkdocs.yml tests/test_course.py
git commit -m "feat: add performance and planning calculations"
```

### Task 12: Operational procedures and complete flight preparation

**Files:**
- Create: `docs/09-operational-procedures/01-sop-checklists-ground.md`
- Create: `docs/09-operational-procedures/02-taxi-circuit-wake.md`
- Create: `docs/09-operational-procedures/03-short-soft-crosswind.md`
- Create: `docs/09-operational-procedures/04-engine-failure-forced-landing.md`
- Create: `docs/09-operational-procedures/05-fire-system-emergencies.md`
- Create: `docs/09-operational-procedures/06-after-incident.md`
- Create: `docs/10-flight-preparation/01-pilot-aircraft-environment.md`
- Create: `docs/10-flight-preparation/02-briefing-route-alternates.md`
- Create: `docs/10-flight-preparation/03-ats-flight-plan.md`
- Create: `docs/10-flight-preparation/04-local-flight-scenario.md`
- Create: `docs/10-flight-preparation/05-cross-country-scenario.md`
- Create: `docs/assets/diagrams/aerodrome-circuit.svg`
- Create: `docs/assets/diagrams/forced-landing-priorities.svg`
- Create: `docs/assets/diagrams/preflight-decision-gates.svg`
- Create: `docs/reference/checklists-flight.md`
- Modify: `docs/reference/glossary.md`
- Modify: `docs/reference/terms.json`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: all theory modules and planning outputs.
- Produces: end-to-end ULM flight workflow and PPL extensions.

- [ ] **Step 1: Add failing procedure-boundary tests**

Require every maneuver/emergency discussion to state that instructor and aircraft checklist take precedence. Require no generic memory item to masquerade as a type-specific checklist.

- [ ] **Step 2: Write normal and abnormal operations**

Cover ramp/fuel/fire safety, start, taxi in wind, circuit, wake turbulence, short/soft field concepts, crosswind decisions, precautionary landing, engine failure, forced landing priorities, fire, system faults and post-incident actions. Highlight ULM energy and wind sensitivity.

- [ ] **Step 3: Write complete planning scenarios**

The local and cross-country scenarios explicitly walk through documents, pilot fitness, maintenance status, weather, NOTAM, airspace, W&B, performance, fuel, communication, diversion and cancellation gates.

- [ ] **Step 4: Add questions, verify and commit**

At least 40 original questions across Tasks 9 and 10 course parts.

Run: `python3 scripts/validate_course.py`

```bash
git add docs/09-operational-procedures docs/10-flight-preparation docs/assets/diagrams docs/reference mkdocs.yml tests/test_course.py
git commit -m "feat: add procedures and flight preparation"
```

### Task 13: International ULM operations — France and Portugal

**Files:**
- Create: `docs/11-international-ulm/01-why-national.md`
- Create: `docs/11-international-ulm/02-six-layer-check.md`
- Create: `docs/11-international-ulm/03-france.md`
- Create: `docs/11-international-ulm/04-portugal.md`
- Create: `docs/11-international-ulm/05-cross-border-scenario.md`
- Create: `docs/11-international-ulm/06-authority-request-templates.md`
- Create: `docs/assets/diagrams/international-ulm-decision-tree.svg`
- Create: `docs/reference/checklists-international.md`
- Modify: `docs/reference/glossary.md`
- Modify: `docs/reference/terms.json`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: cross-border audit, air law, flight preparation, radio and navigation.
- Produces: dated, country-specific decision process without promising automatic recognition.

- [ ] **Step 1: Add failing cross-border safety tests**

Require each country page to contain the exact checked date, official authority link, aircraft-document check, pilot-privilege check, insurance check, radio check, operational/airspace check, aerodrome check and `[ПРОВЕРИТЬ ПЕРЕД ПОЛЁТОМ]` warning.

- [ ] **Step 2: Write the legal model and country pages**

Explain separately pilot privileges, aircraft status, insurance, radio, national operating rules and aerodrome access. For France apply the official European ULM conditions and French definition check. For Portugal apply the current ANAC/legal conditions, including any current duration or authorization requirements only if confirmed by the audit.

- [ ] **Step 3: Add a synthetic Spain–France–Portugal scenario**

Walk through a notional trip without using stale NOTAM or claiming a route is currently open. Include bilingual email templates that ask the authority or aerodrome for written confirmation.

- [ ] **Step 4: Verify and commit**

Run: `python3 scripts/validate_course.py`

```bash
git add docs/11-international-ulm docs/assets/diagrams docs/reference mkdocs.yml tests/test_course.py
git commit -m "feat: add international ULM operations"
```

### Task 14: Exam preparation, question bank and study schedule

**Files:**
- Create: `docs/12-exam-preparation/01-study-strategy.md`
- Create: `docs/12-exam-preparation/02-ulm-mock-1.md`
- Create: `docs/12-exam-preparation/03-ulm-mock-2.md`
- Create: `docs/12-exam-preparation/04-ppl-extension-mock-1.md`
- Create: `docs/12-exam-preparation/05-ppl-extension-mock-2.md`
- Create: `docs/12-exam-preparation/06-answer-key.md`
- Create: `docs/reference/study-plan-16-weeks.md`
- Modify: `tests/test_course.py`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: all module questions and learning objectives.
- Produces: traceable, original mock exams and a ULM-first study plan.

- [ ] **Step 1: Add failing question-integrity tests**

Require globally unique IDs, exactly one marked correct answer, a non-empty explanation, a link back to the teaching section, a source ID for regulatory questions, and no claim that questions come from an official closed bank.

- [ ] **Step 2: Build the ULM-first question bank**

Create two balanced ULM/MAF mocks covering Spanish law, human performance, meteorology, communication/RTC, navigation, principles, systems, performance and operations. Each mock has at least 60 original questions.

- [ ] **Step 3: Build PPL extension mocks**

Create two at-least-90-question study sets mapped across the nine EASA subjects. They are learning assessments, not representations of AESA's current delivery format unless the source audit verifies that format.

- [ ] **Step 4: Write explanations and traceability**

Every answer includes the reasoning, the main misconception, a section link and sources when the answer is normative. The 16-week plan marks the ULM-ready checkpoint before optional PPL-extension weeks.

- [ ] **Step 5: Verify and commit**

Run: `python3 scripts/validate_course.py`

Expected: PASS with no duplicate or unexplained questions.

```bash
git add docs/12-exam-preparation docs/reference/study-plan-16-weeks.md tests/test_course.py mkdocs.yml
git commit -m "feat: add ULM and PPL study assessments"
```

### Task 15: Whole-course editorial, visual and regulatory verification

**Files:**
- Modify: all files identified by verification findings
- Create: `docs/sources/release-audit-2026-07-13.md`
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: complete course.
- Produces: release-ready repository with recorded evidence.

- [ ] **Step 1: Run the full automated suite from a clean environment**

Run:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_course.py
python3 -m mkdocs build --strict
```

Expected: all tests PASS and MkDocs exits 0 with no warnings.

- [ ] **Step 2: Perform syllabus traceability review**

Create `release-audit-2026-07-13.md` with one row for every ULM requirement found in the Spanish audit and every item of the PPL(A) EASA syllabus, linking each to a course section. No uncovered item may be marked complete.

- [ ] **Step 3: Perform terminology and source review**

Check every professional term against `terms.json`, every repeated occurrence link, every normative statement against `official-sources.json`, and every checked date. Resolve all Critical and Important findings before proceeding.

- [ ] **Step 4: Render and inspect all SVGs and representative pages**

Use an installed SVG renderer or browser screenshots to inspect every diagram at desktop and narrow width. Check title, description, contrast, clipped labels and legibility. Inspect the homepage, one chapter from every part, glossary, formula reference, country pages and mock exams.

- [ ] **Step 5: Independently recalculate every worked example**

Record the recalculation result in the release audit. Correct arithmetic, units, rounding and operational interpretation together.

- [ ] **Step 6: Request final whole-branch review**

Provide the reviewer the approved specification, this plan, implementation report and full diff package. Require separate verdicts for specification compliance, source quality, pedagogical clarity, ULM priority and repository quality.

- [ ] **Step 7: Run final verification after review fixes**

Run:

```bash
python3 scripts/validate_course.py
python3 -m mkdocs build --strict
git diff --check
git status --short
```

Expected: tests and build PASS, `git diff --check` exits 0, status contains only intended release-audit/README fixes before commit.

- [ ] **Step 8: Commit the verified release**

```bash
git add README.md CONTRIBUTING.md mkdocs.yml docs scripts tests .github requirements.txt LICENSE
git commit -m "docs: complete verified ULM-first aviation course"
```

- [ ] **Step 9: Push and report remote state**

Run:

```bash
git push -u origin codex/ulm-first-course
```

Expected: remote branch exists. If GitHub authentication or permissions block the push, preserve all local commits and report the exact command the owner must run.

---

## Plan Self-Review Checklist

- Every design criterion maps to at least one task.
- ULM is the first usable milestone; PPL material never blocks the ULM path.
- 2026 Spanish amendments are explicit in the research and air-law tasks.
- All nine PPL subjects are covered.
- International flight claims require country-specific source checks.
- Every technical diagram is original SVG unless separately licensed.
- Every module has questions and explained answers.
- The terminology-link rule is machine-checked.
- Each task has an independently executable verification command and commit boundary.
