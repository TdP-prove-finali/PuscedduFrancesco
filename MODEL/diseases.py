from dataclasses import dataclass

@dataclass
class Malattia:
    Disease:str
    Description:str
    step1:str
    step2:str
    step3:str
    step4:str

    def listaPrecauzioni(self):
        return [self.step1,self.step2,self.step3,self.step4]


