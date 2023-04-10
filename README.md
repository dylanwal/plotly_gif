# Plotly-gif 

---
---
![PyPI](https://img.shields.io/pypi/v/plotly_gif)
![downloads](https://img.shields.io/pypi/dm/plotly_gif)
![license](https://img.shields.io/github/license/dylanwal/plotly_gif)

A simple python package to generate .gif from your plotly figures. It works for both 2D and 3D figures. It can even 
create_gif motion for you in 3D plots. 

## Installation

```
pip install plotly-gif
```

### Dependencies

If you are already using plotly, then you should be good. But, just in case, these are the dependencies:
* [plotly](https://github.com/plotly/plotly.py) (5.9.0)
  * Plots molecules
* [kaleido](https://github.com/plotly/Kaleido)  (0.1.0post1)
  * Converts plotly graphs to images (png, svg, etc.)
  * I am not using the most recent version of kaleido as it does not play nice with my computer. Try the newest 
    version, but if you are having issues install this specific version.
* [Pillow](https://github.com/python-pillow/Pillow) (9.2.0)
  * Used to convert png to gif.
* [numpy](https://github.com/numpy/numpy) (1.23.1)
  * Used for math
  
    
---
## Usage

There are three common methods:

### Built-in Functions/ Macros
Currently, we have the follow:
* two_d_time_series
* three_d_scatter_rotate
* more to come... or submit your own

```python
import plotly.graph_objs as go
from plotly_gif import GIF, two_d_time_series

fig = go.Figure()
# add your traces()
# add your formatting()

gif = GIF()
two_d_time_series(gif, fig)

```




### Decorator

If you have a function that is changing the `go.Figure' with each loop, you can add the decorator to the func.

```python
import plotly.graph_objs as go
from plotly_gif import GIF, capture

gif = GIF()

@capture(gif)
def plot_(x_, y_):
    fig = go.Figure()
    # add your traces()
    # add your formatting()
    
    return fig

gif.create_gif() # generate gif
```

### In-Line
This very similar to the decorator option, but you can call the image capture function directly.

```python
import plotly.graph_objs as go
from plotly_gif import GIF, capture

gif = GIF()

def plot_(x_, y_):
    fig = go.Figure()
    # add your traces()
    # add your formatting()
    
    gif.create_image(fig)  # create_gif image for gif
    
    return fig

gif.create_gif() # generate gif
```

---
## Examples
See examples folder

![2d gif](https://github.com/dylanwal/plotly_gif/blob/master/examples/gifs/example_1.gif)


![3d gif](https://github.com/dylanwal/plotly_gif/blob/master/examples/gifs/example_3.gif)



### Time to generate gif (60 images per gif)
* Simple 2D plots with small data sets (100 pts): ~10 sec
* Simple 3D plots with small data sets (100 pts): ~1.5 min