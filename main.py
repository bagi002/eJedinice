from interface import interface

states, forces = interface.startSeatings()

while(1):
    interface.logo()
    interface.printMenu()
    try:
        x = int(input())
    except:
        x = 0
    interface.logo()
    if x == 8:
        interface.clearScreen()
        interface.saveGame(forces,  states)
        break
    elif x == 1:
        interface.stateList(states)
    elif x == 2:
        interface.forceList(forces)
    elif x == 3:
        pass
    elif x == 4:
        interface.battle(states)
    elif x == 5:
        interface.nextTurn(states, forces)
        pass
    elif x == 6:
        interface.countrySeatings(states, forces)
    elif x == 7:
        interface.forceSeatings(forces, states)
        
