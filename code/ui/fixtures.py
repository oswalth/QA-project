import allure
import pytest
from allure_commons.types import AttachmentType
import hashlib

from ui.pages.login_page import LoginPage


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture(scope='function')
def get_user(request):
    hash_ = hashlib.sha1(request.node.name.encode("utf-8")).hexdigest()
    username = ''.join([char for char in hash_ if char.isalpha()][:8])
    return {
        "username": username,
        "email": username + "@mail.ru",
        "password": "2525",
        "password2": "2525"
    }


@pytest.fixture(scope='function')
def snap_on_fail(request, driver):
    yield
    if request.node.session.testsfailed:
        allure.attach(name=request.node.name,
                      body=driver.get_screenshot_as_png(),
                      attachment_type=AttachmentType.PNG)
