from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object cho quy trình Thanh toán (Checkout Flow - Step 1, Step 2, Complete)."""

    # Step One (Your Information)
    TITLE = (By.CLASS_NAME, "title")
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    # Step Two (Overview)
    SUMMARY_SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    SUMMARY_TAX = (By.CLASS_NAME, "summary_tax_label")
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BTN = (By.ID, "finish")

    # Step Three (Complete)
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BTN = (By.ID, "back-to-products")

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        """Điền thông tin khách hàng tại bước 1."""
        if first_name:
            self.enter_text(self.FIRST_NAME_INPUT, first_name)
        if last_name:
            self.enter_text(self.LAST_NAME_INPUT, last_name)
        if postal_code:
            self.enter_text(self.POSTAL_CODE_INPUT, postal_code)
        self.click(self.CONTINUE_BTN)

    def get_summary_total_text(self) -> str:
        """Lấy chuỗi hiển thị tổng tiền tại trang Overview (ví dụ: 'Total: $32.39')."""
        return self.get_text(self.SUMMARY_TOTAL)

    def click_finish(self):
        """Nhấn nút Finish để xác nhận hoàn tất đơn hàng."""
        self.click(self.FINISH_BTN)

    def get_completion_header(self) -> str:
        """Lấy thông điệp hoàn tất đặt hàng (kỳ vọng: 'Thank you for your order!')."""
        return self.get_text(self.COMPLETE_HEADER)

    def is_order_complete_displayed(self) -> bool:
        """Kiểm tra màn hình hoàn tất đơn hàng và nút Back Home có hiển thị không."""
        return self.is_element_displayed(self.BACK_HOME_BTN)
