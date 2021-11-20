import pymysql
import bcrypt
import pygame

pygame.mixer.init()

class Database(object):
    numScores=15
    def __init__(self,host='database-1.c79ahye2go7m.ap-northeast-2.rds.amazonaws.com',user='admin',password='letskirin',db='hiScores',charset='utf8'):
        self.scoreDB=pymysql.connect(host=host,user=user,password=password,db=db,charset=charset)
        self.cursor=self.scoreDB.cursor(pymysql.cursors.DictCursor)

    # def id_not_exists(self,input_id):
    #     sql="SELECT * FROM users WHERE user_id=%s"
    #     self.cursor.execute(sql,input_id)
    #     data=self.cursor.fetchone()
    #     self.cursor.close()
    #     if data:
    #         return False
    #     else:
    #         return True
        
    # def compare_data(self, id_text, pw_text): # 데이터베이스의 아이디와 비밀번호 비교
    # # 불러 오기
    #     input_password=pw_text.encode('utf-8')
    #     curs = self.score_db.cursor(pymysql.cursors.DictCursor)
    #     sql = "SELECT * FROM users WHERE user_id=%s"
    #     curs.execute(sql,id_text)
    #     data = curs.fetchone()
    #     curs.close()
    #     check_password=bcrypt.checkpw(input_password,data['user_password'].encode('utf-8'))
    #     return check_password


    # def add_id_data(self,user_id): # 아이디 추가
    #     #추가하기
    #     curs = self.score_db.cursor()
    #     sql = "INSERT INTO users (user_id) VALUES (%s)"
    #     curs.execute(sql, user_id)
    #     self.score_db.commit()  #서버로 추가 사항 보내기
    #     curs.close()


    # def add_password_data(self,user_password,user_id): # 비밀번호 추가
    #     #회원가입시 초기 경험치값은 0으로 설정
    #     #추가하기
    #     initial_exp=0
    #     new_salt=bcrypt.gensalt()
    #     new_password=user_password.encode('utf-8')
    #     hashed_password=bcrypt.hashpw(new_password,new_salt)
    #     decode_hash_pw=hashed_password.decode('utf-8')
    #     curs = self.score_db.cursor()
    #     sql = "UPDATE users SET user_password= %s WHERE user_id=%s"
    #     curs.execute(sql,(decode_hash_pw,user_id))
    #     self.score_db.commit()  #서버로 추가 사항 보내기
    #     curs = self.score_db.cursor()
    #     sql = "UPDATE users SET user_exp= %s WHERE user_id=%s"
    #     curs.execute(sql, (initial_exp, user_id))
    #     self.score_db.commit()
    #     curs.close()  

    def getSound(self,music=False):
        curs = self.scoreDB.cursor(pymysql.cursors.DictCursor)
        if music:
            curs.execute("CREATE TABLE if not exists music (setting integer)")
            curs.execute("SELECT * FROM music")
        else:
            curs.execute("CREATE TABLE if not exists sound (setting integer)")
            curs.execute("SELECT * FROM sound")
        self.scoreDB.commit()
        setting = curs.fetchall()
        print(setting)
        curs.close()
        print(bool(setting[0]))
        return bool(setting[0][0]) if len(setting) > 0 else False

    def setSound(self,setting, music=False):
        curs = self.scoreDB.cursor()
        if music:
            curs.execute("DELETE FROM music")
            curs.execute("INSERT INTO music VALUES (%s)", (setting,))
        else:
            curs.execute("DELETE FROM sound")
            curs.execute("INSERT INTO sound VALUES (%s)", (setting,))
        self.scoreDB.commit()
        curs.close()


    def getScores(self):
        curs = self.scoreDB.cursor()

        curs.execute('''CREATE TABLE if not exists scores
                     (name text, score integer, accuracy real)''')
        curs.execute("SELECT * FROM scores ORDER BY score DESC")
        self.scoreDB.commit()
        hiScores = curs.fetchall()
        curs.close()
        return hiScores

    def setScore(self,hiScores,name, score, accuracy):
        curs = self.scoreDB.cursor()
        print(len(hiScores))

        if len(hiScores) == Database.numScores:
            lowScoreName = hiScores[-1][0]
            lowScore = hiScores[-1][1]
            print(lowScoreName,lowScore)
            sql="DELETE FROM scores WHERE (name = %s AND score = %s)"
            curs.execute(sql,(lowScoreName,lowScore))
        sql="INSERT INTO scores VALUES (%s,%s,%s)"
        curs.execute(sql,(name, score, accuracy))
        self.scoreDB.commit()
        curs.close()
    

