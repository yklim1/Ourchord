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

print("USER 테이블 전체 조회")
print(result)
print("--------------------------------------------")

print("USER 테이블 첫번째 줄 조회")
print(result[0])
print("--------------------------------------------")


#USER_SCORE_PDF 테이블 전체 조회
cursor.execute("SELECT *FROM USER_SCORE_PDF")
result = cursor.fetchall()
print("USER_SCORE_PDF 테이블 조회")
print(result)
print("--------------------------------------------")

#집어넣기
#USER 테이블 삽입
print("USER 테이블 삽입시작")
#sql = "INSERT INTO USER(USERNAME, ID, PWD, CPWD, EMAIL) values(%s %s %s %s %s)"
cursor.execute("INSERT INTO USER(USERNAME, ID, PWD, CPWD, EMAIL) values('토정기', 5020, 5020, 7878, 'toeic@google.com')")
#cursor.commit()
print("USER 테이블 삽입완료")
print("--------------------------------------------")

#USER 테이블 삽입 후 전체 재조회
cursor.execute("SELECT *FROM USER")
result = cursor.fetchall()
print("USER 테이블 조회")
print(result)
print("--------------------------------------------")

'''참조무결성 에러발생!
print("USER_SCORE_PDF 테이블 삽입시작")
#PDF_SAVE INSERT에서 문제 생긴거 같음
#sql = "INSERT INTO USER_SCORE_PDF(PDF_ID, PDF_NAME, PDF_PATH, PDF_SAVE) values(%s %s %s %s)"
#cursor.execute(sql, ('minji', '1.pdf', '/home/ec2-user/Ourchord/PDF/1.pdf', '2020-05-20'))
#sql = "INSERT INTO USER_SCORE_PDF(PDF_ID, PDF_NAME, PDF_PATH, PDF_SAVE) values(%s %s %s %s)"
cursor.execute("INSERT INTO USER_SCORE_PDF(PDF_ID, PDF_NAME, PDF_PATH, PDF_SAVE) values('minji', '1.pdf', "
               "'/home/ec2-user/Ourchord/PDF/1.pdf', '2020-05-20')")
print("USER_SCORE_PDF 테이블 삽입완료")
print("--------------------------------------------")

#USER_SCORE_PDF 테이블 삽입 후 전체 재조회
cursor.execute("SELECT *FROM USER_SCORE_PDF")
result = cursor.fetchall()
print("USER_SCORE_PDF 테이블 조회")
print(result)
print("--------------------------------------------")'''
