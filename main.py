from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from pydantic import BaseModel
import asyncio

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sn00py666.github.io/MIREAQRHack/"],  # Добавьте ваш домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Настройка вашего Telegram-бота
TELEGRAM_TOKEN = "7892826601:AAEcY8WNiFKWLvc0wYKGpuMzvtL5HIdfDaY"
CHAT_ID = ["850362750"]
QR_status = ""

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()')

async def send_message_to_telegram(qr_code):
    global CHAT_ID
    try:
        for id in CHAT_ID:
            await bot.send_message(chat_id=id, text=f"Считанный QR-код: {qr_code}")
        print("Сообщение отправлено в Telegram")  # Отладочный вывод
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")  # Логирование ошибок

class QRCode(BaseModel):
    qr_code: str

@app.post("/api/scan")
async def scan_qr(qr_code: QRCode):
    global QR_status
    if qr_code.qr_code != QR_status:
        QR_status = qr_code.qr_code
        print(f"Получен новый QR-код: {QR_status}")  # Отладочный вывод
        await send_message_to_telegram(QR_status)
        return {"status": "success", "message": "QR-код отправлен"}
    
    raise HTTPException(status_code=400, detail="Нет нового QR-кода")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
