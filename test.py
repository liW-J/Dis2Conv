# # import re
# # r="1子2女"
# # _*_ coding:utf8 _*_
# import re
#
# res = '1女' #想要取到这个字符串里面id对应的值（23）
#
# # （.）匹配所有字符，（+）匹配一个或多个，（？）非贪懒，以这文本为例匹配到id:"之后的，就不在匹配,如果不加？会匹配到23, "s
# # re.findall返回数据类型为数组，加了[0]意思返回匹配到的第一个值，要是想获取第2，3个，后面可以加[1],[2]
# s1 = re.findall('(.+?)子', res)
# s2 = re.findall('(.+?)女', res)
# print(s1,s2)
# import time
# import time
# import json
# import jionlp as jio
# text = '''患者家属代诉今晨09时左右起床后突发言语困难不适'''
# res = jio.ner.extract_time(text, time_base=time.time() ,with_parsing=False)
# # print(json.dumps(res, ensure_ascii=False, indent=4, separators=(',', ':')))
# print(res)
# s="123初步诊断：123456"
# index=s.find("初步诊断：")
# print(index)
t=0
print(type(t)== int)