from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException


class Driver:
    def __init__(self, headless: bool = True) -> None:
        self.headless = headless
        self._driver = None

    def __call__(self) -> WebDriver:
        return self._current()

    def _init_driver(self) -> WebDriver:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-dev-shm-usage")
        if self.headless:
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")

        driver = webdriver.Chrome(
            options=options,
            service=ChromeService(),
        )
        return driver

    def _is_session_active(self) -> bool:
        if self._driver is None:
            return False
        try:
            # A simple command to check if the session is still active
            self._driver.title
            return True
        except (NoSuchWindowException, WebDriverException):
            return False

    def _current(self):
        if self._driver is None or not self._is_session_active():
            print("Initializing or reinitializing the WebDriver")
            self._driver = self._init_driver()
        return self._driver
