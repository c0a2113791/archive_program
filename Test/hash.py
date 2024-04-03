import os
import hashlib
from preparation import output_result_comparison
from preparation import output_send_target

def cal_dir_hash(dir):
    dir_hash = hashlib.md5()
    #ディレクトリ内を走査
    for root, dirs, files in os.walk(dir):
        for filename in files:
            file_path = os.path.join(root,filename)
            with open(file_path,'rb')as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    dir_hash.update(data)
                    print(f"Hashing file: {file_path} ({f.tell()} bytes processed)")
    return dir_hash.hexdigest()

dir1 = "/test/test1.txt"
dir2 = "/test_sub/test1.txt"

hash1 = cal_dir_hash(dir1)
hash2 = cal_dir_hash(dir2)

print(hash1)
print(hash2)

#if hash1 == hash2:
#    print("The contents of the directories are identical.")
#else:
#    print("The contents of the directories do not match.")