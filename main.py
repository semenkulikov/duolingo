import os
from datetime import datetime
from time import sleep
from telebot import TeleBot
from telebot.storage import StateMemoryStorage
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
import random
from selenium.webdriver.common.action_chains import ActionChains

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
my_handler = RotatingFileHandler("duo.log", mode='a', maxBytes=2 * 1024 * 1024,
                                 backupCount=1, encoding="utf8", delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
stream_handler.setLevel(logging.DEBUG)


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
SLEEP_SEC_COUNT = 0  # Общий уровень скорости программы. 0 - самый быстрый, 1 - более менее,
# 2 - средний, 3 - медленный, и так далее

def human_like_behavior(driver):
    action = ActionChains(driver)
    app_log.info("Начинаю имитацию действий пользователя.")

    def move_mouse_randomly():
        app_log.debug("Имитирую движения курсора мыши...")
        for _ in range(random.randint(5, 20)):
            x = random.randint(1 * _, 10 * _)
            y = random.randint(2 * _, 10 * _)
            try:
                action.move_by_offset(x, y).perform()
            except Exception:
                app_log.debug(f"По координатам x={x} y={y} не удалось переместить курсор!")
            sleep(random.uniform(0.5, 1.5))

    # def random_click():
    #     app_log.debug("Имитирую рандомные клики...")
    #     elements = WebDriverWait(driver, 100).until(
    #             EC.presence_of_element_located((By.XPATH, '//*')))
    #     random.choice(elements)
    #     sleep(random.uniform(0.5, 1.5))

    def random_scroll():
        app_log.debug("Имитирую рандомные прокрутки страницы...")
        for _ in range(random.randint(1, 3)):
            scroll_value = random.randint(-300, 300)
            driver.execute_script(f"window.scrollBy(0, {scroll_value});")
            sleep(random.uniform(0.5, 1.5))

    def type_text(element, text):
        app_log.debug("Имитирую ввод текста в поле...")
        for char in text:
            element.send_keys(char)
            sleep(random.uniform(0.1, 0.3))

    # Имитируем поведение
    move_mouse_randomly()
    # random_click()
    random_scroll()

    # # Пример ввода текста в поле поиска (замените на ваше)
    # search_box = driver.find_element_by_name("q")  # Убедитесь, что элемент существует на странице
    # type_text(search_box, "Selenium human-like behavior")



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

    def check_authorization() -> None:
        """
        Функция для авторизации на сайте
        """
        app_log.info("Открываю страницу...")
        browser.set_page_load_timeout(10)
        try:
            browser.get("https://www.duolingo.com/?isLoggingIn=true")
        except Exception:
            app_log.warning("Возникли проблемы с открытием страницы авторизации!")
            # continue

        app_log.info("Авторизация...")
        # Нажимаю на У меня есть аккаунт.
        click_button('/html/body/div[1]/div[1]/header/div[2]/div[2]/div/button', 20)

        # Имитирую действия настоящего юзера
        human_like_behavior(browser)
        while True:
            input_login = WebDriverWait(browser, 100).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="web-ui1"]')))

            input_login.send_keys(DUOLINGO_LOGIN)
            sleep(2)
            # 2  1 16
            input_pass = WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="web-ui2"]')))

            input_pass.send_keys(DUOLINGO_PASSWORD)

            click_button('/html/body/div[2]/div[3]/div/div/form/div[1]/button')
            sleep(5)
            try:
                # Находим элемент Не получилось войти с первого раза
                except_auth = WebDriverWait(browser, 2).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    f'/html/body/div[2]/div[3]/div/div/form/div[1]/div[2]/div'))
                )
                sleep(2)
                if except_auth.text == "Неверный пароль. Повторите попытку.":
                    app_log.warning("Авторизация не прошла!")
                    browser.get("https://www.duolingo.com/?isLoggingIn=true")
                    sleep(2)
                    click_button('/html/body/div[1]/div[1]/header/div[2]/div[2]/div/button', 10)
                else:
                    break
            except Exception:
                break

    glob_start_time = datetime.now()
    try:
        app_log.debug("Провожу предварительную настройку...")
        user_agent = FakeUserAgent().chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        # options.add_argument("--headless=new")
        # options.add_argument("--incognito")
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
        exit("Не запустился браузер!")

    check_authorization()
    counter = 0
    while counter < lesson_number:
        try:
            app_log.info("Успешно! Начинаю майнинг очков...")
            try:
                start_time = datetime.now()

                browser.set_page_load_timeout(200)
                try:
                    browser.get("https://www.duolingo.com/lesson/unit/6/level/2")
                    app_log.info("Урок успешно загружен!")
                except Exception:
                    app_log.warning("Превышен таймаут!")
                sleep(4 + SLEEP_SEC_COUNT)

                app_log.debug("Нажимаю 'Начать историю'")
                click_button('//*[@id="root"]/div[1]/div/div/div/div[3]/button')
                sleep(1 + SLEEP_SEC_COUNT)
                app_log.debug("0 этап - запуск урока")
                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                sleep(4 + SLEEP_SEC_COUNT)

                app_log.debug("1 этап - где мой паспорт")

                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                sleep(4 + SLEEP_SEC_COUNT)
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
                sleep(2 + SLEEP_SEC_COUNT)

                app_log.debug("2 этап - поиски")

                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                sleep(2 + SLEEP_SEC_COUNT)
                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                sleep(2 + SLEEP_SEC_COUNT)

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
                sleep(1 + SLEEP_SEC_COUNT)

                app_log.debug("4 этап - выбор варианта 'бежит'")

                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                sleep(3 + SLEEP_SEC_COUNT)
                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                sleep(2 + SLEEP_SEC_COUNT)
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
                        sleep(SLEEP_SEC_COUNT)
                        break

                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div[2]/div/button')
                sleep(1 + SLEEP_SEC_COUNT)

                app_log.debug("5 этап - разговоры")

                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                sleep(2 + SLEEP_SEC_COUNT)
                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                sleep(4 + SLEEP_SEC_COUNT)
                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                sleep(2 + SLEEP_SEC_COUNT)
                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                sleep(1 + SLEEP_SEC_COUNT)
                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                sleep(4 + SLEEP_SEC_COUNT)
                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                sleep(5 + SLEEP_SEC_COUNT)
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
                        sleep(SLEEP_SEC_COUNT)
                        break

                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                sleep(2 + SLEEP_SEC_COUNT)

                app_log.debug("7 этап - выбор варианта 'У него в руке'")

                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div/div/button')
                sleep(2 + SLEEP_SEC_COUNT)
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
                        sleep(SLEEP_SEC_COUNT)
                        break

                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div[2]/div/button')
                sleep(1 + SLEEP_SEC_COUNT)

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
                                sleep(SLEEP_SEC_COUNT)
                                cur_button_2.click()
                                sleep(SLEEP_SEC_COUNT)
                                break
                    else:
                        app_log.warning(f"WARNING! Нет слова {cur_text_1.text} в словаре!")
                        is_not_work = True
                if is_not_work:
                    # browser.close()
                    continue

                click_button('//*[@id="root"]/div[1]/div/div/div[3]/div/div[2]/div/button')
                app_log.debug("8 этап - закончен")
                sleep(4 + SLEEP_SEC_COUNT)
                click_button('//*[@id="root"]/div[1]/div/div/div[2]/div/div/div/button')
                # click_button('//*[@id="root"]/div[1]/div/div/div[2]/div/div/div/button')
                # click_button('//*[@id="root"]/div[1]/div/div/div[2]/div/div/div/button')
                app_log.info("+5 очков!")
                TOTAL_COUNT += 5
                # browser.close()
                stop_time = datetime.now()
                total_time = stop_time - start_time
                app_log.info(f"Прошел урок за {round(total_time.seconds, 2)} секунд")
            except Exception as ex:
                app_log.error(f"ERROR! Что-то пошло не так в процессе прохождения урока!\n{ex}")
                continue
            # finally:
            #     browser.close()
        except Exception as ex:
            app_log.critical(f"CRITICAL ERROR! Пинг упал до критического значения!\n{ex}")
            TOTAL_COUNT += 1
            continue
        # finally:
        #     app_log.info("Закрываю браузер...")
        #     try:
        #         browser.close()
        #     except Exception:
        #         pass
        #     finally:
        #         if platform == "win32":
        #             app_log.debug("Очистка Chrome и Chromedriver...")
        #             os.system("taskkill /f /IM chrome.exe >nul 2>&1")
        #             os.system("taskkill /f /IM chromedriver.exe >nul 2>&1")
        app_log.info(f"{counter + 1} урок пройден!\n")
        counter += 1
    glob_stop_time = datetime.now()
    if platform == "win32":
        os.system("taskkill /f /IM chrome.exe >nul 2>&1")
        os.system("taskkill /f /IM chromedriver.exe >nul 2>&1")
    else:
        os.system("killall chrome")
        os.system("killall chromedriver")
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
        if int(sys.argv[1]) == 0:
            count_lessons = int(input("Введите количество уроков: "))
            text = main(count_lessons)
            bot.send_message(YOUR_ID, text)
        else:
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
