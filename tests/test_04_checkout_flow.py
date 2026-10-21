import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestCheckoutFlow:
    """Bộ kiểm thử cho chức năng Đặt hàng và Thanh toán (E2E Checkout)."""

    @pytest.fixture(autouse=True)
    def setup_logged_in_state(self, driver):
        """Tiền điều kiện: Đăng nhập trước khi thực hiện quy trình mua sắm."""
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

    def test_tc07_complete_checkout_e2e(self, driver):
        """
        TC07: Toàn bộ luồng đặt hàng từ thêm giỏ hàng đến thanh toán thành công (E2E).
        Các bước:
        1. Thêm sản phẩm vào giỏ hàng.
        2. Chuyển vào giỏ hàng và nhấn 'Checkout'.
        3. Điền thông tin giao hàng (Tên, Họ, Mã bưu chính) và bấm 'Continue'.
        4. Kiểm tra trang tổng quan (Overview) hiển thị tổng tiền hợp lệ.
        5. Nhấn 'Finish' để xác nhận đặt hàng.
        6. Xác thực màn hình cảm ơn hiển thị: 'Thank you for your order!'.
        """
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)

        # 1. Thêm sản phẩm và đi tới giỏ hàng
        inventory_page.add_backpack_to_cart()
        inventory_page.go_to_cart()

        # 2. Bắt đầu checkout
        cart_page.click_checkout()
        assert "checkout-step-one.html" in driver.current_url

        # 3. Điền thông tin khách hàng
        checkout_page.fill_checkout_info("Nguyen", "Van A", "70000")
        assert "checkout-step-two.html" in driver.current_url

        # 4. Kiểm tra trang Overview
        total_text = checkout_page.get_summary_total_text()
        assert "Total: $" in total_text, f"Tổng tiền hiển thị không đúng định dạng: {total_text}"

        # 5. Hoàn tất đơn hàng
        checkout_page.click_finish()
        assert "checkout-complete.html" in driver.current_url

        # 6. Xác nhận thông điệp hoàn tất thành công
        completion_msg = checkout_page.get_completion_header()
        assert "Thank you for your order!" in completion_msg, f"Thông báo thực tế: {completion_msg}"
        assert checkout_page.is_order_complete_displayed()

        # Chụp ảnh màn hình hoàn thành test case
        checkout_page.save_screenshot("tc07_complete_checkout_e2e.png")
