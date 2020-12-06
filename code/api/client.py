import json

import requests
from urllib.parse import urljoin


class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = f"http://0.0.0.0:5050"

    def _request(self, method, url, data=None, headers=None, dumps_=False):
        if dumps_:
            data = json.dumps(data)

        return self.session.request(method=method, url=url, headers=headers, data=data)

    def status(self):
        return self._request(method='GET', url=urljoin(self.base_url, 'status'))

    def login(self, username, password):
        data = {
            'username': username,
            'password': password,
            'submit': 'Login'
        }
        url = urljoin(self.base_url, 'login')
        method = 'POST'
        while (response := self._request(method, url, data=data)).status_code == 302:
            url = response.headers.get('Location')
            method = 'GET'

        return response

    def register(self, username, email, password, password2, term='y'):
        data = {
            'username': username,
            'email': email,
            'password': password,
            'confirm': password2,
            'term': term,
            'submit': 'Register'
        }
        if term == 'delete':
            data.pop('term')
        url = urljoin(self.base_url, 'reg')
        method = 'POST'
        while (response := self._request(method, url, data=data)).status_code == 302:
            url = response.headers.get('Location')
            method = 'GET'

        return response

    def logout(self):
        return self._request('GET', urljoin(self.base_url, 'logout'))

    def add_user(self, username, password, email):
        data = {
            'username': username,
            'password': password,
            'email': email,
        }
        headers = {
            'Content-Type': 'application/json'
        }
        url = "/".join([self.base_url, "api", "add_user"])
        return self._request('POST', url, data=data, headers=headers, dumps_=True)

    def delete_user(self, username):
        url = "/".join([self.base_url, "api", "del_user", username])
        return self._request('GET', url)

    def block_user(self, username):
        url = "/".join([self.base_url, "api", "block_user", username])
        return self._request('GET', url)

    def accept_user(self, username):
        url = "/".join([self.base_url, "api", "accept_user", username])
        return self._request('GET', url)