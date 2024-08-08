import os
from datetime import datetime
from time import sleep
from telebot import TeleBot
from telebot.storage import StateMemoryStorage
import selenium
from fake_useragent import FakeUserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging
from logging.handlers import RotatingFileHandler
from sys import platform
from dotenv import load_dotenv, find_dotenv

if platform != "win32":
    from webdriver_manager.chrome import ChromeDriverManager


if not find_dotenv():
    exit('Переменные окружения не загружены, т.к отсутствует файл .env')
else:
    load_dotenv()

DRIVER_PATH = os.getenv('DRIVER_PATH')
BOT_TOKEN = os.getenv("BOT_TOKEN")
YOUR_ID = os.getenv("YOUR_ID")
DUOLINGO_LOGIN = os.getenv("DUOLINGO_LOGIN")
DUOLINGO_PASSWORD = os.getenv("DUOLINGO_PASSWORD")


log_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(funcName)s - %(message)s')
my_handler = RotatingFileHandler("duo.log", mode='a', maxBytes=5 * 1024 * 1024,
                                 backupCount=1, encoding="utf8", delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
stream_handler.setLevel(logging.INFO)


app_log = logging.getLogger('duo_logger')
app_log.setLevel(logging.DEBUG)
app_log.addHandler(my_handler)
app_log.addHandler(stream_handler)


storage = StateMemoryStorage()
bot = TeleBot(token=BOT_TOKEN, state_storage=storage)
BASE_URL = 'https://www.duolingo.com/'
WORDS = {
    "рука": "hand",
    "бежит": "runs",
    "здесь": "here",
    "проблема": "problem",
    "теперь": "now",
    "сумка": "bag",
    "аэропорт": "airport",
    "такси": "taxi",
    "твой": "your",
    "паспорт": "passport",
    "его": "his",
    "жена": "wife",
    "пиджак": "jacket",
    "нет": "no",
    "большая": "big",
    "любимая": "love",
    "но": "but",
    "где": "where"
}
TOTAL_COUNT = 0


def main(lesson_number: int) -> str:
    global TOTAL_COUNT
    result_text = ""

    def click_button(xpath: str, timeout=10) -> None:
        """
        Функция для нажатия на кнопку
        :param browser: объект браузера
        :param timeout: время ожидания
        :param xpath: путь к кнопке
        :return: None
        """
        cur_button = WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        cur_button.click()

    glob_start_time = datetime.now()
    for _ in range(lesson_number):
        counter = 3
        while True:
            if 0 < counter < 3:
                app_log.warning(f"Внимание! Осталось {counter} попытки для запуска урока!")
            if counter == 0:
                app_log.critical(f"Внимание! Закончились попытки запуска урока!")
                return "Короче не, фраер, скрипт упал ("
            counter -= 1
            try:
                try:
                    app_log.debug("Провожу предварительную настройку...")
                    user_agent = FakeUserAgent().chrome
                    options = webdriver.ChromeOptions()
                    options.add_argument("--disable-infobars")
                    # options.add_argument("--headless=new")
                    options.add_argument("--incognito")
                    options.add_argument(f'--user-agent={user_agent}')
                    options.add_argument("start-maximized")
                    options.add_experimental_option("excludeSwitches", ["enable-automation"])
                    options.add_experimental_option('useAutomationExtension', False)
                    options.add_argument('log-level=3')
                    options.add_experimental_option('excludeSwitches', ['enable-logging'])
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')
                    app_log.info("Открываю браузер...")
                    if platform == "win32":
                        browser = webdriver.Chrome(service=Service(executable_path=DRIVER_PATH),
                                                   options=options)
                    else:
                        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

                except Exception as ex:
                    app_log.error("Какие-то ошибки на старте!", ex)
                    continue
                try:
                    app_log.info("Открываю страницу...")
                    browser.set_page_load_timeout(10)
                    try:
                        browser.get("https://www.duolingo.com/?isLoggingIn=true")
                    except Exception:
                        app_log.error("Не удается открыть страницу авторизации, вторая попытка...")
                except selenium.common.exceptions.WebDriverException:
                    browser.get(BASE_URL)
                app_log.info("Авторизация...")
                click_button('//*[@id="root"]/div[1]/header/div[2]/div[2]/div/button', 10)
                input_login = WebDriverWait(browser, 100).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="web-ui1"]')))

                input_login.send_keys(DUOLINGO_LOGIN)

                input_pass = WebDriverWait(browser, 2).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="web-ui2"]')))

                input_pass.send_keys(DUOLINGO_PASSWORD)

                click_button('//*[@id="overlays"]/div[3]/div/div/form/div[1]/button')
                try:
                    click_button('/html/body/div[6]/div[2]/div[1]/div[2]/div[2]/button[1]', 2)
                except Exception:
                    pass
                try:
                    except_auth = WebDriverWait(browser, 2).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        f'/html/body/div[2]/div[3]/div/div/form/div[1]/div[2]/div'))
                    )
                    sleep(3)
                    click_button('/html/body/div[2]/div[3]/div/div/form/div[1]/button', 2)
                    sleep(2)
                    app_log.warning("Не получилось войти в аккаунт с первого раза!")
                    input_login = WebDriverWait(browser, 100).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="web-ui1"]')))

                    input_login.send_keys(DUOLINGO_LOGIN)
                    # 2  1 16
                    input_pass = WebDriverWait(browser, 2).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="web-ui2"]')))

                    input_pass.send_keys(DUOLINGO_PASSWORD)

                    click_button('/html/body/div[2]/div[3]/div/div/form/div[1]/button')

                except Exception:
                    pass
                app_log.info("Успешно! Начинаю майнинг очков...")
                try:
                    start_time = datetime.now()

                    browser.set_page_load_timeout(100)
                    try:
                        browser.get("https://www.duolingo.com/lesson/unit/6/level/2")
                        app_log.info("Урок успешно загружен!")
                    except Exception:
                        app_log.warning("Превышен таймаут!")
                    sleep(4)

                    click_button('//*[@id="root"]/div[1]/div/div/div/div[3]/button')
                    sleep(1)
                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    sleep(4)

                    app_log.debug("1 этап - где мой паспорт")

                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    sleep(4)
                    for i in range(1, 4):
                        cur_button = WebDriverWait(browser, 2).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="root"]/div[1]/div/div/div[1]/div[1]'
                                                            f'/div[5]/div/ul/li[{i}]/button'))
                        )
                        if cur_button.text == "Where is my passport":
                            cur_button.click()
                            break

                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div[2]/div/button')
                    sleep(2)

                    app_log.debug("2 этап - поиски")

                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    sleep(2)
                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    sleep(2)

                    app_log.debug("3 этап - выбор чекбокса 'Да, это правда'")

                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    for i in range(1, 3):
                        cur_button = WebDriverWait(browser, 2).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="root"]/div[1]/div/div/div[1]'
                                                            f'/div[1]/div[10]/div/ul/li[{i}]/button'))
                        )
                        cur_text = WebDriverWait(browser, 2).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="root"]/div[1]/div/div/div[1]/div[1]/'
                                                            f'div[10]/div/ul/li[{i}]/div/div/span'))
                        )
                        if cur_text.text == "Да, это правда.":
                            cur_button.click()
                            break

                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div[2]/div/button', 3)
                    sleep(1)

                    app_log.debug("4 этап - выбор варианта 'бежит'")

                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    sleep(3)
                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    sleep(2)
                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')

                    for i in range(1, 8, 2):
                        cur_button = WebDriverWait(browser, 2).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="root"]/div[1]/div/div/div[1]/div[1]/div[14]/div/'
                                                            f'div[2]/div/span[{i}]/span/button'))
                        )
                        cur_text = WebDriverWait(browser, 2).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="root"]/div[1]/div/div/div[1]/div[1]/'
                                                            f'div[14]/div/div[2]/div/span[{i}]/span/button/span[2]/span'))
                        )
                        if cur_text.text == "runs":
                            cur_button.click()
                            break

                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div[2]/div/button')
                    sleep(1)

                    app_log.debug("5 этап - разговоры")

                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    sleep(2)
                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    sleep(4)
                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    sleep(2)
                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    sleep(1)
                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    sleep(4)
                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    sleep(5)
                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')

                    app_log.debug("6 этап - выбор варианта 'рука'")

                    for i in range(1, 6, 2):
                        cur_button = WebDriverWait(browser, 2).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="root"]/div[1]/div/div/div[1]/div[1]/div[22]/'
                                                            f'div/div[2]/div/span[{i}]/span/button'))
                        )
                        cur_text = WebDriverWait(browser, 2).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="root"]/div[1]/div/div/div[1]/div[1]/div[22]/'
                                                            f'div/div[2]/div/span[{i}]/span/button/span[2]/span'))
                        )
                        if cur_text.text == "hand":
                            cur_button.click()
                            break

                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    sleep(2)

                    app_log.debug("7 этап - выбор варианта 'У него в руке'")

                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                    sleep(2)
                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')

                    for i in range(1, 4):
                        cur_button = WebDriverWait(browser, 2).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="root"]/div[1]/div/div/div[1]/'
                                                            f'div[1]/div[25]/div/ul/li[{i}]/button'))
                        )
                        cur_text = WebDriverWait(browser, 2).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="root"]/div[1]/div/div/div[1]/div[1]/'
                                                            f'div[25]/div/ul/li[{i}]/div/div/span'))
                        )
                        if cur_text.text == "У него в руке.":
                            cur_button.click()
                            break

                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div[2]/div/button')
                    sleep(1)

                    app_log.debug("8 этап (заключительный) - сопоставление слов.")

                    is_not_work = False
                    # Теперь слова
                    for i in range(1, 6):
                        cur_button_1 = WebDriverWait(browser, 2).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="root"]/div[1]/div/div/div[1]/div[1]/div[26]/div/'
                                                            f'div[2]/div/ul[1]/li[{i}]/span/button'))
                        )
                        cur_text_1 = WebDriverWait(browser, 2).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            f'//*[@id="root"]/div[1]/div/div/div[1]/div[1]/div[26]/div/'
                                                            f'div[2]/div/ul[1]/li[{i}]/span/button/span[3]/span[1]'))
                        )
                        if cur_text_1.text in WORDS.keys():
                            for j in range(1, 6):
                                cur_button_2 = WebDriverWait(browser, 2).until(
                                    EC.presence_of_element_located((By.XPATH,
                                                                    f'//*[@id="root"]/div[1]/div/div/div[1]/div[1]/'
                                                                    f'div[26]/div/div[2]/div/ul[2]/li[{j}]/span/button'))
                                )
                                cur_text_2 = WebDriverWait(browser, 2).until(
                                    EC.presence_of_element_located((By.XPATH,
                                                                    f'//*[@id="root"]/div[1]/div/div/div[1]/div[1]/div[26]/div/'
                                                                    f'div[2]/div/ul[2]/li[{j}]/span/button/span[3]/span[1]'))
                                )
                                if WORDS[cur_text_1.text] == cur_text_2.text:
                                    cur_button_1.click()
                                    cur_button_2.click()
                                    break
                        else:
                            app_log.warning("WARNING! Нет слова {cur_text_1.text} в словаре!")
                            is_not_work = True
                    if is_not_work:
                        # browser.close()
                        continue

                    click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div[2]/div/button')
                    sleep(4)
                    click_button('//*[@id="root"]/div[1]/div/div/div[2]/div/div/div/button')
                    app_log.info("+5 очков!")
                    TOTAL_COUNT += 5
                    # browser.close()
                    stop_time = datetime.now()
                    total_time = stop_time - start_time
                    app_log.info(f"Прошел урок за {round(total_time.seconds, 2)} секунд")
                except Exception as ex:
                    app_log.error(f"ERROR! Что-то пошло не так в процессе прохождения урока!\n{ex}")
                    continue
                finally:
                    browser.close()
            except Exception as ex:
                app_log.critical(f"CRITICAL ERROR! Пинг упал до критического значения!\n{ex}")
                continue
            finally:
                app_log.info("Закрываю браузер...")
                try:
                    browser.close()
                except Exception:
                    pass
                finally:
                    if platform == "win32":
                        app_log.debug("Очистка Chrome и Chromedriver...")
                        os.system("taskkill /f /IM chrome.exe >nul 2>&1")
                        os.system("taskkill /f /IM chromedriver.exe >nul 2>&1")
            break
        app_log.info(f"{_ + 1} урок пройден!\n")
    glob_stop_time = datetime.now()
    if platform == "win32":
        os.system("taskkill /f /IM chrome.exe >nul 2>&1")
        os.system("taskkill /f /IM chromedriver.exe >nul 2>&1")
    glob_time = glob_stop_time - glob_start_time
    result_text += (f"Программа завершила свою работу успешно. Было пройдено {lesson_number} урок (-ов).\n"
                    f"Время работы: {round(glob_time.seconds, 2) // 60} минут\n"
                    f"Всего заработал: {TOTAL_COUNT} очков\n")
    app_log.info("\n\n=============================================================================\n\n" +
                 result_text + "\n\n")
    return result_text


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1].isdigit() and int:
        text = main(int(sys.argv[1]))
        bot.send_message(YOUR_ID, text)
    else:
        while True:
            today = datetime.now()
            if today.hour in (8, 9):
                if today.hour == 9 and today.minute == 0:
                    text = main(15)
                    bot.send_message(YOUR_ID, text)
                    sleep(60 * 60 * 15)
                else:
                    sleep(60)
            else:
                sleep(60 * 60)
    os.system("pause") if platform == "win32" else os.system("read -n1 -r -p 'Press any key to continue...' key")
