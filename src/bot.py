import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message, FSInputFile
from aiogram.filters import Text, Command
from pymongo.collection import Collection

from config import BOT_TOKEN, BASE_PATH
from models import Player
from dao import PlayerDao
from database import get_database
from game import GuessGame


bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавай сыграем в игру "Угадай дату"?\n\n'
        "Чтобы получить правила игры и список доступных "
        "команд - отправьте команду /help"
    )
    player = Player(_id=message.from_user.id)
    player = players.create(player)


@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer(
        f"Правила игры:\n\nЯ называю вам историческое событие, "
        f"а вам нужно назвать в каком году оно произошло.\n\n"
        "Пример ответа: 1998\n\n"
        "Доступные команды:\n"
        "/play - начать играть\n"
        "/sur - сдаться\n"
        "/cancel - отменить игру\n"
        "/stat - посмотреть статистику\n"
        "/help - правила игры и список команд\n\nДавай сыграем?"
    )


@dp.message(Command(commands=["play"]))
async def process_help_command(message: Message):
    event = game.play(message.from_user.id)
    await message.answer(event.event)


@dp.message(Command(commands=["sur"]))
async def process_surrender_command(message: Message):
    player = game.get_player(message.from_user.id)
    if not isinstance(player.current_event, int):
        await message.answer("Мы еще не играем. Хотите сыграть? /play")
    else:
        event = game.surrender(player)
        await message.answer(str(event.date) + " - " + event.event)
        if event.image_path:
            image_path = os.path.join(BASE_PATH, event.image_path)
            if os.path.isfile(image_path):
                image = FSInputFile(image_path)
                await bot.send_photo(message.chat.id, image)
        if event.description:
            await message.answer(event.description)


@dp.message(Command(commands=["cancel"]))
async def process_cancel_command(message: Message):
    player = game.get_player(message.from_user.id)
    if not isinstance(player.current_event, int):
        await message.answer("Мы еще не играем. Хотите сыграть? /play")
    else:
        game.cancel(player)
        await message.answer(
            "Вы вышли из игры. Если захотите сыграть "
            "снова - напишите об этом. /play"
        )


@dp.message(Command(commands=["stat"]))
async def process_stat_command(message: Message):
    player = game.get_player(message.from_user.id)
    gussed_events_num = len(player.guessed_events)
    try:
        attempts_average = round(player.attempts / gussed_events_num)
    except ZeroDivisionError:
        attempts_average = 0
    await message.answer(
        f"Очки: {player.score}\n"
        f"Общее число попыток: {player.attempts}\n"
        f"Угаданных дат: {gussed_events_num}\n"
        f"Среднее кол-во попыток на ответ: {attempts_average}"
    )


@dp.message(lambda x: x.text and x.text.isdigit())
async def process_date_answer(message: Message):
    date = int(message.text)
    player = game.get_player(message.from_user.id)

    if not isinstance(player.current_event, int):
        await message.answer("Мы еще не играем. Хотите сыграть? /play")

    elif not 0 <= date <= 2023:
        await message.answer("Присылайте даты от 0 до 2023 года.")
        return

    else:
        msg, event = game.guess(player, date)
        if event:
            await message.answer(
                "{}\n{} - {}".format(msg, str(event.date), event.event)
            )
            if event.image_path:
                image_path = os.path.join(BASE_PATH, event.image_path)
                if os.path.isfile(image_path):
                    image = FSInputFile(image_path)
                    await bot.send_photo(message.chat.id, image)
            if event.description:
                await message.answer(event.description)
        else:
            await message.answer(msg)


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_text_answers(message: Message):
    player = game.get_player(message.from_user.id)
    if isinstance(player.current_event, int):
        await message.answer(
            "Мы же сейчас с вами играем. "
            "Присылайте, пожалуйста, даты в виде 1203"
        )
    else:
        await message.answer(
            "Я играю только по правила, введите /help, чтобы узнать правила"
        )


if __name__ == "__main__":
    database: Collection = get_database()
    players: PlayerDao = PlayerDao(database)
    with GuessGame(database) as game:
        dp.run_polling(bot)
