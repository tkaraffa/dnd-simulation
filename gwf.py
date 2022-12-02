import os
from collections import OrderedDict
from die import Die, GWFDie
import plotly.graph_objects as go

replications = 100_000
params = list(zip(["Vanilla", "Great Weapon Fighting"], [Die, GWFDie]))
greatsword = {
    f"{name}\n{die_type(6, 2).display()}": die_type(6, 2).avg_roll(replications)
    for name, die_type in params
}
greataxe = {
    f"{name}\n{die_type(12, 1).display()}": die_type(12, 1).avg_roll(replications)
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
fig.write_image(os.path.join(os.path.dirname(__file__), "images", "sword_axe.png"))
