# Autotests Project

API и UI автотесты. API тесты идут против Mock Petstore (http.server, stdlib) — никаких внешних зависимостей. UI тесты идут против https://www.saucedemo.com через Selenium + ChromeDriver (webdriver-manager).

## Установка

```bash
pip install -r requirements.txt
```

## Переменные окружения

Скопируйте `.env.example` в `.env` и настройте под свою среду:
```bash
cp .env.example .env
```

## Запуск тестов

```bash
python tasks.py test          # все тесты
python tasks.py test-api      # только API
python tasks.py test-ui       # только UI
python tasks.py test-parallel # параллельно
```

Или напрямую через pytest:
```bash
pytest -m api
pytest -m ui
pytest -n auto
```

## Генерация отчёта

Отчёт генерируется автоматически после каждого прогона тестов.
Для ручной генерации и просмотра:

```bash
python tasks.py report
```

Для скриншота отчёта:
```bash
python tasks.py screenshot
```

## Очистка

```bash
python tasks.py clean
```

Все команды:
```bash
python tasks.py --help
```

## Структура проекта

```
├── config/              # Конфигурация (.env → settings.py)
├── api/                 # API клиент и эндпоинты
├── schemas/             # Pydantic-схемы валидации
├── pages/               # Page Object Model для UI
├── utils/               # Общая инфраструктура
│   └── mock_server.py   # Mock Petstore на http.server
├── tests/
│   ├── api/             # API-тесты (pytest -m api)
│   └── ui/              # UI-тесты (pytest -m ui)
├── browser_utils.py     # Поиск браузера
├── screenshot_report.py # Скриншот Allure-отчёта
├── tasks.py             # Команды для разработчика
├── conftest.py          # Корневой conftest (mock server, base_url)
├── pyproject.toml       # Конфигурация проекта
├── docker-compose.yml   # Локальный Petstore
├── .env.example         # Шаблон переменных окружения
└── requirements.txt     # Зависимости
```

## Mock Petstore

`utils/mock_server.py` имплементирует REST-endpoints:
- `POST /v2/pet` — создать питомца
- `GET /v2/pet/{id}` — получить по ID
- `PUT /v2/pet` — обновить
- `DELETE /v2/pet/{id}` — удалить
- `GET /v2/pet/findByStatus` — поиск по статусу

Стартует автоматически в conftest.py, если реальный Petstore недоступен.
Для запуска реального Petstore локально:
```bash
docker compose up -d
```
