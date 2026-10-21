import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestInventorySorting:
    """Bộ kiểm thử cho chức năng Sắp xếp & Hiển thị danh mục sản phẩm."""

    @pytest.fixture(autouse=True)
    def setup_logged_in_state(self, driver):
        """Tiền điều kiện: Đăng nhập thành công vào hệ thống trước mỗi test case."""
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

    def test_tc04_sort_price_low_to_high(self, driver):
        """
        TC04: Sắp xếp sản phẩm theo giá tăng dần (Price: low to high).
        Kỳ vọng: Danh sách giá sản phẩm hiển thị theo thứ tự tăng dần.
        """
        inventory_page = InventoryPage(driver)

        # Chọn kiểu sắp xếp 'lohi'
        inventory_page.sort_products("lohi")

        prices = inventory_page.get_product_prices()
        assert len(prices) > 0, "Không tìm thấy sản phẩm nào trên trang!"

        # Xác thực danh sách giá đã được sắp xếp tăng dần
        expected_sorted_prices = sorted(prices)
        assert prices == expected_sorted_prices, (
            f"Danh sách giá thực tế: {prices}\nDanh sách kỳ vọng: {expected_sorted_prices}"
        )

        # Chụp ảnh màn hình hoàn thành test case
        inventory_page.save_screenshot("tc04_sort_price_low_to_high.png")

    def test_tc05_sort_price_high_to_low(self, driver):
        """
        TC05: Sắp xếp sản phẩm theo giá giảm dần (Price: high to low).
        Kỳ vọng: Danh sách giá sản phẩm hiển thị theo thứ tự giảm dần.
        """
        inventory_page = InventoryPage(driver)

        # Chọn kiểu sắp xếp 'hilo'
        inventory_page.sort_products("hilo")

        prices = inventory_page.get_product_prices()
        assert len(prices) > 0, "Không tìm thấy sản phẩm nào trên trang!"

        expected_sorted_prices = sorted(prices, reverse=True)
        assert prices == expected_sorted_prices, (
            f"Danh sách giá thực tế: {prices}\nDanh sách kỳ vọng: {expected_sorted_prices}"
        )

        # Chụp ảnh màn hình hoàn thành test case
        inventory_page.save_screenshot("tc05_sort_price_high_to_low.png")
