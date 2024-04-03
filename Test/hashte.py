import hashlib
import os

def hash_file_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(60000), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def hash_directory_md5(directory):
    file_hashes = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hashes[file_path] = hash_file_md5(file_path)
    return file_hashes

directory1 ="/home/c0a21137/Test/test"
directory2 ="/home/c0a21137/Test/test_sub"

file_hashes1 = hash_directory_md5(directory1)
file_hashes2 = hash_directory_md5(directory2)



for file_path1, hash_value1 in file_hashes1.items():
    print(f"{file_path1}: {hash_value1}")
for file_path2, hash_value2 in file_hashes2.items():
    print(f"{file_path2}: {hash_value2}")

if hash_value1 == hash_value2:
    print("The contents of the directories are identical.")
else:
    print("The contents of the directories do not match.")
