import mysql.connector

def hostname_table_create(host,user,password,port,database):
    cconn = mysql.connector.connect(
      host=str(host),
      user=str(user),
      password=str(password),
      port=str(port),
      database=str(databas)
    )
    curs = conn.cursor()
    # テーブル作成(VM-archive用)
    create_table_query1 = """
    CREATE TABLE IF NOT EXISTS `hashtable_sendtoVM_archive` (
      id VARCHAR(255) NOT NULL,
      VMname VARCHAR(255) NOT NULL,
      `hash-value` VARCHAR(255) NOT NULL,
      `date-and-time` VARCHAR(255) NOT NULL,
      Processing VARCHAR(255) NOT NULL
    )
    """
    curs.execute(create_table_query1)

    # テーブル作成(HDD用)
    create_table_query2 = """
    CREATE TABLE IF NOT EXISTS `hashtable_sendtoHDD` (
      id VARCHAR(255) NOT NULL,
      VMname VARCHAR(255) NOT NULL,
      `hash-value` VARCHAR(255) NOT NULL,
      `date-and-time` VARCHAR(255) NOT NULL,
      Processing VARCHAR(255) NOT NULL
    )
    """
    curs.execute(create_table_query2)


def insert_data(host,user,password,port,databas):
    conn = mysql.connector.connect(
      host=str(host),
      user=str(user),
      password=str(password),
      port=str(port),
      database=str(databas)
    )
    curs = conn.cursor()

    # データの挿入
    for i in range(1):
        insert_query = """
        INSERT INTO `hashtable_sendtoVM_archive` (id, VMname, `hash-value`, `date-and-time`, Processing)
        VALUES (%s, %s, %s, %s, %s)
        """
        data = (str(i), "test", "test", "test", "test")
        curs.execute(insert_query, data)
        conn.commit()  # 変更をコミット

    # テーブルの内容を表示
    curs.execute("SELECT * FROM `hashtable_sendtoVM_archive`")
    rows = curs.fetchall()
    for row in rows:
        print(row)

    curs.close()
    conn.close()
#hostname_table_create("192.168.100.148","root","password","30000","hashdatabase")
insert_data("192.168.100.148","root","password","30000","hashdatabase")