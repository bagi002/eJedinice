from units import tanks, armored, artillery, pvo, aircraft, helicopter, prices, unitsInfo
from state import State
import time

class Force:
    def __init__(self, name, state: State):
        self.name = name
        self.state = state
        self.units = {
            "tank": 0,
            "artillery": 0,
            "armored": 0,
            "pvo": 0,
            "aircraft": 0,
            "helicopter": 0
        }
        self.strength = 0
        
    def __str__(self):
        # Formatiranje svakog reda za jedinicu
        return (
            f"{self.name:12} | "
            f"{self.state.name:10} | "
            f"{self.units['tank']:8} | "
            f"{self.units['armored']:10} | "
            f"{self.units['artillery']:12} | "
            f"{self.units['pvo']:6} | "
            f"{self.units['aircraft']:8} | "
            f"{self.units['helicopter']:12} |"
        )

    def printInfo(self):
        print(f"Jedinica: {self.name} | Drzava: {self.state.name} | Budzet: {self.state.budget}")
        print(f"Tenkovi: {self.units["tank"]} | Artiljerija: {self.units["artillery"]} | BOV: {self.units["armored"]} | PVO: {self.units["pvo"]} | Avioni: {self.units["aircraft"]} | Helikopteri: {self.units["helicopter"]}")
    
    def calculateStrength(self):
        self.strength = 0
        for type in self.units:
            self.strength += self.units[type] * unitsInfo[type].strength
    
    def buy(self, type, quantity):
        if type in self.units:
            if self.state.budget > prices[type] * quantity:
                self.state.budget -= prices[type] * quantity
                self.units[type] += quantity
            else:
                print("Nemate dovoljno novca za kupovinu")
        else:
            print("Ne definisani tip naoruzanja")
    
    def changeState(self, states):
        name = ""
        newState: State = None

        while(newState is None):
            name = input("Unesite ime drzave koja treba postati vlasnik jedinice: ")
            for state in states:
                if state.name == name:
                    newState = state
                    break

        newState.forces.append(self)
        self.state.forces.remove(self)
        self.state = newState

    def split(self):
        name = input("Unesite ime nove jedinice: ")
        force = Force(name, self.state)
        tmp = int(input("Unesite procenat naoruzanja od 1 do 100 koji dobija nova jedinica"))
        
        for type, value in self.units.items():
            force.units[type] = int(value * (tmp / 100))
            self.units[type] -= int(value * (tmp / 100))
        self.state.forces.append(force)

        return force

    def donate(self, forces):
        force: Force = None
        type = ""
        amount = 0
        while(not amount):
            forceName = input("Unesite ime jedinice kojoj donirate naoruzanje: ")
            for force in forces:
                if force.name == forceName:
                    while(1):
                        print("Unesite tip naoruzanja")
                        print("\t-tank")
                        print("\t-artillery")
                        print("\t-armored")
                        print("\t-pvo")
                        print("\t-aircraft")
                        print("\t-helicopter")
                        type = input()
                        amount = int(input("Unesite kolicinu naoruzanja koju donirate: "))
                        if type in self.units:
                            if amount <= self.units[type]:
                                self.units[type] -= amount
                                force.acceptDonation(type, amount)
                                break
                        print("Pogresan tip ili kolicina")
                    


    def acceptDonation(self, type, amount):
        self.units[type] += amount

    def changeName(self):
        novo = input("Unesite novo ime: ")
        self.name = novo
        print("Promjena imena je uspjesno obavljena")
        time.sleep(2)


