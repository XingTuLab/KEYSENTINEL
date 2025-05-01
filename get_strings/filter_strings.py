
import sys
sys.path.append('../') # 将上一级目录添加到系统路径中
from difflib import SequenceMatcher
from jellyfish import jaro_winkler_similarity


from get_strings.csv_get import extract_csv
from get_strings.general_get import exract_pattern
from get_strings.go_get import extract_go
from get_strings.ipynb_get import extract_ipynb
from get_strings.java_get import extract_java
from get_strings.json_get import extract_json
from get_strings.plist_get import extract_plist
from get_strings.py_get import extract_python
from get_strings.xml_get import extract_xml
from get_strings.yaml_get import extract_yaml
from get_strings.js_get import extract_js

from base_func.base_func import read_dict_bin,read_json
from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

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
#重写密钥比较，这里可以运行子串了，因为之前就过滤掉了，并且有些程序分析代码里面有些变量是json，特殊情况多
def compare_secret_substr(str1, str2):
    
    if jaro_winkler_similarity(str1, str2) >= 0.7 :
        return True
    if calculate_sequence_similarity(str1, str2) >= 0.6:  #第二个耗时长
        return True
    return False

def filter_strings(file_path,hit_dict):
    construt_flag=True    #看文件是否是已有严格结构的提取还是通用提取
    try:
        if file_path.endswith('.java'):
            strings = extract_java(file_path)
        elif file_path.endswith('.ipynb'):
            strings = extract_ipynb(file_path)
        elif file_path.endswith('.yaml'):
            strings = extract_yaml(file_path)
        elif file_path.endswith('.xml'):
            strings = extract_xml(file_path)
        elif file_path.endswith(('.js', '.jsx', '.ts')):
            strings = extract_js(file_path)  #js报错影响不到python那边获取
        elif file_path.endswith('.csv'):
            strings = extract_csv(file_path)
        elif file_path.endswith('.go'):
            strings = extract_go(file_path)
        elif file_path.endswith('.json'):
            strings = extract_json(file_path)
        elif file_path.endswith('.plist'):
            strings = extract_plist(file_path)
        elif file_path.endswith('.py'):
            strings = extract_python(file_path)
        else:
            construt_flag=False
            strings=exract_pattern(file_path)
        if strings is None:        #前面有些是调用了别人语言或程序，导致结果是None
            raise ValueError("strings cannot be None. This is a custom exception message.")
    except Exception as e:
        print(f"error:{e}")
        construt_flag=False
        strings=exract_pattern(file_path)
 
    strings_value=[]       #出现了解析出来没有value的情况
    for tmp in strings:
        if 'value' in tmp:
            strings_value.append(tmp)
    
    filter_hidt=[]
    if construt_flag:
        for tmp in hit_dict:
            
            if tmp['series']=='jdbc' or tmp['series'] == 'private' or tmp['series']=='uri' or tmp['series']=='jwt' or "url" in tmp['rule_name']:
                filter_hidt.append(tmp)
                continue

            same_local_have_str_andsubstr=False      #相同位置有字符串并且secret是子串
            for tmp1 in strings_value:
                if tmp['line_start']==tmp1['line_start'] :  #相同位置有字符串————可能结尾有匹配换行，但是首行肯定相同
                    if tmp['value']==tmp1['value']:   #看value 使用行的原因是发现很多列解析可能不对
                        filter_hidt.append(tmp)
                        same_local_have_str_andsubstr=True   #已经加入了
                        break
            if same_local_have_str_andsubstr:      
                continue
            else:
                for tmp1 in strings_value:            #因为可能前面又相同的value在最后面。
                    if tmp['line_start']==tmp1['line_start']:  #相同位置有字符串
                        if compare_secret_substr(tmp['value'],tmp1['value'])or (tmp['value'] in tmp1['value'] and is_valid_url(tmp1['value'])==False):      #不相等，但相似或子串
                            same_local_have_str_andsubstr=True
                            break
                if  same_local_have_str_andsubstr:
                    continue
                else:
                    filter_hidt.append(tmp)

    else:
        filter_hidt=hit_dict
    return filter_hidt
if __name__ == '__main__':
    file_path="/app/data/test/signalapp-Signal-Android-351e37b/apntool/apnlists/hangouts.xml"
    hit_dict=read_json('/app/tmp/hit_dict.json')
    filter_hidt=filter_strings(file_path,hit_dict)
    print(len(filter_hidt))


    
        

