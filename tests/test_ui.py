import time
import allure
import pytest
import requests
from allure_commons.types import AttachmentType

from tests.base import BaseUICase


class TestUI(BaseUICase):
    def test1(self):
        with allure.step('Trying test1'):
            time.sleep(2)
            allure.attach(name='Before', body=self.driver.get_screenshot_as_png(), attachment_type=AttachmentType.PNG)
            self.login_page.click(self.login_page.locators.LOGIN_BUTTON)
            time.sleep(2)
            assert 1 == 1
        # response = requests.get('http://0.0.0.0:5050')
        # print(response)

    def test2(self):
        with allure.step('Trying test2'):
            time.sleep(2)
            allure.attach(name='Before', body=self.driver.get_screenshot_as_png(), attachment_type=AttachmentType.PNG)
            self.login_page.click(self.login_page.locators.REG_BUTTON)
            time.sleep(2)
            assert 1 == 2
    # @pytest.mark.skip('no')
    # def test2(self):
    #     assert 2 == 2
    #
    # @pytest.mark.skip('no')
    # def test3(self):
    #     assert 2 == 3