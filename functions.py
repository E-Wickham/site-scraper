
def webscrape(url):
    import urllib.request
    from bs4 import BeautifulSoup
    
    r = urllib.request.Request(url, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    html = urllib.request.urlopen(r)

    soup = BeautifulSoup(html.read(), 'html.parser')
    return soup

def dbInsert(colDict):

    ###### DECLARE DICTIONARY ITEMS
    headline = colDict['headline']
    authorfname = colDict['authorfname']
    authorlname = colDict['authorlname']
    pubdate = colDict['pubdate']
    paper_id = colDict['paper_id']
    bodytext = colDict['bodytext']
    url = colDict['url']
    

    ######      BEGIN INSERT DATA INTO DATABASE     #####

    import mysql.connector
    import re

    # DB information to connect to localhost

    mydb = mysql.connector.connect(
    host="hostname",
    port="3306",
    user="username",
    password="password",
    database ="dbname"
    )

    #get everything from the columnist table

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM columnists")
    result = mycursor.fetchall()

    #check if the first and last name of the columnist matches any of the existing columnists, columnist id = 

    #give columnist id to existing columnist, attribute id to new columnist

    for x in range(0,len(result)):
        if authorfname in result[x] and authorlname in result[x]:
            entryColumnistID = x+1
            newColumnist = False
            break
            
        else: 
            entryColumnistID = len(result)+1
            newColumnist = True

    #if the name of the new columnist does not exist in the columnist table, add it to the table
    if newColumnist == True:
        print('name does not exist in record. Creating new Columnist ID:')
        sqlColumnists = "INSERT INTO columnists (first_name, last_name) VALUES (%s, %s)"
        valColumnists = (authorfname, authorlname)

        mycursor.execute(sqlColumnists, valColumnists)
        print("Adding to database: ", authorfname, authorlname)
        mydb.commit()
    else:
        print(authorfname, authorlname,"exists in record under id#: ", entryColumnistID)

    ##-- insert article --##
    
    mycursor2 = mydb.cursor()
    mycursor2.execute("SELECT headline FROM newscolumns")
    colresult = mycursor2.fetchall()

    #placeholder and specific vars

    newHeadline = headline

    import datetime
    #switch PUBLISH DATE to YYYY-mm-dd
    f = '%b %d, %Y'
    entryDateTime = datetime.datetime.strptime(pubdate, f)


    #try 2 on newscolumn insert

    for x in range(0,len(colresult)):
        if newHeadline in colresult[x]:        
            newColumn = False
            break
            
        else: 
            newColumn = True

    #if this headline does not already exist, add it to my database please
    if newColumn == True:
        print('headline does not exist in record. Creating new Column entry')
        sqlNewsColumns = "INSERT INTO newscolumns (columnist_id, paper_id, headline, body_text, url, publishdate) VALUES (%s, %s, %s, %s, %s, %s)"
        valNewsColumns = (entryColumnistID, paper_id, newHeadline, bodytext, url, entryDateTime)
        mycursor2.execute(sqlNewsColumns, valNewsColumns)
        mydb.commit()
        print('new entry', newHeadline, 'added to the database')
        
    else:
        print("headline already in database, will not add duplicate:", newHeadline)
