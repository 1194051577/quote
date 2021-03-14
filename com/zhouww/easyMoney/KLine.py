import requests
import os
import json
import calendar
import datetime
import csv

import com.zhouww.easyMoney.DownloadCompanyInfo as dci

class KLine:
    kLineType_Day = 'day'
    kLineType_Week = 'week'
    kLineType_Month = 'month'
    kLineType_5 = '5 minutes'
    kLineType_15 = '15 minutes'
    kLineType_30 = '30 minutes'
    kLineType_60 = '60 minutes'

    kltMap = {
        kLineType_Day : "101",
        kLineType_Week : "102",
        kLineType_Month : "103",
        kLineType_5 : "5",
        kLineType_15 : "15",
        kLineType_30 : "30",
        kLineType_60 : "60"

    }

    def downloadYear(self, companyCode, kLineType="day", year="init"):
        if "init" == year or len(str(year)) != 4:
            now = datetime.datetime.now()
            year = now.year

        startDate = str(year) + "0101"
        endDate = str(year) + "1231"
        return self.downloadKLine(companyCode=companyCode, startDate=startDate, endDate=endDate, kLineType=kLineType)

    def downloadMonth(self, companyCode, kLineType="day", yearMonth="init"):
        if "init" == yearMonth or len(str(yearMonth)) != 6:
            now = datetime.datetime.now()
            year = now.year
            month = now.month
        else:
            pYearMonth = datetime.datetime.strptime(yearMonth, "%Y%m")
            year = pYearMonth.year
            month = pYearMonth.month
        dayRangeArr = calendar.monthrange(year, month)

        startDate = datetime.datetime(year=year, month=month, day=1).strftime("%Y%m%d")
        endDate = datetime.datetime(year=year, month=month, day=dayRangeArr[1]).strftime("%Y%m%d")
        return self.downloadKLine(companyCode=companyCode, startDate=startDate, endDate=endDate, kLineType=kLineType)

    def downloadDay(self, companyCode, kLineType="day", yearMonthDay = "init"):
        if "init" == yearMonthDay or len(str(yearMonthDay)) != 8:
            now = datetime.datetime.now()
            yearMonthDay = now.strftime("%Y%m%d")

        return self.downloadKLine(companyCode=companyCode, startDate=yearMonthDay, endDate=yearMonthDay, kLineType=kLineType)

    def downloadDayRange(self, companyCode, startYearMonthDay, endYearMonthDay="init", kLineType="day"):
        if "init" == startYearMonthDay or len(str(startYearMonthDay)) != 8:
            now = datetime.datetime.now()
            startYearMonthDay = now.strftime("%Y%m%d")

        if "init" == endYearMonthDay or len(str(endYearMonthDay)) != 8:
            now = datetime.datetime.now()
            endYearMonthDay = now.strftime("%Y%m%d")
        return self.downloadKLine(companyCode=companyCode, startDate=startYearMonthDay, endDate=endYearMonthDay, kLineType=kLineType)


    def downloadKLine(self, companyCode, startDate, endDate, kLineType="day", resultFilePath="init", kLinePrefix="init"):
        if "init" == kLinePrefix:
            companyInfo = self.getCompany(None, companyCode)
            kLinePrefix = companyInfo["kLinePrefix"]

        if "init" == resultFilePath:
            projectRootDir = os.path.dirname(os.path.realpath(__file__))
            resultFilePath = projectRootDir + "/ResultKLine.csv"

        klt = self.kltMap[kLineType]

        kLineUrl = "http://51.push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112401951851412976897_1615119901825&secid="  + str(kLinePrefix) + "." + str(companyCode) \
                   +  "&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=" + str(klt) \
                   + "&fqt=1&beg=" + startDate \
                   + "&end=" + endDate \
                   + "&smplmt=460&lmt=1000000&_=1615119901851"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "Referer": "http://quote.eastmoney.com/"
        }
        companyResponse = requests.get(kLineUrl, headers=headers)
        companyResponseText = companyResponse.text

        projectRootDir = os.path.dirname(os.path.realpath(__file__))
        originKLineDataPath = projectRootDir + "/originKLineData.txt"
        with open(originKLineDataPath, "w") as file:
            file.write(companyResponseText)

        textStartIdx = companyResponseText.find("(")
        textEndIdx = companyResponseText.rfind(")")
        companyJson = companyResponseText[textStartIdx+1:textEndIdx]
        companyJsonObj = json.loads(s=companyJson, encoding="UTF-8")
        dataObj = companyJsonObj["data"]
        if dataObj == None:
            return
        klines = dataObj["klines"]
        if klines == None:
            return

        resultList = [];
        with open(resultFilePath, "w") as file:
            csvWriter = csv.writer(file)
            csvWriter.writerow(["日期", "开盘", "收盘", "最高", "最低", "成交量", "成交额", "振幅", "涨跌幅", "涨跌额", "换手率"])
            for lineStr in klines:
                lineSplits = lineStr.split(",")
                lineResult = {
                    "riqi" : lineSplits[0],
                    "kaipan": lineSplits[1],
                    "shoupan": lineSplits[2],
                    "zuigao": lineSplits[3],
                    "zuidi": lineSplits[4],
                    "chengjiaoliang": lineSplits[5],
                    "chengjiaoe": lineSplits[6],
                    "zhenfu": lineSplits[7],
                    "zhangdiefu": lineSplits[8],
                    "zhangdiee": lineSplits[9],
                    "huanshoulv": lineSplits[10]
                }
                resultList.append(lineResult)
                csvWriter.writerow([lineSplits[0], lineSplits[1], lineSplits[2], lineSplits[3], lineSplits[4], lineSplits[5], lineSplits[6], lineSplits[7], lineSplits[8], lineSplits[9], lineSplits[10]])

        return resultList

    # 获取上市公司信息
    #           {
    #             "companyCode" : companyCode,
    #             "companyName" : companyName,
    #             "kLinePrefix" : kLinePrefix
    #         }
    def getCompany(self,companyName, companyCode):
        if companyName == None and companyCode == None:
            return
        companyArr = self.readCompanyInfo()
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

    def readCompanyInfo(self):
        projectRootDir = os.path.dirname(os.path.realpath(__file__))
        companyFile = projectRootDir + "/Company.json"
        if os.path.exists(companyFile) == False:
            dci.queryCompanyInfo("hushenAGu")
        with open(companyFile, mode='r') as companyReadFile:
            companyJsonStr = companyReadFile.read()
        return json.loads(companyJsonStr)

    def saveKlineData(self, kLineDataArr):
        pass



kline = KLine()
# print(kline.downloadDay(companyCode="600460", yearMonthDay="20210203"))
# print(kline.downloadMonth(companyCode="600460", yearMonth="202103"))
# print(kline.downloadYear(companyCode="600460", year="2021"))
print(kline.downloadDayRange(companyCode="600460", startYearMonthDay="20210205", endYearMonthDay="20210312"))


