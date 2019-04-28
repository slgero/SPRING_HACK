import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
main_mas = []
mydb = myclient["users"]
mycol = mydb["startup_log"]


class Add_User():
    def __init__(self, name, login, password):
        self.data = {

            'name': name,
            'login': login,
            'password': password

        }

    def add(self):
        mycol.insert_one(self.data)


for x in mycol.find({}, ):
    main_mas.append(x)
print(main_mas)
# py db.py

a = str(input('kommand: '))
if a == '/add':
    while a != '/stop':
        name = str(input('Введите name: '))
        login = str(input('Введите login: '))
        password = str(input('Введите password: '))

        x = Add_User(name, login, password)
        x.add()

        a = input('Напишите что-нибудь для продолжения инициализация админа:  ')
elif a == '/drop_all':
    mycol.delete_many({})
    print('collection was cleaned')