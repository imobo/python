import os
import time

logfile = os.getcwd() + "//" + "log.txt"

def logger(*items):
    global logfile
    stringSum = ""
    file = open(logfile, "a")
    for item in items:
        stringSum = stringSum + " " + str(item)
    print(stringSum)
    logTime = "%s-%s-%s %s:%s:%2s " %  time.localtime(time.time())[:6]
    file.write(logTime + "   " + stringSum + "\n")
    file.close()