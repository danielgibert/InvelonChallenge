import pandas as pd
import os
import glob

data = []

categories = [name for name in os.listdir("./valid")]

for category in categories:
    files = glob.glob("./**/" + category + "/*.stl")
    for file in files:
        data.append([file, category])
        
        
df = pd.DataFrame(data)
df.to_csv("categories.csv")