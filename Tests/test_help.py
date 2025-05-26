import pytest

from Locators import main_page, menu_report, menu_settings
from fixture.conftest import browser_setup2
from Metods import auth_methods, common, help_methods
from fixture import conftest


@pytest.mark.usefixtures("browser_setup2")
def test_help_day_picture(browser_setup2):
    """Тест для раздела 'Картина дня"""
    driver = browser_setup2
    print("\n=== Тест 'Картина дня' ===")

    # Авторизация (уже открывает "Картину дня")
    assert common.check_site(driver), "Неверный сайт"
    auth_methods.login(driver, conftest.Login, conftest.Password)

    #Проверка успешного входа
    picture_day = common.wait_element(driver, main_page.PICTURE_DAY, condition="visible")
    assert picture_day.text == "Картина дня", f"Неверный текст элемента: {picture_day.text}"

    # Проверка
    results = help_methods.check_help_flow(driver)

    # Закрытие схемы
    assert help_methods.close_help_schema(driver), "Не удалось закрыть схему"

    # Отчет
    for name, status, msg in results:
        assert status, f"{name}: {msg}"
    print("✅ Тест завершен успешно")


def test_help_report(browser_setup2):
    driver = browser_setup2
    print('\n== Тест "Отчёт" ==')

    # 1. Авторизация
    assert common.check_site(driver), "Неверный сайт"
    auth_methods.login(driver, conftest.Login, conftest.Password)

    # 2. Переход в раздел "Отчёт"
    # Клик по кнопке перехода в отчёт
    report_btn = common.wait_element(driver, main_page.MENU_REPORT, timeout=20, condition='clickable')
    driver.execute_script("arguments[0].click();", report_btn)

    # 3. Проверка загрузки страницы
    auditore = common.wait_element(driver, menu_report.AUDITORE, timeout=20, condition='visible')
    assert auditore.text == "Аудитории", f"Неверный текст элемента: {auditore.text}"

    # 4. Проверка схемы
    success, msg = help_methods.check_help_on_page(driver, "Отчет")
    print(msg)

    # 5. Проверка подстраниц
    subpages = ["Аудитории", "Сюжеты", "Индикаторы"]

    for subpage in subpages:
        # Переход
        success, msg = help_methods.navigate_to_subpage(driver, subpage)
        print(msg)
        if not success:
            continue  # Переходим к следующей подстранице

        # Проверка схемы
        success, msg = help_methods.check_help_on_page(driver, subpage)
        print(msg)

    print("\n=== Тест завершён ===")


def test_help_settings(browser_setup2):
    driver = browser_setup2
    print('\n== Тест "Настройки" ==')

    # 1. Авторизация
    assert common.check_site(driver), "Неверный сайт"
    auth_methods.login(driver, conftest.Login, conftest.Password)

    # 2. Переход в раздел "Настройки"
    # Клик по кнопке перехода в Настройки
    settings_btn = common.wait_element(driver, main_page.MENU_SETTINGS, timeout=20, condition='clickable')
    driver.execute_script("arguments[0].click();", settings_btn)

    # 3. Проверка загрузки страницы
    auditore = common.wait_element(driver, menu_settings.TEMS, timeout=20, condition='visible')
    assert auditore.text == "Тематики", f"Неверный текст элемента: {auditore.text}"

    # 4. Проверка схемы
    success, msg = help_methods.check_help_on_page(driver, "Настройки")
    print(msg)

    # 5. Проверка подстраниц
    subpages = ["Тематики", "Каналы", "Аудитории"]

    for subpage in subpages:
        # Переход
        success, msg = help_methods.navigate_to_subpage(driver, subpage)
        print(msg)
        if not success:
            continue  # Переходим к следующей подстранице

        # Проверка схемы
        success, msg = help_methods.check_help_on_page(driver, subpage)
        print(msg)

    print("\n=== Тест завершён ===")