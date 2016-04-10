#!/usr/bin/python

""" This module manages the allocation of buffer numbers and samples """

from os.path import abspath, join, dirname

def path(fn):
    return abspath(join(dirname(__file__), fn))


class BufferManager:
    def __init__(self):

        # ServerManager Object
        self.server = None

        # Dictionary of characters to respective buffer number
        self.symbols = {}

        # Dictionary of buffer numbers to character
        self.buffers = {}
        
        
    def from_file(self, configFile="./Settings/sample_names.txt", offset=0):
        """ Reads in a config file """
        with open(path(configFile)) as f:
            lines = f.readlines()

        for bufnum, line in enumerate(lines):
            bufnum = bufnum + offset + 1 # 0 is the empty buffer
            try:
                char, fn = line.strip().split()
                self.symbols[char]   = bufnum 
                self.buffers[bufnum] = fn
            except:
                pass
        return self

    def __call__(self, server):
        self.server = server 
        return self

    def load(self):
        for buf, fn in self.buffers.items():
            self.server.bufferRead(buf, path("./Samples/" + fn))

    def bufnum(self, char):
        b = 0
        for ch, buf in self.symbols.items():
            if ch == char:
                b = buf
        return b
