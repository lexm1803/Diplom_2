# Автоматизированные тесты API сервиса Stellar Burgers.

## Стек технологий

- Python 3.11+
- pytest
- httpx
- pydantic
- allure-pytest

## Структура проекта

```
praktikum-api/
├── tests/
│ ├── api/ # Тесты по функциональности
│ ├── builders/ # Генераторы тестовых данных
│ ├── client/ # Фасады для работы с API
│ └── schemas/ # Pydantic-модели запросов и ответов
├── pytest.ini
└── README.md
```

## Запуск тестов

1. Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Запустите тесты:

```bash
pytest
```

3. Сгенерируйте Allure-отчёт:

```bash
pytest --alluredir=./allure-results
allure serve ./allure-results
```

## Переменные окружения

`API_BASE_URL` — базовый URL API (по умолчанию: `https://stellarburgers.education-services.ru`).

