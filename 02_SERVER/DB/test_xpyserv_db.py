#psycopg2말고--> pymysql사용예정
#python에서 rds접근 test용
import psycopg2 
# DB 정보 입력
conn_string = "host='localhost' " \
              "port= 3306" \
              "dbname ='DB이름' " \
              "user='사용자이름' " \
              "password='비밀번호'"
conn = psycopg2.connect(conn_string)
print("연결전")

# DB 연결
cur = conn.cursor()
print("연결성공")

# DB 데이터 가져오기
# USERNAME, ID, PWD, CPWD, EMAIL 컬럼을 가지는 USER 테이블
# 특정 컬럼(USERNAME, EMAIL)의 데이터를 result에 저장
cur.execute("SELECT USERNAME, ID, PWD, CPWD, EMAIL FROM USER order by USERNAME, EMAIL;")
result = cur.fetchall()

# result에 저장된 값 출력
print(result)

# 연결종료
cur.close()
conn.close()
