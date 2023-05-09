"""
@auhtor=MarioFloresMarcial
"""

import requests
import logging
import utility
import db_utility
import os 
from PIL import Image
from urllib.request import urlopen
from datetime import datetime, timedelta


#initialization
logging.basicConfig(filename='apod_logging.log', level=logging.WARNING, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M %p')
logging.warning("Statred")
nasa_apod_api_key = os.environ.get('nasa_apod_api_key', 'DEMO_KEY')
baseURL = "https://api.nasa.gov/planetary/apod?api_key=" + nasa_apod_api_key
optionsURL = ""


#pulls data from NASA APOD API and adds instrument, image size, and keywords to each entry
#saves new extended APOD to a database
def update_apod_db(URL):
    #get data from NASA APOD API
    response = requests.get(URL).json()
    logging.warning('Calling NASA APOD API....')

    #list of data to be inserted to SQL tables
    apod_data = []
    apod_instrument_data = []
    apod_keywords_data = []

    print("Starting...")
    #loop through each apod
    for apod in response:
        #pull data from json
        try:
            #API provides copyright
            apod_copyright = apod['copyright']
        except KeyError:
            #API does not provide copyright
            apod_copyright = "none"
        try:
            #API provides hdurl
            apod_hd_img = apod['hdurl']
        except KeyError:
            try:
                #API does not provide hdurl
                apod_hd_img = apod["url"]
            except KeyError:
                #API does not provide img url
                apod_hd_img = "None"
                apod_img = "None"
        apod_date = apod["date"]
        apod_expl = apod["explanation"]
        #test for empty explanation
        if len(apod_expl) == 0:
            apod_expl = "Explanation not found"
        apod_media_type = apod["media_type"]
        apod_version = apod["service_version"]
        apod_title = apod["title"]
        try:
            apod_img = apod["url"]
        except KeyError:
            apod_img = "None"
        apod_instrument = []
        
        #process data
        #determine image file format
        if apod_media_type == "image":
            filetype = apod_hd_img.split(".")
            #save type of image file format
            apod_img_type = filetype[-1]
            #determine image size
            try:
                #hd image
                im = Image.open(urlopen(apod_hd_img))
                apod_img_width = str(im.width)
                apod_img_height = str(im.height)
            except:
                try:
                    #try small image
                    apod_hd_img = apod_img
                    im = Image.open(urlopen(apod_hd_img))
                    apod_img_width = str(im.width)
                    apod_img_height = str(im.height)
                except:
                    #default to 0, 0
                    apod_img_width = 0
                    apod_img_height = 0 
        else:
            apod_img_type = apod_media_type
            apod_img_width = 0
            apod_img_height = 0
        #generate keywords
        if apod_expl == "Explanation not found":
            apod_keywords = ["None", "None", "None", "None"]
        else:
            apod_keywords = utility.gen_keywords(apod_expl)

        #determine instrument used
        apod_instrument = utility.get_inst(apod_title, apod_copyright, apod_hd_img, apod_keywords, apod_media_type)
        #generate keywords_id
        apod_keywords_id = str(apod_date).replace('-','')

        #add to tuple array for apod table
        apod_data.append((apod_date, str(apod_title), str(apod_copyright), str(apod_hd_img), str(apod_img), str(apod_media_type), str(apod_img_type), apod_img_width, apod_img_height, str(apod_expl), apod_keywords_id, str(apod_version)))
        #add to tuple for keywords table
        apod_keywords_data.append((apod_keywords_id, str(apod_keywords[0]), str(apod_keywords[1]), str(apod_keywords[2]), str(apod_keywords[3])))
        #add to tuple for apod_instrument table
        for i in apod_instrument:
            apod_instrument_data.append((apod_date, str(i)))
            
    #save extended APOD data to database
    logging.warning('Updating databse')
    db_utility.insert_keywords(apod_keywords_data)
    db_utility.insert_apod(apod_data)
    db_utility.insert_apod_instrument(apod_instrument_data)
    db_utility.close_connection()

#check if apod db is updated to today
today = datetime.today().date()
latest_record = db_utility.get_latest_entry_date()[0]
if latest_record != "None":
    #update needed
    if latest_record < today:
        #add one day to latest record
        latest_record = latest_record + timedelta(days=1)
        #convert to string
        latest_record = latest_record.strftime('%Y-%m-%d')
        #logging.warning('Latest date is ', latest_record)
        optionsURL = "&start_date=" + latest_record
        URL = baseURL + optionsURL
        update_apod_db(URL)
    else:
        print("Database is up to date")
        logging.warning('Database is up to date')
else:
    logging.warning('Error getting latest date')











