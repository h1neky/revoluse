from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import name_cheat

btnUrlChannel2 = InlineKeyboardButton(text="🤗Подписаться", url="https://t.me/h1neky_blyat")
btnDoneSub = InlineKeyboardButton(text="❤Подписался", callback_data="subchanneldone")

checkSubMenu = InlineKeyboardMarkup(row_width=1)
checkSubMenu.insert(btnUrlChannel2)
checkSubMenu.insert(btnDoneSub)

btnProfile = KeyboardButton('Реф. система👨‍💼')
btnSpisok = KeyboardButton('Купить чит💲')
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnSpisok, btnProfile)

btnSpis = InlineKeyboardButton(text=f"{name_cheat} | Неделя", callback_data="buy1")
btnSpis1 = InlineKeyboardButton(text=f"{name_cheat} | Месяц", callback_data="buy2")
btnSpis3 = InlineKeyboardButton(text=f"{name_cheat} | Навсегда", callback_data="buy")

mainSpisok = InlineKeyboardMarkup(row_width=1)
mainSpisok.insert(btnSpis)
mainSpisok.insert(btnSpis1)
mainSpisok.insert(btnSpis3)


def buy_menu(isUrl=True, url="", bill=""):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnUrlQIWI = InlineKeyboardButton(text="Ссылка на оплату🖱", url=url)
        qiwiMenu.insert(btnUrlQIWI)
        
    btnCheckQIWI = InlineKeyboardButton(text="Проверить оплату✅", callback_data="check_"+bill)
    qiwiMenu.insert(btnCheckQIWI)
    return qiwiMenu
    
def buy_menu2(isUrl=True, url="", bill=""):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnUrlQIWI = InlineKeyboardButton(text="Ссылка на оплату🖱", url=url)
        qiwiMenu.insert(btnUrlQIWI)
        
    btnCheckQIWI = InlineKeyboardButton(text="Проверить оплату✅", callback_data="check_2"+bill)
    qiwiMenu.insert(btnCheckQIWI)
    return qiwiMenu