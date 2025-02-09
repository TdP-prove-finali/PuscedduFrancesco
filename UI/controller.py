import base64
import heapq
import time
import matplotlib.pyplot as plt
from collections import Counter
from io import BytesIO

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # valori dei dd
        self.genere = None
        self.tempoSchermi = None
        self.piattaforma = None
        self.livelloIsolamento = None
        self.interazionePubblicitaria = None
        self.qualitaSonno = None


    def analyze_click(self, event):
        ddl = [self._view.ddGender.value,self._view.ddScreenTime.value,self._view.ddPlatform.value,
               self._view.ddIsolationLevel.value,self._view.ddAdInteraction.value,self._view.ddSleepQuality.value]
        conto = 0
        for v in ddl:
            if v == "" or v is None or "Non specificat" in v:
                conto += 1
            if conto > 3:
                self._view.create_alert("Seleziona almeno 3 valori di filtraggio perfavore.\n"
                                        "Il database è troppo grosso!")
                return
        self.genere = ddl[0]
        self.tempoSchermi = ddl[1]
        self.piattaforma = ddl[2]
        self.livelloIsolamento = ddl[3]
        self.interazionePubblicitaria = ddl[4]
        self.qualitaSonno = ddl[5]
        self._view.ddGender.disabled = True
        self._view.ddScreenTime.disabled = True
        self._view.ddPlatform.disabled = True
        self._view.ddAdInteraction.disabled = True
        self._view.ddIsolationLevel.disabled = True
        self._view.ddSleepQuality.disabled = True
        t = time.time()
        self._model.importaUtenti(self.genere,self.tempoSchermi,self.piattaforma,self.livelloIsolamento,self.interazionePubblicitaria,self.qualitaSonno)
        s = time.time()
        print("tempo importazione utenti: " + str(s-t))
        self._view.result_list.controls.append(ft.Text(f"Importazione utenti effettuata correttamente!\n"
                                                       f"importati: {len(self._model.utenti)} utenti"))
        #self.attivitaFisica()
        self._view.update_page()
    def attivitaFisica(self):
        listaOre = []
        listaOreSocial = []
        for u in self._model.utenti:
            listaOre.append(u.Physical_activity_Hours)
            #listaOreSocial.append(u.Daily_Social_Media_Hours)
            # self._view.result_list.controls.append(ft.Text(u.User_ID))
        contatore = Counter(listaOre)
        print(contatore)
        lutenti = self._model.utenti
        for numero, conteggio in sorted(contatore.items(), key=lambda x: x[1], reverse=True):
            percent = conteggio / len(lutenti) * 100
            self._view.result_list.controls.append(ft.Text(f"Si allenano per {numero} ore --> {percent:.2f}% degli utenti"))
        avg = self._model.calcola_media(listaOre)
        self._view.result_list.controls.append(
            ft.Text(f"Gli utenti di questo cluster in media si esercitano {avg:.2f} ore al giorno"))
        self._view.update_page()

    def trovaTester(self,e):
        if not self._view.ddPlatform.disabled:
            self._view.create_alert("Devi effettuare l'analisi prima di poter procedere con le operazioni!")
        if self._view.ddPlatform.value == "Non specificata" or self._view.ddPlatform.value == "":
            self._view.create_alert("Inserire una piattaforma tramite il dropdown!")
            return
        nodi, archi, list = self._model.cercaTester()
        provider = self._view.ddPlatform.value
        self._view.result_list.controls.append(ft.Text(f"nodi: {nodi}\n"
                                                       f"archi: {archi}\n"
                                                       f"Lista tester per {provider}"))
        n = 0
        for l in list:
            i = self._model.mappaUtenti[l]
            n += 1
            self._view.result_list.controls.append(ft.Text(f"{n}) ID: {i.User_ID} --> {i.Daily_Social_Media_Hours}"))
            self._view.result_list.controls.append(ft.Text(f"   '--> età: {i.age}; paese: {i.country}; occupazione: {i.occupation}; salario: {i.Monthly_Income_USD}"))
        self._view.update_page()

    def delete_click(self,e):
        self._view.result_list.controls.clear()
        self._view.update_page()
    def reset_click(self,e):
        self._model.utenti = []
        self._model.grafo.clear()
        print(self._view.ddPlatform.value + "bbb")
        if self._view.ddGender:
            self._view.ddGender.value = None
            self._view.ddGender.disabled = False
        if self._view.ddScreenTime:
            self._view.ddScreenTime.value = None
            self._view.ddScreenTime.disabled = False
        if self._view.ddPlatform != "":
            self._view.ddPlatform.value = ""
            self._view.ddPlatform.disabled = False
        if self._view.ddIsolationLevel:
            self._view.ddIsolationLevel.value = None
            self._view.ddIsolationLevel.disabled = False
        if self._view.ddAdInteraction:
            self._view.ddAdInteraction.value = None
            self._view.ddAdInteraction.disabled = False
        if self._view.ddSleepQuality:
            self._view.ddSleepQuality.value = None
            self._view.ddSleepQuality.disabled = False
        self._view.update_page()

    def percentage_click(self,e):
        self._model.percentuali()
        n = 1
        self._view.result_list.controls.append(ft.Text(f"Tempo giornaliero in percentuale degli utenti"))
        for u in self._model.mappaPercentuali.keys():
            a,b,c = self._model.mappaPercentuali[u]
            self._view.result_list.controls.append(ft.Text(f"{n}) ID: {u} --> Allenamento: {a:.2f}%, Lavoro/Studio: {b:.2f}%, Sonno: {c:.2f}%"))
            n +=1
        self._view.update_page()


    def stats_click(self,e):
        self._view.result_list.controls.append(ft.Text(f"Statistiche degli utenti"))
        paAvg, paMax, paMin, paDevStd, wsAvg, wsMax, wsMin, wsDevStd, sAvg, sMax, sMin, sDevStd = self._model.statistiche()
        self._view.result_list.controls.append(ft.Text(f"Attività fisica:\n"
                                                       f"media: {paAvg:.2f}, massimo: {paMax:.2f}, minimo: {paMin:.2f}, deviazione standard: {paDevStd:.2f}"))
        self._view.result_list.controls.append(ft.Text(f"Lavoro/Studio:\n"
                                                       f"media: {wsAvg:.2f}, massimo: {wsMax:.2f}, minimo: {wsMin:.2f}, deviazione standard: {wsDevStd:.2f}"))
        self._view.result_list.controls.append(ft.Text(f"Sonno:\n"
                                                       f"media: {sAvg:.2f}, massimo: {sMax:.2f}, minimo: {sMin:.2f}, deviazione standard: {sDevStd:.2f}"))
        self._view.update_page()


        """    def generate_chart(self, activity):
             data = self._model.get_activity_data(activity)
             names = list(data.keys())
             values = list(data.values())

             plt.figure(figsize=(7, 3))
             plt.scatter(names, values, color="blue", s=0)  # Grafico a punti
             plt.xlabel("Persone")
             plt.ylabel("Ore spese")
             plt.title(f"Ore spese in {activity}")

             # Convertire il grafico in immagine base64
             img = BytesIO()
             plt.savefig(img, format="png")
             img.seek(0)
             plt.close()

             return base64.b64encode(img.getvalue()).decode()"""


