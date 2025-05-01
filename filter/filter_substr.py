from difflib import SequenceMatcher
import sys
sys.path.append('../') # 将上一级目录添加到系统路径中
from jellyfish import jaro_winkler_similarity
# import pandas as pd
# from base_func.base_func import *
from tqdm import tqdm

# 移除非字母数字字符并转换为单行字符串
def preprocess_secret(secret):
    secret = ''.join(e for e in secret if e.isalnum() or e.isspace())
    secret = secret.replace(' ', '')  # 移除空格
    return secret
# 计算秘密的相似性得分
def calculate_sequence_similarity(secret1, secret2):
    secret1 = preprocess_secret(secret1)
    secret2 = preprocess_secret(secret2)
    matcher = SequenceMatcher(None, secret1, secret2)
    similarity = matcher.ratio()
    return similarity
def compare_secret(str1, str2):
    """if min(len(str1),len(str2))/max(len(str1),len(str2))>0.5: #子串是原长一半以上
        if str1 in str2 or str2 in str1:
            return True"""
    if jaro_winkler_similarity(str1, str2) >= 0.7 :
        return True
    if calculate_sequence_similarity(str1, str2) >= 0.6:  #第二个耗时长
        return True

    return False
def compare_secret_substr(group1, group2):
  
    #判断交集是否是子串————————————————————反正都是直接用index来比较
    start1, end1 = group1["index_start"], group1["index_end"]  
    start2, end2 = group2["index_start"], group2["index_end"]
    if group1['value']==group2['value'] :   #相等的情况先不处理
        return 
    # 判断是否是子集
    elif (start1 >= start2 and end1 <= end2):    #group1范围小
        return 1
    elif (start2 >= start1 and end2 <= end1):    #group2范围小
        return 2
    """相似也先不处理
    # 判断是否有交集，同类有的话，如果相似，随便去一个。否则不反回（两者是不同的密钥）
    elif start1 <= end2 and start2 <= end1:
        if (group1['series']==group2['series']):
            if(compare_secret(group1['value'],group2['value'])):
                return 2"""
       
def combine_substr(data_group):
    duplicate_=set() #记录重复的坐标
    belong_sub={}
    result=[]
    if len(data_group)<2:
        return data_group,duplicate_,belong_sub
    if len(data_group) > 100:
        iterator = tqdm(range(len(data_group) - 1))
    else:
        iterator = range(len(data_group) - 1)
    for i in iterator:  #遍历每个组
        group1=data_group[i]
        for j in range(i+1,len(data_group) ): 
            if j in duplicate_ and i in duplicate_:
                continue
            group2=data_group[j]
            if len(group1)>10000:
                duplicate_.add(i)
            if (compare_secret_substr(group1,group2))==1:
                
                duplicate_.add(i)
                if j not in belong_sub:
                    belong_sub[j]=[i]
                else:
                    belong_sub[j].append(i)
            elif (compare_secret_substr(group1,group2))==2:
                duplicate_.add(j)
                if i not in belong_sub:
                    belong_sub[i]=[j]
                else:
                    belong_sub[i].append(j)
                
    for i in range(len(data_group) ):
        if i not in duplicate_:
            result.append(data_group[i])
    return result,duplicate_,belong_sub
def pre_process(hit_dict_position_value):
    file_line_dict={}
    for tmp in hit_dict_position_value:
        tmp_str=tmp['file']+str(tmp['line_start'])+str(tmp['line_end'])
        if tmp_str not in file_line_dict:
            file_line_dict[tmp_str]=[tmp]
        else:
            file_line_dict[tmp_str].append(tmp)
    line_value_group=[]
    line_value_only=[]
    for tmp in tqdm(file_line_dict):
        if len(file_line_dict[tmp])>1:
            line_value_group.append(file_line_dict[tmp])
        else:
            line_value_only.extend(file_line_dict[tmp])
            continue
    return line_value_group,line_value_only

if __name__ == '__main__':

    result,duplicate_,belong_sub=combine_group_my_tool(www)