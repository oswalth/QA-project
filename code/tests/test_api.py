import pytest
import requests

from tests.base import BaseAPICase


@pytest.mark.skip('no')
class TestAPI(BaseAPICase):
    def test1(self):
        response = requests.get('http://0.0.0.0:5050')
        print(response)


