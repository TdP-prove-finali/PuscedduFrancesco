from database.DB_connect import DBConnect
from model.diseases import Malattia
from model.symptoms import Sintomo


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
    def getNeighbours(sintomo):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.prognosis as d1,t2.prognosis as d2
                from testing t, testing t2
                where t2.%s = t.%s 
                and t2.%s = 1
                and t2.prognosis < t.prognosis """

        cursor.execute(query,(sintomo,sintomo,sintomo))

        for row in cursor:
            result.append((row["d1"], row["d2"]))

        cursor.close()
        conn.close()
        return result


