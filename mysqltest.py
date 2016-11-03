import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='feo',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


try:
    url = "www.naver.com"
    try:
        split = str(url).split('.')
        if(len(split)==1):
            sitename = split[0]
        elif(len(split)==2):
            sitename = split[1]
        else:
            sitename = split[1]
    except Exception:
        sitename = split[1]
        print("url error: " + url)

    with connection.cursor() as cursor:
        sql = "INSERT INTO url_list (sitename) VALUES ('"+sitename+"') ON DUPLICATE KEY UPDATE cnt=cnt+1"
        cursor.execute(sql)
        # Create a new record

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `fullurl`, `cnt` FROM `url_list`" #WHERE `num`=%s"
        #cursor.execute(sql, ('webmaster@python.org',))
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()