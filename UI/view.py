import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Diagnostica Medica"
        self._page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self.countries = []

        self._controller = None
        self.selected_list = None
        self.btn_analyze = None
        self.ddAge = None
        self.ddGender = None
        self.ddCountry = None
        self.ddSocialTime = None
        self.ddPlatform = None
        self.ddIsolationLevel = None
        self.ddAdInteraction = None
        self.result_list = None

    def load_interface(self):
        self._title = ft.Text("Interazioni Social", color="blue", size=24)
        self._page.controls.append(ft.Container(content=self._title, alignment=ft.alignment.center))

        # Dropdown per i filtri
        self.ddAge = ft.Dropdown(
            label="Fascia d'età",
            value=None,
            options=[
                ft.dropdown.Option(None, "Non specificata"),
                ft.dropdown.Option("1","<18"),
                ft.dropdown.Option("2","18-25"),
                ft.dropdown.Option("3","26-35"),
                ft.dropdown.Option("4","36-50"),
                ft.dropdown.Option("5","50+")
            ]
        )

        self.ddGender = ft.Dropdown(
            label="Genere",
            value=None,
            options=[
                ft.dropdown.Option(None, "Non specificato"),
                ft.dropdown.Option("Male", "Maschio"),
                ft.dropdown.Option("Female", "Femmina"),
                ft.dropdown.Option("Other", "Altro")
            ]
        )

        self.ddCountry = ft.Dropdown(
            label="Paese",
            value=None,
            options=[
                ft.dropdown.Option(None, "Non specificato"),
                ft.dropdown.Option("USA"),
                ft.dropdown.Option("India"),
                ft.dropdown.Option("Germany"),
                ft.dropdown.Option("UK"),
                ft.dropdown.Option("France")
            ]
        )

        self.ddSocialTime = ft.Dropdown(
            label="Tempo sui social",
            value=None,
            options=[
                ft.dropdown.Option(None, "Non specificato"),
                ft.dropdown.Option("1","<2h"),
                ft.dropdown.Option("2","2-4h"),
                ft.dropdown.Option("3","4-6h"),
                ft.dropdown.Option("4","6+h")
            ]
        )

        self.ddPlatform = ft.Dropdown(
            label="Piattaforma preferita",
            value=None,
            options=[
                ft.dropdown.Option(None, "Non specificata"),
                ft.dropdown.Option("TikTok"),
                ft.dropdown.Option("YouTube"),
                ft.dropdown.Option("Instagram"),
                ft.dropdown.Option("Facebook")
            ]
        )

        self.ddIsolationLevel = ft.Dropdown(
            label="Livello di isolamento sociale",
            value=None,
            disabled=True,
            options=[ft.dropdown.Option(None, "Non specificato")] + [ft.dropdown.Option(str(i)) for i in range(1, 11)]
        )

        self.ddAdInteraction = ft.Dropdown(
            label="Interazione con gli annunci",
            value=None,
            options=[
                ft.dropdown.Option(None, "Non specificata"),
                ft.dropdown.Option("", "Bassa"),
                ft.dropdown.Option("Medium", "Media"),
                ft.dropdown.Option("High", "Alta")
            ]
        )

        # Prima riga del layout dopo il titolo
        row1 = ft.Row(
            [self.ddAge, self.ddGender, self.ddCountry],  # Aggiungiamo gli elementi
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10  # Spazio tra gli elementi
        )
        self._page.controls.append(row1)

        # Seconda riga del layout
        row2 = ft.Row(
            [self.ddPlatform, self.ddSocialTime, self.ddAdInteraction,], # self.ddIsolationLevel
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
        self._page.controls.append(row2)

        # Pulsante per eseguire l'analisi
        self.btn_analyze = ft.ElevatedButton(
            text="Analizza", on_click=self.controller.analyze_click
        )
        self._page.controls.append(ft.Container(content=self.btn_analyze, alignment=ft.alignment.center))

        # Pulsante per eseguire cancellare la view
        self.btn_delete = ft.ElevatedButton(
            text="Analizza", on_click=self.controller.delete_click
        )
        self._page.controls.append(ft.Container(content=self.btn_analyze, alignment=ft.alignment.center))

        # Pulsante per resettare gli utenti
        self.btn_reset = ft.ElevatedButton(
            text="Analizza", on_click=self.controller.reset_click
        )
        self._page.controls.append(ft.Container(content=self.btn_analyze, alignment=ft.alignment.center))



        # ListView per mostrare i risultati
        self.result_list = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.result_list)

        # Aggiorno la pagina
        self.update_page()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_dropdown(self, symptoms):
        """Aggiorna la lista dei sintomi nel dropdown"""
        for s in symptoms:
            if s.country not in self.countries:
                self.countries.append(s.country)
                #self.dropdown.options.append(ft.dropdown.Option(s.User_ID))
        self.update_page()

    def update_selected_symptoms(self, selected_symptoms):
        """Aggiorna la lista dei sintomi selezionati"""
        self.selected_list.controls = [ft.Text(s) for s in selected_symptoms]
        self.update_page()

    def update_results(self, diagnosis_text):
        """Aggiorna la lista dei risultati della diagnosi"""
        self.selected_list.controls.append(ft.Text(f"🔎 Diagnosi: {diagnosis_text}", color="red"))
        self.update_page()

    def create_alert(self, message):
        """Mostra un alert"""
        dlg = ft.AlertDialog(
            title=ft.Text("Attenzione"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=self.close_alert)],
        )
        self._page.dialog = dlg
        dlg.open = True
        self.update_page()

    def close_alert(self, event):
        """Chiude l'alert dialog"""
        self._page.dialog.open = False
        self.update_page()
    def update_page(self):
        """Aggiorna la UI"""
        self._page.update()

"""      Carica l'interfaccia grafica
        self._title = ft.Text("Diagnostica Medica", color="blue", size=24)
        self._page.controls.append(self._title)

        # Dropdown per selezione sintomi
        self.dropdown = ft.Dropdown(label="Cerca e seleziona sintomi", on_change=self.controller.add_symptom,
                                    options=[])

        # Lista sintomi selezionati
        self.selected_list = ft.ListView(expand=1, spacing=10, padding=10)

        # Bottone per avviare la diagnosi
        self.btn_diagnose = ft.ElevatedButton(text="Diagnostica", on_click=self.controller.on_diagnose_click)

        # Bottone per azzerare i dati
        self.azzera_button = ft.ElevatedButton(text="Azzera", on_click=self.controller.on_azzera_clicked)

        # Prima riga del layout dopo il titolo
        row1 = ft.Row(
            [self.dropdown, self.btn_diagnose, self.azzera_button],  # Aggiungiamo gli elementi
            alignment=ft.MainAxisAlignment.CENTER,  # Allineamento a sinistra (default)
            spacing=10  # Spazio tra gli elementi
        )
        self._page.controls.append(row1)

        # Layout della UI
        self._page.controls.append(ft.Container(content=self.selected_list, alignment=ft.alignment.center))

        self.controller.populate_symptoms()
        self.update_page()"""
