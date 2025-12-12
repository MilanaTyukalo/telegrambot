import telebot

TOKEN = '8562828071:AAE_Qq6yKeNiLHp5qSg83dBxVAHfpDaLO34'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '👋 Добро пожаловать в бот расписания университета!')

@bot.message_handler(commands=['расписание'])


import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import json
import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

SELECT_GROUP, SELECT_DAY = range(2)
SCHEDULE_DATA = {
    "1-МД-13": {
        "Понедельник": [
            {"time": "10:05-11:30", "subject": "Операционные системы, сети и телекомуникации", "teacher": "Зверев В.В.", "кабинет": "В462"},
            {"time": "11:40-13:05", "subject": "Алгоритмизация и программирование", "teacher": "Якуничева Е.Н.", "кабинет": "С407"},
            {"time": "13:05-15:10", "subject": "Математика", "teacher": "Евсеев Е.А.", "кабинет": "В301"},
            {"time": "16:55-18:20", "subject": "Основы российской государственности", "teacher": "Узнаете на паре", "кабинет": "ДОТ"}
        ],
        "Вторник": [
            {"time": "10:05-11:30", "subject": "Математика", "teacher": "Вольнова Д.В", "кабинет": "В323"},
            {"time": "11:40-13:05", "subject": "Операционные системы, сети и телекоммуникации", "teacher": "Лебедева С.В.", "кабинет": "В452"}
            {"time": "9:00-10:30", "subject": "История России", "teacher": "Узнаете на паре", "кабинет": "В409"}
        ],
        "Среда": [
            {"time": "10:05-11:30", "subject": "Алгоритмы", "teacher": "Федоров С.М.", "кабинет": "102"},
            {"time": "11:40-13:05", "subject": "Математика", "teacher": "Иванов А.С.", "кабинет": "101"}
        ],
        "Четверг": [
            {"time": "10:05-11:30", "subject": "Физкультура", "teacher": "Смирнов В.Г.", "кабинет": "Спортзал"},
            {"time": "11:40-13:05", "subject": "Иностранный язык", "teacher": "Ковалева О.Л.", "кабинет": "304"}
        ],
        "Пятница": [
            {"time": "10:45-12:15", "subject": "Проектная деятельность", "teacher": "Петрова М.В.", "кабинет": "203"}
        ]
    },
    "ПИ-1-21": {
        "Понедельник": [
            {"time": "9:00-10:30", "subject": "Экономика", "teacher": "Григорьева Т.Н.", "кабинет": "201"},
            {"time": "13:00-14:30", "subject": "Менеджмент", "teacher": "Волков Р.С.", "кабинет": "202"}
        ],
        "Вторник": [
            {"time": "10:45-12:15", "subject": "Статистика", "teacher": "Иванов А.С.", "кабинет": "101"},
            {"time": "14:45-16:15", "subject": "Маркетинг", "teacher": "Зайцева Л.М.", "кабинет": "302"}
        ]
    }
}
GROUPS = list(SCHEDULE_DATA.keys())
DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
Выберите действие или введите команду.

    await update.message.reply_text(welcome_text)
async def show_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    "Показать список всех групп"
    groups_text = "📋 Список доступных групп:\n\n" + "\n".join([f"• {group}" for group in GROUPS])
    await update.message.reply_text(groups_text)
async def schedule_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    "Начало процесса просмотра расписания"
    # Создаем клавиатуру с группами
    keyboard = [[KeyboardButton(group)] for group in GROUPS]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "📚 Выберите вашу группу:",
        reply_markup=reply_markup
    )
    return SELECT_GROUP


async def select_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    "Обработчик выбора группы"
    group = update.message.text
    if group not in GROUPS:
        await update.message.reply_text("❌ Группа не найдена. Попробуйте еще раз.")
        return SELECT_GROUP

    context.user_data['group'] = group

    # Создаем клавиатуру с днями недели
    keyboard = [[KeyboardButton(day)] for day in DAYS]
    keyboard.append([KeyboardButton("Сегодня"), KeyboardButton("Завтра")])
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        f"📅 Выберите день для группы {group}:",
        reply_markup=reply_markup
    )
    return SELECT_DAY


async def select_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    "Обработчик выбора дня"
    day_input = update.message.text
    group = context.user_data['group']

    # Определяем выбранный день
    if day_input == "Сегодня":
        today = datetime.datetime.now().weekday()
        day = DAYS[today]
    elif day_input == "Завтра":
        tomorrow = (datetime.datetime.now().weekday() + 1) % 7
        day = DAYS[tomorrow] if tomorrow < len(DAYS) else "Воскресенье"
    else:
        day = day_input

    # Получаем расписание
    schedule = SCHEDULE_DATA.get(group, {}).get(day, [])

    if not schedule:
        await update.message.reply_text(
            f"📅 На {day} у группы {group} пар нет 🎉",
            reply_markup=None
        )
    else:
        schedule_text = f"📚 Расписание группы {group} на {day}:\n\n"
        for i, lesson in enumerate(schedule, 1):
            schedule_text += f"{i}. 🕒 {lesson['time']}\n"
            schedule_text += f"   📖 {lesson['subject']}\n"
            schedule_text += f"   👨‍🏫 {lesson['teacher']}\n"
            schedule_text += f"   🏫 Ауд. {lesson['кабинет']}\n\n"

        await update.message.reply_text(schedule_text, reply_markup=None)

    return ConversationHandler.END


async def today_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    "Показать расписание на сегодня для всех групп"
    today = datetime.datetime.now().weekday()
    day = DAYS[today] if today < len(DAYS) else "Воскресенье"

    schedule_text = f"📅 Расписание на сегодня ({day}):\n\n"

    for group in GROUPS:
        schedule = SCHEDULE_DATA.get(group, {}).get(day, [])
        if schedule:
            schedule_text += f"👥 {group}:\n"
            for lesson in schedule:
                schedule_text += f"   🕒 {lesson['time']} - {lesson['subject']} ({lesson['teacher']}, ауд. {lesson['room']})\n"
            schedule_text += "\n"

    if schedule_text == f"📅 Расписание на сегодня ({day}):\n\n":
        schedule_text += "🎉 Сегодня пар нет!"

    await update.message.reply_text(schedule_text)


async def tomorrow_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    "Показать расписание на завтра для всех групп"
    tomorrow = (datetime.datetime.now().weekday() + 1) % 7
    day = DAYS[tomorrow] if tomorrow < len(DAYS) else "Воскресенье"

    schedule_text = f"📅 Расписание на завтра ({day}):\n\n"

    for group in GROUPS:
        schedule = SCHEDULE_DATA.get(group, {}).get(day, [])
        if schedule:
            schedule_text += f"👥 {group}:\n"
            for lesson in schedule:
                schedule_text += f"   🕒 {lesson['time']} - {lesson['subject']} ({lesson['teacher']}, ауд. {lesson['room']})\n"
            schedule_text += "\n"

    if schedule_text == f"📅 Расписание на завтра ({day}):\n\n":
        schedule_text += "🎉 Завтра пар нет!"

    await update.message.reply_text(schedule_text)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    "Отмена текущей операции"
    await update.message.reply_text("Операция отменена.", reply_markup=None)
    return ConversationHandler.END
    
if __name__ == "__main__":
    main()


bot.polling(none_stop=True, interval=0)
