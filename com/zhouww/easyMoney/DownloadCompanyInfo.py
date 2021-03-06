import requests
import json
import os

# 下载公司信息
def downloadCompany(requestUrl):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Referer": "http://www.sse.com.cn/"
    }
    companyResponse = requests.get(requestUrl, headers=headers)
    return companyResponse.text

# 解析企业信息， 获取代码和名称
def parseCompanyInfo(responseText):
    companyResultArr = []

    textStartIdx = responseText.find("(")
    textEndIdx = responseText.rfind(")")
    companyJson = responseText[textStartIdx+1:textEndIdx]
    pJson = json.loads(companyJson)
    companyArr = pJson["data"]["diff"]
    for beanCompany in companyArr:
        companyCode = beanCompany["f12"]
        companyName = beanCompany["f14"]
        kLinePrefix = beanCompany["f13"]
        companyResultArr.append({
            "companyCode" : companyCode,
            "companyName" : companyName,
            "kLinePrefix" : kLinePrefix
        })
    return companyResultArr


# 默认下载5000条
companyUrlMap = {
    # 沪深A股
    "hushenAGu" : "http://62.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124041826244666583023_1615017690401&pn=1&pz=5000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1615017691388"
}

# 整合企业下载，解析
def queryCompanyInfo(tagName):
    requestResultText = downloadCompany(companyUrlMap[tagName])
    content = parseCompanyInfo(requestResultText)
    projectRootDir = os.path.dirname(os.path.realpath(__file__))
    companyFile = projectRootDir + "/Company.json"
    with open(companyFile, "w") as file:
        file.write(json.dumps(content))


queryCompanyInfo("hushenAGu")


