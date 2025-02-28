# Telegram support
Telegram support - телеграм бот для оказания поддержки пользователям какого либо сервиса с помощью телеграм бота.

Как это работает? После полной настройки бота пользователь, у которого возник какой либо вопрос может написать вам в телеграм бота, а вам в заранее подготовленный и подключенный к боту чат будет создаваться топик в чате для ведения диалога с конкретным пользователем, что позволяет обходить спамблок пользователям, которые хотят свзяаться с поддержкой, а на стороне администрации удобно обрабатывать входящие вопросы.

# Технологии
Для разработки используются aiogram v3.5.0 и aiosqlite для работы с базой данных. 

# Функции
1. Привязка чата для поступления вопросов от пользователей прямов в панели администратора!
2. Запрет на контент. Можно запретить тип контента, который могут отправлять пользователи (фото, видео, голосовые сообщения и т.д)
3. Капча (можно выключить)
4. Тех работы (можно выключить)
5. Рабочий режим (если выкл. то пользователю будет писать что сейчастех поддержка не работает)
6. Рассылка в боте с поддержкой медиафайлов и URL кнопок
7. Поиск пользователей через inline mode (нужно включить в настройках бота в @BotFather -> Bot Settings -> Inline Mode -> Turn On)
8. Смена прав для юзеров (модер, бан, админ) в боте
9. Редактирование текстов, FAQ прямо в боте с поддержкой медиафайлов и URL кнопок

# Инструкция
Качаем репу: `git clone https://github.com/asyncTraffic/telegram_support.git` или просто скачайте архивом

В файле `data/config.py` меняем TOKEN на свой, так же добавляем корневого администратора, в коде показано что куда вставлять

## Создаем виртуально окружение: 
Debian/Ubuntu: `python3 -m venv venv`

Windows: `python -m venv venv`

## Установка модулей и запуск:
### Установка
Debian/Ubuntu: `pip3 install -r requirements.txt`

Windows: `pip install -r requirements.txt`

### Запуск:
Debian/Ubuntu: `python3 bot.py`

Windows: `python3 bot.py`

# Настройка бота
1. Запускаем бота и пишем команду /admin, далее жмем кнопку "⚙️ Настройки" ![изображение](https://github.com/user-attachments/assets/73e74a14-46c1-48cf-90a3-21c1d47ca2df)
2. Выбираем кнопку "💭 Чат" и видим, что у нас не привзяан ни один чат, жмем кнопку "Задать чат" ![изображение](https://github.com/user-attachments/assets/c48f693a-5303-42da-832b-19cbba21d464)
3. Теперь нам нужно создать обычную приватную(закрытую) группу/чат (кому как удобно это называть), включаем там темы и сохраняем: ![изображение](https://github.com/user-attachments/assets/85ab51c6-5860-483c-9469-bf92aef9597f)
4. Возвращаемся в бота и жмем "Добавить бота в чат": ![изображение](https://github.com/user-attachments/assets/d26b3d6d-bc86-4562-a3d4-c9360aba6c4a)
5. Выбираем ранее созданный чат с темами: ![изображение](https://github.com/user-attachments/assets/d879d5c9-ff6c-4926-9488-3efa5d26b28a)
6. Выдаем вот такие права и жмем "Назначить бота администратором": ![изображение](https://github.com/user-attachments/assets/c8a92e88-9660-45b9-9b98-d0e8a6f44b7c)
7. В боте жмем кнопку "Проверить", и если вы сделали все правильно у вас будет вот такой текст, под ним жмем кнопку "Задать": ![изображение](https://github.com/user-attachments/assets/567ed50d-c8f7-487f-922b-90c84f2f88cc)
8. Если все сделали верно получим вот такой сообщение, далее нам нужно нажать на кнопку "Работа бота" и получаем меню с свитчами капчи, тех работ и тд, так же там можно настроить разрашенный контент ![изображение](https://github.com/user-attachments/assets/cf6d25b7-3696-44f3-a348-317547ced0e8)
9. Готово! Бот готов к использованию

# Скриншоты бота
![изображение](https://github.com/user-attachments/assets/cd285d01-7bfa-4f94-ae50-744deb1d5219)

![изображение](https://github.com/user-attachments/assets/4156dfab-250d-45f8-a049-cc6c1b822a9e)

![изображение](https://github.com/user-attachments/assets/342442a2-9f20-457c-b7ad-6299265749be)

![изображение](https://github.com/user-attachments/assets/8f2204e6-4cfe-401a-bc0c-e04e83b10172)

![изображение](https://github.com/user-attachments/assets/4d2e38a1-2645-42e3-8420-556d5138647d)

![изображение](https://github.com/user-attachments/assets/0e2cfb36-e5be-4107-8762-f4bc80a4a63c)

![изображение](https://github.com/user-attachments/assets/5f0c8fda-aa17-4124-ab53-e31d585c010f)

![изображение](https://github.com/user-attachments/assets/b7bc087f-d4f6-4ac4-8f4f-7839ba03c783)


# Связь со мной

TG: https://t.me/asyncTraffic




