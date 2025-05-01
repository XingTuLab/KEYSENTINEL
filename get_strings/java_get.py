import javalang
def extract_java(file_path):
    with open(file_path, 'r') as file:
        java_code = file.read()
    # 提取字符串和其位置
    # 使用javatop将Java代码转换为Python AST
    tree = javalang.parse.parse(java_code)
    strings_with_positions = [
        {
            'value': node.value[1:-1],
            "line_start": node.position.line,
            "line_end": node.position.line,
            "col_start":node.position.column,
            "col_end":node.position.column+len(node.value),
        }
        for path, node in tree
        if isinstance(node, javalang.tree.Literal) and isinstance(node.value, str) and node.value.startswith('"') and node.value.endswith('"')
    ]

    return strings_with_positions
if __name__ == '__main__':
    # 用法示例
    java_file_path = "/data2/gitleakage/project/detect_python/test_parser/java/BigDecimalMath.java"
    result = extract_java(java_file_path)
    print(result)