import csv
import os

path_list = []
ks_list = []
found_num = 0
def get_txt(file_pathname=r'./脑梗死病历原始数据 3352份脱敏txt'):
    a = 0
    global path_list
    for filename in os.listdir(file_pathname):
        path = os.path.join(r'./脑梗死病历原始数据 3352份脱敏txt',filename)
        path_list.append(path)

def read_txt():
    global path_list
    global ks_list
    global found_num
    for url in path_list:
        with open(url,'r',encoding='UTF-8') as f:
            reader = csv.reader(f)
            count = 0
            not_found_num = 0
            EHR = []
            for row in reader:
                if count == 3:
                    break
                else:
                    EHR = row[0]
                count += 1
            EHR = EHR.replace(" ","") #删除掉空格
            EHR_list = EHR.split(":")
            try:
                EHR_list.remove('科室')
            except ValueError as e:
                not_found_num += 1
            else:
                for item in EHR_list:
                    try:
                        if '科' in item:
                            pos = item.find('科')
                            ks = item[0:pos+1]
                            found_num += 1
                            if not ks in ks_list:
                                ks_list.append(ks)
                    except ValueError as e:
                        print(e)
                        not_found_num += 1
    print(ks_list,not_found_num)
    print(found_num)

if __name__ == '__main__':
    get_txt()
    read_txt()