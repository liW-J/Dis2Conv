#-*- coding:utf-8 -*-
import jieba
import re
import random
import csv
import time
import os

def clear(txt,dic):
    with open(txt, 'r', encoding='utf8', newline='') as f1:
        with open(dic, 'r', encoding='utf8', newline='') as f2:
            sentence=f1.read()
            sentenceList=sentence.split("\r\n")
            print(sentenceList)
            word=f2.read()
            wordList=word.split("\r\n")
            wordList.remove("")
            flag = True
            for i in sentenceList:
                for j in wordList:
                    if j in i :
                        flag=False
                    else:
                        None
            if flag==True:
                with open("sentence.txt", 'a', encoding='utf8', newline='') as f3:
                    f3_csv = csv.writer(f3)
                    f3_csv.writerow(sentenceList)
# 遍历文件夹
def walkFile(file):
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            #print(os.path.join(root, f))
            clear(os.path.join(root, f), "中医疾病与病征编码.txt")
        # 遍历所有的文件夹
        for d in dirs:
            #print(os.path.join(root, d))
            clear(os.path.join(root, d), "中医疾病与病征编码.txt")




def cemkg(txt,dic=[]):
   with open(txt, 'r') as f4:
       file=f4.read()
       file=file.split("\n")
       for word in file:
           dic.append(word)
       dic.remove('')


def Records(line,disease=[], symptom=[], expriement=[], medical=[]):
    records={"疾病":[],"症状":[],"药物":[],"检查":[]}
    # for disease, symptom, expriement, medical in zip(disease, symptom, expriement, medical):
    #     if disease in line:
    #         records["疾病"].append(disease)
    #     if symptom in line:
    #         records["症状"].append(symptom)
    #     if expriement in line:
    #         records["检查"].append(expriement)
    #     if medical in line:
    #         records["药物"].append(medical)
    for a in disease:
        if a in line:
            print(a)
            records["疾病"].append(a)
    for b in symptom:
        if b in line:
            records["症状"].append(b)
    for c in expriement:
        if c in line:
            records["检查"].append(c)
    for d in medical:
        if d in line:
            records["药物"].append(d)



    return records

def word (txt):
    with open(txt, 'r', encoding='utf8', newline='') as f5:
        tigger=[]
        for line in f5.readlines():
            line=line.strip("\r\n")
            tigger.append(line)
        return tigger
def tigger1 (line ,dic=[],kind=[]):
    for i in dic:
        if i in line:
            kind.append(i)
    return kind

def tigger2 (line ,dic=[],kind=[]):

    # print(line)
    j=line.split(",")
    print(j)
    for k in j:
        if "婚育史" in k:
            print(k)
            l=k.split("，")
            print(l)
            for m in l:
                for i in dic:
                    if i in m:
                        print(m)
                        if m in kind:
                            pass
                        else:
                            kind.append(m)
    return kind

def Ran(dic=[]):
    if len(dic)>3:
        for i in dic :
            random.seed(time.time() + random.randint(0, 50))
            Random = random.randint(0, 1)
            if Random==1:
                dic.remove(i)
            if len(dic)<=3:
                break
            else:
                Ran(dic)
    return dic


if __name__ =='__main__':
    disease=[]
    symptom=[]
    expriement=[]
    medical=[]
    cemkg("./具体实现/CMeKG词库（爬取于CMeKG中文医学知识图谱）-质量最佳/疾病.txt",disease)
    cemkg("./具体实现/CMeKG词库（爬取于CMeKG中文医学知识图谱）-质量最佳/症状.txt",symptom)
    cemkg("./具体实现/CMeKG词库（爬取于CMeKG中文医学知识图谱）-质量最佳/药物.txt",medical)
    cemkg("./具体实现/CMeKG词库（爬取于CMeKG中文医学知识图谱）-质量最佳/检查诊疗技术.txt",expriement)
    walkFile("./病历/")

    with open("sentence.txt","r",encoding='utf8',newline='') as f:
        for line in f:

            sentence=line.split(",")
            kinds = ["主诉", "现病史", "既往史", "辅助检查", "初步诊断"]
            for i in sentence:
                for kind in kinds:
                    if kind in i:
                        file = str(kind) + ".txt"
                        with open(file, "a", encoding='utf8', newline='') as ff:
                            records=Records(i,disease,symptom,expriement,medical)
                            ff.write(str(records))
                            ff.write("\n")
                    else:
                        continue
