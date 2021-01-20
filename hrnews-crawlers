# a crawlers use to grab news and information from hr730 website
import requests
from requests.exceptions import RequestException
import chardet
import urllib.parse
from bs4 import BeautifulSoup
import time
import random
import os
import codecs
import sys

import internetSetting


def getCookies(soup):
    loginUrl = "http://www.hr730.com/account/index/logon"
    account = "user"
    pw = "pw"
    rUrl = "http%3A%2F%2Fwww.hr730.com%2F"
    sf = soup.find("meta",{"name":"SecurityForm"})["content"]
    
    data = {'return_url': rUrl, 'hr730_account': account, 'hr730_pwd': pw, 'remember_login': '1', 'SecurityForm': sf}
    
    ses = requests.Session()
    res = ses.post(loginUrl, data=data, headers=internetSetting.headers, proxies=internetSetting.proxies, verify=False)
    cookies = res.cookies
    cookie = requests.utils.dict_from_cookiejar(cookies)
    return cookie
    

def get_html(url, cookie):
    try:
        ses = requests.Session()
        response = ses.get(url, headers=internetSetting.headers, proxies=internetSetting.proxies, cookies=cookie)

        if response.status_code == 200:
            response.encoding = chardet.detect(response.content).get('encoding')
            html = response.text
            return html
        
    except RequestException:
        print(response)
        return None


def strProcess(s):
    strFilter = ["\n","\r",u'\xa0',"'",'"']
    s = s.strip()
    for ss in strFilter:
        s = s.replace(ss,"")
    return s


def strProcessPunct(s):
    punctuation = "!#$%&'()*+,-./:;<=>?@[\]^_`{|}~＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､　、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。"
    s = s.strip()
    for ss in punctuation:
        s = s.replace(ss,"")
    return s


def saveTxt(items,i):
    n = r"C:\\hr730" + "\\" + str(i) + ".txt"
    file = codecs.open(n,"w+","utf-16")
    for item in items:
        file.write(item)
    file.close()


def main():
    # initial the error list
    errorList = []
    # get SecurityForm from page
    initialUrl = "http://www.hr730.com/"
    html = get_html(initialUrl, "")
    soup = BeautifulSoup(html,"html.parser")
    cookie = getCookies(soup)
    
    for i in range(30000,30001):                                                # article number        
        url = "http://www.hr730.com/home/article/priv/id/{0}".format(i)
        html = get_html(url, cookie)
        soup = BeautifulSoup(html,"html.parser")
        
        try:                                                                    # normal article
            x = soup.find("h1").get_text()                                      # get title
            y = soup.find("h2").get_text()                                      # get subtitle
            zp = soup.find_all('p')                                             # get all paragraph
            
            z = ""                                                              # turn paragraph to a list
            for j in range(0,len(zp)):
                if zp[j].text != "发表评论":                                    # get rid of useless p
                    z = z + zp[j].text

            x = strProcess(x) + '\r\n'                                          # set format
            y = strProcess(y) + '\r\n'
            z = strProcess(z) + '\r\n'
                
            content=[]                                                          # turn xyz into one list
            content.append(x)
            content.append(y)
            content.append(z)

            temp = str(i) + " " + strProcessPunct(x[:-2][:20])                  # remove punctuation marks for file name                 
            print("getting content... ", temp)
            
            saveTxt(content,temp)
            
            
        except Exception:                                                       # if not normal article (dont habe title or subtitle etc.)
            try:
                xp = soup.find_all('p')                                         # get all paragraph
                lt = ['topic_title']                                            # get rid of useless p (the class name of p)
                
                content = []
                for j in range(0,len(xp)):
                    if j < 4:                                                   # for frist 3 of the paragraph, put 2 new lines after it
                        content.append(strProcess(xp[j].text) + '\r\n' + '\r\n')
                    elif xp[j].get('class') == lt:
                        None
                    else:                                                       # for normal paragraph, start a new line after it
                        content.append(strProcess(xp[j].text) + '\r\n')

                temp = str(i) + " " + strProcessPunct(xp[0].text[:7])           # naming
                print("getting content... ", temp)
                
                saveTxt(content, temp)
                
            except Exception as e:
                print("Oops!", e.__class__, "occurred.")
                errorList.append(i)

        slpTime =random.randint(1,8) + random.random()                          # sleep of certain time
        print("sleep for", round(slpTime,4),"secs")
        time.sleep(slpTime)
        
    print("The codes of articles didn't downloaded:",errorList)


if __name__ == '__main__':
    main()
