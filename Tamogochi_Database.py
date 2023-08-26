import mysql.connector

from Config_MySql import connector

def write_data_database(pet):
    connection = connector()

    cursor = connection.cursor()

    query = """INSERT INTO Pets (name, scores, eat, health, mood, sleep, hygiena) VALUES (%s, 100, 100, 100, 100, 100, 100)"""
    values = (pet,)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

def delete_data_database():
    connection = connection = connector()

    cursor = connection.cursor()

    query = """DELETE FROM Pets"""

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()

def update_pets_from_database(choice_pet):
    connect = connection = connector()

    cursor = connect.cursor()
    cursor.execute(f"""SELECT * FROM Pets WHERE name = '{choice_pet.replace("'", "''")}'""")

    data = cursor.fetchall()

    data_scores = data[0][1]
    data_eat = data[0][2]
    data_health = data[0][3]
    data_mood = data[0][4]
    data_sleep = data[0][5]
    data_hygiena = data[0][6]

    cursor.close()
    connect.commit()
    connect.close()

    return data_scores, data_eat, data_health, data_mood, data_sleep, data_hygiena