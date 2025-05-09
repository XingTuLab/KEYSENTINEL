# KEYSENTINEL

> 一款通用的密钥检测工具，结合语义分析、前缀匹配和机器学习技术，有效提升检测准确率，显著降低误报。

---

## 📄 相关资料

- 📄 会议论文：[Hey, Your Secrets Leaked! Detecting and Characterizing Secret Leakage in the Wild](https://www.computer.org/csdl/proceedings-article/sp/2025/223600a412/26hiTHRCdyg)  
  _发表于 2025 IEEE Symposium on Security and Privacy (S&P)_

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/XingTuLab/KEYSENTINEL.git
cd KEYSENTINEL
```

### 2. 环境要求

- Python 3.8
- Node.js v16.17.1

### 3. 安装依赖

```
pip install -r requirements.txt
```

### 4. 查看参数说明

```
python main_arg.py --help
```

示例输出：

```
参数说明：

--path               被检测项目的根目录  
--mode               扫描模式：scan / entropy  
--entropy_path       启发式熵检测路径  
--regex              自定义正则表达式  
--save_name          保存结果的文件名  
--size_limit         单个文件最大扫描限制（单位：字节）  
--core_num           使用的CPU核心数  
--timeout_seconds    每个文件的最大扫描时长（秒）
```

------

## 🔧 使用示例

```
python main_arg.py --path ./your_source_code --save_name result.json
```

------

## 📦 数据集申请

如需获取论文中使用的数据集，请通过邮件联系作者，邮件要求如下：

- 收件人：zhoujiawei01@qianxin.com
- 抄送你的导师及 yinglingyun@qianxin.com
- 邮件正文需说明：
  - 数据集申请的**目的与用途**
  - **需签署一份不用于非法用途或破坏性行为的协议**
  - 明确表示使用数据集所产出的成果需引用我们的论文

------

## 📚 引用格式

```
@INPROCEEDINGS {,
author = { Zhou, Jiawei and Zhang, Zidong and Ying, Lingyun and Chai, Huajun and Cao, Jiuxin and Duan, Haixin },
booktitle = { 2025 IEEE Symposium on Security and Privacy (SP) },
title = {{ Hey, Your Secrets Leaked! Detecting and Characterizing Secret Leakage in the Wild }},
year = {2025},
volume = {},
ISSN = {2375-1207},
pages = {412-430},
abstract = { Secrets, whether structured like API keys or unstructured like passwords, are essential for securing applications and services. However, the growing use of open-source projects and rapid development cycles has amplified the risk of secret leakage. Current detection tools suffer from high false positive rates and low recall due to simplistic methods like regular expressions and entropy checks, often missing unstructured secrets or mislabeling non-sensitive data. In this paper, we introduce KEYSENTINEL, an advanced automated secret detection tool that addresses these limitations through machine learning, semantic analysis, and prefix matching. To evaluate KEYSENTINEL, we created the first cross-platform benchmark with 11,826 labeled secrets in 1,806,530 files across GitHub, PyPI, and WeChat. We compare KEYSENTINEL with six currently available tools. The results show KEYSENTINEL achieves state-of-the-art performance, with precision (91.18%), recall (81.71%), and an F1 score (0.86), surpassing industry-standard tools and significantly reducing false positives. It also outperforms large language models like GPT-4 and o1 in accuracy and cost-effectiveness. Besides, we conduct a large-scale measurement study, analyzing 80,330,098 files from GitHub, PyPI, and WeChat. We found that up to 30% of projects are at risk of secret leaks. Furthermore, we also scan the codebase of an IT company to assess real-world secret leakage risks. Our findings underscore the pervasive nature of secret leaks and highlight the urgent need for enhanced secret management practices across platforms. },
keywords = {secret detection;software supply chain security;security and privacy metrics},
doi = {10.1109/SP61157.2025.00122},
url = {https://doi.ieeecomputersociety.org/10.1109/SP61157.2025.00122},
publisher = {IEEE Computer Society},
address = {Los Alamitos, CA, USA},
month =May}
```
