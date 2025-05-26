from selenium.webdriver.common.by import By

EMAIL_FIELD = (By.XPATH, "//input[@name='email']")
PASSWORD_FIELD = (By.XPATH, "//input[@name='password']")
LOGIN_BUTTON = (By.XPATH, "//button/span[text()='Войти']")