import os
import zipfile
import json
import pandas as pd

df = pd.DataFrame(columns=['patentTitle'])

with zipfile.ZipFile('resultsFile.zip') as z:
    for filename in z.namelist():
        if not os.path.isdir(filename):
            # read the file
            with z.open(filename) as f:
                data = json.load(f)
                print(len(data["PatentData"]))
                for p in data["PatentData"]:
                    df.loc[len(df)]= p["patentCaseMetadata"]["inventionTitle"]["content"]

df.to_csv('patentTitles.csv', index=False, encoding='utf-8')