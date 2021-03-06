import requests
import os
import json

# 下载k线数据
def downloadKLineData(companyName, companyCode):
    companyInfo = getCompany(companyName, companyCode)
    if companyInfo == None:
        return
    companyCode = companyInfo["companyCode"]
    # companyName = companyInfo["companyName"]
    kLinePrefix = companyInfo["kLinePrefix"]
    if str(kLinePrefix) == "0":
        prefix = "1"
    elif str(kLinePrefix) == "1":
        prefix = "0"
    downloadKLineDataByCode(prefix, companyCode, "19890101", "20210330")


# 获取上市公司信息
#           {
#             "companyCode" : companyCode,
#             "companyName" : companyName,
#             "kLinePrefix" : kLinePrefix
#         }
def getCompany(companyName, companyCode):
    if companyName == None and companyCode == None:
        return
    companyArr = readCompanyInfo()
    for company in companyArr:
        if companyName:
            checkName = companyName == company["companyName"]
        else:
            checkName = True
        if companyCode:
            checkCode = str(companyCode) == company["companyCode"]
        else :
            checkCode = True
        if checkName and checkCode:
            return company


# 下载股票历史数据
# prefix 沪为0 深为1
def downloadKLineDataByCode(prefix, companyCode, start, end):
    resultCompanyCode = str(prefix) + str(companyCode)
    downloadFileUrl = "http://quotes.money.163.com/service/chddata.html?code={}&start={}&end={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP".format(resultCompanyCode, start, end)

    execlDir = "/Users/zhouweiwei/PycharmProjects/quote/com/zhouww/163Money/execl"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Referer": "http://quotes.money.163.com/"
    }
    fileName = str(companyCode) + "_20210330.csv"
    saveFilePath = execlDir + "/" + fileName
    if os.path.exists(saveFilePath):
        return
    companyResponse = requests.get(downloadFileUrl, headers=headers)
    with open(saveFilePath, "wb") as file:
        file.write(companyResponse.content)
    # time.sleep(1)

def downloadAllCompany():
    companyArr = readCompanyInfo()
    idx = 1
    for company in companyArr:
        print("下载中=" + str(company["companyCode"]) + ", idx=" + str(idx))
        downloadKLineData(None, company["companyCode"])
        print("完成下载code=" + str(company["companyCode"]) + ", idx=" + str(idx))
        idx = idx + 1
        # try :
        #     print("下载中=" + str(company["companyCode"]) + ", idx=" + str(idx))
        #     downloadKLineData(None, company["companyCode"])
        #     print("完成下载code=" + str(company["companyCode"]) + ", idx=" + str(idx))
        # except BaseException:
        #     print("下载失败code=" + str(company["companyCode"]) + ", idx=" + str(idx))
        # idx = idx + 1

def readCompanyInfo():
    rootDir = "/Users/zhouweiwei/PycharmProjects/quote/com/zhouww/easyMoney"
    companyFile = rootDir + "/Company.json"
    if os.path.exists(companyFile) == False:
        return
    with open(companyFile, mode='r') as companyReadFile:
        companyJsonStr = companyReadFile.read()
    return json.loads(companyJsonStr)

