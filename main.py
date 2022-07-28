import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('')

conn = sqlite3.connect('db/database.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, review: str):
	cursor.execute('INSERT INTO test (user_id, user_name, user_surname, username, review) VALUES (?, ?, ?, ?, ?)', (user_id, user_name, user_surname, username, review))
	conn.commit()

@bot.message_handler(commands=['start'])
def start(message, res=False):

    # Добавляем кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    about = types.KeyboardButton("Обо мне")
    edu = types.KeyboardButton("Образование")
    job = types.KeyboardButton("Опыт работы")
    skills = types.KeyboardButton("Навыки")
    qs = types.KeyboardButton("Частые вопросы")
    contacts = types.KeyboardButton("Контакты")
    review = types.KeyboardButton("Оставить отзыв")
    markup.add(about)
    markup.add(edu)
    markup.add(job)
    markup.add(skills)
    markup.add(qs)
    markup.add(contacts)
    markup.add(review)
    bot.send_message(message.from_user.id,
                     "Здравствуйте, этот бот призван рассказать обо мне в более широком формате, чем обычное резюме. \nНажмите на кнопку в меню.",
                     reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message, res=False):
    bot.send_message(message.from_user.id, "Здравствуйте, этот бот призван рассказать обо мне в более широком формате, чем обычное резюме. \nНажмите на кнопку в меню.")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text.strip() == "Обо мне":
        answer = "Лола Бозорова, 20 лет"
    elif message.text.strip() == "Образование":
        answer = "Обучаюсь на 4 курсе в РТУ МИРЭА"
    elif message.text.strip() == "Опыт работы":
        answer = "2021-2022\nВедущий специалист отдела сопровождения процессинга Альфа-Банк\n•	Работа с базами данных с помощью SQL\n•	Написание скриптов для автоматизации на Python\n•	Администрирование высоконагруженных серверов на Linux\n•	Создание дашбордов в Grafana"
    elif message.text.strip() == "Навыки":
        answer = "Python, R, SQL, Excel, Power BI, Tableau, Git, Jira, Grafana, Elasticsearch, Нейронные сети, ML, Linux, bash, английский язык"
    elif message.text.strip() == "Частые вопросы":
        answer = "Частые вопросы"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        salary = types.KeyboardButton("Зарплатные ожидания")
        leave = types.KeyboardButton("Причина ухода с предыдущего места работы")
        time = types.KeyboardButton("Предпочитаемый график работы")
        uni = types.KeyboardButton("Совмещение работы и учебы")
        markup.add(salary)
        markup.add(leave)
        markup.add(time)
        markup.add(uni)
        bot.send_message(message.from_user.id,
                         "Нажмите на кнопку в меню. Чтобы вернуться в главное меню, нажмите /start",
                         reply_markup=markup)
    elif message.text.strip() == "Контакты":
        answer = "Почта: l0la-02@yandex.ru \nТелефон, whatsapp: +79180809206 \nTelegram: @i1034"
    elif message.text.strip() == "Зарплатные ожидания":
        answer = "От 30 тыс. рублей"
    elif message.text.strip() == "Причина ухода с предыдущего места работы":
        answer = "Очень неприятный коллектив"
    elif message.text.strip() == "Предпочитаемый график работы":
        answer = "Любой, не против удаленной работы"
    elif message.text.strip() == "Совмещение работы и учебы":
        answer = "В университете нет требования посещать занятия, необходимо только являться на сессию"
    elif message.text.strip() == "Оставить отзыв":
        msg = bot.send_message(message.chat.id, "Вводите текст")
        bot.register_next_step_handler(msg, rev)
    else:
        answer = "Бот не принимает рандомный текст"
    bot.send_message(message.chat.id, answer)

def rev(message):
    bot.send_message(message.chat.id, "Ваш ответ записан")
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username

    db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username, message=message)


bot.polling(none_stop=True, interval=0)
