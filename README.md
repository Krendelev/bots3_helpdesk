# Справочный чат-бот

Бот отвечает на распространенные вопросы о работе компании. Построен на основе сервиса распознавания естественного языка [Google Dialogflow](https://cloud.google.com/dialogflow). Пообщаться с ботом можно в [Телеграм](https://t.me/mylittletimer_bot) и [ВКонтакте](https://vk.com/club186139586).

## Запуск

Скачайте код и установите зависимости.

```bash
$ python3 -m pip install -r requirements.txt
```
Создайте проект в [Google Cloud](https://cloud.google.com/dialogflow/es/docs/quick/setup), скачайте ключи авторизации и переименуйте файл в `google-credentials.json`.

Запустите программу:
```bash
$ python3 telegram_bot.py
или
$ python3 vk_bot.py
```
Вы можете обучить бота ответам на определенные группы вопросов. Для этого добавьте вопросы и ответ на них в файл `training_phrases.json` и запустите `utils.py`:
```bash
$ python3 utils.py
```

## Настройки и переменные окружения

Сохраните переменные окружения в файл `.env`.

- `VK_ACCESS_TOKEN` – API-ключ группы ВКонтакте, к которой подключен бот
- `TELEGRAM_TOKEN` – API-ключ телеграм-бота
- `LOGGER_TOKEN` – API-ключ телеграм-бота используемого для логирования
- `TELEGRAM_CHAT_ID` – id чата для отправки логов
- `GOOGLE_APPLICATION_CREDENTIALS` – название файла с ключами проекта Google – `google-credentials.json`

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
