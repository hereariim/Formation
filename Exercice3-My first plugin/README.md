# Plugin

## Template to create plugin

This plugin is generated using the official napari plugin template. **This command creates a Python package containing all files required for a napari plugin.**

```
(formation) user1> pip install copier jinja2-time npe2
(formation) user1> copier copy --trust https://github.com/napari/napari-plugin-template formation

Welcome to the napari plugin template!
This template will help you create a new napari plugin with all the necessary structure of a Python package. 

For more detailed information about each prompt, see:
https://github.com/napari/napari-plugin-template/blob/main/PROMPTS.md

🎤 The name of your plugin, used to name the package and repository (no space!)
   formation
🎤 Display name for your plugin in the napari GUI
   Formation
🎤 Plugin module name, usually the same as the name of the package, but lowercase and with underscores
   formation
🎤 Short description of what your plugin does
   Segmentation of cells
🎤 Email address
   formation@france.fr
🎤 Developer name
   Imhorphen
🎤 Github user or organisation name
   imhorphen
🎤 Github repository URL
   https://github.com/Imhorphen/formation
🎤 Include reader plugin?
   No
🎤 Include writer plugin?
   No
🎤 Include sample data plugin?
   No
🎤 Include widget plugin?
   Yes
🎤 Install pre-commit? (Code formatting checks)
   Yes
🎤 Install dependabot? (Automatic security updates of dependency versions)
   Yes
🎤 Which licence do you want your plugin code to have?
   BSD-3

Select license:
1 - BSD-3
2 - MIT
3 - Mozilla Public License 2.0
4 - Apache Software License 2.0
5 - GNU LGPL v3.0
6 - GNU GPL v3.0
Choose from 1, 2, 3, 4, 5, 6 (1, 2, 3, 4, 5, 6) [1]: 1
```

## Installation du plugin

```
(formation) user1> cd formation
(formation) user1/formation> pip install -e .
```

## widget.py and magic_factory

Contains the function used by the plugin. The widget is created using magicgui, which automatically generates a graphical interface from a Python function.

1- magic_factory is napari decorator to show an user interface to interact with python function.

magic_factory converts the Python function into a napari widget.

- ImageData specifies that the input is an image layer

- LabelsData specifies that the output is a segmentation mask

- call_button creates the button in the GUI


```
from magicgui import magic_factory
from napari.types import ImageData, LabelsData

# Model and Weight

@magic_factory(call_button="Run UNet")
def unet_segmentation(
    image: ImageData,
) -> LabelsData:
   # import image and inference
   pred = ...
   return pred
```
2- Copy and paster code in ``unet_segmentation`` notebook.ipynb in widget.py

## __init__.py

Exports the widget function ``unet_segmentation`` so napari can access it.

```
from ._widget import (
    unet_segmentation,
)

__all__ = (
    'unet_segmentation',
)
```

## napari.yaml

Registers the plugin inside napari.

```
contributions:
  commands:
    - id: formation.make_qwidget
      python_name: formation:unet_segmentation
      title: Segmentation
  widgets:
    - command: formation.make_qwidget
      display_name: Segmentation
  menus:
    napari/layers/segment:
      - command: formation.make_qwidget
```

This configuration tells napari:

- which function to run

- where the widget appears in the interface

- how the plugin is displayed in the menu.

## Dependencies and pyproject.toml

The plugin relies on the following libraries:
``` 
torch
torchvision
```
They are declared in pyproject.toml.