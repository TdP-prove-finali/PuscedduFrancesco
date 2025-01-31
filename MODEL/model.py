from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.sintomi = DAO.getAllSymptoms()
        self.malattie = DAO.getAllDiseases()
        self.diagnosi = None
        self.mappaSintomi = {}
        self.mappaMalattiaSintomi = {}
        self.grafo = nx.Graph()
    def creaMappaSintomi(self):
        for s in self.sintomi:
            self.mappaSintomi[s.__repr__()] = s
    def creaMappaMalattiaSintomi(self):
        pass

    def creaGrafo(self):
        print(self.vicini)
        self.archi = DAO.getPesi(anno,giorni)
        print(list(self.archi))
        for s in self.stati:
            self.statiMap[s.id] = s
            self.grafo.add_node(s.id)
        for v in self.vicini:
            self.grafo.add_edge(v[0],v[1])
        for a in self.archi:
            if (a[0].upper(),a[1].upper()) in self.vicini or (a[1].upper(),a[0].upper()) in self.vicini:
                self.grafo[a[0].upper()][a[1].upper()]["weight"] = a[2]
        print(self.grafo.number_of_edges())
        print(self.grafo.number_of_nodes())










