# -*- coding: utf-8 -*-



from decimal import Decimal

#输入元素为列表的series，每一个列表相同位置的值组成新的列表，输出这个列表集合（嵌套列表）6x13-->13x6
#此处写死，如果constant中的数据有变化，此处要做相应调整
def fenSel(sel):
    dc=sel.to_dict()
    totalList=[[dc["A"][i],dc["B"][i],dc["C"][i],dc["D"][i],dc["E"][i],dc["F"][i],dc["G"][i],dc["H"][i],dc["I"][i],dc["J"][i],dc["K"][i],dc["L"][i],dc["M"][i]] for i in range(6)]
    return  totalList   

#修整数据：除以1000并保留两位小数，所有数据全部变为浮点数
#此处写死，如果constant中的数据有变化，此处要做相应调整
def xiuZheng(totalList):
    for i in range(6):
        for j in range(13):
            totalList[i][j]=Decimal(totalList[i][j])/Decimal(10000)
            totalList[i][j]=totalList[i][j].quantize(Decimal('0.00'))
    for i in range(6):
        for j in range(13):
            totalList[i][j]=float(totalList[i][j])
    return totalList