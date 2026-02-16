# Dungeon Dice

A lightweight Python CLI dungeon crawler.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![Platform](https://img.shields.io/badge/Platform-CLI-orange.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Game Structure](#game-structure)
- [Installation & Usage](#installation--usage)
- [Gameplay](#gameplay)
- [Planned Features](#planned-features)
- [License](#license)
- [Contributing](#contributing)

---

## About

**Dungeon Dice** is a fast-paced command-line dungeon exploration game.

Each room you enter is decided by chance—enemies, traps, treasure, or nothing at all. Manage your health, collect gold, and survive long enough to escape the dungeon.

The project is designed to be simple, expandable, and ideal for learning Python game loops and random event systems.

---

## Features

- Random dungeon events
- Turn-based combat
- Treasure collection system
- Healing potion mechanic
- Expandable game loop
- Pure CLI gameplay

---

## Game Structure

Example project layout:

```text
dungeon-dice/
│
├── main.py        # Main game loop
├── events.py      # Dungeon events logic
├── player.py      # Player stats and inventory
├── combat.py      # Combat handling
└── README.md
````

Small projects may combine everything into `main.py`.

---

## Installation & Usage

### Requirements

- Python **3.8 or above**

### Run the Game

Navigate to the project folder and run:

```bash
python main.py
```

---

## Gameplay

Each turn:

1. Enter a room.

2. A random event occurs:

   - Enemy encounter
   - Trap
   - Treasure
   - Empty room

3. Player chooses actions:

   - Fight
   - Use potion
   - Continue exploring
   - Escape dungeon

Game ends when:

- Player health reaches 0, or
- Player escapes with collected gold.

---

## Planned Features

Future improvements may include:

- Boss encounters
- Inventory expansion
- Shop rooms
- Equipment system
- Critical hits & skills
- Save/load system
- Procedural dungeon paths
- High-score tracking

---

## License

This project is released under the **MIT Liscence**.

You are free to use, modify, and distribute it.

---

## Contributing

Contributions are welcome:

- Report bugs via issues
- Suggest new mechanics
- Submit improvements or refactors

Please keep code clean and consistent with the project structure.

---

### Build fast, expand endlessly, and survive the dungeon!
