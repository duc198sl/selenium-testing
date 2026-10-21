import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


class TestCartManagement:
    """Bộ kiểm thử cho chức năng Quản lý giỏ hàng (Thêm & Xóa sản phẩm)."""

    @pytest.fixture(autouse=True)
    def setup_logged_in_state(self, driver):
        """Tiền điều kiện: Đăng nhập trước khi thao tác giỏ hàng."""
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

    def test_tc06_add_and_remove_products_cart(self, driver):
        """
        TC06: Thêm nhiều sản phẩm vào giỏ hàng và kiểm tra xóa sản phẩm.
        Các bước:
        1. Thêm 'Sauce Labs Backpack' và 'Sauce Labs Bike Light' vào giỏ.
        2. Kiểm tra badge giỏ hàng hiển thị số '2'.
        3. Chuyển vào trang giỏ hàng, xác nhận 2 sản phẩm có mặt.
        4. Xóa 'Sauce Labs Backpack'.
        5. Kiểm tra badge giỏ hàng giảm xuống '1' và chỉ còn 'Sauce Labs Bike Light'.
        """
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)

        # 1. Thêm 2 sản phẩm
        inventory_page.add_backpack_to_cart()
        inventory_page.add_bike_light_to_cart()

        # 2. Kiểm tra badge
        assert inventory_page.get_cart_badge_count() == 2, "Badge giỏ hàng không hiển thị số 2!"

        # 3. Chuyển sang giỏ hàng
        inventory_page.go_to_cart()
        assert "cart.html" in driver.current_url

        item_names = cart_page.get_cart_item_names()
        assert "Sauce Labs Backpack" in item_names
        assert "Sauce Labs Bike Light" in item_names

        # 4. Xóa 'Sauce Labs Backpack'
        cart_page.remove_backpack()

        # 5. Kiểm tra badge và danh sách còn lại
        remaining_names = cart_page.get_cart_item_names()
        assert "Sauce Labs Backpack" not in remaining_names
        assert "Sauce Labs Bike Light" in remaining_names
        assert cart_page.get_cart_badge_count() == 1

        # Chụp ảnh màn hình hoàn thành test case
        cart_page.save_screenshot("tc06_cart_management.png")
