import pytest
import re
from playwright.sync_api import Page, expect

def test_001_price_filter(page: Page):

    #TC-001: Проверка корректности фильтрации объявлений по диапазону цен

    # 1. Открываем страницу списка
    page.goto("/")
    page.wait_for_load_state("networkidle")

    # 2. Вводим диапазон цен
    min_input = page.get_by_placeholder("От", exact=True)
    max_input = page.get_by_placeholder("До", exact=True)

    min_val, max_val = 1000, 5000
    min_input.click()
    min_input.fill(str(min_val))
    max_input.click()
    max_input.fill(str(max_val))

    # Ждем появления хотя бы одной видимой карточки с ценой
    page.wait_for_selector("xpath=//*[@class='_card__price_15fhn_241']", state="visible", timeout=5000)

    # Берем  видимые цены (игнорируем скрытые)
    prices = page.locator("xpath=//*[@class='_card__price_15fhn_241']").filter(visible=True)
    page.wait_for_timeout(500)

    # 4. Проверяем, что есть результаты
    if prices.count() == 0:
        pytest.skip("Фильтр вернул 0 результатов")

    # 5. Собираем цены
    found_prices = []
    for i in range(prices.count()):
        raw_text = prices.nth(i).inner_text()
        clean_price = re.sub(r'[^\d]', '', raw_text)
        if clean_price:
            found_prices.append(int(clean_price))

    #все найденные цены должны быть в диапазоне
    for price in found_prices:
        assert min_val <= price <= max_val, \
            f" BUG: Цена {price} не входит в диапазон {min_val}-{max_val}"

