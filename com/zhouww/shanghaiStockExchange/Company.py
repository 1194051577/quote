import requests
import os
import json

class Company:
    download_url = "http://query.sse.com.cn/security/stock/getStockListData.do?&jsonCallBack=jsonpCallback98904&isPagination=true&stockCode=&csrcCode=&areaName=&stockType=1&pageHelp.cacheSize=1&pageHelp.beginPage=1&pageHelp.pageSize=10000&pageHelp.pageNo=1&_=1621605306576"
    head_referer = "http://www.sse.com.cn/"

    # 下载 上海证券所的公司信息  结果格式：[{"companyName":"公司名字", "companyCode":"股票代码}]
    def download(self):

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "Referer": self.head_referer
        }
        response = requests.get(self.download_url, headers=headers)
        responseText = response.text

        # projectRootDir = os.path.dirname(os.path.realpath(__file__))
        # originKLineDataPath = projectRootDir + "/shanghaiCompany.txt"
        # with open(originKLineDataPath, "w") as file:
        #     file.write(responseText)

        textStartIdx = responseText.find("(")
        textEndIdx = responseText.rfind(")")
        companyJsonStr = responseText[textStartIdx+1:textEndIdx]
        companyJsonObj = json.loads(s=companyJsonStr, encoding="UTF-8")
        companyArr = companyJsonObj["result"]

        companyResultArr = []
        for companyInfo in companyArr:
            companyResultArr.append({
                "companyName" : companyInfo["COMPANY_ABBR"],
                "companyCode" : companyInfo["COMPANY_CODE"]
            })

        return companyResultArr





















