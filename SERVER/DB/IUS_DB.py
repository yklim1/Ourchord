import pymysql

uid = 'flottante'
pwd = '1234'

connect = pymysql.connect(host="",
                          port=,
                          user="",
                          password="",
                          db="")

cursor = connect.cursor()

# EXISTS 테스트------------------------------------------------------------------
sql ="SELECT EXISTS(SELECT *FROM USER WHERE ID=%s AND PWD=%s)"
res = cursor.execute(sql, (uid, pwd))
result = cursor.fetchone()
row_count = result[0]
print(row_count)

if (row_count > 0):  # 수정: line193의 결과가 있으면 print("정보있음)
    connect.commit()
    print('정보있음')  # 정보 있음도 sql문을 실행하고 결과값이 있을때 출력함
    impdata = uid
    print("impdata는", uid)
else:
    print('정보없음')

# INSERT 테스트------------------------------------------------------------------
cursor.execute("SELECT * FROM USER")
before = cursor.rowcount
print('before: ', before)

uid = 'user7'
sql ="INSERT INTO USER(USERNAME, ID, PWD, EMAIL, AUTH) values(%s, %s, %s, %s, '')"
cursor.execute(sql, (uid, 'uu1', '0622', 'u@kpu.ac.kr'))

cursor.execute("SELECT * FROM USER")
after = cursor.rowcount
print("after: ", after)

if(before < after):
    print('삽입 성공')


# UPDATE 테스트------------------------------------------------------------------
sql1 ="UPDATE USER SET PWD=%s WHERE USERNAME=%s"
cursor.execute(sql1, ('622', uid))
#print(res)
connect.commit()
print('업데이트 성공')

# select문에 해당하는 row 출력
query ="SELECT * FROM USER WHERE USERNAME=%s"
cursor.execute(query, uid)
result = cursor.fetchall()
print(result)
