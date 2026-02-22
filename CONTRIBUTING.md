# Contributing

Thanks for contributing to Dungeon Dice.

## Ground Rules

- Keep changes focused and small.
- Prefer readable gameplay logic over clever abstractions.
- Update `CHANGELOG.md` for user-visible changes.
- Keep command behavior consistent with existing CLI style.

## Setup

1. Install dependencies:

```bash
python -m pip install rich
```

2.Run the game:

```bash
python -m main.main
```

3.Run a syntax check before opening a PR:

```bash
python -m py_compile main/main.py main/player.py main/console.py
```

## Branches

- Create a feature branch from `main`.
- Suggested naming:
  - `feature/<short-topic>`
  - `fix/<short-topic>`
  - `docs/<short-topic>`

## Commits

- Use clear, imperative commit messages.
- Examples:
  - `Add monster fight reward healing cap`
  - `Fix potion command parsing for plural input`
  - `Update README and contributing docs`

## Pull Requests

Include:

- What changed
- Why it changed
- How you tested it
- Any balance impacts (damage, drop rates, room odds)

If UI text changed, include a short terminal output snippet.

## Code Style

- Follow existing formatting style in `main/player.py` and `main/main.py`.
- Keep methods short when possible.
- Reuse shared checks and early returns to reduce nested conditionals.

## Gameplay Balance Changes

When changing room odds, monster stats, or potion values:

- Explain expected gameplay impact.
- Share before/after values.
- Verify the game still feels survivable in early runs.

## Reporting Issues

When filing bugs, include:

- Command(s) used
- Expected behavior
- Actual behavior
- Relevant terminal output
