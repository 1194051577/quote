import requests
import os
import json

import com.zhouww.easyMoney.DownloadCompanyInfo as dci

def downloadKLineData(companyName, companyCode):
    projectRootDir = os.path.dirname(os.path.realpath(__file__))
    companyFile = projectRootDir + "/Company.json"
    if os.path.exists(companyFile) == False:
        dci.queryCompanyInfo("hushenAGu")
    with open(companyFile, mode='r') as companyReadFile:
        companyJsonStr = companyReadFile.read()
    companyArr = json.loads(companyJsonStr)
    for company in companyArr:
        checkResult = True
        if companyName:
            checkResult = checkResult and companyName == company["companyName"]
        if companyCode:
            checkResult = checkResult and companyCode == company["companyCode"]
        if checkResult:
            companyInfo = company
            break

    companyCode = companyInfo["companyCode"]
    companyName = companyInfo["companyName"]
    kLinePrefix = companyInfo["kLinePrefix"]

    kLineUrl = "http://90.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery1124019286645481350484_1615024072347&secid=" + str(kLinePrefix) + "." + str(companyCode) + "&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=1&beg=0&end=20500101&smplmt=460&lmt=1000000&_=1615024072495"
    kLineResult = projectRootDir + "/ResultKLine.json"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Referer": "http://www.sse.com.cn/"
    }
    companyResponse = requests.get(kLineUrl, headers=headers)
    companyResponseText = companyResponse.text
    textStartIdx = companyResponseText.find("(")
    textEndIdx = companyResponseText.rfind(")")
    companyJson = companyResponseText[textStartIdx+1:textEndIdx]
    with open(kLineResult, "w") as file:
        file.write(companyJson)


downloadKLineData(None, "300946")

