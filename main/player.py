from .console import console
from random import randint, choice
import sys
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Confirm, Prompt
from .game_data import (
    GLOBAL,
    Monster,
    Trap,
    Potion,
    default_global_state,
    default_monster_table,
    default_potions,
    default_trap_table,
)

class Dice :
    """
    Utility dice helpers for random rolls.
    """
    @staticmethod
    def roll (total : int) -> int :
        """
        Roll a die between 1 and a given upper bound.

        Args:
            total (int): Upper bound of the roll (inclusive).

        Returns:
            int : Random value in the range [1, total].
        """
        return randint (1, total)

    @staticmethod
    def rpg (total : int, success : int = 1) -> bool :
        """
        Roll against a success threshold.

        Args:
            total (int): Upper bound of the roll (inclusive).
            success (int): Maximum value that still counts as success.

        Returns:
            bool : `True` when roll is less than or equal to success threshold.
        """
        return randint (1, total) <= success

class Player :
    """
    Core player model and gameplay controller.
    """
    def __init__ (self) -> None :
        """
        Initialize player state, tables, and command registry.
        """
        self.global_state = default_global_state ()
        self.attack = self.global_state [GLOBAL.BASE_ATTACK]
        self.hp : int = 100
        self.gold : int = 0
        self.potions : dict [str, Potion] = default_potions ()
        self.commands : dict = {"exit" : {"command" : sys.exit, "args" : False},
                                "i" : {"command" : self.inventory, "args" : False},
                                "enter" : {"command" : self.enter, "args" : False},
                                "potion" : {"command" : self.use_potion, "args" : True}}
        self.trap_table : list [Trap] = default_trap_table ()
        self.monster_table : list [Monster] = default_monster_table ()

    def enter (self) -> None:
        """
        Enter a random room and resolve its outcome.

        Notes:
            Room distribution is currently:
                - Empty room : 15%
                - Treasure room : 30%
                - Trap room : 25%
                - Monster fight : 30%
        """
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

            potions_found = [potion for potion in self.potions.values () if Dice.rpg (100, potion.drop_chance)]
            if not potions_found :
                console.print ("[default]No potions this time.[/]")
            for potion in potions_found :
                potion.quantity += 1
                console.print (f"[cyan]You found 1 {potion.tag}![/]")
        elif roll <= 70 :
            console.print ("[red]You stumble into a trap![/]")
            traps_hit = [trap for trap in self.trap_table if Dice.rpg (100, trap.chance)]
            if not traps_hit :
                console.print ("[green]However, you avoid all of them[/]")
            for trap in traps_hit :
                self.hp = max (0, self.hp - trap.damage)
                console.print (f"[red]{trap.name}! You lose {trap.damage} HP.[/]")
        else :
            self.fight_monster ()

    def inventory (self) -> None :
        """
        Display current player stats and potion inventory.
        """
        table = Table (show_header = False, box = None)
        for _ in range (2) : table.add_column ()

        table.add_row ("HP", f"[bold green]{self.hp}[/]")
        table.add_row ("Attack", f"[bold red]{self.attack}[/]")
        table.add_row ("Gold", f"[gold1]x{self.gold}[/]")
        for potion in self.potions.values () :
            label = potion.tag if potion.quantity == 1 else potion.tag + "s"
            table.add_row (label, f"[cyan]x{potion.quantity}[/]")

        console.print (Panel (table, title = "Inventory"))

    def use_potion (self, *args) -> None :
        """
        Use a potion by name.

        Args:
            args (tuple): Potion name tokens from user command input.

        Notes:
            - Escape potion works only during battle.
            - Strength potion works only during battle.
            - Healing values are capped to 100 HP.
        """
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
            if not self.global_state [GLOBAL.BATTLE] :
                console.print ("[red]You have to be in a battle to use this potion.[/]")
                return
            if self.potions ["escape"].quantity <= 0 :
                console.print ("[red]You do not have this potion.[/]")
                return
            self.potions ["escape"].quantity -= 1
            self.global_state [GLOBAL.BATTLE] = False
            console.print ("You escape from the battle.")
            return

        if self.potions [potion].quantity <= 0 :
            console.print ("[red]You do not have this potion.[/]")
            return

        if potion == "strength" :
            if not self.global_state [GLOBAL.BATTLE] :
                console.print ("[red]You have to be in a battle to use this potion.[/]")
                return
            self.attack = self.global_state [GLOBAL.BASE_ATTACK] * 2.5
            self.global_state [GLOBAL.STRENGTH_TURNS_LEFT] = 3
            console.print ("You [cyan]double[/] your attack.")
        else :
            heal = (40 if potion == "greater healing" else 15)
            self.hp = min (100, self.hp + heal)
            console.print (f"[green]+{heal} HP![/]")
        self.potions [potion].quantity -= 1

    def reset_strength_buff (self) -> None :
        """
        Reset temporary strength effects back to base attack.
        """
        self.attack = self.global_state [GLOBAL.BASE_ATTACK]
        self.global_state [GLOBAL.STRENGTH_TURNS_LEFT] = 0

    def fight_monster (self) -> None :
        """
        Run a full monster encounter loop until win, escape, or death.

        Notes:
            - On victory, player gains monster gold and +5 HP.
            - Strength turns are consumed on successful player attacks.
        """
        monster = Monster (**vars (choice (self.monster_table)))
        console.print (f"You face a {monster.name}!")
        self.global_state [GLOBAL.BATTLE] = True

        while monster.hp > 0 and self.hp > 0 and self.global_state [GLOBAL.BATTLE] :
            if Dice.rpg (10, 3) :
                console.print (f"[green]The {monster.name} misses! You lose no HP![/]")
            else :
                self.hp = max (0, self.hp - monster.atk)
                console.print (f"[red]The monster hits you! -{monster.atk} HP.")
                if self.hp == 0 :
                    self.reset_strength_buff ()
                    self.global_state [GLOBAL.BATTLE] = False
                    return
                
            while True :
                command = Prompt.ask ("What do you want to do?").lower ().strip ().split ()
                if command [0] not in ("potion", "attack", "i") :
                    console.print ("[bold red]Command not found[/]")
                else : 
                    if command [0] == "potion" :
                        self.use_potion (*command [1:])
                        break
                    elif command [0] == "i" :
                        self.inventory ()
                    else : break
            if not GLOBAL.BATTLE : return
            monster.hp -= self.attack
            console.print (f"[green]You hit the monster! The monster loses {self.attack} HP.[/]")
            if self.global_state [GLOBAL.STRENGTH_TURNS_LEFT] <= 0 :
                continue
            self.global_state [GLOBAL.STRENGTH_TURNS_LEFT] -= 1
            if self.global_state [GLOBAL.STRENGTH_TURNS_LEFT] == 0 :
                self.reset_strength_buff ()

        self.global_state [GLOBAL.BATTLE] = False
        if monster.hp <= 0 :
            self.gold += monster.gold
            console.print (f"[bold green]Success! You defeat the monster! +{monster.gold} gold![/]")
            self.hp += 5
        else :
            self.reset_strength_buff ()