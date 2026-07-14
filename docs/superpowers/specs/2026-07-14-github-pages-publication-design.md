# Дизайн публикации курса через GitHub Pages

## 1. Цель

Опубликовать существующий MkDocs-курс из репозитория `unet1x/ULM-course` как
общедоступный статический учебник с темой Material, боковой навигацией, поиском
и SVG-иллюстрациями. Канонической веткой публикации становится `master`, а
ожидаемый адрес сайта — `https://unet1x.github.io/ULM-course/`.

## 2. Выбранный подход

Используется официальный GitHub Pages deployment через GitHub Actions. MkDocs
создаёт готовый каталог `site/`; workflow упаковывает именно этот каталог через
`actions/upload-pages-artifact`, а отдельный deploy job публикует его через
`actions/deploy-pages` в environment `github-pages`.

Отдельная ветка `gh-pages` не создаётся. Публикация сырого каталога `docs/`
исключена, потому что она не сохраняет сборку MkDocs Material и поиск.

## 3. Состояние репозитория и изменения

Существующий `.github/workflows/docs.yml` уже устанавливает Python и
зависимости, запускает `scripts/validate_course.py` и получает `site/`, но
загружает его как обычный Actions artifact. Workflow нужно расширить, не
разделяя проверку курса и построение сайта на разные несовместимые пути.

Изменяются только:

- `.github/workflows/docs.yml` — официальный Pages build/deploy pipeline;
- `tests/test_course.py` — regression contract deployment-конфигурации;
- `README.md` — публичная ссылка и краткое объяснение автоматической публикации.

## 4. События и ветки

Workflow сохраняет три входа:

- `pull_request` в `master`: проверка и сборка без публикации;
- `push` в `master`: проверка, сборка и публикация;
- `workflow_dispatch` из `master`: ручная повторная публикация.

Deploy job выполняется только для `refs/heads/master` и никогда не выполняется
для pull request. Репозиторий GitHub переводится на default branch `master`.

## 5. Workflow

### 5.1. Права и concurrency

Workflow получает минимальные права:

- `contents: read` для checkout;
- `pages: write` для публикации;
- `id-token: write` для подтверждения происхождения deployment.

Concurrency group называется `pages`; незавершённая старая публикация
отменяется при появлении более новой.

### 5.2. Build job

Build job выполняет следующую последовательность:

1. `actions/checkout@v4`;
2. `actions/setup-python@v5` с Python 3.13 и pip cache;
3. `python -m pip install -r requirements.txt`;
4. `actions/configure-pages@v5`;
5. `python scripts/validate_course.py`;
6. `actions/upload-pages-artifact@v4` с `path: site/`.

Обычный `actions/upload-artifact` удаляется, чтобы deployment использовал
специализированный и ожидаемый GitHub Pages artifact.

### 5.3. Deploy job

Deploy job:

- зависит от успешного build job через `needs: build`;
- работает только не для pull request и только на `master`;
- использует environment `github-pages`;
- публикует через `actions/deploy-pages@v4`;
- передаёт полученный `page_url` в URL environment.

## 6. Настройки GitHub

После push выполняются две административные операции:

1. default branch репозитория устанавливается в `master`;
2. Pages build type устанавливается в `workflow` (`Source: GitHub Actions`).

Операции выполняются через аутентифицированный GitHub CLI/API или текущую
авторизованную browser session. Если доступ администратора недоступен, работа
останавливается с точным указанием единственного ручного действия; успешный
deployment не заявляется до фактической проверки сайта.

## 7. Проверки и TDD

До изменения workflow добавляется тест, который обязан упасть на текущем
verification-only файле. Тест проверяет:

- ограничение production push веткой `master`;
- необходимые Pages/OIDC permissions;
- `configure-pages@v5`;
- `upload-pages-artifact@v4` и `path: site/`;
- deploy job с `needs: build`, environment `github-pages` и
  `deploy-pages@v4`;
- защиту deploy job от запуска на pull request;
- concurrency группы Pages.

После минимальной правки workflow запускаются сначала новый тест, затем полный
`scripts/validate_course.py` и `git diff --check`.

## 8. Публикация и критерии готовности

Результат считается опубликованным только если одновременно выполнены все
условия:

1. изменения закоммичены и отправлены в `master`;
2. GitHub Actions run для отправленного коммита завершён успешно;
3. GitHub Pages сообщает URL deployment;
4. `https://unet1x.github.io/ULM-course/` отвечает успешно;
5. заголовок курса, навигация и один вложенный раздел доступны по публичным
   URL, а SVG-ресурс загружается без ошибки.

## 9. Границы

В эту работу не входят собственный домен, аналитика, аутентификация,
редизайн темы, изменение содержания курса или создание второго hosting
провайдера. GitHub Pages публикует только уже проверенный MkDocs output.
