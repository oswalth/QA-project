from selenium.webdriver.common.by import By


class BasePageLocators:
    LOGIN_BUTTON = (By.XPATH, '//input[@value="Login"]')
    REG_BUTTON = (By.XPATH, '//a[@href="/reg"]')

