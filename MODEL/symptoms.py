from dataclasses import dataclass

@dataclass
class Sintomo:
    symptom:str
    weight:int

    def __repr__(self):
        self.nome = self.symptom.replace("_", " ")
        return self.nome
