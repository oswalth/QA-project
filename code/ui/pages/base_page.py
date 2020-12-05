from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from ui.locators import basic_locators

RETRY_COUNT = 3


class BasePage(object):

    def __init__(self, driver):
        self.driver = driver

    def check_if_exists(self, locator, value=False):
        if value:
            by, locator = locator
            locator = (by, locator.format(value))
        try:
            self.find(locator, timeout=5)
            return True
        except TimeoutException:
            return False

    def find(self, locator, timeout=None) -> WebElement:
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout=None):

        for i in range(RETRY_COUNT):
            try:
                element = self.find(locator, timeout)
                element.click()
                return

            except StaleElementReferenceException:
                if i < RETRY_COUNT - 1:
                    pass
        raise

    def upload_file(self, locator, file_path, submit=None):
        upload_field = self.find(locator)
        upload_field.send_keys(file_path)
        if submit:
            self.click(locator=submit, timeout=4)

    def fill_field(self, locator, field_value):
        field = self.find(locator=locator)
        field.clear()
        field.send_keys(field_value)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)
