from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.sintomi = DAO.getAllSymptoms()
        self.malattie = DAO.getAllDiseases()
        self.diagnosi = None
        self.archi = None
        self.mappaSintomi = {}
        self.mappaMalattie = {}
        self.mappaMalattiaSintomi = {}
        self.grafo = nx.Graph()
    def creaMappaSintomi(self):
        for s in self.sintomi:
            self.mappaSintomi[s.__repr__()] = s
    def creaMappaMalattie(self):
        for m in self.malattie:
            self.mappaMalattie[m.Disease] = m

    def creaMappaMalattiaSintomi(self):
        pass

    def creaNodi(self):
        for m in self.malattie:
            self.grafo.add_node(m.Disease)

    def aggiornaArchi(self,sintomoStr):
        peso = self.mappaSintomi[sintomoStr].weight
        sintomo = self.mappaSintomi[sintomoStr].symptom
        self.archi = DAO.getEdges(sintomo)
        print(self.archi[0])
        if len(self.archi) == 1:
            self.diagnosi = self.archi[0][0]
            self.prognosi = self.mappaMalattie[self.diagnosi]
            print(self.diagnosi)
            print(self.prognosi)
            return self.prognosi
        for a in self.archi:
            self.grafo.add_edge(a[0],a[1])
            self.grafo[a[0]][a[1]]["weight"] = self.grafo[a[0]][a[1]].get("weight", 0) + peso
        print(self.grafo.number_of_edges())
        print(self.grafo.number_of_nodes())
        return None

    def diagnosis(self,malattia):
        pass












