# tests/test_urgent.py
import pytest
from pages.listing_page import ListingPage


def test_005_urgent_toggle(listing_page: ListingPage):

    #TC-005: Проверка работы тогла "Только срочные"

    # 1. Открываем страницу
    listing_page.open()

    # 2. Получаем статистику до включения фильтра
    initial_count = listing_page.get_ads_count()

    # 3. Включаем тогл "Только срочные"
    listing_page.toggle_urgent_only(enable=True)

    # 4. Проверяем результаты
    filtered_count = listing_page.get_ads_count()
    urgent_statuses = listing_page.get_all_ads_urgent_status()

    # Если нет объявлений — пропускаем тест
    if filtered_count == 0:
        pytest.skip("Нет срочных объявлений для проверки")

    # Проверяем, что ВСЕ отображенные объявления — срочные
    non_urgent_indices = [i for i, is_urgent in enumerate(urgent_statuses) if not is_urgent]

    if non_urgent_indices:
        pytest.fail(
            f"\nBUG: Тогл 'Только срочные' не фильтрует!\n"
            f"   Всего показано: {filtered_count} объявлений (было: {initial_count})\n"
            f"   Срочных: {sum(urgent_statuses)}/{len(urgent_statuses)}\n"
            f"   Не-срочных (ошибка): {len(non_urgent_indices)}\n"
            f"   Позиции с ошибкой: {non_urgent_indices[:10]}"
        )

    # Постусловие: выключаем тогл (всегда, даже если тест прошёл)
    try:
        listing_page.toggle_urgent_only(enable=False)
    except Exception:
        pass