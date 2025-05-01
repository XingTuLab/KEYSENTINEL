import subprocess
import json
def run_go():
    # 定义可执行文件路径和要解析的Go代码文件路径
    executable_path = './go/extract_strings'  # 修改为你的可执行文件路径
    go_code_path = './go/test.go'  # 修改为要解析的Go代码文件路径

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
