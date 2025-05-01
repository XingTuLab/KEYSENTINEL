import os
import subprocess
import json
#解析的列是不对的，我用的是——col_end=col_start+length。但是私钥是跨行的，并且每个列解析还有细微的偏差
def extract_go(go_code_path):
    # 定义可执行文件路径和要解析的Go代码文件路径
    current_path = os.path.dirname(os.path.abspath(__file__))
    executable_path = os.path.abspath(os.path.join(current_path, 'go/extract_strings'))  # 修改为你的可执行文件路径

    # 构造命令行参数列表
    command = [executable_path, go_code_path]

    try:
        # 运行可执行文件并捕获输出
        result = subprocess.check_output(command, universal_newlines=True)
        result = json.loads(result)
        # 打印输出结果
        #print(result)
    except subprocess.CalledProcessError as e:
        print(f"运行可执行文件时发生错误: {e}")
    return result
if __name__ == '__main__':
    f="/data/zhoujiawei/test/secrets-leakage-detector/top5k_hit/target1/concourse-concourse-3793327/fly/integration/suite_test.go"
    result=extract_go(f)
    print(result)