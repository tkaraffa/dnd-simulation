import math
import numpy as np
from character import Character


def generate_character_stats(level: int, hit_die: int) -> dict:
    """
    Generate dict of random variables to use as Character statistics.

    Parameters
    ----------
    level: int
        The level of the character, which corresponds
        to their relative strength
    hit_die: int
        The number of sides of the die to roll
        when gaining hit points at level up


    Returns
    -------
    stats: dict
        Appropriately-named dict of stats
        to pass into a Character object
    """
    levels = [
        1 <= level < 4,
        4 <= level < 6,
        6 <= level < 8,
        8 <= level < 12,
        12 <= level < 14,
        14 <= level,
    ]
    apis = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (2, 3)]
    modifiers = np.select(levels, apis)
    # by the time you get to level 14, if you've exclusively been
    # putting apis into str or con, they will both be 20,
    # and so we don't need to track the two beyond 14th level

    # technically you get 2 points,
    # but it rarely makes sense to use them for anything
    # besides increasing your modifier by 1,
    # so we'll just call it a +1

    # assume the character starts with a +3 strength modifier
    # and a +2 constitution modifier, i.e., a 16 strength and 14 constitution
    # these are standard choices for a strength-based fighter
    # also assume the character progresses alternatingly, i.e.,
    # at level 4, adds +1 to str modifier, at level 6, adds
    # +1 to con modifier, alternating until level 12,
    # then finishing off con to +5 at level 14

    str_modifier = 3 + modifiers[0]
    con_modifier = 2 + modifiers[1]

    stats = dict(
        level=level,
        strength_modifier=str_modifier,
        constitution_modifier=con_modifier,
        hit_die=(hit_die, 1),
    )

    return stats


def find_defeat_index(target: Character, damage_arr: np.ndarray) -> int:
    """
    Find the index at which the cumulative damage from an array
    of damage rolls exceeds the hp of the target

    Parameters
    ----------
    target: Character
        The target whose hp to use to calculate defeat
    damage_arr: np.ndarray
        The array of damage rolls

    Returns
    -------
    defeat_index: int
        The index of the damage array
    """
    total_damage_arr = np.cumsum(damage_arr)
    if total_damage_arr[-1] < target.hp:
        return len(damage_arr)
    defeat_index = (total_damage_arr >= target.hp).argmax()
    return defeat_index


def fight(char1: Character, char2: Character, rolls: int = 500) -> str:
    """
    Simulate a single one-on-one fight between two Characters.

    Parameters
    ----------
    char1: Character
    char2: Character
    rolls: int = 500
        The number of rounds for a single fight
        Should be long enough to ensure one character wins

    Returns
    -------
    winner: str
        The name of the winner
        If neither Character was reduced to 0 hit points in the
        provided number of rounds, returns "Tie"
    """
    char1_damage_arr = char1.attack(char2, rolls)
    char2_damage_arr = char2.attack(char1, rolls)

    char1_defeated_at = find_defeat_index(char1, char2_damage_arr)
    char2_defeated_at = find_defeat_index(char2, char1_damage_arr)
    if rolls == char1_defeated_at == char2_defeated_at:
        winner = "Tie"
    while char1.initiative == char2.initiative:
        char1.roll_initiative()
        char2.roll_initiative()
    if char1.initiative > char2.initiative:
        first = char1_damage_arr
        second = char2_damage_arr
    else:
        first = char2_damage_arr
        second = char1_damage_arr

    if (char1_defeated_at > char2_defeated_at) or (
        char1.initiative > char2.initiative and char1_defeated_at == char2_defeated_at
    ):
        winner = char1.name
    elif (char2_defeated_at > char1_defeated_at) or (
        char2.initiative > char1.initiative and char2_defeated_at == char1_defeated_at
    ):
        winner = char2.name
    return winner


def create_chart(
    results: dict,
    colors: dict,
    title: str,
    filename: str,
    replications: int,
):
    """
    Create a bar chart to track simulation results

    Paramters
    ---------
    results: dict
        Dictionary of results from simulation
    colors: dict
        Dictionary of colors for names of characters
    title: str
        Title for the chart
    filename: str
        Name of the file for the chart
    replications: int
        Number of replications used in the simulation
    """

    # list comprehensions are hard
    chart_data = []
    for level in results:
        chart_data.extend(
            go.Bar(
                x=[str(level)],
                y=[result],
                name=name,
                marker_color=colors.get(name),
                texttemplate="%{y}",
                textposition="inside",
                textangle=0,
                showlegend=False,
            )
            for name, result in zip(results[level][0], results[level][1])
        )

    fig = go.Figure(data=chart_data)
    # add in dummy data for legend
    for name in colors:
        fig.add_trace(
            go.Bar(
                name=name,
                marker_color=colors.get(name),
                y=[0],
                visible="legendonly",
            )
        )
    fig.add_hline(y=replications / 2)
    fig.update_layout(
        width=800,
        height=400,
        barmode="stack",
        xaxis_title="Level",
        yaxis_title="Replications",
        title={
            "text": title,
            "xanchor": "center",
            "yanchor": "top",
            "y": 0.85,
            "x": 0.5,
        },
    )
    fig.write_image(filename)
