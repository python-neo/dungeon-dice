from .console import console
from random import randint
import sys
from rich.panel import Panel

class Dice :
    @staticmethod
    def roll () :
        return randint (1, 4)

class Player :
    def __init__ (self) :
        self.hp = 100
        self.gold = 0
        self.potions = {"Healing Potions" : 0,
                        "Strength Potions" : 0,
                        "Escape Potions" : 0,
                        "Greater Healing Potions" : 0}
        self.commands = {"exit" : {"command" : sys.exit, "args" : False},
                         "i" : {"command" : self.inventory, "args" : False}}

    def enter_room (self) :
        roll = Dice.roll ()
        if roll == 1 :
            console.print ("You find an empty room...")

    def inventory (self) :
        items = []
        if self.gold > 0 : items.append (f"[blue]{self.gold}[/] gold")

        for potion_name, count in self.potions.items () :
            if count > 0 : items.append (f"x{count} {potion_name.lower ()}")

        text = f"You have {', '.join (items)}" if items else "You have nothing."
        console.print (Panel (text, title = "Inventory"))