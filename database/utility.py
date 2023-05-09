"""
Utilities to generate instrument and keywords for APOD entries
@author=MarioFloresMarcial
"""


#dictionary of instruments and their IDs
instruments = {
        'a11': 1001, 
        'a12': 1002, 
        'a13': 1003, 
        'a15': 1005, 
        'a14': 1004,
        'a16': 1006,
        'a17': 1007,
        'apollo': 1008,
        'cassini': 1009, 
        'chandra': 1010, 
        'cobe': 1011, 
        'csx': 1010, 
        'curiosity': 1012, 
        'cxo': 1010, 
        'dart': 1013, 
        'eht': 1014, 
        'fermi': 1015, 
        'gal': 1016, 
        'galileo': 1016, 
        'goes': 1017, 
        'hayabusa': 1018, 
        'hayabusa2': 1019, 
        'herschel': 1020, 
        'hst': 1021, 
        'hubble': 1021, 
        'insight': 1022, 
        'iss': 1023, 
        'juno': 1024, 
        'jwst': 1025, 
        'kepler': 1026, 
        'landsat': 1027, 
        'lro': 1028, 
        'm10': 1029, 
        'mar10': 1029, 
        'mariner': 1030, 
        'marsexpress': 1031, 
        'marspath': 1039, 
        'maven': 1032, 
        'messenger': 1033, 
        'newhorizons': 1034, 
        'nicer': 1035, 
        'nustar': 1036, 
        'odyssey': 1037, 
        'opportunity': 1038, 
        'pathfinder': 1039, 
        'pf': 1039, 
        'perseverance': 1040, 
        'pheonix': 1041, 
        'pioneer': 1042, 
        'planck': 1043, 
        'rosat': 1044, 
        'rosetta': 1045, 
        'sdo': 1046, 
        'skylab': 1047, 
        'soho': 1048, 
        'spirit': 1049, 
        'spitzer': 1050, 
        'station': 1023, 
        'stereo': 1051, 
        'swift': 1052, 
        'vik1': 1053, 
        'vik2': 1054, 
        'viking1': 1053, 
        'viking2': 1054,
        'viking': 1058, 
        'vg1': 1055, 
        'vg2': 1056, 
        'vgr': 1059, 
        'webb': 1025, 
        'wmap': 1057,
        }
#punctuation that will be removed from text
char_remove = [',', '.', '!', '?', ')', '(', "'s", '|', '/']
#words that will be removed from description
stopWords = ['-','--', '=', 'a', 'above', 'across', 'about', 'allow', 'allowed', 'an', 'almost', 'also', 'and', 'are', 'as', 'at', 'be', 'because', 'between', 'but', 'by', 'can', 'closest', 'distinctive', 'few', 'first', 'for', 'from', 'has', 'have', 'he', 'his', 'how', 'in', 'inset', 'image', 'images', 'is', 'it', 'its', 'just', 'left', 'looked', 'of', 'on', 'near', 'north', 'now', 'not', 'only', 'our', 'region', 'right', 'shining', 'shows', 'should', 'so', 'some', 'south', 'than', 'that', 'the', 'this', 'through', 'to', 'two', 'was', 'were', 'when', 'where', 'why', 'would', 'will', 'with', 'you', "you've"]



#attemps to find the instrument used for the image, returns "none" if no match found
def get_inst(title, credit, image_url, keywords, media):
    #holds list of instruments 
    inst_list = []
    #search for instrument in credit
    if credit != "none":
        #remove punctuation
        for char in char_remove:
            credit = credit.replace(char, '')
        #make lowercase
        credit = credit.lower() 
        #split into words
        credit_words = credit.split()
        #check if each word is in instrument list
        for word in credit_words:
            if word in instruments:
                #dont allow duplicates
                if instruments[word] not in inst_list:
                    inst_list.append(instruments[word])
        if len(inst_list) != 0:
            return inst_list

    #search for instrument in url
    #skip if media not image
    if media == 'image':
        image_url = image_url.lower()
        #get filename and extension
        image_url = image_url.split("/")
        filename = image_url.pop()
        #remove file extension
        filename = (filename.split("."))[0]
        #split string into terms
        if '_' in filename:
            terms = filename.split("_")
        else:
            terms = filename.split("-")
        #check url terms against instrument list
        for term in terms:
            if term in instruments:
                #check for duplicates
                if instruments[term] not in inst_list:
                    inst_list.append(instruments[term])
        if len(inst_list) != 0:
            return inst_list

    #check keywords for instrument
    for kw in keywords:
        if kw in instruments:
            #check for duplicates
            if instruments[kw] not in inst_list:
                inst_list.append(instruments[kw])
    if len(inst_list) != 0:
        return inst_list

    #check title for instrument
    #make lowercase
    title = title.lower() 
    #split into words
    title_words = title.split()
    #search for instrument in words
    for t in title_words:
        if t in instruments:
            if instruments[t] not in inst_list:
                inst_list.append(instruments[t])
    if len(inst_list) != 0:
        return inst_list
    else:
        #unknown instrument
        inst_list.append(1000)
        return inst_list
    
    #takes a description string and returns a list of top four keywords
def gen_keywords(desc_string):
    #description with no stop words
    string_no_stop = []
    #dictionary with wordcount as key
    wordCount = {}
    #list with top four keywords
    keywords = []

    #sanitize string
    #remove punctuation
    for char in char_remove:
        desc_string = desc_string.replace(char, '')
    #make lowercase
    desc_string = desc_string.lower()
     #split string into words
    words = desc_string.split()
    #remove stopwords
    for word in words:
        if word not in stopWords:
            string_no_stop.append(word)

    #calculate keywords
    #calculate word frequency
    for s in string_no_stop:
        if s not in wordCount:
            wordCount[s] = string_no_stop.count(s)
    #sort by frequency
    sortedDict = sorted(wordCount.items(), key = lambda item: item[1])
    #convert to dict
    dict(sortedDict)
        
    #add top four keywords
    i = 0
    while i < 4:
        try:
            keywords.append(sortedDict.pop()[0])
        except:
            keywords.append("None")
        i+=1
    return keywords
 

    
    
