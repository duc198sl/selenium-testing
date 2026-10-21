import os
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """Lớp BasePage chứa các phương thức tương tác cơ bản và xử lý Explicit Wait."""

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def open_url(self, url: str):
        """Mở địa chỉ URL."""
        self.driver.get(url)

    def find_element(self, locator: tuple):
        """Chờ và tìm một phần tử hiển thị trên trang."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator: tuple):
        """Chờ và tìm danh sách tất cả các phần tử phù hợp."""
        self.wait.until(EC.presence_of_all_elements_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator: tuple):
        """Chờ phần tử có thể bấm được và thực hiện click."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def enter_text(self, locator: tuple, text: str, clear_first: bool = True):
        """Nhập nội dung văn bản vào ô input."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """Lấy nội dung text hiển thị của phần tử."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text.strip()

    def is_element_displayed(self, locator: tuple, custom_timeout: int = 5) -> bool:
        """Kiểm tra xem phần tử có hiển thị hay không trong thời gian cho trước."""
        try:
            WebDriverWait(self.driver, custom_timeout).until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_url_contains(self, partial_url: str, custom_timeout: int = 10) -> bool:
        """Chờ URL hiện tại chứa đoạn ký tự chỉ định."""
        try:
            return WebDriverWait(self.driver, custom_timeout).until(EC.url_contains(partial_url))
        except TimeoutException:
            return False

    def get_current_url(self) -> str:
        """Lấy URL hiện tại của trình duyệt."""
        return self.driver.current_url

    def get_title(self) -> str:
        """Lấy tiêu đề trang."""
        return self.driver.title

    def save_screenshot(self, filename: str) -> str:
        """Chụp ảnh màn hình lưu vào thư mục screenshots/ của dự án để đưa vào báo cáo."""
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        screenshots_dir = os.path.join(root_dir, "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        filepath = os.path.join(screenshots_dir, filename)
        self.driver.save_screenshot(filepath)
        return filepath
