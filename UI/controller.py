import time

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
        self.ddl = []


    def analyze_click(self, event):
        self.ddl = [self._view.ddGender.value,self._view.ddScreenTime.value,self._view.ddPlatform.value,
               self._view.ddIsolationLevel.value,self._view.ddAdInteraction.value,self._view.ddSleepQuality.value]
        conto = 0
        for v in self.ddl:
            if v == "" or v is None or "Non specificat" in v:
                conto += 1
            if conto > 4:
                self._view.create_alert("Selezionare almeno 2 valori di filtraggio perfavore")
                return
        self.genere = self.ddl[0]
        self.tempoSchermi = self.ddl[1]
        self.piattaforma = self.ddl[2]
        self.livelloIsolamento = self.ddl[3]
        self.interazionePubblicitaria = self.ddl[4]
        self.qualitaSonno = self.ddl[5]
        self._view.ddGender.disabled = True
        self._view.ddScreenTime.disabled = True
        self._view.ddPlatform.disabled = True
        self._view.ddAdInteraction.disabled = True
        self._view.ddIsolationLevel.disabled = True
        self._view.ddSleepQuality.disabled = True
        self._view.result_list.controls.append(ft.Text("Potrebbe richiedere qualche secondo in base al numero di utenti"))
        t = time.time()
        nodi, archi = self._model.importaUtenti(self.genere,self.tempoSchermi,self.piattaforma,self.livelloIsolamento,self.interazionePubblicitaria,self.qualitaSonno)
        s = time.time()
        print("tempo importazione utenti e creazione grafo: " + str(s-t))
        self._view.result_list.controls.append(ft.Text(f"Importazione utenti effettuata correttamente!\n"
                                                       f"Nodi ==> Numero utenti importati: {nodi}\n"
                                                       f"Archi ==> Numero collegamenti tra gli utenti: {archi}",size=15,color="grey"))
        self._view.update_page()

    def trovaTester(self,e):
        if not self._view.ddPlatform.disabled:
            self._view.create_alert("Devi effettuare l'analisi prima di poter procedere con le operazioni!")
            return
        if self._view.ddPlatform.value == "Non specificata" or self._view.ddPlatform.value == "":
            self._view.create_alert("Inserire una piattaforma tramite il dropdown!")
            return
        conto = 0
        for v in self.ddl:
            if v == "" or v is None or "Non specificat" in v:
                conto += 1
            if conto > 2:
                self._view.create_alert("Seleziona almeno 4 valori di filtraggio perfavore.\n"
                                        "Il database è troppo grosso!")
                return
        dim = len(self._model.utenti)
        if dim >= 5:
            if dim > 120:
                self._view.result_list.controls.append(ft.Text("La ricorsione potrebbe necessitare tempo proporzionale al numero di utenti importati."))
                self._view.update_page()
            list = self._model.cercaTester()
        else:
            list = [n for n in self._model.mappaUtenti.keys()]

        provider = self._view.ddPlatform.value
        self._view.result_list.controls.append(ft.Text(f"Lista tester per {provider}",size=10,color="orange"))
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
        self._model.mappaUtenti.clear()
        self._model.livelli.clear()
        self._model.maxScore = -1
        self._model.mappaPercentualiEd.clear()
        self._model.mappaPercentualiFd.clear()
        self._model.mappaPercentualiSi.clear()
        self._model.mappaPercentualiEp.clear()
        self._model.grafo.clear()

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

    def benessereDigitale_click(self,e):
        if not self._view.ddPlatform.disabled:
            self._view.create_alert("Devi effettuare l'analisi prima di poter procedere con le operazioni!")
            return

        utenti_top10,utenti_bottom10 = self._model.calcola_equilibrio_digitale()

        self._view.result_list.controls.append(ft.Text("🔝 Top 10 utenti con miglior equilibrio digitale:",size=15,color="green"))
        for user_id, score in utenti_top10:
            percentuali = self._model.mappaPercentualiEd[user_id]
            self._view.result_list.controls.append(
                ft.Text(f"User {user_id}: Indice {score:.2f} | Attività: {percentuali[0]:.1f}%, "
                        f"Studio: {percentuali[1]:.1f}%, Sonno: {percentuali[2]:.1f}%, Schermo: {percentuali[3]:.1f}%"))

        self._view.result_list.controls.append(ft.Text("\n⚠️ Bottom 10 utenti con peggior equilibrio digitale:",size=15,color="red"))
        for user_id, score in utenti_bottom10:
            percentuali = self._model.mappaPercentualiEd[user_id]
            self._view.result_list.controls.append(
                ft.Text(f"User {user_id}: Indice {score:.2f} | Attività: {percentuali[0]:.1f}%, "
                        f"Studio: {percentuali[1]:.1f}%, Sonno: {percentuali[2]:.1f}%, Schermo: {percentuali[3]:.1f}%"))

        self._view.update_page()  # Aggiorna la UI per mostrare i nuovi dati

    def faticaDigitale_click(self,e):
        if not self._view.ddPlatform.disabled:
            self._view.create_alert("Devi effettuare l'analisi prima di poter procedere con le operazioni!")
            return

        utenti_top10, utenti_bottom10 = self._model.calcola_fatica_digitale()

        self._view.result_list.controls.append(ft.Text("⚠️ Top 10 utenti con maggiore fatica digitale:",size=15,color="red"))
        for user_id, score in utenti_top10:
            percentuali = self._model.mappaPercentualiFd[user_id]
            self._view.result_list.controls.append(
                ft.Text(f"User {user_id}: Indice {score:.2f} | Notifiche: {percentuali[0]}, "
                        f"Tempo in Community: {percentuali[1]}h, Livello Fatica Social: {percentuali[2]}, Qualità del sonno : {percentuali[3]}"))

        self._view.result_list.controls.append(ft.Text("\n🔝 Bottom 10 utenti con minor fatica digitale:",size=15,color="green"))
        for user_id, score in utenti_bottom10:
            percentuali = self._model.mappaPercentualiFd[user_id]
            self._view.result_list.controls.append(
                ft.Text(f"User {user_id}: Indice {score:.2f} | Notifiche: {percentuali[0]}, "
                        f"Tempo in Community: {percentuali[1]}h, Livello Fatica Social: {percentuali[2]}, Qualità del sonno: {percentuali[3]}"))

        self._view.update_page()  # Aggiorna la UI per mostrare i nuovi dati

    def spesaIntrattenimento_click(self,e):
        if not self._view.ddPlatform.disabled:
            self._view.create_alert("Devi effettuare l'analisi prima di poter procedere con le operazioni!")
            return

        utenti_top10, utenti_bottom10 = self._model.calcola_spesa_intrattenimento()

        self._view.result_list.controls.append(ft.Text("🔝 Top 10 utenti con maggiore spesa sull’intrattenimento:",size=15,color="green"))
        for user_id, score in utenti_top10:
            spesa, piattaforme, piattaforma_preferita = self._model.mappaPercentualiSi[user_id]
            self._view.result_list.controls.append(
                ft.Text(f"User {user_id}: Indice {score:.2f} | Spesa: ${spesa:.2f}, "
                        f"Iscrizione a Piattaforme: {piattaforme}, Preferenza: {piattaforma_preferita}"))

        self._view.result_list.controls.append(ft.Text("\n⚠️ Bottom 10 utenti con minore spesa sull’intrattenimento:",size=15,color="red"))
        for user_id, score in utenti_bottom10:
            spesa, piattaforme, piattaforma_preferita = self._model.mappaPercentualiSi[user_id]
            self._view.result_list.controls.append(
                ft.Text(f"User {user_id}: Indice {score:.2f} | Spesa: ${spesa:.2f}, "
                        f"Iscrizione a Piattaforme: {piattaforme}, Preferenza: {piattaforma_preferita}"))

        self._view.update_page()  # Aggiorna la UI per mostrare i nuovi dati

    def esposizioneAds_click(self,e):
        if not self._view.ddPlatform.disabled:
            self._view.create_alert("Devi effettuare l'analisi prima di poter procedere con le operazioni!")
            return

        utenti_top10, utenti_bottom10 = self._model.calcola_esposizione_ads()

        self._view.result_list.controls.append(ft.Text("🔝 Top 10 utenti più esposti ai contenuti pubblicitari:",size=15,color="green"))
        for user_id, score in utenti_top10:
            ad_interactions, screen_hours, notifications = self._model.mappaPercentualiEp[user_id]
            self._view.result_list.controls.append(
                ft.Text(f"User {user_id}: Indice {score:.2f} | Ads: {ad_interactions}, "
                        f"Schermo: {screen_hours:.1f} h, Notifiche: {notifications}"))

        self._view.result_list.controls.append(ft.Text("\n⚠️ Bottom 10 utenti meno esposti ai contenuti pubblicitari:",size=15,color="red"))
        for user_id, score in utenti_bottom10:
            ad_interactions, screen_hours, notifications = self._model.mappaPercentualiEp[user_id]
            self._view.result_list.controls.append(
                ft.Text(f"User {user_id}: Indice {score:.2f} | Ads: {ad_interactions}, "
                        f"Schermo: {screen_hours:.1f} h, Notifiche: {notifications}"))

        self._view.update_page()  # Aggiorna la UI per mostrare i nuovi dati






