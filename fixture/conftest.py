import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import os
from dotenv import load_dotenv
from telnetlib import EC

load_dotenv()
url = os.getenv("url")
Login = os.getenv("login")
Password = os.getenv("password")


@pytest.fixture
def browser_setup(request):
    # Инициализация браузера
    driver = webdriver.Chrome()
    driver.maximize_window()
    print("\nBrowser opened (finalizer)")
    def fin():
        driver.quit()
        print("\nBrowser closed (finalizer)")
    request.addfinalizer(fin)
    return driver

def test_example_with_finalizer(browser_setup):
    driver = browser_setup
    driver.get("https://assist24.tech/app")
    print("\nTest is running with finalizer")


@pytest.fixture()
def browser_setup2():
    # Инициализация драйвера
    driver = webdriver.Chrome()
    driver.maximize_window()
    print("\nBrowser opened (yield)")

    # Передаем драйвер тесту
    yield driver

    # Закрытие браузера после теста
    driver.quit()
    print("\nBrowser closed (via yield)")

def test_check_site(browser_setup2):
    driver = browser_setup2
    driver.get("https://assist24.tech/app")

    # Получаем текущий заголовок
    actual_title = driver.title
    print(f"\nActual title: {actual_title}")

    # Ждем загрузки страницы
    WebDriverWait(driver, 10).until(
        EC.title_is("Ao24 | Главная")
    )

    # Ожидаемый заголовок (используем raw строку для кириллицы)
    expected_title = r"Ao24 | Главная"

    # Сравниваем заголовки
    assert actual_title == expected_title