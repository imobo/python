from logger import logger
import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

useProxies = 1
wanbianAppid = 1111
wanbianAppkey = ""
fixedProxies = ""

class getProxy:
    def __init__(self):
        global useProxies
        global wanbianAppid
        global wanbianAppkey
        global fixedProxies
        self.useProxies = useProxies
        self.wanbianAppid = wanbianAppid
        self.wanbianAppkey = wanbianAppkey
        self.fixedProxies = fixedProxies
        # redis relating url
        self.proxyPoolRedisUrl = 'http://localhost:5555/random'
        # url to return my ip
        self.checkIpUrl = "https://ifconfig.co/"
        # wanbian relating url
        self.wanbianUrl = "http://ip.ipjldl.com/index.php/api/entry?"
        self.wanbianData = {
            'method': 'proxyServer.tiqu_api_url',
            'packid': 0,
            'fa': 0,
            'dt': '',
            'groupid': 0,
            'fetch_key': '',
            'qty': 1,
            'time': 1,
            'port': 1,
            'format': 'txt',
            'ss': 1,
            'css': '',
            'pro': '',
            'city': '',
            'usertype': 6,
        }
        self.wanbianGetWlUrl = "https://www.wanbianip.com/Users-whiteIpListNew.html?"
        self.wanbianAddWlUrl = "https://www.wanbianip.com/Users-whiteIpAddNew.html?"
        self.wanbianDelWlUrl = "https://www.wanbianip.com/Users-whiteIpDelNew.html?"
        self.wanbianBalWlUrl = "https://www.wanbianip.com/Users-getBalanceNew.html?"

    def getProxyFromWanbian(self):
        url = self.getDataSumUrl(self.wanbianData, self.wanbianUrl)
        proxies ={'http': '', 'https': ''}
        if self.useProxies == 1:
            if self.fixedProxies == "":
                logger("[MESSAGE] Get proxies from wanbian...")
                # logger("Use dynamic proxies...")
                while proxies['http'] == "" or proxies['http'] == None:
                    proxies = self.getProxyInLoop(url)
                    proxies = self.proxyInDict(proxies)
                return proxies
            else:
                logger("[MESSAGE] Use fixed proxies...")
                return self.proxyInDict(self.fixedProxies)
        else:
            logger("[MESSAGE] Execute without proxies...")
            return proxies

    def getDataSumUrl(self, dataDict, baseUrl):
        # get url in format likes: baseUrl? key1=value1& key2=value2
        dataSum = ""
        for key, item in dataDict.items():
            dataSum = dataSum + "&" + key + "=" + str(item)
        url = baseUrl + dataSum
        return url

    def getProxyFromPool(self, poolUrl):
        try :
            response = requests.get(poolUrl)
            if response.status_code == 200:
                return response.text
        # except ConnectionError:
        except Exception :
            return None

    def getProxyInLoop(self, poolUrl):
        temp = self.getProxyFromPool(poolUrl)
        if temp is not None:
            logger("[SUCCESS] Get proxies successfully. The proxy settings is", temp)
            return temp
        else:
            logger("[FAIL] Fail to get proxies.")
            return None

    def proxyInDict(self, s):
        proxiesDict = {'http': s, 'https': s}
        return proxiesDict

"""
    def getMyIp(self):
        res = requests.get(self.checkIpUrl, verify=False)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            ip = soup.find('code', {"class": "ip"}).text
            logger("[SUCCESS] Get local ip:", ip)
            return ip
        else:
            logger("[FAIL] Fail to get local ip")
            return False

    def addWhitelistWanbian(self):
        logger("[MESSAGE] Try to add local ip to wanbian whitelist")
        if self.wanbianAppid != "" and self.wanbianAppkey != "":
            data = {
                'appid': self.wanbianAppid,
                'appkey': self.wanbianAppkey,
            }
            try:
                # get balance
                res = requests.get(self.getDataSumUrl(data, self.wanbianBalWlUrl), verify=False)
                bal = json.loads(res.text)["data"]
                logger("[MESSAGE] Getting current balance in wanbian, the balance is:", bal)
                # get current whitelist ip
                res = requests.get(self.getDataSumUrl(data, self.wanbianGetWlUrl), verify=False)
                currentWhitelist = json.loads(res.text)["data"]
                logger("[MESSAGE] Getting current whitelist in wanbian, the current whitelist is:", currentWhitelist)
                # empty the whitelist
                for ip in currentWhitelist:
                    data["whiteip"] = ip
                    res = requests.get(self.getDataSumUrl(data, self.wanbianDelWlUrl), verify=False)
                    logger("[MESSAGE] Empting the whitelist, the result is:", res.text)
                # add local ip to whitelist
                data["whiteip"] = self.getMyIp()
                res = requests.get(self.getDataSumUrl(data, self.wanbianAddWlUrl), verify=False)
                logger("[MESSAGE] Adding local ip to whitelist, the result is:", res.text, "\n")
            except Exception:
                logger("[MESSAGE] Fail to add local ip to wanbian whitelist. Execute without add whitelist\n")
        else :
            logger("[FAIL] appid and appkey are not exist. Execute without add whitelist\n")
"""


def requestUrl(ses, url, data, headers, proxies, func="post", changeIp=True):
    resStatus = True
    while resStatus == True:
        if changeIp == True:
            proxies = getProxy().getProxyFromWanbian()
        try :
            # post or get
            if func == "post":
                response = ses.post(url, data=data, headers=headers, proxies=proxies, verify=False, timeout=30)
            elif func == "get":
                response = ses.get(url, headers=headers, proxies=proxies, verify=False, timeout=30)
            # check res status
            if response.status_code == 200:
                #logger("[SUCCESS] Requests success.", url[:50])
                resStatus == False
                # return respomse and new proxies
                return response, proxies
        except Exception:
            logger("[FAIL] Requests failure. Change proxies and try again.")
            changeIp = True
