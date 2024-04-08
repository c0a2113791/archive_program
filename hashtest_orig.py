import hashlib
import os
from preparation import output_result_comparison
from preparation import output_send_target

def hash_file_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(9900000), b''):
            hasher.update(chunk)
            print(f"Hashing file: {file_path} ({f.tell()} bytes processed)")
    return hasher.hexdigest()

def hash_directory_md5(directory):
    file_hashes = {}
    # ディレクトリ内のファイルをソートしてリスト化
    files = sorted([os.path.join(root, file) for root, _, files in os.walk(directory) for file in files])
    for file_path in files:
        # 各ファイルに対してハッシュ値を計算し、辞書に追加
        file_hashes[file_path] = hash_file_md5(file_path)

    
    return file_hashes


#directory1 = output_result_comparison()
#directory2 = output_send_target()


#file_hashes1 = hash_directory_md5(directory1)
#file_hashes2 = hash_directory_md5(directory2)



#for file_path1, hash_value1 in file_hashes1.items():
    print(f"{file_path1}: {hash_value1}")
#for file_path2, hash_value2 in file_hashes2.items():
    print(f"{file_path2}: {hash_value2}")

#if hash_value1 == hash_value2:
#    print("The contents of the directories are identical.")
##else:
#    print("The contents of the directories do not match.")