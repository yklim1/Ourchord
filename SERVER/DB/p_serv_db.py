#python에서 rds접근 test용
import pymysql

#mysql연동
connect = pymysql.connect(host="localhost",
                          port=3306,
                          user="사용자이름",
                          password="비번",
                          db="DB이름")

#aws rds에서 커서 cursor얻기
#cursor: DB에서 sql문장 수행역할하기 위함
cursor = connect.cursor()

#USER테이블 전체 조회
cursor.execute("SELECT *FROM USER")

#result에 저장(데이터 패치)
result = cursor.fetchall()

print(result)
