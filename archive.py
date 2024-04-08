#!/usr/bin/env python3
import subprocess
import logging
from preparation import output_result_comparison
from preparation import output_send_target
from preparation import generate_destination_storage
from hash import calculate_md5

# ****logの形式を変更する****
logging.basicConfig(format='[%(asctime)s]\t%(levelname)s\t%(message)s', datefmt='%d/%b/%Y:%H:%M:%S %z',filename='/var/log/archive.log',level=logging.INFO)

def archive():
    logging.info("Archiving process started.")
    # 出力先とディレクトリの取得
    
    # rsyncするVMarchiveのディレクトリを取得
    archive_dir = output_send_target()
    # rsync後のstorage内のディレクトリを取得
    storage_dir = generate_destination_storage()
    #print(archive_dir)
    # ターゲットディレクトリの取得
    for i in range(59,60):
        # rsync先のHDDを選択
        archive_destination = output_result_comparison()
        #print(archive_destination)
        logging.info("Rsync destination: %s",archive_destination)
        # ターゲットディレクトリの選択
        archive_dir_target = archive_dir[i]
        storage_dir_target = storage_dir[i]
        #print(archive_dir_target)
        logging.info("Rsync source: %s",archive_dir_target)

        try:
            # rsyncコマンドの実行
            rsync_command = ['sudo','rsync', '-av', archive_dir_target, archive_destination]
            subprocess.run(rsync_command, check=True)
            hash_VM_archive = calculate_md5(archive_dir_target)
            hash_storage = calculate_md5(storage_dir_target)
            
            while hash_storage != hash_VM_archive:
                print("The contents of the files do not match.")
                subprocess.run(rsync_command, check=True)
                hash_VM_archive = calculate_md5(archive_dir_target)
                hash_storage = calculate_md5(storage_dir_target)
                
            print("rsync completed successfully.")
            logging.info("Rsync completed successfully.")

        except subprocess.CalledProcessError as e:
            print(f"Error: rsync command failed with return code {e.returncode}")
            print(e.output)
            logging.error("Rsync failed with return code %s", e.returncode)
            logging.error(e.output)

    logging.info("Archiving process started.")
# archive関数の呼び出し
archive()
