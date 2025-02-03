from database.DB_connect import DBConnect
from model.diseases import Malattia
from model.symptoms import Sintomo
from model.utenti import Utente


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllSymptoms():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                from symptom_severity ss 
                order by ss.symptom asc """

        cursor.execute(query)

        for row in cursor:
            result.append(Sintomo(**row))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getAllDiseases():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select sd.Disease,sd.Description ,sp.step1 ,sp.step2 ,sp.step3 ,sp.step4 
                from symptom_description sd , symptom_precaution sp 
                where sd.Disease = sp.Disease """

        cursor.execute(query)

        for row in cursor:
            result.append(Malattia(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(sintomo):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = f"""select t.prognosis as d1,t2.prognosis as d2
                from testing t, testing t2
                where t2.{sintomo} = t.{sintomo}
                and t2.{sintomo} = 1
                and t2.prognosis <= t.prognosis """

        cursor.execute(query)

        for row in cursor:
            result.append((row["d1"], row["d2"]))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getUtenti():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
                from social_media_entertainment_data smed """

        cursor.execute(query)

        # Social Media Fatigue level, tech savviness level, sleep quality, social isolation feeling
        # Are all classified on a scale from 1 to 10 --> (scale 1-10)#
        for row in cursor:
            u = Utente(**row)
            result.append(u)
            print(u.User_ID)

        cursor.close()
        conn.close()
        return result


