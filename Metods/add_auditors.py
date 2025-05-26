import random

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from Locators import menu_settings, main_page
from Metods import common, auth_methods
from fixture import conftest


def navigate_to_audiences(driver):
    """ Переход от авторизации до подстраницы Аудитории """
    # 1. Авторизация
    assert common.check_site(driver), "Неверный сайт"
    auth_methods.login(driver, conftest.Login, conftest.Password)
    # print("Авторизация успешна")

    # Проверка успешного входа
    picture_day = common.wait_element(driver, main_page.PICTURE_DAY, condition="visible")
    assert picture_day.text == "Картина дня за", f"Неверный текст элемента: {picture_day.text}"

    # 2. Переход в раздел "Настройки"
    settings_btn = common.wait_element(driver, main_page.MENU_SETTINGS, timeout=25, condition='clickable')
    settings_btn.click()
    # print("Перешли в 'Настройки'")

    # 3. Проверка загрузки страницы
    auditore = common.wait_element(driver, menu_settings.TEMS, timeout=20, condition='visible')
    assert auditore.text == "Тематики", f"Неверный текст элемента: {auditore.text}"
    # print("Страница 'Настройки' загружена")

    # 4. Переход в подраздел "Аудитории"
    auditor_btn = common.wait_element(driver, menu_settings.AUDITOR, timeout=30, condition='clickable')
    auditor_btn.click()
    # print("Перешли в 'Аудитории'")

    # 5. Проверка загрузки страницы
    add_auditore = common.wait_element(driver, menu_settings.ADD_AUDITORE, timeout=30, condition='visible')
    assert add_auditore.text == "Добавить аудиторию", f"Неверный текст элемента: {add_auditore.text}"
    # print("Кнопка 'Добавить аудиторию' доступна")


def fill_audience_form(driver, title):
    """ Добавляет запись в форму. """
    title_input = common.wait_element(driver, menu_settings.TITLE_AUDITORE, condition='visible')
    title_input.clear()
    title_input.send_keys(title)


def add_indicator_and_check(driver, text, button_type):
    """Добавляет один индикатор указанного типа"""
    #print(f" - Добавляем {button_type} индикатор: {text}")

    # Вводим текст
    input_field = common.wait_element(driver, menu_settings.INDICATORS_ADD, condition='clickable')
    input_field.clear()
    input_field.send_keys(text)

    # Нажимаем кнопку
    button = menu_settings.GREEN_BUTTON if button_type == 'green' else menu_settings.RED_BUTTON
    common.wait_element(driver, button, condition='clickable').click()

    # Проверяем добавление
    indicator_class = 'positive' if button_type == 'green' else 'negative'
    indicator_locator = f"//div[contains(@class, '{indicator_class}')]//*[contains(text(), '{text}')]"

    if common.wait_element(driver, (By.XPATH, indicator_locator), condition='visible'):
        print(f"   Индикатор добавлен ({button_type})")
    else:
        print(f"   Ошибка добавления индикатора")


def remove_indicator_and_check(driver, text):
    """
    Удаляет указанный индикатор и проверяет его отсутствие
    Возвращает True если удаление прошло успешно, False если возникли проблемы
    """
    #print(f"\nУдаляем индикатор: '{text}'")

    # 1. Формируем локатор для поиска индикатора
    indicator_locator = (By.XPATH, f"//div[contains(@class, 'item_')]//*[contains(text(), '{text}')]")

    # 2. Проверяем наличие индикатора перед удалением
    if not common.wait_element(driver, indicator_locator, condition='visible'):
        print(f"Индикатор '{text}' не найден для удаления")
        return False

    # 3. Находим и нажимаем кнопку удаления
    delete_button_locator = (By.XPATH, f"{indicator_locator[1]}/following-sibling::button")

    if not common.wait_element(driver, delete_button_locator, condition='visible'):
        print(f"Не найдена кнопка удаления для индикатора '{text}'")
        return False

    common.wait_element(driver, delete_button_locator, condition='clickable').click()
    #print(f"Нажата кнопка удаления")

    # 4. Проверяем исчезновение индикатора с помощью wait_element
    if common.wait_element(driver, indicator_locator, timeout=3, condition='invisible'):
        print(f"Индикатор '{text}' успешно удален")
        return True

    #print(f"Индикатор '{text}' не исчез после удаления")
    return False


def political_buttons(driver, **kwargs):
    """
    Проверяет кликабельность политических кнопок
    :kwargs: count - сколько кнопок проверить (по умолчанию 2)
             skip - сколько первых кнопок пропустить (по умолчанию 0)
    """
    # Параметры из kwargs
    count = kwargs.get('count', 2)
    skip = kwargs.get('skip', 0)

    # Получаем все кнопки
    buttons = common.wait_element(driver, menu_settings.POLITICAL_BUTTONS, condition='all_visible')[skip:]

    # Проверяем указанное количество кнопок
    for button in random.sample(buttons, min(count, len(buttons))):
        btn_text = button.text
        was_active = 'active' in button.get_attribute('class')

        button.click()

        now_active = 'active' in button.get_attribute('class')
        assert was_active != now_active, f"Кнопка '{btn_text}' не изменила состояние"

        #print(f"Кнопка '{btn_text}' - {'деактивирована' if was_active else 'активирована'}")

    #print(f"Проверено {count} кнопок")
    return True


def search_audience(driver, title):
    """Ищет аудиторию в таблице"""
    # 1. Находим поле ввода и кликаем по нему
    search_field = common.wait_element(driver, menu_settings.SEARCH, timeout=20, condition='clickable')
    search_field.click()

    # 2. Полностью очищаем поле (3 попытки)
    cleaned = False
    for _ in range(3):
        # Очистка всеми доступными способами
        search_field.clear()  # Стандартный способ
        search_field.send_keys(Keys.CONTROL + 'a')  # Выделить всё
        search_field.send_keys(Keys.DELETE)  # Удалить

        # Проверяем через JavaScript, что поле действительно пустое
        if driver.execute_script("return arguments[0].value", search_field) == "":
            cleaned = True
            break

        # Небольшая пауза между попытками
        ActionChains(driver).pause(0.3).perform()

    if not cleaned:
        print("Ошибка: поле поиска не очистилось")
        return False

    # 3. Вводим новый текст
    search_field.send_keys(title)

    # Простая проверка
    return title in search_field.get_attribute('value')


def create_and_verify_audience(driver, title, should_create=True):
    """
    Создание аудитории и проверка ее наличия в таблице или отмена создания.
    :param driver: WebDriver
    :param title: Название аудитории
    :param should_create: Флаг создания (True - создать, False - отменить)
    :return: True/False в зависимости от результата (для случая создания)
    """
    # 1. Заполнение заголовка
    fill_audience_form(driver, title)
    #print(f"Заполнен заголовок: '{title}'")

    # 2. Добавляем индикатор, проверяем и удаляем
    add_indicator_and_check(driver, "Временный индикатор", button_type='green')
    remove_indicator_and_check(driver, "Временный индикатор")

    # 3. Добавляем постоянные индикаторы (зелёный и красный)
    add_indicator_and_check(driver, "Постоянный зелёный", button_type='green')
    add_indicator_and_check(driver, "Постоянный красный", button_type='red')
    #print("Индикаторы добавлены")

    # 4. Проверка кнопок "политической ориентации"
    political_buttons(driver, count=2, skip=1)
    #print("Кнопки политической ориентации проверены")

    if should_create:
        # 5. Сохранение
        save_button = common.wait_element(driver, menu_settings.SAVE_BUTTON, condition='clickable')
        save_button.click()
        print(f"Форма с аудиторией '{title}' сохранена")

        # 6. Проверка в таблице
        search_audience(driver, title)
        audience_locator = (By.XPATH, f"//*[contains(text(), '{title}')]")
        audience_row = common.wait_element(driver, audience_locator, timeout=15, condition='visible')

        if audience_row:
            print(f"Аудитория '{title}' успешно создана")
            return True
        else:
            print(f"Аудитория '{title}' не найдена")
            return False
    else:
        # 5. Отмена создания
        cancel_button = common.wait_element(driver, menu_settings.CANCEL_BUTTON, condition='clickable')
        cancel_button.click()
        #print(f"Создание аудитории '{title}' отменено")
        return True


def add_indicators(driver, indicators):
    """
    Добавляет указанные индикаторы, предварительно очищая существующие
    :param indicators: список словарей [{'text': 'текст', 'type': 'green/red'}]
    """
    #print("\nДобавляем индикаторы:")

    # Удаляем все существующие индикаторы
    while True:
        try:
            delete_btn = common.wait_element(driver, menu_settings.DELETE_BUTTON_INDICATOR,
                                             timeout=2, condition='clickable')
            delete_btn.click()
            #print("Удален существующий индикатор")
        except:
            break

    # Добавляем новые индикаторы
    for indicator in indicators:
        add_indicator_and_check(driver, indicator['text'], indicator['type'])

    #print(f"Добавлено {len(indicators)} новых индикаторов")


# Метод редактирования аудитории
def edit_audience(driver, title, new_title, indicators):
    """
    Редактирует существующую аудиторию
    :param title: текущее название аудитории
    :param new_title: новое название
    :param indicators: список индикаторов для добавления
    """
    #print(f"\n=== Редактируем аудиторию '{title}' ===")

    # 1. Находим и открываем аудиторию
    search_audience(driver, title)
    common.wait_element(driver, (By.XPATH, f"//a[text()='{title}']"), condition='clickable').click()

    # 2. Меняем название
    fill_audience_form(driver, new_title)
    #print(f"Название изменено на '{new_title}'")

    # 3. Обновляем индикаторы
    add_indicators(driver, indicators)

    # 4. Сохраняем
    common.wait_element(driver, menu_settings.SAVE_BUTTON, condition='clickable').click()
    #print("Изменения сохранены")

    # 5. Проверяем в таблице
    search_audience(driver, new_title)
    assert common.wait_element(driver, menu_settings.SEARCH, condition='visible'), \
        f"Аудитория '{new_title}' не найдена после редактирования"

    print(f"=== Аудитория успешно отредактирована ===")


# Метод удаления аудитории
def delete_audience(driver, new_title, should_delete=True):
    """
    Удаляет аудиторию или сохраняет ее название
    :param new_title: название аудитории
    :param should_delete: флаг удаления (по умолчанию True)
    :return: название аудитории (если should_delete=False)
    """
    #print(f"\n=== {'Удаляем' if should_delete else 'Проверяем'} аудиторию '{new_title}' ===")

    # 1. Находим аудиторию через поиск
    search_audience(driver, new_title)

    # 2. Получаем строку с аудиторией
    assert common.wait_element(driver, menu_settings.SEARCH, condition='visible'), \
        f"Аудитория '{new_title}' не найдена после редактирования"

    if not should_delete:
        print(f"Аудитория '{new_title}' найдена, удаление пропущено")
        return new_title

    # 3. Находим и нажимаем кнопку удаления в строке
    audience_row_btn = common.wait_element(driver, (By.XPATH, f"//a[text()='{new_title}']//following::button[contains(@class, 'deleteBtn')]"), condition='clickable')
    audience_row_btn.click()

    # 4. Удаляем аудиторию
    common.wait_element(driver, menu_settings.AGREE_ON_DELETE_AUDITORE, timeout=15, condition='clickable').click()

    # 5. Проверяем отсутствие
    search_audience(driver, new_title)

    # Проверяем что строка исчезла из DOM (не только стала невидимой)
    audience_present = True
    try:
        driver.find_element(By.XPATH, f"//a[text()='{new_title}']")
    except NoSuchElementException:
        audience_present = False

    assert not audience_present, f"Аудитория '{new_title}' все еще присутствует в DOM"
    print(f"=== Аудитория '{new_title}' успешно удалена ===")
    return None