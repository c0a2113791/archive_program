#!/usr/bin/env python3
import hashlib  # ハッシュ関数を提供するhashlibモジュールをインポート
import os       # オペレーティングシステムとのやり取りを行うosモジュールをインポート
from preparation import output_result_comparison
from preparation import output_send_target
from preparation import generate_destination_storage

#　ここでは計算するだけ，計算するディレクトリはarchive.pyで選出してそれを受け取って比較する．

def calculate_md5(directory):
    files = []  # ファイルパスを格納する空のリストを初期化
    for f in os.listdir(directory):
        file_path = os.path.join(directory, f)  # ファイル/ディレクトリのパスを作成
        if os.path.isfile(file_path):  # アイテムがファイルであるかを確認
            files.append(file_path)     # ファイルパスをファイルのリストに追加
    
    files.sort()  # ファイルのリストをアルファベット順にソート
    
    md5_hash = hashlib.md5()
    
    # ファイルリスト内の各ファイルについて繰り返す
    for file_path in files:
        #print(file)
        # ファイルをバイナリモードで開く
        with open(file_path, "rb") as f:
            # ファイルの内容を読み取り、MD5ハッシュを更新
            md5_hash.update(f.read(65553))
            print(f"Hashing file: {file_path} ({f.tell()} bytes processed)")

    # MD5ハッシュの16進数表現を返す
    return md5_hash.hexdigest()

def test():
    directory1 = generate_destination_storage()
    directory2 = output_send_target()

    print(directory1[59])
    print(directory2[59])

    file_hashes1 = calculate_md5(directory1[59])
    file_hashes2 = calculate_md5(directory2[59])

    print(file_hashes1)
    print(file_hashes2)

