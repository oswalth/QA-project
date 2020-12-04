from ui.fixtures import *
from api.fixtures import *

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


class UnsupportedBrowserException(Exception):
    pass


def pytest_addoption(parser):
    parser.addoption('--url', default='http://myapp:5050')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--browser_ver', default='80.0')
    parser.addoption('--selenoid', default=None)


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    version = request.config.getoption('--browser_ver')
    selenoid = request.config.getoption('--selenoid')

    return {'browser': browser, 'version': version, 'url': url, 'download_dir': '/tmp', 'selenoid': selenoid}


@pytest.fixture(scope="function")
def driver(config):
    browser = config['browser']
    version = config['version']
    url = config['url']
    download_dir = config['download_dir']
    selenoid = config['selenoid']
    print(selenoid)
    if browser == 'chrome':
        options = ChromeOptions()
        if selenoid:
            capabilities = {'acceptInsecureCerts': True,
                            'browserName': browser
                            }

            driver = webdriver.Remote(command_executor=selenoid,
                                      options=options,
                                      desired_capabilities=capabilities
                                      )
        else:
            options.add_argument("--window-size=800,600")

            prefs = {"download.default_directory": download_dir}
            options.add_experimental_option('prefs', prefs)

            manager = ChromeDriverManager(version=version)
            driver = webdriver.Chrome(executable_path=manager.install(),
                                      options=options,
                                      desired_capabilities={'acceptInsecureCerts': True}
                                      )
    else:
        raise UnsupportedBrowserException(f'Unsupported browser: "{browser}"')

    driver.get(url)
    driver.maximize_window()
    yield driver

    driver.quit()
