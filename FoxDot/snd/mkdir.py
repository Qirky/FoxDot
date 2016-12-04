import os
import shutil

alpha = "abcdefghijklmnopqrstuvwxyz"

for char in alpha:
    try:
        os.mkdir(char)
        os.mkdir(char+"/"+"lower")
        os.mkdir(char+"/"+"upper")
    except:
        pass
try:
    os.mkdir("_")
except:
    pass

csv = "samplelib.csv"

with open(csv) as f:
    data = f.readlines()

for line in data:

    char, fn, desc = line.split(",")

    fn = fn[1:]

    ext = fn.rsplit(".",1)[-1]

    folder = ""

    if char in alpha + alpha.upper():

        if char.isupper():

            folder = char.lower() + "/upper/"

        elif char.islower():

            folder = char + "/lower/"

        dst = folder + "0." + ext

        print dst

        shutil.copy(fn, dst)

        

        

            
    
