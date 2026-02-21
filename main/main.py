from .console import console
import sys
from rich.panel import Panel
from rich.prompt import Prompt
from .player import Player

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