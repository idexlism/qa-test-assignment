# tests/test_sorting_ascending_price.py
import pytest
from pages.listing_page import ListingPage


def test_002_sort_by_price_ascending(listing_page: ListingPage):

    # TC-002: Сортировка объявлений по возрастанию цены

    # 1. Открываем страницу
    listing_page.open()

    # 2. Применяем сортировку
    listing_page.set_sorting(sort_by="Цена", order="По возрастанию")

    # 3. Собираем цены
    prices = listing_page.get_all_prices()

    if len(prices) < 2:
        pytest.skip("Недостаточно объявлений для проверки сортировки")

    # 4. Проверяем сортировку
    sorted_prices = sorted(prices)
    is_sorted = prices == sorted_prices

    if not is_sorted:
        # Находим где нарушен порядок
        violations = [i for i in range(len(prices) - 1) if prices[i] > prices[i + 1]]

        pytest.fail(
            f"\nBUG: Сортировка по возрастанию не работает!\n"
            f"   Найдено {len(prices)} объявлений\n"
            f"   Фактический порядок: {prices}\n"
            f"   Ожидаемый порядок:   {sorted_prices}\n"
            f"   Нарушения на позициях: {violations}"
        )