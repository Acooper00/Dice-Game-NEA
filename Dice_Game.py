# Aaron Cooper
# Programming Project June 2019
# Task 2 - Dice Game

#! /usr/bin/python3

import random
from random import *
import csv
from csv import *

Authorised_Players = []# Setting variables
Players = ["",""]
Scores = [0,0]
Banned_Chars = [",","\t","\n",";","\"","\'"," ","\\"]
Collumn_Width = 50
Table_Chars = ["¦","-"]
csv_delimiter = ":"
for i in Table_Chars:
    if i not in Banned_Chars:
        Banned_Chars.append(i)
Banned_Chars.append(csv_delimiter)

Settings = {}
Settings_Options = {"SIDES":range(0,256),"EXTRA_SIDES":range(0,256),"ODD":range(-255,256),"EVEN":range(-255,256),"MULTIPLIER":range(-255,256),"EXTRA_MULTIPLIER":range(-255,256),"ROUNDS":range(1,100),"TYPE_SPEED":[0,1,2,3,4,5]}
Game_Settings = ["SIDES","EXTRA_SIDES","ODD","EVEN","MULTIPLIER","EXTRA_MULTIPLIER","ROUNDS"]

try:
    import time
    from time import *
    time_ = True
except ImportError:
    time_ = False

def Display(string=""):# Outputs the text in a visually pleasing way

    global time_
    global Settings

    if string == "":
        return ""

    if Settings["TYPE_SPEED"] == 0:
        return string
    
    if time_:        
        for char in string:
            print(char,end="")
            sleep(0.1/Settings["TYPE_SPEED"])
        return ""
    else:
        return string

def Find_Authorised_Players():# Gets list of authorised players from external text file "./FILES/Players.txt"
    
    file_ = open("./FILES/PLAYERS.txt","r")# Reads the text file "./FILES/Players.txt"
    lines = file_.readlines()
    file_.close()
    
    for i in lines:
        name = i.strip("\n")# Removes a new line Charsacter from the line to get the name
        globals()["Authorised_Players"].append(name)# Appends the list of names with the new name

    return

def Input_Details():

    Find_Authorised_Players()

    global Authorised_Players
    global Players
    global Banned_Chars

    globals()["Players"] = ["",""]

    for i in range(0,2):

        while Players[i] == "":
            name = str(input(Display("Player "+str(i+1)+": What is your name? "))).upper()# Gets the player to input their name

            if name == "":# Ensures that the player enters a name
                continue

            if name in Players:# Ensures that the players cannot have the same name
                print(Display("Player names cannot match."))
                continue


            a = False# Ensures that the player's name does not contain a banned Charsacter
            for x in Banned_Chars:

                if x in name:
                    print(Display("Your name contains a banned Character."))
                    a = True
                    break
            if a:
                continue
            
            if name in Authorised_Players:# Checks the inputted name against the list of authorised players
                globals()["Players"][i] = name# Changes the players name to the inputted value
            else:
                print(Display("That is an invalid name."))

        print(Display())

    return

def Get_Leaderboard():

    global csv_delimiter
    
    file_ = open("./FILES/LEADERBOARD.csv","r")# Reads the csv file "./FILES/LEADERBOARD.csv"
    csv_file = reader(file_,delimiter=csv_delimiter)

    output = {"HEADERS":"","Scores":[]}
    
    for row in csv_file:# Enters the contents of the csv file into a dictionary
        if row == []:
            continue
        if output["HEADERS"] == "":
            output["HEADERS"] = row
            continue
        output["Scores"].append(row)

    return output# Returns the dictionary containing the leaderboard

def Print_Leaderboard(leaderboard):# Prints the leaderboard

    global Collumn_Width
    global Table_Chars
    
    print(Display("Leaderboard:"),end="\n\n")
    headers = []

    for i in leaderboard["HEADERS"]:# Processes the headers
        headers.append(i.center(Collumn_Width," "))

    print(Display(Table_Chars[0].join(headers)))# Prints the headers
    print(Display(Table_Chars[1]*len(leaderboard["HEADERS"])*Collumn_Width))

    for i in leaderboard["Scores"]:# Processes the scores
        line = []
        for x in i:
            line.append(x.center(Collumn_Width," "))
        print(Display(Table_Chars[0].join(line)))# Prints each line of the scores

    return

def Write_Leaderboard(leaderboard):# Writes the leaderboard to the text file

    global csv_delimiter

    file_ = open("./FILES/LEADERBOARD.csv","w")# Opens the csv file "./FILES/LEADERBOARD.csv" in write mode
    csv_file = writer(file_,delimiter=csv_delimiter)

    csv_file.writerow(leaderboard["HEADERS"])# Writes the headers
    for i in leaderboard["Scores"]:# Writes each row one by one
        csv_file.writerow(i)

    file_.close()# Closes the csv file "./FILES/LEADERBOARD.csv"

    return

def Roll_Dice(sides=6,number=1):# Rolls an unbiased dice with a given number of sides a given number of times

    die = []

    for i in range(number):
        roll = randint(1,sides)
        die.append(roll)

    return die# Returns the results of the die in an array

def Get_Score(current_score):# Rolls the dice and calculates the score appropriately

    global Settings

    even = Settings["EVEN"]
    odd = Settings["ODD"]
    sides = Settings["SIDES"]
    mult = Settings["MULTIPLIER"]
    e_sides = Settings["EXTRA_SIDES"]
    e_mult = Settings["EXTRA_MULTIPLIER"]

    die = Roll_Dice(number=2,sides=sides)# Rolls two dice

    input(Display("You have rolled a "+str(min(die[0],die[1]))+" and a "+str(max(die[0],die[1]))+"."))# Outputs the dice

    die_total= die[0] + die[1]# Calculates the score

    if die_total % 2 == 0:
        die_total += even
    else:
        die_total += odd

    die_total = die_total*mult

    new_score = current_score + die_total

    if die[0] == die[1]:# Gets the user to roll again if they rolled a double
        input(Display("You have rolled a double. Press enter to roll again."))
        extra_die = Roll_Dice(sides=e_sides)
        print(Display("You have rolled a "+str(extra_die[0])+"."))
        new_score += (extra_die[0]*e_mult)

    if new_score < 0:
        new_score = 0

    return new_score# Returns the new score

def Game():

    global Players
    global Scores
    global Settings

    rounds = Settings["ROUNDS"]

    for x in range(1,rounds+1):# Repeats for a given number of rounds

        input(Display("Round "+str(x)+":\n"))

        for i in range(0,2):# Gets the scores for each player
            
            input(Display(str(Players[i])+", press enter to roll your dice."))
            globals()["Scores"][i] = Get_Score(Scores[i])
            print(Display("Your score is now "+str(Scores[i])+".\n"))

    if Scores[0] > Scores[1]:# Checks for a winner, and enters sudden death if the scores are equal
        Win([Players[0],Players[1]],[Scores[0],Scores[1]])
    elif Scores[1] > Scores[0]:
        Win([Players[1],Players[0]],[Scores[1],Scores[0]])
    else:
        winner = SUDDEN_DEATH()
        if winner == Players[0]:
            Win([Players[0],Players[1]],[Scores[0],Scores[1]])
        else:
            Win([Players[1],Players[0]],[Scores[1],Scores[0]])

    return

def SUDDEN_DEATH():# Sudden death

    global Players

    input(Display("Sudden death.\n"))

    scores = [0,0]

    while True:# Rolls each player 1 extra dice
        for i in range(0,2):
            input(Display(str(Players[i])+", press enter to roll your die."))
            die = Roll_Dice()[0]
            scores[i] = die
            print(Display("You rolled a "+str(die)+".\n"))
        
        if scores[0] > scores[1]:# Checks for a winner
            return Players[0]
        elif scores[1] > scores[0]:
            return Players[1]

def Win(Players,Scores):# Declares the winner post-game

    global Default

    print(Display("The winner is "+str(Players[0])+" with "+str(Scores[0])+" points.\n"))# Prints the winner and their points

    leaderboard = Get_Leaderboard()

    if Default:

        for i in range(0,len(Scores)):# Updates the leaderboard
            updated = False
            for x in range(0,len(leaderboard["Scores"])):
                if int(leaderboard["Scores"][x][1]) < Scores[i] and updated == False:
                    leaderboard["Scores"].insert(x,[Players[i],str(Scores[i])])
                    del leaderboard["Scores"][5]
                    break

        Write_Leaderboard(leaderboard)# Writes the new leaderboard to the file
    else:
        print(Display("You will not be written to the leaderboard due to your settings."))

    Print_Leaderboard(leaderboard)# Outputs the leaderboard

    return

def Rules():# Outputs the rules of the game

    input(Display("Welcome to the dice game."))
    input(Display("The rules are simple, press enter to roll your two dice."))
    input(Display("The total of the two dice will be added to your score."))
    input(Display("If the total of the two dice is even, 10 points will be added to your score."))
    input(Display("If the total of the two dice is odd, 5 points will be subtracted from your score."))
    input(Display("If the two dice are the same, you will be given a third dice to roll, this dice will then be added to your score."))
    input(Display("If after five rounds the scores are equal, we will enter sudden death."))
    input(Display("In sudden death each player will roll one extra dice and the player with the highest dice will win."))

    return

def Change_To_Class(value):# Changes a value to its appropriate class
    
    try:
        value = int(value)
    except ValueError:
        pass
    if value == "True":
        value = True
    elif value == "False":
        value = False

    return value

def Check_If_Valid(value,key):# Checks for errors in the line, and updates the global dictionary "Settings" if none are found

    global Settings_Options

    keys = Settings_Options.keys()

    if key not in keys:
        return True
    if value not in Settings_Options[key]:
        return True
    if type(value) == type(True) and Settings_Options[key] != [True,False]:
        return True
    globals()["Settings"][key] = value

    return False# Returns a boolean value based on whether or not or lines were successfully imported

def Settings_Menu():

    global Settings
    global Settings_Options
    global Default_Settings
    global Game_Settings

    keys = list(Settings.keys())

    print(Display("To go back, type 'b'.\n"))

    for i in range(0,len(keys)):
        print(Display(str(i+1)+") "+str(keys[i]).replace("_"," ")+": "+str(Settings[keys[i]])))
    print(Display("\n"+str(len(keys)+1)+") Load a config file"))
    print(Display(str(len(keys)+2)+") Save settings to a config file"))
    print(Display(str(len(keys)+3)+") Reset to default options"))

    while True:
        choice = str(input(Display("\nWhat is your option? "))).replace(" ","_").lower()
        z = False
        for i in range(0,len(keys)):
            if choice in [str(i+1),str(keys[i]).lower()]:
                z = True
                while True:
                    value = str(input(Display("What would you like to change it to? ")))
                    value = Change_To_Class(value)
                    a = Check_If_Valid(value,keys[i])
                    if not a:
                        break
                    print(Display("That is an invalid option."),end="")
                    if type(Settings_Options[keys[i]]) == type(range(0,1)):
                        print(Display("You must enter a number between "+str(Settings_Options[keys[i]][0])+" and "+str(Settings_Options[keys[i]][-1])+"."))
                    else:
                        print(Display("You must enter one of: "))
                        for x in Settings_Options[keys[i]]:
                            print(Display(x))
        if z:
            globals()["Default"] = False
        elif choice in [str(len(keys)+1),"load","config","file"]:
            LOAD()
        elif choice in [str(len(keys)+2),"save","save file"]:
            SAVE()
        elif choice in [str(len(keys)+3),"reset","default"]:
            a = Load_Settings("./FILES/CONFIG/Default_Settings.cfg")
            if a:
                print(Display("Error loading default settings file.\n\nTerminating script."))
                raise SystemExit(0)
            else:
                print(Display("Default settings loaded."))
                globals()["Default"] = True
        elif choice in ["b","back","q"]:
            return
        else:
            print(Display("\nThat is an invalid option.\n"))

        globals()["Default"] = True
        for setting in Game_Settings:
            if Settings[setting] != Default_Settings[setting]:
                globals()["Default"] = False
        

def Load_Settings(path):# Loads the settings from a given external file path into the global variable Settings
    
    try:# Opens the file path in read mode and raises an IOError is it cannot be found
        file_ = open(path,"r")
    except IOError:
        raise IOError

    csv_file = reader(file_,delimiter=csv_delimiter)

    settings = {}

    for row in csv_file:# Reads each row of the file and appends it to a dictionary
        if row == []:
            continue
        
        value = Change_To_Class(row[1].strip("\n"))
        settings[row[0]] = value
        
    keys = Settings_Options.keys()
    keys2 = settings.keys()

    a = True

    for i in keys2:
        b = Check_If_Valid(settings[i],i)
        if b == False:
            a = False

    return a

def LOAD():

    while True:

        fname = str(input(Display("What is the name of the config file that you want to load? ")))
        path = "./FILES/CONFIG/"+fname+".cfg"
        if path != "./FILES/CONFIG/Default_Settings.cfg":
            globals()["Default"] = False
        else:
            globals()["Default"] = True

        try:
            a = Load_Settings(path)
            if not a:
                print(Display("File loaded."))
            else:
                print(Display("Error loading part of file."))
            return
        except IOError:
            print(Display("File could not be found."))

def SAVE():

    global Settings

    while True:

        fname = str(input(Display("What do you want to call this config file? ")))
        path = "./FILES/CONFIG/"+fname+".cfg"

        try:
            a = open(path,"r")
            a.close()
            while True:
                b = str(input(Display("File already exists. Do you want to overwrite? "))).lower()
                z = False
                if b in ["yes","y","true",True,1,"1"]:
                    break
                elif b in ["no","n","false",False,0,"0"]:
                    z = True
                    break
                else:
                    print(Display("Invalid answer, you must enter either yes or no."))
            if z:
                continue
        except IOError:
            pass

        file_ = open(path,"w")
        csv_file = writer(file_,delimiter=":")

        keys = list(Settings.keys())

        for i in keys:
            csv_file.writerow([i,Settings[i]])

        file_.close()

        print(Display("File saved."))

        return
        

def Menu():# The menu for the game

    global Default

    input(Display("Welcome to my dice game."))
    
    while True:
        
        choice = str(input(Display("""\n
1) Play
2) Rules
3) Leaderboard
4) Settings
5) Quit

Please select an option: """))).lower()
        print(Display())

        if choice in [1,"1","a","p","play","game"]:
            z = False
            if not Default:
                while True:
                    yn = str(input(Display("Due to your current settings, you will not be added to the leaderboard. Do you still want to play? "))).lower()
                    if yn in ["yes","y","true",True,"1",1]:
                        break
                    elif yn in ["no","n","false",False,0,"0"]:
                        z = True
                        break
                    else:
                        print(Display("That is an invalid option."))
            if z:
                continue
                    
            Input_Details()
            Game()
        elif choice in [2,"2","b","r","rules"]:
            Rules()
        elif choice in [3,"3","c","l","leaderboard"]:
            leaderboard = Get_Leaderboard()
            Print_Leaderboard(leaderboard)
        elif choice in [4,"4","d","s","settings"]:
            Settings_Menu()
        elif choice in [5,"5","e","q","quit"]:
            raise SystemExit(0)
            return
        else:
           input(Display("That is an invalid option."))

a = Load_Settings("./FILES/CONFIG/Default_Settings.cfg")

if a:
    print(Display("Error loading default settings file.\n\nTerminating script."))
    raise SystemExit(0)

globals()["Default_Settings"] = dict(Settings)
Default = True

Menu()

#print(Get_Leaderboard())#

# Sources:
#"https://realpython.com/python-csv/#" - 25/10/2018, 05/11/2018, 15/11/2018, 12/12/2018
#"https://stackoverflow.com/questions/18552001/accessing-dict-keys-element-by-index-in-python3" - 05/12/2018
