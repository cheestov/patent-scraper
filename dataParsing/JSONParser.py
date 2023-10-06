import os
import zipfile
import json
import pandas as pd
import shutil
import re
import threading
from time import sleep
import random


def update  (zip_filename, filename, lineno, column, text):
    # Create a temporary file and open it for writing
    txtName = "downloadedData/temp{}.txt".format(random.randint(1, 100))
    if (lineno == 1):
       # print("doing the fix thing")
        with open(file=txtName, mode="w", encoding="utf-8") as fout:
            # Open the zipfile
            with zipfile.ZipFile(zip_filename, 'r') as myzip:
                # Open the specific file within the zipfile
                with myzip.open(filename, 'r') as myfile:
                    for i, line in enumerate(myfile):
                        # If this is the line we want to modify
                        if lineno > 1:
                            column = 1
                        if i == lineno - 1:
                            line = line.decode("utf-8")  # Decode line to string
                            # Update the line
                            if (text == " " and column < 25):
                                line = line[0:column - 1] + "{" + line[column + 1:] + "\n"
                            elif (text == "," and lineno > 1 and column == 1):
                                line = text + line[column-1:] + "\n"
                            else:
                                line = line[0:column-1] + text + line[column-1:] + "\n"
                        else:
                            line = line.decode("utf-8") + "\n"
                        # Write the line to the temporary file
                        while line.find("[\\p{Cf}]") != -1:
                            line.replace("[\\p{Cf}]", '')
                        line = re.sub(u"\u200b", "", line)
                        fout.write(line)
        fout.close()
    # Now we're going to update the zipfile with the modified file
    temp_zipfile = "downloadedData/temp.zip"
    with zipfile.ZipFile(temp_zipfile, 'w') as newzip:
        with zipfile.ZipFile(zip_filename, 'r') as oldzip:
            for item in oldzip.infolist():
                if item.filename != filename:
                    #print("adding {}".format(item.filename))
                    data = oldzip.read(item.filename)
                    newzip.writestr(item, data)
        if (lineno == 1):
            newzip.write(txtName, arcname=filename)
    
    # Replace the old zipfile with the new zipfile
    os.remove(zip_filename)
    os.rename(temp_zipfile, zip_filename)

    # Clean up the temporary file   
    # thread = threading.Thread(target=os.remove(), args={"path":"tempt.txt"})
    # thread.start()
    # thread.join()

def ZipFix(targetFile) :
    errorIndexs = []
    names = []
    errorText = []
    returnValue = -1
    lineNo = 1
    with zipfile.ZipFile(targetFile) as z:
        for filename in z.namelist():
            print(filename)
            if not os.path.isdir(filename):
                # read the file
                with z.open(filename) as f:
                    #print(f.readline())
                    try:
                        
                        data = json.load(f)
                    except json.JSONDecodeError as e:
                        returnValue = 1
                        print(f"Error decoding JSON: {e}")
                        lineNo = int(str(e)[str(e).find("line ") + 5:][:str(e)[str(e).find("line ") + 5:].find(" ")])
                        errorIndex = int(str(e)[str(e).rindex(" ") + 1 : len(str(e)) - 1]) + 1
                        print(lineNo)
                        print(errorIndex)
                        if str(e).find('delimiter') != -1:
                            errorText.append(",")
                            print("comma")
                        elif str(e)[str(e).find(":"): str(e).find(":") + 3] == ": l":
                            print("space")
                            errorText.append(" ")
                        names.append(filename)
                        errorIndexs.append(errorIndex)
                        #update("resultsFile.zip", filename, 1, errorIndex, ",")j


    for i in range(len(errorIndexs)):
        update(targetFile, names[i], lineNo, errorIndexs[i], errorText[i])
        print("success on " + names[i])
    return returnValue

def extractVariables(targetFile):
    # Get the variables from the data
    df = pd.DataFrame(columns=['patentNumber', 'title', 'USPC #', "applicationType", "entityStatusCat", 'assignee', "applicantOrg", "applicantOrgCountryCode", "applicantOrgState", 'IPFirm', "IPFirmCountryCode", "IPFirmState", 'patentIssueDate', 'applicationFilingDate'])

    with zipfile.ZipFile(targetFile) as z:
        print(targetFile)
        for filename in z.namelist():
            print(filename)
            if not os.path.isdir(filename):
                # read the file
                with z.open(filename) as f:
                    #print(f.readline())
                    # try:
                    #     lines = f.readlines()
                    #     data = json.loads(lines)
                    # except json.JSONDecodeError as e:
                    #     print(f"Error decoding JSON: {e}")
                    #     errorIndex = int(str(e)[str(e).rindex(" ") + 1 : len(str(e)) - 1])
                    #     print(errorIndex)
                    #     #update("resultsFile.zip", filename, 1, errorIndex, ",")


                    try:
                        data = json.load(f)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                        exit()

                    print(len(data["PatentData"]))
                    for p in data["PatentData"]:
                        applicationType = ""
                        if "applicationTypeCategory" in p["patentCaseMetadata"]:
                            applicationType = p["patentCaseMetadata"]["applicationTypeCategory"]
                        entityStatusCat = ""
                        if "businessEntityStatusCategory" in p["patentCaseMetadata"]:
                            entityStatusCat = p["patentCaseMetadata"]["businessEntityStatusCategory"]
                        if 'patentGrantIdentification' in p['patentCaseMetadata']:
                            patentNumber = p["patentCaseMetadata"]['patentGrantIdentification']["patentNumber"]
                            patentIssueDate = p["patentCaseMetadata"]['patentGrantIdentification']["grantDate"]
                        else:
                            patentNumber = ""
                            patentIssueDate = ""
                        title = p["patentCaseMetadata"]["inventionTitle"]["content"]
                        USPCnum = p["patentCaseMetadata"]["patentClassificationBag"]['cpcClassificationBagOrIPCClassificationOrECLAClassificationBag'][0]["mainNationalClassification"]["nationalClass"]
                        if "firstNamedApplicant" in p['patentCaseMetadata']:
                            applicantOrg = p["patentCaseMetadata"]["firstNamedApplicant"][3:len(p["patentCaseMetadata"]["firstNamedApplicant"]) - 1]
                            applicantOrgState = ""
                            applicantOrgCountryCode = ""
                            for a in p['patentCaseMetadata']['partyBag']['applicantBagOrInventorBagOrOwnerBag']:
                                if 'applicant' in a:
                                    if 'countryCode' in a['applicant'][0]['contactOrPublicationContact'][0]:
                                        applicantOrgCountryCode = a['applicant'][0]['contactOrPublicationContact'][0]['countryCode']
                                        if applicantOrgCountryCode == "US":
                                            applicantOrgState = a['applicant'][0]['contactOrPublicationContact'][0]['geographicRegionName']['value']
                                        else:
                                            applicantOrgState = ""
                        else:
                            applicantOrg = ""
                            applicantOrgState = ""
                            applicantOrgCountryCode = ""

                        assignee = ""
                        if 'assignmentDataBag' in p:
                            if 'assigneeBag' in p['assignmentDataBag']['assignmentData'][0]:
                                try:
                                    if 'contactOrPublicationContact' in p['assignmentDataBag']['assignmentData'][0]['assigneeBag']['assignee']:
                                        assignee = p['assignmentDataBag']['assignmentData'][0]['assigneeBag']['assignee']['contactOrPublicationContact'][0]['name']['personNameOrOrganizationNameOrEntityName'][0]['value']
                                    else:
                                        assignee = p['assignmentDataBag']['assignmentData'][0]['assigneeBag']['assignee'][0]['contactOrPublicationContact'][0]['name']['personNameOrOrganizationNameOrEntityName'][0]['value']
                                except:
                                    print("weird index error in {} {}".format(targetFile, filename))
                                    assignee = ""
                        IPFirm = ""
                        IPFirmState = ""
                        IPFirmCountryCode = ""
                        for a in p['patentCaseMetadata']['partyBag']['applicantBagOrInventorBagOrOwnerBag']:
                            if 'partyIdentifierOrContact' in a:
                                if 'firstName' in a['partyIdentifierOrContact'][0]['name']['personNameOrOrganizationNameOrEntityName'][0]['personStructuredName']:
                                    IPFirm = ""
                                    IPFirmState = ""
                                    IPFirmCountryCode = ""
                                else:
                                    IPFirm = a['partyIdentifierOrContact'][0]['name']['personNameOrOrganizationNameOrEntityName'][0]['personStructuredName']['lastName']
                                    IPFirmCountryCode = a['partyIdentifierOrContact'][0]['postalAddressBag']['postalAddress'][0]['postalStructuredAddress']['countryCode']
                                    if IPFirmCountryCode == "US":
                                        IPFirmState = a['partyIdentifierOrContact'][0]['postalAddressBag']['postalAddress'][0]['postalStructuredAddress']['geographicRegionName'][0]['value']
                            else:
                                IPFirm = ""
                                IPFirm = ""
                                IPFirm = ""
                        
                        applicationFilingDate = p["patentCaseMetadata"]["filingDate"]

                        df.loc[len(df)]= [patentNumber, title, USPCnum, applicationType, entityStatusCat, assignee, applicantOrg, applicantOrgCountryCode, applicantOrgState, IPFirm, IPFirmCountryCode, IPFirmState, patentIssueDate, applicationFilingDate]
    df.to_csv('patentTitles.csv', index=False, encoding='utf-8', header=False, mode='a')


bundledFiles = os.listdir(path="./downloadedData")
df = pd.DataFrame(columns=['patentNumber', 'title', 'USPC #', "applicationType", "entityStatusCat", 'assignee', "applicantOrg", "applicantOrgCountryCode", "applicantOrgState", 'IPFirm', "IPFirmCountryCode", "IPFirmState", 'patentIssueDate', 'applicationFilingDate'])
df.to_csv('patentTitles.csv', index=False, encoding='utf-8', header=True)
threads = []
for targetFile in bundledFiles:
    targetFile = "downloadedData/{}".format(targetFile)
    errChk = ZipFix(targetFile)
    while errChk != -1:
        print(targetFile)
        errChk = ZipFix(targetFile)


    print(targetFile)
    extract_thread = threading.Thread(target=extractVariables, args=(targetFile,))
    extract_thread.start()
    
    threads.append(extract_thread)
for thr in threads:
    thr.join()

print("Success")