from .console import console
import sys
from rich.panel import Panel
from rich.prompt import Prompt
from .player import Player

"""
CLI entry point for Dungeon Dice.

Runs the main command loop, dispatches player commands, and exits when HP reaches 0.
"""

def run_game () -> None :
    """
    Start and run the main Dungeon Dice game loop.

    Notes :
        Reads commands from terminal input and dispatches them through
        the player's command registry.
    """
    player = Player ()

    console.print (Panel ("Welcome to Dungeon Dice!", title = "Dungeon Dice 🎲"))

    while True :
        command = Prompt.ask ("> ")
        commands = command.strip ().lower ().split (" ")
        try :
            func = player.commands [commands [0]]
        except KeyError :
            console.print ("[bold red]Command not found.[/]")
            continue
        if func ["args"] :
            func ["command"] (*commands [1:])
        else :
            func ["command"] ()

        if player.hp <= 0 :
            console.print ("[bold red]You died in the dungeon.[/]")
            sys.exit ()

if __name__ == "__main__" :
    run_game ()
