import os
import re

def rename_files(directory):
    """Rename files in the specified directory."""
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            old_filename = filename
            while True:
                new_filename = re.sub(r'(\d{4}-\d{2}-\d{2}--)*', '', old_filename)  # 删除多余的日期前缀
                new_filename = re.sub(r'(_translated)+', '_translated', new_filename)  # 删除多余的"_translated"后缀
                if new_filename == old_filename:
                    break
                old_filename = new_filename
            new_file_path = os.path.join(directory, new_filename)
            if not os.path.exists(new_file_path):
                os.rename(os.path.join(directory, filename), new_file_path)


# 使用方法：将下面的"path_to_directory"替换为你的目录路径
rename_files("E:/code/runes780.github.io/_posts")