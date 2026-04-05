# tests/test_theme_stats.py
import pytest
from pages.stats_page import StatsPage
from playwright.sync_api import Page


@pytest.fixture
def stats_mobile_page(mobile_page: Page) -> StatsPage:
    return StatsPage(mobile_page)


def test_011_theme_light_to_dark(stats_mobile_page: StatsPage):
    #TC-011: Переключение в тёмную тему на странице Статистика (Светлая -> Темная)
    stats_mobile_page.open()
    stats_mobile_page.set_theme(is_dark=False)

    # Действие
    stats_mobile_page.set_theme(is_dark=True)

    # Проверки
    assert stats_mobile_page.is_dark_theme(), "Тема не переключилась на тёмную"
    assert stats_mobile_page.theme_toggle.is_visible(), "Кнопка темы не видима"

    # Проверка видимости ключевых элементов в тёмной теме
    assert stats_mobile_page.refresh_btn.is_visible(), "Кнопка 'Обновить' скрыта в тёмной теме"
    assert stats_mobile_page.stats_cards.first.is_visible(), "Карточки статистики не отображаются"

    # Постусловие
    stats_mobile_page.set_theme(is_dark=False)


def test_012_theme_dark_to_light(stats_mobile_page: StatsPage):
    #TC-012: Переключение в светлую тему на странице Статистика (Темная -> Светлая)
    stats_mobile_page.open()

    # Предусловие: тёмная тема
    stats_mobile_page.set_theme(is_dark=True)
    assert stats_mobile_page.is_dark_theme(), "Не удалось подготовить тёмную тему"

    # Действие
    stats_mobile_page.set_theme(is_dark=False)

    # Проверки
    assert not stats_mobile_page.is_dark_theme(), "Тема не переключилась на светлую"

    # Проверка видимости элементов в светлой теме
    assert stats_mobile_page.refresh_btn.is_visible(), "Кнопка 'Обновить' скрыта в светлой теме"
    assert stats_mobile_page.stats_cards.first.is_visible(), "Карточки статистики не отображаются"

