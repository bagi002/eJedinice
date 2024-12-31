class Unit:
    def __init__(self,type, name, price, ground_attack, ground_defense, air_attack, air_defense, health):
        self.name = name
        self.price = price
        self.ground_attack = ground_attack
        self.ground_defense = ground_defense
        self.air_attack = air_attack
        self.air_defense = air_defense
        self.health = health
        self.type = type
        self.strength = (ground_attack + ground_defense + air_attack + air_defense) / 10

    def __str__(self):
        return f"{self.name} - Price: {self.price}, Ground Attack: {self.ground_attack}, Ground Defense: {self.ground_defense}, Air Attack: {self.air_attack}, Air Defense: {self.air_defense}"

tanks = Unit(
    type= "gnd",
    name="Tank",
    price=600,
    ground_attack=90,
    ground_defense=70,
    air_attack=0,
    air_defense=0,
    health= 800
)

artillery = Unit(
    type = "gnd",
    name="Artillery",
    price=300,
    ground_attack=120,
    ground_defense=20,
    air_attack=0,
    air_defense=0,
    health= 350
)

armored = Unit(
    type = "gnd",
    name="Armored Vehicle",
    price=350,
    ground_attack=35,
    ground_defense=50,
    air_attack=0,
    air_defense=0,
    health= 550
)

pvo = Unit(
    type = "gnd",
    name="PVO (Anti-Air)",
    price=700,
    ground_attack=0,
    ground_defense=0,
    air_attack=0,
    air_defense=140,
    health= 450
)

aircraft = Unit(
    type = "air",
    name="Aircraft",
    price=1800,
    ground_attack=45,
    ground_defense=10,
    air_attack=120,
    air_defense=60,
    health= 1250
)

helicopter = Unit(
    type = "air",
    name="Helicopter",
    price=850,
    ground_attack=55,
    ground_defense=15,
    air_attack=35,
    air_defense=0,
    health= 850
)

unitsInfo ={
    "tank": tanks,
    "artillery": artillery,
    "armored": armored,
    "pvo": pvo,
    "aircraft": aircraft,
    "helicopter": helicopter
}

prices = {
    "tank": 500,
    "artillery": 300,
    "armored": 400,
    "pvo": 1250,
    "aircraft": 1800,
    "helicopter": 850
}

