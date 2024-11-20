# Майнер для duolingo.com

Это майнер для duolingo.com, который проходит за вас урок каждый день или по команде.

## Installation
1. Клонируйте репозиторий - `git clone https://github.com/semenkulikov/duolingo.git`
2. Создайте виртуальное окружение - `python -m venv venv`
3. Активируйте виртуальное окружение. Windows - `venv/Scripts/activate.bat`, Linux - `. venv\bin\activate`
4. Установите зависимости - `pip install -r requirements.txt`
5. Установите браузер Chrome и драйвер для него по [ссылке](https://googlechromelabs.github.io/chrome-for-testing/)
6. Переименуйте файл .env.template в .env и заполните необходимые поля
7. Запустите main.py, в качестве параметра передайте количество уроков. Например, `python main.py 5` - скрипт пройдет 5 уроков. По умолчанию майнер будет включаться каждый день в 8:00 и проходить 15 уроков, после чего высылать уведомление на Telegram.
8. Для Windows есть батники - `activ.bat` активирует майнер, `start.bat` запускает 10 майнеров сразу


# Стек
* Python
* PyTelegramBotAPI
* Selenium
* webdriver-manager
* requests
* python-dotenv
* fake-useragent

Майнер абсолютно бесплатный, если хотите отблагодарить - просто поставьте звездочку наверху)
