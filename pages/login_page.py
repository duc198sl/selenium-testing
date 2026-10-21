from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object cho trang Đăng nhập (SauceDemo Login)."""

    URL = "https://www.saucedemo.com/"

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def open(self):
        """Mở trang chủ đăng nhập."""
        self.open_url(self.URL)

    def login(self, username: str, password: str):
        """Thực hiện quy trình đăng nhập đầy đủ."""
        if username:
            self.enter_text(self.USERNAME_INPUT, username)
        if password:
            self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """Lấy thông báo lỗi khi đăng nhập không thành công."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_login_page_displayed(self) -> bool:
        """Kiểm tra form đăng nhập có hiển thị không."""
        return self.is_element_displayed(self.LOGIN_BUTTON)
