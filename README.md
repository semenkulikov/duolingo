# Майнер для duolingo.com

Это майнер для duolingo.com, который проходит за вас урок каждый день или по задаче. Один урок - 5 баллов.

## Installation
1. Клонируйте репозиторий - `git clone https://github.com/semenkulikov/duolingo.git`
2. Установите зависимости - `pip install -r requirements.txt`
3. Установите браузер Chrome и драйвер для него по [ссылке](https://googlechromelabs.github.io/chrome-for-testing/)
4. Переименуйте файл .env.template в .env и заполните необходимые поля
5. Активируйте виртуальное окружение. Windows - `venv/Scripts/activate.bat`, Linux - `. venv\bin\activate`
6. Запустите main.py, в качестве параметра передайте количество уроков. Например, `python main.py 5` - скрипт пройдет 5 уроков. По умолчанию майнер будет включаться каждый день в 8:00 и проходить 15 уроков, после чего высылать уведомление на Telegram.
7. Для Windows есть батники - `activ.bat` активирует майнер, `start.bat` запускает 10 майнеров сразу


# Стек
* Python
* PyTelegramBotAPI
* Selenium
* webdriver-manager
* requests
* python-dotenv
* fake-useragent
