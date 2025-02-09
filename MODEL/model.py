import copy
import statistics
import time

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.utenti = None
        self.mappaUtenti = {}
        self.nodoGrosso = None
        self.grafo = nx.Graph()
        self.percorso = []
        self.bestSol = None
        self.maxScore = -1
        self.mappaPercentuali = {}

    def importaUtenti(self, gender=None, social_time=None, platform=None,
                      isolation_level=None, ad_interaction=None, sleep_quality=None):

        query = "SELECT * FROM social_media_entertainment_data smed"
        filters = []
        params = {}

        if gender and gender != "Non specificato":
            filters.append("smed.gender = %(gender)s")
            params["gender"] = gender

        # Mappatura delle fasce di tempo sui social
        if social_time:
            social_time_ranges = {
                "1": "smed.Daily_Social_Media_Hours < 2",
                "2": "smed.Daily_Social_Media_Hours >= 2 AND smed.Daily_Social_Media_Hours <= 4",
                "3": "smed.Daily_Social_Media_Hours >= 4 AND smed.Daily_Social_Media_Hours <= 6",
                "4": "smed.Daily_Social_Media_Hours > 6"
            }
            if social_time in social_time_ranges:
                filters.append(social_time_ranges[social_time])

        if platform and platform != "Non specificata":
            filters.append("smed.Primary_Platform = %(platform)s")
            params["platform"] = platform

        if isolation_level and isolation_level != "Non specificato":
            filters.append("smed.Social_Isolation_Feeling = %(iso_lvl)s")
            params["iso_lvl"] = isolation_level

        # Mappatura delle fasce di interazione con gli annunci
        if ad_interaction:
            ad_interaction_ranges = {
                "Low": "smed.Ad_Interaction_Count < 20",
                "Medium": "smed.Ad_Interaction_Count >= 20 AND smed.Ad_Interaction_Count <= 40",
                "High": "smed.Ad_Interaction_Count > 40"
            }
            if ad_interaction in ad_interaction_ranges:
                filters.append(ad_interaction_ranges[ad_interaction])

        if sleep_quality and sleep_quality != "Non specificata":
            filters.append("smed.Sleep_Quality = %(sleep)s")
            params["sleep"] = sleep_quality

        # Se ci sono filtri, li aggiungiamo alla query
        if filters:
            query += " WHERE " + " AND ".join(filters)

        self.utenti = DAO.getUtenti(query, params)
        self.creaMappa()
    def creaMappa(self):
        for u in self.utenti:
            self.mappaUtenti[u.User_ID] = u
    def creaGrafo(self):
        t = time.time()
        nodes = list(self.mappaUtenti.keys())
        self.grafo = nx.complete_graph(nodes)
        print(len(nodes))
        """oreMax = 0
        for i in range(len(nodes)):
            print(i)
            for j in range(i + 1, len(nodes)):  # Evita di ripetere coppie già viste
                u1, u2 = nodes[i], nodes[j]
                tu1 = self.mappaUtenti[u1].Daily_Social_Media_Hours
                tu2 = self.mappaUtenti[u2].Daily_Social_Media_Hours
                weight = (tu1 + tu2) / 2  # Calcolo del peso (media)
                if weight > oreMax:
                    oreMax = weight
                    self.nodoGrosso = u1
                self.grafo[u1][u2]["weight"] = weight
        s = time.time()
        print("tempo creazione archi: " + str(s-t))"""

    # Un provider di servizi (twitter, facebook ecc...) vuole introdurre nuove features
    # e quindi trovare una decina di persone adeguate al testing e quindi:
    # massimizza il daily social media hours
    # diversifica il più possibile le caratteristiche di queste persone
    # Ad esempio Salario, occupazione, età, paese #
    def cercaTester(self):
        self.creaGrafo()
        nodi_ordinati = list(self.mappaUtenti.keys())
        self.ricorsione([], nodi_ordinati, 0)  # Partiamo con diversità = 0
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges(), self.bestSol

    def ricorsione(self, parziale, nodiRimasti, diversityScore):
        print(parziale)
        print("---------------------------------------")
        if len(parziale) == 3:  # Se abbiamo raggiunto il numero massimo di nodi
            if diversityScore > self.maxScore:  # Aggiorna solo se il punteggio è migliore
                self.bestSol = list(parziale)
                self.maxScore = diversityScore
            return  # Termina la funzione

        for i, u in enumerate(nodiRimasti):
            # Assicura ordine crescente per evitare duplicati e massimizzare le ore sul social media
            if parziale:
                t1 = self.mappaUtenti[u].Daily_Social_Media_Hours
                t2 = self.mappaUtenti[parziale[-1]].Daily_Social_Media_Hours
                if t2 < t1:
                    continue
            parziale.append(u)
            # Calcoliamo solo il contributo aggiuntivo di u
            newScore = self.aggiornaScore(parziale,diversityScore, u)
            # Ricorsione con il nuovo score già aggiornato
            self.ricorsione(parziale, nodiRimasti[i+1:], newScore)
            parziale.pop()

    def aggiornaScore(self, utenti, punteggio, last):
        #----------------------------------------------------------------------------------------
        # Opzione 1: indicizziamo anche le ore del social e le facciamo pesare nel punteggio
        # In questo modo è come se una diversità valesse 1h in più sul social
        punteggio = punteggio + self.mappaUtenti[last].Daily_Social_Media_Hours
        #----------------------------------------------------------------------------------------
        # Opzione 2: il punteggio indica solo la diversità e non tutto un complessivo punteggio
        # comprensivo anche delle ore passate sul social
        # le ore passate sul social verranno considerate solo attraverso la selezione nella ricorsione
        #----------------------------------------------------------------------------------------
        for u in utenti:
            if self.mappaUtenti[u].country != self.mappaUtenti[last].country:
                punteggio += 1
            if self.mappaUtenti[u].occupation != self.mappaUtenti[last].occupation:
                punteggio += 1
            punteggio += self.indiceDiversita(self.mappaUtenti[u].Monthly_Income_USD, self.mappaUtenti[last].Monthly_Income_USD)
            punteggio += self.indiceDiversita(self.mappaUtenti[u].age, self.mappaUtenti[last].age)
        return punteggio
    def indiceDiversita(self,v1,v2):
        # Mi sono inventato questa funzione per avere un indice il più vicino possibile ad 1
        # Inoltre tiene conto anche del fatto che se la differenza tra i valori è molta sarà un po più di 1
        # viceversa se la differenza è poca sarà più vicinp allo 0, infatti se è uguale sarà 0
        # Ho fatto le prove e il massimo valore di differenza di stipendio è circa 1.8, invece per l'età è 1.33, pertanto mi sembra buono
        #-------------------------------------------------------------------------------------------------------------------------------
        # faccio la differenza in valore assoluto dei due valori
        diff = abs(v1-v2)
        # poi ne faccio la media
        avg = (v1+v2)/2
        # restituisco il rapporto dei due
        return diff/avg
        # casi estremi: sono uguali --> diff = 0 ==> indice = 0
        # sono uno il doppio dell'altro --> diff = avg ==> indice = 1
    def percentuali(self):
        for u in self.utenti:
            a = u.Physical_activity_Hours*100/24
            b = u.Work_or_Study_Hours*100/24
            c = u.Average_Sleep_Hours*100/24
            self.mappaPercentuali[u.User_ID] = (a,b,c)
    def statistiche(self):
        lpa = []
        lws = []
        ls = []
        for u in self.utenti:
            lpa.append(u.Physical_activity_Hours)
            lws.append(u.Work_or_Study_Hours)
            ls.append(u.Average_Sleep_Hours)
        paAvg, paMax, paMin, paDevStd = self.calcola_media(lpa),max(lpa),min(lpa),statistics.stdev(lpa)
        wsAvg, wsMax, wsMin, wsDevStd = self.calcola_media(lws),max(lws),min(lws),statistics.stdev(lws)
        sAvg, sMax, sMin, sDevStd = self.calcola_media(ls),max(ls),min(ls),statistics.stdev(ls)
        return paAvg, paMax, paMin, paDevStd, wsAvg, wsMax, wsMin, wsDevStd, sAvg, sMax, sMin, sDevStd
    def calcola_media(self,lista):
        return sum(lista) / len(lista) if lista else 0  # Evita divisioni per zero

    """def get_activity_data(self, activity):
        if activity == "train":
            return {u.User_ID: u.Physical_activity_Hours for u in self.utenti}
        if activity == "work":
            return {u.User_ID: u.Work_or_Study_Hours for u in self.utenti}
        if activity == "read":
            return {u.User_ID: u.Reading_Hours for u in self.utenti}"""












