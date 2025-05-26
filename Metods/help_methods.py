import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from Locators import main_page
from Metods import common


def remove_overlays(driver: WebDriver):
    """Удаляет все overlay-элементы"""
    scripts = [
        "document.querySelectorAll('.UserOnboarding_Backdrop__7IFBc').forEach(el => el.remove());",
        "document.querySelectorAll('[role=\"presentation\"]').forEach(el => el.remove());"
    ]
    for script in scripts:
        try:
            driver.execute_script(script)
        except:
            pass
    time.sleep(0.5)


def check_help_visibility(driver: WebDriver) -> tuple:
    """Проверяет отображение схемы помощи (используется только в первом тесте)"""
    try:
        #remove_overlays(driver)
        help_button = common.wait_element(driver, main_page.HELP_BUTTON, timeout=15, condition='clickable')
        help_button.click()
        common.wait_element(driver, main_page.HELP_SCHEMA, timeout=10, condition='visible')
        return (True, "Схема отображается")
    except Exception as e:
        return (False, f"Ошибка: {str(e)}")



def check_pagination(driver: WebDriver) -> tuple:
    """Проверяет наличие пагинации и возвращает количество страниц
    (Используется только в первом тесте"""
    try:
        dots = common.wait_element(driver, main_page.PAGINATION_DOTS, timeout=10, condition='all_visible')
        return (True, "Пагинация доступна", len(dots))
    except:
        return (True, "Пагинация отсутствует", 1)  # Если точек нет - считаем 1 страницу


def navigate_to_page(driver: WebDriver, page_num: int) -> bool:
    """Переходит на указанную страницу пагинации
    (используется только в первом тесте)"""
    try:
        dots = driver.find_elements(*main_page.PAGINATION_DOTS)
        if page_num < len(dots):
            dots[page_num].click()
            time.sleep(1)
            return True
        return False
    except:
        return False


def close_help_schema(driver: WebDriver) -> bool:
    """Закрытие схемы помощи через ESC"""
    try:
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(0.5)
        return True
    except Exception:
        return False


def check_help_flow(driver: WebDriver) -> list:
    """Проверка схемы помощи (используется только в первом тесте)"""
    results = []

    # 1. Кликаем кнопку помощи один раз в начале
    status, msg = check_help_visibility(driver)
    results.append(("Главная страница", status, msg))

    # 2. Проверяем пагинацию
    p_status, p_msg, total_pages = check_pagination(driver)
    results.append(("Пагинация", p_status, p_msg))

    # 3. Проверяем видимость схемы на других страницах
    for page in range(1, total_pages):
        if not navigate_to_page(driver, page):
            results.append((f"Страница {page + 1}", False, "Ошибка перехода"))
            continue

        # Проверка видимости схемы на каждой подстраницу
        try:
            common.wait_element(driver, main_page.HELP_SCHEMA, timeout=10, condition='all_visible')
            results.append((f"Страница {page + 1}", True, "Схема видна"))
        except:
            results.append((f"Страница {page + 1}", False, "Схема не видна"))

    return results


def check_help_on_page(driver: WebDriver, page_name: str) -> tuple:
    """ Проверяет отображение схемы помощи и закрывает её """
    print(f"\nПроверка схемы помощи для '{page_name}':")

    # 1. Клик по кнопке помощи
    print("1. Ищем кнопку помощи... ", end="")
    help_btn = common.wait_element(driver, main_page.HELP_BUTTON, timeout=5)
    if not help_btn:
        return (False, "Кнопка помощи не найдена")
    print("Найдена")

    # 2. Проверка отображения схемы
    print("2. Кликаем и проверяем схему... ", end="")
    help_btn.click()

    schema_visible = common.wait_element(driver, main_page.HELP_SCHEMA, timeout=5)
    if not schema_visible:
        return (False, "Схема не отобразилась")
    print("Отображается")

    # 3. Закрытие схемы
    print("3. Закрываем схему... ", end="")
    close_help_schema(driver)
    print("Выполнено")

    return (True, f"Схема помощи для '{page_name}' проверена")


def navigate_to_subpage(driver: WebDriver, subpage_name: str) -> tuple:
    """ Переходит на подстраницу и проверяет успешность перехода """
    print(f"\nПереход на подстраницу '{subpage_name}':")

    # 1. Клик по кнопке подстраницы
    btn_locator = (By.XPATH, f"//button[text()='{subpage_name}']")
    print(f"1. Ищем кнопку перехода... ", end="")
    btn = common.wait_element(driver, btn_locator, timeout=5)
    if not btn:
        return (False, "Кнопка перехода не найдена")
    print("Найдена")

    # 2. Клик и проверка загрузки
    print(f"2. Кликаем и проверяем загрузку... ", end="")
    btn.click()

    check_locator = (By.XPATH, f"//button[contains(@class, 'active') and text()='{subpage_name}']")
    page_loaded = common.wait_element(driver, check_locator, timeout=5)
    if not page_loaded:
        return (False, "Страница не загрузилась")

    print("Успешно")
    return (True, f"Успешно перешли на '{subpage_name}'")