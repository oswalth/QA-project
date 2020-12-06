import pytest
from _pytest.fixtures import FixtureRequest

from api.client import APIClient
from orm.builder import OrmBuilder
from orm.client import OrmConnector
from ui.pages.login_page import LoginPage


class BaseUICase:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver, config, request: FixtureRequest, orm_connector: OrmConnector):
        self.driver = driver
        self.config = config
        self.mysql: OrmConnector = orm_connector
        self.builder: OrmBuilder = OrmBuilder(mysql=self.mysql)
        self.login_page: LoginPage = request.getfixturevalue('login_page')


class BaseAPICase:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, request: FixtureRequest, orm_connector: OrmConnector):
        self.api_client : APIClient = request.getfixturevalue('api_client')
        self.mysql: OrmConnector = orm_connector
        self.builder: OrmBuilder = OrmBuilder(mysql=self.mysql)
