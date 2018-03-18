import os, random, telebot, datetime, pyowm

token = "309505601:AAHv7OKe8AR8ZBzJjH3AycbWvLAogt6LD4g"
API_key="bbdffdaf3c5c77897d386127486c03de"

def Weather():
    tomorrow = str(datetime.date.today()+datetime.timedelta(days=1))
    tomorrow_ = str(datetime.date.today()+datetime.timedelta(days=2))
    tomorrow__ = str(datetime.date.today()+datetime.timedelta(days=3))

    owm = pyowm.OWM(API_key, language='ru')

    fc = owm.three_hours_forecast('Moscow, RU')
    f = fc.get_forecast()
    wtr = {}

    weather1 = []
    weather2 = []
    weather3 = []

    for weather in f:
        wtr[weather.get_reference_time('iso')] = [str(weather.get_detailed_status()),
                                                  int(weather.get_temperature(unit='celsius')['temp'])]
    for time, status in wtr.items():
        if tomorrow in str(time):
            weather1.append(f'Завтра в {time[11:13]}:00 будет {status[0]} и {status[1]} градусов.')
        if tomorrow_ in str(time):
            weather2.append(f'Послезавтра в {time[11:13]}:00 будет {status[0]} и {status[1]} градусов.')
        if tomorrow__ in str(time):
            weather3.append(f'Послепослезавтра в {time[11:13]}:00 будет {status[0]} и {status[1]} градусов.')
    return weather1, weather2, weather3

bot = telebot.TeleBot(token)

wtr = Weather()

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(False, False)
    user_markup.row('/music')
    user_markup.row('/weather1', '/weather2', '/weather3')

    bot.send_message(message.from_user.id, 'Ну что, народ, погнали ...',
                     reply_markup=user_markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == '/music':
        bot.send_message(message.from_user.id, 'Подожди пару минут')
        directory = "Музыка для Джарвиса"
        all_files_in_directory = os.listdir(directory)
        random_file = random.choice(all_files_in_directory)
        music = open(directory + '/' + random_file, 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_audio')
        bot.send_audio(message.from_user.id, music)
        music.close()
    elif message.text == '/weather1':
        for i in wtr[0]:
            bot.send_message(message.from_user.id, i)
    elif message.text == '/weather2':
        for i in wtr[0]:
            bot.send_message(message.from_user.id, i)
        for i in wtr[1]:
            bot.send_message(message.from_user.id, i)
    elif message.text == '/weather3':
        for i in wtr[0]:
            bot.send_message(message.from_user.id, i)
        for i in wtr[1]:
            bot.send_message(message.from_user.id, i)
        for i in wtr[2]:
            bot.send_message(message.from_user.id, i)

bot.polling(none_stop=True, interval=0)
