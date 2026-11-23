# Установка и запуск QuantResearch

Инструкция для macOS по установке QuantResearch из GitHub, настройке окружения и проверке библиотек. Проверенная конфигурация: Python 3.12.13, `uv`, Backtrader, FinamPy, MOEXPy и FinLabPy.

## 1. Требования

- Git
- Python 3.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Visual Studio Code с расширением Python — по желанию

Проверка установленных инструментов:

```bash
git --version
python3.12 --version
uv --version
```

## 2. Клонирование репозитория

Перейдите в каталог, в котором хотите разместить проект, и выполните:

```bash
git clone --recurse-submodules https://github.com/cherniakov/QuantResearch.git
cd QuantResearch
```

Параметр `--recurse-submodules` загружает внешние библиотеки из `external/FinamPy`, `external/MOEXPy` и `external/FinLabPy`.

Проверьте ветку и подмодули:

```bash
git branch --show-current
git submodule status
```

По умолчанию используется стабильная ветка `main`.

Если репозиторий был клонирован без подмодулей, выполните:

```bash
git submodule update --init --recursive
```

## 3. Установка зависимостей

В корневом каталоге QuantResearch выполните:

```bash
uv sync --locked
```

Команда создаёт виртуальное окружение `.venv`, устанавливает зависимости по `uv.lock` и подключает FinamPy, MOEXPy и FinLabPy как локальные Python-зависимости.

Проверьте версию Python:

```bash
uv run python --version
```

Для проверенной конфигурации использовалась версия **Python 3.12.13**. Требование проекта — Python 3.12 или выше согласно `pyproject.toml`.

Предупреждение `Failed to hardlink files; falling back to full copy` не означает сбой установки: `uv` копирует файлы вместо создания жёстких ссылок.

## 4. Проверка импортов

Проверьте библиотеки без настройки `PYTHONPATH`:

```bash
env -u PYTHONPATH uv run python -c "import backtrader; from FinamPy import FinamPy; from MOEXPy import MOEXPy; from FinLabPy.Core import Symbol; print('Все библиотеки — OK')"
```

Ожидаемый результат:

```text
Все библиотеки — OK
```

При первом импорте Backtrader возможны предупреждения `SyntaxWarning: invalid escape sequence`. В проверенной конфигурации они не мешали запуску.

**Важно:** задавать `PYTHONPATH` не требуется. Ранее использовавшийся путь к `external/` следует убрать из локальных настроек окружения, если он там остался.

## 5. Настройка переменных окружения

Создайте локальный файл `.env` из шаблона:

```bash
cp .env.example .env
```

Заполните собственными значениями:

```dotenv
# Finam Trade API
FINAM_TOKEN=

# MOEX API
MOEX_API_TOKEN=
MOEX_LOGIN=
MOEX_PASSWORD=
```

Скрипты сохранения токенов используют `FINAM_TOKEN` и `MOEX_API_TOKEN` соответственно. `MOEX_LOGIN` и `MOEX_PASSWORD` оставлены в шаблоне для других сценариев работы с MOEX; данные скрипты сохранения токенов их не считывают.

**Безопасность:** не добавляйте действующие токены, логины и пароли в `.env.example`, Git или публикации. Файл `.env` исключён из Git через `.gitignore`.

## 6. Сохранение API-токенов

Из корня проекта выполните:

```bash
uv run python scripts/save_finam_token.py
uv run python scripts/save_moex_token.py
```

Скрипты читают значения из `.env` посредством `python-dotenv`. При работе на macOS используемые провайдеры сохраняют данные авторизации в системном хранилище учётных данных.

При отсутствии токенов можно сначала проверить установку и импорты — шаг 4 не требует доступа к брокерским API.

## 7. Работа в Visual Studio Code

Откройте папку проекта:

```bash
code .
```

Если команда `code` не настроена, откройте каталог через **File → Open Folder**.

В VS Code выберите **Python: Select Interpreter** и укажите интерпретатор:

```text
<путь-к-QuantResearch>/.venv/bin/python
```

Запускать скрипты можно через **Run Python File in Terminal** или командой `uv run python` из терминала проекта. Отдельная настройка `PYTHONPATH` не нужна.

## 8. Проверка запуска Backtrader и FinLabPy

Проверка примера Backtrader:

```bash
uv run python "external/FinLabPy/BackTrader/QuickStart/01 - Hello BackTrader.py"
```

После настройки доступа к API можно проверить интеграцию FinLabPy:

```bash
uv run python "external/FinLabPy/BackTrader/QuickStart/02 - Hello FinLabPy Broker.py"
```

В проверенном окружении этот пример выводил стартовый и конечный капитал портфеля.

**Предупреждение:** не запускайте другие брокерские примеры без проверки исходного кода. Некоторые примеры могут выставлять или отменять реальные заявки.

## 9. Запуск JupyterLab

После установки зависимостей запустите исследовательскую среду из корня проекта:

```bash
uv run jupyter lab
```

Подробное руководство по запуску сервера, работе с Notebook и выполнению бэктестов: [Работа с JupyterLab](jupyterlab.md).

## 10. Обновление проекта

Обновите текущую ветку и подмодули до зафиксированных в ней версий, затем синхронизируйте окружение:

```bash
git pull --ff-only
git submodule update --init --recursive
uv sync --locked
```

Не используйте обновление подмодулей до последних внешних коммитов без отдельной проверки совместимости.

## 11. Локальные данные и Git

- `.venv/` — виртуальное окружение, не хранится в Git.
- `.env` — локальные секреты, не хранится в Git.
- `.env.example` — публичный шаблон без секретов, хранится в Git.
- `external/Data/` — локальные биржевые данные, исключены из Git.

Проверка состояния репозитория:

```bash
git status --short
```

После запуска Python могут отображаться записи `? external/FinamPy` и `? external/MOEXPy`: это неотслеживаемые служебные файлы внутри подмодулей. Они не означают, что версии подмодулей изменены.

## 12. Быстрый старт

```bash
git clone --recurse-submodules https://github.com/cherniakov/QuantResearch.git
cd QuantResearch
uv sync --locked
cp .env.example .env
```

Заполните `.env`, при необходимости сохраните токены скриптами из раздела 6 и проверьте импорты командой из раздела 4.

---

Инструкция проверялась на стабильной ветке `main` (коммит `0f7e205`) при чистом клонировании и установке `uv sync --locked` на macOS. Фактические версии и состав зависимостей определяются текущими `pyproject.toml` и `uv.lock`.
