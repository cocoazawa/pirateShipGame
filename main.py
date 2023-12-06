# This implementation does NOT use the Go CLI Assistant, but still uses Classes, and simplifies the codebase. 
# New features are weather in the Caribbean to make accurate forecasts as to the ships available to loot, and the inclusion of more probability.

from random import randint
from time import sleep
import requests

weatherAPIAddress = "https://api.open-meteo.com/v1/forecast?latitude=20.7356&longitude=-71.8726&current=temperature_2m,rain,wind_speed_10m,wind_direction_10m,wind_gusts_10m&forecast_days=1"

class CaribbeanBay:
    weatherConditions = "findOut"

    def __init__(self, dockingPositions, dockingCost):
        self.dockingPositions = dockingPositions
        self.dockingCost = dockingCost

    def weather(self):
        caribbeanWeatherData = requests.get(weatherAPIAddress)
        caribbeanWeatherData = caribbeanWeatherData.json()
        currentRain = int(caribbeanWeatherData['current']['rain'])
        currentTemp = int(caribbeanWeatherData['current']['temperature_2m'])
        currentWind = int(caribbeanWeatherData['current']['wind_speed_10m'])
        currentGusts = int(caribbeanWeatherData['current']['wind_gusts_10m'])
        
        if (currentTemp < 35):
            pass
        else: 
            self.weatherConditions = "highTemp"
            return "highTemp"
        
        if (currentWind <= 10) and (currentGusts <= 12):
            pass
        else:
            self.weatherConditions = "highWind"
            return "highWind"

        if (currentRain <= 0.1):
            self.weatherConditions = "allGood"
            return "allGood"
        elif (currentRain <= 0.5):
            self.weatherConditions = "raining"
            return "raining"
        elif (currentRain <= 1.0):
            self.weatherConditions = "highRain"
            return "highRain"

        return "findOut"


class PirateShip:
    locationOfShip = "bay"
    shipDocked = True
    shipGold = 0
    crewLevel = 1

    def __init__(self, shipName, shipGold, shipCrew):
        self.shipName = shipName
        self.shipGold = shipGold
        self.shipCrew = shipCrew
    
    def moveShip(self, dock: CaribbeanBay):
        print("\033[2JYou can steer the ship to the nearest bay or ship.")
        locationInput = str(input("Which one do you want (bay, ship)? "))

        if ("ship" == locationInput):
            print("\033[2JSteering to nearest ship!")
            self.locationOfShip = "otherShipHeading"
            self.shipDocked = False
            self.locationOfShip = "otherShip"
        elif ("bay" == locationInput):
            print("\033[2JSteering to nearest bay!")
            self.locationOfShip = "bayHeading"

            print("Checking dock...")
            if (dock.weather() == "allGood") or (dock.weather() == "raining"):
                print(f"Good to dock! That'll be {dock.dockingCost} gold per turn.")
                self.locationOfShip = "bay"
                self.shipDocked = True
                self.shipGold -= dock.dockingCost
            else:
                print("You can't dock right now due to weather conditions! Returning to sea...")
                self.locationOfShip = "sea"
        
        sleep(2)
        journeyChoices()

    def attackShip(self):
        print("\033[2JAttacking other ship...")

        if (self.locationOfShip != "otherShip"):
            print("Sorry, there been no ship to attack!")
            sleep(2)
            journeyChoices()
        elif (self.shipDocked == True):
            print("Sorry, ye be docked! Un-dock to attack or move.")
            sleep(2)
            journeyChoices()
        
        prob = randint(1, 100)
        prob = (prob <= (5 * self.crewLevel)) if ((5 * self.crewLevel) != 100) and (self.crewLevel != 1) else True

        if prob == True:
            wonGold = randint(0, 200)
            self.crewLevel += 1
            self.shipGold += wonGold
            self.locationOfShip = "sea"
            print(f"Attacked successfully! Won {wonGold} gold, and leveled up crew.")
            sleep(2)
        else:
            lostGold = randint(0, 100)
            self.crewLevel -= 1 if (self.crewLevel >= 1) else self.crewLevel
            self.shipGold -= lostGold
            self.locationOfShip = "sea"
            print(f"Attack failed. We'll get 'em next time! Lost {lostGold} gold, and your crew's level decreased.")
            sleep(2)
        
        journeyChoices()

    def tradeLevel(self):
        if (self.shipDocked == True) or (self.locationOfShip != "bay"):
            print("Sorry, dock (move) to the bay first!")
            sleep(2)
            return

        print("\033[2JThe market sells weapons and grub! What would you like to buy?")
        print("Weapons: 5 gold, 1.5 levels")
        print("Grub: 0.5 gold, 0.1 levels")
        inputShop = str(input("Which would ye like (weapons, grub)? "))

        if (inputShop == "weapons") and (self.shipGold >= 5):
            self.crewLevel += 1.5
            self.shipGold -= 5
            print("Purchase complete! Come again!")
            sleep(2)
        elif (inputShop == "grub") and (self.shipGold >= 0.5):
            self.crewLevel += 0.1
            self.shipGold -= 0.5
            print("Purchase complete! Come again!")
            sleep(2)
        else:
            print("Sorry mate! We don' sell that!")
            sleep(2)
        
        journeyChoices()

mainBay = CaribbeanBay(3, 3.45)
mainShip = PirateShip("Mayflower", 15, 10)
turn = 0

def journeyChoices():
    global turn
    print("\033[2J\033[1mAhoy! Welcome aboard!")
    print("What would ye like to do t'day?\033[0m")
    print(f"Your ship, \033[1m{mainShip.shipName}\033[0m, has {'%.2f' % mainShip.shipGold} gold and is at {mainShip.crewLevel} level.")
    print()
    print(f"{mainShip.shipName} is currently at {mainShip.locationOfShip}.")
    print(f"It costs {mainBay.dockingCost} gold to be docked.")
    print()

    if (mainShip.shipDocked == True) and (turn != 0):
        mainShip.shipGold -= mainBay.dockingCost

    captainChoice = str(input("The choice is yours (move, attack, market, nothing, exit): "))

    if (captainChoice == "move"):
        mainShip.moveShip(mainBay)
    elif (captainChoice == "attack"):
        mainShip.attackShip()
    elif (captainChoice == "market"):
        mainShip.tradeLevel()
    elif (captainChoice == "nothing"):
        pass
    elif (captainChoice == "exit"):
        exit(1)

    turn += 1

    journeyChoices()


journeyChoices()
