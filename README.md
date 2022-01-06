# Plotly-gif 

---
---

A simple python package to generate .gif from your plotly figures. It works for both 2D and 3D figures. It can even 
create_gif motion for you in 3D plots. 

## Installation

```
pip install plotly-gif
```

### Dependencies

If you are already using plotly, then you should be good. But, just in case, these are the dependencies:
```python
pip install numpy
pip install plotly    
pip install kaleido   # used by plotly to generate png
pip install Pillow    # used to convert png to gif
```    

---
## Usage

There are three common methods:

### Built-in Functions



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
## Options


---1
## Examples

