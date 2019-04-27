from telebot import apihelper
from telebot import types
tokenn = "865961769:AAFWrT4pHI1bJnp4KQ1fylL2IOsSL_r1FRs"
import requests
import telebot
sotrudniki = [{'name':'Максим Штиль', 'login':'Max', 'password':'shtil123'}, {'name':'Сачков Владимир', 'login':'Vova', 'password':'sachkov321'}]
chatt = {}
awaitkons = []
awaitcust = []
def make_markup(markup, set):
    markup = markup
    set = [types.KeyboardButton(i) for i in set]
    for k in set:
        markup.add(k)
    return markup
markup1 = types.ReplyKeyboardMarkup(row_width=3)
markup2 = types.ReplyKeyboardMarkup(row_width=3)
markup3 = types.ReplyKeyboardMarkup(row_width=3)
buttonset1 = ['Ближайшие отделения', 'Записаться на приём', 'Связаться с консультантом']
buttonset2 = ['/стоп']
buttonset3 = ['/выйти']
sotrsotr = {}
markup3 = make_markup(markup3, buttonset3)
markup2 = make_markup(markup2, buttonset2)
markup1 = make_markup(markup1, buttonset1)
bot = telebot.TeleBot(tokenn)
loginposl = {}
telebot.apihelper.proxy = {'https': 'socks5://geek:socks@t.geekclass.ru:7777'}
def get_pic(lat, lon):
    APP_ID = "WJKW4xjeKvXn9u5eZ7cw"
    APP_CODE = "2kxrT-Jmes601s_BwANBYw"
    lat = str(lat)
    lon = str(lon)
    url = f"https://image.maps.api.here.com/mia/1.6/mapview?app_id={APP_ID}&app_code={APP_CODE}&lat={lat}&lon={lon}&vt=0&z=14"
    data = requests.get(url)
def check(que1, que2, chatt):
    que1 = que1
    chatt = chatt
    que2 = que2
    if que1 and que2:
        alll = [len(que1), len(que2)]
        for i in range(min(alll)):
            sotr = que2[i]
            cust = que1[i]
            del que1[i]
            del que2[i]
            chatt[str(sotr)] = str(cust)
            chatt[str(cust)] = str(sotr)
            bot.send_message(
                chat_id=sotr,
                text='Вас соединили с клиентом, начинайте беседу. Чтобы окончить беседу, нажмите на кнопку /стоп',
                reply_markup=markup2
            )
            bot.send_message(
                chat_id=cust,
                text='Вы были соединены с конусультантом {}. Чтобы окончить беседу, нажмите на кнопку /стоп'.format(sotrsotr[sotr]),
                reply_markup=markup2
            )
        return (que1,que2,chatt)
    else:
        return (que1,que2,chatt)
def checkna(password,login,data):
    for k in data:
        if password == k['password'] and login == k['login']:
            return k
    return False
@bot.message_handler(content_types=["text"])
def handle_text(message):
    global chatt, awaitkons, awaitcust
    if str(message.chat.id) in list(chatt.keys()):
        if message.text == '/стоп':
            if str(message.chat.id) in list(sotrsotr.keys()):
                awaitkons.append(str(message.chat.id))
                opponent = chatt[str(message.chat.id)]
                del chatt[chatt[str(message.chat.id)]]
                del chatt[str(message.chat.id)]
                bot.send_message(
                    chat_id=message.chat.id,
                    text='Ожидайте пока к вам подключится клиент... Чтобы выйти, нажмите кнопку /выйти',
                    reply_markup=markup3
                )
                bot.send_message(
                    chat_id=opponent,
                    text='Консультант отключился. Вы находитесь в главном меню.',
                    reply_markup=markup1
                )
            else:
                opponent = chatt[str(message.chat.id)]
                awaitkons.append(chatt[str(message.chat.id)])
                del chatt[chatt[str(message.chat.id)]]
                del chatt[str(message.chat.id)]
                bot.send_message(
                    chat_id=message.chat.id,
                    text='Вы вернулись в главное меню',
                    reply_markup=markup1
                )
                bot.send_message(
                    chat_id=opponent,
                    text='Клиент отключился. Вы опять в режиме ожидания',
                    reply_markup=markup3
                )
            awaitcust, awaitkons, chatt = check(awaitcust, awaitkons, chatt)
        else:
            bot.send_message(
                chat_id=chatt[str(message.chat.id)],
                text=message.text,
                reply_markup=markup2
            )
    elif str(message.chat.id) in list(loginposl.keys()):
        if loginposl[str(message.chat.id)]['steps'] % 2 == 1:
            loginposl['login'] = message.text
            loginposl[str(message.chat.id)]['steps'] += 1
            bot.send_message(
                chat_id=message.chat.id,
                text='Впишите ваш пароль',
                reply_markup=None
            )
        else:
            loginposl['password'] = message.text
            loginposl[str(message.chat.id)]['steps'] += 1
            print('kek')
            cheker = checkna(loginposl['password'], loginposl['login'], sotrudniki)
            print('lol')
            if cheker:
                bot.send_message(
                    chat_id=message.chat.id,
                    text='Добро пожаловать, {}'.format(cheker['name']),
                    reply_markup=None
                )
                del loginposl[str(message.chat.id)]
                sotrsotr[str(message.chat.id)] = cheker['name']
                awaitkons.append(str(message.chat.id))
                awaitcust, awaitkons, chatt = check(awaitcust, awaitkons, chatt)
                if str(message.chat.id) not in list(chatt.keys()):
                    bot.send_message(
                        chat_id=message.chat.id,
                        text='Ожидайте пока к вам подключится клиент... Чтобы выйти, нажмите кнопку /выйти',
                        reply_markup=markup3
                    )
            else:
                if loginposl[str(message.chat.id)]['steps'] == 7:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text='У вас закончились попытки. Возвращаю в главное меню',
                        reply_markup=markup1
                    )
                    del loginposl[str(message.chat.id)]
                else:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text='Неверный логин или пароль. Осталось {} попыток'.format(int((7-loginposl[str(message.chat.id)]['steps'])/2)),
                        reply_markup=None
                    )
                    bot.send_message(
                        chat_id=message.chat.id,
                        text='Впишите ваш логин',
                        reply_markup=None
                    )
    elif str(message.chat.id) in awaitkons:
        if '/выйти' in message.text:
            awaitkons.remove(str(message.chat.id))
            bot.send_message(
                chat_id=message.chat.id,
                text='Вы вернулись в главное меню',
                reply_markup=markup1
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text='Вы находитесь в режиме ожидания, чтобы выйти, нажмите на кнопку /выйти',
                reply_markup=markup3
            )
    elif str(message.chat.id) in awaitcust:
        if '/выйти' in message.text:
            awaitcust.remove(str(message.chat.id))
            bot.send_message(
                chat_id=message.chat.id,
                text='Вы вернулись в главное меню',
                reply_markup=markup1
            )
            awaitcust, awaitkons, chatt = check(awaitcust,awaitkons,chatt)
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text='Вы находитесь в режиме ожидания, вы {} в очереди, чтобы выйти, нажмите на кнопку /выйти'.format(str(awaitcust.index(str(message.chat.id)) + 1)),
                reply_markup=markup3
            )
    else:
        if 'консультант' == message.text:
            loginposl[str(message.chat.id)] = {'steps':1,'login':'', 'password':''}
            bot.send_message(
                chat_id=message.chat.id,
                text='Впишите пожалуйста ваш логин консультанта',
                reply_markup=None
            )
            '''
            idd = message.text.replace('консул ', '')
            if idd in list(sotrudniki.keys()):
                sotrsotr[str(message.chat.id)] = sotrudniki[idd]
                awaitkons.append(str(message.chat.id))
                awaitcust, awaitkons, chatt = check(awaitcust,awaitkons,chatt)
                if str(message.chat.id) not in list(chatt.keys()):
                    bot.send_message(
                        chat_id=message.chat.id,
                        text='Ожидайте пока к вам подключится клиент... Чтобы выйти, нажмите кнопку /выйти',
                        reply_markup=markup3
                    )
            '''
        elif 'Связаться с консультантом' in message.text:

            awaitcust.append(str(message.chat.id))
            awaitcust, awaitkons, chatt = check(awaitcust,awaitkons,chatt)
            if str(message.chat.id) not in list(chatt.keys()):
                bot.send_message(
                    chat_id=message.chat.id,
                    text='Ожидайте пока к вам подключится консультант... Вы находитесь {} в очереди. Чтобы выйти, нажмите кнопку /выйти'.format(str(awaitcust.index(str(message.chat.id)) + 1)),
                    reply_markup=markup3
                )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text='Выберите ваш запрос:',
                reply_markup=markup1
            )
@bot.message_handler(content_types=['document', 'audio'])
def other(message):
    bot.send_message(message.chat.id,"Воспринимаю только текстовые команды")
bot.polling(none_stop=True, interval=0)
