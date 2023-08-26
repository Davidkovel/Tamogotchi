import random
import time
import textwrap
import mysql.connector
import sqlite3
import telebot
from telebot import types

from Config_MySql import connector
from Tamogochi_Database import write_data_database, delete_data_database, update_pets_from_database
from config_telegram import bot

# from accessify import private

class Pet:
    ''' Тепер при кожному виклику методу _update() буде використовуватись різниця між
        часом останнього оновлення та поточним часом,
        щоб обчислити, на скільки потрібно зменшити значення параметрів.'''

    # def __new__(cls, *args, **kwargs):
    #     # print('вызов __new__ для' + str(cls))
    #     return super().__new__(cls)  # c версии пайтон 3 все классы наследуеться от базового класса

    def __init__(self, name, scores=100, eat=100, health=100, mood=100, sleep=100, hygiena=100):
        self.scores = scores
        self.name = name
        self.eat = eat
        self.health = health
        self.mood = mood
        self.sleep = sleep
        self.hygiena = hygiena
        self.last_update_time = time.time()

    def feed(self, chat_id):  # процент голодування
        if self.eat > 100:
            self.eat = 100
        elif self.eat <= 0:
            bot.send_message(chat_id, 'Ви забули погодувати пета. Він помер')
            bot.send_message(chat_id, 'Тут ваша статистика пета')
            bot.send_message(chat_id, self.check_statuts())  # универсальна программа
            delete_data_database()
            exit('Гра закінчена')

        bot.send_message(chat_id, 'Ви підняли + 35% голод')
        self.eat += 35
        self.hygiena += 25

        bot.send_message(chat_id, f'Зараз у вас {self.eat} процентiв')

    def play(self, chat_id):
        if self.mood > 100:
            self.mood = 100
        elif self.mood <= 0:
            bot.send_message(chat_id, 'Увага у ваш низький рівень щастя.', self.mood)

        bot.send_message(chat_id, 'Ви підняли +15% щасті')
        self.mood += 15

        bot.send_message(chat_id, f'Зараз у вас {self.mood} процентiв')

    def hygiena(self, chat_id):
        if self.hygiena > 100:
            self.hygiena = 100
        elif self.hygiena <= 0:
            bot.send_message(chat_id, 'Увага у ваш низький рівень гігієна.', self.hygiena)

        bot.send_message(chat_id, 'Ви підняли +15% гігієна')
        self.hygiena += 15

        bot.send_message(chat_id, f'Зараз у вас {self.hygiena} процентiв')

    def sleeping(self, hours, chat_id):
        if self.sleep > 100:
            self.sleep = 100
        elif self.sleep <= 0:
            bot.send_message(chat_id, 'У вас зараз пет втомлений. Рекомендуємо поспати')
            bot.send_message(chat_id, 'Тут ваша статистика пета\n', self.check_statuts(chat_id))  # универсальна программа
        a = self.sleep = hours * 4
        bot.send_message(chat_id, f'Ви підняли +{a}% спати')

        bot.send_message(chat_id, f'Зараз у вас {self.sleep} процентiв')

    def check_statuts(self, chat_id):
        dedent_string = f"""Ваш пет звати: {self.name}
        Процент голодності: {self.eat}
        Процент здоровья: {self.health}
        Процент настроение: {self.mood}
        Процент спать: {self.sleep}
        Процент гігієна: {self.hygiena}
        Всего баллiв вiд iвентiв: {self.scores}"""
        bot.send_message(chat_id, textwrap.dedent(dedent_string))  # <- даний метод прибирає відступів у багаторядковому рядку

    # @private
    def _update(self):
        current_time = time.time()
        time_elapsed = current_time - self.last_update_time
        self.last_update_time = current_time

        decrease_percent = time_elapsed * 0.01  # Відсотки, на які зменшується показник за секунду
        self.eat -= int(
            self.eat * decrease_percent * random.uniform(0.8, 1.2))  # Випадкове зменшення на відсотки від 10% до 100%
        self.mood -= int(self.mood * decrease_percent * random.uniform(0.1, 1.0))
        self.sleep -= int(self.sleep * decrease_percent * random.uniform(0.8, 1.2))
        self.hygiena -= int(self.hygiena * decrease_percent * random.uniform(0.8, 1.2))
        self.health -= int(self.health * decrease_percent * random.uniform(0.8, 1.2))
        self.scores -= int(self.scores * decrease_percent * random.uniform(0.8, 1.2))
        if self.eat < 0:
            self.eat = 0
        elif self.mood < 0:
            self.mood = 0
        elif self.sleep < 0:
            self.sleep = 0
        elif self.scores < 0:
            self.scores = 0
        elif self.hygiena < 0:
            self.hygiena = 0
        elif self.health < 0:
            self.health = 0

    def event_1(self, score, chat_id):
        # bot.send_message(chat_id, 'У вас потрапив івент за назвою вгадай число від Бота. Число від 0 до 100')
        # bot.send_message(chat_id, 'Якщо ви вгадайте число від + 20 балів до вас на кишеню. У вас 3 спроби')
        count = 0
        a = random.randint(0, 100)
        while True:
            try:
                count += 1
                if count == 3:
                    bot.send_message(chat_id, 'У вас спроби закiнчились')
                    break
                elif score == a:
                    bot.send_message(chat_id, 'Ви вгадали')
                    self.scores += 20
                    break
                else:
                    # bot.send_message(chat_id, 'Неправильно введіть інше число')
                    bot.send_message(chat_id, 'Неправильно, ви проиграли')
                    break
            except ValueError:
                bot.send_message(chat_id, 'Помилка: ви повинні ввести ціле число')

    def event_2(self):
        print('У вас потрапив івент за назвою математика')
        print(
            'Ви повинні вгадати вправу. Якщо ви вгадайте число то + 20 балів до вас на кишеню. Якщо не вгадайте це то -5 балів')

        lst = ['+', '-', '*', '/']
        a = random.choice(lst)
        b_1 = random.randint(0, 100)
        b_2 = random.randint(0, 100)

        try:
            if a == '+':
                res = b_1 + b_2
                s = int(input(f'Скільки буде {b_1} + {b_2}: '))

                if s == res:
                    print('Ви вгадали')
                    self.scores += 20
                else:
                    print('Неправильно')
                    self.scores -= 5

            elif a == '-':
                res = b_1 - b_2
                s = int(input(f'Скільки буде {b_1} - {b_2}: '))

                if s == res:
                    print('Ви вгадали')
                    self.scores += 20
                else:
                    print('Неправильно')
                    self.scores -= 5

            elif a == '*':
                res = b_1 * b_2
                s = int(input(f'Скільки буде {b_1} * {b_2}: '))

                if s == res:
                    print('Ви вгадали')
                    self.scores += 20
                else:
                    print('Неправильно')
                    self.scores -= 5

            elif a == '/':
                res = b_1 / b_2
                s = int(input(f'Скільки буде {b_1} / {b_2}: '))

                if s == res:
                    print('Ви вгадали')
                    self.scores += 20
                else:
                    print('Неправильно')
                    self.scores -= 5

            else:
                raise ValueError(
                    "Некоректне арифметичне дійсло")  # якщо випадковий оператор не є однією з чотирьох можливих арифметичних

        except ValueError as e:
            print(f"Помилка: {e}")
            self.scores -= 5

    def update_database(self):
        connect = connector()

        cursor = connect.cursor()

        cursor.execute("""UPDATE Pets SET scores=%s, eat=%s, health=%s, mood=%s, sleep=%s, hygiena=%s WHERE name=%s""",
                       [self.scores, self.eat, self.health, self.mood, self.sleep, self.hygiena, self.name])

        cursor.close()
        connect.commit()
        connect.close()


def main():
    try:
        print('Добро пожаловать в игру Tamogochi')
        pets = int(input('Скільки петів ви хочете пограти: '))  # -
        pet_dict = {}
        for x in range(pets):
            name = input(f'Як звати вашого {x + 1} пета: ')  # -
            if name in pet_dict:
                print("Помилка: Пета з таким ім'ям вже існує. Будь ласка, виберіть інше ім'я.")  # -
                continue
            pet_dict[name] = x + 1
            write_data_database(name)

        print('Ось усі ваші пети, які ви створювали', pet_dict)  # -
        choice_pet = input('Який пета вы хочете поиграти: ')

        if choice_pet not in pet_dict:
            delete_data_database()
            raise TypeError("З таким ім’ям Пета немає в базі даних, яку ви створювали")

        for j in pet_dict.keys():
            if choice_pet == j:
                pet = Pet(j)
                main_2(pet, pet_dict)
    except ValueError as ex:
        raise ValueError('Ви повинні ввести число!')


def change_pet(pet, pet_dict):
    print('Ось усі ваші пети, які ви створювали', pet_dict)  # -
    choice_pet = input('Який пета ви хочете поміняти: ')
    if choice_pet not in pet_dict:
        delete_data_database()
        raise TypeError("З таким ім’ям Пета немає в базі даних, яку ви створювали.")
    for j in pet_dict.keys():
        if choice_pet == j:
            data_scores, data_eat, data_health, data_mood, data_sleep, data_hygiena = update_pets_from_database(
                choice_pet)
            pet = Pet(j, data_scores, data_eat, data_health, data_mood, data_sleep, data_hygiena)
            main_2(pet, pet_dict)


def main_2(pet, pet_dict):
    while True:
        print('Що ти хочеш робити?')
        choice = input(
            '1 - Годувати\n2 - Грати \n3 - Спати\n4 - Перевірити статус\n5 - Вибрати івент\n6 - Змiнити пета\n7 - Вихід\nВаш вибір: ')
        if choice == '1':
            pet.feed()
            pet._update()
            pet.update_database()
            continue
        elif choice == '2':
            pet.play()
            pet._update()
            pet.update_database()
            continue
        elif choice == '3':
            hours = int(input('Скільки годин ви спали?'))
            pet.sleeping(hours)
            pet._update()
            pet.update_database()
            continue
        elif choice == '4':
            pet.check_statuts()
            pet.update_database()
            continue
        elif choice == '5':
            print('Івент вибирається автоматично')
            time.sleep(2)
            a = random.randint(1, 2)
            if a == 1:
                pet.event_1()
                pet._update()
                pet.update_database()
                continue
            elif a == 2:
                pet.event_2()
                pet._update()
                pet.update_database()
                continue
        elif choice == '6':
            change_pet(pet, pet_dict)
        else:
            print('Увага якщо ви виходити з гри, то всі ваші пети видаляються.')
            delete_choice = input('Ви впевнені, що хочете вийти?: Да або Не: ').upper()
            if delete_choice == 'НЕ':
                continue
            elif delete_choice == 'ДА':
                delete_data_database()
                exit('Виходимо з гри Tamogochi')
                break
            else:
                try:
                    raise TypeError('Ви повиннi скажати да або не')
                except TypeError as ex:
                    print(ex)
                    continue


if __name__ == '__main__':  # якщо __name__ запускає на пряму програму, то результат буде  (__main__) <- str
    main()
