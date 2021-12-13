

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
                               InlineKeyboardButton("No", callback_data="cb_no"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())


def halls(update, context):
  list_of_halls = ['Raffles Hall', 'Kent Ridge Hall', 'King Edward VII', 'PGP Hall', 'Sheares Hall', 'Temasek Hall']
  button_list = []
  for each in list_of_halls:
     button_list.append(InlineKeyboardButton(each, callback_data = each))
  reply_markup=InlineKeyboardMarkup(build_menu(button_list,n_cols=1)) 
  #n_cols = 1 is for single column and mutliple rows
  bot.send_message(chat_id=update.message.chat_id, text='Choose your hall',reply_markup=reply_markup)


def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu