from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from fixture import conftest


def wait_element(driver, locator, timeout=10, condition="visible"):
    """Универсальный метод ожидания элемента
    :param condition:
    "visible" | "clickable" | "present" | "invisible" | "allvisible" | "text" | "alert"
    """
    conditions = {
        "visible": EC.visibility_of_element_located,          # Элемент виден
        "clickable": EC.element_to_be_clickable,              # Элемент кликабелен
        "present": EC.presence_of_element_located,            # Элемент есть в DOM
        "invisible": EC.invisibility_of_element_located,      # Элемент не виден
        "all_visible": EC.visibility_of_all_elements_located, # Все элементы видны
        "text": EC.text_to_be_present_in_element,             # Ожидание определенного текста
        "alert": EC.alert_is_present                          # Ожидание наличия алерта
    }

    if condition not in conditions:
        raise ValueError(f"Неверный тип ожидания. Допустимо: {list(conditions.keys())}")

    try:
        return WebDriverWait(driver, timeout).until(
            conditions[condition](locator)
        )
    except TimeoutException:
        raise TimeoutException(f"Элемент {locator} не стал {condition} за {timeout} сек")


# Примеры использования:
# wait_element(driver, LOGIN_BUTTON, condition="clickable")
# wait_element(driver, PICTURE_DAY, condition="visible")


def check_site(driver):  #принимает драйвер и проверяет корректность сайта
    expected_title = "Ao24 | Главная"
    driver.get(conftest.url)
    WebDriverWait(driver, 10).until(
        EC.title_is(expected_title)
    )
    print("Проверка сайта: успешно")
    return True


def scroll_to_find_element(driver, dropdown_locator, items_locator, search_text,
                           exact_match=True, max_attempts=5, timeout=15):
    """
    Универсальный метод поиска элемента в списках с прокруткой и точным совпадением
    :param driver: WebDriver
    :param dropdown_locator: Локатор для открытия dropdown (None если уже открыт)
    :param items_locator: Локатор элементов списка
    :param search_text: Текст для поиска
    :param exact_match: True - точное совпадение, False - частичное
    :param max_attempts: Максимальное количество попыток прокрутки
    :param timeout: Таймаут ожидания элементов
    :return: Найденный элемент или None
    """
    #print(f"\nПоиск элемента: '{search_text}' (точное совпадение: {exact_match})")

    # 1. Открываем dropdown если указан локатор
    if dropdown_locator:
        dropdown = wait_element(driver, dropdown_locator, condition='clickable', timeout=timeout)
        dropdown.click()
        print(" - Dropdown открыт")

    # 2. Получаем контейнер списка
    try:
        first_item = wait_element(driver, items_locator, condition='visible', timeout=5)
        container = first_item.find_element(By.XPATH,
                                            "./ancestor::div[contains(@class, 'dropdown') or contains(@class, 'menu') or contains(@class, 'list')][1]")
    except:
        container = driver.find_element(By.TAG_NAME, 'body')
        print(" - Контейнер списка не найден, используется body")

    # 3. Поиск с прокруткой
    last_height = driver.execute_script("return arguments[0].scrollHeight", container)
    attempts = 0

    while attempts < max_attempts:
        # Получаем текущие элементы
        items = wait_element(driver, items_locator, condition='all_visible', timeout=5)

        # Поиск по точному или частичному совпадению
        for item in items:
            try:
                item_text = item.text.strip()
                match = (item_text == search_text) if exact_match else (search_text in item_text)

                if match:
                    #print(f" - Найден элемент: '{item_text}'")
                    # Прокручиваем и делаем элемент видимым
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", item)
                    ActionChains(driver).move_to_element(item).pause(0.3).perform()
                    return item
            except StaleElementReferenceException:
                continue

        # Прокрутка вниз
        driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight * 0.8",
            container
        )
        ActionChains(driver).pause(0.5).perform()

        # Проверка конца списка
        new_height = driver.execute_script("return arguments[0].scrollHeight", container)
        if new_height == last_height:
            break
        last_height = new_height
        attempts += 1
        #print(f" - Попытка прокрутки {attempts}/{max_attempts}")

    #print(f"Элемент '{search_text}' не найден после {max_attempts} попыток")
    return None