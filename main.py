from telebot import apihelper
from telebot import types
from telegram import KeyboardButton
from PIL import Image
import random
from shutil import copyfile
from string import ascii_letters
from pdf2image import convert_from_path
from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pytils.translit import translify
import pymongo
from haversine import haversine #pip install haversine
import requests
import json
import operator
import time
from io import BytesIO
from random import randint
def set_avalible_time(id = 0):
    result = []
    for i in range(5):
        result.append(randint(int(time.time()), int(time.time()) + 100000))
    return sorted(result)
all_letters = ascii_letters
def otsek(x,y,string):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    #can.setStrokeColor(black)
    #can.setFont("Courier-BoldOblique", 20)
    can.drawString(x,y,string)
    #can.setFillColor(red)
    can.save()
    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("ticket.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page2 = new_pdf.getPage(0)
    page.mergePage(page2)
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open("ticket.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
def make_pdf(bankname,addres1,addres2,timeocher,telphys, telur):
    copyfile('dd.pdf','ticket.pdf')
    bankname = translify(bankname)
    addres1 = translify(addres1)
    addres2 = translify(addres2)
    timeocher = translify(timeocher)
    telphys = translify(telphys)
    telur = translify(telur)
    curtime = time.ctime(time.time())
    token = ''.join([random.choice(all_letters)] + [str(random.randint(0,9)) for _ in range(4)])
    allstrins = [bankname, addres1,addres2, timeocher, telphys, telur, curtime, token]
    positions = [(10,310),(10,290),(10,270),(100,130),(120,60),(120,90),(70,15),(110,200)]
    # create a new PDF with Reportlab
    for i in range(7):
        otsek(positions[i][0],positions[i][1],allstrins[i])
def set_date(number):
    pass
admins = [{'login':'Vova', 'password':'keklol'}]
allusers = []

class Banks:
    def __init__(self, file_name, API):
        self.__flag = False
        self.API = API
        try:
            with open(file_name) as f:
                self.data = json.loads(f.read())
        except Exception:
            print("Проблемы с фалом, невозможно прочитать.")
            self.data = None

    def distant_sphera(self, i):
        next_bank = (float(self.data[i]['lon']), float(self.data[i]['lat']))
        return haversine(self.user, next_bank)

    def get_me_nearest_bank(self, lat, lon):
        if self.data:
            self.user = (lat, lon)
            self.tmp = dict()
            for i in range(len(self.data)):
                self.tmp[i] = self.distant_sphera(i)
            self.nearest_banks = sorted(self.tmp.items(), key=operator.itemgetter(1))[0:10]
            self.__index = -1
            self.next_bank()

    def next_bank(self):
        self.__index += 1
        if self.__index > len(self.nearest_banks):
            self.__index = 0
        self.__i = self.nearest_banks[self.__index][0]
        self.lat = self.data[self.__i]['lat']
        self.lon = self.data[self.__i]['lon']

    def get_bank_name(self):
        return self.data[self.__i]['name']
    def get_photo(self):
        url = f"https://maps.googleapis.com/maps/api/staticmap?center={self.lat},{self.lon}\
        &zoom=15&size=400x400&maptype=roadmap&key={self.API}"
        url = f"https://static-maps.yandex.ru/1.x/?ll={self.lat},{self.lon}&size=450,450&z=16&l=map&pt={self.lat},{self.lon},pm2rdm1"
        return BytesIO(requests.get(url).content)

    def get_number2(self):
        return (self.data[self.__i]['phones'][0]['number'].strip(), self.data[self.__i]['phones'][1]['number'].strip())
    def get_adress(self):
        return self.data[self.__i]['address']

    def get_work_time(self):
        return self.data[self.__i]['workt']

    def get_number(self):
        return str(
            self.data[222]['phones'][0]['number'].strip() + ' ' + self.data[222]['phones'][0]['for_people'].strip()
            + '\n\t ' + self.data[222]['phones'][1]['number'].strip() + ' ' + self.data[222]['phones'][1][
                'for_people'].strip())

    def get_dist(self):
        return float("{0:.1f}".format(self.nearest_banks[self.__index][1]))

    def get_information(self):
        return (f'Ближайщий банк находится в {self.get_dist()}км от Вас.\nАдрес: {self.get_adress()}.\
        .\nЧасы работы: {self.get_work_time()}.\nТелефон: {self.get_number()}.')

    def get_avalible_time(self):
        return set_avalible_time(self.data[self.__i]['rubric_id'])

    def print_avalible_time(self):
        self.__flag = True
        self.avalible = self.get_avalible_time()
        print("Доступное время для записи:")
        for i in self.avalible:
            print(time.ctime(i).split()[3])
        print("Пожалуйста, выберите время, когда Вам будет удобнее.")

    def book_date(self, number):
        if number < 5 and self.__flag:
            print("Ваш талон назначен на", time.ctime(self.avalible[number]).split()[3])
            return set_date(self.avalible[number])
tokenn = "865961769:AAFWrT4pHI1bJnp4KQ1fylL2IOsSL_r1FRs"
import requests
import telebot
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
sotrudniki = []
mydb = myclient["users"]
mycol = mydb["startup_log"]
for x in mycol.find({}, ):
    sotrudniki.append(x)
#sotrudniki = [{'name':'Максим Штиль', 'login':'Max', 'password':'shtil123'}, {'name':'Сачков Владимир', 'login':'Vova', 'password':'sachkov321'}]
chatt = {}
awaitkons = []
awaitcust = []
def make_markup(markup, set):
    markup = markup
    set = [types.KeyboardButton(i) for i in set]
    for k in set:
        markup.add(k)
    return markup
markup1 = types.ReplyKeyboardMarkup(row_width=1)
markup2 = types.ReplyKeyboardMarkup(row_width=1)
markup3 = types.ReplyKeyboardMarkup(row_width=1)
markup7 = types.ReplyKeyboardMarkup(row_width=5)
markup4 = types.ReplyKeyboardMarkup(row_width=1)
markup7.add('1','2','3','4','5')
buttonset1 = ['Ближайшие отделения', 'Связаться с консультантом']
buttonset2 = ['стоп']
buttonset3 = ['Вернуться в главное меню']
buttonset4 = ['Записаться на приём','Другое отделение','Главное меню']
sotrsotr = {}
lococher = {}
markup4 = make_markup(markup4, buttonset4)
markup3 = make_markup(markup3, buttonset3)
markup2 = make_markup(markup2, buttonset2)
markup1 = make_markup(markup1, buttonset1)
bot = telebot.TeleBot(tokenn)
loginposl = {}
loginadmin = {}
location_keyboard = types.ReplyKeyboardMarkup()
button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
location_keyboard.add(button_geo )
telebot.apihelper.proxy = {'https': 'socks5://geek:socks@t.geekclass.ru:7777'}
def get_pic(lat, lon):
    APP_ID = "WJKW4xjeKvXn9u5eZ7cw"
    APP_CODE = "2kxrT-Jmes601s_BwANBYw"
    lat = str(lat)
    lon = str(lon)
    url = f"https://image.maps.api.here.com/mia/1.6/mapview?app_id={APP_ID}&app_code={APP_CODE}&lat={lat}&lon={lon}&vt=0&z=14"
    data = requests.get(url)
    #img = Image.open(BytesIO(data.content))
    return BytesIO(data.content)
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
def kartaiter(sender, chat_id, markup):
    '''
    bot.send_photo(
        chat_id=chat_id,
        photo=sender.get_photo(),
        reply_markup=None
    )
    '''
    bot.send_location(
        chat_id=chat_id,
        latitude=sender.lon,
        longitude=sender.lat,
        reply_markup=markup
    )
    bot.send_message(
        chat_id=chat_id,
        text=sender.get_information(),
        reply_markup=markup
    )
@bot.message_handler(content_types=["text", "location"])
def handle_text(message):
    if message.chat.id not in allusers:
        allusers.append(message.chat.id)
    if message.content_type == 'text':
        global chatt, awaitkons, awaitcust
        if str(message.chat.id) in list(chatt.keys()):
            if message.text == 'стоп':
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
                        text='Консультант отключился. Оцените пожалуйста его работу.',
                        reply_markup=markup7
                    )
                else:
                    opponent = chatt[str(message.chat.id)]
                    awaitkons.append(chatt[str(message.chat.id)])
                    del chatt[chatt[str(message.chat.id)]]
                    del chatt[str(message.chat.id)]
                    bot.send_message(
                        chat_id=message.chat.id,
                        text='Оцените пожалуйста работу специалиста.',
                        reply_markup=markup7
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
        elif str(message.chat.id) in list(lococher.keys()):
            print(lococher[str(message.chat.id)])
            if lococher[str(message.chat.id)]['step'] == 1:
                del lococher[str(message.chat.id)]
                bot.send_message(
                    chat_id=message.chat.id,
                    text='Вы вернулись в главное меню',
                    reply_markup=markup1
                )
            elif lococher[str(message.chat.id)]['step'] == 2:
                if message.text == 'Другое отделение':
                    lococher[str(message.chat.id)]['sender'].next_bank()
                    kartaiter(lococher[str(message.chat.id)]['sender'], message.chat.id, markup4)
                elif message.text == 'Записаться на приём':
                    times = [time.ctime(i) for i in lococher[str(message.chat.id)]['sender'].get_avalible_time()] + ['Другое отделение']
                    timemarkup = make_markup(types.ReplyKeyboardMarkup(row_width=3), times)
                    lococher[str(message.chat.id)]['times'] = times
                    bot.send_message(
                        chat_id=message.chat.id,
                        text='Выберете удобное для вас время.',
                        reply_markup=timemarkup
                    )
                    lococher[str(message.chat.id)]['step'] += 1
                elif message.text == 'Главное меню':
                    del lococher[str(message.chat.id)]

                    bot.send_message(
                        chat_id=message.chat.id,
                        text='Вы вернулись в главное меню.',
                        reply_markup=markup1
                    )

            elif lococher[str(message.chat.id)]['step'] == 3:
                if message.text == 'Другое отделение':
                    lococher[str(message.chat.id)]['step'] -= 1
                    lococher[str(message.chat.id)]['sender'].next_bank()
                    kartaiter(lococher[str(message.chat.id)]['sender'], message.chat.id, markup4)
                elif message.text in lococher[str(message.chat.id)]['times']:
                    print(['Банк',lococher[str(message.chat.id)]['sender'].get_adress(), message.text,lococher[str(message.chat.id)]['sender'].get_number2()[1],lococher[str(message.chat.id)]['sender'].get_number2()[0]])
                    make_pdf('Название Банка',lococher[str(message.chat.id)]['sender'].get_adress()[:35],lococher[str(message.chat.id)]['sender'].get_adress()[35:], message.text,lococher[str(message.chat.id)]['sender'].get_number2()[1],lococher[str(message.chat.id)]['sender'].get_number2()[0])
                    bot.send_document(
                        chat_id=message.chat.id,
                        data=open('ticket.pdf','r'),
                        reply_markup=markup1
                                      )
                    bot.send_message(
                        chat_id=message.chat.id,
                        text='Вы были успешно записаны в данное время: {}. Талон о записи прилагается. Что еще я могу для Вас сделать?'.format(message.text),
                        reply_markup=markup1
                    )
                    del lococher[str(message.chat.id)]
                else:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text='Не понял вас.',
                        reply_markup=markup1
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
                cheker = checkna(loginposl['password'], loginposl['login'], sotrudniki)
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
        elif str(message.chat.id) in list(loginadmin.keys()):
            if loginadmin[str(message.chat.id)]['steps'] % 2 == 1:
                if 'msg' in list(loginadmin[str(message.chat.id)].keys()):
                    for k in allusers:
                        bot.send_message(
                            chat_id=k,
                            text=message.text,
                            reply_markup=None
                        )
                    del loginadmin[str(message.chat.id)]
                else:
                    loginadmin['login'] = message.text
                    loginadmin[str(message.chat.id)]['steps'] += 1
                    bot.send_message(
                        chat_id=message.chat.id,
                        text='Впишите ваш пароль',
                        reply_markup=None
                    )
            else:
                loginadmin['password'] = message.text
                loginadmin[str(message.chat.id)]['steps'] += 1
                cheker = checkna(loginadmin['password'], loginadmin['login'], admins)
                if cheker:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text='Вы успешно вошли, введите ваше рассылочное сообщение.',
                        reply_markup=None
                    )
                    loginadmin[str(message.chat.id)]['msg'] = ''
                else:
                    if loginadmin[str(message.chat.id)]['steps'] == 7:
                        bot.send_message(
                            chat_id=message.chat.id,
                            text='У вас закончились попытки. Возвращаю в главное меню',
                            reply_markup=markup1
                        )
                        del loginadmin[str(message.chat.id)]
                    else:
                        bot.send_message(
                            chat_id=message.chat.id,
                            text='Неверный логин или пароль. Осталось {} попыток'.format(int((7-loginadmin[str(message.chat.id)]['steps'])/2)),
                            reply_markup=None
                        )
                        bot.send_message(
                            chat_id=message.chat.id,
                            text='Впишите ваш логин',
                            reply_markup=None
                        )
        elif str(message.chat.id) in awaitkons:
            if 'Вернуться в главное меню' in message.text:
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
            if 'Вернуться в главное меню' in message.text:
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
            elif 'рассылка' == message.text:
                loginadmin[str(message.chat.id)] = {'steps':1,'login':'', 'password':'', 'times':[]}
                bot.send_message(
                    chat_id=message.chat.id,
                    text='Впишите пожалуйста ваш логин администратора',
                    reply_markup=None
                )
            elif 'Связаться с консультантом' in message.text:

                awaitcust.append(str(message.chat.id))
                awaitcust, awaitkons, chatt = check(awaitcust,awaitkons,chatt)
                if str(message.chat.id) not in list(chatt.keys()):
                    bot.send_message(
                        chat_id=message.chat.id,
                        text='Вы №{} в очереди. Пожалуйста ожидайте, пока к Вам подключится консультант. В любой момент Вы можете завершить сеанс.'.format(str(awaitcust.index(str(message.chat.id)) + 1)),
                        reply_markup=markup3
                    )
            elif 'Ближайшие отделения' == message.text:
                bot.send_message(
                    chat_id=message.chat.id,
                    text='Отправьте ваше местоположение',
                    reply_markup=location_keyboard
                )
                    #photo=get_pic(random.randint(12,54), random.randint(12,54)),
                lococher[str(message.chat.id)] = {'step':1,'sender':Banks('bigdata.json', "AIzaSyC4mGpfZUJqeMQQdNpm32ci4Ilvl2W9zMs"),'times':[]}
                bot.send_chat_action(message.chat.id, 'find_location')
            else:
                bot.send_message(
                    chat_id=message.chat.id,
                    text='Добрый день. Подскажите, пожалуйста чем я могу вам помочь?',
                    reply_markup=markup1
                )
    elif message.content_type == 'location':
        if str(message.chat.id) in list(lococher.keys()):
            if lococher[str(message.chat.id)]['step'] == 1:
                lococher[str(message.chat.id)]['step'] += 1
                lococher[str(message.chat.id)]['sender'].get_me_nearest_bank(message.location.latitude, message.location.longitude)
                kartaiter(lococher[str(message.chat.id)]['sender'],message.chat.id,markup4)
bot.polling(none_stop=True, interval=0)
