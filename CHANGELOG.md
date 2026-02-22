# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 2026-02-22 - 1.1
### Added
- `main/game_data.py` to centralize shared game definitions and defaults.
- `Trap` dataclass usage for trap table entries.
- Sphinx docs pages for `main`, `player`, and `game_data`.
- `CONTRIBUTING.md` with setup, commit, and PR guidance.
- In-fight inventory access (`i`) during monster encounters.

### Changed
- Moved `Monster`, `Trap`, `Potion`, and `GLOBAL` out of `main/player.py` into `main/game_data.py`.
- Moved potion drop chance into `Potion.drop_chance` and removed separate potion drop table.
- Reworked potion inventory to store `Potion` objects (with quantity) instead of raw ints.
- Updated room roll checks to explicit boundary-based percentages.
- Refreshed `README.md` to a standard structured format.
- Updated docstrings in `main/game_data.py`, `main/player.py`, and `main/main.py` for Sphinx/Napoleon rendering.
- Refactored `main/main.py` to use a documented `run_game()` entrypoint.

### Fixed
- Sphinx import path configuration in `sphinx/source/conf.py`.
- Sphinx `.rst` title underline lengths so toctree titles render correctly.
- Ignored Sphinx build artifacts via `.gitignore` (`/sphinx/build/`).

## 2026-02-22 - 1.0.0
### Added
- `potion` command for consuming potions from the command loop.
- Player attack stat in inventory output.
- `Player.battle` combat-state flag to support escape potion behavior during fights.
- Monster encounters (`roll == 4`) with turn-based combat and gold rewards.
- Monster roster (`Rat`, `Bat Swarm`, `Goblin`, `Skeleton`, `Orc Brute`, `Cave Troll`).

### Changed
- Potion inventory now uses normalized internal IDs with display labels for cleaner command parsing.
- Potion drop table and treasure-room potion messages now use shared potion label mapping.
- Refactored `use_potion` to a shorter, shared-control-flow implementation.
- Strength potion now works only in battle and applies a temporary attack buff.
- Room generation moved to percentage-based rolls for room-type balancing.
- Combat balance tuned with adjusted monster damage, potion healing values, and post-fight recovery.

### Fixed
- Potion name parsing now accepts singular/plural suffixes (`potion`/`potions`).
- Healing and greater-healing potions now cap HP at 100.
- Escape potion now checks stock, consumes on use, and requires active battle.

## [2026-02-21]
### Added
- Treasure rooms (`roll == 2`) that award random gold.
- Independent potion drop chances in treasure rooms (multiple potion types can drop in one room).
- Trap rooms (`roll == 3`) with independent trap checks and per-trap damage.
- Potion and trap probability tables on the `Player` model.

### Changed
- Game-over handling now runs in `main.py` after each command and exits when HP reaches 0.

## [2026-02-20]
### Added
- `enter` command wired into the command registry.
- Expanded room-entry flow for empty rooms, including stay/leave prompt and follow-up outcomes.
- Generic dice helpers: `Dice.roll(total)` and `Dice.rpg(total, success)`.
- Type hints for core player and dice methods.

### Changed
- Inventory rendering switched to a structured Rich `Table` inside a `Panel`.
- Command loop no longer clears the console before every command.

### Fixed
- Inventory output now consistently shows HP, gold, and potion counts.

## [2026-02-19]
### Added
- `main/player.py` with `Player` and `Dice` classes.
- Command system (`exit`, `i`) with command dispatch from the main loop.
- `main/console.py` shared Rich console instance.
- Project `.gitignore` for Python, tooling, IDE, and OS artifacts.
- Package marker: `main/__init__.py`.

### Changed
- Refactored `main/main.py` to use the extracted `Player` and shared console modules.
- Added interactive command loop with unknown-command handling.

## [2026-02-16]
### Added
- Initial project scaffold.
- `main/main.py` starter game entry point.
- `README.md`, `LISCENCE.md`, and `CHANGELOG.md`.
