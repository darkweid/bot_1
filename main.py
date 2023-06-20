import time
import csv

import asyncio
import logging
# from background import keep_alive

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, BotCommand, URLInputFile
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, ContentType
from config import Config, load_config

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
logging.basicConfig(level=logging.INFO)

bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp: Dispatcher = Dispatcher()

URL_gift = 'https://drive.google.com/file/d/1HbQI6OHRXwdNeq9D3Dv_O7p5DkRKQBCh/view?usp=drivesdk'
URL_signup = 'https://kids-online.su/bot'
img_svetlana = 'AgACAgIAAxkDAAIEeWSHFhzfUTrsmjbf3S8acjj3ymCAAAJ3yDEbvRE5SIEPoGDXBAABZwEAAwIAA3kAAy8E'
img_pass = 'https://skr.sh/i/070623/ikrphYnm.png?download=1&name=%D0%A1%D0%BA%D1%80%D0%B8%D0%BD%D1%88%D0%BE%D1%82%2007-06-2023%2015:16:21.png'
img_guide = 'AgACAgIAAxkDAAIEg2SHGBRZ4aFx6tnCuHE-mG2FdU54AAJ_yDEbvRE5SFxSXLlJucLTAQADAgADeQADLwQ'
img_question1 = 'AgACAgIAAxkDAAIEhmSHGEw1mYR90_JgUYOgK9zxhkq_AAKEyDEbvRE5SB7rAYROgZ9PAQADAgADeQADLwQ'
img_question2 = 'AgACAgIAAxkDAAIEjmSHGHdJN22mIywbtMkIwduTkBOnAAKGyDEbvRE5SCUmYgaEW2HbAQADAgADeQADLwQ'
img_question3 = 'AgACAgIAAxkDAAIEkWSHGJ4aWbo0JVuc-RehCBYzhT1uAAKHyDEbvRE5SJNv0yRJrctpAQADAgADeQADLwQ'
img_question4 = 'AgACAgIAAxkDAAIElGSHGLj5K6aFb75dyD1_84KoTdykAAKfyDEbvRE5SH8VFmQN0ir_AQADAgADeQADLwQ'
img_question5 = 'AgACAgIAAxkDAAIEl2SHGNYUVoId0bVIFpWtmOhcN86dAAJvyDEbvRE5SLt2jt51AdV6AQADAgADeQADLwQ'
photo1 = 'AgACAgIAAxkDAAIEeWSHFhzfUTrsmjbf3S8acjj3ymCAAAJ3yDEbvRE5SIEPoGDXBAABZwEAAwIAA3kAAy8E'
text_timer = 'Вы просили напомнить, и мы напоминаем 😉\n\nВы можете поиграть сейчас или можем напомнить ещё раз'

img_svetlana, img_question1, img_question2, img_question3, img_question4, img_question5, img_guide = img_pass, img_pass, img_pass, img_pass, img_pass, img_pass, img_pass

flag_signup = False
flag_video = False
flag_read = False
flag_game = False
# handler для копирования id файла
file_ids = []
user_first_name = ' '
user_full_name = ' '
user_nick = ' '


@dp.message(Command('images1'))
async def upload_photo(message: types.Message):
    image_from_url = URLInputFile('')  # <-- ссылка здесь
    result = await message.answer_video(image_from_url, caption="Изображение по ссылке")
    file_ids.append(result.photo[-1].file_id)
    await message.answer(file_ids)


# id video via ValueError
# @dp.message(ContentType)
# async def video_file_id(message: types.Message):
#    await bot.send_message(message.from_user.id, "Ваше id video")
#    await message.answer(message.video.file_id)


quest_id = 0
counter = 0
dict_lex = {
    0: 'баллов',
    1: 'балл',
    2: 'балла',
    3: 'балла',
    4: 'балла',
    5: 'баллов',
    6: 'баллов',
    7: 'баллов',
    8: 'баллов',
    9: 'баллов',
    10: 'баллов'
}


async def send_message_to_admin(dp: Dispatcher, text=None):
    lst = [579649093]
    for i in range(len(lst)):
        await bot.send_message(lst[i], text)


# Меню
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start', description='Начать заново'),
        BotCommand(command='/contacts', description='Другие способы связи')
    ]
    await bot.set_my_commands(main_menu_commands)


# Создаем объекты кнопок
button_help: KeyboardButton = KeyboardButton(text='Помощь')
button_1: InlineKeyboardButton = InlineKeyboardButton(
    text='Узнать', callback_data='Узнать')
button_1_1: InlineKeyboardButton = InlineKeyboardButton(
    text='Читать', callback_data='Читать')
button_2: InlineKeyboardButton = InlineKeyboardButton(
    text='Играть', callback_data='Играть')
button_2_1: InlineKeyboardButton = InlineKeyboardButton(
    text='Через 1 час', callback_data='Напомнить через 1 час')
button_2_2: InlineKeyboardButton = InlineKeyboardButton(
    text='Через 4 часа', callback_data='Напомнить через 4 часа')
button_2_3: InlineKeyboardButton = InlineKeyboardButton(
    text='Через 24 часа', callback_data='Напомнить через 24 часа')
button_3_0: InlineKeyboardButton = InlineKeyboardButton(
    text='0', callback_data='балл 0')
button_3_1: InlineKeyboardButton = InlineKeyboardButton(
    text='1', callback_data='балл 1')
button_3_2: InlineKeyboardButton = InlineKeyboardButton(
    text='2', callback_data='балл 2')
button_3_3: InlineKeyboardButton = InlineKeyboardButton(
    text='Засчитано!', callback_data='Засчит')

button_4: KeyboardButton = KeyboardButton(text='Узнать результат')
button_5: InlineKeyboardButton = InlineKeyboardButton(
    text='🎁 Получить подарок 🎁', url=URL_gift)
button_6: InlineKeyboardButton = InlineKeyboardButton(
    text='✅  Записаться на бесплатное занятие  ✅', callback_data='signup_pressed')

button_6_URL: InlineKeyboardButton = InlineKeyboardButton(
    text='⭐ Нажмите ещё раз для регистрации ⭐', url=URL_signup)

button_video: InlineKeyboardButton = InlineKeyboardButton(text='Смотреть видео', callback_data='Смотреть видео')

# Создаем объект клавиатуры, добавляя в него кнопки
keyboard_help: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_help]],

                                                         resize_keyboard=True,
                                                         input_field_placeholder='Для справки нажмите')
keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_1]])
keyboard1_1: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_1_1]])
keyboard2: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_2], [button_2_1, button_2_2, button_2_3]])
keyboard2_error: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_2]],
                                                           resize_keyboard=True)
keyboard3: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_3_0, button_3_1, button_3_2]])
keyboard3_3: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[button_3_3]])
keyboard4: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_4]],
                                                     resize_keyboard=True)

keyboard_gift: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_5]])
keyboard_signup: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_6]])
keyboard_game: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_6]])

keyboard_video: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[button_video]])

keyboard_url: InlineKeyboardMarkup = types.InlineKeyboardMarkup(inline_keyboard=[[button_6_URL]])


@dp.message(Command(commands=["sending1"]))
async def process_send_command(message: Message):
    lst = [579649093, 6191802805]
    for i in range(len(lst)):
        await bot.send_message(lst[i], 'privet')

# Этот хэндлер будет срабатывать на команду "/start" __
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    global user_first_name
    user_first_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    with open('log.csv', 'a', encoding='utf-8') as log_file:
        log_data = [
            message.from_user.id, message.from_user.full_name,
            message.from_user.username, message.from_user.is_bot,
            time.strftime('%H:%M :: %d/%m/%Y'), time.tzname
        ]
        writer = csv.writer(log_file, delimiter=',')
        writer.writerow(log_data)
    await message.answer_photo(photo=img_svetlana,
                               caption=f"""Здравствуйте, {user_full_name}! \nМеня зовут Светлана Заиграева, я – педагог и основатель онлайн-школы, в которой мы помогаем детям и их родителям подготовиться к школе: научиться читать, считать и любить учиться.
\nПоследние два года я изучала тему подготовки к школе не просто как учитель, но и как мама: мой сын в этом году будет поступать в школу.
\nИ с вами я делюсь этой информацией. Хотите узнать, что должен ребенок знать и уметь к поступлению в первый класс? """,
                               reply_markup=keyboard1)


# Получить гайд
@dp.callback_query(Text(text='Узнать'))
async def process_guide_answer(callback: types.CallbackQuery):
    with open('log_Узнать.csv', 'a', encoding='utf-8') as log_file:
        log_data = [
            callback.from_user.id, callback.from_user.full_name,
            callback.from_user.username, callback.from_user.is_bot,
            time.strftime('%H:%M :: %d/%m/%Y'), time.tzname
        ]
        writer = csv.writer(log_file, delimiter=',')
        writer.writerow(log_data)
    await callback.message.answer_photo(photo=img_guide)
    await callback.answer()
    await asyncio.sleep(15)
    await callback.message.answer(f"""Список умений, которые необходимы в школе внушительный, но самым главным является <b>ЧТЕНИЕ</b>.
\nЧасто к нам приходят детки, которых уже учили читать. После неудачных попыток у ребенка формируются затруднения, которые мешают ему освоить этот навык.
\nКак правило, это последствия одних и тех же ошибок, которые, к сожалению, допускают даже некоторые педагоги.
\nДавайте, я расскажу вам про самые популярные ошибки и о том, как их избежать?""", reply_markup=keyboard1_1)
    await asyncio.sleep(20)
    if flag_read == False or (flag_read == True and flag_game == False): #'BAACAgIAAxkBAAIGfWSKD7Bk92UqhDUh8kPNTNVX2DoqAAJfKwAC90BQSFYMoFQJpBDKLwQ'
        await callback.message.answer_video(img_pass)
        await callback.message.answer(f"""Хотите, чтобы ребенок учился с таким же интересом?
\nТогда приходите к нам 😊
\nМы точно знаем, как сделать занятия полезными и интересными. Приходите к нам на бесплатный урок и убедитесь сами!""",
                                      reply_markup=keyboard_signup)


@dp.callback_query(Text(text='Читать'))
async def process_guide_errors(callback: types.CallbackQuery):
    global flag_read
    flag_read = True
    with open('log_Читать.csv', 'a', encoding='utf-8') as log_file:
        log_data = [
            callback.from_user.id, callback.from_user.full_name,
            callback.from_user.username, callback.from_user.is_bot,
            time.strftime('%H:%M :: %d/%m/%Y'), time.tzname
        ]
        writer = csv.writer(log_file, delimiter=',')
        writer.writerow(log_data)
    global user_nick
    global user_full_name
    user_full_name = callback.from_user.full_name
    user_nick = callback.from_user.username
    await callback.answer()
    await callback.message.answer(f"""Итак, <b>ошибка №1</b>
❌ Изучать одновременно и буквы, и звуки. Например, часто детям говорят "Это буква ЭМ, она обозначает звук М".
\nДля любого ребенка обучение чтению – стресс и очень сложная задача. Когда мы на каждую символ даём ребенку два значения (звук и буква), ребенок теряется, путается и, что самое обидное, теряет интерес.
\n✅ Как лучше: на первых этапах изучайте только буквы как звуки. Вы сможете их легко разделить после того, как ребенок уже освоит навык и начнет читать и понимать целые предложения""")

    await callback.message.answer(f"""<b>Ошибка №2</b>
❌ Часто при изучении букв ребенка перегружают информацией: рассказывают сразу и про гласные и негласные, и про твердые и мягкие, глухие и звонкие. Иногда ребенок уже знает, про звукобуквенный анализ слов, но ещё не умеет читать.
\nКонечно, такое обилие информации только мешает ребенку начать читать. Задача кажется ему непосильной и пугающей.
\n✅ Как лучше: исключите грамматику до тех пор, пока не поймете, что ребенок уверенно читает предложения и понимает смысл прочитанного.""")

    await callback.message.answer(f"""<b>Ошибка №3</b>
❌ Предлагать ребенку читать слова сразу же после того, как он научился сливать звуки в слоги.
\nЯ понимаю стремление многих родителей научить как можно скорее, но в сложных навыках (а вашему ребенку, поверьте, этот навык сейчас кажется очень сложным) нужно проявить терпение.
\n✅ Как лучше: прорабатывать каждый этап очень тщательно и только потом переходить к следующему. То есть, ребенок должен сначала научиться читать слоги не задумываясь, не проговаривая и не путая буквы.
\nИменно эта ошибка часто приводит к тому, что ребенок долгое время остается на этапе побуквенного чтения и не понимает смысл прочитанного. К сожалению, с такими детьми нам приходится возвращаться к самому началу и снова учиться читать слоги.""")

    await asyncio.sleep(15)
    await callback.message.answer(
        f"""Итак, ошибки учли, со списком умений и навыков мы разобрались, но как же понять, насколько ими овладел ваш ребенок?
\nС этим я тоже могу помочь! И тоже бесплатно :)
\nНачнем с чтения: самого важного навыка, именно от него зависит, насколько успешным и легким будет первый школьный год.
\nПредложите вашему малышу сыграть в небольшую игру. В ней всего 10 заданий, на это уйдет не больше 10 минут.
\nА тех, кто пройдет игру до конца ждёт небольшой подарок: <b>бесплатное развивающее пособие "Курс по тренировке мозга на 21 день"</b>, который подойдет деткам от 5 до 7 лет.
\nКогда вы с малышом будете готовы, нажимайте на кнопку ниже
Или мы можем напомнить через нужное вам время
""",
        reply_markup=keyboard2)


# Таймеры на игру
@dp.callback_query(Text(text='Напомнить через 1 час'))
async def process_game_timer1(callback: types.CallbackQuery):
    await callback.message.answer('Хорошо, мы вам напомним через 1 час 👌')
    await callback.answer()
    await asyncio.sleep(15)
    await callback.message.answer(text_timer, reply_markup=keyboard2)


@dp.callback_query(Text(text='Напомнить через 4 часа'))
async def process_game_timer4(callback: types.CallbackQuery):
    await callback.message.answer('Хорошо, мы вам напомним через 4 часа 👌')
    await callback.answer()
    await asyncio.sleep(15)
    await callback.message.answer(text_timer, reply_markup=keyboard2)


@dp.callback_query(Text(text='Напомнить через 24 часа'))
async def process_game_timer24(callback: types.CallbackQuery):
    await callback.message.answer('Хорошо, мы вам напомним через 24 часа 👌')
    await callback.answer()
    await asyncio.sleep(15)
    await callback.message.answer(text_timer, reply_markup=keyboard2)


# Играть
@dp.callback_query(Text(text='Играть'))
async def process_game_answer(callback: types.CallbackQuery):
    global flag_game
    flag_game = True
    with open('log_Играть.csv', 'a', encoding='utf-8') as log_file:
        log_data = [
            callback.from_user.id, callback.from_user.full_name,
            callback.from_user.username, callback.from_user.is_bot,
            time.strftime('%H:%M :: %d/%m/%Y'), time.tzname
        ]
        writer = csv.writer(log_file, delimiter=',')
        writer.writerow(log_data)
    global user_first_name
    user_first_name = callback.from_user.first_name
    await callback.message.answer(text='Выберите количество баллов за выполненные задания при помощи кнопок')
    await callback.message.answer_photo(photo=img_question1,
                                        reply_markup=keyboard3)
    await callback.answer()


@dp.callback_query(Text(startswith='балл'))
async def process_game_answer3(callback: types.CallbackQuery):
    global quest_id
    global counter
    global flag_signup
    global flag_video
    global user_first_name
    user_first_name = callback.from_user.first_name
    counter += int(callback.data.split()[-1])
    await callback.message.edit_reply_markup(reply_markup=keyboard3_3)
    if quest_id == 0:  # кнопка срабатывает первый раз
        await callback.message.answer_photo(photo=img_question2, reply_markup=keyboard3)
        quest_id = 1
    elif quest_id == 1:
        await callback.message.answer_photo(photo=img_question3, reply_markup=keyboard3)
        quest_id = 2
    elif quest_id == 2:
        await callback.message.answer_photo(photo=img_question4, reply_markup=keyboard3)
        quest_id = 3
    elif quest_id == 3:  # кнопка срабатывает четвертый раз
        await callback.message.answer_photo(photo=img_question5, reply_markup=keyboard3)
        quest_id = 4
    elif quest_id == 4:
        if 0 <= counter <= 3:
            await callback.message.answer('Спасибо за игру!')
            await callback.message.answer(
                f"""{user_first_name}, ваш ребёнок набрал {counter} {dict_lex[counter]} из 10. Не пугайтесь, это говорит лишь о том, что к поступлению в школу нужно подготовиться, чтобы учеба в школе проходила без трудностей.
\nЯ, как мама, отлично понимаю, как сложно найти время на занятия и как тяжело бывает уговорить ребенка заниматься. Дело в том, что иногда детям очень тяжело воспринимать родителя как учителя. Но я могу вам с этим помочь!
\nПриходите к нам на бесплатное занятие: опытный педагог проведет диагностику, поделится нашими методами и даст рекомендации для вашего ребенка.


 """,
                reply_markup=keyboard_signup)
            await callback.message.answer(
                'Не забудьте ваш подарок: развивающее пособие "Курс по тренировке мозга на 21 день" ',
                reply_markup=keyboard_gift)
        elif 4 <= counter <= 6:
            await callback.message.answer('Спасибо за игру!')
            await callback.message.answer(
                f"""{user_first_name}, ваш ребёнок набрал {counter} {dict_lex[counter]}. Это говорит о том, что у ребенка уже развиты базовые навыки, но их пока немножко недостаточно, для успешного старта в школе. Стоит уделить особое внимание тем заданиям, которые вызвали сложности.
\nЯ, как мама, отлично понимаю, как сложно найти время на занятия и как тяжело бывает уговорить ребенка заниматься. Дело в том, что иногда детям очень тяжело воспринимать родителя как учителя. Но я могу вам с этим помочь!
\nПриходите к нам на бесплатное занятие: опытный педагог проведет диагностику, поделится нашими методами и даст рекомендации для вашего ребенка.""",
                reply_markup=keyboard_signup)
            await callback.message.answer(
                'Не забудьте ваш подарок: развивающее пособие "Курс по тренировке мозга на 21 день" ',
                reply_markup=keyboard_gift)
        elif 7 <= counter <= 10:
            await callback.message.answer('Спасибо за игру!')
            await callback.message.answer(
                f"""{user_first_name}, ваш ребёнок набрал {counter} {dict_lex[counter]}! Это отличный результат, которого удаётся добиться далеко не всем родителям и педагогам. Поздравляю!
\nПосле того, как ребенок научился читать, очень важно продолжать регулярно тренировать этот навык. Я, как мама, отлично понимаю, как сложно найти время на занятия и как сильно иногда хочется, чтобы ребенок научился всему сам :)
\nПриходите к нам на бесплатное занятие: опытный педагог проведет диагностику, расскажет про наши методы и даст рекомендации для вашего ребенка.""",
                reply_markup=keyboard_signup)
            await callback.message.answer(
                'Не забудьте ваш подарок: развивающее пособие "Курс по тренировке мозга на 21 день" ',
                reply_markup=keyboard_gift)
        else:
            await callback.message.answer(
                f"""Некорректное количество баллов! Пройдите задания заново. Нажимайте кнопку внизу""",
                reply_markup=keyboard2)

        quest_id = 0
        counter = 0
        await asyncio.sleep(30)
        if flag_signup == False:
            await callback.message.answer(
                f"""Ко мне часто приходят родители со словами: "мы уже пытались учиться читать, но никак не получается".
Я вас понимаю, я часто такое вижу в своей практике.
\nУ нас есть опыт обучения разных детей, с разными особенностями и характерами. К любому ребенку можно найти подход.  Посмотрите короткое видео о том, КАК интересно проходят у нас уроки.
Обещаю, ваше представление об обучении навсегда изменится 😊""",
                reply_markup=keyboard_video)
            await asyncio.sleep(30)
            if flag_video == False:
                await callback.message.answer_video(
                    'BAACAgIAAxkBAAIGfWSKD7Bk92UqhDUh8kPNTNVX2DoqAAJfKwAC90BQSFYMoFQJpBDKLwQ')
                await callback.message.answer(f"""Хотите, чтобы ребенок учился с таким же интересом?
\nТогда приходите к нам 😊
\nМы точно знаем, как сделать занятия полезными и интересными. Приходите к нам на бесплатный урок и убедитесь сами!""",
                                              reply_markup=keyboard_signup)


@dp.callback_query(Text(text='Засчит'))
async def process_game_answer2(callback: types.CallbackQuery):
    callback.answer()


@dp.callback_query(Text(text='signup_pressed'))
async def callbacks_num(callback: types.CallbackQuery):
    with open('log_Регистрация.csv', 'w', encoding='utf-8') as log_file:
        log_data = [
            callback.from_user.id, callback.from_user.full_name,
            callback.from_user.username, callback.from_user.is_bot,
            time.strftime('%H:%M :: %d/%m/%Y'), time.tzname
        ]
        writer = csv.writer(log_file, delimiter=',')
        writer.writerow(log_data)
    global flag_signup
    global user_nick
    global user_full_name
    await callback.message.edit_reply_markup(reply_markup=keyboard_url)
    await callback.answer()
    await send_message_to_admin(dp, text=f"Нажата кнопка регистрации!\n@{user_nick} | {user_full_name}")
    flag_signup = True


# ссылка на материал
@dp.message(Text(text='Помощь'))
async def process_result_help(message: Message):
    await message.answer(f"""нажмите /start для перезапуска бота\nнажмите /contacts для связи с командой школы""")


@dp.message(Text(text='Смотреть видео'))
async def process_result_answer(message: Message):
    with open('log_Видео.csv', 'a', encoding='utf-8') as log_file:
        log_data = [
            callback.from_user.id, callback.from_user.full_name,
            callback.from_user.username, callback.from_user.is_bot,
            time.strftime('%H:%M :: %d/%m/%Y'), time.tzname
        ]
        writer = csv.writer(log_file, delimiter=',')
        writer.writerow(log_data)
    global flag_video
    await message.answer_video('BAACAgIAAxkBAAIGfWSKD7Bk92UqhDUh8kPNTNVX2DoqAAJfKwAC90BQSFYMoFQJpBDKLwQ',
                               reply_markup=keyboard_help)
    flag_video = True
    await message.answer(f"""Хотите, чтобы ребенок учился с таким же интересом?
\nТогда приходите к нам 😊
\nМы точно знаем, как сделать занятия полезными и интересными. Приходите к нам на бесплатный урок и убедитесь сами!""",
                         reply_markup=keyboard_signup)


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Здесь будет описание функций бота')


# Этот хэндлер будет срабатывать на команду "/contacts"
@dp.message(Command(commands=['contacts']))
async def process_help_command(message: Message):
    await message.answer(
        'Онлайн-школа Светланы Заиграевой \n"Kids online"\nhttps://kids-online.su\n+7-923-689-07-98\nsvetlana_zaigraeva@mail.ru'
    )


# Этот хэндлер будет срабатывать на любые  текстовые сообщения, кроме команд "/start"  "/help" "/contacts"


@dp.message()
async def send_idontknow(message: Message):
    await message.reply('Я всего лишь бот, я не знаю, что на это ответить🤷🏼‍♀')


if __name__ == '__main__':
    #    keep_alive()
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)
