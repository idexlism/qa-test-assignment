# tests/test_theme_listings.py
import pytest
from pages.listing_page import ListingPage
from playwright.sync_api import Page


@pytest.fixture
def listing_mobile_page(mobile_page: Page) -> ListingPage:
    return ListingPage(mobile_page)


def test_009_theme_light_to_dark(listing_mobile_page: ListingPage):
    #TC-009: Переключение в тёмную тему на странице Объявления (Светлая -> Темная)
    listing_mobile_page.open()

    # Убеждаемся, что стартуем со светлой темы
    listing_mobile_page.set_theme(is_dark=False)

    # Действие: переключаем на тёмную
    listing_mobile_page.set_theme(is_dark=True)

    # Проверки
    assert listing_mobile_page.is_dark_theme(), "Тема не переключилась на тёмную"
    assert listing_mobile_page.theme_toggle.is_visible(), "Кнопка переключения темы не видима"

    # Постусловие: возвращаем светлую тему
    listing_mobile_page.set_theme(is_dark=False)


def test_010_theme_dark_to_light(listing_mobile_page: ListingPage):
    #TC-010: Переключение в светлую тему на странице Объявления (Темная -> Светлая)
    listing_mobile_page.open()

    # Предусловие: включаем тёмную тему
    listing_mobile_page.set_theme(is_dark=True)
    assert listing_mobile_page.is_dark_theme(), "Не удалось подготовить тёмную тему"

    # Действие: переключаем на светлую
    listing_mobile_page.set_theme(is_dark=False)

    # Проверки
    assert not listing_mobile_page.is_dark_theme(), "Тема не переключилась на светлую"
