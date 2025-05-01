from get_strings.json_get import *
import pandas as pd

def extract_csv(csv_file_path):
    
    df = pd.read_csv(csv_file_path)
    # 将DataFrame转换为字典
    json_data = df.to_dict(orient='records')
    all_values_ = extract_leaf_values(json_data)
    result=set([tmp for tmp in all_values_ ])
    result_end=exract_strlist_position(result,csv_file_path)
    return result_end
if __name__ == '__main__':
    # 从CSV文件加载数据到DataFrame
    csv_file_path = './misc/transformers.csv'

    result=extract_csv(csv_file_path)
    # 现在，json_data变量包含了转换后的JSON数据
    print(result)
