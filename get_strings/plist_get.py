from get_strings.json_get import *
import plistlib
import json
def extract_plist(plist_file_path):
    
    with open(plist_file_path, 'rb') as plist_file:
        plist_data = plistlib.load(plist_file)
    
    # 将数据转换为JSON格式
    json_data = json.loads(json.dumps(plist_data, indent=2))
    all_values_ = extract_leaf_values(json_data)

    result=set([tmp for tmp in all_values_ ])
    result_end=exract_strlist_position(result,plist_file_path)
    return result_end
if __name__ == '__main__':
    # 从plist文件加载数据
    plist_file_path = './top5k_hit/target7/alibaba-flutter-go-a41b212/ios/Runner/GoogleService-Info.plist'
    result=extract_plist(plist_file_path)
    # 打印JSON数据或按需使用
    print(result)
