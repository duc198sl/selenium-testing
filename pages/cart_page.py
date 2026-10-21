from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object cho trang Giỏ hàng (Shopping Cart)."""

    TITLE = (By.CLASS_NAME, "title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    REMOVE_BACKPACK_BTN = (By.ID, "remove-sauce-labs-backpack")
    CHECKOUT_BTN = (By.ID, "checkout")
    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def get_page_title(self) -> str:
        """Lấy tiêu đề trang giỏ hàng (kỳ vọng: 'Your Cart')."""
        return self.get_text(self.TITLE)

    def get_cart_item_names(self) -> list[str]:
        """Lấy danh sách tên tất cả các sản phẩm có trong giỏ hàng."""
        if not self.is_element_displayed(self.ITEM_NAMES, custom_timeout=3):
            return []
        elements = self.find_elements(self.ITEM_NAMES)
        return [el.text.strip() for el in elements]

    def remove_backpack(self):
        """Xóa sản phẩm Sauce Labs Backpack khỏi giỏ hàng."""
        self.click(self.REMOVE_BACKPACK_BTN)

    def get_cart_badge_count(self) -> int:
        """Lấy số lượng hiển thị trên badge icon giỏ hàng."""
        if self.is_element_displayed(self.CART_BADGE, custom_timeout=2):
            text = self.get_text(self.CART_BADGE)
            return int(text) if text.isdigit() else 0
        return 0

    def click_checkout(self):
        """Nhấn nút Checkout để chuyển sang bước thanh toán thông tin giao hàng."""
        self.click(self.CHECKOUT_BTN)
