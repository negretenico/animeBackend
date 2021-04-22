import pandas as pd
import os
import mysql.connector as mysql
from mysql.connector import Error


class DataGather:
    def __init__(self):
        self.PATH = os.getcwd()+'\\Recommendation\\Data\\anime.csv'

    def showData(self):
        df = pd.read_csv(self.PATH)
        for col in df.columns:
            print(col)

    def sendToSQL(self):
        data = pd.read_csv(self.PATH)
        df = pd.DataFrame(data, columns=[
                          'Name', 'Genders', 'Score', 'Episodes', 'Producers', 'Rating', 'Duration'])
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
                cursor.execute("CREATE TABLE anime_data(Name varchar(255),Genders varchar(255),Score varchar(255),Episodes varchar(255),Producers varchar(512),Rating varchar(255),Duration varchar(255))")
                print("Table is created....")
                # loop through the data frame
                for i, row in df.iterrows():
                    # here %S means string values
                    sql = "INSERT INTO anime.anime_data VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    print(tuple(row))
                    print(sql)
                    cursor.execute(sql, tuple(row))
                    print("Record inserted")
                    # the connection is not auto committed by default, so we must commit to save our changes
                    conn.commit()


        except Error as e:
            print("Error while connecting to MySQL", e)
dg = DataGather()
dg.sendToSQL()
 