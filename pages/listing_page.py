# pages/listing_page.py
import re
from playwright.sync_api import Page, Locator


class ListingPage:
    def __init__(self, page: Page):
        self.page = page

        # локаторы фильтра
        self.min_price_input: Locator = page.get_by_placeholder("От", exact=True)
        self.max_price_input: Locator = page.get_by_placeholder("До", exact=True)
        self.apply_btn: Locator = page.get_by_role("button", name="Применить", exact=True)

        # локаторы сортировки
        self.sort_by_dropdown: Locator = page.locator("//label[contains(text(), 'Сортировать по')]/following-sibling::select")
        self.order_dropdown: Locator = page.locator("//label[contains(text(), 'Порядок')]/following-sibling::select")

        # локаторы категорий
        self.category_dropdown: Locator = page.locator(
            "//label[contains(text(), 'Категория')]/following-sibling::select"
        )
        self.reset_filters_btn: Locator = page.get_by_role("button", name="Сбросить", exact=True)

        # Локатор для карточки объявления (для извлечения категории)
        self.ad_cards: Locator = page.locator("//*[contains(@class, '_card__price_15fhn_241')]")

    def open(self) -> None:
        #Открывает страницу списка
        self.page.goto("/")
        self.page.wait_for_load_state("networkidle")

    def set_price_range(self, min_val: int, max_val: int) -> None:
        #Устанавливает диапазон цен и применяет фильтр
        self.min_price_input.clear()
        self.min_price_input.fill(str(min_val))
        self.max_price_input.clear()
        self.max_price_input.fill(str(max_val))
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)  # даём время на перерисовку

    def set_sorting(self, sort_by: str = "Цена", order: str = "По возрастанию") -> None:
        """
        Args:
            sort_by: "Цена", "Дате создания", "Приоритету"
            order: "По возрастанию", "По убыванию"
        """
        # Открываем dropdown "Сортировать по"
        self.sort_by_dropdown.click()

        # 1. Выбираем критерий сортировки
        if sort_by == "Цена":
            self.sort_by_dropdown.select_option(value="price")
        elif sort_by == "Дате создания":
            self.sort_by_dropdown.select_option(value="createdAt")
        elif sort_by == "Приоритету":
            self.sort_by_dropdown.select_option(value="priority")

        # 2. Выбираем порядок
        if order == "По возрастанию":
            self.order_dropdown.select_option(value="asc")
        else:
            self.order_dropdown.select_option(value="desc")

        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

        print(f"Сортировка установлена")

    def select_category(self, category: str) -> None:
        """
        Выбирает категорию из выпадающего списка
        Args:
            category: Название категории (например, "Животные", "Услуги", "Транспорт")
        """
        # Открываем dropdown и выбираем опцию по тексту
        self.category_dropdown.select_option(label=category)

        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000)

    def reset_filters(self) -> None:
        """Сбрасывает все фильтры"""
        if self.reset_filters_btn.is_visible(timeout=2000):
            self.reset_filters_btn.click()
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(1000)

    def get_all_prices(self) -> list[int]:
        # Ждём появления хотя бы одной цены
        price_locator = self.page.locator(
            "xpath=//*[@class='_card__price_15fhn_241']"
        ).filter(visible=True)

        # Ждём появления хотя бы одной цены
        try:
            price_locator.first.wait_for(state="visible", timeout=5000)
        except Exception:
            return []

        count = price_locator.count()

        prices = []
        for i in range(count):
            try:
                element = price_locator.nth(i)
                raw_text = element.inner_text(timeout=2000)
                clean_price = re.sub(r'[^\d]', '', raw_text)
                if clean_price:
                    prices.append(int(clean_price))
            except Exception as e:
                print(f"Не удалось прочитать цену #{i}: {e}")
                continue

        return prices

    def get_ad_categories(self) -> list[str]:
        """
        Собирает категории всех отображенных объявлений

        Returns:
            Список категорий (например: ["Транспорт", "Транспорт", "Работа"])
        """
        # Ищем карточки объявлений
        cards = self.page.locator("//*[contains(@class, '_card__content_15fhn_90')]").filter(visible=True)

        try:
            cards.first.wait_for(state="visible", timeout=5000)
        except Exception:
            return []

        self.page.wait_for_timeout(1000)
        count = cards.count()

        categories = []
        for i in range(count):
            try:
                card = cards.nth(i)
                # Ищем элемент с категорией внутри карточки
                # Обычно это badge или tag с категорией
                category_element = card.locator(
                    "//*[contains(@class, '_card__category_15fhn_259')"
                ).first

                if category_element.is_visible(timeout=2000):
                    category_text = category_element.inner_text().strip()
                    if category_text:
                        categories.append(category_text)
            except Exception:
                # Если категорию не нашли, пропускаем
                continue

        return categories

    def get_ads_count(self) -> int:
        """Возвращает количество отображенных объявлений"""
        cards = self.page.locator("//*[contains(@class, '_card_')]").filter(visible=True)
        try:
            cards.first.wait_for(state="visible", timeout=3000)
            return cards.count()
        except Exception:
            return 0
