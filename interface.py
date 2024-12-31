import os
import pickle
import random
import time
from force import Force
from state import State
from battle import Battle

class Interface:
    def __init__(self):
        self.date = 1
        self.numberStates = 0
        self.numberForces = 0

    def startSeatings(self):
        forces = []
        states = []
        self.clearScreen()

        print("Za ucitavanje postojece igre pritisni 1\n za novu igru 2")
        m = int(input())
        if m == 1:
            forces, states = self.loadGame()
            state: State = None
            force: Force = None
            force2: Force = None
            for state in states:
                i = 0
                for force in state.forces:
                    for force2 in forces:
                        if(force.name == force2.name):
                            state.forces[i] = force2
                    i+=1
            
            for force in forces:
                for state in states:
                    if force.state.name == state.name:
                        force.state = state
            
                    
            return states, forces

        print("\t Pocetna podesavanja igre ")

        territory = int(input("Unesite broj teritorija u igri: "))

        while territory > 0:
            self.clearScreen()
            print(f"Preostalo je {territory} teritorija na mapi: ")
            x = 0
            while territory - x < 0 or x <= 0:
                x = int(input("Unesite broj teritorija nove drzave: "))
            territory = territory - x
            tmpName = input("Unesite ime nove drzave: ")
            tmpBudget = int(input("Unesite pocetni budzet drzave: "))
            tmpState = State(tmpName, x, tmpBudget)
            states.append(tmpState)
            self.numberStates += 1
        
        self.clearScreen()
        self.logo()
        return states, forces

    def printMenu(self):
        print("\t ")
        print("\t\t Main Menu")
        print("1. Spisak drzava")
        print("2. Spisak jedinica")
        print("3. Kombinovani spisak")
        print("4. Bitka")
        print("5. Sledeci potez")
        print("6. Upravljaj drzavom")
        print("7. Upravljaj jedinicom")
        print("8. Kraj")

    def logo(self):
            self.clearScreen()
            print(r"""
                                           /$$   /$$                     /$$              
                                          | $$$ | $$                    |__/              
                                  /$$$$$$ | $$$$| $$  /$$$$$$   /$$$$$$$ /$$ /$$  /$$$$$$ 
                                 /$$__  $$| $$ $$ $$ |____  $$ /$$_____/| $$|__/ /$$__  $$
                                | $$$$$$$$| $$  $$$$  /$$$$$$$| $$      | $$ /$$| $$$$$$$$
                                | $$_____/| $$\  $$$ /$$__  $$| $$      | $$| $$| $$_____/
                                |  $$$$$$$| $$ \  $$|  $$$$$$$|  $$$$$$$| $$| $$|  $$$$$$$
                                 \_______/|__/  \__/ \_______/ \_______/|__/| $$ \_______/
                                                                       /$$  | $$          
                                                                      |  $$$$$$/          
                                                                       \______/   
    """)
            print("\n\n")
            print(f"Datum: {random.randint(1,28)}/{(self.date % 12)+1}/{(self.date - (self.date % 12))/12 + 1980}  Broj drzava: {self.numberStates}   Broj jedinica: {self.numberForces}\n\n")

    def clearScreen(self):
        os.system('clear')

    def stateList(self, states: State):
        print("\t\t\t Spisak drzava \n\n")
        print("Br.  |   Drzava   | Teritorije |   Budzet   | Broj jedinica |")
        i = 1
        for x in states:
            print(f"{i}.   |{x}")
            i+=1
        input()

    def forceList(self, forces):
        self.logo()
        print("\t\t\tSpisak jedinica")
        print("=" * 120)
        print(
            f"{'Br.':<4} | {'Jedinica':<12} | {'Drzava':<10} | {'Tenkova':<8} | {'Oklopnih':<10} | "
            f"{'Artiljerija':<12} | {'PVO':<6} | {'Avioni':<8} | {'Helikopteri':<12} |"
        )
        print("=" * 120)

        for i, force in enumerate(forces, start=1):
            print(
                f"{i:<4} | {force}"
            )

        print("=" * 120)
        input()

    def nextTurn(self, states: State, forces):
        self.date += 1
        state: State = None
        for state in states:
            state.budget += state.territory * 30
        
            self.saveGame(forces, states)
            self.sortForces(forces)
            self.sortStates(states)

    def stateMenu(self, state: State):
        self.logo()
        print(f"Drzava: {state.name}    Budzet: {state.budget}    Teritorija: {state.territory} \n\n")
        print("\t Meni")
        print("1. Edituj ime")
        print("2. Odvoji novu drzavu")
        print("3. Kreiraj novu jedinicu")
        print("4. Doniraj novac drugoj drzavi")
        print("5. doniraj teritorije drugoj drzavi")
        print("6. Izlaz")

    def countrySeatings(self, states: State, forces: Force):
        self.logo()
        status = False
        currentState: State = None
        while not status:
            stateName = input("Unesite ime drzave kojoj pristupate: ")
            for state in states:
                if state.name == stateName:
                    currentState = state
                    status = True
                    break
            if not status:
                print("Drzava sa daatim imenom ne postoji ponovite unos") 

        self.logo()
        select = 0
        while select != 6:
            self.stateMenu(currentState)
            try:
                select = int(input())
            except:
                select = 0

            if select == 1:
                currentState.changeName()
            elif select == 2:
                states.append(currentState.splitState())
                self.numberStates += 1
            elif select == 3:
                currentState.createForce(forces)
                self.numberForces += 1
            elif select == 4:
                currentState.donateMoney(states)
            elif select == 5:
                currentState.donateTerritory(states)
            else:
                pass
        
    def forceMenu(self):
        print("1. Kupovina naoruzanja")
        print("2. Doniranje naoruzanja")
        print("3. Promjeni ime")
        print("4. podijeli jedinicu")
        print("5. Obrisi jedinicu")
        print("6. Promjeni vlasnika")
        print("7. Izlaz")

    def buyingWeapons(self, force: Force):
        print("Unesite tip naoruzanja")
        print("\t-tank")
        print("\t-artillery")
        print("\t-armored")
        print("\t-pvo")
        print("\t-aircraft")
        print("\t-helicopter")
        type = input()
        amount = int(input("Unesite kolicinu naoruzanja: "))
        force.buy(type, amount)

    def delateForce(self, force: Force, forces):
        tmp = True
        for type, value in force.units.items():
            if value != 0:
                tmp = False
                break
        
        if tmp:
            force.state.forces.remove(force)
            forces.remove(force)
            print("Jedinica uspjesno obrisana")
            return
        
        print("Jedinica nije obrisana")
        time.sleep(2)

    def sortForces(self, forces):
        force: Force = None

        for force in forces:
            force.calculateStrength()

        forces.sort(key=lambda force: force.strength, reverse = True)

    def sortStates(self, states):
        state: State = None

        for state in states:
            state.calculateStrength()

        states.sort(key=lambda state: state.strength, reverse = True)

    def forceSeatings(self, forces, states):
        forceName = "none"
        currentForce: Force = None
        select = -1
        while select == -1:
            forceName = input("Unesite ime jedinice kojoj pristupate ")
            for force in forces:
                if force.name == forceName:
                    currentForce = force
                    select = 0
                    break
            if select != 0:
                print("Pogresan unos!!!")
            

        while select != 7:
            self.logo()
            currentForce.printInfo()
            self.forceMenu()
            try:
                select = int(input())
            except:
                select = 0

            if select == 1:
                self.buyingWeapons(currentForce)
            elif select == 2:
                currentForce.donate(forces)
            elif select == 3:
                currentForce.changeName()
            elif select == 4:
                forces.append(currentForce.split())
                self.numberForces += 1
            elif select == 5:
                self.delateForce(currentForce, forces)
            elif select == 6:
                currentForce.changeState(states)
    
    def saveGame(self, forces, states):
        with open("data/forces.pkl", "wb") as file:
            pickle.dump(forces, file)
        with open("data/states.pkl", "wb") as file:
            pickle.dump(states, file)
        with open("data/game.pkl", "wb") as file:
            pickle.dump(self, file)
            
    def loadGame(self):
        forces = []
        states = []

        with open("data/forces.pkl", "rb") as file:
            forces = pickle.load(file)
        with open("data/states.pkl", "rb") as file:
            states = pickle.load(file)
        with open("data/game.pkl", "rb") as file:
            tmp: Interface = pickle.load(file)

        self.date = tmp.date
        self.numberForces = tmp.numberForces
        self.numberStates = tmp.numberStates

        return forces, states

    def battle(self, states):
        self.logo()
        battle1 = Battle()
        battle1.startBattle(states)
        self.logo()
        battle1.caclulatingStatistics()
interface = Interface()
        
    
