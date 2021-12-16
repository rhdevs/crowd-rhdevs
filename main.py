import os
import telebot
import json
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY, parse_mode=None)

# Opening JSON file
f = open('store.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)
# print(data['Raffles Hall'])
# print(data['Raffles Hall']['Gymnasium'])
# db["Raffles Hall"] = {"Gym": 10, "Hall": 2}
# value = db["Raffles Hall"]["Gym"]
db = {}
user_dict = {}
db["Gym"] = [0,0,0,0,0]
# try hard code calculation, need to firebase instead
class User:
  def __init__(self, name):
    self.name = name
    self.hall = None
    self.venue = None
    self.capacity = None

@bot.message_handler(commands=['start'])
def greet(message):
  process_hall_step(message)



def process_hall_step(message):
  try:
    chat_id = message.chat.id
    name = message.text
    user = User(name)
    user_dict[chat_id] = user
    button_list = []
    # static list for options
    for each in data['halls']:
      button_list.append(InlineKeyboardButton(each, callback_data = each))

    reply_markup=InlineKeyboardMarkup(build_menu(button_list, n_cols=1)) 
    #n_cols = 1 is for single column and mutliple rows
    bot.send_message(
      chat_id=chat_id,
      text='Choose your hall',
      reply_markup=reply_markup
      )
    # bot.register_next_step_handler(message, process_venue_step)
  except Exception:
    bot.reply_to(message, 'oooops')

# def process_venue_step(message):
#     try:
#       chat_id = message.chat.id
#       venue = message.text
#       #if not age.isdigit():
#       #    msg = bot.reply_to(message, 'Age should be a number. How old are you?')
#       #    bot.register_next_step_handler(msg, process_venue_step)
#       #    return
#       user = user_dict[chat_id]
#       user.venue = venue
#       markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
#       markup.add('Yes', 'No')
#       msg = bot.reply_to(message, 'Is there space', reply_markup=markup)
#       # bot.register_next_step_handler(msg, process_capacity_step)
#     except Exception as e:
#       bot.reply_to(message, 'oooops')


# def process_capacity_step(message):
#     try:
#       chat_id = message.chat.id
#       capacity = message.text
#       user = user_dict[chat_id]
#       if (capacity == u'Yes') or (capacity == u'No'):
#           user.capacity = capacity
#       else:
#           raise Exception("Unknown capacity")
#       bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Venue:' + str(user.venue) + '\n Capacity:' + user.capacity)
#     except Exception as e:
#       bot.reply_to(message, 'oooops')

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
  user = user_dict[call.message.chat.id]

  bot.answer_callback_query(call.id, call.data)
  if call.data in data['halls']:
    user.hall = call.data
    
    if user.hall not in db:
      db[user.hall] = {}
    print("DATABASE", db)
    print(user.hall)
    button_list = []
    for each in data[user.hall]:
     button_list.append(InlineKeyboardButton(each, callback_data = each))
    
    reply_markup=InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    bot.answer_callback_query(call.id, call.data)
    bot.edit_message_text(chat_id=call.message.chat.id,                     message_id=call.message.message_id, text=f'You have chosen {user.hall}' ,reply_markup=reply_markup)
    #print(bot.message_text)

  # facilities in hall
  # each facility will have list of latest 5 votes
  rating_list = [0,0,0,0,0]
  
  if call.data in data[user.hall]:
    user.venue = call.data
    print(f'{user.hall} {user.venue}')
    button_list = []

    # SPACE VOTING OPTIONS
    button_list.append(InlineKeyboardButton(text = 'Empty', callback_data = '0'))
    button_list.append(InlineKeyboardButton(text = 'Some Space', callback_data = '0.5'))
    button_list.append(InlineKeyboardButton(text = 'Full', callback_data = '1'))
    reply_markup=InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    bot.answer_callback_query(call.id, call.data)
    # text in message depends on average
    handleRatings(call, reply_markup, rating_list, user.hall, user.venue)
    print(rating_list)

  if user.venue and user.venue in db[user.hall]:
    rating_list = db[user.hall][user.venue]

  if call.data == '0':
    rating_list.pop(0)
    rating_list.append(0)
    db[user.hall][user.venue] = rating_list
    handleRatings(call, None, rating_list, user.hall, user.venue)
    
  if call.data == '0.5':
    print(rating_list.pop(0))
    rating_list.append(0.5)
    db[user.hall][user.venue] = rating_list
    handleRatings(call, None, rating_list, user.hall, user.venue)
  if call.data == '1':
    rating_list.pop(0)
    rating_list.append(1)
    db[user.hall][user.venue] = rating_list
    handleRatings(call, None, rating_list, user.hall, user.venue)
  

def handleRatings(call, reply_markup, location, hall, venue):
  average = sum(location) / len(location)
  print(average)

  if average <= 0.1:
    bot.edit_message_text(chat_id=call.message.chat.id,                   message_id=call.message.message_id, text=f'Crowd level for {hall} {venue}: \n \U0001F525', reply_markup=reply_markup)
  elif average <= 0.3:
    bot.edit_message_text(chat_id=call.message.chat.id,                   message_id=call.message.message_id, text=f'Crowd level for {hall} {venue}:\n \U0001F525\U0001F525' ,reply_markup=reply_markup)
  elif average <= 0.5:
    bot.edit_message_text(chat_id=call.message.chat.id,                   message_id=call.message.message_id, text=f'Crowd level for {hall} {venue}:\n \U0001F525\U0001F525\U0001F525' ,reply_markup=reply_markup)
  elif average <= 0.7:
    bot.edit_message_text(chat_id=call.message.chat.id,                   message_id=call.message.message_id, text=f'Crowd level for {hall} {venue}:\n \U0001F525\U0001F525\U0001F525\U0001F525' ,reply_markup=reply_markup)
  else: 
    bot.edit_message_text(chat_id=call.message.chat.id,                   message_id=call.message.message_id, text=f'Crowd level for {hall} {venue}:\n \U0001F525\U0001F525\U0001F525\U0001F525\U0001F525' ,reply_markup=reply_markup)
  

bot.infinity_polling()