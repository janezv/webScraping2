#!/usr/bin/python3

#automtic runing in the Ubuntu 18 https://hostadvice.com/how-to/how-to-setup-a-cron-job-on-ubuntu-18-04/
# sudo nano /etc/crontab

import MySQLdb
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Utility.readMySql import readMySql
from Utility.Logs import log


#ARSO najde TEMPERATURNE PODATKE
url = 'http://www.arso.gov.si/vreme/napovedi%20in%20podatki/zrak/opozorila/'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html)

logger = log()
for div in soup.findAll("div", {"id": "opozorila"}):   #najdi vse tabele
    links=div.findAll("a")   #najdi vse tabele
    for link in links:
        msgt=link.contents[0]
        if len(msgt)>5:
            print("  ")
            print(type(msgt))
            war=str(msgt)
            print(type(war))
            print(war)
            print(len(msgt))
            print("  ")

            #check if the Arso warning for today has laready bean parsed
            warningFromMySQL = readMySql();
            strWarningFromMySQL = warningFromMySQL.lastArsoWarning()
            if not strWarningFromMySQL == "No such Arrso warning for today":
                logger.logMessage("Program ustavljen, je že poslano opozorilo")
                quit() #exit the program, because this warning for this day has already been parsed


            #pripravi mail
            msg = MIMEMultipart()
            #recipients = ['janez_vegan@yahoo.com','janez.vegan@gmail.com']
            recipients = ['janez.vegan@gmail.com']
            # recipients = ['janez_vegan@yahoo.com','janez.vegan@gmail.com']
            #msg['To'] = ", ".join(recipients)  //polje to
            msg['Subject'] = "Opozorila iz ARSO"
            msg.attach(MIMEText(war, 'plain'))
            #logiraj se in poslji mail
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("autoPython.send@gmail.com", "******gesloZakritoo*****")
            text = msg.as_string()
            server.sendmail("autoPython.send@gmail.com", recipients, text)
            #server.sendmail("autoPython.send@gmail.com", "hocevar.roman@gmail.com", msg)
            server.quit()

            logger.logMessage("Opozorila je bilo prebrano in poslano na izbrane naslove")

            #write to DB
            #connect to db
            try:
                db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                                 user="webScreping",  # your username
                                 passwd="*******",  # your password
                                 db="webScraping")  #(Server, User, Password, Data Base)
                db.set_character_set('utf8')
                cursor = db.cursor()  # prepare a cursor object using cursor() method
                cursor.execute('SET NAMES utf8;')
                cursor.execute('SET CHARACTER SET utf8;')
                cursor.execute('SET character_set_connection=utf8;')
                print ("connection succesful")
            except MySQLdb.Error as errorConnection:
                print("Nakapke pri povezavi:", errorConnection)
            try:
                cursor.execute("INSERT INTO webScraping.opozorila VALUE (CURRENT_DATE(),%s)", (war,))
                db.commit()
                print ("Vpisovano je opozorilo v DB")
            except MySQLdb.Error as error:
                db.rollback()
                print ("napaka pri vpisovanju v DB", error)
        else:
            logger.logMessage("Na ta dan ni bilo izdanega nobenega opozorila")
















