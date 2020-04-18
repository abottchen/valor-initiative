#!/usr/local/bin/python3

import sys
import getopt
import json
import re
import random
from colorcodes import clr


def handleReroll(initOrder, roll, creatureName):
    dictName = str(initOrder[roll])
    # When python prints the dict entries, the color codes are not interpreted, so we scrub them out
    dictName = re.sub(r'\\.*?m', "", dictName)
    print("Rolloff needed between " + creatureName +
          " and " + dictName)
    roll1 = random.randint(1, 10)
    roll2 = random.randint(1, 10)
    while(roll1 == roll2):
        print("They tied again with " +
              str(roll1) + "...  Re-rolling")
        roll1 = random.randint(1, 10)
        roll2 = random.randint(1, 10)
    return dict([(roll1, initOrder[roll]), (roll2, creatureName)])


def printDict(d, indent=''):
    for i in sorted(d.keys(), reverse=True):
        if type(d[i]) is dict:
            print(indent + str(i) + " -> ")
            printDict(d[i], indent + "  ")
        else:
            print(indent + str(i) + " -> " + str(d[i]))


# List comes in as creature,number,bonus,creature,number,bonus,creature,number,bonus...
# -c "Biker:12:0,Carlito:1:0" -p "Adam:4,David:2,Max:10,Simon:6,Steve:5"
def main(argv):
    creatures = ""
    players = ""
    try:
        opts, args = getopt.getopt(argv, "hc:p:", ["creatures=", "players="])
    except getopt.GetoptError:
        print('randomEncounter.py -c <creaturelist> -p <playerlist>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('initiative.py -c <creature:number:bonus,creature:number:bonus,...> -p <playername:number,playername:number,...>')
            sys.exit()
        elif opt in ("-c", "--creatures"):
            creatures = arg
        elif opt in ("-p", "--players"):
            players = arg

    initOrder = {}

    for playerType in players.split(','):
        name, roll = playerType.split(":")
        name = clr.WHITE + name.strip() + clr.ENDC
        roll = int(roll.strip())
        if roll in initOrder.keys():
          initOrder[roll] = handleReroll(initOrder, roll, name)
        else:
          initOrder[roll] = name

    for creatureType in creatures.split(','):
        name, number, bonus = creatureType.split(":")
        name = name.strip()
        number = number.strip()
        bonus = bonus.strip()
        if int(number) > 1:
            localColors = list(clr.COLORS.keys())
        else:
            localColors = ['']
        for _ in range(int(number)):
            c = localColors.pop(0)
            if c == "":
                creatureName = name
            else:
                creatureName = clr.COLORS[c] + c + " " + name + clr.ENDC
            roll = random.randint(1, 10) + int(bonus)
            if roll in initOrder.keys():
                initOrder[roll] = handleReroll(initOrder, roll, creatureName)
            else:
                initOrder[roll] = creatureName

    print("---===== Final Order =====---")
    printDict(initOrder)


if __name__ == "__main__":
    main(sys.argv[1:])
