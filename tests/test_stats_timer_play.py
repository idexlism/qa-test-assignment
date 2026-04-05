# tests/test_stats_timer_play.py
import pytest
from pages.stats_page import StatsPage


def test_007_start_timer(stats_page: StatsPage):

    #TC-007: Проверка кнопки запуска таймера

    # 1. Открываем страницу
    stats_page.open()

    # 2. Проверяем начальное состояние (должен быть Play)
    assert stats_page.play_pause_btn.is_visible(), "Кнопка управления не видима"
    assert stats_page.is_play_button(), "Ожидалась кнопка Play, но найдена Pause"

    # Запоминаем состояние таймера ДО
    timer_before = stats_page.get_timer_text()

    # 3. Действие: Нажимаем Play
    stats_page.click_play_pause()

    # 4. Проверяем результат
    # Кнопка должна смениться на Pause
    assert stats_page.is_pause_button(), (
        f"Кнопка не сменилась на Pause после нажатия.\n"
        f"Текущее состояние: {'Pause' if stats_page.is_pause_button() else 'Play'}"
    )

    # Таймер должен появиться или обновиться
    assert stats_page.is_timer_visible(), "Таймер не появился после запуска"

    # Если таймер был до этого, он должен сброситься (время измениться)
    timer_after = stats_page.get_timer_text()
    if timer_before:
        assert timer_after != timer_before, (
            f"Таймер не сбросился\n"
            f"Было: {timer_before}\n"
            f"Стало: {timer_after}"
        )