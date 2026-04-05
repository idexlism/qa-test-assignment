# pages/stats_page.py
import re
from playwright.sync_api import Page, Locator, Error, expect


class StatsPage:
    def __init__(self, page: Page):
        self.page = page

        # локаторы
        self.refresh_btn: Locator = page.get_by_role("button", name="Обновить", exact=True)
        # Таймер
        self.timer_container: Locator = page.locator("//*[contains(@class, '_time_ir5wu_61']")

        # Карточки статистики (для проверки наличия данных)
        self.stats_cards: Locator = page.locator("//*[contains(@class, '_card_s99h9_8 _card_primary_s99h9_41']")

        # Кнопка Play
        self.play_pause_btn: Locator = page.locator(
            "//*[contains(@class, '_toggleButton_ir5wu_69')]"
        ).first

        # Текст статуса автообновления
        self.auto_update_status: Locator = page.locator(
            "//*[contains(text(), 'Автообновление выключено')]"
        ).first

        # локатор для смены темы
        self.theme_toggle: Locator = page.locator("//*[contains(@class, '_themeToggle_127us_1')]")

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

    def click_play_pause(self) -> None:
        # Нажимает кнопку Play/Pause
        self.play_pause_btn.click()
        self.page.wait_for_timeout(500)

    def is_timer_visible(self) -> bool:
        #Проверяет, виден ли таймер
        try:
            return self.timer_text.is_visible(timeout=2000)
        except Exception:
            return False

    def get_status_text(self) -> str:
        #Возвращает текст статуса автообновления
        try:
            return self.auto_update_status.inner_text().strip()
        except Exception:
            return ""

    def is_play_button(self) -> bool:
        # Проверяет, отображается ли кнопка как Play
        try:
            # Ищем иконку Play или aria-label
            return (
                    self.play_pause_btn.get_attribute("aria-label") == "Start auto-refresh" or
                    "play" in self.play_pause_btn.get_attribute("class", "").lower()
            )
        except Exception:
            # Фоллбэк: проверяем по тексту/иконке
            btn_content = self.play_pause_btn.inner_text().lower()
            return "play" in btn_content

    def is_pause_button(self) -> bool:
        # Проверяет, отображается ли кнопка как Pause
        try:
            return (
                    self.play_pause_btn.get_attribute("aria-label") == "Pause auto-refresh" or
                    "pause" in self.play_pause_btn.get_attribute("class", "").lower()
            )
        except Exception:
            btn_content = self.play_pause_btn.inner_text().lower()
            return "stop" in btn_content or "pause" in btn_content

    def set_theme(self, is_dark: bool) -> None:

        # Переключает тему, если текущее состояние не совпадает с целевым.
        # :param is_dark: True - включить темную, False - включить светлую

        # 1. Проверяем, нужна ли вообще смена темы
        current_is_dark = self.is_dark_theme()

        if current_is_dark != is_dark:
            # 2. Если состояние отличается — кликаем по кнопке
            self.theme_toggle.click()

            # Ждем, пока атрибут data-theme обновится на <html>
            if is_dark:
                expect(self.page.locator("html")).to_have_attribute("data-theme", "dark", timeout=5000)
            else:
                expect(self.page.locator("html")).to_have_attribute("data-theme", "light", timeout=5000)

    def is_dark_theme(self) -> bool:
        # Проверяет тему по атрибуту data-theme у тега <html>
        # Получаем значение атрибута data-theme
        theme_value = self.page.locator("html").get_attribute("data-theme")
        # Возвращаем True, если значение именно "dark"
        return theme_value == "dark"