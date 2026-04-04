# tests/test_price_filter.py
import pytest
import re
from playwright.sync_api import Page, expect
from pages.listing_page import ListingPage


def test_001_price_filter(listing_page: ListingPage):
    #TC-001: Проверка корректности фильтрации объявлений по диапазону цен
    # 1. Действия через методы Page Object
    listing_page.open()
    listing_page.set_price_range(1000, 5000)

    # 2. Получаем данные
    found_prices = listing_page.get_all_prices()

    # 3. если пусто тест не падает
    if not found_prices:
        pytest.skip("Фильтр вернул 0 результатов (нет объявлений в диапазоне)")

    # 4. проверки
    invalid_prices = [p for p in found_prices if not (1000 <= p <= 5000)]

    assert len(invalid_prices) == 0, \
        f"BUG: Найдены цены вне диапазона 1000-5000: {invalid_prices}"
