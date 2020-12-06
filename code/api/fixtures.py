import pytest

from api.client import APIClient


@pytest.fixture(scope='function')
def api_client():
    return APIClient()


@pytest.fixture(scope='session', autouse=True)
def admin_user():
    APIClient().register(**{
        'username': 'adminuser',
        'email': 'admin@mail.ru',
        'password': 'admin',
        'password2': 'admin'
    })
    # api_client.login('admin', 'admin')


@pytest.fixture(scope='function')
def login_as_admin(request):
    request.instance.api_client.login('adminuser', 'admin')
    yield
    request.instance.api_client.logout()
