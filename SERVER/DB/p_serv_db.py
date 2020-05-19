import pymysql

connect = pymysql.connect(host="localhost",
                          port=3306,
                          user="사용자이름",
                          password="비번",
                          db="DB이")

cursor = connect.cursor()

cursor.execute("SELECT *FROM USER")
result = cursor.fetchall()

print(result)
