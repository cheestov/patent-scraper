import os
import zipfile
import json
import pandas as pd
import shutil

def update  (zip_filename, filename, lineno, column, text):
    # Create a temporary file and open it for writing
    with open("temp.txt", "w") as fout:
        # Open the zipfile
        with zipfile.ZipFile(zip_filename, 'r') as myzip:
            # Open the specific file within the zipfile
            with myzip.open(filename, 'r') as myfile:
                for i, line in enumerate(myfile):
                    # If this is the line we want to modify
                    if i == lineno - 1:
                        line = line.decode("utf-8")  # Decode line to string
                        # Update the line
                        line = line[0:column-1] + text + line[column-1:] + "\n"
                    else:
                        line = line.decode("utf-8") + "\n"
                    # Write the line to the temporary file
                    fout.write(line)

    # Now we're going to update the zipfile with the modified file
    temp_zipfile = "temp.zip"
    with zipfile.ZipFile(temp_zipfile, 'w') as newzip:
        with zipfile.ZipFile(zip_filename, 'r') as oldzip:
            for item in oldzip.infolist():
                if item.filename != filename:
                    data = oldzip.read(item.filename)
                    newzip.writestr(item, data)
        newzip.write("temp.txt", arcname=filename)
    
    # Replace the old zipfile with the new zipfile
    os.remove(zip_filename)
    os.rename(temp_zipfile, zip_filename)

    # Clean up the temporary file
    os.remove("temp.txt")

df = pd.DataFrame(columns=['patentNumber', 'title', 'USPC #', 'company', 'companyState', 'patentIssueDate', 'applicationFilingDate'])

errorIndexs = []
names = []


with zipfile.ZipFile('resultsFile.zip') as z:
    for filename in z.namelist():
        print(filename)
        if not os.path.isdir(filename):
            # read the file
            with z.open(filename) as f:
                #print(f.readline())
                try:
                    
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    errorIndex = int(str(e)[str(e).rindex(" ") + 1 : len(str(e)) - 1]) + 1
                    print(errorIndex)
                    names.append(filename)
                    errorIndexs.append(errorIndex)
                    #update("resultsFile.zip", filename, 1, errorIndex, ",")


for i in range(len(errorIndexs)):
    update("resultsFile.zip", names[i], 1, errorIndexs[i], ",")
    print("success on " + names[i])


with zipfile.ZipFile('resultsFile.zip') as z:
    for filename in z.namelist():
        print(filename)
        if not os.path.isdir(filename):
            # read the file
            with z.open(filename) as f:
                #print(f.readline())
                try:
                    lines = f.readlines()
                    data = json.loads(lines)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    errorIndex = int(str(e)[str(e).rindex(" ") + 1 : len(str(e)) - 1])
                    print(errorIndex)
                    #update("resultsFile.zip", filename, 1, errorIndex, ",")
                
                f = z.open(filename)


                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")

                print(len(data["PatentData"]))
                for p in data["PatentData"]:
                    patentNumber = p["patentCaseMetadata"]['patentGrantIdentification']["patentNumber"]
                    title = p["patentCaseMetadata"]["inventionTitle"]["content"]
                    USPCnum = p["patentCaseMetadata"]["patentClassificationBag"]['cpcClassificationBagOrIPCClassificationOrECLAClassificationBag'][0]["mainNationalClassification"]["nationalClass"]
                    if "firstNamedApplicant" in p['patentCaseMetadata']:
                        assignee = p["patentCaseMetadata"]["firstNamedApplicant"][3:len(p["patentCaseMetadata"]["firstNamedApplicant"]) - 1]
                        assigneeState = "N/A"
                        for a in p['patentCaseMetadata']['partyBag']['applicantBagOrInventorBagOrOwnerBag']:
                            if 'applicant' in a:
                                assigneeState = a['applicant'][0]['contactOrPublicationContact'][0]['geographicRegionName']['value']
                    else:
                        assignee = "N/A"
                        assigneeState = "N/A"
                        assigneeSize = "N/A"
                    patentIssueDate = p["patentCaseMetadata"]['patentGrantIdentification']["grantDate"]
                    applicationFilingDate = p["patentCaseMetadata"]["filingDate"]

                    df.loc[len(df)]= [patentNumber, title, USPCnum, assignee, assigneeState, patentIssueDate, applicationFilingDate]

df.to_csv('patentTitles.csv', index=False, encoding='utf-8')