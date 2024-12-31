from __future__ import annotations
import time

class State:
    def __init__(self, name, territory, budget: int):
        self.name = name
        self.territory= territory
        self.budget = budget
        self.numForces = 0
        self.forces = []
        self.strength = 0

    def __str__(self):
        return f" {self.name:10} | {self.territory:10} | {self.budget:10} | {self.numForces:13} |"

    def createForce(self, allForces):
        from force import Force
        if self.budget > 5000:
            print("Za kreiranje jedinice potrebno je 5000$")
            tmp = ""
            while tmp != "Yes" and tmp != "No":
                print("Ako zelite da nstavite unesite Yes, za prekid No")
                tmp = input()

            if tmp == "Yes":
                self.budget -= 5000
                name = input("Unesite ime jedinice: ")
                force = Force(name, self)
                self.forces.append(force)
                allForces.append(force)
            else:
                pass

        else:
            print("Za kreiranje jedinice potrebno je 5000$")
    
    def changeName(self):
        novo = input("Unesite novo ime: ")
        self.name = novo
        print("Promjena imena je uspjesno obavljena")
        time.sleep(2)

    def splitState(self):
        name = input("Unesite ime nove drzave: ")
        while(1):
            num = int(input("Unesite broj teritorija nove drzave: "))
            if(num <= self.territory):
                break
            print("Morate unjeti broj teritorija mnji od broja teritorija maticne drzave")
        
        newState = State(name, num, int(self.budget*(num/self.territory)))
        self.budget = self.budget - int(self.budget*(num/self.territory))
        self.territory -= num
        return newState

    def calculateStrength(self):
        self.strength = 0
        from force import Force
        force : Force = None
        for force in self.forces:
            self.strength += force.strength
        
        self.strength += self.budget / 5
        self.strength += self.territory * 10

    def donateMoney(self, states):
        name = ""
        newState: State = None

        while(newState is None):
            name = input("Unesite ime drzave kojoj donirate novac: ")
            for state in states:
                if state.name == name:
                    newState = state
                    break
        
            amount = int(input("Unesite kolicinu novca koju donirate: "))
            if amount > self.budget: 
                print("Nemate dovoljno novca za ovu radnju!!")
                return
            
            newState.budget += amount
            self.budget -= amount


    def donateTerritory(self, states):
        name = ""
        newState: State = None

        while(newState is None):
            name = input("Unesite ime drzave kojoj donirate teritorije: ")
            for state in states:
                if state.name == name:
                    newState = state
                    break
        
            amount = int(input("Unesite broj teritorija koje donirate: "))
            if amount > self.budget: 
                print("Nemate dovoljno teritorije za ovu radnju!!")
                return
            
            newState.territory += amount
            self.territory -= amount