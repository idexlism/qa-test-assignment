# tests/test_stats_timer_pause.py
import pytest
from pages.stats_page import StatsPage


def test_008_stop_timer(stats_page: StatsPage):

    #TC-008: Проверка кнопки остановки таймера

    # 1. Открываем страницу
    stats_page.open()

    # 2. Подготовка: Убеждаемся, что таймер запущен
    # Если кнопка Play — кликаем, чтобы запустить
    if stats_page.is_play_button():
        stats_page.click_play_pause()
        stats_page.page.wait_for_timeout(1000)  # Ждем инициализации

    # Проверяем, что мы находимся в состоянии "Пауза" (таймер работает)
    assert stats_page.is_pause_button(), "Не удалось запустить таймер для теста"
    assert stats_page.is_timer_visible(), "Таймер не виден при запущенном автообновлении"

    # Запоминаем время ДО остановки
    timer_before_stop = stats_page.get_timer_text()

    # 3. Действие: Нажимаем Pause
    stats_page.click_play_pause()

    # 4. Проверяем результат
    # Кнопка должна вернуться в состояние Play
    assert stats_page.is_play_button(), (
        f"Кнопка не вернулась в состояние Play после нажатия Pause.\n"
        f"Текущее состояние: {'Play' if stats_page.is_play_button() else 'Pause'}"
    )

    # Проверяем остановку таймера
    stats_page.page.wait_for_timeout(1500)  # Даем время тикнуть, если он не остановился
    timer_after_stop = stats_page.get_timer_text()

    # Если таймер остановился, время должно быть таким же (или таймер исчез)
    if stats_page.is_timer_visible():
        assert timer_before_stop == timer_after_stop, (
            f"Таймер продолжает работать после нажатия Pause!\n"
            f"Время до: {timer_before_stop}\n"
            f"Время после: {timer_after_stop}"
        )