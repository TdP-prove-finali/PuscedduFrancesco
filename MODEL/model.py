from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.sintomi = DAO.getAllSymptoms()
        self.grafo = nx.Graph()
    def creaGrafo(self):
        pass





