import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from atlant_bot.settings import GAZOVIK_PASSWORD, GAZOVIK_USERNAME


def get_driver(headless: bool = True) -> WebDriver:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--headless")

    driver = webdriver.Chrome(
        options=options,
        service=ChromeService(),
    )
    return driver


class Gazovik:
    def __init__(
        self,
        username: str = GAZOVIK_USERNAME,
        password: str = GAZOVIK_PASSWORD,
    ):
        self.driver = get_driver()
        self.username = username
        self.password = password
        self._login()

    def _login(self, login_url: str = "https://gazovik.ng-club.com/ua/auth/login"):
        self.driver.get(login_url)
        if self.driver.current_url != login_url:
            print("Already logged in")
            return

        form: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "yw0"))
        )
        self.driver.find_element(By.ID, "MFormLogin_login").send_keys(self.username)
        self.driver.find_element(By.ID, "MFormLogin_password").send_keys(self.password)
        form.submit()

    def get_balance(self):
        table: WebElement = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "container_12"))
        )
        el = table.find_element(
            By.CSS_SELECTOR,
            "div:nth-child(8) > div > div > div",
        )
        if not el:
            print("Couldn't find an element with balance")
            return
        balance = float(el.text)
        return balance
