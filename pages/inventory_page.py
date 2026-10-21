from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Page Object cho trang Danh sách sản phẩm (Inventory / Catalog)."""

    TITLE = (By.CLASS_NAME, "title")
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")

    ADD_BACKPACK_BTN = (By.ID, "add-to-cart-sauce-labs-backpack")
    REMOVE_BACKPACK_BTN = (By.ID, "remove-sauce-labs-backpack")
    ADD_BIKE_LIGHT_BTN = (By.ID, "add-to-cart-sauce-labs-bike-light")
    REMOVE_BIKE_LIGHT_BTN = (By.ID, "remove-sauce-labs-bike-light")

    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    BURGER_MENU_BTN = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def get_page_title(self) -> str:
        """Lấy tiêu đề trang sản phẩm (kỳ vọng: 'Products')."""
        return self.get_text(self.TITLE)

    def sort_products(self, sort_value: str):
        """
        Sắp xếp danh sách sản phẩm theo giá trị:
        - 'az': Tên A đến Z
        - 'za': Tên Z đến A
        - 'lohi': Giá từ thấp đến cao
        - 'hilo': Giá từ cao đến thấp
        """
        element = self.find_element(self.SORT_SELECT)
        select = Select(element)
        select.select_by_value(sort_value)

    def get_product_prices(self) -> list[float]:
        """Lấy toàn bộ danh sách đơn giá hiển thị trên trang dưới dạng float."""
        price_elements = self.find_elements(self.ITEM_PRICES)
        prices = []
        for el in price_elements:
            text = el.text.strip().replace("$", "")
            prices.append(float(text))
        return prices

    def get_product_names(self) -> list[str]:
        """Lấy toàn bộ danh sách tên sản phẩm hiển thị trên trang."""
        elements = self.find_elements(self.ITEM_NAMES)
        return [el.text.strip() for el in elements]

    def add_backpack_to_cart(self):
        """Thêm sản phẩm Sauce Labs Backpack vào giỏ."""
        self.click(self.ADD_BACKPACK_BTN)

    def remove_backpack_from_cart(self):
        """Xóa sản phẩm Sauce Labs Backpack khỏi giỏ ngay tại trang inventory."""
        self.click(self.REMOVE_BACKPACK_BTN)

    def add_bike_light_to_cart(self):
        """Thêm sản phẩm Sauce Labs Bike Light vào giỏ."""
        self.click(self.ADD_BIKE_LIGHT_BTN)

    def get_cart_badge_count(self) -> int:
        """Lấy số lượng hiển thị trên badge icon giỏ hàng (trả về 0 nếu chưa có sản phẩm)."""
        if self.is_element_displayed(self.CART_BADGE, custom_timeout=2):
            text = self.get_text(self.CART_BADGE)
            return int(text) if text.isdigit() else 0
        return 0

    def go_to_cart(self):
        """Nhấn icon giỏ hàng để chuyển sang trang Cart."""
        self.click(self.CART_LINK)

    def logout(self):
        """Thực hiện đăng xuất thông qua menu điều hướng bên trái."""
        self.click(self.BURGER_MENU_BTN)
        self.click(self.LOGOUT_LINK)
