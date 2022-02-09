from urllib import parse
import requests
import json
import sys

def ddCalcu(url):
    new_url = parse.urlparse(url)
    para = dict(parse.parse_qsl(new_url.query))
    userid = para.get("userid","")
    timestamp = para.get("timestamp","")
    ProgramID = para.get("ProgramID","")
    Channel_ID = para.get("Channel_ID","")
    puData = para.get("puData","")
    t = userid if userid else "eeeeeeeee" 
    r = timestamp if timestamp else "tttttttttttttt"
    n = ProgramID if ProgramID else "ccccccccc"
    a = Channel_ID if Channel_ID else "nnnnnnnnnnnnnnnn"
    o = puData if puData else ""
    if not o:
        return url
    s = list("2624")
    u = list(t)[int(s[0])] or "e"
    l = list(r)[int(s[1])] or "t"
    c = list(n)[int(s[2])] or "c"
    f = list(a)[len(a)-int(s[3])] or "n"
    d = list(o)
    h = []
    p = 0
    while p*2 < len(d):
        h.append(d[len(d)-p-1])
        if p < len(d) - p -1:
            h.append(o[p])
        if p == 1:
            h.append(u)
        if p == 2:
            h.append(l)
        if p == 3:
            h.append(c)
        if p == 4:
            h.append(f)
        p += 1
    v = "".join(h)
    return url + "&ddCalcu=" + v
 

def getMiguContId(cid):
    try:
        url = "https://webapi.miguvideo.com/gateway/playurl/v3/play/playurl?contId=%s&rateType=3&startPlay=true&flvEnable=true" % cid
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
        cobeurl=jsdata["body"]["urlInfo"]["url"]
        return cobeurl
    except:
        return ""

if __name__ == '__main__':
    xcode='713587377'
    try:
        xcode=sys.argv[1]
    except:
        pass
    curl=getMiguContId(xcode)#20220209008')
    #24小时：713587377
    #雪上    713591450
    #冰上    713589837    
    furl=ddCalcu(curl)
    print(furl)
