"""
Compare 2d6 and 1d12 damage dice with and without the 
Great Weapon Fighting feat, which allows 1s and 2s to be 
rerolled once.
"""

import os
from collections import OrderedDict
from die import Die, GWFDie
import plotly.graph_objects as go
from utils import images_directory


def main():
    replications = 100_000
    params = list(zip(["Vanilla", "Great Weapon Fighting"], [Die, GWFDie]))
    greatsword = {
        f"{name}\n{die_type(6, 2).display()}": die_type(6, 2).avg_roll(replications)
        for name, die_type in params
    }
    greataxe = {
        f"{name} - {die_type(12, 1).display()}": die_type(12, 1).avg_roll(replications)
        for name, die_type in params
    }

    data = OrderedDict(**greatsword, **greataxe)
    fig = go.Figure(
        go.Bar(
            x=list(data.keys()),
            y=list(data.values()),
            texttemplate="%{y}",
            textposition="inside",
        )
    )
    fig.update_layout(
        xaxis_title="Weapon",
        yaxis_title="Average Damage",
        width=800,
        height=400,
    )
    fig.write_image(os.path.join(images_directory, "sword_axe.png"))


if __name__ == "__main__":
    main()
