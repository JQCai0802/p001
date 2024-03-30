from tools import constant
from tools.common import excel001


#功能2：项目表可视化
#可调整项
#地市字典：在constant中指定
cityDic = constant.cityDic
#sheet名
sheetName="704+444=1148"
#用来分类的字段名，每一类会生成一个独立的结果
key='产业类别'
#源文件地址及开始行数
sourcePath="D:\datasite01\python-working-site\p001\产业振兴项目1148（1-8月）111.xls"
beginLine=2
resultType=excel001.getTypes(sourcePath,beginLine,sheetName,key)

#遍历各产业门类
for i in resultType:
    # 存各城市项目数量，13个元素
    list_totalCount = []
    # 存各城市总计划投资数
    list_totalInvestion = []
    # 存各城市投资完成数
    list_totalComplete = []
    # 存各城市投资完成率
    list_totalratio = []
    #固定类别的基础上，遍历各城市
    for value in cityDic.values():
        #得到该地市数据列表（项目数、年度投资、完成投资）
        listReturn = excel001.dataArr(i, key, sourcePath, beginLine, value, sheetName)
        #笨方法，将每一行的每个元素分配到一个新的行中，相当于将矩阵的列变成行
        list_totalCount.append(listReturn[0])
        list_totalInvestion.append(listReturn[1])
        list_totalComplete.append(listReturn[2])
    #对于两列同一位置的两项做一个除法，排除除0报错
    list_totalratio = [a / b if b != 0 else 0 for a, b in zip(list_totalComplete, list_totalInvestion)]
    excel001.barView(i,list_totalInvestion, list_totalComplete, list_totalratio, f"D:\datasite01\python-working-site\p001\output\{i}.png")


# 1132表将特定产业筛出，每个地市算三个总数，形成饼状图以图片形式输出至文件夹
# excel001.pie(list_totalCount,'生物经济个数',"D:\高技术处2023\输出\个数.png")
# excel001.pie(list_totalInvestion,'生物经济总数',"D:\高技术处2023\输出\总数.png")
# excel001.pie(list_totalComplete,'生物经济已完成',"D:\高技术处2023\输出\已完成.png")


