from selenium.webdriver.common.by import By

#Подстраницы
TEMS = (By.XPATH,"//button[text()='Тематики']")
CANAL = (By.XPATH,"//button[text()='Каналы']")
AUDITOR = (By.XPATH,"//button[text()='Аудитории']")

#Подстраница "Аудитории"
ADD_AUDITORE = (By.XPATH,"//button[text()='Добавить аудиторию']")

# Форма добавления аудитории
TITLE_AUDITORE = (By.XPATH,"//input[@placeholder='Аудитория 1' or @name='name']")
INDICATORS_ADD = (By.XPATH,"//input[@placeholder='Добавьте сущности' or @name='indicators']")
GREEN_BUTTON = (By.XPATH,"//button[contains(@class, 'green')]")
RED_BUTTON = (By.XPATH,"//button[contains(@class, 'red')]")
POSITIVE_INDICATOR = (By.XPATH, "//div[contains(@class, 'positive')]//span[contains(text(), '{text}')]")
NEGATIVE_INDICATOR = (By.XPATH, "//div[contains(@class, 'negative')]//span[contains(text(), '{text}')]")
INDICATOR = (By.XPATH, "//div[contains(@class, 'item_positive') or contains(@class, 'item_negative')]//span[text()='{text}']")
DELETE_BUTTON_INDICATOR = (By.XPATH, "//*[contains(@class, 'item_positive')]/button")
POLITICAL_BUTTONS = (By.XPATH, "//div[contains(@class, 'AudienceOrientation_orientation__option_')]")
SAVE_BUTTON = (By.XPATH, "//button[text()='Сохранить']")
CANCEL_BUTTON = (By.XPATH, "//button[text()='Отмена']")
SEARCH = (By.XPATH, "//input[@placeholder='Поиск по аудиториям']")
SEARCH_ON_TABLE = (By.XPATH, "//a[text()='{title}']")
DELETE_BUTTON_AUDITORE = (By.XPATH, "//div[.//button[normalize-space()='{new_title}']]//button[contains(@class, '_deleteBtn_')]")
AGREE_ON_DELETE_AUDITORE = (By.XPATH, "//button[text()= 'Да']")


#Подстраница "Каналы"
ADD_CANAL = (By.XPATH,"//button[text()='Добавить канал']")

# Форма добавления канала
TITLE_CANAL = (By.XPATH,"//input[@name='name']")
TYPE_CANAL = (By.XPATH, "//div[@role='combobox']")
TELEGRAM_TYPE = (By.XPATH, "//div[text()='Telegram']")
INTERNAL_TYPE = (By.XPATH, "//div[text()='Внутренний']")
IDENTIFIER = (By.XPATH, "//input[@name='address']")
ADD_BUTTON = (By.XPATH, "//button[text()='Добавить']")
CANCEL_BUTTON_CANAL = (By.XPATH, "//button[text()='Отмена']")
SEARCH_CANALS = (By.XPATH, "//input[@placeholder='Поиск по каналам']")
SEARCH_ON_TABLE_CANALS = (By.XPATH, "//span[text()='{title}']")
DELETE_BUTTON_CANAL = (By.XPATH, "//span[text()='{new_title}']/ancestor::div[contains(@class,'TableBody')]/descendant::div[contains(@class,'Trash')]")
AGREE_ON_DELETE_CANAL = (By.XPATH, "//button[text()= 'Да']")
NOT_AGREE_ON_DELETE_CANAL = (By.XPATH, "//button[text()= 'Отмена']")


#Подстраница "Тематики"
ADD_TEM = (By.XPATH,"//button[text()='Добавить тематику']")

# Форма добавления аудитории
TITLE_TEM = (By.XPATH,"//input[@placeholder='Выборы в США' or @name='name']")
ADD_CLASS = (By.XPATH,"//input[@placeholder='Выбор класса']")
EVENT = (By.XPATH, "//div[contains(@class, 'mantine-Select-dropdown')]")
EVENT_CLASS = (By.XPATH, "//div[contains(@class, 'mantine-Select-item')]")
CANAL_FOR_TEM = (By.XPATH,"//div[contains(@class,'mantine-Input-wrapper mantine-MultiSelect-wrapper mantine')]")
# несколько элементов в одном, можно выбрать несколько каналов
CANALS_TEM = (By.XPATH,"//div[contains(@class,'mantine-MultiSelect-item')]")
ROW_CANALS_TEM = (By.XPATH,"//div[@data-onboarding='keywords:telegram-channel-select']//div[contains(@class, 'Chips_chip_')]")
BUTTON_DELETE_CANAL_FOR_TEM = (By.XPATH,"//div[contains(@class,'Chips_chip')]//button")
ADD_LANGUAGE = (By.XPATH,"//button[contains(@class, 'LanguageInput_Anchor')]")
# Чекбокс из нескольких элементов
CHECKBOX_LANGUAGE = (By.XPATH,"//div[@id='radix-:r8:']")
CHECKBOX_LANGUAGE_ITEM = (By.XPATH,"//div[contains(@class,'LanguageInput_Popover__item_')]")
ALL_LANGUAGE = (By.XPATH,"//input[@id='language-all']")
ROW_LANGUAGE = (By.XPATH,"//div[contains(@class, 'LanguageInput_Chips')]//div")
LANGUAGE_DELETE = (By.XPATH,"//div[contains(@class,'LanguageInput_Chips')]//button")     # несколько элеменетов
GEOGRAPHY_EVENT = (By.XPATH,"//input[@placeholder='Выбор страны']")
DROPDOWN_LIST_GEOGRAPHY = (By.XPATH,"//div[contains(@class, 'mantine-Select-itemsWrapper')]")
ITEM_GEOGRAPHY = (By.XPATH,"//div[contains(@class, 'mantine-Select-item')]")
GEOGRAPHY_EVENT_REGION = (By.XPATH,"//input[@placeholder='Выбор региона']")
DROPDOWN_LIST_REGION = (By.XPATH,"//div[contains(@class, 'mantine-Select-itemsWrapper')]")
ADD_GEOGRAPHY = (By.XPATH,"//div[contains(@class, 'GeographyInput_GeographyInput_')]//button")
ROW_GEOGRAPHY = (By.XPATH,"//div[contains(@class, 'GeographyInput_GeographyInput__values_')]/div")
DELETE_GEOGRAPHY = (By.XPATH,"//div[contains(@class, 'GeographyInput_GeographyInput__values_')]//button")
KEY_WORDS = (By.XPATH,"//input[contains(@placeholder,'Введите или вставьте ключевые слова')]")
KEY_WORDS_ADD = (By.XPATH,"//div[contains(@class,'ThematicForm_AddKeyWord')]/button")
ROW_KEY_WORDS = (By.XPATH,"//div[@data-onboarding='keywords:keywords-input']//div[contains(@class, 'ThematicForm_ItemKey_')]")
# кнопок удаления ключевых фраз может быть несколько
KEY_WORDS_DELETE = (By.XPATH,"//div[@data-onboarding='keywords:keywords-input']//*[local-name()='path']")
SOURCES = (By.XPATH,"//input[contains(@class, 'PublicationSourceInput_Input')]")
PUBLICATION_OPTION = (By.XPATH, "//span[text()='Добавить канал']")
PUBLICATION_OPTION_ITEM = (By.XPATH, "//div[contains(@class, 'PublicationSourceInput_Item_')]")
LINK_CHANNEL = (By.XPATH,"//input[@placeholder='t.me/NAME']")
LINK_CHANNEL_ADD = (By.XPATH, "//button[contains(@class,'AddChannelModal_Button')]")
ROW_SOURCES = (By.XPATH, "//div[@data-onboarding='keywords:sources-input']//div[contains(@class, 'ThematicForm_ItemKey')]")
LINK_CHANNEL_DELETE = (By.XPATH, "//div[@data-onboarding='keywords:sources-input']//*[local-name()='path']")
SAVE_BUTTON_TEM = (By.XPATH, "//button[text()='Сохранить']")
CANCEL_BUTTON_TEM = (By.XPATH, "//button[text()='Отмена']")
SEARCH_TEMS = (By.XPATH, "//input[@placeholder='Поиск по тематикам']")
SEARCH_ON_TABLE_TEM = (By.XPATH, "//a[text()='{title}']")
ADD_AUDITORE_ON_TEM = (By.XPATH, "//div[contains(@class, 'ThematicsTable_Row')][.//span[text()='{title}']]//button[contains(@class, 'ThematicsTable_PositionBox_')]")
ELEMENT_CHECKBOX = (By.XPATH, "//div[contains(@class, 'ThematicAudiencePopover_audiencePopover__item')]")
# Отмеченные элементы чекбокса отобразятся в title
AUDITORE_ON_TEM = (By.XPATH, "//div[contains(@class, 'ThematicsTable_Row')][.//span[text()='{title}']]//div[contains(@class, 'ThematicsTable_Audience')]//span[@title]")
DELETE_BUTTON_TEM = (By.XPATH, "//div[contains(@class, 'ThematicsTable_Row')][.//span[text()='{new_title}']]//div[contains(@class, 'PositionBox')]")
AGREE_ON_DELETE_TEM = (By.XPATH, "//button[text()= 'Да']")
CANCEL_ON_DELETE_TEM = (By.XPATH, "//button[text()= 'Отмена']")
DELETE_TEM = (By.XPATH, "//div[@class='go2072408551']//div[text()='Тематика удалена']")