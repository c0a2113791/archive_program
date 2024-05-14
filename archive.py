#!/usr/bin/env python3
import mysql.connector
import subprocess
import logging
import os
from preparation import convert_to_bytes
from preparation import output_dict_result
from preparation import output_result_comparison
from preparation import output_send_target
from preparation import generate_destination_storage
from hash import calculate_md5
from read_DB import mysql_read_data
from insert_DB import mysql_insert_data
from delete import oldest_VM_path
from delete import del_check_data
from datetime import datetime
# ****logの形式を変更する****

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
#storage_dir = output_result_comparison()

cur = conn.cursor()

def archive():
    logging.info("Archiving process started.")
    # rsync後のstorage内のディレクトリを取得
    # ターゲットディレクトリの取得
    for i,row in enumerate(rows):
        date_time, vmname,esxi,hash_value,user,VM_size = row 
        data,storage_capacity = output_dict_result()
        #print(row)
        conv_size = convert_to_bytes(VM_size)
        retry_count = 0
        max_retries = 2
        #print(esxi,hash_value)
        # rsyncするVMarchiveのディレクトリを取得
        archive_dir = f"/mnt/iscsi/target-mini2/VM-archive/{vmname}"
        # rsync先のHDDを選択
        
        #print(archive_destination)
        storage_dir = output_result_comparison()

        # ターゲットディレクトリの選択
        archive_destination = os.path.join(storage_dir, vmname)
        logging.info("Rsync source: %s",archive_dir)
        logging.info("Rsync destination: %s",archive_destination)

        #　リトライは２回まで
        while retry_count < max_retries:
            try:
                if conv_size < storage_capacity[storage_dir]:
                    #print(archive_dir)
                    # rsyncコマンドの実行
                    rsync_command = ['sudo','rsync', '-av', archive_dir, storage_dir]
                    subprocess.run(rsync_command, check=True)
                    #print(f"rysnc_data{archive_dir}")
                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    hash_VM_archive = hash_value
                    hash_storage = calculate_md5(archive_destination)
                    VM_path = archive_destination.replace("/home/c0a21137/","")

                    rsync_start_query = "INSERT INTO HISTORY_OF_HDD (date_time, VM_path, ESXi, user, Processing) VALUES (%s, %s, %s, %s, %s)"
                    cur.execute(rsync_start_query, (current_datetime, VM_path, esxi, user, 'Archiving process started'))
                    conn.commit()

                    if hash_storage == hash_VM_archive:
                        print("rsync completed successfully.\n")
                        #ここにrsync完了したらDB(INSERT_AFTER_DATA)に書き込む
                        mysql_insert_data(conn,current_datetime,VM_path,esxi,hash_storage,user,VM_size)
                        #rsync完了したら，VM_ARCHIVE_CHECKから該当データを消す
                        logging.info("Rsync completed successfully.")
                        rsync_end_query = "INSERT INTO HISTORY_OF_HDD (date_time, VM_path, ESXi, user, Processing) VALUES (%s, %s, %s, %s, %s)"
                        cur.execute(rsync_end_query, (current_datetime, VM_path, esxi, user, 'Archiving process successfully'))
                        del_check_data(conn,vmname,esxi,user,hash_value)
                        conn.commit()
                        break
                    else:
                        print(f"Hash values do not match for {vmname}. Retrying rsync...")
                        retry_count += 1
                # ここで容量が足りなくなった時の処理を行う．
                # データ削除
                else:
                    print("Not enough storage space.")
                    logging.info("Not enough storage space.")
                    old_vm = oldest_VM_path(conn)
                    os.rmdir(old_vm)
                    print("Directory deleted successfully.")
                    logging.info("Directory deleted successfully.")

            except subprocess.CalledProcessError as e:
                print(f"Error: rsync command failed with return code {e.returncode}")
                print(e.output)
                logging.error("Rsync failed with return code %s", e.returncode)
                logging.error(e.output)
                retry_count += 1

    logging.info("Archiving process finished.")
    conn.close()
# archive関数の呼び出し
archive()
