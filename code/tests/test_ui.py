import json
import allure
import pytest
import requests
from selenium.webdriver import ActionChains

from tests.base import BaseUICase


@pytest.mark.usefixtures("snap_on_fail")
@pytest.mark.UI
class TestLoginPage(BaseUICase):
    def test_register_positive(self, get_user):
        user = get_user
        with allure.step('Registering valid user'):
            self.login_page.register(**user, should_logout=False)
            assert 'http://myapp:5050/welcome/' == self.login_page.driver.current_url
        with allure.step('Checking if user has been added to db'):
            query_user = self.builder.get_by_username(user.get('username'))
            assert query_user is not None
            assert query_user.username == user['username'] and query_user.email == user['email']
            assert query_user.access == 1

    def test_register_negative_username_used(self, get_user):
        user = get_user
        bad_user = user.copy()
        bad_user['email'] = 'fineemail@mail.ru'
        with allure.step('Registering valid user'):
            self.login_page.register(**user)
        with allure.step('Registering user with used username'):
            self.login_page.register(**bad_user)
            assert 'http://myapp:5050/reg' == self.login_page.driver.current_url
            assert self.login_page.check_if_exists(self.login_page.locators.USER_EXIST_MSG)
        with allure.step('Checking if user has not been added to db'):
            query_user = self.builder.get_by_email(bad_user.get('email'))
            assert query_user is None

    def test_register_negative_email_used(self, get_user):
        user = get_user
        bad_user = user.copy()
        bad_user['username'] = 'fineuser'
        with allure.step('Registering valid user'):
            self.login_page.register(**user)
        with allure.step('Registering user with used email'):
            self.login_page.register(**bad_user)
            assert 'http://myapp:5050/reg' == self.login_page.driver.current_url
            assert self.login_page.check_if_exists(self.login_page.locators.EMAIL_EXIST_MSG)
        with allure.step('Checking if user has not been added to db'):
            query_user = self.builder.get_by_username(bad_user.get('username'))
            assert query_user is None

    def test_register_negative_username_email_used(self, get_user):
        user = get_user
        with allure.step('Registering valid user'):
            self.login_page.register(**user)
        with allure.step('Registering thi user again'):
            self.login_page.register(**user)
            assert 'http://myapp:5050/reg' == self.login_page.driver.current_url
            assert self.login_page.check_if_exists(self.login_page.locators.USER_EXIST_MSG)

    def test_register_negative_username_length(self, get_user):
        user = get_user
        user['username'] = "a"
        with allure.step('Registering user with short username'):
            self.login_page.register(**user)
            assert 'http://myapp:5050/reg' == self.login_page.driver.current_url
            assert self.login_page.check_if_exists(self.login_page.locators.USERNAME_LENGTH_MSG)
        with allure.step('Checking if user has not been added to db'):
            query_user = self.builder.get_by_username(user.get('username'))
            assert query_user is None

    def test_register_negative_email_invalid(self, get_user):
        user = get_user
        user['email'] = user['email'].split('@')[0]
        with allure.step('Registering user with invalid email'):
            self.login_page.register(**user)
            assert 'http://myapp:5050/reg' == self.login_page.driver.current_url
            assert self.login_page.check_if_exists(self.login_page.locators.EMAIL_INVALID_MSG)
        with allure.step('Checking if user has not been added to db'):
            query_user = self.builder.get_by_email(user.get('email'))
            assert query_user is None

    def test_register_negative_terms(self, get_user):
        user = get_user
        with allure.step('Registering user without accepting terms'):
            self.login_page.register(**user, terms=False)
            assert 'http://myapp:5050/reg' == self.login_page.driver.current_url
        with allure.step('Checking if user has not been added to db'):
            query_user = self.builder.get_by_email(user.get('email'))
            assert query_user is None

    def test_login_negative(self, get_user):
        user = get_user
        with allure.step('Login with wrong data'):
            self.login_page.login(user['username'], user['password'])
            assert 'http://myapp:5050/login' == self.login_page.driver.current_url
            assert self.login_page.check_if_exists(self.login_page.locators.LOGIN_INVALID_MSG)
        with allure.step('Checking if user has not been added to db'):
            query_user = self.builder.get_by_username(user.get('username'))
            assert query_user is None

    def test_login_positive(self, get_user):
        user = get_user
        self.login_page.register(**user)
        with allure.step('Valid login'):
            self.login_page.login(user['username'], user['password'])
            assert 'http://myapp:5050/welcome/' == self.login_page.driver.current_url
        with allure.step('Checking if user is active'):
            query_user = self.builder.get_by_username(user.get('username'))
            assert query_user is not None
            assert query_user.active == 1


@pytest.mark.UI
@pytest.mark.usefixtures("snap_on_fail")
class TestMainPage(BaseUICase):
    def test_login_vkid_should_be(self, get_user):
        user = get_user
        vk_id = '4321'
        with allure.step('Registering user an sending request to vk_api'):
            self.login_page.register(**user)
            requests.post(f'http://0.0.0.0:5052/vk_id/{user["username"]}', data=json.dumps({'vk_id': vk_id}))
        with allure.step('Login as this user'):
            self.login_page.login(user['username'], user['password'])
            assert self.login_page.check_if_exists(self.login_page.locators.VKID_LOCATOR, vk_id)

    def test_login_vkid_should_not_be(self, get_user):
        user = get_user
        with allure.step('Registering user without sending request to vk_api'):
            self.login_page.register(**user)
        with allure.step('Login as this user'):
            self.login_page.login(user['username'], user['password'])
            assert not self.login_page.check_if_exists(self.login_page.locators.VKID_LOCATOR, '')

    def test_logout_active(self, get_user):
        user = get_user
        with allure.step('Registering user'):
            self.login_page.register(**user)
        with allure.step('Login user'):
            self.login_page.login(user['username'], user['password'])
        with allure.step('Logout user and check if user is not active'):
            self.login_page.logout()
            query_user = self.builder.get_by_username(user.get('username'))
            assert query_user.active == 0

    def test_click_logo(self, get_user):
        user = get_user
        self.login_page.register(**user, should_logout=False)
        with allure.step('Clicking logo image'):
            self.login_page.click(self.login_page.locators.LOGO_BUTTON)
        with allure.step('Check if url is valid'):
            assert 'http://myapp:5050/welcome/' == self.login_page.driver.current_url
            self.login_page.logout()

    def test_click_home(self, get_user):
        user = get_user
        self.login_page.register(**user, should_logout=False)
        with allure.step('Clicking home button'):
            self.login_page.click(self.login_page.locators.HOME_BUTTON)
        with allure.step('Check if url is valid'):
            assert 'http://myapp:5050/welcome/' == self.login_page.driver.current_url
            self.login_page.logout()

    def test_click_python(self, get_user):
        user = get_user
        self.login_page.register(**user, should_logout=False)
        with allure.step('Clicking python button'):
            self.login_page.click(self.login_page.locators.PYTHON_BUTTON)
        with allure.step('Check if url is valid'):
            assert 'https://www.python.org/' == self.login_page.driver.current_url
        with allure.step('Going back'):
            self.login_page.driver.back()
            self.login_page.logout()

    def test_click_python_history(self, get_user):
        user = get_user
        self.login_page.register(**user, should_logout=False)
        action = ActionChains(self.login_page.driver)
        with allure.step('Moving python button'):
            action.move_to_element(self.login_page.find(self.login_page.locators.PYTHON_BUTTON)).perform()
        with allure.step('Clicking python history'):
            self.login_page.click(self.login_page.locators.PYTHON_HISTORY)
        with allure.step('Check if url is valid'):
            assert 'https://en.wikipedia.org/wiki/History_of_Python' == self.login_page.driver.current_url
        with allure.step('Going back'):
            self.login_page.driver.back()
            self.login_page.logout()

    def test_click_python_flask(self, get_user):
        user = get_user
        self.login_page.register(**user, should_logout=False)
        action = ActionChains(self.login_page.driver)
        with allure.step('Moving python button'):
            action.move_to_element(self.login_page.find(self.login_page.locators.PYTHON_BUTTON)).perform()
        with allure.step('Clicking python flask'):
            self.login_page.click(self.login_page.locators.PYTHON_FLASK)
        window_before = self.login_page.driver.window_handles[0]
        window_after = self.login_page.driver.window_handles[1]
        with allure.step('Switching to next tab and check its url'):
            self.login_page.driver.switch_to.window(window_after)
            assert 'https://flask.palletsprojects.com/en/1.1.x/#' == self.login_page.driver.current_url
        with allure.step('Switching to prev tab'):
            self.login_page.driver.switch_to.window(window_before)
            self.login_page.logout(timeout=10)

    def test_click_linux_centos(self, get_user):
        user = get_user
        self.login_page.register(**user, should_logout=False)
        action = ActionChains(self.login_page.driver)
        with allure.step('Moving linux button'):
            action.move_to_element(self.login_page.find(self.login_page.locators.LINUX_BUTTON)).perform()
        with allure.step('Clicking linux centos'):
            self.login_page.click(self.login_page.locators.LINUX_CENTOS)
        window_before = self.login_page.driver.window_handles[0]
        window_after = self.login_page.driver.window_handles[1]
        with allure.step('Switching to next tab and check its url'):
            self.login_page.driver.switch_to.window(window_after)
            assert 'https://www.centos.org/download/' == self.login_page.driver.current_url
        with allure.step('Switching to prev tab'):
            self.login_page.driver.switch_to.window(window_before)
            self.login_page.logout()

    def test_click_network_ws_news(self, get_user):
        user = get_user
        self.login_page.register(**user, should_logout=False)
        action = ActionChains(self.login_page.driver)
        with allure.step('Moving network button'):
            action.move_to_element(self.login_page.find(self.login_page.locators.NETWORK_BUTTON)).perform()
        with allure.step('Clicking network -> wireshark news'):
            self.login_page.click(self.login_page.locators.NETWORK_WS_NEWS)
        window_before = self.login_page.driver.window_handles[0]
        window_after = self.login_page.driver.window_handles[1]
        with allure.step('Switching to next tab and check its url'):
            self.login_page.driver.switch_to.window(window_after)
            assert 'https://www.wireshark.org/news/' == self.login_page.driver.current_url
        with allure.step('Switching to prev tab'):
            self.login_page.driver.switch_to.window(window_before)
            self.login_page.logout()

    def test_click_network_ws_download(self, get_user):
        user = get_user
        self.login_page.register(**user, should_logout=False)
        action = ActionChains(self.login_page.driver)
        with allure.step('Moving network button'):
            action.move_to_element(self.login_page.find(self.login_page.locators.NETWORK_BUTTON)).perform()
        with allure.step('Clicking network -> wireshark download'):
            self.login_page.click(self.login_page.locators.NETWORK_WS_DOWNLOAD)
        window_before = self.login_page.driver.window_handles[0]
        window_after = self.login_page.driver.window_handles[1]
        with allure.step('Switching to next tab and check its url'):
            self.login_page.driver.switch_to.window(window_after)
            assert 'https://www.wireshark.org/#download' == self.login_page.driver.current_url
        with allure.step('Switching to prev tab'):
            self.login_page.driver.switch_to.window(window_before)
            self.login_page.logout()

    def test_click_network_tcpdump_examples(self, get_user):
        user = get_user
        self.login_page.register(**user, should_logout=False)
        action = ActionChains(self.login_page.driver)
        with allure.step('Moving network button'):
            action.move_to_element(self.login_page.find(self.login_page.locators.NETWORK_BUTTON)).perform()
        with allure.step('Clicking network -> tcpdump examples'):
            self.login_page.click(self.login_page.locators.NETWORK_TCPDUMP_EXAMPLES)
        window_before = self.login_page.driver.window_handles[0]
        window_after = self.login_page.driver.window_handles[1]
        with allure.step('Switching to next tab and check its url'):
            self.login_page.driver.switch_to.window(window_after)
            assert 'https://hackertarget.com/tcpdump-examples/' == self.login_page.driver.current_url
        with allure.step('Switching to prev tab'):
            self.login_page.driver.switch_to.window(window_before)
            self.login_page.logout()

    def test_click_content_1(self, get_user):
        user = get_user
        self.login_page.register(**user, should_logout=False)
        with allure.step('Clicking first content image'):
            self.login_page.click(self.login_page.locators.CONTENT_IMAGE_1)
        window_before = self.login_page.driver.window_handles[0]
        window_after = self.login_page.driver.window_handles[1]
        with allure.step('Switching to next tab and check its url'):
            self.login_page.driver.switch_to.window(window_after)
            assert 'https://en.wikipedia.org/wiki/API' == self.login_page.driver.current_url
        with allure.step('Switching to prev tab'):
            self.login_page.driver.switch_to.window(window_before)
            self.login_page.logout()

    def test_click_content_2(self, get_user):
        user = get_user
        self.login_page.register(**user, should_logout=False)
        with allure.step('Clicking second content image'):
            self.login_page.click(self.login_page.locators.CONTENT_IMAGE_2)
        window_before = self.login_page.driver.window_handles[0]
        window_after = self.login_page.driver.window_handles[1]
        with allure.step('Switching to next tab and check its page source'):
            self.login_page.driver.switch_to.window(window_after)
            assert 'future of the internet' in self.login_page.driver.page_source
        with allure.step('Switching to prev tab'):
            self.login_page.driver.switch_to.window(window_before)
            self.login_page.logout()

    def test_click_content_3(self, get_user):
        user = get_user
        self.login_page.register(**user, should_logout=False)
        with allure.step('Clicking third content image'):
            self.login_page.click(self.login_page.locators.CONTENT_IMAGE_3)
        window_before = self.login_page.driver.window_handles[0]
        window_after = self.login_page.driver.window_handles[1]
        with allure.step('Switching to next tab and check its url'):
            self.login_page.driver.switch_to.window(window_after)
            assert 'https://ru.wikipedia.org/wiki/SMTP' == self.login_page.driver.current_url
        with allure.step('Switching to prev tab'):
            self.login_page.driver.switch_to.window(window_before)
            self.login_page.logout()
