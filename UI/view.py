import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Diagnostica Medica"
        self._page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self._page.theme_mode = ft.ThemeMode.LIGHT

        self._controller = None
        self.selected_list = None
        self.btn_diagnose = None
        self.dropdown = None

    def load_interface(self):
        """Carica l'interfaccia grafica"""
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
            nome = s.__repr__()
            self.dropdown.options.append(ft.dropdown.Option(text=nome, key=s))
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