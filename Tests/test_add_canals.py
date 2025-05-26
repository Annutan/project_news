import pytest
import random
from fixture.conftest import browser_setup2
from Metods import add_canals


@pytest.mark.usefixtures("browser_setup2")
def test_canal_workflow(browser_setup2):
    driver = browser_setup2
    # Генерируем уникальное имя для теста
    base_name = f"TestChannel {random.randint(100, 999)}"
    telegram_link1 = "https://t.me/testchannel1"
    #telegram_link2 = "https://t.me/testchannel2"

    print("\n=== Начало теста: полный цикл работы с каналами ===")

    # 1. Авторизация и переход в раздел Каналы
    #print("\nШаг 1: Переход в раздел Каналы")
    add_canals.navigate_to_canals(driver)

    # 2. Создание канала с типом "Telegram". Тип "внутренний" временно не работает
    #print("\nШаг 2: Создание Telegram канала")
    assert add_canals.create_and_verify_canal(
        driver,
        base_name,
        canal_type='Telegram',  # Тип меняем на Telegram
        telegram_link=telegram_link1  # Идентификатор
    ), "Ошибка редактирования канала"

    # 3. Редактирование канала
    #print("\nШаг 3: Редактирование канала")
    updated_name = f"Updated {base_name}"
    assert add_canals.edit_canal(driver, base_name, updated_name, new_type='Внутренний'), "Ошибка создания Telegram канала"

    # 4. Попытка удаления с отменой
    #print("\nШаг 4: Пробное удаление (с отменой)")
    assert add_canals.delete_canal(driver, updated_name, confirm_deletion=False), "Ошибка при отмене удаления"

    # 5. Фактическое удаление
    #print("\nШаг 5: Фактическое удаление канала")
    assert add_canals.delete_canal(driver, updated_name), "Ошибка при удалении"

    print("\n=== Тест успешно завершен ===")