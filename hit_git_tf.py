"""
It is necessary to traverse each file, all files need to be scanned and each file needs to be scanned by all regular expressions,
and if a file is scanned from the beginning to the end, if there are multiple matches, they must be matched.
(Multiple keys may appear in a file)

"""
import multiprocessing

from multiprocessing import Pool, Manager
import re
import time

# import chardet

from base_func.base_func import *
# import pandas as pd
from filter.filter_multireason import check_multi_reason
from filter.key_value_Filter import key_value_filter_single
# from filter.filter_pattern_word import filter_pattern_word_single

from urllib.parse import urlparse     #urlparse
from filter.filter_substr import combine_substr
from get_strings.filter_strings import filter_strings
from base_func.logger import setup_logger
from base_func.save_state import *
import signal
import platform
from tqdm import tqdm

# Define timeout processing function # 30s for each file
def handler(signum, frame):
    raise TimeoutError("File processing exceeded time limit")

# Check if SIGALRM is available (not on Windows)
HAS_SIGALRM = hasattr(signal, 'SIGALRM')



def get_sub(a,b):
    # Find the starting position of b in a
    start_index = a.find(b)  

    if start_index != -1:  

        return a[:start_index]  
    else:  

        return a


def scan_project_tf(rules_single,file_list,log_path):
    logger_instance = setup_logger(log_path)
    single_dict=[]

    for file_path in tqdm(file_list):

        file_value_set=set()
        hit_num=0
        hit_dict=[]
        try:
            with open(file_path, 'r',encoding='utf-8') as f:
                content = f.read()
                #content.encode().decode('unicode_escape')

            for rule_info in rules_single:
                rule_name=rule_info['rule_name']
                rule_pattern =rule_info['regex']
                try:
                    rule = re.compile(rule_pattern)
                except:
                    continue
                if len(hit_dict)>100000:
                    break
                for match in rule.finditer(content):
                    start, end = match.start(), match.end()


                    line_start = content.count('\n', 0, start) + 1
                    line_end = content.count('\n', 0, end) + 1
                    col_start = start - content.rfind('\n', 0, start)
                    col_end = end - content.rfind('\n', 0, end)
                    # print(f"Found '{rule_name}' at position {line_start}-{line_end}: {match.group(0)}")
                    # Print previous five lines and following five lines

                    value=match.group(1) if rule.groups==1 else match.group(0)
                    if rule_info['series']=='private':
                        if len(value)<100:
                            continue

                    #对于有熵的机械密钥
                    if 'entropy'in rule_info:
                        if entropy(value)<rule_info['entropy']:
                            continue

                    """if file_path+value in file_value_set:
                        continue
                    else:
                        file_value_set.add(file_path+value)"""

                    hit_dict.append({
                    "file": file_path,
                    'value': value,
                    'match':match.group(),
                    "rule_name": rule_name,
                    "is_mechanical": rule_info["is_mechanical"],
                    "series":rule_info["series"]   ,
                    "filter_count":[],
                    "word_weight":0,
                    "line_start": line_start,
                    "line_end": line_end,
                    "col_start":col_start,
                    "col_end":col_end,
                    "index_start": start,
                    "index_end": end,
                    "regex":rule_pattern
                    })
                    hit_num+=1

        except Exception as e:
            # print(f"{file_path} Unable to read")
            pass

        hit_dict_check_multi=check_multi_reason(hit_dict)
        hit_dict_single,duplicate_,belong_sub=combine_substr(hit_dict_check_multi)
        hit_dict_single=filter_strings(file_path,hit_dict_single)

        result_hit_dict=[]
        for tmp in  hit_dict_single:
            if tmp['series']!="certification":
                result_hit_dict.append(tmp)


        info={"scaned_file_path":file_path,"hit":len(hit_dict)}
        info=str(info)
        logger_instance.info(info)

        single_dict.extend(result_hit_dict)
    return single_dict

def scan_filelist_tf(rules_single,file_list,single_dict,duplicate_dict,shared_variable,log_path,timeout_seconds):



    timeout_seconds = 300

    logger_instance = setup_logger(log_path)
    for file_path in tqdm(file_list):

        file_value_set = set()
        hit_num = 0
        hit_dict = []
        shared_variable.value += 1
        if (shared_variable.value % 3000) == 0:
            print("Inside the function:", shared_variable.value)
        try:

            if HAS_SIGALRM:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(timeout_seconds)
            # print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh",file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # content.encode().decode('unicode_escape')
            # ————————————单因素————————————
            for rule_info in rules_single:
                rule_name = rule_info['rule_name']
                rule_pattern = rule_info['regex']
                try:
                    rule = re.compile(rule_pattern)
                except:
                    continue

                for match in rule.finditer(content):

                    start, end = match.span(1) if rule.groups == 1 else match.span(0)
                    if rule_info["series"] == 'jdbc' or rule_info['series'] == 'private' or rule_info[
                        'series'] == 'uri' or rule_info['series'] == 'jwt':
                        start, end = match.start(), match.end()

                    line_start = content.count('\n', 0, start) + 1
                    line_end = content.count('\n', 0, end) + 1
                    col_start = start - content.rfind('\n', 0, start)
                    col_end = end - content.rfind('\n', 0, end)


                    if rule_info['series'] != "uri":
                        value = match.group(1) if rule.groups == 1 else match.group(0)


                    else:
                        # Parsing URLs
                        parsed_url = urlparse(match.group(0))
                        # Get username and password
                        user_info = parsed_url.username, parsed_url.password

                        value = user_info[1]
                        if value == None:  # The detected URL has no secret———https://localhost:3000/jqueryui@1.2.3
                            continue


                    prefix = ""
                    if rule_info['series'] == 'generic':
                        prefix = match.group(1)
                        value = match.group(2)
                        if len(value) == 42 and value.startswith("0x"):  # Special case representing address
                            continue
                        key_value = get_sub(match.group(), value)
                        key_value = re.sub(r'[^a-zA-Z]*$', '', key_value)
                        start = start + len(key_value)

                    if rule_info['series'] == 'private':
                        if len(value) < 128:
                            continue


                        if len(value) < 256 and 'ECC' in match.group():
                            continue
                        if len(value) < 256 and 'RSA' in match.group():
                            continue
                    if value is None:
                        continue
                    if len(value) < 5:
                        continue
                    # 对于有熵的机械密钥
                    if 'entropy' in rule_info:
                        if entropy(value) < rule_info['entropy']:
                            continue
                    secret_hit = {
                        "file": file_path,
                        'value': value,
                        'match': match.group(),
                        'prefix': prefix,
                        "rule_name": rule_name,
                        "is_mechanical": rule_info["is_mechanical"],
                        "series": rule_info["series"],
                        "filter_count": [],
                        "word_weight": 0,
                        "line_start": line_start,
                        "line_end": line_end,
                        "col_start": col_start,
                        "col_end": col_end,
                        "index_start": start,
                        "index_end": end,
                        "regex": rule_pattern,
                        "need_keyvalue": rule_info['need_keyvalue']
                    }
                    # Prefix filter___________________________
                    if not key_value_filter_single(secret_hit):
                        continue

                    hit_dict.append(secret_hit)
                    hit_num += 1

            hit_dict_check_multi = check_multi_reason(hit_dict)
            hit_dict_single, duplicate_, belong_sub = combine_substr(hit_dict_check_multi)
            hit_dict_single = filter_strings(file_path, hit_dict_single)  #string-assisted filter


            result_hit_dict = []
            for tmp in hit_dict_single:
                if tmp['series'] != "certification":
                    result_hit_dict.append(tmp)


            info = {"scaned_file_path": file_path, "hit": len(hit_dict)}
            info = str(info)
            logger_instance.info(info)

            single_dict.extend(result_hit_dict)

        except TimeoutError:
            print(f"Timeout occurred for file: {file_path}")
            logger_instance.info(f"Timeout occurred for file: {file_path}")
        except Exception as e:
            info = {"error": e, "scaned_file_path": file_path}
            print(info)
            logger_instance.info(str(info))
        finally:
            # 重置定时器
            if HAS_SIGALRM:
                signal.alarm(0)
    return single_dict


if __name__ == '__main__':

    time1 = time.time()

    # rules_single = read_dict_bin("./data/regex/regex_machine_human_v2.bin")
    rules_single = read_json(
        "./data/regex/regex_machine_human_v2.json")
    print(len(rules_single))

    manager = Manager()
    shared_variable = manager.Value('i', 0)
    # file_list = read_json("./testfiles.json")
    file_list = ["./target6/sahat-satellizer-ae28633/test/shared.spec.ts"]
    save_root = './tmp'
    log_path = './tmp/log.json'
    hit_dict=scan_filelist_tf(rules_single,file_list, [],[],shared_variable,log_path,300)

    print("test time", time.time() - time1)
    print(f"length:{len(hit_dict)}")
    save_dict2bin(hit_dict, "hit_dict", save_root)
    write_json('./tmp/hit_dict.json', hit_dict)
    # save_hit_dict_trufflehog(hit_dict,name='test_multipro',save_root=save_root)

