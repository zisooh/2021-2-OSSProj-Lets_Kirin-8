import pymysql
import bcrypt

class Database(object):
    numScores = 15
    def __init__(self,host='database-1.c79ahye2go7m.ap-northeast-2.rds.amazonaws.com',user='admin',password='letskirin',db='hiScores',charset='utf8'):
        self.scoreDB=pymysql.connect(host=host,user=user,password=password,db=db,charset=charset)
        self.cursor=self.scoreDB.cursor(pymysql.cursors.DictCursor)

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
        curs.close()
        return bool(setting[0][0]) if len(setting) > 0 else False

    def setSound(self,setting, music=False):
        curs = self.scoreDB.cursor()
        if music:
            curs.execute("DELETE FROM music")
            curs.execute("INSERT INTO music VALUES (?)", (setting,))
        else:
            curs.execute("DELETE FROM sound")
            curs.execute("INSERT INTO sound VALUES (?)", (setting,))
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

        if len(hiScores) == Database.numScores:
            lowScoreName = hiScores[-1][0]
            lowScore = hiScores[-1][1]
            sql="DELETE FROM scores WHERE (name = %s AND score = %s)"
            curs.execute(sql,(lowScoreName,lowScore))
        sql="INSERT INTO scores VALUES (%s,%s,%s)"
        curs.execute(sql,(name, score, accuracy))
        self.scoreDB.commit()
        curs.close()
