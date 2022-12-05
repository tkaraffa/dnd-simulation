# dnd-simulation

This repository contains primarily exploratory simulations, focused in addressing several common dichotomies facing the Dungeons and Dragons player.

These questions include:
* should a character use a shield (harder to be hit, slightly lower damage), or two-hand their weapon (easier to be hit, slightly higher damage)?
* should a character use a greatsword (more consistent, slightly higher damage) or a greataxe (more variable, slightly lower damage), given the presence or absence of certain abilities

Files are split by simulation into subdirectories:
* `greatsword_vs_greataxe/`
* `shield_vs_two_hand/`

Additionally, classes and utility functions are organized into self-titled files:

* `die.py`
* `character.py`
* `utils.py`

## Usage

Usage is preferably done through Docker Compose, with the following commands:

```sh
docker-compose build dnd-simulation
```

```sh
docker-compose run --rm dnd-simulation <path/to/file>
```

Files are run from the container's top-level directory, `src/`. For example: 

```sh
docker-compose run --rm dnd-simulation greatsword_vs_greataxe/gwf.py
```

If Docker is unavailable or not preferred, the same functionality can be achieved through a local Python environment. The container is based on Python 3.8.10. It is recommended to use this version to ensure package compatability.

```
virtualenv dnd-simulation -p /path/to/python3.8.10
cd dnd-simulation
pip install --user -r requirements.txt
```

## General-Purpose Files

### die.py

This file contains several classes for rolling dice. The standard `Die` class is initialized with a number of sides and a number of die; thus Die(6, 2) provides the equivalent of 2d6, or 2 6-sided dice. The class contains methods for creating an array of rolls, as well as summing and averaging that array. The `D20` class contains methods for rolling with advantage or disadvantage. The `GWFDie` class is a special die with the ability to reroll 1s and 2s on each of its dice.

### character.py

This file contains several classes for simulating characters, with attributes such as `ac` (Armor Class), `strength_modifier`, and `hit_die`. The `Character` class is a general-purpose class with the most parameters available for specification. The `Monster` class is more specialized, as it randomly generates the statistics of the monster based on its `cr` (Challenge Rating) parameter. The `Barbarian` class uses an overloaded `damage` method, which incorporates the Brutal Critical ability, as well as an overloaded `damage_dice` attribute, which optionally allows for the Great Weapon Fighting feat.

### utils.py

This file contains utility functions for generating character statistics based on a character's level, and for simulating a fight between two characters.

## Two-Hand vs Shield

The simulation script `shield_vs_two_hand/shield_battle.py` simulates two characters fighting across levels 1-20. It also simulates these same characters fighting a monster. Finally, it generates a visualization of the results of these types of fights.

## Greatsword vs Greataxe

All scripts for this simulation are contained in the `greatsword_vs_greataxe/` directory. `gwf.py` visualizes the comparison between the 4 combinations of a greatsword/greataxe with/without the Great Weapon Fighting feat. `gwf_bc.py` incorporates the previous comparison, but includes the previously-used damage dice as a Barbarian's. This simulation measures the effectiveness of each combination of feat/ability/weapon at different levels and against different ACs.
