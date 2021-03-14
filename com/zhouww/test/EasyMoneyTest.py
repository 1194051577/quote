from com.zhouww.easyMoney.KLine import KLine


kline = KLine()
# print(kline.downloadDay(companyCode="600460", yearMonthDay="20210203"))
# print(kline.downloadMonth(companyCode="600460", yearMonth="202103"))
# print(kline.downloadYear(companyCode="600460", year="2021"))
print(kline.downloadDayRange(companyCode="600460", startYearMonthDay="20210205", endYearMonthDay="20210312", fqType="不复权"))
print(kline.downloadDayRange(companyCode="600460", startYearMonthDay="20210205", endYearMonthDay="20210312", fqType="前复权"))
print(kline.downloadDayRange(companyCode="600460", startYearMonthDay="20210205", endYearMonthDay="20210312", fqType="后复权"))
