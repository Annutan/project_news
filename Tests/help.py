import pytest
from selenium.webdriver.common.by import By
from Locators import main_page, menu_report, menu_settings
from fixture.conftest import browser_setup2
from Metods import auth_methods, common, help_methods
from fixture import conftest
import time



@pytest.mark.usefixtures("browser_setup2")
def test_help_schema_in_all_sections(browser_setup2):
    driver = browser_setup2
    sections = ["Картина дня", "Отчёт", "Настройки"]

    # 1. Авторизация
    assert common.check_site(driver), "Неверный сайт"
    try:
        auth_methods.login(driver, conftest.Login, conftest.Password)
    except Exception as e:
        pytest.fail(f"Ошибка авторизации: {str(e)}")

    # 2. Проверка в каждом разделе
    for section in sections:
        print(f"\n=== Проверка раздела: {section} ===")

        # Переход в раздел
        if not help_methods.navigate_to_section(driver, section):
            pytest.skip(f"Не удалось перейти в раздел {section}")

        # Полная проверка схемы помощи
        results = []

        # Проверка на главной странице раздела
        status, msg = help_methods.check_help_visibility(driver)
        results.append((f"{section} - главная", status, msg))

        # Проверка пагинации (если есть)
        p_status, p_msg, total_pages = help_methods.check_pagination(driver)

        if total_pages > 1:
            for page in range(1, total_pages):
                if not help_methods.navigate_to_page(driver, page):
                    results.append((f"{section} - страница {page + 1}", False, "Ошибка перехода"))
                    continue

                status, msg = help_methods.check_help_visibility(driver)
                results.append((f"{section} - страница {page + 1}", status, msg))

        # Закрытие схемы

        if not help_methods.close_help_schema(driver):
            results.append((f"{section} - закрытие", False, "Ошибка закрытия"))

        # Проверка результатов для раздела
        for page, status, msg in results:
            assert status, f"{page}: {msg}"

    print("\n=== Проверка во всех разделах завершена ===")


@pytest.mark.usefixtures("browser_setup2")
def test_help_day_picture(browser_setup2):
    """Тест для раздела 'Картина дня'"""
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


@pytest.mark.usefixtures("browser_setup2")
def test_help_report(browser_setup2):
    """Тест для раздела 'Отчёт'"""
    driver = browser_setup2
    print("\n=== Тест 'Отчёт' ===")

    # 1. Авторизация
    assert common.check_site(driver), "Неверный сайт"
    auth_methods.login(driver, conftest.Login, conftest.Password)

    # 2. Проверка успешного входа
    picture_day = common.wait_element(driver, main_page.PICTURE_DAY, condition="visible")
    assert picture_day.text == "Картина дня", f"Неверный текст элемента: {picture_day.text}"

    # 3. Переход в раздел "Отчёт"
    # Клик по кнопке перехода в отчёт
    report_btn = common.wait_element(driver, main_page.MENU_REPORT, timeout=20, condition='clickable')
    driver.execute_script("arguments[0].click();", report_btn)

    # Проверка загрузки страницы по локатору AUDITORE
    auditore = common.wait_element(driver, menu_report.AUDITORE, timeout=20, condition='visible')
    assert auditore.text == "Аудитории", f"Неверный текст элемента: {auditore.text}"

    # 4. Проверка схемы помощи
    results = help_methods.check_help_flow(driver)

    # 5. Закрытие схемы
    assert help_methods.close_help_schema(driver), "Не удалось закрыть схему"

    # 6. Отчет
    for name, status, msg in results:
        assert status, f"{name}: {msg}"
    print("✅ Тест завершен успешно")



@pytest.mark.usefixtures("browser_setup2")
def test_help_settings(browser_setup2):
    """Тест для раздела 'Настройки'"""
    driver = browser_setup2
    print("\n=== Тест 'Настройки' ===")
    # 1. Авторизация
    assert common.check_site(driver), "Неверный сайт"
    auth_methods.login(driver, conftest.Login, conftest.Password)
    # Проверка успешного входа
    picture_day = common.wait_element(driver, main_page.PICTURE_DAY, condition="visible")
    assert picture_day.text == "Картина дня", f"Неверный текст элемента: {picture_day.text}"
    # 3. Переход в раздел "Настройки" # Клик по кнопке перехода в отчёт
    report_btn = common.wait_element(driver, main_page.MENU_SETTINGS, timeout=25, condition='clickable')
    driver.execute_script("arguments[0].click();", report_btn)
    # Проверка загрузки страницы "Настройки"
    tems = common.wait_element(driver, menu_settings.TEMS, timeout=20, condition='visible')
    assert tems.text == "Тематики", f"Неверный текст элемента: {tems.text}"
    # 4. Проверка схемы помощи
    results = help_methods.check_help_flow(driver)
    assert help_methods.close_help_schema(driver), "Не удалось закрыть схему"   # Закрытие схемы
    # Отчет
    for name, status, msg in results:
        assert status, f"{name}: {msg}"
    print("✅ Тест завершен успешно")