from com.zhouww.shanghaiStockExchange.Company import Company as ShanghaiCompany
import json

shCompany = ShanghaiCompany()

arr = shCompany.download()
print(json.dumps(arr))