# -*- coding: utf-8 -*-
from flask import Flask, request
import threading, json, requests

''' APIs '''
API = "https://api.telegram.org/bot"
CHAT_BOT_API = "http://api.program-o.com/v2/chatbot/"
''' APIs '''

app = Flask(__name__)

'''DataBase connection'''
# try:
# 	db = MySQLdb.connect(host="",    
#                      user="",         
#                      passwd="", 
#                      db="")        
# 	cur = db.cursor()
# 	print "Connection to DB is OK"
# 	db.close()
# except Exception,e:
# 	print(e)
'''Check connection to MySql'''


''' URL methods'''
@app.route('/', methods=['GET','POST'])
def test():
	print("It works!")
	return 'OK'

@app.route('/123', methods=['GET','POST'])
def get_message_from_telegram():
	data = json.loads(request.get_data())
	print data
	message = data['message']
	print message['text'].encode('utf-8')
	try:
		id = processing(message['text'])
		send_message(message['chat']['id'],id)
		print "msg sended"
	except Exception,e:
		print e
	return 'OK'
	
@app.route('/denis', methods=['POST'])
def message_from_dennis():
	#chat_id = request.form['chat_id']
	#print chat_id
	return 'OK Denis Horow'

@app.route('/abay', methods=['POST'])
def message_from_abay():
	data = request.get_data()
	today_file = open("menu_today.txt","r+")
	tomorrow_file = open("menu_tomorrow.txt","r+")
	yesterday_file = open("menu_yesterday.txt", "r+")
	tomorrow = tomorrow_file.read()
	today = today_file.read()
	yesterday = yesterday_file.read()

	yesterday_file.seek(0)
	yesterday_file.truncate()
	yesterday_file.write(today)
	today_file.seek(0)
	today_file.truncate()
	today_file.write(tomorrow)
	tomorrow_file.seek(0)
	tomorrow_file.truncate()
	tomorrow_file.write(data)

	today_file.close()
	tomorrow_file.close()
	yesterday_file.close()
	return 'OK Abay Molodec'
''' URL methods'''

''' Functions '''
def send_message(chat_id, id):
	buttons = get_buttons_by_id(id)
	text = get_answer_by_id(id)
	keyboard = {'keyboard':buttons, 'resize_keyboard':True}
	params = {'chat_id':chat_id, 'text': text, 'reply_markup': json.dumps(keyboard)}
	requests.post(API+'sendMessage', params=params)

def processing(msg):
	# get message and responce id
	msg = msg.encode('utf-8')
	for i in range(len(menu_messages)):
		for j in range(len(menu_messages[i])):
			if lower_russian(menu_messages[i][j]) == lower_russian(msg):
				return i*10+j
	return 0
	

def get_buttons_by_id(id):
	# get id and responce corresponding keyboard of buttons
	row = []
	arrOfRow = []
	if id==1 or id==2:
		row = menu_messages[id]
		arrOfRow.append(row)
		row = [{'text':"На главную"}]
		arrOfRow.append(row)
	else:
		row = menu_messages[0][1:3]
		arrOfRow.append(row)
		row = menu_messages[0][3:5]
		arrOfRow.append(row)
		row = menu_messages[0][5:7]
		arrOfRow.append(row)
	return arrOfRow

def get_answer_by_id(id):
	msg = ""
	i = id/10
	j = id%10
	if i==1:
		read_menu_files()

	return responce_messages[i][j]



def parse_menu(menu):
	# parse json MENU 
	menu = json.loads(menu)
	menu = menu['menu']
	lunch = arrayOfMenuToString(menu['lunch'])
	afternoon_snack = arrayOfMenuToString(menu['afternoon snack'])
	dinner = arrayOfMenuToString(menu['dinner'])
	obed = u"Обед"
	poldnik = u"Полдник"
	uzhin = u"Ужин"
	response = obed+':'+lunch+'\n\n'+poldnik+':'+afternoon_snack+'\n\n'+uzhin+':'+dinner+'\n\n'
	return response


def arrayOfMenuToString(foods):
	# convert array of menu to string 
	result = "" 
	k=1
	for i in foods:
		result = result + ("\n%s. %s. %s")%(str(k),i['name'],i['description'])
		k=k+1
	return result

def request_message_to_chat_bot(msg):
	# conversetion with chat bot outside
	params = {'bot_id':6, 'convo_id':'123', 'format':'json', 'say':msg}
	p = {'botsay':'no changes'}
	p = requests.get(CHAT_BOT_API, params=params).content
	print p
	t = json.loads(p)
	return t['botsay']

def lower_russian(msg):
	# decode and make lower case
	return msg.decode('utf-8').lower()

def read_menu_files():
	today_file = open("menu_today.txt","r")
	tomorrow_file = open("menu_tomorrow.txt","r")
	yesterday_file = open("menu_yesterday.txt", "r")
	tomorrow = tomorrow_file.read()
	today = today_file.read()
	yesterday = yesterday_file.read()

	responce_messages[1][1] = parse_menu(yesterday)
	responce_messages[1][2] = parse_menu(today)
	responce_messages[1][3] = parse_menu(tomorrow)

	today_file.close()
	tomorrow_file.close()
	yesterday_file.close()
''' Functions '''

''' Strings '''
MENU1 = '{"menu":{"lunch":[{"photo":"url","name":"Грибной крем-суп", "description":"грибной крем суп с плав сыром"}, {"photo":"url", "name":"Тыквенный крем-суп", "description":""}, {"photo":"url", "name":"Хлебцы", "description":"Хлебцы ржаные"}, {"photo":"url", "name":"Перец фаршированный под сыром", "description":""},{"photo":"url", "name":"Индейка под устричным соусом с овощами", "description":""}], "afternoon snack":[{"photo":"url", "name":"Грануллы", "description":""},{"photo":"url", "name":"Йогурт", "description":""},{"photo":"url", "name":"Чизкейк кокосовый", "description":"сахар пудра 75гр; сливки10%100гр; творог 0% 250гр; желатин 20гр; кокосовая стружка 50гр; пюре яблочное 200гр; мед70гр; печенье крокет 200гр"},{"photo":"url", "name":"Яблоко", "description":""}], "dinner":[{"photo":"url","name":"Маффины из индейки с овощами","description":""}, {"photo":"url","name":"Овощи запеченные","description":""}, {"photo":"url","name":"Стейк из дикого лосося","description":""}]}}'
MENU2 = '{"menu":{"lunch":[{"photo":"url","name":"Грибной крем-суп", "description":"грибной крем суп с плав сыром"}, {"photo":"url", "name":"Тыквенный крем-суп", "description":""}, {"photo":"url", "name":"Хлебцы", "description":"Хлебцы ржаные"}, {"photo":"url", "name":"Перец фаршированный под сыром", "description":""},{"photo":"url", "name":"Индейка под устричным соусом с овощами", "description":""}], "afternoon snack":[{"photo":"url", "name":"Грануллы", "description":""},{"photo":"url", "name":"Йогурт", "description":""},{"photo":"url", "name":"Чизкейк кокосовый", "description":"сахар пудра 75гр; сливки10%100гр; творог 0% 250гр; желатин 20гр; кокосовая стружка 50гр; пюре яблочное 200гр; мед70гр; печенье крокет 200гр"},{"photo":"url", "name":"Яблоко", "description":""}], "dinner":[{"photo":"url","name":"Маффины из индейки с овощами","description":""}, {"photo":"url","name":"Овощи запеченные","description":""}, {"photo":"url","name":"Стейк из дикого лосося","description":""}]}}'
MENU3 = '{"menu":{"lunch":[{"photo":"url","name":"Грибной крем-суп", "description":"грибной крем суп с плав сыром"}, {"photo":"url", "name":"Тыквенный крем-суп", "description":""}, {"photo":"url", "name":"Хлебцы", "description":"Хлебцы ржаные"}, {"photo":"url", "name":"Перец фаршированный под сыром", "description":""},{"photo":"url", "name":"Индейка под устричным соусом с овощами", "description":""}], "afternoon snack":[{"photo":"url", "name":"Грануллы", "description":""},{"photo":"url", "name":"Йогурт", "description":""},{"photo":"url", "name":"Чизкейк кокосовый", "description":"сахар пудра 75гр; сливки10%100гр; творог 0% 250гр; желатин 20гр; кокосовая стружка 50гр; пюре яблочное 200гр; мед70гр; печенье крокет 200гр"},{"photo":"url", "name":"Яблоко", "description":""}], "dinner":[{"photo":"url","name":"Маффины из индейки с овощами","description":""}, {"photo":"url","name":"Овощи запеченные","description":""}, {"photo":"url","name":"Стейк из дикого лосося","description":""}]}}'
PROGRAMM1 = "Slim \n\nЦена: 3800 тг. за 1 день. \n\nПрограмма питания «Slim»- это готовое решение для клиентов наших партнерских спортивных залов. Программа Slim была специально разработана с учетом рекомендаций профессиональных фитнес и кроссфит тренеров партнерских залов, наших врачей эндокринолога и диетолога. Синергетический эффект применения спортивной программы и правильного питания- это гарантированный успех в достижении личных показателей по снижению веса."
PROGRAMM2 = "Strong \n\nЦена: 3800 тг. за 1 день. \n\nПрограмма питания «Strong»- это готовое решение для клиентов наших партнерских спортивных залов. Программа Slim была специально разработана с учетом рекомендаций профессиональных фитнес и кроссфит тренеров партнерских залов, наших врачей эндокринолога и диетолога. Синергетический эффект применения спортивной программы и правильного питания- это гарантированный успех в достижении личных показателей по снижению веса."
welcome_text = "Вас приветствует бот DostykCatering! "
conversetion_text = "Привет, выбери интересующий пункт в меню ниже"
delivery_condition_text = "Доставка 500 тенге по центру города. Заявки принимаются за сутки до начала питания"
apply_request_text = "Для оформления заявки перейдите по ссылке doscat.kz"
contacts_text = " Адрес: г. Алматы, ТРЦ Ритц-Палас, пр.Аль-фараби, 1\nE-mail: zhkiro@gmail.com\nТелефон: +7 (707) 336-99-22"
whos_here_text = "Если вам надоел бот, то можете задать вопрос живому человеку ;) просто нажмите сюда @kozhaly "

menu_messages = [["","Меню дня", "Описание программ питания и цены", "Условия доставки", "Подать заявку", "Контакты", "Кто здесь?"],  
["", "Меню на вчера", "Меню на сегодня", "Меню на завтра"],  ["", "Снизить вес", "Набрать вес"]]

responce_messages = [[conversetion_text, "Выберите меню", "Выберите программу", delivery_condition_text, apply_request_text, contacts_text, whos_here_text], 
["", parse_menu(MENU1), parse_menu(MENU2), parse_menu(MENU3)], ["", PROGRAMM1, PROGRAMM2]]
''' Strings '''

