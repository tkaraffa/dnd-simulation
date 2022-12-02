import math
import numpy as np
import itertools
from die import Die, D20
from character import Character
from utils import find_defeat_index


# what is the expected value of a normal attack
# vs a power attack
# vs a FF power attack?
# How much are the two feats actually worth?

# assume a two-handed str weapon, since that's
# usually what you'd use with PA

REPLICATIONS = 10000

DAMAGE_DICE = [(6, 2), (12, 1)]

# randomize to-hit/str bonii - normal distr
# randomize ACs - normal distr

stats = dict(name="1", hp=500, ac=17, damage_dice=(6, 2))
stats2 = dict(name="2", hp=500, ac=17, damage_dice=(6, 2))
c = Character(**stats)
t = Character(**stats2)


def fight(char1, char2, rolls=10):
    char1_damage_arr = char1.attack(char2, rolls)
    char2_damage_arr = char2.attack(char1, rolls)

    char1_defeated_at = find_defeat_index(char1, char2_damage_arr)
    char2_defeated_at = find_defeat_index(char2, char1_damage_arr)
    if rolls == char1_defeated_at == char2_defeated_at:
        return "Tie"
    while char1.initiative == char2.initiative:
        char1.roll_initiative()
        char2.roll_initiative()
    if char1.initiative > char2.initiative:
        first = char1_damage_arr
        second = char2_damage_arr
    else:
        first = char2_damage_arr
        second = char1_damage_arr

    # last_turn = str(1 + min([char1_defeated_at, char2_defeated_at]))
    if (char1_defeated_at > char2_defeated_at) or (
        char1.initiative > char2.initiative and char1_defeated_at == char2_defeated_at
    ):
        return char1.name
    elif (char2_defeated_at > char1_defeated_at) or (
        char2.initiative > char1.initiative and char2_defeated_at == char1_defeated_at
    ):
        return char2.name


winner = fight(t, c, rolls=10000)
print(winner)
