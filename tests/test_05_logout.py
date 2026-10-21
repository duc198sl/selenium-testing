import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestLogout:
    """Bộ kiểm thử cho chức năng Đăng xuất và Bảo mật phiên đăng nhập."""

    def test_tc08_logout_and_session_invalidation(self, driver):
        """
        TC08: Đăng xuất khỏi hệ thống và kiểm tra bảo mật phiên.
        Các bước:
        1. Đăng nhập với tài khoản hợp lệ.
        2. Mở menu và nhấn Logout.
        3. Xác thực đã chuyển hướng về trang chủ Login.
        4. Cố gắng truy cập trực tiếp URL /inventory.html.
        5. Xác thực hệ thống chặn truy cập và hiển thị thông báo yêu cầu đăng nhập.
        """
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)

        # 1. Đăng nhập
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        assert "inventory.html" in driver.current_url

        # 2. Đăng xuất qua menu
        inventory_page.logout()

        # 3. Xác thực quay về trang chủ đăng nhập
        assert login_page.is_login_page_displayed()
        assert driver.current_url.rstrip("/") == "https://www.saucedemo.com"

        # 4. Thử truy cập trái phép trang inventory khi đã logout
        driver.get("https://www.saucedemo.com/inventory.html")

        # 5. Xác thực bị chặn và có thông báo lỗi bảo mật
        assert login_page.is_login_page_displayed()
        error_msg = login_page.get_error_message()
        assert "You can only access '/inventory.html' when you are logged in" in error_msg

        # Chụp ảnh màn hình hoàn thành test case
        login_page.save_screenshot("tc08_logout_and_session_invalidation.png")
