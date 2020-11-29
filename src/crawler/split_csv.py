import pandas as pd
import ntpath
import random

"""

Splits the csv with the current data into training and validation sets

"""

rootPath = "/home/vdasilva@lleidanet.lnst.es/Sergi/InvelonChallenge"

inputCSV = rootPath + "/data/valid/categories.csv"
exportPath = rootPath + "/data/valid/"

df = pd.read_csv(inputCSV, skiprows=1)
df = df[["filename", "ID"]]
percentageTraining = 0.8
numElementsTraining = int(len(df.index) * percentageTraining)

# Shuffle
df = df.sample(frac=1).reset_index(drop=True)
training = df.iloc[:numElementsTraining]
test = df.iloc[numElementsTraining:]

training.to_csv(exportPath + "training.csv", index=False)
test.to_csv(exportPath + "validation.csv", index=False)