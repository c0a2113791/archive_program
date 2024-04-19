#!/usr/bin/env python3
import mysql.connector
import subprocess
import logging
from preparation import output_result_comparison
from preparation import output_send_target
from preparation import generate_destination_storage
from hash import calculate_md5
from read_DBtest import mysql_read_data
from insert_DBtest import mysql_insert_data
from datetime import datetime
# ****logの形式を変更する****
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logging.basicConfig(format='[%(asctime)s]\t%(levelname)s\t%(message)s', datefmt='%d/%b/%Y:%H:%M:%S %z',filename='/var/log/archive.log',level=logging.INFO)
#DBに接続
conn = mysql.connector.connect(
    host="192.168.100.148",
    user="root",
    password="password",
    port="30000",
    database="VM_archive_DB"
)

rows = mysql_read_data(conn)

def archive():
    logging.info("Archiving process started.")
    # rsync後のstorage内のディレクトリを取得
    # ターゲットディレクトリの取得
    for i,row in enumerate(rows):
        vmname,esxi,hash_value = row 
        #print(row)
        retry_count = 0
        max_retries = 2
        #print(esxi,hash_value)
        # rsyncするVMarchiveのディレクトリを取得
        archive_dir = f"/mnt/iscsi/target-mini2/VM-archive/{vmname}"
        # rsync先のHDDを選択
        
        #print(archive_destination)
        storage_dir = generate_destination_storage(conn,vmname)
        # ターゲットディレクトリの選択
        archive_destination = output_result_comparison()
        logging.info("Rsync destination: %s",archive_destination)
        
        logging.info("Rsync source: %s",archive_dir)
        #　リトライは２回まで
        while retry_count < max_retries:
            try:
                #print(archive_dir)
                # rsyncコマンドの実行
                rsync_command = ['sudo','rsync', '-av', archive_dir, archive_destination]
                subprocess.run(rsync_command, check=True)
                #print(f"rysnc_data{archive_dir}")
                
                hash_VM_archive = hash_value
                hash_storage = calculate_md5(storage_dir)
                if hash_storage == hash_VM_archive:
                    print("rsync completed successfully.\n")
                    #ここにrsync完了したらDB(INSERT_AFTER_DATA)に書き込む
                    mysql_insert_data(conn,current_datetime,vmname,esxi,hash_storage)
                    logging.info("Rsync completed successfully.")
                    break
                else:
                    print(f"Hash values do not match for {vmname}. Retrying rsync...")
                    retry_count += 1

            except subprocess.CalledProcessError as e:
                print(f"Error: rsync command failed with return code {e.returncode}")
                print(e.output)
                logging.error("Rsync failed with return code %s", e.returncode)
                logging.error(e.output)
                retry_count += 1

    logging.info("Archiving process started.")
    conn.close()
# archive関数の呼び出し
archive()
