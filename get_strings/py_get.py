import ast

def extract_python(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
        strings = extract_strings_from_python_code(code)
        return strings

def extract_strings_from_python_code(code):
    strings = []

    def visit(node, parent_node):
        if isinstance(node, ast.Str):
            value = node.s
            line_start, col_start = node.lineno, node.col_offset
            line_end, col_end = node.end_lineno, node.end_col_offset
            strings.append({
                'value': value,
                'line_start': line_start,
                'line_end': line_end,
                'col_start': col_start,
                'col_end': col_end
            })
        for child_node in ast.iter_child_nodes(node):
            visit(child_node, node)

    parsed_ast = ast.parse(code)
    visit(parsed_ast, None)

    return strings
if __name__ == '__main__':
    # 用法示例
    python_file_path = "./main_arg.py"
    result = extract_python(python_file_path)

    print(result)