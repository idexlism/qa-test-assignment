# conftest.py
import pytest
from playwright.sync_api import Page
from pages.listing_page import ListingPage
from datetime import datetime


@pytest.fixture
def listing_page(page: Page) -> ListingPage:
   # Фикстура возвращает инициализированный Page Object
    return ListingPage(page)


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