import os

current_path = os.path.dirname(os.path.abspath(__file__))
executable_path = os.path.abspath(os.path.join(current_path, 'go/extract_strings'))
print(executable_path)