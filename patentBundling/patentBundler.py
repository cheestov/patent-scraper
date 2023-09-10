import json
from time import sleep
import requests

# use pandas to turn the JSON into a dataframe and then make it into a csv

# {"searchText":"","fq":["patentIssueDate:[2019-01-01T00:00:00Z TO 2019-01-01T23:59:59Z]"],"fl":"*","mm":"100%","df":"patentTitle","qf":"patentIssueDate appLocationYear appEarlyPubNumber applId appLocation appType appStatus_txt appConfrNumber appCustNumber appGrpArtNumber appCls appSubCls appEntityStatus_txt patentNumber patentTitle primaryInventor firstNamedApplicant wipoEarlyPubNumber pctAppType firstInventorFile appClsSubCls rankAndInventorsList","facet":"false","sort":"applId asc","start":"0"}

def querymaker(year):
    issueDate = "{}-01-01T00:00:00Z TO {}-01-01T23:59:59Z".format(year, year)
    variables = "patentIssueDate appLocationYear appEarlyPubNumber applId appLocation appType appStatus_txt appConfrNumber appCustNumber appGrpArtNumber appCls appSubCls appEntityStatus_txt patentNumber patentTitle primaryInventor firstNamedApplicant firstNamedApplicantNameList wipoEarlyPubNumber pctAppType firstInventorFile appClsSubCls rankAndInventorsList"

    query = {"searchText":"*:*",
"fq":["appFilingDate:[2019-01-01T00:00:00Z TO 2019-01-01T23:59:59Z]"],
"fl":"*",
"mm":"100%",
"df":"patentTitle",
"qf":"patentIssueDate appLocationYear appEarlyPubNumber applId appLocation appType appStatus_txt appConfrNumber appCustNumber appGrpArtNumber appCls appSubCls appEntityStatus_txt patentNumber patentTitle primaryInventor firstNamedApplicant firstNamedApplicantNameList wipoEarlyPubNumber pctAppType firstInventorFile appClsSubCls rankAndInventorsList",
"facet":"false",
"sort":"applId asc",
"start":"0"}

   # query = json.dumps({"searchText":"firstNamedApplicant:(Google)","fq":["appFilingDate:[2013-01-01T00:00:00Z TO 2013-12-31T23:59:59Z]","appStatus:\"Patented Case\""],"fl":"*","mm":"100%","df":"patentTitle","qf":"appEarlyPubNumber applId appLocation appType appStatus_txt appConfrNumber appCustNumber appGrpArtNumber appCls appSubCls appEntityStatus_txt patentNumber patentTitle primaryInventor firstNamedApplicant appExamName appExamPrefrdName appAttrDockNumber appPCTNumber appIntlPubNumber wipoEarlyPubNumber pctAppType firstInventorFile appClsSubCls rankAndInventorsList","facet":"false","sort":"applId asc","start":"0"})
    return query
    
def download_file(url):
    local_filename = "resutsFile.zip"
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename

postJSON = querymaker("2019")
print(postJSON)

url = 'https://ped.uspto.gov/api/queries'
myobj = {'somekey': 'somevalue'}


#print(requests.get(url='https://ped.uspto.gov/api/search-params').status_code)
#exit()

queryOne = requests.post(url, json=postJSON, headers={'accept' : 'application/json'})

print(queryOne.status_code)
print(queryOne.content)

if queryOne.status_code != 200 :
    exit("Non-200 OK response.")

#initialJSON = queryOne.json()
#initialJSON_dict = json.load(initialJSON)
initialDict = queryOne.json()
print(type(initialDict))

firstQueryID = initialDict['queryId']

print(firstQueryID)

jobStatus = "initiated"

while (jobStatus != "CREATED"):
    url = 'https://ped.uspto.gov/api/queries/{}'.format(firstQueryID)
    queryStatus = requests.get(url, headers={'accept' : 'application/json'})

    print(queryStatus.status_code)
    print(queryStatus.content)

    status = queryStatus.status_code
    if status != 200:
        exit("non-200 status code.")

    queryStatusDict = queryStatus.json()
    jobStatus = queryStatusDict["jobStatus"]
    print(jobStatus)
    if jobStatus != "CREATED":
        sleep(30)

url = "https://ped.uspto.gov/api/queries/{}/package?format=JSON".format(firstQueryID)
downloadPut = requests.put(url, headers={"accept":"application/json"})

status = downloadPut.status_code
print(downloadPut.content)
print(status)

if status != 200:
    exit("non-200 response code.")

jobStatus = "initiated"

while (jobStatus != "COMPLETED"):
    url = 'https://ped.uspto.gov/api/queries/{}'.format(firstQueryID)
    queryStatus = requests.get(url, headers={'accept' : 'application/json'})

    print(queryStatus.status_code)
    print(queryStatus.content)

    status = queryStatus.status_code
    if status != 200:
        exit("non-200 status code.")

    queryStatusDict = queryStatus.json()
    jobStatus = queryStatusDict["jobStatus"]
    print(jobStatus)
    if jobStatus != "COMPLETED":
        sleep(30)

url = "https://ped.uspto.gov/api/queries/{}/download?format=JSON".format(firstQueryID)
download_file(url)

# status == 400
# while status != 302:
#     url = "https://ped.uspto.gov/api/queries/{}/download?format=JSON".format(firstQueryID)
#     download = requests.get(url, headers={'accept' : 'application/json'})
#     status = download.status_code
#     print(download.content)
#     print(status)

#     if (status != 200 and status != 302):
#         exit("non-200 and non-302 response code.")

#while statusDict[]



# x = requests.post(url, json = myobj)




