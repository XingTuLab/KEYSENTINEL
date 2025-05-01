import json
import os
import subprocess

def extract_js(file_path):
    current_path = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.abspath(os.path.join(current_path, 'execute_js.js'))

    try:
        result = subprocess.run(['node', script_path,file_path], capture_output=True, text=True, check=True)
        output = json.loads(result.stdout)
        return output
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    file_path="./shared.spec.ts"
    output = extract_js(file_path)

    print(output)