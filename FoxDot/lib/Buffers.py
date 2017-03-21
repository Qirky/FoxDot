#!/usr/bin/python

""" This module manages the allocation of buffer numbers and samples """

from os.path import abspath, join, dirname
from Settings import FOXDOT_SND, FOXDOT_BUFFERS_FILE
from ServerManager import Server
import wave
import os

def path(fn):
    return abspath(join(dirname(__file__), fn))

alpha    = "abcdefghijklmnopqrstuvwxyz"

nonalpha = {"&" : "ampersand",
            "*" : "asterix",
            "@" : "at",
            "|" : "bar",
            "^" : "caret",
            ":" : "colon",
            "$" : "dollar",
            "=" : "equals",
            "!" : "exclamation",
            "/" : "forwardslash",
            ">" : "greaterthan",
            "#" : "hash",
            "-" : "hyphen",
            "<" : "lessthan",
            "%" : "percent",
            "+" : "plus",
            "?" : "question",
            "~" : "tilde",
            "\\" :"backslash" }

DESCRIPTIONS = { 'a' : "Unknown",
                 'b' : "Unknown",
                 'c' : "Choral",
                 'd' : "Unknown",
                 'e' : "Unknown",
                 'f' : "Wood",
                 'g' : "Unknown",
                 'h' : "Unknown",
                 'i' : "Unknown",
                 'j' : "Unknown",
                 'k' : "Unknown",
                 'l' : "Unknown",
                 'm' : "Toms",
                 'n' : "Unknown",
                 'o' : "Snare drum",
                 'p' : "Tabla",
                 'q' : "Unknown",
                 'r' : "Metal",
                 's' : "Shaker",
                 't' : "Cowbell",
                 'u' : "Unknown",
                 'v' : "Unknown",
                 'w' : "Unknown",
                 'x' : "Bass drum",
                 'y' : "Unknown",
                 'z' : "Unknown",
                 '-' : "Hi hat closed",
                 '=' : "Hi hat open",
                 '*' : "Clap",
                 '~' : "Ride cymbal",
                 '^' : "'Donks'",
                 '#' : "Crash",
                 '+' : "Clicks",
                 '@' : "Computer" }

class Buffer:
    def __init__(self, fn, number, channels=1):
        self.fn = fn
        self.bufnum   = int(number)
        self.channels = channels
    def __repr__(self):
        return "<Buffer num {}>".format(self.bufnum)
    def __int__(self):
        return self.bufnum

class BufChar:
    server = Server
    def __init__(self, char):
        self.char    = char
        self.buffers = []
    def __str__(self):
        return "BufChar '{}': '{}'".format(self.char, DESCRIPTIONS.get(self.char, "unknown"))
    def addbuffer(self, fn, num, num_channels=1):
        self.buffers.append( Buffer(fn, num, num_channels) )
        if fn is not None:
            self.server.bufferRead(fn, num)
        return
    def __getitem__(self, key):
        return self.buffers[key]
    def __iter__(self):
        for buf in self.buffers:
            yield buf.fn, buf.bufnum
    def bufnum(self, n):
        return self.buffers[n % len(self.buffers)] if self.buffers else Buffer(None, 0)

class BufferManager:
    def __init__(self):

        # Dictionary of characters to respective buffer number
        self.symbols = {}

        # Dictionary of buffer numbers to character
        self.buffers = {}

        # Load buffers
        bufnum = 1
        root   = FOXDOT_SND

        # Go through the alphabet

        for folder in ('lower', 'upper'):

            for char in alpha:

                if folder == "upper":

                    char = char.upper()
                
                path = join(root, char.lower(), folder)

                self.symbols[char] = BufChar(char)

                if os.path.isdir(path):
                
                    for f in sorted(os.listdir(path)):

                        try:

                            snd = wave.open(join(path, f))
                            numChannels = snd.getnchannels()
                            snd.close()

                        except wave.Error as e:

                            numChannels = 1

                        self.symbols[char].addbuffer(join(path, f), bufnum, numChannels)
                        self.buffers[bufnum] = self.symbols[char][-1]

                        bufnum += 1

        # Go through symbols

        for char in nonalpha:

            self.symbols[char] = BufChar(char)

            path = join(root, "_", nonalpha[char])

            if (os.path.isdir(path)):
        
                for f in sorted(os.listdir(path)):

                    try:

                        snd = wave.open(join(path, f))
                        numChannels = snd.getnchannels()
                        snd.close()

                    except wave.Error:

                        numChannels = 1

                    self.symbols[char].addbuffer(join(path, f), bufnum, numChannels)
                    self.buffers[bufnum] = self.symbols[char][-1]

                    bufnum += 1

        # Define empty buffer
        self.nil = BufChar(None)
        self.nil.addbuffer(None, 0)

        # Write to file
        self.write_to_file()

    def __getitem__(self, key):
        if hasattr(key, 'char'):
            key = key.char
        return self.symbols.get(key, self.nil)

    def getBuffer(self, bufnum):
        return self.buffers[int(bufnum)]

    def __str__(self):
        return "\n".join(["{}: {}".format(symbol, b) for symbol, b in self.symbols.items()])

    def write_to_file(self):
        f = open(FOXDOT_BUFFERS_FILE, 'w')
        for char in self.symbols:
            for fn, buf in self.symbols[char]:
                f.write('Buffer.read(s, "{}", bufnum:{});\n'.format(path(fn).replace("\\","/"), buf))
        return

    def load(self):
        for char in self.symbols:
            for fn, buf in self.symbols[char]:
                self.server.bufferRead(buf, path(fn))
        return

    def bufnum(self, char):
        return self.symbols.get(char, 0)
