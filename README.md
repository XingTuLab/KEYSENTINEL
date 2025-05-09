# KEYSENTINEL

> A general-purpose secret detection tool that leverages semantic analysis, prefix matching, and machine learning to improve accuracy and significantly reduce false positives.

---

[中文版](./README.zh-CN.md)

## 📄 Paper

- 📄 Conference Paper: [Hey, Your Secrets Leaked! Detecting and Characterizing Secret Leakage in the Wild](https://www.computer.org/csdl/proceedings-article/sp/2025/223600a412/26hiTHRCdyg)  
  _Presented at 2025 IEEE Symposium on Security and Privacy (S&P)_

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/XingTuLab/KEYSENTINEL.git
cd KEYSENTINEL
```

### 2. Environment requirements

- Python 3.8
- Node.js v16.17.1

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Command-line usage

```
python main_arg.py --help
```

Example output:

```
Arguments:

--path               Root path of the source code to be scanned  
--mode               Scan mode: scan / entropy  
--entropy_path       Path used in entropy-based mode  
--regex              Custom regex for matching secrets  
--save_name          Filename to save detection results  
--size_limit         File size limit in bytes  
--core_num           Number of CPU cores to use  
--timeout_seconds    Max timeout for scanning a single file (in seconds)
```

## 🔧 Example

```
python main_arg.py --path ./your_source_code --save_name test_name
```

## 📦 Dataset Access

To obtain the dataset used in the paper, please send an email request that includes:

- To: zhoujiawei01@qianxin.com
- CC: your advisor and yinglingyun@qianxin.com
- In the email body, please include:
  - The **purpose and intended use** of the dataset
  - A statement that you **will sign an agreement not to use the dataset for any malicious or illegal purposes**
  - A confirmation that any publication based on the dataset will cite our paper

## 📚 Citation

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
