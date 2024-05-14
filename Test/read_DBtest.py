import mysql.connector

conn = mysql.connector.connect(
    host="192.168.100.148",
    user="root",
    password="password",
    port="30000",
    database="VM_archive_DB"
)

def mysql_read_data(conn):
    curs = conn.cursor()
    # テーブルの内容を表示
    curs.execute("SELECT VMname, ESXi,hash_value from VM_ARCHIVE_CHECK where complete = 'OK'")
    rows = curs.fetchall()
    curs.close()
    #print(rows)
    return rows


#mysql_read_data(conn)
