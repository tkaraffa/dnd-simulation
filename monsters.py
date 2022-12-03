"""
Utility functions for randomly generating the statistics of a Monster class object.
Only a CR is provided on initialization - every function which is used during
object construction uses this integer value to create a normally-distributed
random variable and uses it to select an integer value that can then be
used by the Monster object.
"""
from typing import Tuple
import numpy as np
import itertools
from collections import OrderedDict
from die import Die


def _choose_value(cr: int, options: list, factor: int = 1, scale: int = 1):
    """
    Prototypical function for choosing values based
    on CR. Choose a rounded, triangularly-distributed value
    that is roughly centered on CR, and index the ordered options with
    that value to produce an output.
    Bottom value is bounded by either 0 or CR - 5
    Top value is bounded by either CR + 5 or max index of options
    Mode is the scaled CR, which is obtained by dividing the CR
    by the maximum CR (20) and multiplying by the maximum value of
    the distribution (the length of the list of options).
    With the above parameters, as CR increases, so does the mode, and
    potentially the bottom and top bounds.
    E.g., with input options = [1, 2, 3, 4, 5, 6, 7], a higher CR will
    more often produce an index of [6], which corresponds to
    a value of 3. A lower CR will more oftten produce an index
    of [0], which corresponds to a value of 1. A CR of 20 will
    have bounds (5, 6, 6), which will most often result in returning
    an index of [6], and the corresponding value of 7.

    Parameters
    ----------
    cr: int
        The mean of the normal distribution
    options: list
        Ordered list of choices for the output
    factor: int
        The scaling factor to divide the normal RV by before
        rounding to get the index - higher generally results in
        a lower final value
    scale: int
        The standard deviation of the normal distribution
    """
    max_cr = 20
    cr_range = 5
    if cr > max_cr:
        raise NotImplementedError("Only up to CR 20 is supported!")
    # add max possible value of CR+5
    max_value = min(len(options) - 1, cr + cr_range)
    # add min possible value of CR-5, and force to be below max_value to be a valid Triangular distribution
    min_value = min(max(0, cr - cr_range), max_value - 1)
    # force the mode's boundaries to be inclusively between max and min values
    mode_value = max(min(cr * max_value / max_cr, max_value), min_value)
    index = round(np.random.triangular(min_value, mode_value, max_value))
    return options[index]


def choose_hit_die(cr: int) -> Tuple[int, int]:
    """
    Randomly choose a Hit Die (the Die to use to roll for HP increase
    at each level up).
    """
    hit_die_options = [(i, 1) for i in [6, 8, 10, 12]]
    hit_die = _choose_value(cr, hit_die_options, factor=3, scale=2)
    return hit_die


def choose_constitution_modifier(cr: int) -> int:
    """
    Randomly choose a constitution modifier (the static value
    added to a Character's HP at each level up).
    """
    constituion_modifier_options = list(range(-2, 8))
    constituion_modifier = _choose_value(
        cr, constituion_modifier_options, factor=3, scale=2
    )
    return constituion_modifier


def choose_strength_modifier(cr: int) -> int:
    """
    Randomly choose a strength modifier (the static value
    added to a Character's to-hit and damage rolls).
    """
    strength_modifier_options = list(range(-2, 8))
    strength_modifier = _choose_value(cr, strength_modifier_options, factor=3, scale=2)
    return strength_modifier


def choose_ac(cr: int) -> int:
    """
    Randomly choose an Armor Class (the value used to determine
    whether or not an attack against it hits (to-hit>=AC) or
    misses (to-hit<AC)).
    """
    ac_options = list(range(10, 22))
    ac = _choose_value(cr, ac_options, factor=5, scale=2)
    return ac


def choose_initiative_bonus(cr: int) -> int:
    """
    Randomly choose an initiative bonus (the static value added
    to a d20 roll to determine which character goes first in a round).
    """
    initiative_bonus_options = list(range(-2, 9))
    initiative_bonus = _choose_value(cr, initiative_bonus_options, factor=2, scale=1)
    return initiative_bonus


def choose_hit_bonus(cr: int) -> int:
    """
    Randomly choose a hit bonus (the static value added to a d20
    attack roll to determine whether or not an attack hits (to-hit>=AC)
    or misses (to-hit<AC)).
    """
    hit_bonus_options = list(range(-2, 10))
    hit_bonus = _choose_value(cr, hit_bonus_options, factor=2, scale=2)
    return hit_bonus


def choose_damage_bonus(cr: int) -> int:
    """
    Randomly choose a damage bonus (the static value added to a damage roll
    to determine how much damange is dealt to the target on a successful hit).
    """
    damage_bonus_options = list(range(-2, 7))
    damage_bonus = _choose_value(cr, damage_bonus_options, factor=2, scale=2)
    return damage_bonus


def choose_damage_dice(cr: int) -> Tuple[int, int]:
    """
    Choose the damage dice of a monster based on its CR
    Damage dice will be normally distributed around the index
    that corresponds to the input CR.
    Do some fancy ordering based on the expected value of each
    dice tuple.

    Parameters
    ----------
    cr: int
        The CR of the monster for whom to choose damage dice

    Returns
    -------
    damage_dice: tuple(int, int)
        The tuple of damage dice
    """

    damage_dice_options = itertools.product([4, 6, 8, 10, 12], [1])

    unordered_dice = {
        damage_dice: Die(*damage_dice).expected_value
        for damage_dice in damage_dice_options
    }
    ordered_dice = OrderedDict(
        {
            die: expected_value
            for die, expected_value in sorted(
                unordered_dice.items(), key=lambda item: item[1]
            )
        }
    )
    damage_dice = _choose_value(cr, list(ordered_dice), factor=4, scale=1)
    return damage_dice
