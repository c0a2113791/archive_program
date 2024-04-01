#!/usr/bin/env python3
import subprocess
import logging
from preparation import output_result_comparison
from preparation import output_send_target
logging.basicConfig(format='[%(asctime)s]\t%(levelname)s\t%(message)s', datefmt='%d/%b/%Y:%H:%M:%S %z',filename='/var/log/archive.log',level=logging.INFO)

def archive():
    logging.info("Archiving process started.")
    # 出力先とディレクトリの取得
    
    # rsyncするVMarchiveのディレクトリを取得
    archive_dir = output_send_target()
    #print(archive_dir)
    # ターゲットディレクトリの取得
    for i in range(51,60):
        # rsync先のHDDを選択
        archive_destination = output_result_comparison()
        print(archive_destination)
        logging.info("Rsync destination: %s",archive_destination)
        # ターゲットディレクトリの選択
        archive_dir_target = archive_dir[i - 1]
        print(archive_dir_target)
        logging.info("Rsync source: %s",archive_dir_target)

        try:
            # rsyncコマンドの実行
            rsync_command = ['sudo','rsync', '-av', archive_dir_target, archive_destination]
            subprocess.run(rsync_command, check=True)
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
