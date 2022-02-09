import json
import requests
import time
import getmigu as gm

def getDbID(pid):
    try:
        url = "https://app-sc.miguvideo.com/vms-match/v5/staticcache/basic/basic-data/%s/miguvideo" % pid
        headers = {
            'Accept' : 'application/json, text/plain, */*',
            'terminalId' : 'www',
            'appId' : 'miguvideo',
            'User-Agent' : 'Mozilla/5.0 (X11; Linux amd64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Content-Type' : 'application/json',
            'Origin' : 'https://www.miguvideo.com',
            'Sec-Fetch-Site' : 'same-site',
            'Sec-Fetch-Mode' : 'cors',
            'Sec-Fetch-Dest' : 'empty',
            'Referer' : 'https://www.miguvideo.com/mgs/website/prd/sportsHomePage.html',
            'Accept-Encoding' : 'gzip, deflate, br',
            'Accept-Language' : 'zh-CN,zh;q=0.9',
        }
        res = requests.get(url, headers=headers)
        jsdata = json.loads(res.text)
        return jsdata["body"]["commentaryList"]["preList"]
    except:
        return ""


def pID2Url(pid):
    curl=gm.getMiguContId(pid)
    furl=gm.ddCalcu(curl)
    furl=gm.pushUrl(furl)
    return furl

#js=getDbID('120000204149')
#for ijs in js:
#    print("%s -- %s" % ( ijs["pID"] ,pID2Url(ijs["pID"])))
