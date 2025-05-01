import re
from tqdm import tqdm
def exract_pattern(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # 定义正则表达式
    pattern = r"""(?<!\\)"(.*?)(?<!\\)"|(?<!\\)'(.*?)(?<!\\)'"""
    rule = re.compile(pattern)
    match_list = []

    for line_number, line in tqdm(enumerate(lines, start=1)):
        for match in rule.finditer(line):
            start, end = match.start(), match.end()

            value=match.group(1) if rule.groups==1 else match.group(0)
            dict={
                'value': value,
                "line_start": line_number,
                "line_end": line_number,
                "col_start":start,
                "col_end":end,
            }
            match_list.append(dict)
    return match_list
if __name__ == '__main__':
    file_path='./pypi_single.json'
    match_list=exract_pattern(file_path)
    print(match_list)