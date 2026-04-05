# conftest.py
import pytest
from playwright.sync_api import Page, Browser
from pages.listing_page import ListingPage
from pages.stats_page import StatsPage
from datetime import datetime


@pytest.fixture
def listing_page(page: Page) -> ListingPage:
   # Фикстура возвращает инициализированный Page Object
    return ListingPage(page)

@pytest.fixture
def stats_page(page: Page) -> StatsPage:  # ← Добавь эту фикстуру
    #Фикстура для страницы статистики
    return StatsPage(page)

@pytest.fixture
def mobile_page(browser: Browser, base_url) -> Page:
    #Фикстура для эмуляции Samsung Galaxy S25
    context = browser.new_context(
        base_url=base_url,
        user_agent="Mozilla/5.0 (Linux; Android 14; Samsung Galaxy S25) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        viewport={"width": 360, "height": 780},
        device_scale_factor=3.0,
        is_mobile=True,
        has_touch=True
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def test_report():
    #Фикстура для сбора информации о тесте
    report_data = {
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "steps": []
    }
    yield report_data
    print(f"\n Завершено в {datetime.now().strftime('%H:%M:%S')}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    #Показывает результат каждого теста
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        if report.passed:
            print(f"\n✅ РЕЗУЛЬТАТ: ТЕСТ ПРОЙДЕН")
        elif report.failed:
            print(f"\n❌ РЕЗУЛЬТАТ: ТЕСТ УПАЛ")