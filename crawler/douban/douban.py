import time
import csv
import requests
from bs4 import BeautifulSoup
from net import getProxy
from net import requestUrl
from logger import logger

checkTimeLimit = 10
dataFn = "DBtopic"
urlCol = 2

commonHeader = {
    "Host": "www.douban.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    }


def getSoup(url, headers, proxies):
    ses = requests.Session()
    res, proxies = requestUrl(ses, url, "", headers, proxies, "get", False)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        return soup
    else :
        logger("[FAIL] Fail to get web content")
        return False


def getDBTopic(s):
    """@ para: s - beautiful soup object"""
    topics = []
    try:
        tds = s.find_all("td",class_='title')
        for td in tds:
            row = td.parent.find('a')
            title = row["title"]
            titleUrl = row["href"]
            temp = [title, titleUrl]
            topics.append(temp)
    except Exception:
        logger("[FAIL] Fail to get content of Topic")
        return False
    logger("[SUCCESS] Get", len(topics), "topic in total")
    return topics


def getNext(s):
    try:
        a = s.find("span",class_='next').parent.find_all("a")
        last = a[-1]
        return(last["href"])
    except Exception:
        return None


def mainGetDBTopic(groupId):
    # get header
    global commonHeader
    global dataFn
    global checkTimeLimit
    # get Proxies
    proxies = getProxy().getProxyFromWanbian()
    # initialize
    allTopic = []
    topicPage = 0
    increment = 25
    checkTime = 0
    # loop
    while True:
        logger("[MESSAGE] Start get topic data in page", ((topicPage + increment) / increment))
        # get topic
        url = "https://www.douban.com/group/{0}/discussion?start={1}".format(groupId, topicPage)
        s = getSoup(url, commonHeader, proxies)
        res = getDBTopic(s)
        # handle soup
        if len(res) != 0 and res != False:
            allTopic.append(res)
            topicPage += increment
        # when IP got ban, or get
        elif len(res) == 0:
            logger("[MESSAGE] Something happened, Change IP and continue after 10 seconds")
            time.sleep(10)
            proxies = getProxy().getProxyFromWanbian()
            s = getSoup(url, commonHeader, proxies)
            check = getNext(s)
            checkTime = checkTime + 1
            if check != None and checkTime < checkTimeLimit:
                continue
            else:
                logger("[MESSAGE] Got all topic in group")
                break
        else:
            logger("[MESSAGE] Error occur when trying to get topic")
            break
    # write result to csv file
    for i in range(0, len(allTopic)):
        for j in range(0, len(allTopic[i])):
            writeCSV(allTopic[i][j], dataFn)


def mainGetComment():
    global dataFn
    global urlCol
    topicUrls = readCSV(dataFn, urlCol)
    logger("[MESSAGE] Get", len(topicUrls),"elements from CSV file in column", urlCol)
    # initialize proxies
    proxies = getProxy().getProxyFromWanbian()
    for topicUrl in topicUrls:
        getCommentInTopic(topicUrl, proxies)

def getCommentInTopic(topicURL, proxies):
    global commonHeader
    s = getSoup(topicURL, commonHeader, proxies)



def readCSV(fn, col):
    fn = fn + ".csv"
    result = []
    with open(fn, encoding='utf8') as file:
        content = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in content:
            if row != []:
                result.append(row[col-1])
        return result

def writeCSV(l,fn):
    fn = fn + ".csv"
    with open(fn, mode='a', encoding='utf8') as file:
        content = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        content.writerow(l)


if __name__ == '__main__' :
    # get group id
    groupId = 700000
    # execute
    #mainGetDBTopic(groupId)
    mainGetComment()
