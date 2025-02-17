import statistics
import time

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.utenti = None
        self.mappaUtenti = {}
        self.livelli = {}
        self.grafo = nx.DiGraph()
        self.bestSol = []
        self.maxScore = -1
        self.mappaPercentualiEd = {}
        self.mappaPercentualiFd = {}
        self.mappaPercentualiSi = {}
        self.mappaPercentualiEp = {}


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
        self.creaMappe()
        nodi = self.grafo.number_of_nodes()
        archi = self.grafo.number_of_edges()
        return nodi, archi
    def creaMappe(self):
        for u in self.utenti:
            # Dizionario per raggruppare TUTTI gli utenti
            self.mappaUtenti[u.User_ID] = u
            # Dizionario per raggruppare utenti per livello
            if u.Subscription_Platforms == 0:  # Escludo gli utenti non iscritti alla piattaforma
                continue

            livello = u.Social_Media_Platforms_Used

            if livello not in self.livelli:
                self.livelli[livello] = []
            self.livelli[livello].append(u.User_ID)

        if len(self.utenti) < 30:
            self.creaGrafoPiccolo()
        else:
            self.creaGrafo()

    def creaGrafoPiccolo(self):
        nodes = list(self.mappaUtenti.keys())
        self.grafo = nx.complete_graph(nodes, create_using=nx.Graph())
        print(self.grafo.number_of_edges())
    def creaGrafo(self):
        t = time.time()
        nodes = list(self.mappaUtenti.keys())
        self.grafo.add_nodes_from(nodes)
        # Connessioni solo tra livelli adiacenti
        livelli_ordinati = sorted(self.livelli.keys())
        for i in range(len(livelli_ordinati) - 1):  # Iteriamo solo fino al penultimo livello
            livello_attuale = livelli_ordinati[i]
            livello_successivo = livelli_ordinati[i + 1]
            for u1 in self.livelli[livello_attuale]:
                for u2 in self.livelli[livello_successivo]:
                    self.grafo.add_edge(u1, u2)  # Collegamento tra livelli adiacenti
                    print(u1,u2)
        s = time.time()
        print("tempo creazione archi: " + str(s-t))

    # Un provider di servizi (twitter, facebook ecc...) vuole introdurre nuove features
    # e quindi trovare una decina di persone adeguate al testing e quindi:
    # massimizza il daily social media hours
    # diversifica il più possibile le caratteristiche di queste persone
    # Ad esempio Salario, occupazione, età, paese #
    def cercaTester(self):
        if len(self.utenti) < 30:
            for nodo in self.mappaUtenti.keys():
                self.ricorsione([nodo], nodo,[nodo],0)
        else:
            for nodo in self.livelli[1]:  # Partiamo dai nodi del livello 1
                self.ricorsione([nodo], nodo, [nodo], 0)  # Ogni chiamata ha una lista separata
        return self.grafo.number_of_nodes(), self.grafo.number_of_edges(), self.bestSol

    def ricorsione(self, parziale, nodoAttuale, nodiVisitati, diversityScore):
        #(parziale)
        #print("---------------------------------------")

        if len(parziale) == 5:  # Se abbiamo raggiunto il numero massimo di nodi
            if diversityScore > self.maxScore:  # Aggiorna solo se il punteggio è migliore
                self.bestSol = list(parziale)
                self.maxScore = diversityScore
                print(self.bestSol)
                print(f"score: + {self.maxScore:.2f}")
                print("---------------------------------------")
            return  # Termina la funzione

        vicini = list(self.grafo.neighbors(nodoAttuale))  # Nodi adiacenti al nodo attuale
        nodiViciniBuoni = [n for n in vicini if n not in nodiVisitati]  # Lista normale

        for nodo in nodiViciniBuoni:
            # Assicura ordine crescente per evitare duplicati e massimizzare le ore sul social media
            t1 = self.mappaUtenti[nodo].Daily_Social_Media_Hours
            t2 = self.mappaUtenti[parziale[-1]].Daily_Social_Media_Hours
            if t2 > t1:  # Mantiene ordine corretto
                continue
            parziale.append(nodo)
            nodiVisitati.append(nodo)

            # Calcoliamo solo il contributo aggiuntivo di nodo
            newScore = self.aggiornaScore(parziale, diversityScore, nodo)

            # Ricorsione con il nuovo score già aggiornato
            self.ricorsione(parziale, nodo, nodiVisitati[:], newScore)  # Passiamo una copia di nodiVisitati

            parziale.pop()
            nodiVisitati.pop()

    def aggiornaScore(self, utenti, punteggio, last):
        #----------------------------------------------------------------------------------------
        # Indicizzo anche le ore del social e le facciamo pesare nel punteggio
        # In questo modo è come se una diversità valesse 1h in più sul social
        punteggio = punteggio + self.mappaUtenti[last].Daily_Social_Media_Hours
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
        #-------------------------------------------------------------------------------------------------------------------------------
        # faccio la differenza in valore assoluto dei due valori
        diff = abs(v1-v2)
        # poi ne faccio la media
        avg = (v1+v2)/2
        # restituisco il rapporto dei due
        return diff/avg
        # casi estremi: sono uguali --> diff = 0 ==> indice = 0
        # sono uno il doppio dell'altro --> diff = avg ==> indice = 1

    # Ho fatto le prove e il massimo valore di differenza di stipendio è circa 1.8, invece per l'età è 1.33, pertanto mi sembra buono

    def calcola_equilibrio_digitale(self):
        equilibrio_digitale = {}

        # Calcolo indice e percentuali giornaliere
        for u in self.utenti:
            # Percentuali sul totale di 24 ore
            a = (u.Physical_activity_Hours * 100) / 24  # Attività fisica
            b = (u.Work_or_Study_Hours * 100) / 24  # Lavoro/studio
            c = (u.Average_Sleep_Hours * 100) / 24  # Sonno
            d = (u.Screen_Hours * 100) / 24  # Tempo davanti a uno schermo

            # Memorizziamo le percentuali per l'utente
            self.mappaPercentualiEd[u.User_ID] = (a, b, c, d)

            # Calcolo dell'indice di equilibrio digitale
            score = (u.Physical_activity_Hours +
                     u.Average_Sleep_Hours -
                     u.Work_or_Study_Hours -
                     u.Screen_Hours)

            equilibrio_digitale[u.User_ID] = score

        # Ordiniamo gli utenti in base all'Indice di Equilibrio Digitale
        risultati_top10 = sorted(equilibrio_digitale.items(), key=lambda x: x[1], reverse=True)[:10]
        risultati_bottom10 = sorted(equilibrio_digitale.items(), key=lambda x: x[1])[:10]

        return risultati_top10, risultati_bottom10

    def calcola_fatica_digitale(self):
        fatica_digitale = {}

        # Calcolo indice e percentuali giornaliere
        for u in self.utenti:
            a = u.Notifications_Received_Daily
            b = u.Hours_Spent_in_Online_Communities # Ore in community rispetto a 24h
            c = u.Social_Media_Fatigue_Level
            d = u.Sleep_Quality

            # Memorizziamo le percentuali per l'utente
            self.mappaPercentualiFd[u.User_ID] = (a, b, c, d)

            # Calcolo dell'indice di fatica digitale
            score = (a * b/24 + c - d)

            fatica_digitale[u.User_ID] = score

        # Ordiniamo gli utenti per punteggio di fatica digitale
        utenti_top10 = sorted(fatica_digitale.items(), key=lambda x: x[1], reverse=True)[:10]
        utenti_bottom10 = sorted(fatica_digitale.items(), key=lambda x: x[1])[:10]

        return utenti_top10, utenti_bottom10

    def calcola_spesa_intrattenimento(self):
        spesa_intrattenimento = {}

        # Calcolo indice e percentuali giornaliere
        for u in self.utenti:
            a = u.Monthly_Expenditure_on_Entertainment_USD
            b = u.Subscription_Platforms  # Normalizziamo considerando un massimo di 10 piattaforme
            if b == 0:  # Escludo utenti non iscritti a piattaforme
                continue
            # Memorizziamo le percentuali per l'utente
            self.mappaPercentualiSi[u.User_ID] = (a, b, u.Preferred_Entertainment_Platform)

            # Calcolo dell'indice di spesa per l’intrattenimento
            score = (a/500 * b) # Normalizziamo su un massimo di 500$

            spesa_intrattenimento[u.User_ID] = score

        # Ordiniamo gli utenti per punteggio di spesa sull’intrattenimento
        utenti_top10 = sorted(spesa_intrattenimento.items(), key=lambda x: x[1], reverse=True)[:10]
        utenti_bottom10 = sorted(spesa_intrattenimento.items(), key=lambda x: x[1])[:10]

        return utenti_top10, utenti_bottom10

    def calcola_esposizione_ads(self):
        esposizione_ads = {}

        # Calcolo indice e salvataggio dati reali
        for u in self.utenti:
            a = u.Ad_Interaction_Count  # Numero puro
            b = u.Screen_Hours  # Ore
            c = u.Notifications_Received_Daily  # Numero puro

            # Memorizziamo i valori per l'utente
            self.mappaPercentualiEp[u.User_ID] = (a,b,c)

            # Calcolo dell'indice di esposizione agli ads
            score = (a + c) * b/24

            esposizione_ads[u.User_ID] = score

        # Ordiniamo gli utenti per punteggio di esposizione agli ads
        utenti_top10 = sorted(esposizione_ads.items(), key=lambda x: x[1], reverse=True)[:10]
        utenti_bottom10 = sorted(esposizione_ads.items(), key=lambda x: x[1])[:10]

        return utenti_top10, utenti_bottom10

    def calcola_media(self,lista):
        return sum(lista) / len(lista) if lista else 0  # Evita divisioni per zero













