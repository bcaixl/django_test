from pymysql import cursors, connect

# 连接数据库
conn = connect(host='127.0.0.1', user='root', password='123456', db='guest',
               charset='utf8mb4', cursorclass=cursors.DictCursor)
try:
    with conn.cursor() as cursor:
        sql = 'INSERT INTO sign_guest (realname, phone, email, sign, event_id, create_time) VALUES ("tom", 18800100012, "tom@mail.com", 0, 1,NOW());'
        cursor.execute(sql)
    conn.commit()

    with conn.cursor() as cursor:
        sql = "SELECT * FROM sign_guest WHERE phone=%s"
        cursor.execute(sql, ('18800100012',))
        result = cursor.fetchone()
        print(result)
finally:
    conn.close()
