
import requests
import json
from lxml import etree

# 科创板 http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=8
# 主板A股 http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=1
# 主板B股 http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=2
# 下载公司信息
def downloadCompany(stockType, targetFilePath):
    companyUrl = "http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=" + stockType
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Referer": "http://www.sse.com.cn/"
    }
    companyResponse = requests.get(companyUrl, headers=headers)
    with open(targetFilePath, "wb") as file:
        file.write(companyResponse.content)

# 查询企业信息
def queryCompany(stockType):
    queryCompanyUrl = "http://query.sse.com.cn/security/stock/getStockListData.do?&jsonCallBack=jsonpCallback20997&isPagination=true&stockCode=&csrcCode=&areaName=&stockType=" + str(stockType) + "&pageHelp.cacheSize=1&pageHelp.beginPage=1&pageHelp.pageSize=2000&pageHelp.pageNo=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Referer": "http://www.sse.com.cn/"
    }
    queryCompanyResponse = requests.get(queryCompanyUrl, headers=headers)
    responseText = queryCompanyResponse.text
    textStartIdx = responseText.find("(")
    textEndIdx = responseText.rfind(")")
    responseJsonStr = responseText[textStartIdx+1:textEndIdx]
    pJson = json.loads(responseJsonStr)
    resultFieldJson = pJson["result"]
    return json.dumps(resultFieldJson)

# 查询股票信息
def queryStock(companyCode):
    queryStockUrl = "http://www.sse.com.cn/assortment/stock/list/info/price/index.shtml?COMPANY_CODE=" + str(companyCode)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Referer": "http://www.sse.com.cn/"
    }
    queryStockResponse = requests.get(queryStockUrl, headers=headers)
    responseText = queryStockResponse.text
    print(responseText)
    html = etree.HTML(responseText)
    print(html.xpath('//*[@id="pad01"]/table/tbody/tr[1]/td[2]/h1'))





