import telebot
from telebot import types

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

user_data = {}
group_schedule = {}

# Расписание для групп
schedule_data = {
    "Группа 1-МД-13": {
        "odd_week": {  # Нечетная неделя
            "понедельник": "Операционные системы, сети и телекоммуникации (10:05-11:30)\n Алгоритмизация и программирование (11:40-13:05) Математика (13:45-15:10)",
            "вторник": "Математика (10:05-11:30)\n  Операционные системы, сети и телекоммуникации (11:40-13:05) История России (13:45-15:10)",
            "среда": "Физ-ра (15:20-16:45)\n  Иностранный язык (16:55-18:20) Физика (18:30-20:00)",
            "четверг": "Физика (10:05-11:30)\n  Русский язык (11:40-13:05)",
            "пятница": "Дизайн-проектирование (08:30-09:55)\n  История России (10:05-11:30) Математика (11:40-13:05) Алгоритмизация и программирование (13:45-15:10)",
            "суббота": "✌️ Выходной",
            "воскресенье": "✌️ Выходной"
        },
        "even_week": {  # Четная неделя
            "понедельник": "Операционные системы, сети и телекоммуникации (10:05-11:30)\n Алгоритмизация и программирование (11:40-13:05) Математика (13:45-15:10)",
            "вторник": "Математика (10:05-11:30)\n  Операционные системы, сети и телекоммуникации (11:40-13:05) История России (13:45-15:10)",
            "среда": "Физ-ра (15:20-16:45)\n  Иностранный язык (16:55-18:20) Физика (18:30-20:00)",
            "четверг": "Физика (10:05-11:30)\n  Русский язык (11:40-13:05)",
            "пятница": "Дизайн-проектирование (08:30-09:55)\n  История России (10:05-11:30) Математика (11:40-13:05) Алгоритмизация и программирование (13:45-15:10)",
            "суббота": "✌️ УРА!!! Выходной",
            "воскресенье": "✌️ УРА!!! Выходной"
        }
    },
    "Группа 1-МД-35": {
        "odd_week": {
            "понедельник": "📚 Математика (9:00-10:30)\n📖 Физика (11:00-12:30)",
            # ... остальные дни
        },
        "even_week": {
            "понедельник": "📖 Физика (9:00-10:30)\n📚 Математика (11:00-12:30)",
            # ... остальные дни
        }
    }
}


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    user_data[user_id] = {'step': 'awaiting_first_name'}

    bot.send_message(user_id, '👋 Добро пожаловать! Введите ваше имя:')


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('step') == 'awaiting_first_name')
def get_first_name(message):
    user_id = message.chat.id
    user_data[user_id]['first_name'] = message.text
    user_data[user_id]['step'] = 'awaiting_last_name'

    bot.send_message(user_id, '📝 Теперь введите вашу фамилию:')


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('step') == 'awaiting_last_name')
def get_last_name(message):
    user_id = message.chat.id
    user_data[user_id]['last_name'] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Группа 1-МД-13')
    btn2 = types.KeyboardButton('Группа 1-МД-35')
    btn3 = types.KeyboardButton('Группа 1-МД-20')
    markup.add(btn1, btn2, btn3)

    user_data[user_id]['step'] = 'awaiting_group'
    bot.send_message(user_id,
                     f"✅ Отлично, {user_data[user_id]['first_name']} {user_data[user_id]['last_name']}!\n\nТеперь выберите вашу группу:",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('step') == 'awaiting_group')
def get_group(message):
    user_id = message.chat.id
    user_data[user_id]['group'] = message.text
    user_data[user_id]['step'] = 'registered'

    markup = types.ReplyKeyboardRemove()
    bot.send_message(user_id,
                     f"🎉 Регистрация завершена!\n\n👤 Имя: {user_data[user_id]['first_name']}\n📌 Фамилия: {user_data[user_id]['last_name']}\n🎓 Группа: {user_data[user_id]['group']}",
                     reply_markup=markup)

    show_main_menu(user_id)


def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('📅 Расписание на сегодня')
    btn2 = types.KeyboardButton('📆 Расписание на неделю')
    btn3 = types.KeyboardButton('📝 Выбрать день')
    btn4 = types.KeyboardButton('🔄 Сменить группу')
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(chat_id, "📋 Главное меню:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '📅 Расписание на сегодня')
def schedule_today(message):
    user_id = message.chat.id
    if user_id not in user_data or 'group' not in user_data[user_id]:
        bot.send_message(user_id, "⚠️ Сначала пройдите регистрацию! Введите /start")
        return

    group = user_data[user_id]['group']
    day_of_week = datetime.today().strftime('%A').lower()

    # Перевод дней недели
    days_translation = {
        'monday': 'понедельник',
        'tuesday': 'вторник',
        'wednesday': 'среда',
        'thursday': 'четверг',
        'friday': 'пятница',
        'saturday': 'суббота',
        'sunday': 'воскресенье'
    }

    day_russian = days_translation.get(day_of_week, day_of_week)

    # Определяем четность недели
    week_number = datetime.datetime.now().isocalendar()[1]
    week_type = "odd_week" if week_number % 2 == 1 else "even_week"
    week_type_text = "нечетная" if week_number % 2 == 1 else "четная"

    if group in schedule_data:
        schedule = schedule_data[group][week_type].get(day_russian, "❌ Занятий нет")

        # Отправляем фото расписания
        photo_id = schedule_photos.get(week_type)
        if photo_id:
            bot.send_photo(user_id, photo_id,
                           caption=f"📅 Расписание на {day_russian} ({week_type_text} неделя)\n\n{schedule}")
        else:
            bot.send_message(user_id, f"📅 Расписание на {day_russian} ({week_type_text} неделя):\n\n{schedule}")
    else:
        bot.send_message(user_id, "❌ Для вашей группы расписание не найдено")


@bot.message_handler(func=lambda message: message.text == '📆 Расписание на неделю')
def schedule_week(message):
    user_id = message.chat.id
    if user_id not in user_data or 'group' not in user_data[user_id]:
        bot.send_message(user_id, "⚠️ Сначала пройдите регистрацию! Введите /start")
        return

    group = user_data[user_id]['group']

    # Определяем четность недели
    week_number = datetime.datetime.now().isocalendar()[1]
    week_type = "odd_week" if week_number % 2 == 1 else "even_week"
    week_type_text = "нечетная" if week_number % 2 == 1 else "четная"

    if group in schedule_data:
        schedule = schedule_data[group][week_type]
        response = f"📅 Расписание на неделю ({week_type_text} неделя):\n\n"

        for day, lessons in schedule.items():
            response += f"📌 {day.capitalize()}:\n{lessons}\n\n"

        # Отправляем фото расписания
        photo_id = schedule_photos.get(week_type)
        if photo_id:
            bot.send_photo(user_id, photo_id, caption=response[:1024])
        else:
            bot.send_message(user_id, response)
    else:
        bot.send_message(user_id, "❌ Для вашей группы расписание не найдено")


@bot.message_handler(func=lambda message: message.text == '📝 Выбрать день')
def choose_day(message):
    user_id = message.chat.id
    if user_id not in user_data or 'group' not in user_data[user_id]:
        bot.send_message(user_id, "⚠️ Сначала пройдите регистрацию! Введите /start")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    for day in days:
        markup.add(types.KeyboardButton(day))
    markup.add(types.KeyboardButton('⬅️ Назад'))

    bot.send_message(user_id, "📅 Выберите день недели:", reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.text in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота',
                                          'Воскресенье'])
def get_day_schedule(message):
    user_id = message.chat.id
    if user_id not in user_data or 'group' not in user_data[user_id]:
        bot.send_message(user_id, "⚠️ Сначала пройдите регистрацию! Введите /start")
        return

    group = user_data[user_id]['group']
    day = message.text.lower()


    week_number = datetime.datetime.now().isocalendar()[1]
    week_type = "odd_week" if week_number % 2 == 1 else "even_week"
    week_type_text = "нечетная" if week_number % 2 == 1 else "четная"

    if group in schedule_data:
        schedule = schedule_data[group][week_type].get(day, "❌ Занятий нет")



@bot.message_handler(func=lambda message: message.text == '🔄 Сменить группу')
def change_group(message):
    user_id = message.chat.id
    user_data[user_id]['step'] = 'awaiting_group'
import datetime
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Группа 1-МД-13')
    btn2 = types.KeyboardButton('Группа 1-МД-35')
    btn3 = types.KeyboardButton('Группа 1-МД-20')
    markup.add(btn1, btn2, btn3)




@bot.message_handler(func=lambda message: message.text == '⬅️ Назад')
def back_to_menu(message):
    user_id = message.chat.id
    show_main_menu(user_id)


@bot.message_handler(commands=['info'])
def info_message(message):
    user_id = message.chat.id
    if user_id in user_data:
        info = f"👤 Ваши данные:\n\nИмя: {user_data[user_id].get('first_name', 'Не указано')}\nФамилия: {user_data[user_id].get('last_name', 'Не указано')}\nГруппа: {user_data[user_id].get('group', 'Не выбрана')}"
        bot.send_message(user_id, info)
    else:
        bot.send_message(user_id, "❌ Вы еще не зарегистрированы. Введите /start")


@bot.message_handler(commands=['расписание'])
def old_schedule_command(message):
    bot.send_message(message.chat.id, "ℹ️ Эта команда устарела. Используйте кнопки меню.")


if __name__ == '__main__':
    print("Бот запущен...")

bot.polling(none_stop=True, interval=0)