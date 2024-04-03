import os
import math

def get_directory_size(directory):
    total_size = 0
    # ディレクトリ内のすべてのファイルとディレクトリについて処理を行う
    for root, dirs, files in os.walk(directory):
        # 各ディレクトリについてサイズを合計する
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            # サブディレクトリのサイズを再帰的に取得して合計する
            total_size += get_directory_size(dir_path)
        # ディレクトリ内のファイルのサイズを合計する
        for file_name in files:
            file_path = os.path.join(root, file_name)
            total_size += os.path.getsize(file_path)
    return total_size

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_names[i])

def get_subdirectories_size(directory):
    subdirectories_size = {}
    # ディレクトリ内のすべてのサブディレクトリについて処理を行う
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            # サブディレクトリのサイズを取得する
            dir_size = get_directory_size(dir_path)
            subdirectories_size[dir_path] = dir_size
    return subdirectories_size

# ディレクトリのパスを指定してサブディレクトリのサイズを取得する
directory_path = '/mnt/iscsi/target-mini2/VM-archive'
subdirectories_size = get_subdirectories_size(directory_path)

# 各サブディレクトリのサイズを表示する
for subdirectory, size in subdirectories_size.items():
    print(f"Subdirectory: {subdirectory}, Size: {convert_size(size)}")
