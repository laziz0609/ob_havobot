import asyncio
import logging
import sys

from dates import weather_info
import os
from threading import Thread
from flask import Flask

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from dotenv import load_dotenv
load_dotenv()  
TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()

# ===== Flask server for ping =====
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run_flask():
    port = int(os.environ.get("PORT", 3000))  # Replit / Render Free plan port
    app.run(host='0.0.0.0', port=port)

# Start Flask server in separate thread
Thread(target=run_flask).start()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Assalomu alaykum, {html.bold(message.from_user.full_name)}!\n Men ob-havo botiman. Menga O'zbekiston viloyatlari  (Toshkent shahri va Qoraqalpog'iston)  nomini yozing . Men sizga 5 kunlik ob-havo ma'lumotlarini taqdim etaman.")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        response = weather_info(message.text.lower())
        if response:
            if response['code'] == 200:
                dates = response['informations']['time']
                max_temps = response['informations']['temperature_2m_max']
                min_temps = response['informations']['temperature_2m_min']
                rain_sums = response['informations']['rain_sum']
                snow_sums = response['informations']['snowfall_sum']
                precipitations = response['informations']['precipitation_probability_max']
                weather_report = f"<b>{message.text.title()} shahri uchun 5 kunlik ob-havo ma'lumotlari:</b>\n"
                for i in range(len(dates)):
                    weather_report += f"\n<b>{dates[i]}</b>\n"
                    if max_temps[i]>0:
                        weather_report+= f"Eng yuqori harorat:   +{max_temps[i]}°C\n"
                    else:
                        weather_report+= f"Eng yuqori harorat:   {max_temps[i]}°C\n"
                    if min_temps[i]>0:
                        weather_report+= f"Eng past harorat:    +{min_temps[i]}°C\n"
                    else:
                        weather_report+= f"Eng past harorat:    {min_temps[i]}°C\n"
                    if rain_sums[i]>0 and snow_sums[i]>0:
                        weather_report+= f"Yomg'ir va qor: {precipitations[i]}% \n"
                    elif rain_sums[i]>0:
                        weather_report+= f"Yomg'ir: {precipitations[i]}% \n"
                    elif snow_sums[i]>0:
                        weather_report+= f"Qor: {precipitations[i]}% \n"
                    else:
                        weather_report+= f"Yomg'ingarchilik kutilmaydi \n"
                await message.answer(weather_report)
            else:
                await message.answer("Xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.")
        else:
            await message.answer("Kechirasiz, kiritilgan joy nomi noto'g'ri yozilgan yoki mavjud emas.\n\n <b>Faqat O'zbekiston hududidagi joylarni yozing</b>")
    except:
        pass

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
