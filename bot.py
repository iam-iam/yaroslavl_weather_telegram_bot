from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
import config as cfg

def hello(update, context):
    update.message.reply_text(
        'Hello {}, введите дату в формате ММ-ДД(например, 01-24), чтобы узнать прогноз погоды'
            .format(update.message.from_user.first_name))


def echo(update, context):
    """Echo the user message."""
    url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/daily"

    querystring = {"units": "M", "lang": "ru", "lat": "57.626549", "lon": "39.893885"}

    headers = {
        'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
        'x-rapidapi-key': cfg.RAPIDAPI_API_KEY
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_data = json.loads(response.text)
    output_dict = [x for x in json_data['data'] if x['valid_date'] == '2020-'+update.message.text]
    forecast = '''  Температура: {0}
        Вероятность осадков: {1}
        Давление: {2}
        Влажность: {3} '''.format(output_dict[0]['temp'], output_dict[0]['pop'], output_dict[0]['pres'], output_dict[0]['rh'])
    update.message.reply_text(forecast)


updater = Updater(cfg.TELEGRAM_API_KEY, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler('hello', hello))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

updater.start_polling()
updater.idle()
