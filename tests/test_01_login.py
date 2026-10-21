import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestLogin:
    """Bộ kiểm thử cho chức năng Đăng nhập."""

    def test_tc01_valid_login(self, driver):
        """
        TC01: Đăng nhập thành công với tài khoản hợp lệ.
        Kỳ vọng: Chuyển hướng đến /inventory.html và hiển thị tiêu đề 'Products'.
        """
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        # 1. Mở trang đăng nhập
        login_page.open()

        # 2. Nhập thông tin tài khoản hợp lệ
        login_page.login("standard_user", "secret_sauce")

        # 3. Xác thực kết quả
        assert "inventory.html" in driver.current_url, f"URL thực tế: {driver.current_url}"
        assert inventory_page.get_page_title() == "Products"

        # 4. Chụp ảnh màn hình hoàn thành test case
        inventory_page.save_screenshot("tc01_valid_login.png")

    def test_tc02_locked_out_user(self, driver):
        """
        TC02: Đăng nhập với tài khoản bị khóa trong hệ thống.
        Kỳ vọng: Hiển thị thông báo tài khoản đã bị khóa.
        """
        login_page = LoginPage(driver)
        login_page.open()

        # Nhập thông tin tài khoản bị khóa
        login_page.login("locked_out_user", "secret_sauce")

        # Xác thực thông báo lỗi
        error_msg = login_page.get_error_message()
        assert "Sorry, this user has been locked out" in error_msg, f"Thông báo lỗi thực tế: {error_msg}"

        # Chụp ảnh màn hình hoàn thành test case
        login_page.save_screenshot("tc02_locked_out_user.png")

    def test_tc03_invalid_password(self, driver):
        """
        TC03: Đăng nhập với sai mật khẩu.
        Kỳ vọng: Hiển thị thông báo thông tin đăng nhập không khớp.
        """
        login_page = LoginPage(driver)
        login_page.open()

        login_page.login("standard_user", "wrong_password_123")

        error_msg = login_page.get_error_message()
        assert "Username and password do not match" in error_msg, f"Thông báo lỗi thực tế: {error_msg}"

        # Chụp ảnh màn hình hoàn thành test case
        login_page.save_screenshot("tc03_invalid_password.png")
