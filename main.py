
import telebot
from telebot import types


bot = telebot.TeleBot('6293338837:AAHjJTDgkKHkMY8Zp8g-4t0uY7lBNwVrBiQ')


transactions = {
    "доходы": [],
    "расходы": []
}

START_TEXT = """ Привет, я бот который поможет тебе рассчитать твой доход и твой рассход💸
Для рассчета дохода нажми - /доход  
Для рассчета рассхода напиши - /расход
Для рассчета своего баланса - /сумма
Для помощи нажмите команду /help
"""

HELP_TEXT = """ Ты не понял как пользоваться ботом?😅
Все хорошо, я объясню:
1) Ты нажимаешь доход либо расход(кнопки у тебя на панели)
2) Ты вводишь сумму которую ты хочешь ввести в бота
3) У тебя все получилось 💸
"""
ERROR = """Чувак,я без понятия, что ты написал, нажми на /help 😅
"""



@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/help',)
    btn2 = types.KeyboardButton('/сумма')
    markup.row(btn1,btn2)
    btn3 = types.KeyboardButton('/доход')
    btn4 = types.KeyboardButton('/расход')
    markup.row(btn3, btn4)
    bot.send_message(message.chat.id,START_TEXT, reply_markup=markup)
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,HELP_TEXT)


@bot.message_handler(commands=['доход'])
def income(message):
    bot.send_message(message.chat.id,'Отлично напиши теперь свою сумму')
    bot.register_next_step_handler(message,add_income)

def add_income(message):
    try:
        text = message.text.split(' ')
        amount = float(text[-1])
        transactions['доходы'].append(amount)
        bot.reply_to(message, "Доход успешно записан💸")
    except:
        bot.reply_to(message, ERROR)

@bot.message_handler(commands=['расход'])
def add_expense(message):
    bot.send_message(message.chat.id, 'Отлично напиши теперь свою сумму')
    bot.register_next_step_handler(message, expense)

def expense(message):
    try:
        text = message.text.split(' ')
        amount = float(text[-1]) 
        transactions['расходы'].append(amount) 
        bot.reply_to(message, "Расход успешно записан📉")
    except:
        bot.reply_to(message, ERROR)


@bot.message_handler(commands=['сумма'])
def show_summary(message):
    income = sum(transactions['доходы'])  
    expense = sum(transactions['расходы'])  
    balance = income - expense  
    summary = f"Доходы: {income:.2f}\nРасходы: {expense:.2f}\nБаланс: {balance:.2f}"  

    bot.reply_to(message, summary)



bot.polling(none_stop=True)
