# Autotests Project

API и UI автотесты. API тесты идут против Mock Petstore (http.server, stdlib) — никаких внешних зависимостей. UI тесты идут против https://www.saucedemo.com через Selenium + ChromeDriver (webdriver-manager).

## Установка

```bash
pip install -r requirements.txt
```

## Запуск тестов

```bash
# Все тесты
pytest

# Только API (без браузера)
pytest -m api

# Только UI
pytest -m ui
```

После каждого прогона:
- Allure-отчёт генерируется в `allure-report/` (если есть Java)
- Скриншот отчёта сохраняется в `screenshots/`

Для просмотра Allure-отчёта в браузере:
```bash
allure serve allure-results
```

## Структура проекта

```
├── config/              # Конфигурация (.env → settings.py)
├── api/                 # API клиент и эндпоинты
├── schemas/             # Pydantic-схемы валидации
├── pages/               # Page Object Model для UI
├── tests/
│   ├── conftest.py      # Фикстуры API (mock server, base_url)
│   ├── mock_server.py   # Mock Petstore на http.server
│   ├── browser_utils.py # Поиск браузера (общий для UI и скриншотов)
│   ├── screenshot_report.py  # Allure generate + скриншот
│   ├── api/             # API-тесты (pytest -m api)
│   └── ui/              # UI-тесты (pytest -m ui)
├── conftest.py          # pytest_sessionfinish → отчёт + скриншот
├── pytest.ini
└── requirements.txt
```

## Mock Petstore

`tests/mock_server.py` имплементирует REST-endpoints:
- `POST /v2/pet` — создать питомца
- `GET /v2/pet/{id}` — получить по ID
- `PUT /v2/pet` — обновить
- `DELETE /v2/pet/{id}` — удалить
- `GET /v2/pet/findByStatus` — поиск по статусу

Стартует автоматически в conftest.py, если реальный Petstore недоступен.
