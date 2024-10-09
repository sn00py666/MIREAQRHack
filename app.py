from quart import Quart, request, jsonify
from quart_cors import cors
from aiogram import Bot, Router, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
import asyncio
import sqlite3

app = Quart(__name__)
app = cors(app)

# Настройка вашего Telegram-бота
TELEGRAM_TOKEN = "7892826601:AAEcY8WNiFKWLvc0wYKGpuMzvtL5HIdfDaY"
CHAT_ID = ["850362750"]
QR_statys = ""

bot = Bot(token=TELEGRAM_TOKEN)

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()',
                         )

async def send_message_to_telegram(qr_code):
    global CHAT_ID
    try:
        for id in CHAT_ID:
            await bot.send_message(chat_id=id, text=f"Считанный QR-код: {qr_code} {CHAT_ID}")
        print("Сообщение отправлено в Telegram")  # Отладочный вывод
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")  # Логирование ошибок

async def start():
    TELEGRAM_TOKEN = "7892826601:AAEcY8WNiFKWLvc0wYKGpuMzvtL5HIdfDaY"
    bot = Bot(token=TELEGRAM_TOKEN)
    start_router = Router()
    await start_router.start_polling(bot)

@app.route('/api/scan', methods=['POST'])
async def scan_qr():
    global QR_statys
    data = await request.json
    qr_code = data.get('qrCode')

    if qr_code != QR_statys:
        QR_statys = qr_code
        print(f"Получен новый QR-код: {qr_code}")  # Отладочный вывод
        await send_message_to_telegram(qr_code)

        return jsonify({"status": "success", "message": "QR-код отправлен"}), 200
    
    return jsonify({"status": "error", "message": "Нет нового QR-кода"}), 400

if __name__ == '__main__':
    #app.run(debug=True)
    asyncio.run(start)

