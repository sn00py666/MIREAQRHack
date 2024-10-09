import telebot as t
TELEGRAM_TOKEN = "7892826601:AAEcY8WNiFKWLvc0wYKGpuMzvtL5HIdfDaY"

bot = t.TeleBot(token=TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    
