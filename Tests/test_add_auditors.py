import pytest
import random
from Locators import menu_settings
from fixture.conftest import browser_setup2
from Metods import common, add_auditors


@pytest.mark.usefixtures("browser_setup2")
def test_audience_creation(browser_setup2):
    """ Тест для добавления новой аудитории """
    driver = browser_setup2
    print('\n== Тест "Создание новой аудитории" ==')

    # 1. Авторизация и переход на страницу Аудитории
    add_auditors.navigate_to_audiences(driver)

    # 2. Переход в подраздел "Добавить аудиторию"
    add_auditor_btn = common.wait_element(driver, menu_settings.ADD_AUDITORE, timeout=30, condition='clickable')
    driver.execute_script("arguments[0].click();", add_auditor_btn)

    # 3. Проверка загрузки страницы
    title_auditore = common.wait_element(driver, menu_settings.SAVE_BUTTON, condition='visible')
    assert title_auditore.text == "Сохранить", f"Неверный текст элемента: {title_auditore.text}"

    # 4. Добавление новой Аудитории
    original_name = f"Тестовая аудитория {random.randint(1, 1000)}"
    add_auditors.create_and_verify_audience(driver, original_name)

    # 5. Редактируем аудиторию
    new_name = f"Обновленная {original_name}"
    add_auditors.edit_audience(driver, original_name, new_name, [
        {'text': 'Новый индикатор 1', 'type': 'green'},
        {'text': 'Новый индикатор 2', 'type': 'red'}
    ])

    # 6. Вариант 1 - удаляем аудиторию
    add_auditors.delete_audience(driver, new_name)

    # Или вариант 2 - сохраняем название для другого теста
    # saved_name = delete_audience(driver, new_name, should_delete=False)
    # print(f"Сохраненное название для следующего теста: {saved_name}")