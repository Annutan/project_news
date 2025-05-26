from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from Locators import menu_settings, main_page
from Metods import common, auth_methods
from fixture import conftest


def navigate_to_tems(driver):
    """ Переход от авторизации до подстраницы Тематики """
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


def fill_text_field(driver, locator, text):
    """Заполнение текстового поля с очисткой"""
    field = common.wait_element(driver, locator)
    field.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
    field.send_keys(text)
    #print(f"Заполнено поле {locator}: {text}")


def select_event_class(driver, class_index=0):
    """
    Выбор класса событий из выпадающего списка
    :param driver: WebDriver
    :param class_index: Индекс класса (0-based)
    :return: Название выбранного класса или None если не удалось
    """
    #print("\n=== Выбор класса событий ===")

    # 1. Открываем список классов
    #print("1. Кликаем на поле выбора")
    add_class_field = common.wait_element(driver, menu_settings.ADD_CLASS, condition='clickable')
    add_class_field.click()

    # 2. Получаем список классов (с ожиданием)
    #print("2. Получаем список классов")
    class_locator = "//div[contains(@class, 'mantine-Select-item')]"
    class_items = common.wait_element(driver, (By.XPATH, class_locator), condition='all_visible')

    if not class_items or class_index >= len(class_items):
        #print(f"3. Ошибка: нет класса с индексом {class_index}")
        return None

    # 3. Получаем текст перед кликом
    selected_class = class_items[class_index]
    class_name = selected_class.text
    #print(f"Выбираем: {class_name}")

    # 4. Кликаем через JavaScript (чтобы избежать StaleElement)
    #print("4. Кликаем через JS")
    selected_class.click()

    # 5. Проверяем результат
    #print(f"Шаг 5: Проверяем результат выбора")
    current_value = add_class_field.get_attribute('value')
    if class_name in current_value:
        #print(f"Успешно выбрано: {class_name}")
        return class_name

    print(f"Проверка не пройдена. В поле: {current_value}")
    return None


def fill_required_fields(driver, title, class_index=0):
    """Заполнение обязательных полей"""
    fill_text_field(driver, menu_settings.TITLE_TEM, title)

    # Выбираем класс
    selected_class = select_event_class(driver, class_index)
    if selected_class:
        print(f"Выбран класс: {selected_class}")
    else:
        print("Не удалось выбрать класс событий")
    #print(f"Заполнены обязательные поля: {title}")


def fill_optional_fields(driver):
    """
    Заполнение необязательных полей тематики
    :param driver: WebDriver
    :return: None
    """
    #print("\n=== Заполнение необязательных полей ===")

    # 1. Каналы для публикации
    #print("1. Добавление каналов публикации")
    add_channels(driver, count=3)

    # 2. Языки
    #print("2. Добавление языков")
    add_languages(driver)

    # 3. География событий
    #print("3. Добавление географии")
    add_geography(driver)

    # 4. Ключевые слова
    #print("4. Добавление ключевых слов")
    add_keywords(driver, "тест,пример,ключевое слово")

    # 5. Источники публикаций
    print("5. Добавление источников временно не работает")
    #add_publication_sources(driver, ["https://t.me/test1", "https://t.me/test2"])


def verify_and_remove(driver, items_locator, delete_locator, expected_before):
    """
    Проверяет количество элементов и гарантированно удаляет первый элемент
    Параметры:
    - driver: экземпляр WebDriver
    - items_locator: локатор элементов для проверки
    - delete_locator: локатор кнопок удаления
    - expected_before: ожидаемое количество элементов до удаления
    Возвращает:
    - Список оставшихся элементов после удаления
    """
    #print("\n=== Начало проверки и удаления ===")

    # 1. Получаем текущие элементы
    items = common.wait_element(driver, items_locator, condition='all_visible')
    #print(f"Найдено элементов: {len(items)}")

    # 2. Проверяем количество элементов
    if len(items) != expected_before:
        print(f"Ошибка: ожидалось {expected_before} элементов, найдено {len(items)}")
        return items

    if not items:
        print("Нет элементов для удаления")
        return []

    # 3. Запоминаем текст удаляемого элемента
    item_to_delete = items[0].text
    #print(f"Пытаемся удалить: '{item_to_delete}'")

    # 4. Находим кнопку удаления
    delete_button = driver.find_element(*delete_locator)

    # 5. Пробуем разные способы удаления
    success = False

    # Способ 1: Обычный клик
    try:
        delete_button.click()
        #print("Стандартный клик выполнен")
        success = True
    except:
        print("Стандартный клик не сработал")

    # Способ 2: ActionChains если первый не сработал
    if not success:
        try:
            ActionChains(driver).move_to_element(delete_button).pause(0.5).click().perform()
            #print("Клик через ActionChains выполнен")
            success = True
        except:
            print("ActionChains не сработал")

    # Способ 3: JavaScript если предыдущие не сработали
    if not success:
        try:
            driver.execute_script("arguments[0].click();", delete_button)
            #print("Клик через JavaScript выполнен")
            success = True
        except:
            print("JavaScript клик не сработал")

    # 6. Проверяем реальное удаление
    if success:
        # Ждем обновления списка
        ActionChains(driver).pause(1).perform()  # Небольшая пауза для гарантированного обновления

        # Получаем обновленный список
        remaining_items = common.wait_element(driver, items_locator, condition='all_visible')
        actual_count = len(remaining_items)

        # Проверяем, что количество уменьшилось
        if actual_count == expected_before - 1:
            #print(f"Удаление подтверждено. Осталось элементов: {actual_count}")
            return remaining_items
        else:
            print(f"Ошибка: элемент не удалился. Осталось: {actual_count}")
    else:
        print("Не удалось выполнить удаление")

    return items


def add_channels(driver, count=3):
    """Добавление каналов с использованием универсального метода проверки"""
    #print(f"\nДобавляем {count} канала(ов)")

    # 1. Открываем dropdown
    dropdown = common.wait_element(driver, menu_settings.CANAL_FOR_TEM, condition='clickable')
    dropdown.click()

    # 2. Добавляем каналы
    channels = common.wait_element(driver, menu_settings.CANALS_TEM, condition='all_visible')
    channels_to_add = [channel.text for channel in channels[:min(count, len(channels))]]

    for i in range(len(channels_to_add)):
        driver.find_elements(*menu_settings.CANALS_TEM)[i].click()
        #print(f"Добавлен: {channels_to_add[i]}")

    # 3. Закрываем dropdown
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    # 4. Проверяем и удаляем через универсальный метод
    remaining = verify_and_remove(
        driver,
        menu_settings.ROW_CANALS_TEM,
        menu_settings.BUTTON_DELETE_CANAL_FOR_TEM,
        expected_before=len(channels_to_add)
    )

    return {
        'added': channels_to_add,
        'remaining': len(remaining)
    }


def add_languages(driver):
    """Добавление языков с использованием универсального метода"""
    #print("\n=== Добавление языков ===")

    # 1. Открываем dropdown языков
    lang_dropdown = common.wait_element(driver, menu_settings.ADD_LANGUAGE, condition='clickable')
    lang_dropdown.click()

    # 2. Сбрасываем "Все языки" если активно
    try:
        all_langs = common.wait_element(driver, menu_settings.ALL_LANGUAGE, condition='visible')
        if all_langs.is_selected():
            all_langs.click()
            #print(" - Сбросили выбор 'Все языки'")
    except Exception as e:
        print(f" - Не удалось сбросить 'Все языки': {str(e)}")

    # 3. Добавляем нужные языки
    languages_to_add = ["Русский", "Английский"]
    added_languages = []

    for lang in languages_to_add:
        element = common.scroll_to_find_element(
            driver,
            dropdown_locator=None,  # Dropdown уже открыт
            items_locator=menu_settings.CHECKBOX_LANGUAGE_ITEM,
            search_text=lang,
            timeout=15
        )

        if element:
            element.click()
            added_languages.append(lang)
            #print(f" - Добавлен язык: {lang}")

    # 4. Закрываем dropdown
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    # 5. Проверяем и удаляем один язык
    if added_languages:
        #print(" - Проверяем добавленные языки:")
        remaining = verify_and_remove(
            driver,
            menu_settings.ROW_LANGUAGE,
            menu_settings.LANGUAGE_DELETE,
            expected_before=len(added_languages))

        #print(f" - Осталось языков: {len(remaining)}")

    #print("=== Языки добавлены ===")
    return added_languages


def add_geography(driver: object) -> bool:
    """Добавление географии с использованием универсального поиска"""
    #print("\n=== Добавление географии ===")

    # 1. Добавляем страну (точное совпадение)
    #print(" - Добавляем страну 'Россия'")
    country = common.scroll_to_find_element(
        driver,
        dropdown_locator=menu_settings.GEOGRAPHY_EVENT,
        items_locator=menu_settings.ITEM_GEOGRAPHY,
        search_text="Россия",
        exact_match=True,
        timeout=20
    )

    if not country:
        print(" - Страна 'Россия' не найдена")
        return False

    country.click()
    common.wait_element(driver, menu_settings.ADD_GEOGRAPHY, condition='clickable').click()

    # 2. Добавляем регион
    #print(" - Добавляем регион 'Бенго' страны 'Ангола'")

    # Кликаем на поле ввода страны
    country_field = common.wait_element(driver, menu_settings.GEOGRAPHY_EVENT, condition='clickable')
    country_field.click()
    #print(" - Открыли список стран")

    # Для регионов сначала нужно выбрать страну
    #print(" - Выбираем страну для фильтрации регионов")
    country1 = common.scroll_to_find_element(
        driver,
        dropdown_locator=menu_settings.GEOGRAPHY_EVENT,
        items_locator=menu_settings.ITEM_GEOGRAPHY,
        search_text="Ангола",
        exact_match=True,
        timeout=20
    )
    if country1:
        country1.click()
        #print(" - Страна для регионов выбрана")
    else:
        print(" - Не удалось выбрать страну для регионов")
        return False

    # Кликаем на поле ввода региона
    region_field = common.wait_element(driver, menu_settings.GEOGRAPHY_EVENT_REGION, condition='clickable')
    region_field.click()
    #print(" - Открыли список регионов")

    # Ищем регион в списке
    region = common.scroll_to_find_element(
        driver,
        dropdown_locator=None,
        items_locator=menu_settings.ITEM_GEOGRAPHY,
        search_text="Бенго",
        timeout=20
    )

    if region:
        region.click()
        #print(" - Регион выбран")

        # Нажимаем кнопку "Добавить"
        add_button = common.wait_element(driver, menu_settings.ADD_GEOGRAPHY, condition='clickable')
        add_button.click()
        #print(" - Регион добавлен")
    else:
        print(" - Регион не найден")
        return False

    # 3. Проверяем и удаляем один элемент
    try:
        geo_items = common.wait_element(driver, menu_settings.ROW_GEOGRAPHY, condition='all_visible', timeout=10)
        if geo_items:
            #print(f" - Найдено элементов географии: {len(geo_items)}")

            # Удаляем первый элемент
            remaining = verify_and_remove(
                driver,
                menu_settings.ROW_GEOGRAPHY,
                menu_settings.DELETE_GEOGRAPHY,
                expected_before=len(geo_items)
            )

            #print(f" - Осталось элементов географии: {len(remaining)}")
    except Exception as e:
        print(f" - Ошибка при проверке географии: {str(e)}")
        return False

    #print("=== География успешно добавлена ===")
    return True


def add_keywords(driver, keywords="тест,пример,ключевое слово"):
    """Добавление ключевых слов с проверкой"""
    #print("\n=== Работа с ключевыми словами ===")

    # 1. Вводим ключевые слова
    kw_field = common.wait_element(driver, menu_settings.KEY_WORDS, condition='clickable')
    kw_field.clear()
    kw_field.send_keys(keywords)
    #print(f"1. Ввели ключевые слова: {keywords}")

    # 2. Добавляем
    common.wait_element(driver, menu_settings.KEY_WORDS_ADD, condition='clickable').click()

    # 3. Проверяем добавленные слова
    added_keywords = common.wait_element(driver, menu_settings.ROW_KEY_WORDS, condition='all_visible')

    # 4. Проверяем и удаляем
    if added_keywords:
        #print(f"2. Добавлено ключевых слов: {len(added_keywords)}")
        verify_and_remove(
            driver,
            menu_settings.ROW_KEY_WORDS,
            menu_settings.KEY_WORDS_DELETE,
            expected_before=len(added_keywords)
        )
    else:
        print("2. Ключевые слова не добавились")

    #print("=== Работа завершена ===")


def add_publication_sources(driver, sources):
    """Добавление источников публикаций (2 способа) с проверкой
    :param sources: добавит 3 источника, чередуя способы
                "https://t.me/direct1" - Будет добавлен напрямую
                "https://t.me/menu1"- Через меню
                "https://t.me/direct2" - Снова напрямую
    """
    #print("\n=== Работа с источниками публикаций ===")
    added_sources = []

    for i, source in enumerate(sources):
        try:
            # Чередуем способы добавления
            if i % 2 == 0:
                # Способ 1: Прямой ввод в инпут
                #print(f"{i + 1}. Добавляем напрямую: {source}")
                source_input = common.wait_element(driver, menu_settings.SOURCES, condition='clickable')
                source_input.clear()
                source_input.send_keys(source)
                source_input.send_keys(Keys.RETURN)
            else:
                # Способ 2: Через меню "Добавить канал"
                #print(f"{i + 1}. Добавляем через меню: {source}")
                channel = common.scroll_to_find_element(
                        driver,
                        menu_settings.SOURCES,
                        menu_settings.PUBLICATION_OPTION,
                        "Добавить канал"
                        )

                if channel:
                    channel.click()
                    #print(" - Нажали на кнопку Добавить канал")

                # Ждем появления модального окна
                link_input = common.wait_element(driver, menu_settings.LINK_CHANNEL, timeout=20, condition='visible')
                link_input.clear()
                link_input.send_keys(source)
                common.wait_element(driver, menu_settings.LINK_CHANNEL_ADD, condition='clickable').click()

            added_sources.append(source)
            #print(f"   Успешно добавлен: {source}")

        except Exception as e:
            print(f"Ошибка при добавлении источника {source}: {str(e)}")

    # Проверяем и удаляем один источник
    if added_sources:
        #print("Проверяем добавленные источники:")
        verify_and_remove(
            driver,
            menu_settings.ROW_SOURCES,
            menu_settings.LINK_CHANNEL_DELETE,
            expected_before=len(added_sources)
        )

    #print("=== Работа завершена ===")


def add_audience_to_thematic(driver, title, audience_text="Москвичи"):
    """Добавление аудитории к тематике с использованием универсального метода поиска"""
    #print(f"\n=== Добавление аудитории к тематике '{title}' ===")

    # 1. Находим и кликаем кнопку добавления аудитории
    audience_button = common.wait_element(
        driver,
        (By.XPATH,
         f"//span[text()='{title}']/ancestor::div[contains(@class,'ThematicsTable_Row')]//button[contains(@class,'PositionBox')]"),
        condition='clickable'
    )
    audience_button.click()
    #print(" - Кнопка добавления аудитории нажата")

    # 2. Используем универсальный метод для поиска аудитории "Москвичи"
    audience_element = common.scroll_to_find_element(
        driver,
        dropdown_locator=None,  # Dropdown уже открыт после клика
        items_locator=menu_settings.ELEMENT_CHECKBOX,
        search_text=audience_text,
        exact_match=True,
        timeout=20
    )

    if not audience_element:
        print(f" - Аудитория '{audience_text}' не найдена")
        return False

    # 3. Кликаем на найденный элемент аудитории
    audience_element.click()
    #print(f" - Аудитория '{audience_text}' выбрана")

    # 4. Проверяем, что аудитория добавилась
    audience_span = common.wait_element(
        driver,
        (By.XPATH,
         f"//span[text()='{title}']/ancestor::div[contains(@class,'ThematicsTable_Row')]//div[contains(@class,'ThematicsTable_Audience')]//span[@title]"),
        condition='visible'
    )

    current_audience = audience_span.get_attribute('title')
    if audience_text in current_audience:
        #print(f" - Проверка: аудитория '{audience_text}' успешно добавлена")
        return True

    print(f" - Ошибка: аудитория '{audience_text}' не добавилась. Текущая аудитория: {current_audience}")
    return False



def search_thematic(driver, title):
    """
    Поиск тематики в таблице
    :param driver: WebDriver
    :param title: Название тематики
    :return: None
    """
    #print(f"\nПоиск канала: '{title}'")

    # 1. Ожидаем поле поиска
    search_field = common.wait_element(driver, menu_settings.SEARCH_TEMS, timeout=20, condition='visible')
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


def create_thematic(driver, title, save=True, class_index=2):
    """
    Создание тематики с обязательными полями
    :param driver: WebDriver
    :param title: Название тематики
    :param save: Флаг сохранения (True - сохранить, False - отменить)
    :param class_index: Индекс класса
    :return: None
    """
    #print(f"\nСоздание тематики: '{title}' (save={save})")

    # Открываем форму
    common.wait_element(driver, menu_settings.ADD_TEM).click()

    # Заполняем обязательные поля
    fill_required_fields(driver, title, class_index)

    # Сохраняем или отменяем
    if save:
        common.wait_element(driver, menu_settings.SAVE_BUTTON_TEM, condition='clickable').click()
        #print(f"Тематика '{title}' сохранена")
    else:
        common.wait_element(driver, menu_settings.CANCEL_BUTTON_TEM, condition='clickable').click()
        #rint("Создание тематики отменено")


def edit_thematic(driver, old_title, new_title, new_class_index):
    """ Редактирование тематики
    :param driver: WebDriver
    :param old_title: Текущее название
    :param new_title: Новое название
    :param new_class_index: Индекс нового класса событий
    :return: None
    """
    #print(f"\nРедактирование тематики: '{old_title}' -> '{new_title}'")

    # Поиск и открытие тематики
    search_thematic(driver, old_title)
    common.wait_element(driver, (By.XPATH, f"//span[text()='{old_title}']")).click()

    # Изменение обязательных полей
    fill_required_fields(driver, new_title, new_class_index)

    #print("\n=== Заполнение необязательных полей ===")
    # Заполняем необязательные поля
    fill_optional_fields(driver)

    # Сохраняем изменения
    common.wait_element(driver, menu_settings.SAVE_BUTTON_TEM).click()


def delete_thematic(driver, title, confirm_deletion=True):
    """
    Удаление тематики
    :param driver: WebDriver
    :param title: Название тематики
    :param confirm_deletion: Флаг подтверждения (True - удалить, False - отменить)
    :return: bool - результат удаления
    """
    #print(f"\nУдаление тематики: '{title}' (confirm={confirm_deletion})")

    # 1. Поиск тематики в таблице
    if not search_thematic(driver, title):
        print(f"Тематика '{title}' не найдена в таблице")
        return False

    # 2. Формируем полный XPath до кнопки удаления
    full_delete_xpath = (
        f"//div[contains(@class, 'ThematicsTable_Row')][.//span[text()='{title}']]//div[contains(@class, 'PositionBox')]")


    # 3. Ожидаем и кликаем кнопку удаления
    try:
        # Сначала находим элемент без ожидания кликабельности
        delete_btn = common.wait_element(driver, (By.XPATH, full_delete_xpath), timeout=25)

        # Кликаем через JavaScript
        driver.execute_script("arguments[0].click();", delete_btn)
        #print("Кнопка удаления успешно нажата")
    except Exception as e:
        print(f"Ошибка при клике на кнопку удаления: {str(e)}")
        return False

    # 4. Обработка подтверждения
    if confirm_deletion:
        agree_btn = common.wait_element(driver, menu_settings.AGREE_ON_DELETE_TEM, timeout=10)
        if agree_btn:
            agree_btn.click()
            #print("Подтверждение удаления выполнено")
    else:
        cancel_btn = common.wait_element(driver, menu_settings.CANCEL_ON_DELETE_TEM, timeout=10)
        if cancel_btn:
            cancel_btn.click()
            #print("Удаление отменено")
            return True

    # 5. Проверка результата
    is_deleted = common.wait_element(driver, menu_settings.DELETE_TEM, timeout=90, condition='visible')

    #print(f"Результат удаления: {'успешно' if is_deleted else 'не удалось'}")
    return is_deleted