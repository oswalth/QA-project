import allure
import pytest
import requests

from tests.base import BaseAPICase


@pytest.mark.API
class TestRawRequests(BaseAPICase):
    def test_registration_positive(self, get_user):
        with allure.step(f'Trying valid registration request'):
            response = self.api_client.register(**get_user)
        with allure.step(f'Checking if response has status 200'):
            assert response.status_code == 200
        with allure.step(f'Checking if user was created'):
            query_user = self.builder.get_by_username(get_user.get('username'))
            assert query_user is not None
        with allure.step(f'Checking if user active after successful registration'):
            assert query_user.active == 1
            assert query_user.start_active_time is not None

    def test_registration_negative_username_used(self, get_user):
        bad_user = get_user.copy()
        bad_user['email'] = "usernameused@mail.ru"
        with allure.step(f'Creating user to duplicate username'):
            self.api_client.register(**get_user)
        with allure.step(f'Trying registration request, username used'):
            response = self.api_client.register(**bad_user)
        with allure.step(f'Checking if response has status 400'):
            assert response.status_code == 400
        with allure.step(f'Checking if user was not created'):
            query_user = self.builder.get_by_email(bad_user.get('email'))
            assert query_user is None

    def test_registration_negative_email_used(self, get_user):
        bad_user = get_user.copy()
        bad_user['username'] = "emailused"
        with allure.step(f'Creating user to duplicate email'):
            self.api_client.register(**get_user)
        with allure.step(f'Trying registration request, email used'):
            response = self.api_client.register(**bad_user)
        with allure.step(f'Checking if response has status 400'):
            assert response.status_code == 400
        with allure.step(f'Checking if user was not created'):
            query_user = self.builder.get_by_username(bad_user.get('username'))
            assert query_user is None

    def test_registration_negative_email_username_used(self, get_user):
        with allure.step(f'Creating user to duplicate'):
            self.api_client.register(**get_user)
        with allure.step(f'Trying registration request, email used'):
            response = self.api_client.register(**get_user)
        with allure.step(f'Checking if response has status 400'):
            assert response.status_code == 400

    def test_registration_invalid_email(self, get_user):
        bad_user = get_user.copy()
        bad_user['email'] = bad_user['email'].split('@')[0]
        with allure.step(f'Trying registration request, email has no @ and domen'):
            response = self.api_client.register(**bad_user)
        with allure.step(f'Checking if response has status 400'):
            assert response.status_code == 400
        with allure.step(f'Checking if user was not created'):
            query_user = self.builder.get_by_email(bad_user.get('email'))
            assert query_user is None

    def test_registration_diff_passwords(self, get_user):
        bad_user = get_user.copy()
        bad_user['password2'] += 's'
        with allure.step(f'Trying registration request, passwords do not match'):
            response = self.api_client.register(**bad_user)
        with allure.step(f'Checking if response has status 400'):
            assert response.status_code == 400
        with allure.step(f'Checking if user was not created'):
            query_user = self.builder.get_by_email(bad_user.get('email'))
            assert query_user is None

    def test_registration_term_not_y(self, get_user):
        with allure.step(f'Trying registration request, term="n"'):
            response = self.api_client.register(**get_user, term='n')
        with allure.step(f'Checking if response has status 400'):
            assert response.status_code == 400
        with allure.step(f'Checking if user was not created'):
            query_user = self.builder.get_by_email(get_user.get('email'))
            assert query_user is None

    def test_registration_term_not_sent(self, get_user):
        with allure.step(f'Trying registration request, without term'):
            response = self.api_client.register(**get_user, term='delete')
        with allure.step(f'Checking if response has status 400'):
            assert response.status_code == 400
        with allure.step(f'Checking if user was not created'):
            query_user = self.builder.get_by_email(get_user.get('email'))
            assert query_user is None

    def test_login_positive(self, get_user):
        with allure.step(f'Valid registration request'):
            self.api_client.register(**get_user)
        with allure.step(f'Trying to login'):
            response = self.api_client.login(get_user['username'], get_user['password'])
        with allure.step(f'Checking if status code is 200'):
            assert response.status_code == 200
        with allure.step(f'Checking if user is active'):
            query_user = self.builder.get_by_username(get_user.get('username'))
            assert query_user.active == 1
            assert query_user.start_active_time is not None

    def test_login_negative(self, get_user):
        with allure.step(f'Valid registration request'):
            self.api_client.register(**get_user)
        with allure.step(f'Trying to login'):
            response = self.api_client.login(get_user['username'], get_user['password'] + 's')
        with allure.step(f'Checking if status code is 401'):
            assert response.status_code == 401
        with allure.step(f'Checking if user is not active'):
            query_user = self.builder.get_by_username(get_user.get('username'))
            assert query_user.active == 0

    def test_logout(self, get_user):
        with allure.step(f'Valid registration request'):
            self.api_client.register(**get_user)
        with allure.step(f'Trying to login'):
            self.api_client.login(get_user['username'], get_user['password'])
        with allure.step(f'Trying to logout'):
            response = self.api_client.logout()
        with allure.step(f'Checking if status code is 200'):
            assert response.status_code == 200
        with allure.step(f'Checking if user is not active'):
            query_user = self.builder.get_by_username(get_user.get('username'))
            assert query_user.active == 0

    def test_status(self):
        with allure.step(f'Checking server status'):
            response = self.api_client.status()
        with allure.step(f'Checking if status code is 200'):
            assert response.status_code == 200
        with allure.step(f'Checking if message status is ok'):
            assert response.json().get('status') == 'ok'


@pytest.mark.usefixtures('login_as_admin')
@pytest.mark.API
class TestAPI(BaseAPICase):
    def test_adduser_positive(self, get_user_add):
        with allure.step(f'Trying valid add_user request'):
            response = self.api_client.add_user(**get_user_add)
        with allure.step(f'Checking if response has status 200'):
            assert response.status_code == 200
        with allure.step(f'Checking if user was created'):
            query_user = self.builder.get_by_username(get_user_add.get('username'))
            assert query_user is not None
        with allure.step(f'Checking if user active after successful registration'):
            assert query_user.active == 1
            assert query_user.start_active_time is not None

    def test_adduser_negative_username_used(self, get_user_add):
        bad_user = get_user_add.copy()
        bad_user['email'] = "userusedapi@mail.ru"
        with allure.step(f'Creating user to duplicate username'):
            self.api_client.add_user(**get_user_add)
        with allure.step(f'Trying add_user request, username used'):
            response = self.api_client.add_user(**bad_user)
        with allure.step(f'Checking if response has status 304'):
            assert response.status_code == 304
        with allure.step(f'Checking if user was not created'):
            query_user = self.builder.get_by_email(bad_user.get('email'))
            assert query_user is None

    def test_adduser_negative_email_used(self, get_user_add):
        bad_user = get_user_add.copy()
        bad_user['username'] = "emailusedapi"
        with allure.step(f'Creating user to duplicate email'):
            self.api_client.add_user(**get_user_add)
        with allure.step(f'Trying add_user request, email used'):
            response = self.api_client.add_user(**bad_user)
        with allure.step(f'Checking if response has status 304'):
            assert response.status_code == 304
        with allure.step(f'Checking if user was not created'):
            query_user = self.builder.get_by_username(bad_user.get('username'))
            assert query_user is None

    def test_adduser_negative_email_username_used(self, get_user_add):
        with allure.step(f'Creating user to duplicate'):
            self.api_client.add_user(**get_user_add)
        with allure.step(f'Trying add_user request, email used'):
            response = self.api_client.add_user(**get_user_add)
        with allure.step(f'Checking if response has status 304'):
            assert response.status_code == 304

    def test_adduser_invalid_email(self, get_user_add):
        bad_user = get_user_add.copy()
        bad_user['email'] = bad_user['email'].split('@')[0]
        with allure.step(f'Trying add_user request, email has no @ and domen'):
            response = self.api_client.add_user(**bad_user)
        with allure.step(f'Checking if response has status 400'):
            assert response.status_code == 400
        with allure.step(f'Checking if user was not created'):
            query_user = self.builder.get_by_email(bad_user.get('email'))
            assert query_user is None

    def test_adduser_username_length(self, get_user_add):
        bad_user = get_user_add.copy()
        bad_user['username'] = bad_user['username'][:2]
        with allure.step(f'Trying add_user request, username too short'):
            response = self.api_client.add_user(**bad_user)
        with allure.step(f'Checking if response has status 400'):
            assert response.status_code == 400
        with allure.step(f'Checking if user was not created'):
            query_user = self.builder.get_by_username(bad_user.get('username'))
            assert query_user is None

    def test_deluser_positive(self, get_user_add):
        with allure.step(f'Adding user via api'):
            self.api_client.add_user(**get_user_add)
        with allure.step(f'Trying delete user'):
            response = self.api_client.delete_user(get_user_add['username'])
        with allure.step(f'Checking if response has status 204'):
            assert response.status_code == 204
        with allure.step(f'Checking if user was deleted'):
            query_user = self.builder.get_by_username(get_user_add.get('username'))
            assert query_user is None

    def test_deluser_notexist(self):
        with allure.step(f'Trying delete non exist user'):
            response = self.api_client.delete_user('totallyrandomusername')
        with allure.step(f'Checking if response has status 404'):
            assert response.status_code == 404

    def test_block_positive(self, get_user_add):
        with allure.step(f'Adding user via api'):
            self.api_client.add_user(**get_user_add)
        with allure.step(f'Blocking user via api'):
            self.api_client.block_user(get_user_add['username'])
        with allure.step(f'Checking if user is blocked'):
            query_user = self.builder.get_by_username(get_user_add.get('username'))
            assert query_user.access == 0
        with allure.step(f'Trying to login as blocked user'):
            response = self.api_client.login(get_user_add['username'], get_user_add['password'])
            assert response.status_code == 401

    def test_accept_positive(self, get_user_add):
        with allure.step(f'Adding user via api'):
            self.api_client.add_user(**get_user_add)
        with allure.step(f'Blocking user via api'):
            self.api_client.block_user(get_user_add['username'])
        with allure.step(f'Accepting user via api'):
            self.api_client.accept_user(get_user_add['username'])
        with allure.step(f'Checking if user is accepted'):
            query_user = self.builder.get_by_username(get_user_add.get('username'))
            assert query_user.access == 1
        with allure.step(f'Trying to login as blocked user'):
            response = self.api_client.login(get_user_add['username'], get_user_add['password'])
            assert response.status_code == 200

    def test_block_blocked_user(self, get_user_add):
        with allure.step(f'Adding user via api'):
            self.api_client.add_user(**get_user_add)
        with allure.step(f'Blocking user via api'):
            self.api_client.block_user(get_user_add['username'])
        with allure.step(f'Blocking blocked user via api'):
            response = self.api_client.block_user(get_user_add['username'])
            assert response.status_code == 304
        with allure.step(f'Checking if user is still blocked'):
            query_user = self.builder.get_by_username(get_user_add.get('username'))
            assert query_user.access == 0

    def test_accept_accepted_user(self, get_user_add):
        with allure.step(f'Adding user via api'):
            self.api_client.add_user(**get_user_add)
        with allure.step(f'Accepting user via api'):
            self.api_client.accept_user(get_user_add['username'])
        with allure.step(f'Accepting accepted user via api'):
            response = self.api_client.accept_user(get_user_add['username'])
            assert response.status_code == 304
        with allure.step(f'Checking if user is still blocked'):
            query_user = self.builder.get_by_username(get_user_add.get('username'))
            assert query_user.access == 1



