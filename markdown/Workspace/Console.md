# `Console`

## Classes

### `console(self, master, font)`



#### Methods

##### `__init__(self, master, font)`

Initialize self.  See help(type(self)) for accurate signature.

##### `__str__(self)`

str(s) -> string 

##### `canvas_mouseclick(self, event)`

Forces the text to align itself and gives focus to the console 

##### `canvas_mousedrag(self, event)`

Changes selection 

##### `clear(self)`

Clears the console 

##### `drag_mouseclick(self, event)`

Allows the user to resize the console height 

##### `draw_arrow(self, start_x, start_y, width, colour, direction, degree=45)`

Works out the line to draw at 45 degrees, returns the x and y of the end
of the line. Direction should be a string, "up" or "down" 

##### `draw_logo(self)`

Draws the red and green lines in the bg of the console.
Future versions will have randomly created lines & possibly
animated.

##### `hide(self)`

Removes console from interface 

##### `move_text(self, delta)`

Moves the text up (negative) or down (positive) 

##### `read(self)`

Returns contents of the console widget 

##### `update_scrollbar(self, point=None)`

point should be a value between 0 and 1.0 

##### `write(self, string)`

Adds string to the bottom of the console 

---

## Functions

## Data

