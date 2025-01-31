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

        # Dropdown per selezione sintomi
        self.dropdown = ft.Dropdown(label="Cerca e seleziona sintomi", on_change=self._controller.add_symptom,
                                    options=[])

        # Lista sintomi selezionati
        self.selected_list = ft.ListView(expand=1, spacing=10, padding=10)

        # Bottone per avviare la diagnosi
        self.btn_diagnose = ft.ElevatedButton(text="Diagnostica", on_click=self._controller.on_diagnose_click)

        # Layout della UI
        self._page.controls.extend([
            ft.Container(content=self._title, alignment=ft.alignment.center),
            ft.Container(content=self.dropdown, alignment=ft.alignment.center),
            ft.Container(content=self.selected_list, alignment=ft.alignment.center),
            ft.Container(content=self.btn_diagnose, alignment=ft.alignment.center),
        ])

        self._controller.populate_symptoms()
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