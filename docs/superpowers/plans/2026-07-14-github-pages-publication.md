# GitHub Pages Publication Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Опубликовать проверенный MkDocs-курс из ветки `master` по адресу `https://unet1x.github.io/ULM-course/` через официальный GitHub Pages workflow.

**Architecture:** Один build job устанавливает закреплённые зависимости, настраивает Pages, запускает существующий единый валидатор и передаёт готовый `site/` как Pages artifact. Отдельный deploy job запускается только после успешной сборки для `master`, публикует artifact в environment `github-pages`, а pull request выполняет только проверку. Настройки репозитория изменяются через текущую аутентифицированную GitHub browser session до production-push, затем фактический Actions run и публичные URL проверяются независимо.

**Tech Stack:** MkDocs 1.6.1, Material for MkDocs 9.7.6, Python 3.13, `unittest`, GitHub Actions, GitHub Pages, in-app browser.

## Global Constraints

- Изменять только `.github/workflows/docs.yml`, `tests/test_course.py` и `README.md`; этот план и утверждённая спецификация остаются служебной документацией.
- Не менять учебный текст, тему MkDocs, навигацию, диаграммы, домен или аналитику.
- Не создавать ветку `gh-pages` и не публиковать исходный каталог `docs/`.
- Не заявлять успешную публикацию до зелёного Actions run и HTTP-проверки публичных страниц.

---

## Task 1: Закрепить Pages pipeline тестами и реализовать его

**Files:**

- Modify: `tests/test_course.py:2365`
- Modify: `.github/workflows/docs.yml:1`
- Modify: `README.md:17`

- [ ] **Step 1: Подготовить воспроизводимое Python-окружение**

Run:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Expected: установка `mkdocs==1.6.1` и `mkdocs-material==9.7.6` завершается без ошибки.

- [ ] **Step 2: Добавить падающие regression tests**

В начало `CourseStructureTests` после `test_required_entry_points_exist` добавить:

```python
    def test_github_pages_workflow_deploys_verified_master_site(self):
        workflow = (ROOT / ".github/workflows/docs.yml").read_text(
            encoding="utf-8"
        )
        required_fragments = (
            "pages: write",
            "id-token: write",
            "group: pages",
            "cancel-in-progress: true",
            "actions/configure-pages@v5",
            "actions/upload-pages-artifact@v4",
            "path: site/",
            "needs: build",
            "name: github-pages",
            "actions/deploy-pages@v4",
        )
        for fragment in required_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, workflow)

        self.assertRegex(
            workflow,
            r"(?ms)^  push:\s*\n    branches:\s*\n      - master$",
        )
        self.assertRegex(
            workflow,
            r"(?ms)^  pull_request:\s*\n    branches:\s*\n      - master$",
        )
        self.assertIn(
            "if: github.event_name != 'pull_request' && "
            "github.ref == 'refs/heads/master'",
            workflow,
        )

    def test_readme_links_to_public_course(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("https://unet1x.github.io/ULM-course/", readme)
```

- [ ] **Step 3: Запустить только новые тесты и подтвердить красное состояние**

Run:

```bash
.venv/bin/python -m unittest \
  tests.test_course.CourseStructureTests.test_github_pages_workflow_deploys_verified_master_site \
  tests.test_course.CourseStructureTests.test_readme_links_to_public_course -v
```

Expected: `FAILED (failures=2)`; первый тест сообщает об отсутствии `pages: write`, второй — об отсутствии публичного URL.

- [ ] **Step 4: Заменить verification-only workflow на Pages build/deploy workflow**

Полное содержимое `.github/workflows/docs.yml`:

```yaml
name: Verify and publish course site

on:
  push:
    branches:
      - master
  pull_request:
    branches:
      - master
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: pip

      - name: Install documentation dependencies
        run: python -m pip install -r requirements.txt

      - name: Configure GitHub Pages
        uses: actions/configure-pages@v5

      - name: Validate and build course
        run: python scripts/validate_course.py

      - name: Upload GitHub Pages artifact
        uses: actions/upload-pages-artifact@v4
        with:
          path: site/

  deploy:
    if: github.event_name != 'pull_request' && github.ref == 'refs/heads/master'
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 5: Добавить публичную точку входа в README**

В разделе `## Читать на GitHub` первой строкой добавить:

```markdown
Готовый учебник с навигацией и поиском доступен на
[GitHub Pages](https://unet1x.github.io/ULM-course/). После каждого успешного
обновления ветки `master` сайт публикуется автоматически.
```

Существующую ссылку на `docs/index.md`, каталог источников и журнал выпуска сохранить.

- [ ] **Step 6: Подтвердить зелёные regression tests**

Run:

```bash
.venv/bin/python -m unittest \
  tests.test_course.CourseStructureTests.test_github_pages_workflow_deploys_verified_master_site \
  tests.test_course.CourseStructureTests.test_readme_links_to_public_course -v
```

Expected: `Ran 2 tests` и `OK`.

- [ ] **Step 7: Выполнить полную локальную проверку**

Run:

```bash
.venv/bin/python scripts/validate_course.py
git diff --check
git status --short
```

Expected: все unit tests проходят, строгая MkDocs-сборка завершается без ошибки, `git diff --check` не выводит ошибок, а status показывает только три запланированных изменённых файла.

- [ ] **Step 8: Зафиксировать реализацию**

Run:

```bash
git add .github/workflows/docs.yml tests/test_course.py README.md
git commit -m "feat: publish course with GitHub Pages"
```

Expected: один новый commit в `master`, содержащий только три заявленных файла.

---

## Task 2: Включить Pages, опубликовать и проверить публичный учебник

**Files:**

- Verify: `.github/workflows/docs.yml`
- Verify: `mkdocs.yml`
- Verify: `docs/index.md`
- Verify: `docs/00-start/01-how-to-study.md`
- Verify: `docs/assets/diagrams/ulm-to-lapl-ppl-roadmap.svg`

- [ ] **Step 1: Проверить remote и GitHub browser session**

Run:

```bash
git remote get-url origin
git ls-remote --heads origin master
```

Expected: `origin` указывает на `unet1x/ULM-course`, а удалённая ветка `master` существует. Затем применить skill `browser:control-in-app-browser`, открыть `https://github.com/unet1x/ULM-course` и подтвердить, что текущая GitHub session показывает вкладку `Settings`. Если вкладка недоступна или GitHub требует вход, остановиться и попросить пользователя войти в текущем окне браузера; не сохранять токен или пароль в проекте.

- [ ] **Step 2: Сделать `master` default branch в GitHub UI**

В авторизованном браузере открыть:

`https://github.com/unet1x/ULM-course/settings`

В секции `Default branch` нажать кнопку изменения, выбрать `master`, подтвердить `Update` и предупреждение. Вернуться на главную репозитория и проверить, что branch selector помечает `master` как default.

- [ ] **Step 3: Включить GitHub Actions как источник Pages**

В авторизованном браузере открыть:

`https://github.com/unet1x/ULM-course/settings/pages`

В секции `Build and deployment` установить `Source` в `GitHub Actions`. Если уже выбрано `GitHub Actions`, не менять настройку. Настройка выполняется до production-push, потому что удалённая ветка `master` уже существует и `actions/configure-pages` должен увидеть включённый Pages с первого запуска.

- [ ] **Step 4: Отправить deployment commit**

Run:

```bash
git push origin master
```

Expected: remote `master` обновлён commit из Task 1; push запускает workflow `Verify and publish course site`.

- [ ] **Step 5: Найти и дождаться именно запущенного workflow**

Run локально:

```bash
git rev-parse HEAD
```

Открыть `https://github.com/unet1x/ULM-course/actions/workflows/docs.yml`, выбрать самый новый run для напечатанного commit SHA и дождаться завершения. Expected: jobs `build` и `deploy` получают зелёный статус, а deployment показывает URL Pages. Во время ожидания проверять состояние не реже чем раз в 60 секунд и сообщать пользователю о продолжающейся сборке.

- [ ] **Step 6: Получить канонический URL Pages**

Открыть `https://github.com/unet1x/ULM-course/settings/pages` и проверить опубликованный URL через кнопку `Visit site`.

Expected: URL равен `https://unet1x.github.io/ULM-course/`, source остаётся `GitHub Actions`, интерфейс не показывает ошибку deployment.

- [ ] **Step 7: Проверить публичную главную страницу, урок и SVG**

Run:

```bash
curl --fail --location --retry 6 --retry-delay 10 https://unet1x.github.io/ULM-course/ --output /tmp/ulm-course-index.html
curl --fail --location https://unet1x.github.io/ULM-course/00-start/01-how-to-study/ --output /tmp/ulm-course-first-lesson.html
curl --fail --location https://unet1x.github.io/ULM-course/assets/diagrams/ulm-to-lapl-ppl-roadmap.svg --output /tmp/ulm-course-roadmap.svg
rg -q "Теория ULM/MAF" /tmp/ulm-course-index.html
rg -q "Как учиться" /tmp/ulm-course-first-lesson.html
rg -q "<title" /tmp/ulm-course-roadmap.svg
rg -q "<desc" /tmp/ulm-course-roadmap.svg
```

Expected: все три команды завершаются с exit code 0; главная страница содержит `Теория ULM/MAF`, вложенная страница содержит `Как учиться`, SVG начинается с XML/SVG-разметки и содержит доступные `<title>`/`<desc>`.

- [ ] **Step 8: Проверить чистоту и зафиксировать доказательства выпуска**

Run:

```bash
git status --short
git log -2 --oneline
```

Expected: рабочее дерево чистое, два верхних commit — реализация Pages и план публикации. Повторно открыть run из Step 5 и убедиться, что он по-прежнему показывает успешные build/deploy jobs и deployment URL.

## Definition of Done

- `master` является default branch репозитория.
- Workflow на pull request проверяет и собирает курс без deployment.
- Workflow на push в `master` проверяет, собирает и публикует `site/`.
- Последний Actions run зелёный, а Pages settings сообщает source `GitHub Actions`.
- Главная страница, первый урок и оригинальная SVG-схема доступны публично.
- README ведёт на опубликованный учебник, рабочее дерево чистое.
