import pytest

from ui.pages.login_page import LoginPage


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver=driver)