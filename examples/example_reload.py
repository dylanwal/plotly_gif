from plotly_gif import GIF

# If you have a folder of pngs you can quickly remake a gif with different settings.

# using default file location "./examples/gif_imgs"
gif = GIF(mode="png",  verbose=True)
gif.create_gif(length=500)
