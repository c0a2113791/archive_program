#!/bin/bash

hash_file_md5() {
    file_path=$1
    md5sum "$file_path" | awk '{print $1}'
}

hash_directory_md5() {
    directory=$1
    find "$directory" -type f | while read -r file; do
        hash_file_md5 "$file"
    done
}

directory="/home/c0a21137/Test/test/test1.txt"
hash_directory_md5 "$directory"
