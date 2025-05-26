import pytest
import random

from selenium.webdriver.common.by import By
from fixture.conftest import browser_setup2
from Metods import add_tems, common
from Locators import menu_settings


@pytest.mark.usefixtures("browser_setup2")
def test_add_thematic(browser_setup2):
    driver = browser_setup2
    original_title = f"Тест {random.randint(100, 999)}"
    new_title = f"Обновленная {original_title}"

    # 1. Переход в раздел тематик
    add_tems.navigate_to_tems(driver)
    print("\n=== 1. Переход на страницу тематики успешно завершен ===")

    # 2. Создание тематики (с отменой)
    add_tems.create_thematic(driver, original_title, save=False)
    print("\n=== 2. Отменили создание тематики ===")

    # 3. Создание тематики (сохранение)
    add_tems.create_thematic(driver, original_title, class_index=5)
    add_tems.search_thematic(driver, original_title)
    assert common.wait_element(driver, (By.XPATH, f"//span[text()='{original_title}']")), "Тематика не создана"
    print(f"\n=== 3. Тематика {original_title} создана ===")

    # 4. Редактирование
    add_tems.edit_thematic(driver, original_title, new_title, new_class_index=8)
    common.wait_element(driver, menu_settings.SEARCH_TEMS, timeout=20, condition='visible')
    add_tems.search_thematic(driver, new_title)
    assert common.wait_element(driver, (By.XPATH, f"//span[text()='{new_title}']")), "Изменения не сохранились"
    print(f"\n=== 4. Тематика {new_title} отредактирована ===")

    # 5. Добавление аудитории к тематике
    assert add_tems.add_audience_to_thematic(driver, new_title), "Не удалось добавить аудиторию"
    print(f"\n=== 5. Аудитории тематики {new_title} добавлены ===")

    # 6. Удаление (с отменой)
    add_tems.delete_thematic(driver, new_title, confirm_deletion=False)
    print(f"\n=== 5. Удаление тематики {new_title} отменено ===")

    # 7. Фактическое удаление
    assert add_tems.delete_thematic(driver, new_title), "Тематика не была удалена"
    print(f"\n=== 6. Тематика {new_title} удалена ===")

    print("\n=== Тест успешно завершен ===")


@pytest.mark.usefixtures("browser_setup2")
def test_thematic_lifecycle(browser_setup2):
    driver = browser_setup2
    original_title = "Тест 453"
    new_title = "Обновленная Тест 175"

    # 1. Переход в раздел тематик
    add_tems.navigate_to_tems(driver)
    print("\n=== 1. Переход на страницу тематики успешно завершен ===")

    # 7. Фактическое удаление
    assert add_tems.delete_thematic(driver, new_title), "Тематика не была удалена"
    print(f"\n=== 6. Тематика {new_title} удалена ===")