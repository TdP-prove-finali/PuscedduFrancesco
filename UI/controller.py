import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
    def handle_graph(self,e):
        self._model.creaGrafo()
        self._view.update_page()
    """def fillDD(self):
        for s in self._model.sintomi:
            if r.datetime.year not in self._model.anni:
                self._model.anni.append(r.datetime.year)
            if r.shape not in self._model.forme:
                self._model.forme.append(r.shape)
        self._model.anni.sort()
        for a in self._model.anni:
            self._view.ddyear.options.append(ft.dropdown.Option(a))
        for s in self._model.forme:
            self._view.ddshape.options.append(ft.dropdown.Option(s))"""