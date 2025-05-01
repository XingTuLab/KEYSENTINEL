# 使用Python 3.8作为基础镜像
FROM python:3.8

# 安装Node.js和Go环境
# 这里假设你的工具需要Node.js和Go环境，你可以根据实际情况修改
# 请确保你的工具所需环境已经包含在这个镜像中
# 如果不是，请根据需要添加相应的安装命令
RUN apt-get update && apt-get install -y nodejs npm

# 设置工作目录
WORKDIR .

# 将当前目录下的所有文件复制到工作目录中
COPY . .

# 安装Python依赖
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 设置默认命令
CMD ["python", "main_arg.py"]
