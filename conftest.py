import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


def pytest_addoption(parser):
    """Thêm các tham số dòng lệnh tùy chọn cho pytest."""
    parser.addoption(
        "--browser",
        action="store",
        default="edge",
        help="Trình duyệt kiểm thử: 'edge' hoặc 'chrome' (mặc định: 'edge')"
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Chạy ở chế độ có giao diện (headed mode). Mặc định là headless."
    )


@pytest.fixture(scope="function")
def driver(request):
    """Fixture khởi tạo WebDriver trước mỗi test case và đóng sau khi hoàn tất."""
    browser_name = request.config.getoption("--browser").lower()
    is_headed = request.config.getoption("--headed")

    web_driver = None

    if browser_name == "chrome":
        options = ChromeOptions()
        if not is_headed:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        try:
            web_driver = webdriver.Chrome(options=options)
        except Exception as e:
            # Fallback nếu máy không có Chrome
            print(f"Không thể khởi tạo Chrome ({e}), chuyển sang Microsoft Edge...")
            edge_opts = EdgeOptions()
            if not is_headed:
                edge_opts.add_argument("--headless=new")
            edge_opts.add_argument("--no-sandbox")
            edge_opts.add_argument("--disable-dev-shm-usage")
            edge_opts.add_argument("--window-size=1920,1080")
            web_driver = webdriver.Edge(options=edge_opts)
    else:
        # Default Microsoft Edge (có sẵn trên mọi máy Windows)
        edge_opts = EdgeOptions()
        if not is_headed:
            edge_opts.add_argument("--headless=new")
        edge_opts.add_argument("--no-sandbox")
        edge_opts.add_argument("--disable-dev-shm-usage")
        edge_opts.add_argument("--window-size=1920,1080")
        web_driver = webdriver.Edge(options=edge_opts)

    web_driver.implicitly_wait(5)
    web_driver.maximize_window()

    yield web_driver

    # Chụp ảnh màn hình nếu test thất bại
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshots_dir = os.path.join(os.path.dirname(__file__), "reports", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        screenshot_path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
        web_driver.save_screenshot(screenshot_path)
        print(f"\n[Artifact] Đã lưu ảnh chụp lỗi tại: {screenshot_path}")

    web_driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook ghi nhận kết quả thực thi test case để xử lý capture screenshot."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
