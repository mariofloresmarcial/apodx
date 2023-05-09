"""
Utilities to interact with the apod database
@author=MarioFloresMarcial
"""

import mysql.connector
import logging
from mysql.connector import Error
import os

#get parameters from the environment
db_user = os.environ["db_user_name"]
db_password = os.environ["db_user_password"]
#db_host = os.environ["db_host_ip"]
db_host='0.0.0.0'


cnx = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database='apod_db')
cursor = cnx.cursor()

#inserts a record into the instrument table
def insert_instrument(table_data):
    sqlFormula = "INSERT INTO instrument (instrument_id, instrument_name) VALUES (%s, %s)"
    try:
        cursor.executemany(sqlFormula, table_data)
        logging.warning('Execute many successful instrument table')
        cnx.commit()
        logging.warning("commited changes instrument table")
        print("instrument table updated")
    except: 
        print("Error executing SQL for instrument table")
        logging.warning('Error with SQL execution instrument table')

#inserts a record into the connecting table apod_instrument
def insert_apod_instrument(table_data):
    sqlFormula = "INSERT INTO apod_instrument (apod_date, instrument_id) VALUES (%s, %s)"
    try:
        cursor.executemany(sqlFormula, table_data)
        logging.warning('Execute many successful apod_instrument table')
        cnx.commit()
        logging.warning('Changes committed apod_instrument table')
        print("apod_instrument table updated")
    except:
        print("Error executing SQL for apod_instrument table")
        logging.warning('Error with SQL execution apod_instrument table')
        
#inserts a record into the keywords table
def insert_keywords(table_data):
    sqlFormula = "INSERT INTO keywords (keywords_id, word1, word2, word3, word4) VALUES (%s, %s, %s, %s, %s)"
    try:
        cursor.executemany(sqlFormula, table_data)
        logging.warning('Execute many successful keywords table')
        cnx.commit()
        logging.warning('Changes committed keywords table')
        print("keywords table updated")
    except:
        print("Error executing SQL for keywords table")
        logging.warning('Error with SQL execution keywords table')

#updates a record in the keywords table
def update_keywords(table_data):
    sqlFormula = "UPDATE keywords SET word1 = %s, word2 = %s, word3 = %s, word4 = %s WHERE keywords_id = %s"
    try:
        cursor.executemany(sqlFormula, table_data)
        cnx.commit()
        logging.warning('Table keywords updated')
    except:
        print("Error updating table keywords")
        logging.warning('Error updating table keywords')
    
#inserts a record into the apod table
def insert_apod(table_data):
    sqlFormula = "INSERT INTO apod (apod_date, apod_title, apod_copyright, apod_hd_img, apod_img, apod_media_type, apod_img_type, apod_img_width, apod_img_height, apod_explanation, keywords_id, apod_version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.executemany(sqlFormula, table_data)
        logging.warning('Execute many successful apod tabel')
        cnx.commit()
        logging.warning('Changes committed to apod tabel')
        print("apod table updated")
    except:
        print("Error executing SQL for apod table")
        logging.warning('Error with SQL execution apod table')

#returns the date of the latest apod record
def get_latest_entry_date():
    try:
        cursor.execute("SELECT MAX(apod_date) from apod")
        latest_date = cursor.fetchone()
        logging.warning('Latest date: ' + str(latest_date[0]))
        print("Latest date: " + str(latest_date[0]))
        return latest_date
    except Error as e:
        print("Error getting latest date")
        print(e)
        logging.warning('Error getting latest date')
        logging.warning(e)
        return "None"

#closes db connection
def close_connection():
    try:
        cursor.close()
        cnx.close()
        print("DB connection closed")
        logging.warning('DB connection closed')
    except:
        print("Error closing DB connection")
    
