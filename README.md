# qa-test-assignment
Тестовое задание на стажировку QA - Автоматизация тестирования

## Задание 1: Скриншот с багами
Найденные дефекты оформлены в файле: [bugs.md](https://github.com/idexlism/qa-test-assignment/blob/main/BUGS.md)

## Задание 2.2: Тесты UI

### Требования
- Python 3.8+
- pip

### Установка
1. **Клонируйте репозиторий:**
 - `git clone https://github.com/idexlism/qa-test-assignment`
 - `cd qa-test-assignment`

2. **Установите зависимости:**
- `pip install -r requirements.txt`

4. **Установите браузеры Playwright**
- `playwright install`

## Запуск тестов
- Все тесты: `python -m pytest -v`

- Все тесты с открытием браузера: `python -m pytest -v --headed`

- Конкретный тест-кейс:
  
| Команда | Тест-кейсы | Описание |
|---------|------------|----------|
| `python -m pytest tests/test_price_filter.py -v` | TC-001 | Фильтр цен |
| `python -m pytest tests/test_sorting.py -v` | TC-002, TC-003 | Сортировка (возрастание/убывание) |
| `python -m pytest tests/test_category.py -v` | TC-004 | Фильтр по категории |
| `python -m pytest tests/test_urgent.py -v` | TC-005 | Тоггл "Только срочные" |
| `python -m pytest tests/test_stats_refresh.py -v` | TC-006 | Кнопка "Обновить" |
| `python -m pytest tests/test_stats_timer_play.py -v` | TC-007 | Запуск таймера |
| `python -m pytest tests/test_stats_timer_pause.py -v` | TC-008 | Остановка таймера |
| `python -m pytest tests/test_theme_listings.py -v` | TC-009, TC-010 | Темы (объявления) |
| `python -m pytest tests/test_theme_stats.py -v` | TC-011, TC-012 | Темы (статистика) |

## Конфигурация
Настройки тестов находятся в `pytest.ini`:
- **Режим по умолчанию:** Headless (без открытия окна браузера)
- **Браузер:** Chromium
- **Детализация:** Подробный вывод (`-v -s`) с цветами
