import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='feo',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `url_list` (`url`, `count`) VALUES (%s, %s)"
        cursor.execute(sql, ('http://www.naver.com', 1))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `url`, `count` FROM `url_list`" #WHERE `num`=%s"
        #cursor.execute(sql, ('webmaster@python.org',))
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()