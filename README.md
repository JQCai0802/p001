这是一个待完善的项目，目前可以处理两种excel表式，实现三个功能。
表式1：项目调度表，包含的关键字段有：建设地点、产业类别、年度总投资、年度完成投资
表式2：企业调度表，包含的关键字段有：地点、产业类别、营收、利润、利税
目前可以实现的功能有：
功能1：对于表式1，指定：数据源、以上相关字段名，对于每一个产业类别输出一张表，里面根据投资额多少划分为多个分表，并自动计算投资完成率。
功能2：对于表式1，指定：数据源、以上相关字段名，对于每一个产业类别输出一张bar图，横坐标为城市名称，纵坐标为数值（包含总投资、完成投资、完成率）。
功能3：对于表式2，指定：数据源、以上相关字段名，对于每一个关键指标（如营收、利润、利税）分别输出一张bar图，横坐标为城市名称，纵坐标为数值（各产业类别，单位亿元）

使用者可对代码进行细致化调整：
1.constant中存有城市字典和仅针对于表式2的产业类别字典，可按需调整
2.common.py中有几个针对表式1的处理函数和绘图函数是写死的，可按需调整
3.如果修改了constant中的两个字典，transform.py中的两个函数必须做相应调整，common.py中的绘图函数也要做调整
