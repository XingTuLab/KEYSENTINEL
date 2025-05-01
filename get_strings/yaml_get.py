import yaml


from get_strings.json_get import *
def extract_yaml(yaml_file_path):
    # 读取YAML文件
    #yaml_file_path = './test/test_inbox_reply_message.yaml'
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    
    # 将YAML数据转换为JSON
    json_data = json.loads(json.dumps(yaml_data, indent=2, default=str))  # 使用default=str将字节转换为字符串
 
    all_values_ = extract_leaf_values(json_data)
    result=set([tmp for tmp in all_values_ ])
    result_end=exract_strlist_position(result,yaml_file_path)
    return result_end

if __name__ == '__main__':
    yaml_file_path = "./tests/cassettes/test_subscription_page_invalid.yaml"

    yaml_strings=extract_yaml(yaml_file_path)

    print(yaml_strings)
    print(len(yaml_strings))