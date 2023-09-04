# Date Duel - игровой телеграм бот для угадывания исторических дат 

Это Telegram-бот для игры в угадывание исторических дат. Пользователь запускает игру, набрав `/play`, и бот выдает событие. Пользователь должен угадать дату события. Бот будет давать подсказки после каждого неверного предположения и обновлять счет пользователя после каждой игры. Пользователь может просмотреть свой прогресс, набрав `/stat`.

 <img src="https://s3.gifyu.com/images/ezgif.com-gif-maker1f6d5675cbaff03bf.gif" align="right" />

Когда пользователь правильно угадает дату события, бот предоставит дополнительную информацию о событии и связанное с ним изображение. Это не только позволяет пользователям больше узнать об исторических событиях, но и делает игру более увлекательной и визуально привлекательной.

**Команды**:

 - `/start` - запустить бота.
 - `/help` - правила игры и команды.
 - `/play` - начать играть.
 - `/sur` - сдаться и получить информацию о событии.
 - `/cancel` - выход из режима игры.
 - `/stat` - просмотреть статистику.

Бот использует базу данных MongoDB для хранения исторических событий, пользовательской информации и результатов игр. Это позволяет боту отслеживать прогресс пользователя с течением времени и обеспечивать точную запись его результатов и производительности.

# Зависимости 

    Python 3.8
    aiogram 3.0.* - для использования Telegram Bot API
    PyMongo - драйвер для MongoDB

# Установка

1. Клонирование репозитория:

```bash
git clone https://github.com/welel/date-duel-bot.git
```

2. Создание виртуального окружения и установка зависимостей:

```bash
python3.8 -m venv env
source env/bin/activate
pip install -r requirements/local.txt
```

3. Создать бота и создать базу данных MongoDB. Данные с историческими событиями в json файле `res/events.json`.

**Структура MongoDB:**

```js
// Collection - HistoricalEvents
{
  "_id": 0, // Уникальное
  "_type": "date",
  "event": "Начало княжения Рюрика",
  "date": 862,
  "description": "Рюрик начал свое княжение...", // Опциональное
  "image_path": "res/images/date-0.jpg" // Опциональное
}

// Collection - Players
{
  "_id": {
    "$numberLong": "6855231396" // Уникальное (tg user id)
  },
  "current_event": null,
  "guessed_events": [0, 1],
  "attempts": 7,
  "score": 37
}
```

4. Заполнить файл `.env.dist` и переименовать его `.env`.

5. Запуск бота.

```bash
python bot.py
```

