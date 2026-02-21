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
        self.potion_drop_table : tuple = (
            ("Healing Potions", 40),
            ("Strength Potions", 25),
            ("Escape Potions", 20),
            ("Greater Healing Potions", 15),
        )
        self.trap_table : tuple = (
            ("Darts", 5, 35),
            ("Spikes", 8, 25),
            ("Poison Needle", 6, 20),
            ("Swinging Blade", 12, 15),
            ("Crushing Wall", 18, 5),
        )

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
        elif roll == 2 :
            console.print ("[green]You find treasure![/]")
            gold = Dice.roll (10)
            self.gold += gold
            console.print (f"[gold1]+{gold} gold.[/]")

            potions_found = [name for name, chance in self.potion_drop_table if Dice.rpg (100, chance)]
            if not potions_found :
                console.print ("[default]No potions this time.[/]")
            for potion in potions_found :
                self.potions [potion] += 1
                console.print (f"[cyan]You found 1 {potion[:-1]}![/]")
        elif roll == 3 :
            console.print ("[red]You stumble into a trap![/]")
            traps_hit = [(name, damage) for name, damage, chance in self.trap_table if Dice.rpg (100, chance)]
            if not traps_hit :
                console.print ("[green]However, you avoid all of them[/]")
            for name, damage in traps_hit :
                self.hp = max (0, self.hp - damage)
                console.print (f"[red]{name}! You lose {damage} HP.[/]")
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