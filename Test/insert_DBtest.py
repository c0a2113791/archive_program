import mysql.connector
from read_DBtest import mysql_read_data


def mysql_insert_data(conn,time,VM_path,ESXi,hash_value):
    curs = conn.cursor()
    insert_query = """
  INSERT INTO `AFTER_ARCHIVE_DATA` (date_time, VM_path, ESXi, hash_value)
    VALUES (%s, %s, %s, %s)
    """
    data = (time, VM_path, ESXi, hash_value)
    curs.execute(insert_query,data)
    conn.commit()  # 変更をコミット

    curs.close()
    

#current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#data = (current_datetime,"test","test","test")
#mysql_insert_data(conn,data)
