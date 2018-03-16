# `Parse`

Patterns.Parse.py
=================

Handles the parsing of Sample Player Object Strings

## Classes

## Functions

### `ParsePlayString(string)`

Returns the parsed play string used by sample player 

### `arrow_zip(pat1, pat2)`

Zips two patterns together. If one item is a tuple, it extends the tuple / PGroup
i.e. arrow_zip([(0,1),3], [2]) -> [(0,1,2),(3,2)]

### `feed(string)`

Used to recursively parse nested strings, returns a list object (not Pattern),
and a boolean denoting if the list contains a nested list 

## Data

