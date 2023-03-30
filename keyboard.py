from aiogram import types

apanel = types.InlineKeyboardMarkup(row_width=3)
apanel.add(types.InlineKeyboardButton(text='📢 Рассылка', callback_data='rass'))
apanel.add(types.InlineKeyboardButton(text='📊 Статистика', callback_data='stats'))
apanel.add(types.InlineKeyboardButton(text='💎 Восстановить роль "Владельца"', callback_data='owner'))
apanel.add(types.InlineKeyboardButton(text='👑 Скачать базу данных', callback_data='getdb'))

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back.add(types.KeyboardButton('Отмена'))

