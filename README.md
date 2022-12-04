# dnd-simulation

This repository contains primarily exploratory simulations, focused in addressing several common dichotomies facing the Dungeons and Dragons player.

These questions include:
* should a character use a shield, or two-hand their weapon?
* should a character use a greatsword (more consistent, average damage) or a greataxe (more variable damage), given the presence or absence of certain abilities

Files are split by simulation into subdirectories:
* `greatsword_vs_greataxe/`
* `shield_vs_two_hand/`

## Usage

`docker-compose run --rm dnd-simulation <path/to/file>`


### Example

`docker-compose run --rm dnd-simulation greatsword_vs_greataxe/gwf.py`