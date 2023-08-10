from telebot import TeleBot, types
from config import *
from db.db import Database
import random

bot = TeleBot(bot_token)
db = Database()


def process_adders(adders: str):
    adders = adders.split('+')
    for adder in adders:
        if not adder.isdigit():
            return False
    adders = [int(adder) for adder in adders]
    return adders


def process_roll(roll: str):
    adders = []
    if roll.count('+') > 0:
        adders = process_adders(roll.split('+', 1)[1])
        roll = roll.split("+", 1)[0]
        if not adders:
            adders = []

    if roll.count('d') != 1:
        return False
    roll = roll.split('d')
    cubes = roll[0]
    sides = roll[1]

    if cubes == '':
        cubes = '1'

    if not cubes.isdigit() or not sides.isdigit():
        return False
    cubes, sides = int(cubes), int(sides)

    if sides < 1 or cubes < 0:
        return False

    results = []

    for cube in range(cubes):
        result = random.randint(1, sides)
        results.append(result)
    return results, adders


@bot.message_handler(commands=['r', 'roll'])
def roll_handler(m):
    if m.text.count(' ') < 1:
        bot.reply_to(m, 'Неправильне використання команди.')
        return
    arguments = m.text.split(' ', 2)

    roll = arguments[1]
    if len(arguments) == 3:
        description = f" {arguments[2]}"
    else:
        description = ''

    result = process_roll(roll)
    if not result:
        bot.reply_to(m, 'Неправильне використання команди.')
        return
    result, adders = result

    tts = f"{m.from_user.full_name} кинув{description}:\n" \
          f"  ({' + '.join([str(d) for d in result])}) + {' + '.join([str(d) for d in adders])} = \n" \
          f"{sum(result)+sum(adders)}"

    bot.send_message(m.chat.id, tts)


@bot.message_handler(commands=['start'])
def start_handler(m):
    bot.send_message(m.chat.id, 'Розпочнімо!')


@bot.message_handler(commands=['manage'])
def start_handler(m):
    tts = f"💬Гурт: {m.chat.title}\n\n"

    games = db.get_roleplays(m.chat.id)
    if not games:
        tts += f"📓Ігри: Ігор ще не створено!\n"
    else:
        tts += f"📓Ігри:\n"
        for game in games:
            tts += f"- {game.title}"

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='📖Створити нову гру', callback_data="new_game"))
    kb.add(types.InlineKeyboardButton(text='📔Управління іграми', callback_data="manage_games"))

    bot.send_message(m.chat.id, tts, reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == 'manage_games')
def manage_games(c):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='📖Створити нову гру', callback_data="new_game"))
    kb.add(types.InlineKeyboardButton(text='🔙Головне меню', callback_data='manage'))

    tts = f"💬Гурт: {c.message.chat.title}\n\n"
    games = db.get_roleplays(c.message.chat.id)
    if not games:
        tts += f"📓Ігор ще не створено!\n"
    else:
        tts += f"❓Оберіть гру."
    bot.edit_message_text(tts, c.message.chat.id, c.message.message_id, reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data == 'new_game')
def manage_games(c):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='🔙Головне меню', callback_data='manage'))

    tts = f"🆕Створення нової гри:\n\n"
    tts += 'Будь ласка, у відповідь на це повідомлення напишіть назву цієї гри, наприклад 🦑Пригода кальмарчиків.\n' \
           'Або поверніться в головне меню.'
    tts += f'\n\n🆔: {c.from_user.id}'
    bot.edit_message_text(tts, c.message.chat.id, c.message.message_id, reply_markup=kb)


@bot.message_handler(func=lambda m: m.reply_to_message and m.reply_to_message.from_user.id == bot.user.id)
def reply_handler(m):
    if m.reply_to_message.text.startswith(f"🆕Створення нової гри:\n\n"):
        bot.reply_to(m, f'Створюю гру {m.text}...')


bot.infinity_polling()
