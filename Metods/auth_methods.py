from Locators.auth import EMAIL_FIELD, PASSWORD_FIELD, LOGIN_BUTTON
from Metods.common import wait_element

def login(driver, email, password, timeout=10):
    """Авторизация на сайте"""
    # Ввод email с ожиданием видимости поля
    email_input = wait_element(driver, EMAIL_FIELD, timeout=timeout, condition="visible")
    email_input.clear()
    email_input.send_keys(email)

    # Ввод пароля с ожиданием видимости
    password_input = wait_element(driver, PASSWORD_FIELD, timeout=timeout, condition="visible")
    password_input.clear()
    password_input.send_keys(password)

    # Клик по кнопке с ожиданием кликабельности
    login_btn = wait_element(driver, LOGIN_BUTTON, timeout=timeout, condition="clickable")
    login_btn.click()

    # Возвращаем драйвер для цепочки вызовов
    return driver