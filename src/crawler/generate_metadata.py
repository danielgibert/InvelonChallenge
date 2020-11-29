import pandas as pd
import os
import glob
import json

"""

Exports .json files with the renaming of categories and
exports the .jpeg files found in grayscale folders of
the valid .slt files

"""

rootPath = "/home/vdasilva@lleidanet.lnst.es/Sergi/InvelonChallenge"

dataPath = rootPath + "/" + "data/valid/"

data = []
print(dataPath)
print(os.listdir(dataPath))
categories = []
for name in os.listdir(dataPath):
    if ".csv" in name or ".json" in name or ".tfrecords" in name or ".ipynb_checkpoints" in name:
        continue
    categories.append(name)

categories.sort()

categoriesMap = dict((v, k) for (k,v) in enumerate(categories))
categoriesReversedMap = dict((k, v) for (k,v) in enumerate(categories))

print(categoriesMap)
print(categoriesReversedMap)

with open(dataPath + "categoriesMap.json", "w") as outfile:
    json.dump(categoriesMap, outfile)
    
with open(dataPath + "categoriesReversedMap.json", "w") as outfile:
    json.dump(categoriesReversedMap, outfile)

data.append(["filename", "ID"])
for category in categories:
    files = glob.glob(dataPath + category + "/grayscale/*.jpeg")
    for file in files:
        data.append([file, categoriesMap[category]])        
df = pd.DataFrame(data)
df.to_csv(dataPath + "categories.csv")