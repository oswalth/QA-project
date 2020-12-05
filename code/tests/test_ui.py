import json
import allure
import pytest
import requests
from selenium.webdriver import ActionChains

from tests.base import BaseUICase



class TestLoginPage(BaseUICase):
    def test_register_positive(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user, should_logout=False)
            query_user = self.builder.get_by_username(user.get('username'))

            assert 'http://myapp:5050/welcome/' == self.login_page.driver.current_url
            assert user is not None
            assert query_user.username == user['username'] and query_user.email == user['email']
            assert query_user.access == 1

    def test_register_negative_username_used(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            bad_user = user.copy()
            bad_user['email'] = 'fineemail@mail.ru'

            self.login_page.register(**user)
            self.login_page.register(**bad_user)

            assert 'http://myapp:5050/reg' == self.login_page.driver.current_url
            assert self.login_page.check_if_exists(self.login_page.locators.USER_EXIST_MSG)
            query_user = self.builder.get_by_email(bad_user.get('email'))
            assert query_user is None

    def test_register_negative_email_used(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            bad_user = user.copy()
            bad_user['username'] = 'fineuser'

            self.login_page.register(**user)
            self.login_page.register(**bad_user)

            assert 'http://myapp:5050/reg' == self.login_page.driver.current_url
            assert self.login_page.check_if_exists(self.login_page.locators.EMAIL_EXIST_MSG)
            query_user = self.builder.get_by_username(user.get('username'))
            assert query_user is None

    def test_register_negative_username_length(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            user['username'] = "a"
            self.login_page.register(**user)
            assert 'http://myapp:5050/reg' == self.login_page.driver.current_url
            assert self.login_page.check_if_exists(self.login_page.locators.USERNAME_LENGTH_MSG)
            query_user = self.builder.get_by_username(user.get('username'))
            assert query_user is None

    # def test_register_negative_email_length(self, my_name, get_user):
    #     with allure.step(f'Starting {my_name}'):
    #         user = get_user
    #         user['email'] = 'a@mail.ru'
    #         self.login_page.register(**user)
    #         assert 'http://myapp:5050/reg' == self.login_page.driver.current_url
    #         assert self.login_page.check_if_exists(self.login_page.locators.EMAIL_LENGTH_MSG)
    #         query_user = self.builder.get_by_email(user.get('email'))
    #         assert query_user is None

    def test_register_negative_email_invalid(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            user['email'] = user['email'].split('@')[0]
            self.login_page.register(**user)
            assert 'http://myapp:5050/reg' == self.login_page.driver.current_url
            assert self.login_page.check_if_exists(self.login_page.locators.EMAIL_INVALID_MSG)
            query_user = self.builder.get_by_email(user.get('email'))
            assert query_user is None

    def test_register_negative_terms(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user, terms=False)
            assert 'http://myapp:5050/reg' == self.login_page.driver.current_url
            query_user = self.builder.get_by_email(user.get('email'))
            assert query_user is None

    def test_login_negative(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.login(user['username'], user['password'])
            assert 'http://myapp:5050/login' == self.login_page.driver.current_url
            query_user = self.builder.get_by_username(user.get('username'))
            assert self.login_page.check_if_exists(self.login_page.locators.LOGIN_INVALID_MSG)
            assert query_user is None


    def test_login_positive(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user)
            self.login_page.login(user['username'], user['password'])
            assert 'http://myapp:5050/welcome/' == self.login_page.driver.current_url
            query_user = self.builder.get_by_username(user.get('username'))
            assert query_user is not None
            assert query_user.active == 1


@pytest.mark.usefixtures("snap_on_fail")
class TestMainPage(BaseUICase):
    def test_login_vkid_should_be(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            vk_id = '4321'
            self.login_page.register(**user)
            requests.post(f'http://0.0.0.0:5052/vk_id/{user["username"]}', data=json.dumps({'vk_id': vk_id}))
            self.login_page.login(user['username'], user['password'])
            assert self.login_page.check_if_exists(self.login_page.locators.VKID_LOCATOR, vk_id)

    def test_login_vkid_should_not_be(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user)
            self.login_page.login(user['username'], user['password'])
            assert not self.login_page.check_if_exists(self.login_page.locators.VKID_LOCATOR, '')

    def test_login_active(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user)
            self.login_page.login(user['username'], user['password'])
            query_user = self.builder.get_by_username(user.get('username'))
            assert query_user.active == 1

    def test_logout_active(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user)
            self.login_page.login(user['username'], user['password'])
            self.login_page.logout()
            query_user = self.builder.get_by_username(user.get('username'))
            assert query_user.active == 0

    def test_click_logo(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user, should_logout=False)
            self.login_page.click(self.login_page.locators.LOGO_BUTTON)
            assert 'http://myapp:5050/welcome/' == self.login_page.driver.current_url
            self.login_page.logout()

    def test_click_home(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user, should_logout=False)
            self.login_page.click(self.login_page.locators.HOME_BUTTON)
            assert 'http://myapp:5050/welcome/' == self.login_page.driver.current_url
            self.login_page.logout()

    def test_click_python(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user, should_logout=False)
            self.login_page.click(self.login_page.locators.PYTHON_BUTTON)
            assert 'https://www.python.org/' == self.login_page.driver.current_url
            self.login_page.driver.back()
            self.login_page.logout()

    def test_click_python_history(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user, should_logout=False)
            action = ActionChains(self.login_page.driver)
            action.move_to_element(self.login_page.find(self.login_page.locators.PYTHON_BUTTON)).perform()
            self.login_page.click(self.login_page.locators.PYTHON_HISTORY)
            assert 'https://en.wikipedia.org/wiki/History_of_Python' == self.login_page.driver.current_url
            self.login_page.driver.back()
            self.login_page.logout()

    @pytest.mark.usefixtures("snap_on_fail")
    def test_click_python_flask(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user, should_logout=False)
            action = ActionChains(self.login_page.driver)
            action.move_to_element(self.login_page.find(self.login_page.locators.PYTHON_BUTTON)).perform()
            self.login_page.click(self.login_page.locators.PYTHON_FLASK)
            # go to next tab
            window_before = self.login_page.driver.window_handles[0]
            window_after = self.login_page.driver.window_handles[1]
            self.login_page.driver.switch_to_window(window_after)
            assert 'https://flask.palletsprojects.com/en/1.1.x/#' == self.login_page.driver.current_url
            self.login_page.driver.switch_to_window(window_before)
            self.login_page.logout(timeout=10)

    def test_click_linux_centos(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user, should_logout=False)
            action = ActionChains(self.login_page.driver)
            action.move_to_element(self.login_page.find(self.login_page.locators.LINUX_BUTTON)).perform()
            self.login_page.click(self.login_page.locators.LINUX_CENTOS)
            # go to next tab
            window_before = self.login_page.driver.window_handles[0]
            window_after = self.login_page.driver.window_handles[1]
            self.login_page.driver.switch_to_window(window_after)
            assert 'https://www.centos.org/download/' == self.login_page.driver.current_url
            self.login_page.driver.switch_to_window(window_before)
            self.login_page.logout()

    def test_click_network_ws_news(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user, should_logout=False)
            action = ActionChains(self.login_page.driver)
            action.move_to_element(self.login_page.find(self.login_page.locators.NETWORK_BUTTON)).perform()
            self.login_page.click(self.login_page.locators.NETWORK_WS_NEWS)
            # go to next tab
            window_before = self.login_page.driver.window_handles[0]
            window_after = self.login_page.driver.window_handles[1]
            self.login_page.driver.switch_to_window(window_after)
            assert 'https://www.wireshark.org/news/' == self.login_page.driver.current_url
            self.login_page.driver.switch_to_window(window_before)
            self.login_page.logout()

    def test_click_network_ws_download(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user, should_logout=False)
            action = ActionChains(self.login_page.driver)
            action.move_to_element(self.login_page.find(self.login_page.locators.NETWORK_BUTTON)).perform()
            self.login_page.click(self.login_page.locators.NETWORK_WS_DOWNLOAD)
            # go to next tab
            window_before = self.login_page.driver.window_handles[0]
            window_after = self.login_page.driver.window_handles[1]
            self.login_page.driver.switch_to_window(window_after)
            assert 'https://www.wireshark.org/#download' == self.login_page.driver.current_url
            self.login_page.driver.switch_to_window(window_before)
            self.login_page.logout()

    def test_click_network_tcpdump_examples(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user, should_logout=False)
            action = ActionChains(self.login_page.driver)
            action.move_to_element(self.login_page.find(self.login_page.locators.NETWORK_BUTTON)).perform()
            self.login_page.click(self.login_page.locators.NETWORK_TCPDUMP_EXAMPLES)
            # go to next tab
            window_before = self.login_page.driver.window_handles[0]
            window_after = self.login_page.driver.window_handles[1]
            self.login_page.driver.switch_to_window(window_after)
            assert 'https://hackertarget.com/tcpdump-examples/' == self.login_page.driver.current_url
            self.login_page.driver.switch_to_window(window_before)
            self.login_page.logout()

    def test_click_content_1(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user, should_logout=False)

            self.login_page.click(self.login_page.locators.CONTENT_IMAGE_1)
            # go to next tab
            window_before = self.login_page.driver.window_handles[0]
            window_after = self.login_page.driver.window_handles[1]
            self.login_page.driver.switch_to_window(window_after)
            assert 'https://en.wikipedia.org/wiki/API' == self.login_page.driver.current_url
            self.login_page.driver.switch_to_window(window_before)
            self.login_page.logout()

    def test_click_content_2(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user, should_logout=False)

            self.login_page.click(self.login_page.locators.CONTENT_IMAGE_2)
            # go to next tab
            window_before = self.login_page.driver.window_handles[0]
            window_after = self.login_page.driver.window_handles[1]
            self.login_page.driver.switch_to_window(window_after)
            assert 'future of the internet' in self.login_page.driver.page_source
            self.login_page.driver.switch_to_window(window_before)
            self.login_page.logout()

    def test_click_content_3(self, my_name, get_user):
        with allure.step(f'Starting {my_name}'):
            user = get_user
            self.login_page.register(**user, should_logout=False)

            self.login_page.click(self.login_page.locators.CONTENT_IMAGE_3)
            # go to next tab
            window_before = self.login_page.driver.window_handles[0]
            window_after = self.login_page.driver.window_handles[1]
            self.login_page.driver.switch_to_window(window_after)
            assert 'https://ru.wikipedia.org/wiki/SMTP' == self.login_page.driver.current_url
            self.login_page.driver.switch_to_window(window_before)
            self.login_page.logout()
