import os
import sqlite3
import pymysql

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')


class Database(object):
    #path = os.path.join(data_dir, 'hiScores.db')
    numScores = 15
    def __init__(self):
        self.score_db=pymysql.connect(
            user='admin',
            password='letskirin',
            host='database-1.c79ahye2go7m.ap-northeast-2.rds.amazonaws.com',
            db='hiScores',
            charset='utf8'
        )
    @staticmethod
    def getSound(self,music=False):
        
        curs = self.score_db.cursor()
        if music:
            curs.execute("CREATE TABLE if not exists music (setting integer)")
            curs.execute("SELECT * FROM music")
        else:
            curs.execute("CREATE TABLE if not exists sound (setting integer)")
            curs.execute("SELECT * FROM sound")
        self.score_db.commit()
        setting = curs.fetchall()
        curs.close()
        return bool(setting[0][0]) if len(setting) > 0 else False

    @staticmethod
    def setSound(self,setting, music=False):
        curs = self.score_db.cursor()
        if music:
            curs.execute("DELETE FROM music")
            curs.execute("INSERT INTO music VALUES (?)", (setting,))
        else:
            curs.execute("DELETE FROM sound")
            curs.execute("INSERT INTO sound VALUES (?)", (setting,))
        self.score_db.commit()
        curs.close()

    @classmethod
    def getScores(self):
        curs = self.score_db.cursor()

        curs.execute('''CREATE TABLE if not exists scores
                     (name text, score integer, accuracy real)''')
        curs.execute("SELECT * FROM scores ORDER BY score DESC")
        self.score_db.commit()
        hiScores = curs.fetchall()
        curs.close()
        return hiScores

    @staticmethod
    def setScore(self,hiScores,entry):
        curs = self.score_db.cursor()

        if len(hiScores) == Database.numScores:
            lowScoreName = hiScores[-1][0]
            lowScore = hiScores[-1][1]
            curs.execute("DELETE FROM scores WHERE (name = ? AND score = ?)",
                      (lowScoreName, lowScore))
        curs.execute("INSERT INTO scores VALUES (?,?,?)", entry)
        self.score_db.commit()
        curs.close()
