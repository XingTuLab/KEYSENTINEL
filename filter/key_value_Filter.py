import sys
sys.path.append('../') # 将上一级目录添加到系统路径中
# import time
#
from base_func.base_func import *
# import multiprocessing
from multiprocessing import Pool, Manager
from tqdm import tqdm
import re
import wordninja

def count_matching_words(input_string, filter_key):
    count = 0
    input_string_lower = input_string.lower()  # 将输入字符串转换为小写形式

    for key in filter_key:
        if key.lower() in input_string_lower:  # 将关键词也转换为小写形式进行比较
            count += 1
    return count

def filter_prefix(key_list,left_splited_list,right_splited_list,confusion_list,list_left,list_right,prefix): #前缀拆词，前缀左拆、前缀右拆，混淆、左右白名单
    #————————key混淆————————
    key_list_lower=[tmp.lower() for tmp in key_list]
    confusion_list=[tmp.lower() for tmp in confusion_list]
    for tmp in confusion_list:
        if tmp in key_list_lower and prefix.lower() in tmp:      #后面的and是需要确认哪个prefix命中的这个只能用于混淆
            return True
    #————————key左边过滤————————
    list_left_lower=[tmp.lower() for tmp in list_left]
    left_splited_list_lower=[tmp.lower() for tmp in left_splited_list]
    for tmp in list_left_lower:
        if tmp in left_splited_list_lower :      #左边
            return True
    #————————key右边过滤————————
    list_right_lower=[tmp.lower() for tmp in list_right]
    right_splited_list_lower=[tmp.lower() for tmp in right_splited_list]
    for tmp in list_right_lower:
        if tmp in right_splited_list_lower :      #右边
            return True
    return False
def split_words(secret_match,word_list):
     
    tokens = re.split(r'[._-]', secret_match)
    tokens = [token.rstrip() for token in tokens if len(token)>=2]  # 删除空字符串
    # 进一步拆解
    new_tokens = []
    for token in tokens:
        if token not in word_list and len(token)>3:
            split_tokens = [split_token for split_token in  wordninja.split(token)if len(split_token)>=2]
            new_tokens.extend(split_tokens)
        else:
            new_tokens.append(token)
    return new_tokens
def split_string_by_word(s, word):
    if not word:  # Check if the word is empty
        return s, '', ''  # Return the input string and empty strings
    if word in s:
        parts = s.split(word)
        left_part = parts[0]
        right_part = word.join(parts[1:])
        return left_part, word, right_part
    else:
        return s, '', ''

def get_sub(a,b):
    # 查找b在a中的起始位置  
    start_index = a.find(b)  
    # 如果b是a的子串  
    if start_index != -1:  
        # 提取b之前的那部分字符串  
        return a[:start_index]  
    else:  
        # 如果b不是a的子串，可以设置一个默认值或抛出异常  
        return a

def key_value_filter_single(single_hit):
    current_path = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.abspath(os.path.join(current_path, '../data/fixed_top_english_words_mixed_500000.json'))
    word_list=read_json(target_path)
    end_filtered=[]
    whole_value_list=["templateid:","@tmp","@example",'example',"@test","@hostname",'test:test','example.com','@somewhere','_key','@url','hello:world@',"****@localhost","127.0.0.1:443@"]
    value_placeholder=["changeit","changeme","change","guest","printf","return","test","user",'pass',"password","username","secret",'test','bar','foobar','api_secret','TOKEN','pwd','password','apikey',"Parola","Parolan","Wachtwoord","Salasana","Pasahitza","boolean","Lozinka","before","blahblah"]
    value_machine=["ca-pub-"]  #机械密钥的
    test_path=["test","example",'demo']
    list_right=["Oid","author","hash",'Fingerprint','keyword','checksum','addr','type','id']
    target_path = os.path.abspath(os.path.join(current_path, '../data/sorted_end_right_list_fasle_more20.json'))
    sorted_end_right_list_fasle_more20=read_json(target_path)
    list_right.extend([key for key,value in sorted_end_right_list_fasle_more20.items()])
    list_left=['PublicKey','public',"fake",'input','put','enter',"invalid"]
    target_path = os.path.abspath(os.path.join(current_path, '../data/end_confuse_words.txt'))
    confusion_list=load_txt(target_path)
    whole_key_list=["formkey","?key"," h1","GPG key","SAPageKey","pubkey","key_hex","fake_",'Password_label','Password_action','Password_msg',"git-tree","_id"," id",'sha256','-sha','sha1',' h1','keyword','apiUsername','PublicKey','public','.js','.py','.yaml','_type','_addr','.txt'] #"?key",——先保留吧
    target_path = os.path.abspath(os.path.join(current_path, '../data/file_extension.txt'))
    file_extention=load_txt(target_path)
    
    tmp=single_hit
    flag=False
    #if tmp['series']=='generic'or  tmp['match']!=tmp['value']:       #只有当key有别的语义时
    if tmp['need_keyvalue']== True and tmp['match']!=tmp['value']:                                        #暂时只对通用密钥有效
        key_value=get_sub(tmp['match'],tmp['value'])
        key_value = re.sub(r'[^a-zA-Z]*$', '', key_value)   #去除非字母数字字符
        if any(key_value.endswith(ext) for ext in file_extention):
            print(f"filter:{tmp['match']}")
            return False
        pre_left, target, pre_right = split_string_by_word(key_value, tmp['prefix'])
        
        key_list=split_words(key_value,word_list)
        left_splited_list=split_words(pre_left,word_list)
        right_splited_list=split_words(pre_right,word_list)
        if  filter_prefix(key_list,left_splited_list,right_splited_list,confusion_list,list_left,list_right,tmp['prefix']) or count_matching_words(key_value,whole_key_list) or count_matching_words(tmp['value'],value_machine):
            print(f"filter:{tmp['match']}")
            return False
    elif  tmp['match']!=tmp['value']:            #除了generic的他们可能没有prefix，但是可能也有前缀
        if 'password' in tmp['rule_name'] or'Jdbc'in tmp['rule_name'] or 'Uri'in tmp['rule_name']or 'jwt'in tmp['rule_name']:  
            pass
        else:
            key_value=get_sub(tmp['match'],tmp['value'])
            key_value = re.sub(r'[^a-zA-Z]*$', '', key_value)  
            if any(key_value.endswith(ext) for ext in file_extention):
                print(f"filter:{tmp['match']}")
                return False
    if tmp['is_mechanical'] =='human': 
        if 'password' in tmp['rule_name'] or'Jdbc'in tmp['rule_name'] or 'Uri'in tmp['rule_name']:                #password
            count_match=count_matching_words(tmp['value'],value_placeholder)
            count_match+=count_matching_words(tmp['match'],whole_value_list)
            #count_match+=count_matching_words(tmp['file'],test_path)
            if count_match>=1:
                print(f"filter:{tmp['value']}")
                return False
            #这里我感觉只能算作是风险评级——————————————————————————————————————————
            split_value = re.split(r'\W+',tmp['value'])    #拆分单词，过滤常见密钥
            result_value = [s for s in split_value if len(s) >= 3]  
            if flag:
                return False   
            #这里我感觉只能算作是风险评级——————————————————————————————————————————
        else:                                 #其它链接数据库的密钥
            count_match=count_matching_words(tmp['value'],value_placeholder)
            count_match+=count_matching_words(tmp['match'],whole_value_list)
            #count_match+=count_matching_words(tmp['file'],test_path)
            if count_match>=2:
                print(f"filter:{tmp['value']}")
                return False
        
    return True


def multiprocess(batch,share_dict):
    for tmp in tqdm(batch):
        if key_value_filter_single(tmp):
            share_dict.append(tmp)

if __name__ == '__main__':
#     tmp= {'file': './data/top5k_hit/target2/1N3-Sn1per-72d7fda/bin/zap-scan.py',
#   'value': 'guest',
#   'match': "Password=guest'",
#   'prefix': 'Password',
#   'rule_name': 'generic-password',
#   'is_mechanical': 'human',
#   'series': 'generic',
#   'filter_count': [],
#   'word_weight': 0,
#   'line_start': 154,
#   'line_end': 154,
#   'col_start': 54,
#   'col_end': 69,
#   'index_start': 6823,
#   'index_end': 6830,
#   'regex': '(?i)(?:[0-9a-z]{0,20})(?:[\\-_ .]{0,1})(passwd|password|pwd)(?:[0-9a-z\\-_\\t .]{0,20})(?:[ |\\t|\\r|\\f|\\v|\']|[ |\\t|\\r|\\f|\\v|"]){0,3}(?:=|>|:{1,3}=|\\|\\|:|<=|=>|:|\\?=)(?:\'|\\"| |\\t|\\r|\\f|\\v|=|\\x60){0,5}([0-9a-z\\-_.=!@#$%^&*+~\\(\\{\\}\\)]{5,150})(?:[\'|\\"|\\n|\\r|\\s|\\x60|;]|$)'}
#     print(key_value_filter_single(tmp))
    manager = Manager()
    single_dict = manager.list()
    num_cores = 35
    hit_dict=read_json("./PyPI/all_pypi_res_infos.json")
    batch_size=len(hit_dict)//num_cores
    pool = Pool(processes=num_cores)
    for i in range(num_cores):
        start_idx = i * batch_size
        end_idx = (i + 1) * batch_size if i < num_cores - 1 else len(hit_dict)
        batch_files = hit_dict[start_idx:end_idx]
        pool.apply_async(multiprocess, (batch_files, single_dict))
    pool.close()
    pool.join()
    result_single_dict = list(single_dict)
    
    #print("test time",time.time()-time1)
    print(f"length:{len(hit_dict)}")
    
    save_root='./test'
    save_name="all_pypi_res_infos_KeyvalueFix_2"
    save_dict2bin(result_single_dict,save_name,save_root)  
    write_json(f'./test/{save_name}.json',result_single_dict)