import pytest
from fixture.conftest import browser_setup2
from Locators import main_page
from Metods.auth_methods import login
from Metods.common import wait_element, check_site
from fixture import conftest

@pytest.mark.usefixtures("browser_setup2")
def test_successful_auth(browser_setup2):
    driver = browser_setup2

    # 1. Проверка сайта
    assert check_site(driver), "Неверный сайт"

    # 2. Авторизация с обработкой таймаута
    try:
        login(driver, conftest.Login, conftest.Password, timeout=15)
    except Exception as e:
        pytest.fail(f"Ошибка авторизации: {str(e)}")

    # 3. Проверка успешного входа
    picture_day = wait_element(driver, main_page.PICTURE_DAY, condition="visible")
    assert picture_day.text == "Картина дня за ", f"Неверный текст элемента: {picture_day.text}"