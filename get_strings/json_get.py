import json
import re
from filter.filter_substr import combine_substr
def extract_leaf_values(obj):
    leaf_values = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            sub_leaf_values = extract_leaf_values(value)
            leaf_values.extend(sub_leaf_values)
    elif isinstance(obj, list):
        for item in obj:
            sub_leaf_values = extract_leaf_values(item)
            leaf_values.extend(sub_leaf_values)
    elif isinstance(obj, str):
        if not obj.isdigit() :
            if len(obj)>3:
                try:
                    # 尝试解析字符串为字典
                    value_dict = json.loads(obj)
                    if isinstance(value_dict, dict):
                        # 如果解析成功且是字典类型，则继续提取字典中的值
                        sub_leaf_values = extract_leaf_values(value_dict)
                        leaf_values.extend(sub_leaf_values)
                    else:
                        # 如果解析成功但不是字典类型，将整个字符串作为值添加到列表中
                        leaf_values.append(obj)
                except json.JSONDecodeError:
                    # 如果解析失败，将整个字符串作为值添加到列表中
                    leaf_values.append(obj)
        else:
            if len(obj)>4:
                # 如果是其他类型，直接添加到列表中
                leaf_values.append(obj)
    else:
        if len(str(obj))>4:
            # 如果是其他类型，直接添加到列表中
            leaf_values.append(obj)

    return leaf_values

def exract_str_position(file_path,target_str):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 定义正则表达式
    target_str = str(target_str)
    pattern =  re.escape(target_str)
    rule = re.compile(pattern)
    match_list = []

   
    for match in rule.finditer(content):
        start, end = match.start(), match.end()

        # 获取匹配项所在行的行号
        line_start = content.count('\n', 0, start) + 1
        line_end = content.count('\n', 0, end) + 1

        value= match.group(0)
        dict={
            'value': value,
            "line_start": line_start,
            "line_end": line_end,
            "index_start": start,
            "index_end": end
        }
        match_list.append(dict)
    return match_list

def exract_strlist_position(strings_language,file_path):

    str_dict=[]
    for tmp in strings_language:
        str_dict.extend(exract_str_position(file_path,tmp))
    return str_dict
def extract_json(p):
    
    # 从JSON文件中读取数据
    with open(p, 'r') as file:
        json_data = json.load(file)
    all_values_ = extract_leaf_values(json_data)
    all_values_=[tmp for tmp in all_values_ if isinstance(tmp, str)]
    result = set([tmp for tmp in all_values_ if len(tmp) > 10])   #5的话数据量有点大，10的话可以减少一些，反正是辅助过滤
    result_end=exract_strlist_position(result,p)
    result_combined,duplicate_,belong_sub=combine_substr(result_end)    #修复的bug，其实还有潜在的hug
    return result_combined
if __name__ == '__main__':
    p="./region-usage-json/NC.json"
    result=extract_json(p)
    for tmp in result:
        if "Gunakan" in tmp['value']:
            print(tmp)