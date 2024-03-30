# -*- coding: utf-8 -*-

import pandas as pd
from numpy import nan
from tools import constant
from tools.common import excel001
from tools import transform

#功能3：解析企业表，算各城市各领域关键指标，每一个指标单独一张图
bioDic=constant.bioDic
cityDic=constant.cityDic
#存储（城市代号：对应的rd）序列
rdDic={}
#存储（城市代号：嵌套列表）
testDic={}
#根据需要调整
sourcePath="D:\datasite01\python-working-site\p001\企业1-12.xls"
sheetName="3"
#字段1
place="地点"
#字段2
field="所属领域"
#关键指标字段
keyWord=["营业收入","利润总额","上缴税金"]

#读表
rd = pd.read_excel(sourcePath,sheetName, header=2)
rd = rd.replace(nan, 0)
for key,value in cityDic.items():
    #将rd以城市拆分，并存到字典里
    rdDic[key]=rd.loc[rd[place].str.contains(value,na=False),:]
    #将城市rd再通过领域拆分，算出每个领域的关键数总和，返回嵌套列表
    #字典的格式为：{城市名：[[1领域数量，1领域关键数1总量，1领域关键数2总量，......]，]}
    testDic[key]=excel001.splitRd(rdDic[key],bioDic,field,keyWord)
#将字典转回rd
df=pd.DataFrame(testDic)

#计数部分单独画一个图
selCount=df.loc[0]
totalCount=transform.fenSel(selCount)
excel001.barView2(totalCount, '个', '各地市企业数', "D:\datasite01\python-working-site\p001\output\企业个数.png", 0)

#对每一个关键指标分别画图
for i in range(1,df.shape[0]):
    selTemp=df.loc[i]
    totalTemp=transform.xiuZheng(transform.fenSel(selTemp))
    excel001.barView2(totalTemp, '亿元', keyWord[i-1], f"D:\datasite01\python-working-site\p001\output\{keyWord[i-1]}.png", 2)








   