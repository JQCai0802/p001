# -*- coding: utf-8 -*-

import pandas as pd
from numpy import nan
import numpy as np
import matplotlib.pyplot as plt

class excel001:

    #输入源文件地址及类别字段后输出由每个类别名字组成的列表（通用）
    def getTypes(sourcePath,beginLine,sheetName,key):
        rd=pd.read_excel(sourcePath,sheetName, header=beginLine)
        seriesType=rd[key].unique().tolist()
        return seriesType

    #(无返回值)输入筛选字段及筛选值、分类字段、新加字段、源地址、输出地址、开始行号--->实现将一个表分解成多个表并添加一列（功能1）
    def daoChu(rdType,resultPath,level,newRow,sourcePath,key,beginLine,sheetName):
        #使用read_excel函数将表读为DF，header指定为colume名的那一行
        rd = pd.read_excel(sourcePath,sheetName, header=beginLine)
        rd = rd.replace(nan, 0)
        #指定某一列的值，筛选出满足条件的数据
        rd = rd[rd[key]==rdType]
        #根据某一列值的范围，将数据分为不同的组
        rd0 = rd[rd[level] > 2]
        rd1 = rd[(rd[level] > 1.5)& (rd[level] <=2)]
        rd2 = rd[(rd[level] >= 1)& (rd[level] <=1.5)]
        rd3 = rd[(rd[level] < 1) & (rd[level] >= 0.5)]
        rd4 = rd[(rd[level] < 0.5) & (rd[level] >= 0.2)]
        rd5 = rd[rd[level] < 0.2]
        #给不同组指定编号，存到字典里
        dic={"0":rd0,"1":rd1,"2":rd2,"3":rd3,"4":rd4,"5":rd5}
        #给每一组数据添加一个新的列
        for value in dic.values():
            value[newRow]=value['2023年1-8月完成投资']/value['2023年计划\n完成投资']
        #将数据写入一个excel文件的各个分sheet中
        with pd.ExcelWriter(resultPath) as writer:
            for dic_key in dic.keys():
                dic[dic_key].to_excel(writer,index=False, sheet_name = dic_key)

    #输入表格参数和城市，模糊匹配城市，形成城市专属list数据便于绘图
    def dataArr(rdType,key,sourcePath,beginLine,city,sheetName):
        rd = pd.read_excel(sourcePath,sheetName, header=beginLine)
        rd = rd.replace(nan, 0)
        #第一次筛选，根据是否为某个str（通常用于分类）
        rd = rd[rd[key]==rdType]
        #第二次筛选，根据是否含有某个str
        rd=rd.loc[rd["建设地点"].str.contains(city),:]
        #得到数据条数、两个字段的总和，三个数据组成一个list
        count=rd.shape[0]
        investion=rd['2023年计划\n完成投资'].sum()
        complete=rd['2023年1-8月完成投资'].sum()
        viewList=[count,investion,complete]
        return viewList

    #绘制项目表bar图的函数。输入三个数据列表（13个元素）和一个文件地址，输出一张图。
    def barView(i,investion,complete,ratio,outPath):
        #设置绘图风格
        plt.style.use('ggplot')
        #设置图的rc配置（字典赋值）此处只改了字体
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        bar_width = 0.4
        #横坐标
        labels = ["哈尔滨","齐齐哈尔","牡丹江","佳木斯","大庆","鸡西","双鸭山","伊春","七台河","鹤岗","黑河","绥化","大兴安岭"]
        #绘制第一序列的bar图：传入横纵坐标序列、颜色及图例、柱宽度
        plt.bar(x = np.arange(len(labels)), height = investion, label = '年度总投资', color = 'steelblue', width = bar_width)
        #绘制第二序列的bar图：传入横纵坐标序列，颜色及图例、柱宽度
        plt.bar(x = np.arange(len(labels))+bar_width, height = complete, label = '年度已完成投资', color = 'indianred', width = bar_width)
        #设置x轴的刻度（有刻度位置的数组+城市名字列表）
        plt.xticks(np.arange(13)+0.2,labels,rotation=90,fontsize=10)
        #y坐标和图名
        plt.ylabel('亿元')
        plt.title(f'{i}各地市本年度投资情况')
        #在图中相应位置添加额外的数字（横纵坐标-默认y+1、保留小数位数、对齐）
        for x,y in enumerate(investion):
            plt.text(x,y+1,"%s"%round(y,2),ha='center')      
        for x,y in enumerate(complete):
            plt.text(x+bar_width,y+1,"%s"%round(y,2),ha='center')
        for i in np.arange(13):
            plt.text(-0.1+i,21.5,'%.2f'%ratio[i],fontsize=12, family = "fantasy", color = "r")
        #创建图例、保存、关闭图层
        plt.legend()
        plt.savefig(outPath)
        plt.close()

    #输入某一城市的rd、类别字典、分类字段、关键字字段列表。算每一个字段下几个关键字的总数形成一个列表，再嵌套在一起
    def splitRd(rd,bioDic,field,keyWord):
        dic={}
        list_count=[]
        dicList = [list_count]
        #根据分类字段在城市rd的基础上再细分领域rd，并放入到字典中
        for key,value in bioDic.items():
            dic[key]=rd[rd[field]==value]
        #对于每一个细分领域rd计算几个关键字段的总数，放入列表
        for key in dic.keys():
            list_count.append(dic[key].shape[0])
        for i in keyWord:
            listTemp = []
            for key in dic.keys():
                listTemp.append(dic[key][i].sum())
            dicList.append(listTemp)
        return dicList

    #输入13x6嵌套列表，纵坐标图例、标题、输出地址、保留位数，输出图像
    def barView2(listIn,ylabel,title,outPath,i):
        #画幅、风格、rc配置
        plt.figure(figsize=(18,10))
        plt.style.use('ggplot')
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        bar_width = 0.15
        labels = ["哈尔滨","齐齐哈尔","牡丹江","佳木斯","大庆","鸡西","双鸭山","伊春","七台河","鹤岗","黑河","绥化","大兴安岭"]
        #给定横纵坐标序列，注意间距，画6次，一次画13个。
        plt.bar(x=np.arange(len(labels)),height=listIn[0],label='生物医药',color='steelblue',width=bar_width)
        plt.bar(x=np.arange(len(labels))+bar_width,height=listIn[1],label='生物农业',color='green',width=bar_width)
        plt.bar(x=np.arange(len(labels))+bar_width*2,height=listIn[2],label='生物制造',color='red',width=bar_width)
        plt.bar(x=np.arange(len(labels))+bar_width*3,height=listIn[3],label='生物能源',color='yellow',width=bar_width)
        plt.bar(x=np.arange(len(labels))+bar_width*4,height=listIn[4],label='生物环保',color='grey',width=bar_width)
        plt.bar(x=np.arange(len(labels))+bar_width*5,height=listIn[5],label='生物医学工程',color='purple',width=bar_width)
        #横纵坐标、标题
        plt.xticks(np.arange(13)+0.3,labels,rotation=90,fontsize=10)
        plt.ylabel(ylabel)
        plt.title(title)
        #给柱状图添加数值，添加6次。
        for x,y in enumerate(listIn[0]):
            if(y!=0):
                plt.text(x,y+0.1,"%s"%round(y,i),ha='center') 
        for x,y in enumerate(listIn[1]):
            if(y!=0):
                plt.text(x+bar_width,y+0.1,"%s"%round(y,i),ha='center') 
        for x,y in enumerate(listIn[2]):
            if(y!=0):
                plt.text(x+bar_width*2,y+0.1,"%s"%round(y,i),ha='center') 
        for x,y in enumerate(listIn[3]):
            if(y!=0):
                plt.text(x+bar_width*3,y+0.1,"%s"%round(y,i),ha='center') 
        for x,y in enumerate(listIn[4]):
            if(y!=0):
                plt.text(x+bar_width*4,y+0.1,"%s"%round(y,i),ha='center') 
        for x,y in enumerate(listIn[5]):
            if(y!=0):
                plt.text(x+bar_width*5,y+0.1,"%s"%round(y,i),ha='center') 
        plt.legend()
        plt.savefig(outPath)
        plt.close()
        
    def pie(list_totalCount,title,outPath):
        total=sum(list_totalCount)
        fig, ax = plt.subplots()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.axis('off')
        plt.rcParams['font.sans-serif']=['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus']=False
        plt.axes(aspect='equal')
        ax=plt.pie(x=list_totalCount,  #绘图数据
                labels = ["哈尔滨","齐齐哈尔","牡丹江","佳木斯","大庆","鸡西","双鸭山","伊春","七台河","鹤岗","黑河","绥化","大兴安岭"],  #添加教育水平标签
                autopct=lambda p:'{:.2f}'.format(p*total*0.01),
                labeldistance=1.1,#设置教育水平标签与圆心的距离
                pctdistance=0.5,
                startangle=180,#设置饼图的初始角度
                radius=1.2,#设置饼图的半径
                counterclock=False,#是否逆时针，这里设置为顺时针方向
                wedgeprops={'linewidth':1, 'edgecolor':'green'},#设置饼图内外边界的属性值
                textprops={'fontsize':8, 'color':'black'},#设置文本标签的属性值
                )
        plt.tight_layout()
        plt.title(title)
        plt.savefig(outPath)
        plt.close(fig)
        
        
        
        
        
        
        