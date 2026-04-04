# tests/test_sorting_descending_price.py
import pytest
from pages.listing_page import ListingPage


def test_003_sort_by_price_descending(listing_page: ListingPage):

    # TC-003: Сортировка объявлений по убыванию цены

    # 1. Открываем страницу
    listing_page.open()

    # 2. Применяем сортировку
    listing_page.set_sorting(sort_by="Цена", order="По убыванию")

    # 3. Собираем цены
    prices = listing_page.get_all_prices()

    # Если мало данных — пропускаем тест
    if len(prices) < 2:
        pytest.skip("Недостаточно объявлений для проверки сортировки")

    # 4. Проверяем, что цены отсортированы по убыванию
    expected_prices = sorted(prices, reverse=True)
    is_sorted = prices == expected_prices

    if not is_sorted:
        # Находим позиции, где нарушен порядок (текущая < следующей)
        violations = [
            i for i in range(len(prices) - 1)
            if prices[i] < prices[i + 1]
        ]

        pytest.fail(
            f"\nBUG: Сортировка по убыванию не работает!\n"
            f"   Найдено {len(prices)} объявлений\n"
            f"   Фактический порядок: {prices}\n"
            f"   Ожидаемый порядок:   {expected_prices}\n"
            f"   Нарушения на позициях: {violations}\n"
        )