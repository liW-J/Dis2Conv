import csv
import os
import re
import time
import json
import jionlp as jio


path_list = []
ks_list = []
found_num = 0
def get_txt(file_pathname=r'.\脑梗死病历原始数据 3352份脱敏txt'):
    a = 0
    global path_list
    for filename in os.listdir(file_pathname):
        path = os.path.join(r'.\脑梗死病历原始数据 3352份脱敏txt',filename)
        path_list.append(path)

def write_ks(txt,ff,key,records):
    with open(txt, 'r', encoding='UTF-8') as fff:
        talk = fff.readlines()
        num = records[key]
        # print(num)
        key = ""
        for j in num:
            if j == num [-1]:
                key += j
            else:
                key += j + "、"

        for x in talk:
            x = x.replace("______", key, 1)
            ff.write(x)


def kids(ff,row):
    txt = "./模板./5婚育史./2.txt"
    with open(txt, 'r', encoding='UTF-8') as fff:
        talk = fff.readlines()
    s2 = re.findall('子(.\d?)女', row)
    if s2 == []:
        key1 = "没有"
    else:
        key1 = s2[0]+"个"

    s1 = re.findall('，(.\d?)子', row)
    if s1 == []:
        key2 = "没有"
    else:
        key2 = "有"+s1[0]+"个"

    for x in talk:
        x = x.replace("______", key1, 2)
        x = x.replace(key1, key2, 1)
        ff.write(x)




def kind_question(kind,file,row):
    with open(file, "a", encoding='utf8', newline='') as ff:
        if kind=="主诉":
            newrow=row.split(":")
            txt="./模板./1主诉./1.txt"
            with open(txt, 'r', encoding='UTF-8') as fff:
                talk=fff.readlines()
                for x in talk:
                    x = x.replace("______",newrow[-1] , 1)
                    if newrow[-1][-1]=="。":
                        x = x.replace("。", "", 1)
                    ff.write(x)
        if kind=="现病史":
            BB=""
            newrow = re.split('[，。；]', row)
            disease = []
            symptom = []
            expriement = []
            medical = []
            cemkg("./具体实现/CMeKG词库（爬取于CMeKG中文医学知识图谱）-质量最佳/疾病.txt", disease)
            cemkg("./具体实现/CMeKG词库（爬取于CMeKG中文医学知识图谱）-质量最佳/症状.txt", symptom)
            cemkg("./具体实现/CMeKG词库（爬取于CMeKG中文医学知识图谱）-质量最佳/药物.txt", medical)
            cemkg("./具体实现/CMeKG词库（爬取于CMeKG中文医学知识图谱）-质量最佳/检查诊疗技术.txt", expriement)
            ffile = str(kind) + ".txt"
            NOTffile = "否定"+str(kind) + ".txt"
            records = {"疾病": [], "症状": [], "药物": [], "检查": []}
            NOTrecords = {"疾病": [], "症状": [], "药物": [], "检查": []}
            with open(ffile, "a", encoding='utf8', newline='') as ffile:
                with open(NOTffile, "a", encoding='utf8', newline='') as NOTffile:
                    for i in newrow:
                        #否认回答
                        if "否认" in i:
                            name = i.replace(":", "")
                            name = name.replace("否认", "")
                            # 否认词
                            txt = "./模板./3既往史./1.txt"
                            with open(txt, 'r', encoding='UTF-8') as fff:
                                talk = fff.readlines()
                                for x in talk:
                                    x = x.replace("______", name, 1)
                                    ff.write(x)
                        #找出否认疾病等
                        elif ("无" in i) and ("无力" not in i):
                            NOTrecords = Records(i, NOTrecords, disease, symptom, expriement, medical)
                        #找出肯定疾病等
                        else:
                            # print(records)
                            records = Records(i, records, disease, symptom, expriement, medical)
                            # print(i)


                    #对肯定疾病、症状提问
                    if records["疾病"] != []:
                        # print(records)
                        txt = "./模板./2现病史./5.txt"
                        write_ks(txt, ff, "疾病", records)
                        # 否认的症状
                    if records["症状"] != []:
                        txt = "./模板./2现病史./6.txt"
                        write_ks(txt, ff, "症状", records)


                    #对时间提问
                    for i in newrow:
                        res = jio.ner.extract_time(i, time_base=time.time(), with_parsing=False)
                        # print(res)
                        if res!=[] and records["疾病"]!=[]:
                            for j in records["疾病"]:
                                if (j in i) and (re.findall('(.\d?)年(.\d?)月(.\d?)日',res[0]['text'])==[]) and (re.findall('(.\d?)-(.\d?)-(.\d?)', res[0]['text']) == []):

                                    # print(i)
                                    # print(res)
                                    # print(j)
                                    if res[0]['type']=='time_span':
                                        t="持续多久了"
                                    if res[0]['type']=='time_point':
                                        t="什么时候开始的"

                                    D="你的"+j+t
                                    P=res[0]['text']
                                    TIME(D,P,ff)

                        if res != [] and records["症状"] != []:
                            for j in records["症状"]:
                                if (j in i) and (re.findall('(.\d?)年(.\d?)月(.\d?)日', res[0]['text']) == []) and (re.findall('(.\d?)-(.\d?)-(.\d?)', res[0]['text']) == []):


                                    if res[0]['type'] == 'time_span':
                                        t = "持续多久了"
                                    if res[0]['type'] == 'time_point':
                                        t = "什么时候开始的"

                                    D = "你的" + j + t
                                    P = res[0]['text']
                                    TIME(D, P,ff)

                        # 排便情况
                        if "便" in i:
                            list=i.split("、")
                            for k in list:
                                if "便" in k:
                                    BB+= k+","



                    # 否认的疾病
                    if NOTrecords["疾病"] != []:
                        # print(records)
                        txt = "./模板./2现病史./1.txt"
                        write_ks(txt, ff, "疾病", NOTrecords)
                    # 否认的症状
                    if NOTrecords["症状"] != []:
                        txt = "./模板./2现病史./2.txt"
                        write_ks(txt, ff, "症状", NOTrecords)
                    #排便情况
                    if BB !="":
                        BB=BB[:-1]
                        txt = "./模板./2现病史./4.txt"
                        with open(txt, 'r', encoding='UTF-8') as fff:
                            talk = fff.readlines()
                            for x in talk:
                                x = x.replace("______", BB, 1)
                                ff.write(x)

                    NOTffile.write(str(NOTrecords))
                    NOTffile.write("\n")
                ffile.write(str(records))
                ffile.write("\n")
        if kind=="既往史":
            newrow = re.split('[，。；]',row)
            disease = []
            symptom = []
            expriement = []
            medical = []

            cemkg("./具体实现/CMeKG词库（爬取于CMeKG中文医学知识图谱）-质量最佳/疾病.txt", disease)
            cemkg("./具体实现/CMeKG词库（爬取于CMeKG中文医学知识图谱）-质量最佳/症状.txt", symptom)
            cemkg("./具体实现/CMeKG词库（爬取于CMeKG中文医学知识图谱）-质量最佳/药物.txt", medical)
            cemkg("./具体实现/CMeKG词库（爬取于CMeKG中文医学知识图谱）-质量最佳/检查诊疗技术.txt", expriement)
            ffile = str(kind) + ".txt"
            records = {"疾病": [], "症状": [], "药物": [], "检查": []}
            with open(ffile, "a", encoding='utf8', newline='') as ffile:
                for i in newrow:
                    if "否认" in i:
                        name = i.replace(":","")
                        name = name.replace("否认", "")
                        #否认词
                        txt = "./模板./3既往史./1.txt"
                        with open(txt, 'r', encoding='UTF-8') as fff:
                            talk = fff.readlines()
                            for x in talk:
                                x = x.replace("______", name, 1)
                                ff.write(x)
                    else:
                        # print(records)
                        records = Records(i,records, disease, symptom, expriement, medical)

                ffile.write(str(records))
                ffile.write("\n")
            #曾患过什么疾病
            if records["疾病"]!=[]:
                # print(records)
                txt = "./模板./3既往史./2.txt"
                write_ks(txt, ff, "疾病", records)
            #曾吃过什么药物
            if records["药物"]!=[]:
                txt = "./模板./3既往史./3.txt"
                write_ks(txt, ff, "药物", records)

            # 曾有什么症状
            if records["症状"] != []:
                txt = "./模板./3既往史./4.txt"
                write_ks(txt, ff, "症状", records)

        if kind=="个人史":
            newrow = re.split('[，。；]', row)
            for i in newrow:
                if "否认" in i:
                    name = i.replace(":", "")
                    name = name.replace("否认", "")
                    txt = "./模板./4个人史./1.txt"
                    with open(txt, 'r', encoding='UTF-8') as fff:
                        talk = fff.readlines()
                        for x in talk:
                            x = x.replace("______", name, 1)
                            ff.write(x)
        if kind=="婚育史":
            row = row.replace("婚育史", "")
            #婚育情况
            marriage={"婚":"未婚","育":"未育"}
            H=["婚育","已婚已育","已婚"]
            Y=["婚育","已婚已育","已育"]
            for n in H:
                if n in row:
                    marriage["婚"]="已婚"
            # print(marriage)
            for m in Y:
                if m in row:
                    # print(m)
                    marriage["育"]="已育"
            txt = "./模板./5婚育史./1.txt"
            with open(txt, 'r', encoding='UTF-8') as fff:
                talk = fff.readlines()
                for x in talk:
                    x = x.replace("______",marriage["婚"], 1)
                    x = x.replace("______",marriage["育"], 1)
                    ff.write(x)
            #子女个数
            if marriage["育"]=="已育":
                kids(ff,row)
                # print(123)
            #初潮年龄
            menarche=re.findall('(.\d?)岁初潮', row)
            if  menarche!=[]:
                txt = "./模板./5婚育史./3.txt"
                with open(txt, 'r', encoding='UTF-8') as fff:
                    talk = fff.readlines()
                    for x in talk:
                        x = x.replace("______", menarche[0], 1)
                        ff.write(x)
            #绝经年龄
            newrow = re.split('[，。；]', row)
            for i in newrow:
                if "绝经" in i:
                    menopause = re.findall('(.\d?)', i)
                    if menopause!=[]:
                        key=","+menopause[0]+"岁时绝经的"
                    else:
                        key = ""

                    txt = "./模板./5婚育史./4.txt"
                    with open(txt, 'r', encoding='UTF-8') as fff:
                        talk = fff.readlines()
                        for x in talk:
                            x = x.replace("______", key, 1)
                            ff.write(x)
            #经期时间
                if "经期" in i:
                    menstruation = re.findall('[-0-9]{3}', i)
                    if menstruation != []:
                        key =  menstruation[0]
                        txt = "./模板./5婚育史./5.txt"
                        with open(txt, 'r', encoding='UTF-8') as fff:
                            talk = fff.readlines()
                            for x in talk:
                                x = x.replace("______", key, 1)
                                ff.write(x)
                    else:
                        pass
            #既往月经量
                if '既往月经量正常' in i:
                    txt = "./模板./5婚育史./6.txt"
                    with open(txt, 'r', encoding='UTF-8') as fff:
                        talk = fff.readlines()
                        for x in talk:
                            x = x.replace("______", key, 1)
                            ff.write(x)
            #白带
                if '白带正常' in i:
                    txt = "./模板./5婚育史./7.txt"
                    with open(txt, 'r', encoding='UTF-8') as fff:
                        talk = fff.readlines()
                        for x in talk:
                            x = x.replace("______", key, 1)
                            ff.write(x)






        if kind=="家族史":
            newrow = row.split("，")
            for i in newrow:
                if "未患有与患者类似疾病" in i:
                    txt = "./模板./6家族史./2.txt"
                    with open(txt, 'r', encoding='UTF-8') as fff:
                        talk = fff.readlines()
                        for x in talk:

                            ff.write(x)
                if "父母已故" in i:
                    txt = "./模板./6家族史./3.txt"
                    with open(txt, 'r', encoding='UTF-8') as fff:
                        talk = fff.readlines()
                        for x in talk:

                            ff.write(x)
                if "否认" in i:
                    name = i.replace(":", "")
                    name = name.replace("家族史", "")
                    name = name.replace("否认", "")
                    txt = "./模板./6家族史./1.txt"
                    with open(txt, 'r', encoding='UTF-8') as fff:
                        talk = fff.readlines()
                        for x in talk:
                            x = x.replace("______", name, 1)
                            if name[-1] == "。":
                                x = x.replace("。", "", 1)
                            ff.write(x)
        if kind=="体格检查":
            pass
        if kind=="辅助检查":
            pass
        if kind=="初步诊断":
            print(row)
            row=row.replace("五、初步诊断:","")
            txt = "./模板./9初步诊断./1.txt"
            with open(txt, 'r', encoding='UTF-8') as fff:
                talk = fff.readlines()
                for x in talk:
                    x = x.replace("______", row, 1)
                    ff.write(x)
        if kind=="补充诊断":
            pass

def cemkg(txt,dic=[]):
   with open(txt, 'r') as f4:
       file=f4.read()
       file=file.split("\n")
       for word in file:
           dic.append(word)
       dic.remove('')

def TIME(D,P,ff):
    txt = "./模板./2现病史./3.txt"
    with open(txt, 'r', encoding='UTF-8') as f:
        talk = f.readlines()
        for x in talk:
            x = x.replace("________", D, 1)
            x = x.replace("______", P, 1)

            ff.write(x)

def Records(line,records,disease=[], symptom=[], expriement=[], medical=[]):

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
        if a in line and (a not in records["疾病"]):
            # print(a)

            records["疾病"].append(a)
    for b in symptom:
        if b in line and (b not in records["症状"]):
            records["症状"].append(b)
    for c in expriement:
        if (c in line) and (c not in records["检查"]):
            records["检查"].append(c)
    for d in medical:
        if (d in line) and (d not in records["药物"]):
            records["药物"].append(d)
            # print(line)
            # print(d)
    return records







def read_txt():
    global path_list
    global ks_list
    global found_num
    for url in path_list:
        with open(url,'r',encoding='UTF-8') as f:
            file=url.replace("脑梗死病历原始数据 3352份脱敏txt","对话流")
            reader = csv.reader(f)
            sentence=[]
            for i in reader:
                sentence.append(i[0])
            # print(sentence)
            count = 0
            # not_found_num = 0
            # EHR = []
            kind=["主诉","现病史","既往史","个人史","婚育史","家族史","体格检查","辅助检查","初步诊断","补充诊断"]
            print(url)
            for row in sentence:
                if kind[0] in row:
                    if kind[0] in ["体格检查","辅助检查"]:
                        row==sentence[count+1]
                        # print(row[0])
                    kind_question(kind[0],file,row)
                    kind.remove(kind[0])
                    # print(row)
                # print(count)
                count+=1



            #找到科室行
            # EHR = EHR.replace(" ","") #删除掉空格


if __name__ == '__main__':
    get_txt()
    read_txt()