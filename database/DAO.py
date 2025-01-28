from database.DB_connect import DBConnect
from model.symptoms import Sintomo


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllSymptoms():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from symptom_severity ss """

        cursor.execute(query)

        for row in cursor:
            result.append(Sintomo(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNeighbours():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
from neighbor n
where n.state1 < n.state2 """

        cursor.execute(query)

        for row in cursor:
            result.append((row["state1"],row["state2"]))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getPesi(anno,giorni):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select s1.state as s1,s2.state as s2,sum(abs(DATEDIFF(s1.`datetime`, s2.`datetime`))) as peso
            from sighting s1,sighting s2
            where year(s1.`datetime`) = year(s2.`datetime`) 
            and year(s2.`datetime`) = %s
            and abs(DATEDIFF(s1.`datetime`, s2.`datetime`)) <= %s
            and s1.state < s2.state
            group by s1.state,s2.state"""

        cursor.execute(query,(anno,giorni))

        for row in cursor:
            result.append((row["s1"],row["s2"],row["peso"]))

        cursor.close()
        conn.close()
        return result


