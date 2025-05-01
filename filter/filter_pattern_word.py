"""
第三阶段：三个过滤器
    Entropy Filter
    Words Filter
    Pattern Filter
"""
"""
此文件设置为命令行运行，设置参数
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from base_func.base_func import read_json
import math
from base_func.save_state import *
from base_func.logger import setup_logger
from tqdm import tqdm
import wordninja
import re
# 计算单词字符串的熵
def entropy(string):

    prob_dict = {}
    for character in string:
        if character in prob_dict.keys():
            prob_dict[character] += 1
        else:
            prob_dict[character] = 1
    probs = [float(prob_dict[character]) / len(string) for character in prob_dict]
    return - sum([prob * math.log(prob, 2) for prob in probs])

def read_dict_bin(path):
    # 从二进制文件中加载hit_dict
    with open(path, 'rb') as f:
        return pickle.load(f)

def split_string_entropy(string, length=30):  #用于拆分长的字符串计算熵_对于machine的并且没有private
    if len(string) < length :
        if  entropy(string)< 2.4:
            return True
        else:
            return False 
    step=len(string)//length
    str_splited=[]
    for i in range(step):
        start_idx = i * length
        end_idx = (i + 1) * length if i < step - 1 else len(string)
        batch_str = string[start_idx:end_idx]
        str_splited.append(batch_str)
    value_entropy=[ entropy(secret_substr)  for secret_substr in str_splited]
    if any(x < 3 for x in value_entropy):
        return True
    else:
        return False
def split_word(secret_match,words_list):
     
    tokens = re.split(r'[._\(\)\{\}\-\#\@\$\%\^\&\*]', secret_match)
    tokens = [token for token in tokens if len(token)>=1]  # 删除空字符串
    # 进一步拆解
    new_tokens = []
    for token in tokens:
        if token not in words_list and len(token)>3:
            split_tokens = [split_token for split_token in  wordninja.split(token)if len(split_token)>2]    #wordninja不适合长度短的单词
            new_tokens.extend(split_tokens)
        else:
            new_tokens.append(token)
    return new_tokens
def count_dictionary_words_long_value(secret, words_list,secret_fixed_prefixes):
    secret['word_weight']=0
    secret['filter_count']=[]
    have_meaning=False
    secret_match=secret['value']
    
    more5=0
    for key in words_list:
        if len(key)<4:
            continue
        if key in secret_fixed_prefixes.lower():  #正则表达式本身可能就会出现单词
            continue
        if key in secret_match:  # 将关键词也转换为小写形式进行比较
            count = secret_match.count(key) 
            for i in range(count):
                secret['filter_count'].append(key)
                secret['word_weight']+=len(key)
            if len(key)>=6:                   #直接由长度大于6的单词
                have_meaning= True
                return secret,have_meaning        
            if (secret['word_weight']/len(secret_match))>=0.25:  
                have_meaning= True
                return secret,have_meaning
    return secret,have_meaning
def count_dictionary_words(secret, words_list,secret_fixed_prefixes):
    secret['word_weight']=0
    secret['filter_count']=[]
    have_meaning=False
    secret_match=secret['value']
    words=split_word(secret_match,words_list)

    more4=0
    value_list=[]
    for word in words:
        # if len(word)>2 and len(word)<5:
        #     value_list.append(word)
        # else:
        value_list.append(word.lower())
    for key in words_list:
        if key in secret_fixed_prefixes.lower():  #正则表达式本身可能就会出现单词
            continue
        if key in value_list:  # 将关键词也转换为小写形式进行比较
            count = value_list.count(key) 
            for i in range(count):
                secret['filter_count'].append(key)
                secret['word_weight']+=len(key)
            if len(key)>4:
                more4+=1
            if  len(secret_match)<=30:
                if more4>0 :
                    have_meaning= True
                    return secret,have_meaning
            elif len(secret_match)>30 and len(secret_match)<=60:
                if more4>1 :
                    have_meaning= True
                    return secret,have_meaning          
        if (secret['word_weight']/len(secret_match))>0.35:  
            have_meaning= True
            return secret,have_meaning
    return secret,have_meaning
def filter_pattern_word_single(single_hit,words_list,patterns, rules_single,log_path):
    logger_instance = setup_logger(log_path)
    secret=single_hit
    if secret['is_mechanical']=="human":
        return secret
   
    if secret['series']!='private' and split_string_entropy(secret['value']):
        return False

    #print(secret)
    rule_name = secret['rule_name']
    secret_match = secret['value']
    secret['word_weight']=0
    secret['filter_count']=[]
    secret_fixed_prefixes=''
    for tmp in rules_single:
        if rule_name == tmp['rule_name'] :   #特殊处理general
            if rule_name !='generic-api-key':
                secret_fixed_prefixes=tmp["regex"]     #正则表达式本身可能就会出现单词

    # ——————————pattrn过滤—————————
    pattern_count=[]   #对每个类别的word_可以计数————>可以统计一下私钥之类的word情况,先弄2个的情况

    for pattern in patterns:            #这里就不需要过滤word了它是pattern
        if pattern.lower() in secret_fixed_prefixes.lower(): #排除前后缀
            continue
        if pattern in secret_match:  #pattern就不要lower了
            pattern_count.append(pattern)
        if(len(pattern_count)>0):
            secret['filter_count'].extend(pattern_count)
            return False
    #加特殊情况————    "api': 6.5.9_biqbaboplfbrettd7655fr4n2y\n"
    pattern_nums = r'^\d+\.\d+\.\d+'
    # 检查字符串是否匹配模式
    match = re.match(pattern_nums, secret['value'])
    if match:
        return False
    secret['filter_count'].extend(pattern_count)    
    # ——————————单词过滤——————————
    # 不能将匹配的单词打印出来if any(word.lower() in secret.lower() for word in words_list):   #不区分大小写
    """if len(secret['value'])>60:
        secret,have_meaning=count_dictionary_words_long_value(secret,words_list,secret_fixed_prefixes)
    else:  """    
    secret,have_meaning=count_dictionary_words(secret,words_list,secret_fixed_prefixes)
    if have_meaning:         #单词长度占比大于密钥的百分之三十了
        return False

    
    
    return secret

def filter_pattern_word(hit_dict,words_list,patterns,rules_single,log_path):
    filtered_meaning=[]
    for tmp in tqdm(hit_dict):
        if  filter_pattern_word_single(tmp,words_list,patterns,rules_single,log_path):
            filtered_meaning.append(tmp)
    return filtered_meaning
# def kk():
#     import os
#
#     current_path = os.path.dirname(os.path.abspath(__file__))
#     target_path = os.path.abspath(os.path.join(current_path, '../data/regex/regex_machine_human_v2.json'))
#     rules_single = read_json(target_path)
#     print(rules_single)


if __name__ == '__main__':
    log_path='./log'
    rules_single=read_json('./data/regex/regex_machine_human_v2.json')
    words_list=read_json('./data/fixed_top_english_words_mixed_100w.json')
    patterns = []
    with open('./data/patterns.txt', "r") as f:
        patterns = f.readlines()
    patterns = [pattern.strip() for pattern in patterns]
    # hit_dict=read_json("/PyPI/all_pypi_res_infos.json")
    # len(hit_dict)
    # eddd=filter_pattern_word(hit_dict,words_list,patterns,rules_single,log_path)
    # write_json('./filtered_meaning.json',eddd)
    # save_dict2bin(eddd,'filtered_meaning','./')
#     tmp={'file': 'b2dcfae90949f9c63e5ae08ff24f79ca10e57bb723863deb4427b374ef4132e4/tmp/cryptography_vectors/ciphers/AES/GCM/gcmEncryptExtIV128.rsp',
#   'value': 'cb8644ab828ba8dd1457782a35396a99',
#   'match': 'Key = cb8644ab828ba8dd1457782a35396a99\n',
#   'prefix': 'Key',
#   'rule_name': 'generic-api-key',
#   'is_mechanical': 'machine',
#   'series': 'generic',
#   'filter_count': [],
#   'word_weight': 0,
#   'line_start': 38744,
#   'line_end': 38745,
#   'col_start': 1,
#   'col_end': 1,
#   'index_start': 1234650,
#   'index_end': 1234686,
#   'regex': '(?i)(?:[0-9a-z]{0,20})(?:[\\-_ .]{0,1})(key|api|token|cred|secret|client|auth|access)(?:[0-9a-z\\-_\\t .]{0,20})(?:[\\s|\']|[\\s|"]){0,3}(?:=|>|:{1,3}=|\\|\\|:|<=|=>|:|\\?=)(?:\'|\\"|\\s|=|\\x60){0,5}([0-9a-z\\-_.=!@#$%^&*+~\\(\\{\\}\\)]{10,150})(?:[\'|\\"|\\n|\\r|\\s|\\x60|;]|$)',
#   'hash_256': 'b2dcfae90949f9c63e5ae08ff24f79ca10e57bb723863deb4427b374ef4132e4',
#   'version': '41.0.4',
#   'publish_time': '2023-09-19T16:32:29',
#   'distrubution': 'cryptography_vectors-41.0.4-py2.py3-none-any.whl',
#   'email': 'The Python Cryptographic Authority and individual contributors <cryptography-dev@python.org>',
#   'pypi_id': '6509ce32a86d981155392e30',
#   'package_name': 'cryptography-vectors',
#   'need_keyvalue': True}
#     a=filter_pattern_word_single(tmp,words_list,patterns,rules_single,log_path)
#     print(a)