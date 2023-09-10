import json
import requests

# use pandas to turn the JSON into a dataframe and then make it into a csv

# {"searchText":"","fq":["patentIssueDate:[2019-01-01T00:00:00Z TO 2019-01-01T23:59:59Z]"],"fl":"*","mm":"100%","df":"patentTitle","qf":"patentIssueDate appLocationYear appEarlyPubNumber applId appLocation appType appStatus_txt appConfrNumber appCustNumber appGrpArtNumber appCls appSubCls appEntityStatus_txt patentNumber patentTitle primaryInventor firstNamedApplicant wipoEarlyPubNumber pctAppType firstInventorFile appClsSubCls rankAndInventorsList","facet":"false","sort":"applId asc","start":"0"}

def querymaker(year):
    issueDate = "{}-01-01T00:00:00Z TO {}-01-01T23:59:59Z".format(year, year)
    variables = "patentIssueDate appLocationYear appEarlyPubNumber applId appLocation appType appStatus_txt appConfrNumber appCustNumber appGrpArtNumber appCls appSubCls appEntityStatus_txt patentNumber patentTitle primaryInventor firstNamedApplicant firstNamedApplicantNameList wipoEarlyPubNumber pctAppType firstInventorFile appClsSubCls rankAndInventorsList"

    query = json.dumps({"searchText":"",
"fq":["appFilingDate:[2019-01-01T00:00:00Z TO 2019-01-01T23:59:59Z]"],
"fl":"*",
"mm":"100%",
"df":"patentTitle",
"qf":"patentIssueDate appLocationYear appEarlyPubNumber applId appLocation appType appStatus_txt appConfrNumber appCustNumber appGrpArtNumber appCls appSubCls appEntityStatus_txt patentNumber patentTitle primaryInventor firstNamedApplicant firstNamedApplicantNameList wipoEarlyPubNumber pctAppType firstInventorFile appClsSubCls rankAndInventorsList",
"facet":"false",
"sort":"applId asc",
"start":"0"})

   # query = json.dumps({"searchText":"firstNamedApplicant:(Google)","fq":["appFilingDate:[2013-01-01T00:00:00Z TO 2013-12-31T23:59:59Z]","appStatus:\"Patented Case\""],"fl":"*","mm":"100%","df":"patentTitle","qf":"appEarlyPubNumber applId appLocation appType appStatus_txt appConfrNumber appCustNumber appGrpArtNumber appCls appSubCls appEntityStatus_txt patentNumber patentTitle primaryInventor firstNamedApplicant appExamName appExamPrefrdName appAttrDockNumber appPCTNumber appIntlPubNumber wipoEarlyPubNumber pctAppType firstInventorFile appClsSubCls rankAndInventorsList","facet":"false","sort":"applId asc","start":"0"})
    return query
    

postJSON = querymaker("2019")
print(postJSON)

url = 'https://ped.uspto.gov/api/queries'
myobj = {'somekey': 'somevalue'}


#print(requests.get(url='https://ped.uspto.gov/api/search-params').status_code)
#exit()


postJSON = {"searchText":"",
"fq":["appFilingDate:[2019-01-01T00:00:00Z TO 2019-01-01T23:59:59Z]"],
"fl":"*",
"mm":"100%",
"df":"patentTitle",
"qf":"patentIssueDate appLocationYear appEarlyPubNumber applId appLocation appType appStatus_txt appConfrNumber appCustNumber appGrpArtNumber appCls appSubCls appEntityStatus_txt patentNumber patentTitle primaryInventor firstNamedApplicant firstNamedApplicantNameList wipoEarlyPubNumber pctAppType firstInventorFile appClsSubCls rankAndInventorsList",
"facet":"false",
"sort":"applId asc",
"start":"0"}
queryOne = requests.post(url, json=postJSON, headers={'accept' : 'application/json'})

print(queryOne.status_code)
print(queryOne.content)

if queryOne.status_code != 200 :
    exit("Non-200 OK response.")

initialJSON = queryOne.json()
initialJSON_dict = json.load(initialJSON)

queryResult_dict = initialJSON_dict['queryResults']

firstQueryID = initialJSON_dict['queryId']
responseQueryID = queryResult_dict['queryId']
print(firstQueryID)
print(responseQueryID)




# x = requests.post(url, json = myobj)




