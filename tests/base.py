import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.login_page import LoginPage


class BaseUICase:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config
        self.login_page: LoginPage = request.getfixturevalue('login_page')

        # self.base_page: BasePage = request.getfixturevalue('base_page')
        # self.main_page: MainPage = request.getfixturevalue('main_page')


class BaseAPICase:
    pass
    # @pytest.fixture(scope="function", autouse=True)
    # def setup(self, driver, config):
    #     self.driver = driver
    #     self.config = config