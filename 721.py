import os
import sys
import urllib.error
import urllib.request
from configparser import ConfigParser, ParsingError, NoSectionError

import pyglet
from pyglet.util import debug_print
from pyglet.math import Mat4, Vec3

# Set up the debugging flag calls.
_debug_flag = len(sys.argv) > 1 and sys.argv[1] in ('-D', '-d', '--debug')
_debug_print = debug_print(_debug_flag)
_debug_print("Debugging Active")

# Load the images from the /theme folder.
pyglet.resource.path.append("theme")
pyglet.resource.reindex()
_debug_print("Theme Loaded")

# Start the main window

window = pyglet.window.Window(1280, 720, caption="721", resizable=True, vsync=True)
window.set_icon(pyglet.resource.image("icon.png"))
config = ConfigParser()
config.add_section('layout')
config.add_section('images')
_debug_print("Main window created")

# Set the (x,y) parameters for where certain elements should be displayed.
_layout = {
    "icon": (640, 360),

}
_debug_print("Layout loaded.")

# Connect the image file names to their definitions.
_images = {
    'icon': 'icon.png',

}

def load_configuration():
    # Load the button mapping configuration.
    global _layout, _images
    layout = _layout.copy()
    images = _images.copy()

    with pyglet.resource.file('layout.ini', 'r') as file:
        loaded_configs = config.read(file.name)

    if not loaded_configs:
        _debug_print("No valid layout.ini found. Falling back to default.")
        return

    try:
        for key, value in config.items('layout'):
            x, y = value.split(', ')
            layout[key] = int(x), int(y)

        for key, value in config.items('images'):
            images[key] = value

        _layout = layout.copy()
        _images = images.copy()

    except (KeyError, ParsingError, NoSectionError):
        _debug_print("Invalid theme/layout.ini. Falling back to default.")



class SceneManager:
    """A Scene Management class.

    The SceneManager is responsible for switching between
    the various scenes cleanly.

    """
    def __init__(self, window_instance):
        self.window = window_instance
        self.window.push_handlers(self)

    def enforce_aspect_ratio(self, dt):
        # Enforce aspect ratio by readjusting the window height.
        aspect_ratio = 1.641025641
        target_width = int(window.height * aspect_ratio)
        target_height = int(window.width / aspect_ratio)

        if self.window.width != target_width and self.window.height != target_height:
            self.window.set_size(window.width, target_height)
            
# Window Events:

def on_draw(self):
    self.window.clear()
    self._current_scene.batch.draw()

def on_resize(self, width, height):
    projection_matrix = Mat4.orthogonal_projection(0, width, 0, height, 0, 1)
    scale_x = width / 1280.0
    scale_y = height / 720.0
    self.window.projection = projection_matrix.scale(Vec3(scale_x, scale_y, 1))
    self.window.viewport = 0, 0, width, height
    return pyglet.event.EVENT_HANDLED


if __name__ == "__main__":
    load_configuration()

    scene_manager = SceneManager(window_instance=window)
    # Enforce aspect ratio by readjusting the window height.
    pyglet.clock.schedule_interval(scene_manager.enforce_aspect_ratio, 0.3)
    pyglet.app.run()