from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime
import os

print("Running....")


#returns relevant info for one apod object
base_query = """
SELECT  apod.apod_date,
apod.apod_title,
apod.apod_copyright,
apod.apod_hd_img,
apod.apod_img,
apod.apod_media_type,
apod.apod_img_type,
apod.apod_img_width,
apod.apod_img_height,
apod.apod_explanation,
apod.apod_version,
keywords.word1,
keywords.word2,
keywords.word3,
keywords.word4,
instrument.instrument_name 
FROM apod
INNER JOIN keywords ON apod.keywords_id = keywords.keywords_id
INNER JOIN apod_instrument ON apod.apod_date = apod_instrument.apod_date
INNER JOIN instrument ON apod_instrument.instrument_id = instrument.instrument_id 
"""

#Get valid api key from os
apodx_api_key = os.environ['apodx_api_key']
apodx_api_key2 = os.environ['apodx_api_key2']
#initialization
app = Flask(__name__)
app.config['MYSQL_HOST'] = os.environ['db_host_ip']
app.config['MYSQL_USER'] = os.environ['db_user_name']
app.config['MYSQL_PASSWORD'] = os.environ['db_user_password']
app.config['MYSQL_DB'] = 'apod_db'
mysql = MySQL(app)

SERVICE_VERSION = 'v1'
APOD_METHOD_NAME = 'apod'
#feilds allowed to be used to call api
ALLOWED_API_FIELDS = [
    'search_term', 
    'search_title', 
    'search_expl', 
    'search_copyright', 
    'search_keywords', 
    'search_inst',
    'img_width',
    'img_height',
    'img_width2',
    'img_height2',
    'date',
    'date_recc',
    'start_date',
    'end_date',
    'media_type',
    'count',
    'api_key'
    ]

def abort(code, msg):
    response = jsonify(service_version = SERVICE_VERSION, msg = msg, code = code)
    response.status_code = code
    return response

#validate api query parameter
def validate(query):
    for key in query:
        if key not in ALLOWED_API_FIELDS:
            return False
    return True

#validate api key
def validate_api_key(key):
    if (str(key) != apodx_api_key) and (str(key) != apodx_api_key2):
        return False
    return True
        

#validate query date
def validate_date(query_date):
    today = datetime.today().date()
    #first apod date 
    begin = datetime(1995, 6, 16).date()
    #validate input
    #date outside of range
    if (query_date > today) or (query_date < begin):
        today_str = today.strftime('%b %d, %Y')
        begin_str = begin.strftime('%b %d, %Y')
        raise ValueError('Date must be between %s and %s.' % (begin_str, today_str))
    
#checks for valid search parameters, returns dict with valid search parameters
#default will search in title only
def validate_search_params(search_title, search_expl, search_copyright, search_keywords, search_inst, search_term, media_type):
    #set to false if no parameter passed
    if not search_title:
        search_title = 'false'
    if not search_expl:
        search_expl = 'false'
    if not search_copyright:
        search_copyright = 'false'
    if not search_keywords:
        search_keywords = 'false'
    if not search_inst:
        search_inst = 'false'
    #set search term to wildcard if no search term passed
    if not search_term:
        search_term = '%'
    #set media_type to all as default
    if not media_type:
        media_type = 'all'

    #convert strings to lowercase
    try:
        search_title = str(search_title).lower()
        search_expl = str(search_expl).lower()
        search_copyright = str(search_copyright).lower()
        search_keywords = str(search_keywords).lower()
        search_inst = str(search_inst).lower()
    except:
        raise ValueError("search_title, search_expl, search_copyright, search_keywords must be string")

    #check values for true or false
    if search_title == 'true':
        title_term = '%' + search_term + '%'
    elif search_title == 'false':
        title_term = ''
    else:
        raise ValueError('search_title must be true or false.')
    
    if search_expl == 'true':
        expl_term = '%' + search_term + '%'
    elif search_expl == 'false':
        expl_term = ''
    else:
        raise ValueError('search_expl must be true or false.')
    
    if search_copyright == 'true':
        copyright_term = '%' + search_term + '%'
    elif search_copyright == 'false':
        copyright_term = ''
    else:
        raise ValueError('search_copyright must be true or false.')
    
    if search_keywords == 'true':
        keywords_term = search_term
    elif search_keywords == 'false':
        keywords_term = ''
    else:
        raise ValueError('search_keywords must be true or false.')
    
    if search_inst == 'true':
        inst_term = '%' + search_term + '%'
    elif search_inst == 'false':
        inst_term = ''
    else:
        raise ValueError('search_inst must be true or false.')
    
    #if all false, set search_title to true as default
    if not (title_term + expl_term + copyright_term + keywords_term + inst_term):
         title_term = '%' + search_term + '%'
    
    #validate media type
    try:
        media_type = str(media_type).lower()
    except:
        raise ValueError('media_type must be a string')
    if media_type == 'image':
        media_term = 'image'
    elif media_type == 'video':
        media_term = 'video'
    elif media_type == 'all':
        media_term = '%'
    else:
        raise ValueError ('media_type must be image, video or all')
     
    #return valid parameters as dict
    return({"title_term": title_term, "expl_term": expl_term, "copyright_term": copyright_term, "keywords_term": keywords_term, "inst_term": inst_term, "media_type": media_type, "media_term": media_term})

#checks for and returns dict with valid image size parameters
def validate_image_size_params(img_width, img_height, img_width2, img_height2):
    #set default vlaues if no params passed
    if not img_width:
        img_width = 0
    if not img_height:
        img_height = 0
    if not img_width2:
        img_width2 = 99999
    if not img_height2:
        img_height2 = 99999

    #convert params to int
    try:
        img_width = int(img_width)
        img_height = int(img_height)
        img_width2 = int(img_width2)
        img_height2 = int(img_height2)
    except:
        raise ValueError('img_width, img_height, img_width2, img_height2 must be integers')

    #img_width and img_height must be less than img_width2 and img_height2
    if (img_width > img_width2) or (img_height > img_height2):
        raise ValueError('img_width and img_height must be less than or equal to img_width2 and img_height2')
    
    #img size must be greater than zero
    if (img_width < 0) or (img_height < 0) or (img_width2 < 0) or (img_height2 < 0):
        raise ValueError("img_width, img_height, img_width2, img_height2 must not be negative")
    #return dict of parameters
    return ({"img_width": str(img_width), "img_height": str(img_height), "img_width2": str(img_width2), "img_height2": str(img_height2)})

#accepts sql query and parameters, returns results as a dictionary
def apod_db_handler(query, params):
    try:
        conn = mysql.connect
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, params)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(e)

    
#return data for single date or recurring date
def get_entry_for_date(input_date, date_recc, key):
    print("get entry for date")
    if not validate_api_key(key):
        return abort(403, "Invalid API key.")
    #validate date reccuring
    if not date_recc:
        reccuring = 'false'
    else:
        reccuring = date_recc
    try:
        reccuring = str(reccuring).lower()
    except:
        raise ValueError('date_recc must be a string')
     #get date parameter
    if not input_date:
        #use todays date if none specified
        query_date = datetime.today().date()
    else:
        query_date = datetime.strptime(str(input_date), "%Y-%m-%d").date()
        validate_date(query_date)
    #convert date to string
    query_date_str = query_date.strftime("%Y-%m-%d")
    
    if reccuring == 'false':
        date_query = " WHERE apod.apod_date = %s ;"
        query = base_query + date_query
        #tuple to pass to apod_db_handler
        params = (query_date_str,)
        data = apod_db_handler(query, params)
    #reccuring date
    elif reccuring == 'true':
        date_query = " WHERE apod.apod_date LIKE %s ORDER BY apod.apod_date DESC;"
        query = base_query + date_query
        #remove year from date
        query_date_str = query_date_str.replace(query_date_str[0 : 4],'____', 1)
        query_date_str = '%' + query_date_str + '%'
        #tuple to pass to apod_db_handler
        params = (query_date_str,)
        data = apod_db_handler(query, params)
    else:
        raise ValueError('date_recc must be true or false')

    return jsonify(data)

#returns random date apods, amount determined by count
def get_entries_for_random_dates(count, key):
    if not validate_api_key(key):
        return abort(403, "Invalid API key.")
    if count > 365 or count <= 0:
        raise ValueError('Count must be between 1 and 365')
    
    query = base_query + " ORDER BY RAND() LIMIT %s ;"
    params = (count,)
    data = apod_db_handler(query, params)
    return jsonify(data)

#returns entry data for a range of dates, if end_date is None, defaults to todays date
def get_entry_for_date_range(start_date, end_date, key):
    if not validate_api_key(key):
        return abort(403, "Invalid API key.")
    #validate input data
    start_dt = datetime.strptime(str(start_date), "%Y-%m-%d").date()
    validate_date(start_dt)

    #get the date param
    if not end_date:
        #use todays date if not specified
        end_date = datetime.strftime(datetime.today(), '%Y-%m-%d')

    #validate input date
    end_dt = datetime.strptime(str(end_date), "%Y-%m-%d").date()
    validate_date(end_dt)

    start_ordinal = start_dt.toordinal()
    end_ordinal = end_dt.toordinal()
    
    #validate date range
    if start_ordinal > end_ordinal:
        raise ValueError('start_date cannot be after end_date')
    #get data
    #convert date to string
    start_dt = start_dt.strftime("%Y-%m-%d")
    end_dt = end_dt.strftime("%Y-%m-%d")
    query = base_query + " WHERE apod.apod_date BETWEEN %s AND %s ORDER BY apod.apod_date DESC;"
    params = (start_dt, end_dt)
    data = apod_db_handler(query, params)
    
    return jsonify(data)


#returns image search results, default: search title, any image size
def get_entry_from_search(search_term, search_title, search_expl, search_copyright, search_keywords, search_inst, img_width, img_height, img_width2, img_height2, media_type, key):
    if not validate_api_key(key):
        return abort(403, "Invalid API key.")

    search_params = validate_search_params(search_title, search_expl, search_copyright, search_keywords, search_inst, search_term, media_type)
    size_params = validate_image_size_params(img_width, img_height, img_width2, img_height2)
    #results for images only
    if search_params["media_type"] == 'image':
        search_query = " WHERE (apod.apod_media_type = 'image') AND (apod.apod_title LIKE %s OR apod.apod_explanation LIKE %s OR apod.apod_copyright LIKE %s OR keywords.word1 = %s OR keywords.word2 = %s OR keywords.word3 = %s OR keywords.word4 = %s OR instrument.instrument_name LIKE %s) AND (apod.apod_img_width BETWEEN %s AND %s) AND (apod.apod_img_height BETWEEN %s AND %s) ORDER BY apod.apod_date DESC;"
        search_query = base_query + search_query
        params = (search_params["title_term"], search_params["expl_term"], search_params["copyright_term"], search_params["keywords_term"], search_params["keywords_term"], search_params["keywords_term"], search_params["keywords_term"], search_params["inst_term"], size_params["img_width"], size_params["img_width2"], size_params["img_height"], size_params["img_height2"])
        data = apod_db_handler(search_query, params)
        return jsonify(data)
    #results for video only 
    elif search_params["media_type"] == 'video':
        search_query = " WHERE (apod.apod_media_type = 'video') AND (apod.apod_title LIKE %s OR apod.apod_explanation LIKE %s OR apod.apod_copyright LIKE %s OR keywords.word1 = %s OR keywords.word2 = %s OR keywords.word3 = %s OR keywords.word4 = %s OR instrument.instrument_name LIKE %s) ORDER BY apod.apod_date DESC;"
        search_query = base_query + search_query
        params = (search_params["title_term"], search_params["expl_term"], search_params["copyright_term"], search_params["keywords_term"], search_params["keywords_term"], search_params["keywords_term"], search_params["keywords_term"], search_params["inst_term"])
        data = apod_db_handler(search_query, params)
        return jsonify(data)
    #results for both
    else:
        search_query = " WHERE (apod.apod_title LIKE %s OR apod.apod_explanation LIKE %s OR apod.apod_copyright LIKE %s OR keywords.word1 = %s OR keywords.word2 = %s OR keywords.word3 = %s OR keywords.word4 = %s OR instrument.instrument_name LIKE %s) AND (apod.apod_img_width BETWEEN %s AND %s) AND (apod.apod_img_height BETWEEN %s AND %s) ORDER BY apod.apod_date DESC;"
        search_query = base_query + search_query
        params = (search_params["title_term"], search_params["expl_term"], search_params["copyright_term"], search_params["keywords_term"], search_params["keywords_term"], search_params["keywords_term"], search_params["keywords_term"], search_params["inst_term"], size_params["img_width"], size_params["img_width2"], size_params["img_height"], size_params["img_height2"])
        data = apod_db_handler(search_query, params)
        return jsonify(data)
    

#returns entries based on image size
def get_entry_by_image_size(img_width, img_height, img_width2, img_height2, key):
    if not validate_api_key(key):
        return abort(403, "Invalid API key.")
    search_query = " WHERE (apod.apod_img_width BETWEEN %s AND %s) AND (apod.apod_img_height BETWEEN %s AND %s) ORDER BY apod.apod_date DESC;"
    size_params = validate_image_size_params(img_width, img_height, img_width2, img_height2)
    params = (size_params["img_width"], size_params["img_width2"], size_params["img_height"], size_params["img_height2"])
    search_query = base_query + search_query
    data = apod_db_handler(search_query, params)
    return jsonify(data)


#
# Endpoints
#



@app.route('/' + SERVICE_VERSION + '/' + APOD_METHOD_NAME + '/', methods=['GET'])
def apod():
    try:
        args = request.args
        

        if not validate(args):
            return abort(400, 'Bad request: incorrect field passed.')
        # retrieve parameters from api call
        search_term = args.get('search_term')
        search_title = args.get('search_title')
        search_expl = args.get('search_expl')
        search_copyright = args.get('search_copyright')
        search_keywords = args.get('search_keywords')
        search_inst = args.get('search_inst')
        img_width = args.get('img_width')
        img_height = args.get('img_height')
        img_width2 = args.get('img_width2')
        img_height2 = args.get('img_height2')
        date = args.get('date')
        date_recc = args.get('date_recc')
        start_date = args.get('start_date')
        end_date = args.get('end_date')
        media_type = args.get('media_type')
        count = args.get('count')
        api_key = args.get('api_key')

        #invalid combination of parameters
        if not api_key:
            return abort(403, 'api_key is a required feild.')
        if search_term and (date or start_date or count):
            return abort(400, 'Bad Request: invalid field combination passed.')
        if date and count:
            return abort(400, 'Bad Request: invalid field combination passed.')
        if date and (start_date or end_date):
            return abort(400, 'Bad Request: invalid field combination passed.')
        if (img_width or img_width2 or img_height or img_height2) and (count or date or start_date):
            return abort(400, 'Bad Request: invalid field combination passed.')
        if end_date and not start_date:
            return abort(400, 'Bad request: invalid field combination passed.')

        #no arguments called in api, return todays apod
        if count:
            return get_entries_for_random_dates(int(count), api_key)
        #search term param used
        elif search_term:
            return get_entry_from_search(search_term, search_title, search_expl, search_copyright, search_keywords, search_inst, img_width, img_height, img_width2, img_height2, media_type, api_key)
        #search by image size if size parameters used
        elif img_width or img_height or img_width2 or img_height2:
            return get_entry_by_image_size(img_width, img_height, img_width2, img_height2, api_key)
        #return date single or reccuring
        elif date:
            return get_entry_for_date(date, date_recc, api_key)
        #return date range
        elif start_date:
            return get_entry_for_date_range(start_date, end_date, api_key)
        else:
            return get_entry_for_date(date, date_recc, api_key)
                    

    except ValueError as ve:
        return abort(400, str(ve))




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)

