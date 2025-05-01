from difflib import SequenceMatcher
import os
import sys
from jellyfish import jaro_winkler_similarity
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from base_func.base_func import *


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
def compare_secret_similarstr(group1, group2):
  
    #判断交集是否是子串————————————————————反正都是直接用index来比较
    start1, end1 = group1["index_start"], group1["index_end"]  
    start2, end2 = group2["index_start"], group2["index_end"]
    if group1['value']==group2['value'] and start1==start2 :
        if group2['series']=='generic':
            return 2
        else:
            return 1   
    # 判断是否有交集，如果相似，如果1号是通用返回1。否则返回2（两者是不同的密钥）
    elif start1 <= end2 and start2 <= end1:
        if(compare_secret(group1['value'],group2['value'])):
            if (group1['series']=='generic'):
                return 1
            else:
                return 2
       
def combine_group_similarstr(data_group):
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
            if (compare_secret_similarstr(group1,group2))==1:
                
                duplicate_.add(i)
                if j not in belong_sub:
                    belong_sub[j]=[i]
                else:
                    belong_sub[j].append(i)
            elif (compare_secret_similarstr(group1,group2))==2:
                duplicate_.add(j)
                if i not in belong_sub:
                    belong_sub[i]=[j]
                else:
                    belong_sub[i].append(j)
                
    for i in range(len(data_group) ):
        if i not in duplicate_:
            result.append(data_group[i])
    return result,duplicate_,belong_sub
def combine_similarstr(hit_dict):
    # 使用字典来根据文件分类数据  
    file_data_dict = {}  
    for item in hit_dict:  
        file_path = item["file"]  
        if file_path not in file_data_dict:  
            file_data_dict[file_path] = []  
        file_data_dict[file_path].append(item)  
    hit_dict_nosimiarstr=[]
    for file_path, data_items in file_data_dict.items():  

        result,duplicate_,belong_sub=combine_group_similarstr(data_items)
        hit_dict_nosimiarstr.extend(result)
    return hit_dict_nosimiarstr


if __name__ == '__main__':

    result=combine_similarstr(www)