# `FoxDot.lib.Workspace.Editor`

Tkinter interface made for Live Coding with Python syntax highlighting 

## Classes

### `workspace(self, CodeClass)`



#### Methods

##### `backspace(self, event=None, insert=insert)`

Deletes a character or selected area 

##### `check_namespace(self)`

Sets the label 

##### `colour_line(self, line)`

Checks a line for any tags that match regex and updates IDE colours 

##### `delete(self, event=None, insert=insert)`

Delete the next character 

##### `delete_selection(self)`

If an area is selected, it is deleted and returns True 

##### `delete_word(self, event)`

Deletes the preceeding text to the last whitespace or '.' 

##### `edit_paste(self, event=None)`

Pastes any text and updates the IDE 

##### `exec_block(self, event=None, insert=insert)`

Method to highlight block of code and execute 

##### `exec_line(self, event=None, insert=insert)`

Highlights a single line and executes 

##### `highlight(self, start, end, colour=Red)`

Highlights an area of text 

##### `indent(self, event=None, insert=insert)`

Indent the current line or selected text 

##### `keypress(self, event=None)`

Handles any keypress 

##### `kill(self)`

Proper exit function 

##### `killall(self, event=None)`

Stops all player objects 

##### `newfile(self, event=None)`

Clears the document and asks if the user wants to save 

##### `newline(self, event=None, insert=insert)`

Adds whitespace to newlines where necessary 

##### `replace(self, line, old, new)`

Replaces text on a specified line and updates the IDE 

##### `replace_re(self, line, new=)`

Replaces text on a specified line and updates the IDE 

##### `run(self)`

Starts the Tk mainloop for the master widget 

##### `save(self, event=None)`

Saves the contents of the text editor 

##### `selectall(self, event=None)`

Select the contents of the editor 

##### `submit(self, code_str)`

Runs the chunk of code through FoxDot processing and execute 

##### `tab(self, event=None, insert=insert)`

Move selected text forward 4 spaces 

##### `terminate(self)`

Called on window close. Ends Clock thread process 

##### `text_selected(self)`

Returns True if text is selected 

##### `unhighlight(self)`

Creates thread to wait 0.2 seconds before removing any highlights from the text 

##### `unindent(self, event)`

Moves the current row or selected text back by 4 spaces 

##### `update(self, event=None, insert=insert)`

Updates the the colours of the IDE 

##### `update_all(self)`

Updates every line in the IDE 

##### `zoom_in(self, event=None)`

Ctrl+= increases text size 

##### `zoom_out(self, event=None)`

Ctrl+- decreases text size (minimum of 8) 

---

## Functions

## Data

