import pandas as pd

def analyse_result(filtered):
    print(f"能够匹配到的密钥数量（含同一密钥不同类别,重复的密钥等）有{len(filtered)}")
    files_uniq = set()
    secret_uniq = set()
    for tmp in filtered:
        files_uniq.add(tmp['file'])
        secret_uniq.add(tmp['value'])
   
    print(f"能够匹配到的文件数量有{len(set(files_uniq))}")
    print(f"能够匹配到非重复密钥有{len(set(secret_uniq))}")
    
    #创建 单因素19类的DataFrame
    print(f"单因素900+类的DataFrame")
    data = filtered
    df = pd.DataFrame(data)
    # 统计每种secret_type的出现次数
    if type in df:
        secret_type_counts = df['series'].value_counts()
    # 打印或查看结果
        print(secret_type_counts)

