from datetime import datetime
from bs4 import BeautifulSoup
import re
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import config

def getsoup(url, headers, cookies):
    ses = requests.Session()
    res = ses.get(url, headers=headers, cookies=cookies, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")
    #soup = BeautifulSoup(res.text,'lxml')
    return soup


def getRoomGrid(content):
    q = []
    n = []
    # find td for getting the room name
    x = content.find_all("td",{"class":"fistTow","style":"width:51px; border-right:1px solid #CCC"})
    # find td (start of the grid)
    a = content.find(valign="middle",align="center")
    b = a
    # for every room 
    for i in range(0,len(x)):
        # get meeting room name
        q.append(x[i].get_text())
        # get data in the grid (9 * 7 day)
        stateList = []
        for j in range(0,7):
            tempList = []
            for k in range(0,9):
                c = b.find_next("div",{"style":"cursor:pointer"})
                state = c.get("class")
                flag = 0
                if state == None:
                    flag = 0
                elif keywordCheck(state) == 1:
                    flag = 1
                b = c
                tempList.append(flag)
            stateList.append(tempList)
            #print( i + 1,len(stateList), q[i], "    ", stateList[j])
        n.append(stateList)
    # q: a list of room names, n: a list of reservation of meeting room.
    return q, n


def keywordCheck(l):
    f = 0
    keyword = ['orange', 'firstOne orange','lastOne orange']
    for e in range(len(l)):
        if l[e] in keyword:
            f = 1
    return f


def roomSizeMap(roomName):
    big = ["room1","room2"]
    small = ["room3","room4","room5","room6","room7"]

    f = 0
    if roomName in big:
        #print(roomName,"is big")
        f = 1
    elif roomName in small:
        #print(roomName,"is small")
        f = 2
    return f


def gbUrlEncoder(string):
    temp = string.encode("gb2312")
    temp = str(temp)
    temp = temp.replace("\\x","%").replace("b'","").replace("'","")
    return temp


def postUrl(headers, cookies, tf, rm, bookDate, bookid, mode, sub="无标题"):
    if tf is not None:
        bd = bookDate +"+"+ timeMapping(tf)[0]
        ed = bookDate +"+"+ timeMapping(tf)[1]
    else:
        pass

    td = datetime.now().strftime("%Y-%m-%d")
    rmId = roomMapping(rm)
    sub = gbUrlEncoder(sub)
    d = bookDate
    if config.bookname != "":
        bookUsername = gbUrlEncoder(config.bookname)
    else:
        bookUsername = cookies["name"]
    bookUserid = bookid
    dept = gbUrlEncoder(config.dept)
    tel = config.tel
    
    if mode[:6] == "single":
        url = config.submitUrl + "?updateFlag=0&bookingId=&timeFlags={0}&beginDate={1}&endDate={2}&\
bookUsername={7}&crDate={3}&bookUserid={8}&room={4}&subject={5}&meetingDate={6}&timeFlag={0}&department={9}&linkMan={7}&\
linkTel={10}&remark=bookedByPythonScript".format(tf, bd, ed, td, rmId, sub, d, bookUsername, bookUserid, dept, tel)
        
    elif mode == "hA":
        url = config.submitUrl + "?updateFlag=&bookingId=&timeFlags=1234&beginDate={0}+08%3A30%3A00&\
endDate={0}+12%3A30%3A00&bookUsername={4}&crDate={1}&bookUserid={5}&room={2}&subject={3}&meetingDate={0}&timeFlag=1&timeFlag=2&\
timeFlag=3&timeFlag=4&department={6}&linkMan={4}&linkTel={7}&remark=bookedByPythonScript".format(bookDate, td, rmId, sub, bookUsername, bookUserid, dept, tel)

    elif mode == "hP":
        url = config.submitUrl + "?updateFlag=&bookingId=&timeFlags=5678&beginDate={0}+13%3A00%3A00&\
endDate={0}+17%3A00%3A00&bookUsername={4}&crDate={1}&bookUserid={5}&room={2}&subject={3}&meetingDate={0}&timeFlag=5&timeFlag=6&\
timeFlag=7&timeFlag=8&department={6}&linkMan={4}&linkTel={7}&remark=bookedByPythonScript".format(bookDate, td, rmId, sub, bookUsername, bookUserid, dept, tel)

    elif mode == "whole":
        url = config.submitUrl + "?updateFlag=&bookingId=&timeFlags=12345678&beginDate={0}+08%3A30%3A00&\
endDate={0}+17%3A00%3A00&bookUsername={4}&crDate={1}&bookUserid={5}&room={2}&subject={3}&meetingDate={0}&timeFlag=1&timeFlag=2&\
timeFlag=3&timeFlag=4&timeFlag=5&timeFlag=6&timeFlag=7&timeFlag=8&department={6}&linkMan={4}&linkTel={7}&remark=bookedByPythonScript".format(bookDate, td, rmId, sub, bookUsername, bookUserid, dept, tel)

    r = requests.post(url, headers=headers, cookies=cookies, verify=False)
    return r


def roomMapping(rm):
    rmDict = {
        "room1":2,
        "room2":4,
        "room3":6,
        "room4":9,
        "room5":11,
        "room6":16,
        "room7":17,
        "room8":19,
        "room9":21,
        "room10":24,
        "room11":25
        }
    roomFlag = rmDict.get(rm)
    return roomFlag


def timeMapping(tf):
    tDict = {
        1:"8%3A30%3A00,9%3A30%3A00",
        2:"9%3A30%3A00,10%3A30%3A00",
        3:"10%3A30%3A00,11%3A30%3A00",
        4:"11%3A30%3A00,12%3A30%3A00",
        5:"13%3A00%3A00,14%3A00%3A00",
        6:"14%3A00%3A00,15%3A00%3A00",
        7:"15%3A00%3A00,16%3A00%3A00",
        8:"16%3A00%3A00,17%3A00%3A00",
        9:"17%3A00%3A00,23%3A59%3A00"
        }
    timeStr = tDict.get(tf).split(",")
    startT = timeStr[0]
    endT = timeStr[1]
    return startT,endT


def weekdayMapping(d):
    #周一返回0、周日返回6
    wd = datetime.strptime(d, '%Y-%m-%d').weekday()
    return wd


def changeContentUrl(d):
    bookingUrl = config.bookingUrl
    url = bookingUrl + '?bookDate={0}'.format(d)
    return url


def getRangeForIndex(mode):
    rIndex =[0,0]
    if mode == "hA":
        rIndex[0], rIndex[1] = 0, 4
    elif mode == "hP":
        rIndex[0], rIndex[1] = 5, 8
    elif mode == "whole":
        rIndex[0], rIndex[1] = 0, 8
    elif mode[:6] == "single":
        rIndex[0], rIndex[1] = int(mode[6:])-1, int(mode[6:])
    return rIndex


def roomAvailabilityCheck(mode, bookDate, n, r, rmSize=None):
    # get room flag form room size
    if rmSize == "big":
        rmF = 1
    elif rmSize == "small":
        rmF = 2
    elif rmSize == None:
        rmF = 0
    
    for i in range(0,len(n)):
        # get the room fited size, if specificed
        if roomSizeMap(n[i]) ==  rmF or rmSize == None:
            j = weekdayMapping(bookDate)
            kRange = getRangeForIndex(mode)
            availability = 1
            # check availability of room, if not (==1) set flag = 0 (availability)
            for k in range(kRange[0],kRange[1]): 
                if r[i][j][k] == 1:
                    availability = 0
                    #print(n[i]," is NOT available in",bookDate,timeMapping(k)[0].replace("%3A",":"),"-",timeMapping(k)[1].replace("%3A",":"))
                #print(n[i]," is available in",bookDate,timeMapping(k)[0].replace("%3A",":"),"-",timeMapping(k)[1].replace("%3A",":"))

            # if available
            if availability == 1:
                print(n[i],"is available in ",bookDate,timeMapping(kRange[0]+1)[0].replace("%3A",":"),"-",timeMapping(kRange[1])[1].replace("%3A",":"))
                print("Room check end.")
                #return room name
                return n[i]

    print("Room check end. NO room is available.")
    return None


def getResContent(url, headers, cookies):
    res = requests.get(url, headers=headers, cookies=cookies, verify=False)
    return res.content


def getCaptchaByHand(headers, cookies):
    from PIL import Image
    from os import remove
    imgUrl = config.imgUrl
    saveUrl = config.saveUrl + r"\temp.jpg"
    # get new captcha
    with open(saveUrl,"wb") as f:
        img = getResContent(imgUrl, headers, cookies)
        f.write(img)
    # save as image
    img = Image.open(saveUrl)
    img.save(saveUrl)
    img.show()
    # enter code by hand
    captchaCode = input("Enter the validation code: ")
    # delete cache
    remove(saveUrl)
    return captchaCode


def loginGetCookies(idcode, pw, headers):
    # get cookies(cookie1 = 'JSESSIONID')
    firstLoginUrl = config.firstLoginUrl
    ses = requests.Session()
    res = ses.get(firstLoginUrl, headers=headers, verify=False)
    cookies = res.cookies
    cookie1 = requests.utils.dict_from_cookiejar(cookies)

    # use the same cookies get captcha
    from base64 import b64encode
    a = b64encode(idcode)
    b = b64encode(pw)
    c = getCaptchaByHand(headers, cookie1)
    data = {'name': a,'password': b,'code': c,'type': '1'}
    
    # login
    loginUrl = config.loginUrl
    res = ses.post(loginUrl, data=data, headers=headers, verify=False)
    # get cookies
    cookies = res.cookies
    # turn to dict ( cookies2 = 'name')
    cookie2 = requests.utils.dict_from_cookiejar(cookies)
    # 2 in 1 ({'JSESSIONID': 'aaa245q4tLH2gcTQuapqx', 'name': '000000'})
    try:
        cookie1['name']= cookie2['name']
    except Exception:
        print("Failed to get cookies")
        return None
    print("Get cookies successfully.",cookie1)
    return cookie1


def loginStatusCheck(headers, cookies):
    LoginCheckUrl = config.LoginCheckUrl
    cont = getResContent(LoginCheckUrl, headers, cookies)
    soup = BeautifulSoup(cont,"html.parser")
    # find: <script>alert('你还没有登陆，请先登陆')</script>
    s = soup.find('script').text
    if s == "alert('你还没有登陆，请先登陆')":
        print("Login failed")
        return 0
    else:
        print("Login successed")
        return 1


def getAppointmentId(headers, cookies, d):
    # post url of requesting appointment data in day d.
    data = {
	"pageid": "1",
	"startDate": d,
	"startHour": "",
	"startMinute": "",
	"endDate": d,
	"endHour": "",
	"endMinute": "",
	"roomid": "",
	"subject": ""
    }
    res = requests.post(config.queryUrl, headers=headers, cookies=cookies, data=data, verify=False)
    soup = BeautifulSoup(res.text,"html.parser")

    appointmentId = []
    try:
        s = soup.find_all("a")
        for i in s:
            if i.text == "取消预定":
                appointmentId.append(str(i)[34:][:5])
        print("Find", len(appointmentId), "appointment(s) at", d)
        return appointmentId
    except Exception:
        print("Find no appointment at", d)
        pass


def cancelAppointment(headers, cookies, appoId):
    cUrl = config.cancelUrl + str(appoId)
    res = getResContent(cUrl, headers=headers, cookies=cookies)
    print("Cancel query have been sent. The appointment id is", appoId)

        
def bookLoop(url, headers, cookies, sub, mode, bookDate, rmSize, rmNum):
    # loop room num
    for num in range(0,rmNum):
        s = getsoup(url, headers, cookies)
        n ,r = getRoomGrid(s)
        # get bookUserid from page
        flameUrl = config.flameUrl
        sBookid = getsoup(flameUrl, headers, cookies)
        bookid = sBookid.find("input",{"name":"bookUserid"})["value"]
        # get room name if available
        rmName = roomAvailabilityCheck(mode, bookDate, n, r, rmSize)
        # if room is available
        if rmName is not None:
            # get tf (a number if specificed(single), None if not(hA/hP/whole))
            if mode[:6] == "single":
                tf = int(mode[6:])
            else:
                tf = None
            postUrl(headers, cookies, tf, rmName, bookDate, bookid, mode, sub)
            print("booking data sent.","Room:",rmName)
            

def main():
    headers = config.headers
    status = 0
    
    while True:
        if status == 1:
            # get cookies
            cookies = cookie
            modeSelect = int(input("Select a Mode: 1 (fix pattern booking) or 2 (normal booking) or 3(cancel appointment), \nor enter 9 to exit the program."))
            if modeSelect != 9:
                bookDate = input("Enter booking date(YYYY-MM-DD,YYYY-MM-DD).")
                bookDates = bookDate.split(",")
            else:
                print("Exit program")
                exit()
                
            if modeSelect == 1:
                # loop 2 times
                for tempTime in range(0,2):
                    # parameters for first loop
                    if tempTime == 0:
                        mode = "whole"
                        rmNum = 1
                        sub = "sub"
                        rmSize = "big"
                    # parameters for second loop
                    elif tempTime == 1:
                        mode = "hP"
                        rmNum = 2
                        sub = "sub"
                        rmSize = "small"
                    # book meeting room using parameters defined above
                    for bookDate in range(0,len(bookDates)):
                        url = changeContentUrl(bookDates[bookDate])
                        bookLoop(url, headers, cookies, sub, mode, bookDates[bookDate], rmSize, rmNum)
                        print("Completed",bookDates[bookDate],"booking.")
                        print("  ") 

            elif modeSelect == 2:
                temp = input("Enter booking time. 1 for AM, 2 for PM, 3 for Whole Day, 4 for an hour.")
                if temp == "1":
                    mode = "hA"
                if temp == "2":
                    mode = "hP"
                if temp == "3":
                    mode = "whole"
                if temp == "4":
                    mode = "single" + input("Enter a number in range of 1 - 8.(eg: 1 = 8:30-9:30）.")
                    
                rmNum = int(input("How many room do you want? Enter a number."))
                sub = input("Enter name of the meeting.")
                rmSize = input("Enter the require size of room(big,small), if any.")
                if rmSize=="":
                    rmSize = None

                for bookDate in range(0,len(bookDates)):
                    url = changeContentUrl(bookDates[bookDate])
                    bookLoop(url, headers, cookies, sub, mode, bookDates[bookDate], rmSize, rmNum)
                    print("Completed",bookDates[bookDate],"booking.")
                    print("  ")

            elif modeSelect == 3:
                for bookDate in bookDates:
                    # get the id of appointment in query page
                    appoIds = getAppointmentId(headers, cookies, bookDate)
                    # if appointment existed
                    if appoIds != []:
                        # cancel every appointment in that day
                        for appoId in appoIds:
                            cancelAppointment(headers, cookies, appoId)
                    
        else:
            print("Try to login")
            cookie = loginGetCookies(config.idcode, config.pw, headers)
            status = loginStatusCheck(headers, cookie)
            #time.sleep(3)


if __name__ == "__main__":
    main()
