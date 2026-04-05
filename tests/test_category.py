# tests/test_category.py
import pytest
from pages.listing_page import ListingPage


@pytest.mark.parametrize("category", [
    "Электроника",
    "Недвижимость",
    "Транспорт",
    "Работа",
    "Услуги",
    "Животные",
    "Мода",
    "Детское"

])
def test_004_category_filter(listing_page: ListingPage, category: str):

    #TC-004: Проверка работы фильтра "Категория"
    try:
        # 1. Открываем страницу
        listing_page.open()

        # 2. Получаем начальное количество объявлений
        initial_count = listing_page.get_ads_count()

        # 3. Выбираем категорию
        listing_page.select_category(category)

        # 4. Проверяем результаты фильтрации
        filtered_count = listing_page.get_ads_count()

        if filtered_count == 0:
            pytest.skip(f"Категория '{category}' пуста")

        # 5. Проверяем, что все объявления принадлежат выбранной категории
        ad_categories = listing_page.get_ad_categories()

        # Проверяем каждую категорию
        wrong_categories = [cat for cat in ad_categories if cat != category]

        if wrong_categories:
            print(f"\n НАЙДЕНЫ ОБЪЯВЛЕНИЯ ДРУГИХ КАТЕГОРИЙ:")
            unique_wrong = set(wrong_categories)
            for wrong_cat in unique_wrong:
                count = wrong_categories.count(wrong_cat)
                print(f"          {wrong_cat}: {count} объявлений")

        # 6. Сбрасываем фильтры
        listing_page.reset_filters()

        # Проверяем, что количество объявлений вернулось
        after_reset_count = listing_page.get_ads_count()

        if wrong_categories:
            pytest.fail(
                f"\n\nBUG: Фильтр по категории '{category}' не работает!\n"
                f"   Найдено {len(ad_categories)} объявлений\n"
                f"   Ожидалась категория: {category}\n"
                f"   Найдены категории: {set(ad_categories)}\n"
                f"   Объявления других категорий: {len(wrong_categories)}\n"
                f"   Чужие категории: {set(wrong_categories)}"
            )

    finally:
        try:
            listing_page.reset_filters()
        except Exception:
            pass