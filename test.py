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
#t=0
#print(type(t)== int)
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt

# #############################################################################
# Generate sample data
X = np.sort(5 * np.random.rand(40, 1), axis=0)
y = np.sin(X).ravel()

# #############################################################################
# Add noise to targets
y[::5] += 3 * (0.5 - np.random.rand(8))

# #############################################################################
# Fit regression model
svr_rbf = SVR(kernel="rbf", C=100, gamma=0.1, epsilon=0.1)
svr_lin = SVR(kernel="linear", C=100, gamma="auto")
svr_poly = SVR(kernel="poly", C=100, gamma="auto", degree=3, epsilon=0.1, coef0=1)

# #############################################################################
# Look at the results
lw = 2

svrs = [svr_rbf, svr_lin, svr_poly]
kernel_label = ["RBF", "Linear", "Polynomial"]
model_color = ["m", "c", "g"]

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 10), sharey=True)
for ix, svr in enumerate(svrs):
    axes[ix].plot(
        X,
        svr.fit(X, y).predict(X),
        color=model_color[ix],
        lw=lw,
        label="{} model".format(kernel_label[ix]),
    )
    axes[ix].scatter(
        X[svr.support_],
        y[svr.support_],
        facecolor="none",
        edgecolor=model_color[ix],
        s=50,
        label="{} support vectors".format(kernel_label[ix]),
    )
    axes[ix].scatter(
        X[np.setdiff1d(np.arange(len(X)), svr.support_)],
        y[np.setdiff1d(np.arange(len(X)), svr.support_)],
        facecolor="none",
        edgecolor="k",
        s=50,
        label="other training data",
    )
    axes[ix].legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.1),
        ncol=1,
        fancybox=True,
        shadow=True,
    )

fig.text(0.5, 0.04, "data", ha="center", va="center")
fig.text(0.06, 0.5, "target", ha="center", va="center", rotation="vertical")
fig.suptitle("Support Vector Regression", fontsize=14)
plt.show()