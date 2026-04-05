# pages/stats_page.py
import re
from playwright.sync_api import Page, Locator, Error


class StatsPage:
    def __init__(self, page: Page):
        self.page = page

        # локаторы
        self.refresh_btn: Locator = page.get_by_role("button", name="Обновить", exact=True)
        # Таймер
        self.timer_container: Locator = page.locator("//*[contains(@class, '_time_ir5wu_61']")

        # Карточки статистики (для проверки наличия данных)
        self.stats_cards: Locator = page.locator("//*[contains(@class, '_card_s99h9_8 _card_primary_s99h9_41']")


    def open(self) -> None:
        #Открывает страницу статистики
        response = self.page.goto("/stats")
        self.page.wait_for_load_state("networkidle")

        # Проверяем HTTP статус
        if response and response.status != 200:
            raise AssertionError(
                f"Страница /stats вернула HTTP {response.status}\n"
                f"URL: {self.page.url}"
            )

    def click_refresh(self) -> None:
        #Нажимает кнопку 'Обновить'
        self.refresh_btn.click()
        # Небольшая задержка для обновления UI
        self.page.wait_for_timeout(500)

    def get_timer_text(self) -> str:
        #Возвращает текст таймера
        try:
            return self.timer_container.inner_text().strip()
        except Exception:
            return ""

    def wait_for_timer_change(self, old_text: str, timeout: int = 3000) -> bool:
        #Ждет, пока текст таймера изменится относительно old_text
        try:
            # Ждем, пока текст перестанет быть равным старому
            self.timer_container.wait_for(
                state="visible",
                timeout=timeout
            )
            new_text = self.get_timer_text()
            return new_text != old_text
        except Exception:
            return False