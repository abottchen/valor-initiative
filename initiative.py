#!/usr/local/bin/python3

import sys
import getopt
import re
import random
from colorcodes import clr


def handleReroll(initOrder):
    # initorder will be a hash of arrays
    # 1 => [adam,simon,bob]
    # 2 => [steve]
    # ...
    # if a hash key is a list of more than one thing
    #  it becomes a hash of arrays for rerolls for each thing in the list
    #
    #  1 => {2 => [adam, bob], 5 => [simon]}
    #  recurse until there are no lists of more than one person
    # else:
    #    the value sticks
    for roll in initOrder.keys():
        if len(initOrder[roll]) > 1:
            print("Rerolling for ties on " + str(roll) + " by ", end='')
            newRolls = {}
            for name, bonus in initOrder[roll]:
                print(name + ", ", end='')
                newRoll = random.randint(1, 10) + bonus
                addCreatureRoll(newRolls, newRoll, [name, bonus])
            handleReroll(newRolls)
            initOrder[roll] = newRolls
            print("")


def printResult(d):
    for i in sorted(d.keys(), reverse=True):
        if type(d[i]) is dict:
            printResult(d[i])
        else:
            print(d[i][0][0] + ",", end='')


def prettyPrintResult(d, indent=''):
    for i in sorted(d.keys(), reverse=True):
        if type(d[i]) is dict:
            print(indent + str(i) + " -> ")
            prettyPrintResult(d[i], indent + "  ")
        else:
            print(indent + str(i) + " -> " + d[i][0][0])


def addCreatureRoll(d, r, c):
    if r in d.keys():
        d[r].append(c)
    else:
        d[r] = [c]


def parseCreature(creatureStr):
    try:
        name, roll, bonus = creatureStr.split(":")
    except ValueError:
        try:
            name, roll = creatureStr.split(":")
            bonus = "0"
        except Exception as e:
            print("Error processing player string: '" + creatureStr + "'")
            print(e)
            sys.exit(1)
    return(name.strip(), int(roll.strip()), int(bonus.strip()))


def main(argv):
    creatures = ""
    players = ""
    try:
        opts, _ = getopt.getopt(argv, "hc:p:", ["creatures=", "players="])
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

    # List comes in as creature,number,bonus,creature,number,bonus,creature,number,bonus...
    # -c "Biker:12:0,Carlito:1:0" -p "Adam:4,David:2,Max:10,Simon:6,Steve:5"

    if players != "":
        for player in players.split(','):
            name, roll, bonus = parseCreature(player)
            name = clr.WHITE + name + clr.ENDC
            addCreatureRoll(initOrder, roll, [name, bonus])

    if creatures != "":
        for creature in creatures.split(','):
            name, number, bonus = parseCreature(creature)
            if number > 1:
                localColors = list(clr.COLORS.keys())
            else:
                localColors = ['']
            for _ in range(number):
                c = localColors.pop(0)
                if c == "":
                    creatureName = name
                else:
                    creatureName = clr.COLORS[c] + c + " " + name + clr.ENDC
                roll = random.randint(1, 10) + bonus
                addCreatureRoll(initOrder, roll, [creatureName, bonus])

    handleReroll(initOrder)
    print("---===== Final Order =====---")
    prettyPrintResult(initOrder)
    printResult(initOrder)
    print("")


if __name__ == "__main__":
    main(sys.argv[1:])
