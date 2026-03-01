import os
import magic
import shutil
from typing import Dict, Set

# ===================================================================================
# --- 用户指定的路径配置 (Windows路径) ---
# ===================================================================================

# 您的 120 万个文件所在的根目录
SOURCE_DIR = r'D:\dev\keysentinel-project\test_data\input'
# 存放 KEYSENTINEL 可扫描文件的软链接的目标目录
TARGET_DIR_ROOT = r'D:\dev\keysentinel-project\test_data\output_links'
# 存放纯二进制文件的文件路径列表的目录
BINARY_FILES_DIR = r'D:\dev\keysentinel-project\test_data\binary_files'

# 存放纯二进制文件的文件路径列表（文件将创建在 BINARY_FILES_DIR 中）
BINARY_FILES_LIST = os.path.join(BINARY_FILES_DIR, "binary_files_list.txt")

# ===================================================================================
# --- 扫描配置 (保持不变，已包含扩展后的 MIME 类型) ---
# ===================================================================================

# KEYSENTINEL 需要扫描的 MIME 类型白名单 (基于语义分析能力)
SCAN_MIMETYPES: Set[str] = {
    # 核心代码类型
    'text/x-python',  # Python (.py)
    'application/javascript',  # JavaScript (.js) / 编译后的小程序代码
    'text/javascript',  # JavaScript (别名)
    'application/json',  # JSON (.json) / 小程序配置
    'application/x-yaml',  # YAML (.yml/.yaml) / 配置模板
    'image/svg+xml',  # SVG (XML 格式，含大量文本)
    'text/html',  # HTML / WXML (.wxml)
    'text/xml',  # XML (如配置)
    'text/markdown',  # Markdown (.md)
    'text/plain',  # 纯文本 (Text) / 无法识别语法的代码或文档
    'text/x-sh',  # Shell Script
    'text/x-typescript',  # TypeScript
    'text/x-c',  # C/C++
    'text/x-java',  # Java
}

# MIME 类型到文件扩展名的映射
MIME_TO_EXT: Dict[str, str] = {
    'text/x-python': '.py',
    'application/json': '.json',
    'application/x-yaml': '.yaml',
    'image/svg+xml': '.svg',
    'text/html': '.html',
    'text/markdown': '.md',
    'application/javascript': '.js',
    'text/javascript': '.js',
    'text/plain': '.txt',
    # 添加常见的编码文件
    'text/x-c': '.c',
    'text/x-java': '.java',
}


# --- 函数定义 ---

def classify_and_link_files():
    """
    遍历源目录中的文件，根据其 MIME 类型进行分类，并创建软链接或记录二进制文件。
    """
    if not os.path.exists(SOURCE_DIR):
        print(f"错误: 源代码目录 {SOURCE_DIR} 不存在。请检查路径。")
        return

    # 创建目标目录，如果不存在
    os.makedirs(TARGET_DIR_ROOT, exist_ok=True)
    os.makedirs(BINARY_FILES_DIR, exist_ok=True)

    # 初始化文件类型检测器
    try:
        mime = magic.Magic(mime=True)
    except Exception as e:
        print(f"初始化 python-magic 失败: {e}")
        print("请确保已安装 python-magic 库和 libmagic 库。")
        print("Windows 用户请运行: pip install python-magic-bin")
        return

    binary_file_paths = []
    processed_count = 0
    scanned_count = 0
    binary_count = 0

    for filename in os.listdir(SOURCE_DIR):
        full_path = os.path.join(SOURCE_DIR, filename)

        if not os.path.isfile(full_path) or os.path.islink(full_path):
            continue

        processed_count += 1
        if processed_count % 10000 == 0:
            print(f"已处理文件数量: {processed_count}...")

        try:
            file_mime = mime.from_file(full_path)

            # 针对编码问题，尝试更细粒度的检查 (例如 .txt 可能包含代码)
            if file_mime.startswith('text/plain'):
                try:
                    content = open(full_path, 'r', errors='ignore').read(1024)
                    if any(k in content for k in
                           ['import', 'def ', 'class ', '{', ':', 'function', '//', 'public static']):
                        file_mime = 'text/plain_code'
                except:
                    pass

        except Exception as e:
            print(f"警告: 无法处理文件 {filename}: {e}")
            file_mime = "application/octet-stream"  # 无法打开或识别

        # 核心分类逻辑
        if file_mime in SCAN_MIMETYPES or file_mime.startswith('text/') or file_mime == 'text/plain_code':
            # 1. 文本/代码文件: 创建带扩展名的软链接供 KEYSENTINEL 扫描

            ext = MIME_TO_EXT.get(file_mime, '.txt')

            # 针对微信小程序 WXML 文件进行特殊识别（通常被识别为 text/html）
            if ext == '.html':
                try:
                    # 快速检查 WXML 特征，如 <wxs> 标签
                    content = open(full_path, 'r', errors='ignore').read(2048)
                    if '<wxs ' in content:
                        ext = '.wxml'
                except:
                    pass

            target_filename = filename + ext
            target_path = os.path.join(TARGET_DIR_ROOT, target_filename)

            try:
                if not os.path.exists(target_path):
                    # 在 Windows 上创建软链接
                    # 需要管理员权限或启用开发者模式
                    try:
                        os.symlink(os.path.abspath(full_path), target_path)
                    except OSError as os_err:
                        if "privilege" in str(os_err).lower() or "access denied" in str(os_err).lower():
                            # 如果没有权限创建符号链接，改为复制
                            print(f"\n提示: 无符号链接权限，正在复制文件 {filename}...")
                            shutil.copy2(full_path, target_path)
                        else:
                            raise
            except Exception as e:
                # 软链接失败（如权限问题或旧系统），则回退到复制文件
                # 注意：对于 1.2M 文件，复制非常耗时！
                print(f"\n警告: 软链接失败 ({e})，正在复制文件 {filename}...")
                try:
                    shutil.copy2(full_path, target_path)
                except Exception as copy_err:
                    print(f"错误: 复制文件失败 {filename}: {copy_err}")

            scanned_count += 1

        else:
            # 2. 纯二进制文件: 记录路径供后续 strings 命令处理
            binary_file_paths.append(full_path)
            binary_count += 1

    # 写入纯二进制文件的列表
    try:
        with open(BINARY_FILES_LIST, 'w', encoding='utf-8') as f:
            f.write('\n'.join(binary_file_paths))
    except Exception as e:
        print(f"警告: 无法写入二进制文件列表: {e}")

    print("\n" + "=" * 70)
    print(f"✅ 文件分类完成。总计处理文件: {processed_count} 个")
    print(f"   - 可扫描文件 (文本/代码): {scanned_count} 个")
    print(f"   - 纯二进制文件: {binary_count} 个")
    print(f"\n📁 输出位置:")
    print(f"   - KEYSENTINEL 可扫描文件已放入: {TARGET_DIR_ROOT}")
    print(f"   - 纯二进制文件列表已保存至: {BINARY_FILES_LIST}")
    print("=" * 70)


if __name__ == '__main__':
    classify_and_link_files()