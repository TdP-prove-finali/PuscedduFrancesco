from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.sintomi = None #DAO.getAllSymptoms()
        self.malattie = None #DAO.getAllDiseases()
        self.utenti = None
        self.diagnosi = None
        self.archi = None
        self.mappaSintomi = {}
        self.mappaMalattie = {}
        self.mappaMalattiaSintomi = {}
        self.grafo = nx.Graph()

    def importaUtenti(self,age=None, gender=None, country=None, social_time=None, platform=None,
                      isolation_level=None, ad_interaction=None):

        query = "SELECT * FROM social_media_entertainment_data smed"
        filters = []
        params = {}

        # Mappatura delle fasce d'età in condizioni SQL
        if age:
            age_ranges = {
                "18-25": "smed.age >= 18 AND smed.age <= 25",
                "26-35": "smed.age >= 26 AND smed.age <= 35",
                "36-50": "smed.age >= 36 AND smed.age <= 50",
                "50+": "smed.age >= 50"
            }
            if age in age_ranges:
                filters.append(age_ranges[age])

        if gender:
            filters.append("smed.gender = %(gender)s")
            params["gender"] = gender

        if country:
            filters.append("smed.country = %(country)s")
            params["country"] = country

        # Mappatura delle fasce di tempo sui social
        if social_time:
            social_time_ranges = {
                "<2h": "smed.Daily_Social_Media_Hours < 2",
                "2-4h": "smed.Daily_Social_Media_Hours >= 2 AND smed.Daily_Social_Media_Hours    <= 4",
                "4-6h": "smed.Daily_Social_Media_Hours >= 4 AND smed.Daily_Social_Media_Hours <= 6",
                "6+h": "smed.Daily_Social_Media_Hours > 6"
            }
            if social_time in social_time_ranges:
                filters.append(social_time_ranges[social_time])

        if platform:
            filters.append("smed.Primary_Platform = %(platform)s")
            params["platform"] = platform

        # Mappatura del livello di isolamento
        if isolation_level:
            isolation_level_ranges = {
                "1-3": "smed.Social_Isolation_Feeling >= 1 AND smed.Social_Isolation_Feeling <= 3",
                "4-7": "smed.Social_Isolation_Feeling >= 4 AND smed.Social_Isolation_Feeling <= 7",
                "8-10": "smed.Social_Isolation_Feeling >= 8 AND smed.Social_Isolation_Feeling <= 10"
            }
            if isolation_level in isolation_level_ranges:
                filters.append(isolation_level_ranges[isolation_level])

        # Mappatura delle fasce di interazione con gli annunci
        if ad_interaction:
            ad_interaction_ranges = {
                "Low": "smed.Ad_Interaction_Count < 20",
                "Medium": "smed.Ad_Interaction_Count >= 20 AND smed.Ad_Interaction_Count <= 40",
                "High": "smed.Ad_Interaction_Count > 40"
            }
            if ad_interaction in ad_interaction_ranges:
                filters.append(ad_interaction_ranges[ad_interaction])

        # Se ci sono filtri, li aggiungiamo alla query
        if filters:
            query += " WHERE " + " AND ".join(filters)

        self.utenti = DAO.getUtenti(query, params)

    def creaMappaSintomi(self):
        for s in self.sintomi:
            self.mappaSintomi[s.__repr__()] = s
    def creaMappaMalattie(self):
        for m in self.malattie:
            self.mappaMalattie[m.Disease] = m

    def creaMappaMalattiaSintomi(self):
        pass

    def creaNodi(self):
        for m in self.malattie:
            self.grafo.add_node(m.Disease)

    def aggiornaArchi(self,sintomoStr):
        peso = self.mappaSintomi[sintomoStr].weight
        sintomo = self.mappaSintomi[sintomoStr].symptom
        self.archi = DAO.getEdges(sintomo)
        print(self.archi[0])
        if len(self.archi) == 1:
            self.diagnosi = self.archi[0][0]
            self.prognosi = self.mappaMalattie[self.diagnosi]
            print(self.diagnosi)
            print(self.prognosi)
            return self.prognosi
        for a in self.archi:
            self.grafo.add_edge(a[0],a[1])
            self.grafo[a[0]][a[1]]["weight"] = self.grafo[a[0]][a[1]].get("weight", 0) + peso
        print(self.grafo.number_of_edges())
        print(self.grafo.number_of_nodes())
        return None
    def azzeraModel(self):
        self.diagnosi = None
        self.archi = None
        self.grafo.clear_edges()

    def diagnosis(self,malattia):
        pass

    def calcola_media(self,lista):
        return sum(lista) / len(lista) if lista else 0  # Evita divisioni per zero












