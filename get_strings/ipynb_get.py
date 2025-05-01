
from get_strings.json_get import *


def extract_ipynb(ipynb_file_path):
    
    with open(ipynb_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    all_values_ = extract_leaf_values(json_data)
    result=set([tmp for tmp in all_values_ ])
    result_end=exract_strlist_position(result,ipynb_file_path)
    return result_end
if __name__ == '__main__':
    # 用法示例
    ipynb_file_path = "./top5k_hit/target5/zylo117-Yet-Another-EfficientDet-Pytorch-15403b5/tutorial/train_shape.ipynb"

    result=extract_ipynb(ipynb_file_path)
    print(result)

