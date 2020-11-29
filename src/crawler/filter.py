import glob
import os
from shutil import copyfile
import ntpath
import sys

"""
Export the .stl files that accomplish some criteria
"""

rootPath = "/home/vdasilva@lleidanet.lnst.es/Sergi/InvelonChallenge"

dataPath = rootPath + "/" + "data/"

# animals tools
category = sys.argv[1]
files = glob.glob(dataPath + "stls/" + category + "/**/*.stl")

# Maximum size 1MB
maxSize = 1000000

# Filename filter to avoid incomplete models
noNames = ["part", "body", "left", "right", "arm", "leg", "front", "back"]

validFolder = rootPath + "/data/valid"
categoryFolder = validFolder + "/" + category

if not os.path.exists(categoryFolder):
    os.makedirs(categoryFolder)


for file in files:
    valid = True
    filename = ntpath.basename(file).lower()
    
    for noName in noNames:
        if noName in filename:
            valid = False
            break
            
    if os.stat(file).st_size > maxSize:
        valid = False
    
    if valid:
        print(categoryFolder)
        copyfile(file, categoryFolder + "/" + filename)
        print("Valid: " + filename)