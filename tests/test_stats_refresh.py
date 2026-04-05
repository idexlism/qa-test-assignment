# tests/test_stats_refresh.py
import pytest
from pages.stats_page import StatsPage


def test_006_manual_refresh_button(stats_page: StatsPage):

    #TC-006: Проверка кнопки ручного обновления "Обновить"

    # 1. Открываем страницу статистики
    stats_page.open()

    # 2. Проверяем, что кнопка "Обновить" существует и активна
    assert stats_page.refresh_btn.is_visible(), "Кнопка 'Обновить' не видима"
    assert stats_page.refresh_btn.is_enabled(), "Кнопка 'Обновить' не активна"

    # 3. Запоминаем состояние таймера ДО нажатия
    timer_before = stats_page.get_timer_text()

    # Если таймер не найден — пропускаем проверку таймера
    if not timer_before:
        pytest.skip("Таймер не найден на странице")

    # 4. Нажимаем кнопку "Обновить"
    stats_page.click_refresh()

    # 5. Проверяем, что таймер сбросился (текст изменился)
    is_timer_changed = stats_page.wait_for_timer_change(timer_before)

    assert is_timer_changed, (
        f"Таймер не сбросился после нажатия 'Обновить'!\n"
        f"Было: {timer_before}\n"
        f"Стало: {stats_page.get_timer_text()}"
    )