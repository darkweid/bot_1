import time
import csv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, BotCommand
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup,ReplyKeyboardRemove
from config import Config, load_config

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
# просто коммент

bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()

URL_gift = 'https://drive.google.com/file/d/1HbQI6OHRXwdNeq9D3Dv_O7p5DkRKQBCh/view?usp=drivesdk'
URL_signup = 'https://kids-online.su/bot'
img_svetlana = 'https://i.imgur.com/T04VVfl.jpg'
img_pass = 'https://skr.sh/i/070623/ikrphYnm.png?download=1&name=%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%2007-06-2023%2015:16:21.png'
img_guide = 'https://i.imgur.com/VHbyVyS.jpg'
img_question1 = 'https://i.imgur.com/YXPMuPy.jpg'
img_question2 = 'https://i.imgur.com/I8u15VD.jpg'
img_question3 = 'https://i.imgur.com/ZZU1SRn.jpg'
img_question4 = 'https://i.imgur.com/HgDRNfy.jpg'
img_question5 = 'https://i.imgur.com/1uMcv7k.jpg'
quest_id = 0
counter = 0
dict_lex = {0:'баллов', 1:'балл', 2:'балла', 3:'балла', 4:'балла',
            5:'баллов', 6:'баллов', 7:'баллов', 8:'баллов', 9:'баллов', 10:'баллов'}
# Меню
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Начать заново'),
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/contacts',
                   description='Другие способы связи')]
    await bot.set_my_commands(main_menu_commands)


# Создаем объекты кнопок
button_1: KeyboardButton = KeyboardButton(text='Узнать')
button_2: KeyboardButton = KeyboardButton(text='Играть')
button_3: KeyboardButton = KeyboardButton(text='Следующий вопрос')
button_3_0: KeyboardButton = KeyboardButton(text='0 баллов')
button_3_1: KeyboardButton = KeyboardButton(text='1 балл')
button_3_2: KeyboardButton = KeyboardButton(text='2 балла')
button_4: KeyboardButton = KeyboardButton(text='Узнать результат')
button_5: KeyboardButton = KeyboardButton(text='Получить подарок 🎁')
button_6: InlineKeyboardButton = InlineKeyboardButton(text='Записаться на пробное занятие',
                                                      url=URL_signup)
# Создаем объект клавиатуры, добавляя в него кнопки
keyboard1: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_1]],
                                    resize_keyboard=True)
keyboard2: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_2]],
                                    resize_keyboard=True)
keyboard3: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard =[[button_3_0, button_3_1, button_3_2]],
                                    resize_keyboard=True)
keyboard4: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard =[[button_4]],
                                    resize_keyboard=True)
keyboard_gift: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard =[[button_5]],
                                    resize_keyboard=True)
keyboard_signup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard = [[button_6]])
keyboard_game = InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard = [[button_6]])



# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    user_full_name = message.from_user.full_name
    with open('log.csv', 'a', encoding='utf-8') as log_file:
        log_data = [message.from_user.id, message.from_user.full_name, message.from_user.username,
                    message.from_user.is_bot,time.strftime('%H:%M %x'), time.tzname]
        writer = csv.writer(log_file, delimiter=',')
        writer.writerow(log_data)
    await message.answer_photo(photo= img_svetlana, caption=f"""Привет, {user_full_name}! Меня зовут Светлана Заиграева.
\nЯ основатель онлайн-школы, в которой мы учим детей читать, считать и многому другому.
Если вашему ребенку 5-7 лет, то пора думать о школе. Хотите узнать, что должен знать и уметь ребёнок к школе?
Моему сыну 6 лет. За последние два года я изучила эту тему досконально.
\nИ с вами хочу поделиться этой информацией совершенно бесплатно: "Что должен знать и уметь ребёнок к школе" """, reply_markup=keyboard1)



#Получить гайд
@dp.message(Text(text='Узнать'))
async def process_guide_answer(message: Message):
    await message.answer_photo(photo=img_guide ,reply_markup=ReplyKeyboardRemove())
    time.sleep(5)
    await message.answer(f"""Прямо сейчас у вас есть возможность проверить насколько развит у вашего ребёнка базовый навык: ЧТЕНИЕ.

Ведь успех в школе с первых дней зависит именно от чтения. Может ли ребёнок прочитать текст, задания и понять, что необходимо сделать.

Если вы хотите УЗНАТЬ УРОВЕНЬ ГОТОВНОСТИ К ШКОЛЕ - предлагаю игру.  Пройдите с вашим ребёнком игру. Ему нужно будет выполнить 5 заданий. За каждый верный ответ - 1 балл.
А в конце получите развивающее пособие совершенно бесплатно

"Курс по тренировке мозга на 21 день" Подойдет для детей 5-7 лет.

Нажимайте на кнопку ниже. Это займёт не более 10 минут.
""", reply_markup=keyboard2)


#Играть
@dp.message(Text(text='Играть'))
async def process_game_answer1(message: Message):
    await message.answer_photo(photo=img_question1,
                         reply_markup=keyboard3)
#Следующий вопрос
@dp.message(Text(text=['0 баллов', '1 балл', '2 балла']))
async def process_game_answer2(message: Message):
    global quest_id
    global counter
    user_name = message.from_user.first_name
    if quest_id == 0:                                 #кнопка срабатывает первый раз
        await message.answer_photo(photo=img_question2,reply_markup=keyboard3)
        counter += int(message.text[0])
        quest_id = 1
    elif quest_id == 1:
        await message.answer_photo(photo=img_question3, reply_markup=keyboard3)
        counter += int(message.text[0])
        quest_id = 2
    elif quest_id == 2:
        await message.answer_photo(photo=img_question4, reply_markup=keyboard3)
        counter += int(message.text[0])
        quest_id = 3
    elif quest_id == 3:                                             #кнопка срабатывает четвертый раз
        await message.answer_photo(photo=img_question5, reply_markup=keyboard3)
        counter += int(message.text[0])
        quest_id = 4
    elif quest_id == 4:
        counter += int(message.text[0])
        if 0 <= counter <= 3:
            await message.answer(f"""{user_name}, ваш ребёнок набрал {counter} {dict_lex[counter]}
Ребёнок обладает еще недостаточными знаниями и навыками по чтению, чтобы идти в школу.
\nКак обещали, дарим вам пособие для развития вашего ребенка! """, reply_markup=keyboard_gift)
        elif 4 <= counter <= 6:
            await message.answer(f"""{user_name}, ваш ребёнок набрал {counter} {dict_lex[counter]}.
У ребёнка развиты базовые навыки, но недостаточно для школы.
Обратите внимание на те упражнения, которые вызвали сложность и поделайте подобные задания.
\nКак обещали, дарим вам пособие для развития вашего ребенка!""", reply_markup=keyboard_gift)
        elif 7 <= counter <= 10:
            await message.answer(f"""{user_name}, ваш ребёнок набрал {counter} {dict_lex[counter]}!
Поздравляем, ваш малыш обладает важными навыками для успешного обучения в школе.
\nКак обещали, дарим вам пособие для развития вашего ребенка!""", reply_markup=keyboard_gift)
        else:
            await message.answer(f"""Некорректное количество баллов! Пройдите задания заново. Введите команду /start""", reply_markup=keyboard_gift)

        quest_id = 0
        counter = 0
#ссылка на материал
@dp.message(Text(text='Получить подарок 🎁'))
async def process_result_answer(message: Message):
    await message.answer(f"""⬇️Открывайте пособие по ссылке на GoogleDisk⬇️\n{URL_gift}""",reply_markup=ReplyKeyboardRemove())
    time.sleep(15)
    await message.answer(f"""Мы рады знакомству с вами и хотим сделать ещё один подарок!
\nПриглашаем вас на БЕСПЛАТНОЕ ЗАНЯТИЕ в нашу онлайн школу.
На занятии опытный педагог проведет диагностику, покажет, как проходят у нас занятия, и даст рекомендации для вашего ребёнка. 
Всё это совершенно бесплатно и вас ни к чему не обязывает.""", reply_markup= keyboard_signup)

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Здесь будет описание функций бота')


# Этот хэндлер будет срабатывать на команду "/contacts"
@dp.message(Command(commands=['contacts']))
async def process_help_command(message: Message):
    await message.answer('Онлайн-школа Светланы Заиграевой \n"Kids online"\nhttps://kids-online.su\n+7-923-689-07-98\nsvetlana_zaigraeva@mail.ru')


# Этот хэндлер будет срабатывать на любые  текстовые сообщения, кроме команд "/start"  "/help" "/contacts"
@dp.message()
async def send_idontknow(message: Message):
    await message.reply('Я всего лишь бот, я не знаю, что на это ответить🤷🏼‍♀')


if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)
