from state import State
from force import Force
from units import unitsInfo
import random
import copy
import time

class Battle:
    def __init__(self):
        self.stateA: State = None
        self.stateB: State = None

        self.forcesA = []
        self.forcesB = []

        self.scoreAirA = 0
        self.scoreAirB = 0
        self.scoreGroundA = 0
        self.scoreGroundB = 0

        self.teamA = [5, 2, 3]
        self.teamB = [5, 2, 3]

    def selectState(self, states):
        name = ""
        state: State = None
        while state is None:
            name = input("Unesite ime drzave A: ")
            for state in states:
                if state.name == name:
                    break
            if state is None:
                print("Molimo vas ponovite unos")
        self.stateA = state

        state: State = None
        while state is None:
            name = input("Unesite ime drzave B: ")
            for state in states:
                if state.name == name:
                    break
            if state is None:
                print("Molimo vas ponovite unos")
        self.stateB = state

        print("Uspjesno ste izabrali zaracene strane, slijedi izbor jedinica")

    def selectForces(self):
        print(f"Odaberite jedinice koje drzava {self.stateA.name} poziva u borbu")
        print("Ako zelite dodati jedinicu otkucajte yes, u suprotnom mozete pritisnuti enter")
        for force in self.stateA.forces:
            if input(f"{force.name} - ") == "yes":
                self.forcesA.append(force)
        
        print(f"Odaberite jedinice koje drzava {self.stateB.name} poziva u borbu")
        print("Ako zelite dodati jedinicu otkucajte yes, u suprotnom mozete pritisnuti enter")
        for force in self.stateB.forces:
            if input(f"{force.name} - ") == "yes":
                self.forcesB.append(force)

        print("Jedinice za borbu su uspjesno dodate")

    def calculateScores(self):
        force: Force = None
        for force in self.forcesA:
            for type in force.units:
                self.scoreAirA += force.units[type] * unitsInfo[type].air_attack
                self.scoreAirB -= force.units[type] * unitsInfo[type].air_defense
                self.scoreGroundA += force.units[type] * unitsInfo[type].ground_attack
                self.scoreGroundB -= force.units[type] * unitsInfo[type].ground_defense

        force: Force = None
        for force in self.forcesB:
            for type in force.units:
                self.scoreAirB += force.units[type] * unitsInfo[type].air_attack
                self.scoreAirA -= force.units[type] * unitsInfo[type].air_defense
                self.scoreGroundB += force.units[type] * unitsInfo[type].ground_attack
                self.scoreGroundA -= force.units[type] * unitsInfo[type].ground_defense

        if self.scoreAirA < 0 and self.scoreAirB < 0:
                b = -self.scoreAirB - self.scoreAirA
                self.scoreAirB = -self.scoreAirB / b * 100
                self.scoreAirA = -self.scoreAirA / b * 100
        else:
            if self.scoreAirA < 0:
                self.scoreAirA = 0
            if self.scoreAirB < 0:
                self.scoreAirB = 0

        if self.scoreGroundA < 0 and self.scoreGroundB < 0:
                b = -self.scoreGroundB - self.scoreGroundA
                self.scoreGroundB = -self.scoreGroundB / b * 100
                self.scoreGroundA = -self.scoreGroundA / b * 100
        else:
            if self.scoreGroundA < 0:
                self.scoreGroundA = 0
            if self.scoreGroundB < 0:
                self.scoreGroundB = 0


        print(" Statistika bitke\n")
        print("\t Vazdusna bitka: ")
        print(f"\t\t {self.stateA.name} -> Ukupni skor: {self.scoreAirA} postotak: {self.scoreAirA / (self.scoreAirA + self.scoreAirB) * 100} %")
        print(f"\t\t {self.stateB.name} -> Ukupni skor: {self.scoreAirB} postotak: {self.scoreAirB / (self.scoreAirA + self.scoreAirB) * 100} %")
        self.teamA[1] = 2 * self.scoreAirA / (self.scoreAirA + self.scoreAirB)
        self.teamB[1] = 2 * self.scoreAirB / (self.scoreAirA + self.scoreAirB)
        if self.teamA[1] > self.teamB[1]:
            print(f"U vazdusnoj bitci pobjedila je {self.stateA.name} sa osvojenih {self.teamA[1]} bodova")
        else:
            print(f"U vazdusnoj bitci pobjedila je {self.stateB.name} sa osvojenih {self.teamB[1]} bodova")

        print("\n\n\t Kopnena bitka: ")
        print(f"\t\t {self.stateA.name} -> Ukupni skor: {self.scoreGroundA} postotak: {self.scoreGroundA / (self.scoreGroundA + self.scoreGroundB) * 100} %")
        print(f"\t\t {self.stateB.name} -> Ukupni skor: {self.scoreGroundB} postotak: {self.scoreGroundB / (self.scoreGroundA + self.scoreGroundB) * 100} %")

        self.teamA[2] = 3 * self.scoreGroundA / (self.scoreGroundA + self.scoreGroundB)
        self.teamB[2] = 3 * self.scoreGroundB / (self.scoreGroundA + self.scoreGroundB)
        if self.teamA[2] > self.teamB[2]:
            print(f"U kopnenoj bitci pobjedila je {self.stateA.name} sa osvojenih {self.teamA[2]} bodova")
        else:
            print(f"U kopnenoj bitci pobjedila je {self.stateB.name} sa osvojenih {self.teamB[2]} bodova")

        self.teamA[0] = self.teamA[1] + self.teamA[2]
        self.teamB[0] = self.teamB[1] + self.teamB[2]

    def calculateEquipmentLosses(self):
        print("\n\n")
        copyForcesA = copy.deepcopy(self.forcesA)
        copyForcesB = copy.deepcopy(self.forcesB)

        scoreAirA = self.scoreAirA
        scoreAirB = self.scoreAirB
        scoreGroundA = self.scoreGroundA
        scoreGroundB = self.scoreGroundB

        force: Force = None
        m = 0
        while scoreAirA > 900 and m < 150:
            for force in self.forcesB:
                for x in force.units:
                    if force.units[x] == 0 and unitsInfo[x].type == "air":
                        m += 1
                    else:
                        if unitsInfo[x].type == "air" and unitsInfo[x].health < scoreAirA:
                            m = 0
                    if unitsInfo[x].type == "air" and unitsInfo[x].health < scoreAirA and force.units[x] > 0:
                        if random.randint(0, 10) > 5:
                            m = 0
                            force.units[x] -= 1
                            scoreAirA -= unitsInfo[x].health
        m = 0
        while scoreAirB > 900 and m < 150:
            for force in self.forcesA:
                for x in force.units:
                    if force.units[x] == 0 and unitsInfo[x].type == "air":
                        m += 1
                    else:
                        if unitsInfo[x].type == "air" and unitsInfo[x].health < scoreAirB:
                            m = 0
                    if unitsInfo[x].type == "air" and unitsInfo[x].health < scoreAirB and force.units[x] > 0:
                        if random.randint(0, 10) > 5:
                            m = 0
                            force.units[x] -= 1
                            scoreAirB -= unitsInfo[x].health  
        m = 0
        while scoreGroundA > 400 and m < 150:
            for force in self.forcesB:
                for x in force.units:
                    if force.units[x] == 0 and unitsInfo[x].type == "gnd":
                        m += 1
                    else:
                        if unitsInfo[x].type == "gnd" and unitsInfo[x].health < scoreGroundA:
                            m = 0
                    if unitsInfo[x].type == "gnd" and unitsInfo[x].health < scoreGroundA and force.units[x] > 0:
                        if random.randint(0, 10) > 5:
                            m = 0
                            force.units[x] -= 1
                            scoreGroundA -= unitsInfo[x].health 
        m = 0
        while scoreGroundB > 400 and m < 150:
            for force in self.forcesA:
                for x in force.units:
                    if force.units[x] == 0 and unitsInfo[x].type == "gnd":
                        m += 1
                    else:
                        if unitsInfo[x].type == "gnd" and unitsInfo[x].health < scoreGroundB:
                            m = 0
                    if unitsInfo[x].type == "gnd" and unitsInfo[x].health < scoreGroundB and force.units[x] > 0:
                        if random.randint(0, 10) > 5:
                            m = 0
                            force.units[x] -= 1
                            scoreGroundB -= unitsInfo[x].health 

        for force, forceCop in zip(self.forcesA, copyForcesA):
            for type in force.units:
                forceCop.units[type] -= force.units[type]

        for force, forceCop in zip(self.forcesB, copyForcesB):
            for type in force.units:
                forceCop.units[type] -= force.units[type]
        

        print("\t\t\tSpisak gubitaka jedinica")
        print("=" * 120)
        print(
            f"{'Br.':<4} | {'Jedinica':<12} | {'Drzava':<10} | {'Tenkova':<8} | {'Oklopnih':<10} | "
            f"{'Artiljerija':<12} | {'PVO':<6} | {'Avioni':<8} | {'Helikopteri':<12} |"
        )
        print("=" * 120)

        for i, force in enumerate(copyForcesA, start=1):
            print(
                f"{i:<4} | {force}"
            )
        for i, force in enumerate(copyForcesB, start=1):
            print(
                f"{i:<4} | {force}"
            )

        print("=" * 120)

    def calculateTerritory(self):

        if self.teamA[0] > self.teamB[0]:
            print(f"U bitci je pobjedila {self.stateA.name} sa osvojenih {self.teamA[0]} bodova")
            a = self.teamA[0] - 2.5
            b = int(a*20)
            if b > self.stateB.territory:
                b = self.stateB.territory
            self.stateB.territory -= b
            self.stateA.territory += b
            print(f"Drzava {self.stateA.name} osvojila je {b} teritorija")
        else:
            print(f"U bitci je pobjedila {self.stateB.name} sa osvojenih {self.teamB[0]} bodova")
            a = self.teamB[0] - 2.5
            b = int(a*20)
            if b > self.stateA.territory:
                b = self.stateA.territory
            self.stateA.territory -= b
            self.stateB.territory += b
            print(f"Drzava {self.stateB.name} osvojila je {b} teritorija")

        

    def startBattle(self, states):
        self.selectState(states)
        self.selectForces()
        
    def caclulatingStatistics(self):
        self.calculateScores()
        self.calculateEquipmentLosses()
        self.calculateTerritory()
        input()
        

