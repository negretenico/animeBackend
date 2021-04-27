import pandas as pd
import numpy as np
import os
import mysql.connector as mysql
from mysql.connector import Error
from Search.searcher import Search

class DataGather:
    def __init__(self):
        self.PATH = os.getcwd()+'\\Data'

    def showData(self):
        df = pd.read_csv(self.PATH)
        for col in df.columns:
            print(col)
    def getImageUrls(self):
        search= Search()
        df =pd.read_csv(self.PATH)
        animeNames = df['Name']
        listOfImageUrls = []
        for name in animeNames:
            url = search.do_search(keywords = name+" anime",limits=1,download= False)
            if(url):
                listOfImageUrls.append(url)
            else:
                listOfImageUrls.append('')
        self.addNewColumn("image_url",listOfImageUrls)
    def addNewColumn(self,columnName,columnToAdd):
        df =pd.read_csv(self.PATH)
        df[columnName] = columnToAdd
        df.to_csv(self.PATH, index=False)


    def combine(self):
        crunchy = pd.read_csv(self.PATH+'\\crunchyroll.csv')
        anime = pd.read_csv(self.PATH+'\\anime.csv')
        anime2 = pd.read_csv(self.PATH+'\\anime2.csv')
        merged = pd.merge(crunchy,anime, on = 'anime')
        merged = pd.merge(merged,anime2,on = 'anime')
        merged.to_csv(self.PATH+'\\merged.csv', index=False)

    def sendToSQL(self):
        data = pd.read_csv(self.PATH+'\\merged.csv')
        df = pd.DataFrame(data, columns=[
                          'anime', 'Genre', 'rate', 'anime_url', 'anime_img', 'episodes', 'Duration','Producers','Studios','description'])
        df.fillna('', inplace=True)
        print(df['description'].isna().sum())

        try:
            conn = mysql.connect(host='localhost', database='anime',
                        user='root', password='League123!')

            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                cursor.execute('DROP TABLE IF EXISTS anime_data;')
                print('Creating table....')
                # in the below line please pass the create table statement which you want #to create
                cursor.execute("CREATE TABLE anime_data(Name varchar(255),Genre varchar(255),Rating Double(10,2) ,CrunchyRollUrl varchar(255),ImageUrl varchar(512),Episodes INT ,Duration varchar(255),Producers varchar(255), Studio varchar(255), Description varchar(1024))")
                print("Table is created....")
                # loop through the data frame
                for i, row in df.iterrows():
                    # here %S means string values
                    sql = "INSERT INTO anime.anime_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql, tuple(row))
                    print("Record inserted")
                    # the connection is not auto committed by default, so we must commit to save our changes
                    conn.commit()


        except Error as e:
            print("Error while connecting to MySQL", e)
dg = DataGather()
dg.combine()
dg.sendToSQL()
 