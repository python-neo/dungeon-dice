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
        self.attack = 5
        self.battle = False
        self.hp : int = 100
        self.gold : int = 0
        self.potions : dict = {"healing" : 0,
                        "strength" : 0,
                        "escape" : 0,
                        "greater healing" : 0}
        self.potion_labels : dict = {"healing" : "Healing Potion",
                              "strength" : "Strength Potion",
                              "escape" : "Escape Potion",
                              "greater healing" : "Greater Healing Potion"}
        self.commands : dict = {"exit" : {"command" : sys.exit, "args" : False},
                                "i" : {"command" : self.inventory, "args" : False},
                                "enter" : {"command" : self.enter, "args" : False},
                                "potion" : {"command" : self.use_potion, "args" : True}}
        self.potion_drop_table : tuple = (
            ("healing", 40),
            ("strength", 25),
            ("escape", 20),
            ("greater healing", 15),
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
                console.print (f"[cyan]You found 1 {self.potion_labels [potion]}![/]")
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

    def inventory (self) -> None :
        table = Table (show_header = False, box = None)
        for _ in range (2) : table.add_column ()

        table.add_row ("HP", f"[bold green]{self.hp}[/]")
        table.add_row ("Attack", f"[bold red]{self.attack}[/]")
        table.add_row ("Gold", f"[gold1]x{self.gold}[/]")
        for potion_name, count in self.potions.items () :
            table.add_row (self.potion_labels [potion_name] + "s", f"[cyan]x{count}[/]")

        console.print (Panel (table, title = "Inventory"))

    def use_potion (self, *args) -> None :
        if not args :
            console.print ("[bold red]Choose a potion.[/]")
            return

        potion = " ".join (args).strip ().lower ()
        potion = potion.removesuffix (" potions")
        potion = potion.removesuffix (" potion")
        if potion not in self.potions :
            console.print ("[bold red]Potion not found[/]")
            return

        if potion == "escape" :
            if not self.battle :
                console.print ("[red]You have to be in a battle to use this potion.[/]")
                return
            if self.potions ["escape"] <= 0 :
                console.print ("[red]You do not have this potion.[/]")
                return
            self.potions ["escape"] -= 1
            self.battle = False
            console.print ("You escape from the battle.")
            return

        if self.potions [potion] <= 0 :
            console.print ("[red]You do not have this potion.[/]")
            return

        if potion == "strength" :
            self.attack *= 2
            console.print ("You [cyan]double[/] your attack.")
        else :
            heal = (30 if potion == "greater healing" else 10)
            self.hp = min (100, self.hp + heal)
            console.print (f"[green]+{heal} HP![/]")
        self.potions [potion] -= 1