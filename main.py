import os
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY, parse_mode=None)
chat_id = ''


numbers={}

@bot.message_handler(commands=['start'])
def greet(message):
  bot.reply_to(message, "Hellooooooo whatsup")

@bot.message_handler(commands=['options'])
def option(message):
  markup = types.ReplyKeyboardMarkup()
  itembtna = types.KeyboardButton('a')
  itembtnv = types.KeyboardButton('v')
  itembtnc = types.KeyboardButton('c')
  itembtnd = types.KeyboardButton('d')
  itembtne = types.KeyboardButton('e')
  markup.row(itembtna, itembtnv)
  markup.row(itembtnc, itembtnd, itembtne)
  bot.send_message(message.chat.id, "Choose one letter:",  reply_markup=markup)

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu

@bot.message_handler(commands=['halls'])
def halls(message):
  list_of_halls = ['Raffles Hall', 'Kent Ridge Hall', 'King Edward VII', 'PGP Hall', 'Sheares Hall', 'Temasek Hall']
  button_list = []
  for each in list_of_halls:
     button_list.append(InlineKeyboardButton(each, callback_data = each))
  reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1)) ,
  #n_cols = 1 is for single column and mutliple rows
  bot.send_message(
    chat_id=message.chat.id,
    text='Choose your hall',
    reply_markup=reply_markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # if call.data == "Raffles Hall":
    #     bot.answer_callback_query(call.id, call.data)
    bot.answer_callback_query(call.id, call.data)
    



bot.infinity_polling()