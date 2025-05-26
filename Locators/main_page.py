from selenium.webdriver.common.by import By

PICTURE_DAY = (By.XPATH,"//span[text()='Картина дня за ']")

#основная навигация
MENU_DAY_PICTURE = (By.XPATH, "//div[contains(@class, 'Header_Navigation')]//span[text()='Картина дня']")
MENU_REPORT = (By.XPATH, "//div[contains(@class, 'Header_Navigation')]//span[text()='Отчет']")
MENU_SETTINGS = (By.XPATH, "//div[contains(@class, 'Header_Navigation')]//span[text()='Настройки']")


HELP_BUTTON = (By.XPATH, "//div[contains(@class, 'Header_Question')]")             # кнопка помощь (?)
HELP_SCHEMA = (By.XPATH, "//div[contains(@class, 'UserOnboarding_Item')]")         # описание. схема
PAGINATION_CONTAINER = (By.XPATH, "//div[contains(@class, 'UserOnboarding_StepControls')]")    #контейнер пагинаций
PAGINATION_DOTS = (By.XPATH, "//div[contains(@class, 'UserOnboarding_StepControls')]/div[contains(@class, 'UserOnboarding_StepDot')]")
# пагинация в функциональности помощи