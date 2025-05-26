from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from Locators import menu_settings, main_page
from Metods import common, auth_methods
from fixture import conftest


def navigate_to_canals(driver):
    """ Переход от авторизации до подстраницы Каналы """
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
    canal = common.wait_element(driver, menu_settings.TEMS, timeout=20, condition='visible')
    assert canal.text == "Тематики", f"Неверный текст элемента: {canal.text}"
    # print("Страница 'Настройки' загружена")

    # 4. Переход в подраздел "Каналы"
    canal_btn = common.wait_element(driver, menu_settings.CANAL, timeout=30, condition='clickable')
    canal_btn.click()
    #print("Перешли в 'Каналы'")

    # 5. Проверка загрузки страницы
    add_canal = common.wait_element(driver, menu_settings.ADD_CANAL, timeout=30, condition='visible')
    assert add_canal.text == "Добавить канал", f"Неверный текст элемента: {add_canal.text}"
    #print("Кнопка 'Добавить канал' доступна")


def fill_canal_form(driver, title):
    """Заполняет название канала"""
    title_input = common.wait_element(driver, menu_settings.TITLE_CANAL, condition='visible')
    title_input.clear()
    title_input.send_keys(title)
    #print(f"Заполнено название: '{title}'")


def select_canal_type(driver, canal_type, telegram_link=None):
    """Выбор типа канала с валидацией
    :param canal_type: 'Telegram' или 'Внутренний'
    :param telegram_link: Ссылка в форматах:
                         https://t.me/channel (публичный канал)
                         https://t.me/c/1234567890/123 (приватный канал/сообщение)
    """
    type_dropdown = common.wait_element(driver, menu_settings.TYPE_CANAL, condition='clickable')
    type_dropdown.click()

    if canal_type == 'Telegram':
        if not telegram_link or not telegram_link.startswith('https://t.me/'):
            print("Ошибка: неверный формат Telegram ссылки")
            common.wait_element(driver, menu_settings.INTERNAL_TYPE).click()
            return False

        common.wait_element(driver, menu_settings.TELEGRAM_TYPE).click()
        id_field = common.wait_element(driver, menu_settings.IDENTIFIER)
        id_field.clear()
        id_field.send_keys(telegram_link)
        #print(f"Выбран Telegram с ссылкой: {telegram_link}")
        return True

    elif canal_type == 'Внутренний':
        common.wait_element(driver, menu_settings.INTERNAL_TYPE).click()
        print("Выбран внутренний тип")
        return True

    return False


def search_canal(driver, title):
    """
    Поиск канала в таблице
    Шаги:
    1. Ожидаем появление поля поиска
    2. Очищаем поле (3 попытки)
    3. Вводим текст для поиска
    4. Проверяем что текст введен корректно
    """
    #print(f"\nПоиск канала: '{title}'")

    # 1. Ожидаем поле поиска
    search_field = common.wait_element(driver, menu_settings.SEARCH_CANALS, timeout=20, condition='visible')
    if not search_field:
        print("Поле поиска не найдено")
        return False

    # 2. Очистка поля
    cleaned = False
    for attempt in range(3):
        search_field.send_keys(Keys.CONTROL + 'a')
        search_field.send_keys(Keys.DELETE)
        ActionChains(driver).pause(0.3).perform()

        if search_field.get_attribute('value') == '':
            cleaned = True
            break

    if not cleaned:
        print("Не удалось очистить поле поиска")
        return False

    # 3. Ввод текста
    search_field.send_keys(title)
    ActionChains(driver).pause(0.5).perform()

    # 4. Проверка ввода
    current_text = search_field.get_attribute('value')
    if title not in current_text:
        print(f"Ошибка: введен текст '{current_text}', ожидалось '{title}'")
        return False

    #print("Поиск выполнен успешно")
    return True


def create_and_verify_canal(driver, title, canal_type='Внутренний', telegram_link=None, should_create=True):
    """Создание/отмена создания канала
    :param canal_type: 'Telegram' или 'Внутренний'
    :param telegram_link: обязателен для типа 'Telegram'
    :param should_create: True - создать, False - отменить
    """
    # Открываем форму
    common.wait_element(driver, menu_settings.ADD_CANAL, condition='clickable').click()

    # Заполняем данные
    fill_canal_form(driver, title)
    select_canal_type(driver, canal_type, telegram_link)

    if should_create:
        common.wait_element(driver, menu_settings.ADD_BUTTON, condition='clickable').click()
        assert search_canal(driver, title), f"Канал '{title}' не найден после создания"
        #print(f"\n=== Канал '{title}' создан ===")
        return True
    else:
        common.wait_element(driver, menu_settings.CANCEL_BUTTON_CANAL, condition='clickable').click()
        return True


def edit_canal(driver, old_title, new_title, new_type='Внутренний', telegram_link=None):
    """Редактирование канала
    :param old_title: текущее название аудитории
    :param new_title: новое название
    :param telegram_link: ссылка на Telegram канал или сообщение
    """
    #print(f"\n=== Редактирование канала: {old_title} -> {new_title} ===")

    # 1. Поиск канала
    #print(f"Ищем канал: {old_title}")
    if not search_canal(driver, old_title):
        print(f"Ошибка: канал '{old_title}' не найден в таблице")
        return False

    # 2. Клик по названию
    #print("Пытаемся кликнуть по названию канала")
    title_locator = (By.XPATH, f"//span[text()='{old_title}']")

    # Ждем пока элемент станет видимым
    title_element = common.wait_element(driver, title_locator, timeout=20, condition='visible')
    if not title_element:
        print(f"Ошибка: не удалось найти элемент с названием '{old_title}'")
        return False

    # Пробуем кликнуть обычным способом или через JS
    try:
        title_element.click()
    except:
        print("Обычный клик не сработал, пробуем через JavaScript")
        driver.execute_script("arguments[0].click();", title_element)

    #print("Форма редактирования открыта")

    # 3. Изменение данных
    # Очищаем и вводим новое название
    #print(f"Меняем название на: {new_title}")
    title_field = common.wait_element(driver, menu_settings.TITLE_CANAL, condition='clickable')
    if title_field:
        title_field.clear()
        title_field.send_keys(new_title)
    else:
        print("Ошибка: не найдено поле для ввода названия")
        return False

    # Меняем тип канала если нужно
    if new_type:
        #print(f"Меняем тип на: {new_type}")
        if not select_canal_type(driver, new_type, telegram_link):
            return False

    # 4. Сохранение
    #print("Сохраняем изменения")
    save_btn = common.wait_element(driver, menu_settings.SAVE_BUTTON, timeout=20, condition='clickable')
    if save_btn:
        save_btn.click()
    else:
        print("Ошибка: не найдена кнопка сохранения")
        return False

    # 5. Проверка обновления
    #print("Проверяем обновленные данные")
    ActionChains(driver).pause(2).perform()  # Даем время на обновление

    if not search_canal(driver, new_title):
        print(f"Ошибка: новое название '{new_title}' не найдено в таблице")
        return False

    #print("=== Канал успешно отредактирован ===")
    return True



def delete_canal(driver, canal_name, should_delete=True, confirm_deletion=True):
    """
    Удаление канала с возможностью отмены на разных этапах
    :param canal_name: название канала
    :param should_delete: False - пропустить удаление
    :param confirm_deletion: True - подтвердить удаление, False - отменить в диалоге
    """
    if not should_delete:
        print(f"Удаление канала '{canal_name}' пропущено по флагу")
        return True

    # Поиск и открытие канала
    search_canal(driver, canal_name)
    new_title_locator = (By.XPATH, f"//span[text()='{canal_name}']/ancestor::div[contains(@class,'TableBody')]/descendant::div[contains(@class,'Trash')]")
    common.wait_element(driver, new_title_locator, condition='clickable').click()

    # Обработка диалога подтверждения
    if confirm_deletion:
        common.wait_element(driver, menu_settings.AGREE_ON_DELETE_CANAL, condition='clickable').click()

        # Проверка отсутствия
        ActionChains(driver).pause(1).perform()       # Небольшая пауза для обновления таблицы
        return not driver.find_elements(By.XPATH, f"//span[text()='{canal_name}']")
    else:
        common.wait_element(driver, menu_settings.NOT_AGREE_ON_DELETE_CANAL, condition='clickable').click()
        return search_canal(driver, canal_name)