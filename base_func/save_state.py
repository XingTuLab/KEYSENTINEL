import os
import pickle
import json
import shutil


#这个对于非镜像而言
# def make_result():
#     # 判断当前目录是否有 stats 文件夹，没有则创建
#     if not os.path.exists('./states'):
#         os.makedirs('./states')
#     folder_prefix = "result_"
#     folder_count = 1
#
#     # 检测结果文件夹的根目录，在当前目录下的 state 文件夹中
#     root_folder_path = os.path.join(os.getcwd(), "states")
#
#     while True:
#         folder_name = folder_prefix + str(folder_count)
#         folder_path = os.path.join(root_folder_path, folder_name)
#
#         if not os.path.exists(folder_path):
#             os.mkdir(folder_path)
#             print(f"新建文件夹 {folder_path}")
#             break
#         folder_count += 1
#     return folder_path
def cleanup_result(temp_dir):
    # 删除目标文件夹中的所有文件和子文件夹，但保留目标文件夹本身
    if os.path.exists(temp_dir):
        # 遍历目标文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(temp_dir, topdown=False):
            # 删除文件
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    pass
                except Exception as e:
                    pass

            # 删除子文件夹
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)
                    pass
                except Exception as e:
                    pass
    else:
        pass

def make_result():
    # 判断当前目录是否有 stats 文件夹，没有则创建
    if not os.path.exists('./states'):
        os.makedirs('./states')
    folder_prefix = "result_"
    folder_count = 1

    # 检测结果文件夹的根目录，在当前目录下的 state 文件夹中
    root_folder_path = os.path.join(os.getcwd(), "states")

    while True:
        folder_name = folder_prefix + str(folder_count)
        folder_path = os.path.join(root_folder_path, folder_name)

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            print(f"新建文件夹 {folder_path}")
            break
        folder_count += 1
    return folder_path

def write_json(p,value):
    with open(p, 'w') as file_a:
        json.dump(value, file_a, indent=4)
#保存变量stats_dict to bin文件
def save_dict2bin(stats_dict,name,save_root):
    folder_path=save_root  #建立新的文件夹便于每次自动区分
    file_path = os.path.join(folder_path, f"{name}.bin")
    with open(file_path, 'wb') as f:
        pickle.dump(stats_dict, f)

def read_dict_bin(path):
    # 从二进制文件中加载hit_dict
    with open(path, 'rb') as f:
        return pickle.load(f)

def save_temp_trufflehog(hit_dict, name, save_root):
    folder_path = save_root  # 建立新的文件夹便于每次自动区分
    # 定义一个字典来保存数据
    file_path = os.path.join(folder_path, f"{name}.json")
    # 将整个数据字典保存为JSON文件
    with open(file_path, "w") as fp:
        for item in hit_dict:
            json_str = json.dumps(item)
            fp.write(json_str + '\n')
    print(f"结果保存在{file_path}里")
#读取tmp
def load_temp_trufflehog(file_path):
    hit_dict = []  # 创建一个空列表来保存读取的数据
    with open(file_path, "r") as fp:
        for line in fp:
            # 逐行读取JSON数据并解析
            item = json.loads(line.strip())
            hit_dict.append(item)
    return hit_dict


#保存单个GitHub项目结果的json文件
def save_hit_dict_trufflehog(hit_dict, name, save_root):
    
    folder_path = save_root  # 建立新的文件夹便于每次自动区分
    # 定义一个字典来保存数据

    file_path_single = os.path.join(folder_path, f"{name}_single.json")
    # 将整个数据字典保存为JSON文件
    write_json(file_path_single,hit_dict)
    print(f"结果保存在{file_path_single}里")





