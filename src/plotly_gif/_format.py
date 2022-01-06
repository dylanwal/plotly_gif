# Just trying to make the plots look nice!! :)
layout = {
        "autosize": False,
        "width": 800,
        "height": 600,
        "showlegend": False,
        "font": dict(family="Arial", size=18, color="black"),
        "plot_bgcolor": "white"
}

xaxis = {
    "title": "<b>X<b>",
    "tickprefix": "<b>",
    "ticksuffix": "</b>",
    "showline": True,
    "linewidth": 5,
    "mirror": True,
    "linecolor": 'black',
    "ticks": "outside",
    "tickwidth": 4,
    "showgrid": False,
    "gridwidth": 1,
    "gridcolor": 'lightgray'
}

yaxis = {
    "title": "<b>Y<b>",
    "tickprefix": "<b>",
    "ticksuffix": "</b>",
    "showline": True,
    "linewidth": 5,
    "mirror": True,
    "linecolor": 'black',
    "ticks": "outside",
    "tickwidth": 4,
    "showgrid": False,
    "gridwidth": 1,
    "gridcolor": 'lightgray'
}

fig.update_layout(layout)
fig.update_xaxes(xaxis)
fig.update_yaxes(yaxis)