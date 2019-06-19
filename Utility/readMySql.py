import MySQLdb
from datetime import datetime


class readMySql:

   def __init__(self):
       lastDate=""
       try:
           db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                                user="webScreping",  # your username
                                passwd="webScreping",  # your password
                                db="webScraping")  # (Server, User, Password, Data Base)
           self.cursor = db.cursor()  # prepare a cursor object using cursor() method
           print("connection succesful")
       except MySQLdb.Error as error:
           print("Nakapke pri povezavi:", error)

   def lastArsoWarning(self):
       #read the last date that is in database
       self.cursor.execute("SELECT max(dan) FROM opozorila")
       myresult = self.cursor.fetchall()

       #get a date time variable from tuple and transorm it to a string
       sqlDate=myresult[0][0].strftime('%Y-%m-%d')

       #get a system date:
       sysDate = datetime.now().strftime('%Y-%m-%d')
       if sysDate == sqlDate:

           sql = "SELECT opoz FROM opozorila WHERE dan = %s"
           adr = (sqlDate,)

           self.cursor.execute(sql, adr)
           sqlResult = self.cursor.fetchall()
           strSqlResult=sqlResult[0][0]
           return strSqlResult
       else:
           return "No such Arrso warning for today"




