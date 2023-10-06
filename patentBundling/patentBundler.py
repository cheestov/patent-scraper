import json
from time import sleep
import requests
from datetime import datetime, timedelta
import threading
import queue
import os.path

# use pandas to turn the JSON into a dataframe and then make it into a csv

# {"searchText":"","fq":["patentIssueDate:[2019-01-01T00:00:00Z TO 2019-01-01T23:59:59Z]"],"fl":"*","mm":"100%","df":"patentTitle","qf":"patentIssueDate appLocationYear appEarlyPubNumber applId appLocation appType appStatus_txt appConfrNumber appCustNumber appGrpArtNumber appCls appSubCls appEntityStatus_txt patentNumber patentTitle primaryInventor firstNamedApplicant wipoEarlyPubNumber pctAppType firstInventorFile appClsSubCls rankAndInventorsList","facet":"false","sort":"applId asc","start":"0"}

def queryformatter(startDate, endDate):
    issueDate = "{}Z TO {}Z".format(startDate.isoformat(), endDate.isoformat())
    variables = "appLocationYear appEarlyPubNumber applId appLocation appType appStatus_txt appConfrNumber appCustNumber appGrpArtNumber appCls appSubCls appEntityStatus_txt patentNumber patentTitle primaryInventor firstNamedApplicant firstNamedApplicantNameList wipoEarlyPubNumber pctAppType firstInventorFile appClsSubCls rankAndInventorsList"
    query = {"searchText":"*:*",
"fq":["patentIssueDate:[{}]".format(issueDate)],
"fl":"*",
"mm":"100%",
"df":"patentTitle",
"qf":"{}".format(variables),
"sort":"applId asc",
"start":"0"}

   # query = json.dumps({"searchText":"firstNamedApplicant:(Google)","fq":["appFilingDate:[2013-01-01T00:00:00Z TO 2013-12-31T23:59:59Z]","appStatus:\"Patented Case\""],"fl":"*","mm":"100%","df":"patentTitle","qf":"appEarlyPubNumber applId appLocation appType appStatus_txt appConfrNumber appCustNumber appGrpArtNumber appCls appSubCls appEntityStatus_txt patentNumber patentTitle primaryInventor firstNamedApplicant appExamName appExamPrefrdName appAttrDockNumber appPCTNumber appIntlPubNumber wipoEarlyPubNumber pctAppType firstInventorFile appClsSubCls rankAndInventorsList","facet":"false","sort":"applId asc","start":"0"})
    return query
    
def download_file(url, index):
    print("Downloading {}...".format(index))
    local_filename = "downloadedData/dataresultsFile_{}.zip".format(index)
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    if os.path.getsize(local_filename) > 80000000:
        os.remove(local_filename)
        return index
        
    return -1

def getQueryResults(queryId, downloadIndex):
    
    ## CHECK STATUS UNTIL CAN DOWNLOAD
    jobStatus = "initiated"
    count = 0
    while (jobStatus != "COMPLETED"):
        url = 'https://ped.uspto.gov/api/queries/{}'.format(queryId)
        queryStatus = requests.get(url, headers={'accept' : 'application/json'})


        status = queryStatus.status_code
        if status != 200:
            exit("non-200 status code.")

        queryStatusDict = queryStatus.json()
        jobStatus = queryStatusDict["jobStatus"]
        print("Download {} : {} {}".format(downloadIndex, queryStatus.status_code, jobStatus))
        print(jobStatus)
        if jobStatus != "COMPLETED":
            count = count + 1
            if (count == 20):
                return downloadIndex
            sleep(30)

    ## DOWNLOAD THE FILE

    url = "https://ped.uspto.gov/api/queries/{}/download?format=JSON".format(queryId)
    returnV = download_file(url, downloadIndex)
    sleep(1.6)
    if (returnV == -1):
        print("SUCCESS on {}".format(downloadIndex))
        return -1
    if (returnV != -1):
        print("FAIL on : {}".format(returnV))

def downloadWorker(q, i):
   # result = getQueryResults(i[0], i[1])

    q.put(i[1])


def failureFixing(failNum):
    # for each week split it into each day or something and if the day fails then we dont get that day or somethig/ or maybe go by hour?
    if len(failNum) == 0:
        return failNum
    newFails = []
    print("Download failure on : {}".format(failNum))
    print("Retrying...")
    for f in range(0, len(failNum)):
        queries = []
        for jid in range(0, 4):
            startDate = datetime.fromisoformat("2019-01-01T00:00:00")
            endDate = datetime.fromisoformat("2019-01-01T00:00:00")
            failChange = timedelta(days=7*failNum[f])
            startDate = startDate + failChange
            endDate = endDate + failChange

            startHourChange = timedelta(hours=42*jid)
            endHourChange = timedelta(hours=42*(jid+1))
            startDate += startHourChange
            endDate += endHourChange
            print("start : {} End : {} ".format(startDate.isoformat(), endDate.isoformat()))

            finalDate = datetime.fromisoformat("2020-01-01T00:00:00")
            postJSON = queryformatter(startDate, endDate)
            downloadIndex = 0
            url = 'https://ped.uspto.gov/api/queries'
            postJSON = queryformatter(startDate, endDate)
            url = 'https://ped.uspto.gov/api/queries'
            queryOne = requests.post(url, json=postJSON, headers={'accept' : 'application/json'})

            #print(postJSON)
            print("query request {} : {}".format(failNum[f], queryOne.status_code))
            #print(queryOne.content)

            if queryOne.status_code != 200 :
                exit("Non-200 OK response.")


            initialDict = queryOne.json()

            firstQueryID = initialDict['queryId']

            print(firstQueryID)

            jobStatus = "initiated"

            ## CHECK IF THE JOB HAS BEEN CREATED

            while (jobStatus != "CREATED"):
                url = 'https://ped.uspto.gov/api/queries/{}'.format(firstQueryID)
                queryStatus = requests.get(url, headers={'accept' : 'application/json'})

                print("query creation check {} : {}".format(failNum[f], queryOne.status_code))

                status = queryStatus.status_code
                if status != 200:
                    exit("non-200 status code.")

                queryStatusDict = queryStatus.json()
                jobStatus = queryStatusDict["jobStatus"]
                print(jobStatus)
                if jobStatus != "CREATED":
                    sleep(30)


            ## THIS IS WHERE WE WILL GET 416 RESPONSE IF IT IS TOO LONG

            url = "https://ped.uspto.gov/api/queries/{}/package?format=JSON".format(firstQueryID)
            downloadPut = requests.put(url, headers={"accept":"application/json"})

            status = downloadPut.status_code
            print(downloadPut.content)
            print(status)

            if status == 200:
                queries.append((firstQueryID, "{}_{}".format(failNum[f], jid)))
            else:
                exit("200 status code")

        print("Download executing...")
        for i in queries:
            download_thread = threading.Thread(target=getQueryResults, args=(i[0], i[1]))
            download_thread.start()
    
    return -1


    
startDate = datetime.fromisoformat("2019-01-01T00:00:00")
endDate = datetime.fromisoformat("2019-01-08T00:00:00")

finalDate = datetime.fromisoformat("2020-01-01T00:00:00")
postJSON = queryformatter(startDate, endDate)
downloadIndex = 0
queries = []
url = 'https://ped.uspto.gov/api/queries'
myobj = {'somekey': 'somevalue'}
complete = 0

while complete != 1:

    ## START OF COMMUNICATING WITH SERVER
    postJSON = queryformatter(startDate, endDate)
    url = 'https://ped.uspto.gov/api/queries'
    queryOne = requests.post(url, json=postJSON, headers={'accept' : 'application/json'})

    #print(postJSON)
    print("query request {} : {}".format(downloadIndex, queryOne.status_code))
    #print(queryOne.content)

    if queryOne.status_code != 200 :
        exit("Non-200 OK response.")


    initialDict = queryOne.json()

    firstQueryID = initialDict['queryId']

    print(firstQueryID)

    jobStatus = "initiated"

    ## CHECK IF THE JOB HAS BEEN CREATED

    while (jobStatus != "CREATED"):
        url = 'https://ped.uspto.gov/api/queries/{}'.format(firstQueryID)
        queryStatus = requests.get(url, headers={'accept' : 'application/json'})

        print("query creation check {} : {}".format(downloadIndex, queryOne.status_code))

        status = queryStatus.status_code
        if status != 200:
            exit("non-200 status code.")

        queryStatusDict = queryStatus.json()
        jobStatus = queryStatusDict["jobStatus"]
        print(jobStatus)
        if jobStatus != "CREATED":
            sleep(30)


    ## THIS IS WHERE WE WILL GET 416 RESPONSE IF IT IS TOO LONG

    url = "https://ped.uspto.gov/api/queries/{}/package?format=JSON".format(firstQueryID)
    downloadPut = requests.put(url, headers={"accept":"application/json"})

    status = downloadPut.status_code
    print(downloadPut.content)
    print(status)

    if status == 200:
        queries.append((firstQueryID, downloadIndex))
        downloadIndex = downloadIndex + 1
        if endDate.isoformat() == "2020-01-01T00:00:00":
            complete = 1
            continue

        timeChange = timedelta(days=7)
        startDate = datetime.fromisoformat(endDate.isoformat())

        endDate = endDate + timeChange
        if (endDate > finalDate) :
            endDate = datetime.fromisoformat(finalDate.isoformat())
    elif status == 416:
        timeChange = timedelta(days=1)
        endDate = endDate - timedelta
        continue
    else:
        exit("non 200 or 416 status code")

print("Download executing...")
queueThing = queue.Queue()
fails = []
threads = []
for i in queries:
    download_thread = threading.Thread(target=downloadWorker, args=(queueThing, i))
    download_thread.start()
    threads.append(download_thread)
for thr in threads:
    thr.join()
for i in queries:
  result = queueThing.get()
  if result != None and result > -1:
      fails.append(result)
  

failureFixing(fails)
print(fails)
print("finished")
# for i in queries:
#     download_thread = threading.Thread(target=getQueryResults, args=(i[0], i[1]))
#     download_thread.start()






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




