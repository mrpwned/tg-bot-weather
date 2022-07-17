import requests
import datetime
from API import api_weather
from  code_to import code_to_smile
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token='token')
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды!")


@dp.message_handler()
async def get_weather(message: types.Message):

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={api_weather}&units=metric"
        )
        data = r.json()
        temp = data['main']['temp']
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = '\U0001F937'
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
              f'Температура: {temp}C° {wd}\n'
              f'Влажность: {humidity}%\n'
              f'Давление: {pressure} мм.рт.ст\n'
              f'Ветер: {wind} м/с\n'
              f'Восход: {sunrise}\n'
              f'Закат: {sunset}'
              )

    except:
        await message.reply("Проверь название города")


if __name__ == '__main__':
    executor.start_polling(dp)