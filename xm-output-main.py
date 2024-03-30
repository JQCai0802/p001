# -*- coding: utf-8 -*-
from unittest import result

from tools.common import excel001

#功能1：项目表批量导出功能
#将所有项目分类别输出，每一类中再按年度投资金额将项目放入各分表
level="2023年计划\n完成投资"
newRow='完成率'
sourcePath="D:\datasite01\python-working-site\p001\产业振兴项目1148（1-8月）111.xls"
key='产业类别'
beginLine=2
sheetName="704+444=1148"
resultType=excel001.getTypes(sourcePath,beginLine,sheetName,key)
for i in resultType:
    excel001.daoChu(i,f"D:\datasite01\python-working-site\p001\output\{i}.xls",level,newRow,sourcePath,key,beginLine,sheetName)




        










