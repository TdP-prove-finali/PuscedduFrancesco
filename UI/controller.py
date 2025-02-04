import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.selected_symptoms = []  # Lista per i sintomi selezionati
        self.checkboxes = []  # Lista di checkbox

    def populate_symptoms(self):
        """Riempie il dropdown con i sintomi disponibili"""
        symptoms = self._model.sintomi
        utenti = self._model.utenti
        #self._model.creaMappaSintomi()
        #self._model.creaNodi()
        #self._model.creaMappaMalattie()
        self._view.update_dropdown(utenti)

    def add_symptom(self, event):
        """Aggiunge un sintomo alla lista selezionata"""
        symptom = self._view.dropdown.value
        if symptom and symptom not in self.selected_symptoms:
            self.selected_symptoms.append(symptom)
            self._view.update_selected_symptoms(self.selected_symptoms)
            self.disease = self._model.aggiornaArchi(symptom)
            #if self.disease:
               # self._view.dropdown.disabled = True
              #  self._view.btn_diagnose.disabled = True
             #   self.output = "L'ultimo sintomo selezionato è presente solamente in una patologia, si tratta di: " + self.disease.__repr__()
            #    self._view.update_results(self.output)
            print(symptom)
            #print(self._model.mappaSintomi[symptom].symptom)

    def analyze_click(self, event):
        """Esegue la diagnosi in base ai sintomi selezionati"""
        anni = self._view.ddAge.value
        genere = self._view.ddGender.value
        paese = self._view.ddCountry.value
        tempoSocial = self._view.ddSocialTime.value
        piattaforma = self._view.ddPlatform.value
        livelloIsolamento = self._view.ddIsolationLevel.value
        interazionePubblicitaria = self._view.ddAdInteraction.value
        self._model.importaUtenti(anni,genere,paese,tempoSocial,piattaforma,livelloIsolamento,interazionePubblicitaria)
        listaOre=[]
        for u in self._model.utenti:
            listaOre.append(u.Physical_activity_Hours)
            #self._view.result_list.controls.append(ft.Text(u.User_ID))
        avg = self._model.calcola_media(listaOre)
        self._view.result_list.controls.append(ft.Text(f"Gli utenti di questo cluster in media si esercitano {avg:.2f} ore al giorno"))
        self._view.update_page()

        """diagnosis = self.get_diagnosis(self.selected_symptoms)
        self._view.update_results(diagnosis)"""
    def delete_click(self):
        pass
    def reset_click(self):
        pass

    def on_azzera_clicked(self,e):
        self._model.azzeraModel()
        self._view.selected_list.controls.clear()
        self.selected_symptoms.clear()
        self._view.dropdown.disabled = False
        self._view.btn_diagnose.disabled = False
        self._view.update_page()

    def get_diagnosis(self, symptoms):
        """Restituisce una diagnosi in base ai sintomi selezionati"""
        pass