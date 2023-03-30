import aiogram
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from decimal import Decimal
import sqlite3
import config
from db import Database
from config import token, id_channel1, not_sub_message, admin, cena, vremya, name_cheat, cena2, cena3
import murkups as nav
import loguru
from loguru import logger
import pyqiwip2p
from pyqiwip2p import QiwiP2P
import random, time, asyncio
import keyboard as kb
import ftplib

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
# bot init
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)
db = Database('users.db')

class Form(StatesGroup):
    start = State()  # Will be represented in storage as 'Form:name'

class info(StatesGroup):
  name = State()
  rasst = State()
  click = State()

class CountUsers(StatesGroup):
    count_users = State()

connect = sqlite3.connect('users.db')
cursor = connect.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS stat (user_id INTEGER, status INTEGER)")
connect.commit()

p2p = QiwiP2P(auth_key="eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjYzd3Z4Ny0wMCIsInVzZXJfaWQiOiIzNzUyNTU0NTgwMzMiLCJzZWNyZXQiOiI0MmE5NTI1NmU3MGQwNDBjMjcxZjc3ZGFlMzZkM2ZjYjQ1MjgxMWUzMDE3OTU5ZTY2Zjk2Yjg0YmQ1OTg3YWQ0In19")

logger.add("logs.ini", format="{time} | {message}")


#проверка подписки на канал
def check_sub(chat_member):
    print(chat_member['status'])
    if chat_member['status'] != 'left':
        return True
    else:
        return False

@dp.callback_query_handler(text="subchanneldone")
async def subchanneldone(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if check_sub(await bot.get_chat_member(chat_id=id_channel1, user_id=message.from_user.id)):
        await bot.send_message(message.from_user.id, f"<b>Ты успешно подписался, продублируй комманду заново</b>",  parse_mode='html', reply_markup=nav.mainMenu)
    else:
        await bot.send_message(message.from_user.id, not_sub_message, reply_markup=nav.checkSubMenu)

#конец проверки
        
        
        
#комманда старт    
@dp.message_handler(commands=['start'], commands_prefix='!?./')
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    cursor.execute("SELECT * FROM stat WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO stat (user_id, status) VALUES (?, ?)", (user_id, 0))
        connect.commit()
    if not db.user_exists(message.from_user.id):
        start_command = message.text
        referrer_id = str(start_command[7:])
        if str(referrer_id) != "":
            if str(referrer_id) != str(message.from_user.id):
                db.add_user(message.from_user.id, referrer_id)
                try:
                    await bot.send_message(referrer_id, "<b>По вашей ссылке зарегистрировался новый человек</b>",  parse_mode='html')
                except:
                    pass
            else:
                await bot.send_message(message.from_user.id, "<b>Нельзя регать самого себя</b>")
        else:
            db.add_user(message.from_user.id)

    if check_sub(await bot.get_chat_member(chat_id=id_channel1, user_id=message.from_user.id)):
        await bot.send_message(message.from_user.id, f"<b>Привет, смотри на клавиатуру и нажимай на то что тебе нужно</b>",  parse_mode='html', reply_markup=nav.mainMenu)
    else:
        await bot.send_message(message.from_user.id, not_sub_message, reply_markup=nav.checkSubMenu)


#каллбеки оплата
@dp.callback_query_handler(text="buy")
async def check(callback: types.CallbackQuery):
    comment = "revoluse" + str(random.randint(1000, 9999)) + "__navsegda" 
    bill = p2p.bill(amount=cena, lifetime=vremya, comment=comment)
    db.add_check(callback.from_user.id, bill.bill_id)
                
    await bot.send_message(callback.from_user.id, f"<b>Товар: {name_cheat} | Навсегда</b>\n<b>Цена: {cena}₽</b>\n<b>Кол-во: 1 шт.</b>\n\n<b>Ссылка для оплаты:</b> {bill.pay_url}\n\n<b>Время на оплату {vremya} минут</b>", reply_markup=nav.buy_menu(url=bill.pay_url, bill=bill.bill_id), parse_mode='html')

@dp.callback_query_handler(text="buy1")
async def check(callback: types.CallbackQuery):
    comment1 = "revoluse" + str(random.randint(1000, 9999)) + "__nedelya" 
    bill = p2p.bill(amount=cena2, lifetime=vremya, comment=comment1)
    db.add_check(callback.from_user.id, bill.bill_id)
                
    await bot.send_message(callback.from_user.id, f"<b>Товар: {name_cheat} | Неделя</b>\n<b>Цена: {cena2}₽</b>\n<b>Кол-во: 1 шт.</b>\n\n<b>Ссылка для оплаты:</b> {bill.pay_url}\n\n<b>Время на оплату {vremya} минут</b>", reply_markup=nav.buy_menu(url=bill.pay_url, bill=bill.bill_id), parse_mode='html')

@dp.callback_query_handler(text="buy2")
async def check(callback: types.CallbackQuery):
    comment2 = "revoluse" + str(random.randint(1000, 9999)) + "__mesyac" 
    bill = p2p.bill(amount=cena3, lifetime=vremya, comment=comment2)
    db.add_check(callback.from_user.id, bill.bill_id)
                
    await bot.send_message(callback.from_user.id, f"<b>Товар: {name_cheat} | Месяц</b>\n<b>Цена: {cena3}₽</b>\n<b>Кол-во: 1 шт.</b>\n\n<b>Ссылка для оплаты:</b> {bill.pay_url}\n\n<b>Время на оплату {vremya} минут</b>", reply_markup=nav.buy_menu(url=bill.pay_url, bill=bill.bill_id), parse_mode='html')

#каллбеки проверка оплаты
@dp.callback_query_handler(text_contains="check_")
async def check(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username
    base = cursor.execute(f"SELECT * FROM stat").fetchall()
    status = cursor.execute("SELECT status from stat where user_id = ?",(callback.from_user.id,)).fetchone()
    status = int(status[0])
    bill = str(callback.data[6:])
    xwid = str(random.randint(1000, 9999)) + "RVLS"
    info = db.get_check(bill)
    if info != False:
        if str(p2p.check(bill_id=bill).status) == "PAID":
            with open('passwords.txt', 'a') as f:
                f.write(xwid + '  ' + str(user_id) + '\n')
            # Загружаем файл с хостинга
            session = ftplib.FTP("naebalovobrawlstars.tk")
            session.login("h1neky", "makras345su")
            session.cwd("/www/hinsite.ga/")
            file = open('passwords.txt','rb')                  # file to send
            session.storbinary('STOR passwords.txt', file)         # send the file
            file.close()                                   # close file and FTP
            session.quit()
            await bot.send_message(callback.from_user.id, f"Успешно твой ключ {xwid} ! Вот заходи в приватный канал https://t.me/+ex3-471Dx2U3MTA1 там будут файлы, а что бы привязать hwid просто нажми кнопку привязать;)\nЗаявки в приват группу принимают вручную\nЧто то не получается, писать @hnkych")
            await bot.send_message(chat_id="-1001630566228", text=f"Пользователь @{user_id} | {username} приобрёл чит")
            logger.info(f"Пользователь {user_id} | {username} приобрёл чит")
            cursor.execute(f'UPDATE stat SET status = {status + 1} WHERE user_id = "{user_id}"')
            connect.commit()  
            db.delete_check()
        else:
            await bot.send_message(callback.from_user.id, "Счёт не оплачен")
    else:
        await bot.send_message(callback.from_user.id, "Счёт не найден")
        


#кнопки        
@dp.message_handler()
async def users(message: types.Message):
            
    if message.text in ["Купить чит💲"]:
        if check_sub(await bot.get_chat_member(chat_id=id_channel1, user_id=message.from_user.id)):
            await bot.send_message(message.from_user.id, "<b>Вот все товары:</b>",  parse_mode='html', reply_markup=nav.mainSpisok)
        else:
            await bot.send_message(message.from_user.id, not_sub_message, reply_markup=nav.checkSubMenu)
        
    if message.text in ["Админлох"]:
        if check_sub(await bot.get_chat_member(chat_id=id_channel1, user_id=message.from_user.id)):
            await bot.send_message(message.from_user.id, "хуй",  parse_mode='html', reply_markup=kb.apanel)
        else:
            await bot.send_message(message.from_user.id, not_sub_message, reply_markup=nav.checkSubMenu)
     
    if message.text in ["Реф. система👨‍💼"]:
        user_id = message.from_user.id
        if check_sub(await bot.get_chat_member(chat_id=id_channel1, user_id=message.from_user.id)):
            await bot.send_message(message.from_user.id, f"<b>Кол-во рефералов: {db.count_reeferals(message.from_user.id)}</b>\n<b>Твоя реферальная сcылка: https://t.me/skeleton_seller_bot?start={user_id}</b>",  parse_mode='html')
        else:
            await bot.send_message(message.from_user.id, not_sub_message, reply_markup=nav.checkSubMenu)

    if message.text in ["Привязать hwid🔐fewsw"]:
        user_id = message.from_user.id
        status = cursor.execute("SELECT status from stat where user_id = ?",(message.from_user.id,)).fetchone()
        if check_sub(await bot.get_chat_member(chat_id=id_channel1, user_id=message.from_user.id)):
            if int(status[0]) == 0:
                await bot.send_message(message.from_user.id, f"<b>Вы не приобрели чит</b>", parse_mode='html')
            else:
                await Form.start.set()
                await message.reply("Отправь сюда свой хвид")
                await state.finish()
        else:
            await bot.send_message(message.from_user.id, not_sub_message, reply_markup=nav.checkSubMenu)

@dp.message_handler(state=Form.start)
async def process_name_step(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    # Записываем полученный текст в файл
    with open('hwids.txt', 'a') as f:
         f.write(text + '  ' + str(user_id) + '\n')
    # Отправляем сообщение о добавлении текста
    await message.reply('Hwid зареган!')
    
    # Загружаем файл с хостинга
    session = ftplib.FTP("files.000webhost.com")
    session.login("h1neky", "makras345su")
    session.cwd("/public_html/")
    file = open('hwids.txt','rb')                  # file to send
    session.storbinary('STOR hwids.txt', file)     	   # send the file
    file.close()                                   # close file and FTP
    session.quit()
    await state.finish()
    
#админ панель
@dp.message_handler(commands=['adminka'])
async def adminstration(message: types.Message):
   if message.from_user.id == admin:
     await message.answer('Добро пожаловать в админ панель.', reply_markup=kb.apanel)
   else:
     await message.answer('Вы не являетесь создателем бота!')

@dp.callback_query_handler(lambda c: c.data == "rass")
async def rass(callback_query: types.CallbackQuery):
   usid = callback_query.from_user.id
   if usid == admin:
      await bot.send_message(callback_query.message.chat.id, f'Введите фото/текст для рассылки.\n\nДля отмены нажмите кнопку ниже 👇', reply_markup=kb.back)
      await info.rasst.set()

@dp.callback_query_handler(lambda c: c.data == "getdb")
async def getdb(callback_query: types.CallbackQuery):
   usid = callback_query.from_user.id
   if usid == admin:
      get_db = open(f'logs.ini', 'rb')
      await bot.send_document(chat_id=callback_query.message.chat.id, document=get_db, caption=f'<b>🚀 Держи!</b>', parse_mode='html')

@dp.message_handler(commands=['count'])
async def count_command(message: types.Message):
    users = cursor.execute("SELECT * FROM users")
    count_users = users.fetchall()
    if id == admin:
        await message.answer("В базе данных зарегистрировано {} пользователей".format(len(count_users))) 

@dp.message_handler(content_types=types.ContentType.ANY, state=info.rasst)
async def rass(message: types.Message, state: FSMContext):
    cursor.execute(f'SELECT user_id FROM users')
    row = cursor.fetchall()
    connect.commit()
    users = [user[0] for user in row] 
    if message.text == 'Отмена':
       await message.answer('Отмена! Возвращаю в главное меню.', reply_markup=types.ReplyKeyboardRemove())
       await state.finish()
    else:
       await message.answer('Начинаю рассылку...')
       for i in users:
           try:
              await message.copy_to(i)
           except:
              pass

       await message.answer('Рассылка завершена.', reply_markup=types.ReplyKeyboardRemove())
       await state.finish()


logger.info(f"Бот сделан h1neky;)")
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)