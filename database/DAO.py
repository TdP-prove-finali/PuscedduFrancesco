from database.DB_connect import DBConnect
from model.utenti import Utente


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getUtenti(query,params):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        cursor.execute(query,params)
        print(query)

        # Social Media Fatigue level, tech savviness level, sleep quality, social isolation feeling
        # Are all classified on a scale from 1 to 10 --> (scale 1-10)#
        for row in cursor:
            u = Utente(**row)
            result.append(u)
            print(u.User_ID)

        cursor.close()
        conn.close()
        return result




