#!/usr/bin/python3

# 实时下载股票信息
import com.zhouww.excel.ExcelParse
import com.zhouww.shangzheng.CompanyHandle as CompanyHandle
import os

kbcCompanyArrJsonStr = CompanyHandle.queryCompany(8)
zbagCompanyArrJsonStr = CompanyHandle.queryCompany(1)
zbbgCompanyArrJsonStr = CompanyHandle.queryCompany(2)


