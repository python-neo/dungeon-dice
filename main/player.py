from .console import console
from random import randint
import sys
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Confirm

class Dice :
    @staticmethod
    def roll (total : int) -> int : return randint (1, total)

    @staticmethod
    def rpg (total : int, success : int = 1) -> bool : return randint (1, total) <= success

class Player :
    def __init__ (self) -> None :
        self.hp : int = 100
        self.gold : int = 0
        self.potions : dict = {"Healing Potions" : 0,
                        "Strength Potions" : 0,
                        "Escape Potions" : 0,
                        "Greater Healing Potions" : 0}
        self.commands : dict = {"exit" : {"command" : sys.exit, "args" : False},
                         "i" : {"command" : self.inventory, "args" : False},
                         "enter" : {"command" : self.enter, "args" : False}}

    def enter (self) -> None:
        roll = Dice.roll (4)
        if roll == 1 :
            console.print ("You find an empty room...")
            _exit = Confirm.ask ("Leave the room?")
            if _exit : 
                console.print ("You leave the room.")
            else :
                roll = Dice.roll (100)
                if roll <= 90 :
                    console.print ("[default]You find nothing...[/]")
                elif roll <= 97 :
                    console.print ("[red bold]SLAM![/][red]You get hit by an arrow! -5 HP.[/]")
                    self.hp -= 5
                else :
                    console.print ("[green]You find treasure! +5 gold.[/]")
                    self.gold += 5 
        else :
            raise NotImplementedError

    def inventory (self) :
        table = Table (show_header = False, box = None)
        for _ in range (2) : table.add_column ()

        table.add_row ("HP", f"[bold red]{self.hp}[/]")
        table.add_row ("Gold", f"[gold1]x{self.gold}[/]")
        for potion_name, count in self.potions.items () :
            table.add_row (potion_name, f"[cyan]x{count}[/]")

        console.print (Panel (table, title = "Inventory"))