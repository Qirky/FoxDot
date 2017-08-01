#!/usr/bin/python

""" This module manages the allocation of buffer numbers and samples """
from __future__ import absolute_import, division, print_function

from os.path import abspath, join, dirname
from .Settings import FOXDOT_SND, FOXDOT_BUFFERS_FILE
from .Settings import FOXDOT_LOOP
from .ServerManager import Server
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
            "\\" :"backslash",
            "1" : "1",
            "2" : "2",
            "3" : "3",
            "4" : "4" }

DESCRIPTIONS = { 'a' : "Gameboy hihat", 'A' : "Sword",
                 'b' : "Cowbell",       'B' : "Short saw",
                 'c' : "Box",           'C' : "Choral",
                 'd' : "Click",         'D' : "Buzz",
                 'e' : "Cowbell",       'E' : "Sparkle",
                 'f' : "Wood",          'F' : "Swipe",
                 'g' : "Ominous",       'G' : "Stab",
                 'h' : "Rough clap",    'H' : "Clap",
                 'i' : "Jungle snare",  'I' : "Rock snare",
                 'j' : "Jug",           'J' : "Reverse",
                 'k' : "Bass",          'K' : "Dub shot",
                 'l' : "Knock",         'L' : "Siren",
                 'm' : "Toms",          'M' : "Electro Tom",
                 'n' : "Noise",         'N' : "Gameboy SFX",
                 'o' : "Snare drum",    'O' : "Heavy snare",
                 'p' : "Tabla 1",       'P' : "Tabla long",
                 'q' : "Table 2",       'Q' : "Tabla long",
                 'r' : "Metal",         'R' : "Metallic",
                 's' : "Shaker",        'S' : "Tamborine",
                 't' : "Cowbell",       'T' : "Cowbell",
                 'u' : "Frying pan",    'U' : "Misc. Fx",   
                 'v' : "Kick drum 3",   'V' : "Soft kick",
                 'w' : "Dub hits",      'W' : "Distorted",
                 'x' : "Bass drum 1",   'X' : "Heavy kick",
                 'y' : "Bleep",         'Y' : "High buzz",
                 'z' : "Scratch",       "Z" : "Buzz",
                 '-' : "Hi hat closed", "|" : "Glitch",
                 '=' : "Hi hat open",   "/" : "Reverse sounds",
                 '*' : "Clap",          "\\" : "Lazer",
                 '~' : "Ride cymbal",
                 '^' : "'Donk'",
                 '#' : "Crash",
                 '+' : "Clicks",
                 '@' : "Computer",
                 '1' : "Vocals (One)",
                 '2' : 'Vocals (Two)',
                 '3' : 'Vocals (Three)',
                 '4' : 'Vocals (Four)'}

class Buffer(object):
    def __init__(self, fn, number, channels=1):
        self.fn = fn
        self.bufnum   = int(number)
        self.channels = channels
    def __repr__(self):
        return "<Buffer num {}>".format(self.bufnum)
    def __int__(self):
        return self.bufnum

class BufChar(object):
    server = Server
    def __init__(self, char):
        self.char    = char
        self.buffers = []
    def __str__(self):
        return "BufChar '{}': '{}'".format(self.char, DESCRIPTIONS.get(self.char, "----"))
    def __getitem__(self, key):
        return self.buffers[key]
    def __iter__(self):
        for buf in self.buffers:
            yield buf.fn, buf.bufnum
    # Comparisons
    def __eq__(self, other):
        return str(self.char) == str(other)
    def __ne__(self, other):
        return str(self.char) != str(other)
    # Methods
    def addbuffer(self, fn, num, num_channels=1):
        self.buffers.append( Buffer(fn, num, num_channels) )
        self.buffers[-1].char = self.char
        if fn is not None:
            self.server.bufferRead(fn, num)
        return
    def bufnum(self, n):        
        return self.buffers[int(n % len(self.buffers))] if self.buffers else Buffer(None, 0)

class LoopFile(BufChar):
    def __str__(self):
        return "LoopFile '{}' loaded in buffer {}".format(self.char, self.buffers[0])

class BufferManager:
    def __init__(self):

        # Dictionary of characters to respective buffer number
        self.symbols = {}

        # Dictionary of buffer numbers to character
        self.buffers = {}
        self.loop_files = {}

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

        # Sort out loop buffers

        for filename in os.listdir(FOXDOT_LOOP):

            path = join(root, FOXDOT_LOOP)

            name = "".join(filename.split(".")[:-1])

            self.loop_files[name] = LoopFile(name)
            self.loop_files[name].addbuffer(join(path, filename), bufnum, 2)

            bufnum += 1

        self.loops = list(self.loop_files.keys())

        # Write to file
        self.write_to_file()

    def __getitem__(self, key):
        if hasattr(key, 'char'):
            key = key.char
        return self.symbols.get(key, self.nil)

    def getBuffer(self, bufnum):
        return self.buffers[int(bufnum)]

    def __str__(self):
        # return "\n".join(["{}: {}".format(symbol, b) for symbol, b in self.symbols.items()])
        return "\n".join([str(value) for value in self.symbols.values()])

    def write_to_file(self):
        f = open(FOXDOT_BUFFERS_FILE, 'w')
        for data_list in [self.symbols, self.loop_files]:
            for char in data_list:
                for fn, buf in data_list[char]:
                    f.write('Buffer.read(s, "{}", bufnum:{});\n'.format(path(fn).replace("\\","/"), buf))
        return

    def load(self):
        for data_list in [self.symbols, self.loop_files]:
            for char in data_list:
                for fn, buf in data_list[char]:
                    self.server.bufferRead(buf, path(fn))
        return

    def bufnum(self, char):
        return self.symbols.get(char, 0)

Samples = BufferManager()

def FindBuffer(name):
    if name in Samples.loop_files:
        return int(Samples.loop_files[name].bufnum(0))
    else:
        print("File '{}' not found".format(name))
        return 0

from .SCLang import SampleSynthDef

class LoopSynthDef(SampleSynthDef):
    def __init__(self):
        SampleSynthDef.__init__(self, "loop")
        self.pos = self.new_attr_instance("pos")
        self.defaults['pos']   = 0
        self.base.append("osc = PlayBuf.ar(2, buf, BufRateScale.kr(buf) * rate, startPos: BufSampleRate.kr(buf) * pos);")
        self.base.append("osc = osc * EnvGen.ar(Env([0,1,1,0],[0.05, sus-0.05, 0.05]));")
        self.osc = self.osc * self.amp
        self.add()
    def __call__(self, filename, pos=0, **kwargs):
        kwargs["buf"] = FindBuffer(filename)
        return SampleSynthDef.__call__(self, pos, **kwargs)

loop = LoopSynthDef()
