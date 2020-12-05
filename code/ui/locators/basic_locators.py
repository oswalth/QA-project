from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN_BUTTON = (By.XPATH, '//input[@value="Login"]')
    REG_BUTTON = (By.XPATH, '//a[@href="/reg"]')

    USERNAME_FIELD = (By.XPATH, '//input[@placeholder="Username"]')
    PASSWORD_FIELD = (By.XPATH, '//input[@placeholder="Password"]')

    # REGISTER BLOCK
    EMAIL_REG_FIELD = (By.XPATH, '//input[@placeholder="Email"]')
    PASSWORD2_REG_FIELD = (By.XPATH, '//input[@placeholder="Repeat password"]')
    TERMS_CHECKBOX = (By.XPATH, '//input[@type="checkbox"]')
    CONFIRM_REG_BUTTON = (By.XPATH, '//input[@value="Register"]')

    USER_EXIST_MSG = (By.XPATH, '//div[text()="User already exist"]')
    USERNAME_LENGTH_MSG = (By.XPATH, '//div[text()="Incorrect username length"]')

    EMAIL_EXIST_MSG = (By.XPATH, '//div[text()="Email already exist"]')
    EMAIL_INVALID_MSG = (By.XPATH, '//div[text()="Invalid email address"]')
    EMAIL_LENGTH_MSG = (By.XPATH, '//div[text()="Incorrect email length"]')

    # LOGIN BLOCK
    LOGIN_INVALID_MSG = (By.XPATH, '//div[text()="Invalid username or password"]')

    # MAIN PAGE BLOCK
    LOGOUT_BUTTON = (By.XPATH, '//a[@href="/logout"]')
    VKID_LOCATOR = (By.XPATH, '//div[@id="login-name"]//li[text()="VK ID: {}"]')

    LOGO_BUTTON = (By.XPATH, '//nav/ul/a[@href="/"]')
    HOME_BUTTON = (By.XPATH, '//nav/ul/li/a[@href="/"]')
    PYTHON_BUTTON = (By.XPATH, '//nav/ul/li/a[text()="Python"]')
    LINUX_BUTTON = (By.XPATH, '//nav/ul/li/a[text()="Linux"]')
    NETWORK_BUTTON = (By.XPATH, '//nav/ul/li/a[text()="Network"]')

    PYTHON_DROPDOWN = (By.XPATH, '//li[contains(@class, "uk-open")]/a[text()="Python"]')
    PYTHON_HISTORY = (By.XPATH, '//li[contains(@class, "uk-open")]//li/a[text()="Python history"]')
    PYTHON_FLASK = (By.XPATH, '//li[contains(@class, "uk-open")]//li/a[contains(text(),"About Flask")]')

    LINUX_DROPDOWN = (By.XPATH, '//li[contains(@class, "uk-open")]/a[text()="Linux"]')
    LINUX_CENTOS = (By.XPATH, '//li[contains(@class, "uk-open")]//li/a[text()="Download Centos7"]')

    NETWORK_DROPDOWN = (By.XPATH, '//li[contains(@class, "uk-open")]/a[text()="Network"]')
    NETWORK_WS_NEWS = (By.XPATH,
                       '//li[contains(@class, "uk-open")]//li[contains(text(),"Wireshark")]/ul/li/a[text()="News"]')
    NETWORK_WS_DOWNLOAD = (By.XPATH,
                           '//li[contains(@class, "uk-open")]//li[contains(text(),"Wireshark")]/ul/li/a[text('
                           ')="Download"]')
    NETWORK_TCPDUMP_EXAMPLES = (By.XPATH, '//li[contains(@class, "uk-open")]//li[contains(text(),"Tcpdump")]/ul/li/a['
                                          'contains(text(),"Examples")]')

    CONTENT_IMAGE_1 = (By.XPATH, '//div[@id="content"]/*[2]/*[1]/figure')
    CONTENT_IMAGE_2 = (By.XPATH, '//div[@id="content"]/*[2]/*[2]/figure')
    CONTENT_IMAGE_3 = (By.XPATH, '//div[@id="content"]/*[2]/*[3]/figure')
