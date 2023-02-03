"""
This module implements a Telegram bot for a game of guessing dates of historical events.

The game is initiated by sending the `/play` command, followed by guessing
dates in response to the bot's prompts. The player can surrender by sending
the `/sur` command, or cancel the game by sending the `/cancel` command.
The game's rules and commands can be viewed by sending the `/help` command.
The player's game statistics can be viewed by sending the `/stat` command.

The module contains functions to process the following commands:

    `/start` - start the bot.
    `/help` - view the rules of the game and available commands.
    `/play` - start a new game.
    `/sur` - surrender and receive information about the historical event.
    `/cancel` - exit the game mode.
    `/stat` - view game statistics.

It also contains functions to process date answers and other text answers
received from the player during the game.

"""
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from pymongo.database import Database

from config import BOT_TOKEN
from dao import PlayerDao
from database import get_database
from game import GuessGame
from models import Player


bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    """Process the start command for the historical date guessing game.

    This function processes the start command from the user, sends a welcome
    message and information about the game, and creates a new player in
    the database.
    """
    await message.answer(
        'Привет!\nДавай сыграем в игру "Угадай дату"?\n\n'
        "Чтобы получить правила игры и список доступных "
        "команд - отправьте команду /help"
    )
    # Create new player
    player = Player(_id=message.from_user.id)
    player = players.create(player)


@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    """Sends game rules and a list of commands."""
    await message.answer(
        "Правила игры:\n\nЯ называю вам историческое событие, "
        "а вам нужно назвать в каком году оно произошло.\n\n"
        "Пример ответа: 1998\n\n"
        "Доступные команды:\n"
        "/play - начать играть\n"
        "/sur - сдаться\n"
        "/cancel - отменить игру\n"
        "/stat - посмотреть статистику\n"
        "/help - правила игры и список команд\n\nДавай сыграем?"
    )


@dp.message(Command(commands=["play"]))
async def process_play_command(message: Message):
    """Process the play command for the historical date guessing game.

    This function starts a new round of the game. The function retrieves
    the next event from the game memory and sends it to the user for guessing.
    """
    event = game.play(message.from_user.id)
    await message.answer(event.event)


@dp.message(Command(commands=["sur"]))
async def process_surrender_command(message: Message):
    """Process the surrender command for the historical date guessing game.

    This function processes the surrender command from the user during a round
    of the game. If the user is currently in a game, the function retrieves
    the correct event from the game memory, sends it to the user,
    and updates the user's statistics in the database.
    """
    player = game.get_player(message.from_user.id)
    if not player.in_game:
        await message.answer("Мы еще не играем. Хотите сыграть? /play")
    else:
        event = game.surrender(player)
        await message.answer(event.explain())
        if image := event.get_image_file():
            await bot.send_photo(message.chat.id, image)
        if event.description:
            await message.answer(event.description)


@dp.message(Command(commands=["cancel"]))
async def process_cancel_command(message: Message):
    """Process the cancel command for the historical date guessing game.

    This function processes the cancel command from the user during a round of
    the game. If the user is currently in a game, the function cancels the
    current game and sends a message to the user indicating that the user
    have left the game.
    """
    player = game.get_player(message.from_user.id)
    if not player.in_game:
        await message.answer("Мы еще не играем. Хотите сыграть? /play")
    else:
        game.cancel(player)
        await message.answer(
            "Вы вышли из игры. Если захотите сыграть "
            "снова - напишите об этом. /play"
        )


@dp.message(Command(commands=["stat"]))
async def process_stat_command(message: Message):
    """Handles the stat command, which retrieves the statistics of the player.

    The statistics include:

        Score: the number of points the player has accumulated.
        Total number of attempts: the total number of attempts the player
                                  has made to guess the date of an event.
        Number of guessed events: the number of events that the player has
                                  successfully guessed.
        Average number of attempts per answer: the average number of attempts
                                the player takes to guess the date of an event.
    """
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
    """Process a user's answer to a date in the current game.

    Validates an answer. Gets a result from the game and sends a result message
    to the user. The result message has either gussed event infomation or
    hints for guessing.
    """
    date = int(message.text)
    player = game.get_player(message.from_user.id)

    if not player.in_game:
        await message.answer("Мы еще не играем. Хотите сыграть? /play")

    elif not 0 <= date <= 2023:
        await message.answer("Присылайте даты от 0 до 2023 года.")

    else:
        msg, event = game.guess(player, date)
        if event:
            await message.answer(event.explain())
            if image := event.get_image_file():
                await bot.send_photo(message.chat.id, image)
            if event.description:
                await message.answer(event.description)
        else:
            await message.answer(msg)


@dp.message()
async def process_other_text_answers(message: Message):
    """Processes the text messages that are not associated with any specific command.

    If the player is in a game, they will receive a message asking them
    to provide a date in the format "YYYY".
    If the player is not in a game, they will receive a message asking them
    to start a game by using the "/play" command.
    """
    player = game.get_player(message.from_user.id)
    if player.in_game:
        await message.answer(
            "Мы же сейчас с вами играем. "
            "Присылайте, пожалуйста, даты в виде 1998."
        )
    else:
        await message.answer(
            "Я играю только по правилам, введите /help, чтобы узнать правила."
        )


if __name__ == "__main__":
    database: Database = get_database()
    players: PlayerDao = PlayerDao(database)
    with GuessGame(database) as game:
        dp.run_polling(bot)
