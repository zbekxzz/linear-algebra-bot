import telebot
from telebot import types
import functions
from random import choice, shuffle

bot = telebot.TeleBot('BOT_TOKEN')

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/menu")
    markup.add(btn1)
    gif = open("hello.gif", 'rb')
    bot.send_animation(message.from_user.id, gif)
    bot.send_message(message.from_user.id, "Hello! I am your bot helper. Type '/menu' and I will help you", reply_markup=markup)



@bot.message_handler(commands=['menu'])
def menu(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Send me tutorials')
    btn2 = types.KeyboardButton('A want to take quiz')
    btn3 = types.KeyboardButton('Help me with calculations')
    btn4 = types.KeyboardButton('Send me motivation quotes')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.from_user.id, 'How can I help you?', reply_markup=markup)



@bot.message_handler(commands=['determinant'])
def determinant(message):
    msg = bot.send_message(message.from_user.id, "What is dimension of your matrix?\nExample: 2 2")
    bot.register_next_step_handler(msg, determinant_1)

def determinant_1(message):
    msg = bot.send_message(message.from_user.id, 'Insert all the elements:\nExample: 2 1 0 3\n`2 1\n0 3`', parse_mode='Markdown')
    bot.register_next_step_handler(msg, determinant_2, message.text)

def determinant_2(message, row):
    det = functions.find_determinant(row, message.text)
    bot.send_message(message.from_user.id, det)



@bot.message_handler(commands=['rank'])
def rank(message):
    msg = bot.send_message(message.from_user.id, "What is dimension of your matrix?\nExample: 2 2")
    bot.register_next_step_handler(msg, rank_1)

def rank_1(message):
    msg = bot.send_message(message.from_user.id, 'Insert all the elements:\nExample: 2 1 0 3\n`2 1\n0 3`', parse_mode='Markdown')
    bot.register_next_step_handler(msg, rank_2, message.text)

def rank_2(message, row):
    rank = functions.find_rank(row, message.text)
    bot.send_message(message.from_user.id, rank)



@bot.message_handler(commands=['eigenvalue'])
def eigenvalue(message):
    msg = bot.send_message(message.from_user.id, "What is dimension of your matrix?\nExample: 2 2")
    bot.register_next_step_handler(msg, eigenvalue_1)

def eigenvalue_1(message):
    msg = bot.send_message(message.from_user.id, 'Insert all the elements:\nExample: 2 1 0 3\n`2 1\n0 3`', parse_mode='Markdown')
    bot.register_next_step_handler(msg, eigenvalue_2, message.text)

def eigenvalue_2(message, row):
    eigenvalue = functions.find_eigenvalue(row, message.text)
    bot.send_message(message.from_user.id, eigenvalue)



@bot.message_handler(commands=['eigenvector'])
def eigenvector(message):
    msg = bot.send_message(message.from_user.id, "What is dimension of your matrix?\nExample: 2 2")
    bot.register_next_step_handler(msg, eigenvector_1)

def eigenvector_1(message):
    msg = bot.send_message(message.from_user.id, 'Insert all the elements:\nExample: 2 1 0 3\n`2 1\n0 3`', parse_mode='Markdown')
    bot.register_next_step_handler(msg, eigenvector_2, message.text)

def eigenvector_2(message, row):
    eigenvector = functions.find_eigenvector(row, message.text)
    bot.send_message(message.from_user.id, f"`{eigenvector}`\nYour eigenvectors", parse_mode="Markdown")



@bot.message_handler(regexp=r"Tut - \d+\.\d+\.\d+")
def send_video(message):
    link = functions.get_video_link(message.text)
    video = open(link, "rb")
    bot.send_message(message.from_user.id, f"*Tutorial - {message.text[6:]}*", parse_mode="Markdown")
    bot.send_video(message.chat.id, video)
    bot.send_message(message.from_user.id, "Enjoy watching, I hope the material will be useful! Video from YouTube channel:")
    bot.send_message(message.from_user.id, "[Kimberly Brehm](https://www.youtube.com/@SawFinMath)", parse_mode="Markdown")



@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == 'Send me tutorials':
        bot.send_message(message.from_user.id, functions.get_tutorials_list(), parse_mode= 'Markdown')
        bot.send_message(message.from_user.id, "To get tutorial by any theme send me number of tutorial.\nEx. 'Tut - 1.1.2'")

    elif message.text == 'A want to take quiz':
        rand_task = choice(["linear", "matrix"])
        task = functions.get_random_task(rand_task)
        if rand_task == "linear":
            text = task["task"]

            markup = types.InlineKeyboardMarkup(row_width = 2)
            btn1 = types.InlineKeyboardButton(task["correct"], callback_data="correct")
            btn2 = types.InlineKeyboardButton(task["incorrect"], callback_data="incorrect")
            btns = [btn1, btn2]
            shuffle(btns)
            markup.add(btns[0], btns[1])

            bot.send_message(message.from_user.id, text, reply_markup=markup, parse_mode="Markdown")
        if rand_task == "matrix":
            arr = task["matrix"]
            matrix = ""
            for i in range(len(arr)):
                row = ""
                for j in range(len(arr[0])):
                    row += f"{arr[i][j]} "
                row += "\n"
                matrix += row
            text = task["task"]

            markup = types.InlineKeyboardMarkup(row_width = 2)
            btn1 = types.InlineKeyboardButton(task["correct"], callback_data="correct")
            btn2 = types.InlineKeyboardButton(task["incorrect"], callback_data="incorrect")
            btns = [btn1, btn2]
            shuffle(btns)
            markup.add(btns[0], btns[1])

            bot.send_message(message.from_user.id, f"`{matrix}`\n{text}", reply_markup=markup, parse_mode= 'Markdown')

    elif message.text == 'Help me with calculations':
        bot.send_message(message.from_user.id, functions.get_calc_commands(), parse_mode="Markdown")

    elif message.text == 'Send me motivation quotes':
        bot.send_message(message.from_user.id, functions.get_random_quote(), parse_mode= 'Markdown')



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "correct":
        bot.answer_callback_query(call.id, "You are correct!")
    elif call.data == "incorrect":
        bot.answer_callback_query(call.id, " You are mistaken!")
        

bot.polling(none_stop=True, interval=0)