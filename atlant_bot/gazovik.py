from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from atlant_bot.driver import Driver
from atlant_bot.settings import LOGIN_URL


def authenticate(func):
    def wrapper(self, *args, **kwargs):
        if not self.username or not self.password:
            raise Exception("Credentials are not provided")

        self.driver().get(LOGIN_URL)
        if self.driver().current_url != LOGIN_URL:
            print("Already logged in")
            return func(self, *args, **kwargs)

        form: WebElement = WebDriverWait(self.driver(), 20).until(
            EC.element_to_be_clickable((By.ID, "yw0"))
        )
        self.driver().find_element(By.ID, "MFormLogin_login").send_keys(self.username)
        self.driver().find_element(By.ID, "MFormLogin_password").send_keys(
            self.password
        )
        form.submit()

        return func(self, *args, **kwargs)

    return wrapper


class Gazovik:
    def __init__(
        self,
        driver: Driver,
        username: str,
        password: str,
    ):
        self.driver = driver
        self.username = username
        self.password = password

    @authenticate
    def get_balance(self):
        table: WebElement = WebDriverWait(self.driver(), 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "container_12"))
        )
        print(table)
        balance = float(
            table.find_element(
                By.CSS_SELECTOR,
                "div:nth-child(8) > div > div > div",
            ).text
        )
        return balance
