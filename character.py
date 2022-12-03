from typing import List
import textwrap
import math
import numpy as np

from die import Die, D20, GWFDie
from monsters import (
    choose_ac,
    choose_constitution_modifier,
    choose_damage_dice,
    choose_hit_die,
    choose_initiative_bonus,
    choose_strength_modifier,
)


class Character:
    def __init__(
        self,
        name: str = None,
        level: int = 1,
        ac: int = None,
        strength_modifier: int = 0,
        constitution_modifier: int = 0,
        hit_die: tuple = None,
        damage_dice: tuple = None,
        initiative_bonus: int = 0,
    ) -> None:
        self.name = name if name is not None else "Anonymous"
        self.level = level
        self.ac = ac
        self.strength_modifier = strength_modifier
        self.damage_bonus = self.strength_modifier
        self.constitution_modifier = constitution_modifier
        self.initiative_bonus = initiative_bonus
        self._hit_die = hit_die
        self._damage_dice = damage_dice
        self.d20 = D20()

        self.roll_initiative()

    @property
    def hit_bonus(self):
        """
        The static modifier to add to to-hit rolls, based
        on a Character's level (by way of their proficiency bonus)
        and their strength modifier
        """
        proficiency_bonus = math.ceil(self.level / 4) + 1
        return self.strength_modifier + proficiency_bonus

    @property
    def damage_dice(self):
        """
        The die object used by the Character class to roll damage.
        """
        if not self._damage_dice:
            raise ValueError("No damage dice provided!")
        return Die(*self._damage_dice)

    @property
    def hit_die(self):
        """
        The die object used by the Character class to
        add Hit Points at each level up.
        """
        if not self._hit_die:
            raise ValueError("No hit die provided!")
        return Die(*self._hit_die)

    @property
    def hp(self):
        """
        The integer value of how much damage a Character can
        take before being defeated. This value is compared against a
        cumulative sum of damage rolls to determine the turn (the index
        of the damage roll array) on which the Character is defeated.
        """
        hp = (
            self.hit_die.sides  # level 1 HP
            + (self.hit_die.sum_roll(self.level - 1))  # all other levels' HP
            + (
                self.constitution_modifier * self.level
            )  # constitution bonus for every level
        )
        return hp

    def show_stats(self):
        stats = f"""
        ---Character---
        Name: {self.name}
        Level: {self.level}
        Hit Points: {self.hp}
        AC: {self.ac}
        Damage Dice: {self.damage_dice.display()}
        Hit Die: {self.hit_die.display()}
        Hit Bonus: {self.hit_bonus}
        Damage Bonus: {self.damage_bonus}
        Constitution Modifier: {self.constitution_modifier}
        Initiative: {self.initiative[0]}"""
        return textwrap.dedent(stats)

    def roll_initiative(self):
        """
        Generate a uniformly-distributed value with a=(1 + initiative bonus) and
        b=(20 + initiative bonus), to determine which character acts first.
        """
        self.initiative = self.d20.roll() + self.initiative_bonus

    def hit(
        self,
        target,
        rolls: int = 1,
        advantage: bool = False,
        disadvantage: bool = False,
    ) -> bool:
        """
        Roll a d20 to try to hit a target, and return an array of
        # of damage dice to roll for damage
        0 if miss or critical miss
        1 if hit
        2 if critical hit

        Parameters
        ----------
        target: Character
            the target of the attack
        rolls: int
            The number of times to roll, and the length of the resulting array
        advantage/disadvantage: bool
            Whether to roll twice and take the better/worse

        Returns
        -------
        is_hit: np.array
            Array of int values for whether the original array was a miss (0), hit (1), or critical hit (2).
            Corresponds to the number of damage dice to roll for the damage
        """
        # use this to check after calculating all to-hits whether or not
        # the natural roll was a 20 or 1, so we don't have to store the nat roll,
        # only the modified roll
        natural_20 = 20 + self.hit_bonus
        natural_1 = 1 + self.hit_bonus

        if advantage:
            roll_arr = self.d20.roll_with_advantage(rolls)
        elif disadvantage:
            roll_arr = self.d20.roll_with_disadvantage(rolls)
        else:
            roll_arr = self.d20.roll(rolls)
        # we have an array of d20 rolls
        roll_arr += self.hit_bonus

        hit_conditions = [
            roll_arr == natural_20,
            roll_arr == natural_1,
            roll_arr >= target.ac,
            roll_arr < target.ac,
        ]
        hit_results = [2, 0, 1, 0]

        hit_arr = np.select(hit_conditions, hit_results)
        return hit_arr

    def damage(self, hit_arr: np.array):
        """
        Construct array of damage rolls based on an input array of to-hit values

        hit_arr: np.array
            Array of the number of damage dice to roll
        args:
            Any damage modifiers

        Returns
        -------
        damage_arr: np.array
            Array of damage rolls
        """
        damage_roll = np.vectorize(
            lambda to_hit: self.damage_dice.sum_roll(to_hit)
            + (self.damage_bonus * to_hit)
        )
        damage_arr = damage_roll(hit_arr)
        return damage_arr

    def attack(
        self,
        target,
        rolls: int = 1,
        advantage: bool = False,
        disadvantage: bool = False,
    ):

        hit_arr = self.hit(target, rolls, advantage, disadvantage)
        damage_arr = self.damage(hit_arr)
        return damage_arr


class Barbarian(Character):
    def __init__(
        self,
        name: str = None,
        level: int = 1,
        ac: int = None,
        strength_modifier: int = 0,
        constitution_modifier: int = 0,
        damage_dice: tuple = None,
        initiative_bonus: int = 0,
        great_weapon_fighting: bool = False,
    ):
        super().__init__(
            name=name,
            level=level,
            ac=ac,
            # at level 20, barbarians get +2 to strength and constitiution modifiers
            strength_modifier=strength_modifier + (int(level == 20) * 2),
            constitution_modifier=constitution_modifier + (int(level == 20) * 2),
            hit_die=(12, 1),
            damage_dice=damage_dice,
            initiative_bonus=initiative_bonus,
        )
        self.damage_bonus += self.rage_bonus
        self.great_weapon_fighting = great_weapon_fighting

    @property
    def rage_bonus(self):
        levels = [self.level <= 8, 9 <= self.level <= 15, 16 <= self.level]
        bonus = [2, 3, 4]
        bonus = np.select(levels, bonus)
        return bonus

    @property
    def damage_dice(self):
        """
        Overloaded property to allow for optional use of
        the Great Weapon Fighting feat.
        """
        if not self._damage_dice:
            raise ValueError("No damage dice provided!")
        if self.great_weapon_fighting is True:
            return GWFDie(*self._damage_dice)
        else:
            return Die(*self._damage_dice)

    def damage(self, hit_arr: np.array):
        """
        Overloaded `damage` function for barbarian's, to utilize the
        Brutal Critical feature:
        "Beginning at 9th level, you can roll one additional
        weapon damage die when determining the extra damage for
        a critical hit with a melee attack.
        This increases to two additional dice at 13th level
        and three additional dice at 17th level."
        Construct array of damage rolls based on an input array of to-hit values

        hit_arr: np.array
            Array of the number of damage dice to roll
        args:
            Any damage modifiers

        Returns
        -------
        damage_arr: np.array
            Array of damage rolls
        """

        # brutal critical
        die_type = type(self.damage_dice)
        extra_die = die_type(self.damage_dice.sides, 1)
        # get a single extra damage die of the same type (Die or GWFDie) as
        # the character's normal damage dice

        # determine the number of extra damage dice to roll
        level_conditions = [
            self.level <= 8,
            9 <= self.level <= 12,
            13 <= self.level <= 16,
            17 <= self.level,
        ]
        extra_dice_rolls = [
            0,
            1,
            2,
            3,
        ]
        brutal_critical_extra_rolls = np.select(level_conditions, extra_dice_rolls)
        damage_roll = np.vectorize(
            lambda to_hit: self.damage_dice.sum_roll(to_hit)
            + (self.damage_bonus * to_hit)
            # whenever to_hit==2, add 0-3 extra single damage die
            # (e.g., damage dice of 2d6 gives an extra 1d6 roll) rolls
            + (max(0, to_hit - 1) * extra_die.sum_roll(brutal_critical_extra_rolls))
        )
        damage_arr = damage_roll(hit_arr)
        return damage_arr


class Monster(Character):
    def __init__(
        self,
        name: str = "Monster",
        cr: int = None,
        ac: int = None,
    ) -> None:
        super().__init__(
            name,
            hit_die=choose_hit_die(cr),
            ac=ac if ac is not None else choose_ac(cr),
            strength_modifier=choose_strength_modifier(cr),
            initiative_bonus=choose_initiative_bonus(cr),
            damage_dice=choose_damage_dice(cr),
            constitution_modifier=choose_constitution_modifier(cr),
        )
        self.cr = cr
        self.level = self.cr
