import glob
import os
from shutil import copyfile
import ntpath


files = glob.glob("./**/*/*.stl")

maxSize = 1000000
noNames = ["part", "body", "left", "right", "arm", "leg", "front", "back"]

category = "animals"

validFolder = "./valid"
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
        copyfile(file, categoryFolder + "/" + filename)
        print("Valid: " + filename)