import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from base_func.base_func import read_dict_bin

def check_multi_reason(hit_dict):
    series_have = {}
    current_path = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.abspath(os.path.join(current_path, '../data/regex/regex_multiple_rulename.bin'))
    regex_multiple_rulename=read_dict_bin(target_path)
    for tmp in hit_dict:
        if tmp['series'] in regex_multiple_rulename:    # 只判断多因素
    
            if tmp['series'] not in series_have:
                series_have[tmp['series']] = {tmp["rule_name"]}  # 将字符串转换为集合
            else:
                series_have[tmp['series']].add(tmp["rule_name"])  # 将字符串作为一个元素添加到集合中
    check_false=set()
    
    for series in series_have:
        if series_have[series]==regex_multiple_rulename[series]:       #说明类别集齐满了
            check_false.add(series)  
    end_result=[]
    suffixes=["URL", "ID",  "User",  "Domain"] 
    for tmp in hit_dict:
        if tmp['series'] not in regex_multiple_rulename:
            end_result.append(tmp)
        else:
            if any(char.isupper() for char in tmp['rule_name']):    #在tf的正则里面判断
                if tmp['series'] in check_false and (not any(tmp['rule_name'].endswith(suffix) for suffix in suffixes)):
                    end_result.append(tmp)
            else:
                end_result.append(tmp)
                
    return end_result
        
            
    
    