"""
This simulation seeks to address the question: should you use a greatsword or a greataxe?
A greatsword's damage dice are 2d6, while a greataxe's is 1d12.

In this simulation, we will investigate the case of a Barbarian class 
using each weapon. Importantly, the Barbarian gains the feature:
Brutal Critical
"Beginning at 9th level, you can roll one additional 
weapon damage die when determining the extra damage for a critical hit with a melee attack.
This increases to two additional dice at 13th level and three additional dice at 17th level."

All other parameters will be held equal for the duelling characters - 
level is scaled equally, with hit bonus, damage bonus, AC, and other
stat modifiers increasing linearly with level. The hit die is set as 1d12,
which is native to the Barbarian class.
Statistics may vary slightly, due to random variable generation; e.g., 
even though the characters both use the same hit die, each level 
involves rolling the hit die and adding its value to the characters
total Hit Points, so if one character consistently rolls well and 
the other does not, their Hit Points will differ significantly.

Each replication will have its own random variables - the rolls on Hit Points at
each level up, the to-hit rolls, and the damage rolls. These will be averaged
across all replications to provide a sample mean of wins/losses that approaches
the true mean of wins/losses by the Central Limit Theorem.

Each set of parameters (level, hit die, and AC) will be considered its own 
simulation, with the outputs averaged within that simulation only. However, 
in the overarching analysis, all simulations will be considered cohesively.
"""
import os
import math

import numpy as np
from plotly import graph_objects as go

from die import Die
from character import Character, Monster
from utils import find_defeat_index, fight, generate_fighter_stats, create_chart


def main():
    REPLICATIONS = 10_000
    levels = range(1, 21)
    hit_die = 10
    char_fight_results = dict()
    longsword_mon_fight_results = dict()
    shield_mon_fight_results = dict()

    images_directory = os.path.join(os.path.dirname(__file__), "images")

    for level in levels:
        # assume both players have equal AC, which increases by 1 every 4 levels
        # up to a non-shield value of 22 at level 20
        ac = 17 + math.floor(level / 4)
        shared_stats = generate_fighter_stats(level)
        longswordington = Character(
            name="Longswordington",
            **shared_stats,
            ac=ac,
            damage_dice=(10, 1),
        )
        shieldsworth = Character(
            name="Shieldsworth",
            **shared_stats,
            ac=ac + 2,
            damage_dice=(8, 1),
        )
        monster = Monster(
            name="Zombie",
            cr=level,
        )

        char_fight_results[level] = np.unique(
            [
                fight(
                    longswordington,
                    shieldsworth,
                )
                for _ in range(REPLICATIONS)
            ],
            return_counts=True,
        )
        longsword_mon_fight_results[level] = np.unique(
            [
                fight(
                    longswordington,
                    monster,
                )
                for _ in range(REPLICATIONS)
            ],
            return_counts=True,
        )
        shield_mon_fight_results[level] = np.unique(
            [
                fight(
                    shieldsworth,
                    monster,
                )
                for _ in range(REPLICATIONS)
            ],
            return_counts=True,
        )

    tie = {"Tie": "green"}
    ls = {"Longswordington": "blue"}
    sh = {"Shieldsworth": "red"}
    mon = {"Zombie": "purple"}
    char_fight_colors = {**tie, **ls, **sh}
    longsword_mon_fight_colors = {**tie, **ls, **mon}
    shield_mon_fight_colors = {**tie, **sh, **mon}

    # create_chart(
    #     char_fight_results,
    #     char_fight_colors,
    #     "Longswordington vs Shieldsworth",
    #     os.path.join(images_directory, "shield_battleXXX.png"),
    #     REPLICATIONS,
    # )
    # create_chart(
    #     longsword_mon_fight_results,
    #     longsword_mon_fight_colors,
    #     "Longswordington vs Monster",
    #     os.path.join(images_directory, "ls_mon.png"),
    #     REPLICATIONS,
    # )
    # create_chart(
    #     shield_mon_fight_results,
    #     shield_mon_fight_colors,
    #     "Shieldsworth vs Monster",
    #     os.path.join(images_directory, "sh_mon.png"),
    #     REPLICATIONS,
    # )


if __name__ == "__main__":
    main()
