import os
import zipfile
import json
import pandas as pd

df = pd.DataFrame(columns=['patentNumber', 'title', 'USPC #', 'company', 'companyState', 'patentIssueDate', 'applicationFilingDate'])

with zipfile.ZipFile('resultsFile.zip') as z:
    for filename in z.namelist():
        print(filename)
        if not os.path.isdir(filename):
            # read the file
            with z.open(filename) as f:
                print(f.readline())
                data = json.load(f)
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