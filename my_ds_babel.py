import csv
import sqlite3
import pandas as pd

class Converter:

    def sql_to_csv(self, connection):

        # creating cursor
        cur = connection.cursor()

        # reading table name
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table_name = cur.fetchone()[0]

        # create table
        query='select * from ' + table_name
        data = pd.read_sql(query,connection)
        data.to_csv('all_fault_lines.csv')

        connection.close()

    # ---------------------------------------------------

    def csv_to_sql(self, csv_table_name):
        con = sqlite3.connect('list_volcanos.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE list_volcanos (a,b,c,d,e,f)')
        # cur.execute ('CREATE TABLE list_volcanos (Volcano Name,Country,Type,Latitude (dd),Longitude (dd),Elevation (m))')

        with open(csv_table_name,'r') as fin:
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin) # comma is default delimiter
            to_db = [(i['Volcano Name'], i['Country'], i['Type'], i['Latitude (dd)'], i['Longitude (dd)'], i['Elevation (m)']) for i in dr]

        cur.executemany("INSERT INTO list_volcanos (a,b,c,d,e,f) VALUES (?, ?, ?, ?, ?, ?);", to_db)
        # ---- .db file check ----
        # for row in cur.execute("SELECT * FROM list_volcanos"):
        #     print (row)
        con.commit()
        con.close()


table = Converter()

# creating a SQL connection to our SQLite database
connection = sqlite3.connect('all_fault_line.db')
table.sql_to_csv(connection)

table.csv_to_sql('list_volcano.csv')
