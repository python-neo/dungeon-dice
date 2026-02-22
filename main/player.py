from .console import console
from random import randint, choice
import sys
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Confirm, Prompt
from dataclasses import dataclass

class Dice :
    @staticmethod
    def roll (total : int) -> int : return randint (1, total)

    @staticmethod
    def rpg (total : int, success : int = 1) -> bool : return randint (1, total) <= success

@dataclass
class Monster :
    name : str
    hp : int | float
    atk : int
    gold : int

class Player :
    def __init__ (self) -> None :
        self.base_attack = 5
        self.attack = self.base_attack
        self.battle = False
        self.strength_turns_left = 0
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
        self.monster_table = [
            Monster ("Rat", 12, 2, 2),
            Monster ("Bat Swarm", 16, 3, 3),
            Monster ("Goblin", 16, 4, 3),
            Monster ("Skeleton", 28, 5, 7),
            Monster ("Orc Brute", 36, 6, 10),
            Monster ("Cave Troll", 52, 9, 15)
        ]

    def enter (self) -> None:
        roll = Dice.roll (100)
        if roll <= 15 :
            console.print ("You find an empty room...")
            _exit = Confirm.ask ("Leave the room?")
            if _exit : 
                console.print ("You leave the room.")
            else :
                roll = Dice.roll (100)
                if roll <= 90 :
                    console.print ("[default]You find nothing...[/]")
                elif roll <= 97 :
                    console.print ("[red bold]SLAM! [/][red]You get hit by an arrow! -5 HP.[/]")
                    self.hp -= 5
                else :
                    console.print ("[green]You find treasure! +5 gold.[/]")
                    self.gold += 5 
        elif roll <= 45 :
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
        elif roll <= 70 :
            console.print ("[red]You stumble into a trap![/]")
            traps_hit = [(name, damage) for name, damage, chance in self.trap_table if Dice.rpg (100, chance)]
            if not traps_hit :
                console.print ("[green]However, you avoid all of them[/]")
            for name, damage in traps_hit :
                self.hp = max (0, self.hp - damage)
                console.print (f"[red]{name}! You lose {damage} HP.[/]")
        else :
            self.fight_monster ()

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
            if not self.battle :
                console.print ("[red]You have to be in a battle to use this potion.[/]")
                return
            self.attack = self.base_attack * 2.5
            self.strength_turns_left = 3
            console.print ("You [cyan]double[/] your attack.")
        else :
            heal = (40 if potion == "greater healing" else 15)
            self.hp = min (100, self.hp + heal)
            console.print (f"[green]+{heal} HP![/]")
        self.potions [potion] -= 1

    def reset_strength_buff (self) -> None :
        self.attack = self.base_attack
        self.strength_turns_left = 0

    def fight_monster (self) -> None :
        monster = Monster (**vars (choice (self.monster_table)))
        console.print (f"You face a {monster.name}!")
        self.battle = True

        while monster.hp > 0 and self.hp > 0 and self.battle :
            if Dice.rpg (10, 3) :
                console.print (f"[green]The {monster.name} misses! You lose no HP![/]")
            else :
                self.hp = max (0, self.hp - monster.atk)
                console.print (f"[red]The monster hits you! -{monster.atk} HP.")
                if self.hp == 0 :
                    self.reset_strength_buff ()
                    self.battle = False
                    return

            command = Prompt.ask ("What do you want to do?").lower ().strip ().split ()
            while command [0] not in ("potion", "attack") :
                console.print ("[bold red]Command not found[/]")
                command = Prompt.ask ("What do you want to do?").lower ().strip ().split ()
            if command [0] == "potion" :
                self.use_potion (*command [1:])
                continue

            monster.hp -= self.attack
            console.print (f"[green]You hit the monster! The monster loses {self.attack} HP.[/]")
            if self.strength_turns_left <= 0 :
                continue
            self.strength_turns_left -= 1
            if self.strength_turns_left == 0 :
                self.reset_strength_buff ()

        self.battle = False
        if monster.hp <= 0 :
            self.gold += monster.gold
            console.print (f"[bold green]Success! You defeat the monster! +{monster.gold} gold![/]")
            self.hp += 5
        else :
            self.reset_strength_buff ()
