from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from random import randint

console = Console ()

class Player :
    def __init__ (self) :
        self.hp = 100
        self.gold = 0
        self.potions = {"Healing Potion" : 0,
                        "Strength Potion" : 0,
                        "Escape Potion" : 0,
                        "Greater Healing" : 0}

    def enter_room (self) :
        roll = Dice.roll ()
        if roll == 1 :
            console.print ("You find an empty room...")

class Dice :
    @staticmethod
    def roll () :
        return randint (1, 4)

console.print ()