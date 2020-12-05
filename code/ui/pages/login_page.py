from ui.locators import basic_locators
from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    locators = basic_locators.LoginPageLocators()

    def register(self, username, email, password, password2, terms=True, should_logout=True):
        self.click(self.locators.REG_BUTTON)
        self.fill_field(self.locators.USERNAME_FIELD, username)
        self.fill_field(self.locators.EMAIL_REG_FIELD, email)
        self.fill_field(self.locators.PASSWORD_FIELD, password)
        self.fill_field(self.locators.PASSWORD2_REG_FIELD, password2)
        if terms:
            self.click(self.locators.TERMS_CHECKBOX)
        self.click(self.locators.CONFIRM_REG_BUTTON)
        if should_logout and self.check_if_exists(self.locators.LOGOUT_BUTTON):
            self.click(self.locators.LOGOUT_BUTTON)

    def login(self, username, password):
        self.fill_field(self.locators.USERNAME_FIELD, username)
        self.fill_field(self.locators.PASSWORD_FIELD, password)
        self.click(self.locators.LOGIN_BUTTON)

    def logout(self, timeout=None):
        self.click(self.locators.LOGOUT_BUTTON, timeout)
