from dataclasses import dataclass
from enum import Enum, auto

@dataclass
class Monster :
    """
    Represents a monster template used in dungeon fights.

    Args:
        name (str): Monster display name.
        hp (int | float): Starting health points.
        atk (int): Damage dealt per successful hit.
        gold (int): Gold rewarded when defeated.
    """
    name : str
    hp : int | float
    atk : int
    gold : int

@dataclass
class Trap :
    """
    Represents a trap template for trap rooms.

    Args:
        name (str): Trap display name.
        damage (int): Damage dealt when triggered.
        chance (int): Trigger chance out of 100.
    """
    name : str
    damage : int
    chance : int

@dataclass
class Potion :
    """
    Represents a potion definition and current inventory count.

    Args:
        name (str): Internal potion key.
        tag (str): Human-readable potion name.
        quantity (int): Current potion count in inventory.
        drop_chance (int): Drop chance out of 100 in treasure rooms.
    """
    name : str
    tag : str
    quantity : int
    drop_chance : int

class GLOBAL (Enum) :
    """
    Enum keys for mutable player-wide runtime values.
    """
    BASE_ATTACK = auto ()
    BATTLE = auto ()
    STRENGTH_TURNS_LEFT = auto ()


def default_global_state () -> dict [GLOBAL, int | bool] :
    """
    Build default runtime state for a new player.

    Returns:
        dict [GLOBAL, int | bool] : Initial values for base attack, battle state, and strength turns.
    """
    return {
        GLOBAL.BASE_ATTACK : 5,
        GLOBAL.BATTLE : False,
        GLOBAL.STRENGTH_TURNS_LEFT : 0,
    }

def default_potions () -> dict [str, Potion] :
    """
    Build default potion inventory and drop metadata.

    Returns:
        dict [str, Potion] : Potion mapping keyed by internal potion name.
    """
    return {
        "healing" : Potion ("healing", "Healing Potion", 0, 40),
        "strength" : Potion ("strength", "Strength Potion", 0, 25),
        "escape" : Potion ("escape", "Escape Potion", 0, 20),
        "greater healing" : Potion ("greater healing", "Greater Healing Potion", 0, 15),
    }

def default_trap_table () -> list [Trap] :
    """
    Build the default trap table.

    Returns:
        list [Trap] : Trap templates with damage and trigger chance.
    """
    return [
        Trap ("Darts", 5, 35),
        Trap ("Spikes", 8, 25),
        Trap ("Poison Needle", 6, 20),
        Trap ("Swinging Blade", 12, 15),
        Trap ("Crushing Wall", 18, 5),
    ]

def default_monster_table () -> list [Monster] :
    """
    Build the default monster table.

    Returns:
        list [Monster] : Monster templates for random encounters.
    """
    return [
        Monster ("Rat", 12, 2, 2),
        Monster ("Bat Swarm", 16, 3, 3),
        Monster ("Goblin", 16, 4, 3),
        Monster ("Skeleton", 28, 5, 7),
        Monster ("Orc Brute", 36, 6, 10),
        Monster ("Cave Troll", 52, 9, 15),
    ]
