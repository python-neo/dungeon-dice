# Dungeon Dice

Turn-based dungeon crawler in the terminal, built with Python.

## Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Gameplay](#gameplay)
- [Configuration](#configuration)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Background

Dungeon Dice is a lightweight CLI game where each `enter` command rolls a room event:

- empty room
- treasure room
- trap room
- monster fight

You manage HP, attack, gold, and potions while trying to survive dungeon runs.

## Install

### Requirements

- Python 3.10+
- `rich`

### Setup

```bash
pip install -r requirements.txt
```

## Usage

Run from the project root:

```bash
python -m main.main
```

Core commands:

- `enter` - roll a new room event
- `i` - show inventory and stats
- `potion <name>` - use a potion
- `exit` - quit the game

Potion examples:

- `potion healing`
- `potion greater healing`
- `potion strength`
- `potion escape`

## Gameplay

- HP starts at 100.
- Monster fights are turn-based.
- Strength potion applies a temporary attack buff during battle.
- Escape potion only works during battle and ends the current fight.
- Healing effects are capped at 100 HP.

## Configuration

Main balancing tables live in `main/player.py`:

- `self.potion_drop_table`
- `self.trap_table`
- `self.monster_table`

Room probabilities are defined in `Player.enter()`.

## Development

Project layout:

```text
main/
  __init__.py
  console.py
  main.py
  player.py
CHANGELOG.md
README.md
LISCENCE.md
```

Quick syntax check:

```bash
python -m py_compile main/main.py main/player.py main/console.py
```

## Contributing

Issues and pull requests are welcome.

For gameplay changes, include:

- what changed
- why the change improves balance or UX
- how you tested the behavior

## License

This project is licensed under MIT. See `LISCENCE.md`.
