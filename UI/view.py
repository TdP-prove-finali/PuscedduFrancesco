import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Interazioni Social"
        self._page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self.image_display = ft.Image()
        self._controller = None

        self.selected_list = None
        self.btn_analyze = None
        self.ddGender = None
        self.ddScreenTime = None
        self.ddPlatform = None
        self.ddIsolationLevel = None
        self.ddAdInteraction = None
        self.ddSleepQuality = None
        self.result_list = None
        self.lookFor = None

    def load_interface(self):
        self._title = ft.Text("Social Entertainment", color="blue", size=24)
        self._page.controls.append(ft.Container(content=self._title, alignment=ft.alignment.center))


        # Dropdown per i filtri
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
        self.ddScreenTime = ft.Dropdown(
            label="Tempo giornaliero allo schermo",
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
            value="",
            #on_change= self.change_btn,
            options=[
                ft.dropdown.Option("", "Non specificata"),
                ft.dropdown.Option("TikTok"),
                ft.dropdown.Option("YouTube"),
                ft.dropdown.Option("Instagram"),
                ft.dropdown.Option("Facebook"),
                ft.dropdown.Option("Twitter")
            ]
        )
        self.ddIsolationLevel = ft.Dropdown(
            label="Livello isolamento sociale",
            value=None,
            options=[ft.dropdown.Option(None, "Non specificato")] + [ft.dropdown.Option(str(i)) for i in range(1, 11)]
        )
        self.ddSleepQuality = ft.Dropdown(
            label="Qualità del sonno",
            value=None,
            options=[ft.dropdown.Option(None, "Non specificata")] + [ft.dropdown.Option(str(i)) for i in range(1, 11)]

        )
        self.ddAdInteraction = ft.Dropdown(
            label="Interazione con gli annunci",
            value=None,
            options=[
                ft.dropdown.Option(None, "Non specificata"),
                ft.dropdown.Option("Low", "Bassa"),
                ft.dropdown.Option("Medium", "Media"),
                ft.dropdown.Option("High", "Alta")
            ]
        )

        # Prima riga del layout dopo il titolo
        row1 = ft.Row(
            [self.ddGender, self.ddPlatform,self.ddSleepQuality],  # Aggiungiamo gli elementi
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10  # Spazio tra gli elementi
        )
        self._page.controls.append(row1)

        # Seconda riga del layout
        row2 = ft.Row(
            [self.ddScreenTime, self.ddAdInteraction, self.ddIsolationLevel], # self.ddIsolationLevel
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
        self._page.controls.append(row2)

        # Pulsante per eseguire l'analisi
        self.btn_analyze = ft.ElevatedButton(
            text="Analizza dati", on_click=self.controller.analyze_click, color="green"
        )

        # Pulsante per eseguire cancellare la view
        self.btn_delete = ft.ElevatedButton(
            text="Cancella lista", on_click=self.controller.delete_click, color="red"
        )

        # Pulsante per resettare gli utenti
        self.btn_reset = ft.ElevatedButton(
            text="Resetta filtri", on_click=self.controller.reset_click, color="blue"
        )

        # Pulsante per iniziare la ricorsione
        self.btn_lookFor = ft.ElevatedButton(
            text="Crea grafo e cerca Tester", on_click=self.controller.trovaTester, color="orange"
        )


        # Terza riga (riga dei bottoni)
        row3 = ft.Row(
            [self.btn_analyze, self.btn_reset, self.btn_delete, self.btn_lookFor],  # self.ddIsolationLevel
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
        self._page.controls.append(row3)

        # bottoni per le analisi e i grafici
        self.btn_BenDig = ft.ElevatedButton(
            text="Benessere Digitale", on_click=self.controller.benessereDigitale_click
        )
        self.btn_FatDig = ft.ElevatedButton(
            text="Fatica Digitale", on_click=self.controller.faticaDigitale_click
        )
        self.btn_SpesaIntr = ft.ElevatedButton(
            text="Spesa Intrattenimento", on_click=self.controller.spesaIntrattenimento_click
        )
        self.btn_ExpAds = ft.ElevatedButton(
            text="Esposizione agli ads", on_click=self.controller.esposizioneAds_click
        )
        # Quarta riga (seconda riga dei bottoni)
        row4 = ft.Row(
            [self.btn_BenDig, self.btn_FatDig, self.btn_SpesaIntr,self.btn_ExpAds],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )

        self._page.controls.append(row4)


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

    def change_btn(self,e):
        selected_platform = self.ddPlatform.value

        # Se selezioni "Non specificata", lascia il testo base e disabilita il pulsante
        if selected_platform is None:
            self.btn_lookFor.text = "Cerca Tester"
            self.btn_lookFor.disabled = True
        else:
            self.btn_lookFor.text = f"Cerca Tester per {selected_platform}"
            self.btn_lookFor.disabled = False

        self.update_page()  # Aggiorna la UI"""


    """def update_chart(self, e):
        activity = e.control.data
        img_data = self.controller.generate_chart(activity)
        self._page.controls.append(ft.Container(content=self.image_display, alignment=ft.alignment.center))
        self.image_display.src_base64 = img_data
        self.update_page()"""

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

