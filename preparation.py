#!/usr/bin/env python3
import subprocess
import random
import os

def output_dict_result():
    command1 = ['df', '-h']
    command2 = ['grep', '/dev/sd']

    process1 = subprocess.Popen(command1, stdout=subprocess.PIPE)
    process2 = subprocess.Popen(command2, stdin=process1.stdout, stdout=subprocess.PIPE)

    # コマンド2の実行結果を取得
    output, error = process2.communicate()

    # 空の辞書を作成
    result_dict = {}

    # 行ごとに処理
    for line in output.decode().splitlines():
        # スペースで分割
        parts = line.split()

        # パーティションと使用量の情報を抽出
        partition = parts[5]
        usage_info = parts[2]

        # 辞書に追加
        if usage_info.endswith('K'):
            usage_bytes = float(usage_info[:-1]) * 1024
        elif usage_info.endswith('M'):
            usage_bytes = float(usage_info[:-1]) * 1024 * 1024
        elif usage_info.endswith('G'):
            usage_bytes = float(usage_info[:-1]) * 1024 * 1024 * 1024
        elif usage_info.endswith('T'):
            usage_bytes = float(usage_info[:-1]) * 1024 * 1024 * 1024 * 1024
        else:
            usage_bytes = float(usage_info)

        result_dict[partition] = int(round(usage_bytes))
    # 結果を表示
    return result_dict

#容量の比較
def output_result_comparison():
    data = output_dict_result()
    
    min_value = min(int(v) for v in data.values())
    min_keys = [k for k, v in data.items() if int(v) == min_value]

    random_min_key = random.choice(min_keys)
    #print(random_min_key)
    return random_min_key


#送る対象を見つける関数
def output_send_target():
    dir_path = "/mnt/iscsi/target-mini2/VM-archive"
    output_send_target = os.listdir(dir_path)
    absolute_paths = [os.path.join(dir_path, item) for item in output_send_target]
    #print(absolute_paths[50])
    return absolute_paths

#output_send_target()