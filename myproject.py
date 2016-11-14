from flask import Flask, render_template, request, jsonify, current_app
import h2checker, scraper, namesplit, operator, pagespeed_api, snapshot,os,redirecturl
from functools import wraps
import pymysql.cursors

app = Flask(__name__)
connection = pymysql.connect(host='52.78.203.106',
                             user='root',
                             password='soma1234',
                             db='feo',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def main():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM feo.url_list ORDER BY cnt DESC LIMIT 0,4"
            cursor.execute(sql)
            url_list1 = cursor.fetchall()
            sql = "SELECT * FROM feo.url_list ORDER BY cnt DESC LIMIT 4,4"
            cursor.execute(sql)
            url_list2 = cursor.fetchall()
    finally:
        connection.commit()

    url = request.args.get('url')
    if (url == None or ""):
        return render_template('index.html', url_list1=url_list1, url_list2=url_list2)
    else:
        # h2scheck
        h2scheck = h2checker.checkH2S(url)
        if (h2checker.checkH2(url) == 2):
            return jsonify(url=url, notice='Failed to open URL')
        else:
            if (h2scheck == 3):
                return jsonify(url=url, notice='This domain supports HTTP/2')
            else: #not support http2
                try:
                    sitename = namesplit.make(url)
                    # make snapshot
                    imgname = sitename + ".png"

                    with connection.cursor() as cursor:
                        if os.path.isfile('static/images/' + imgname):
                            sql = "UPDATE `url_list` SET cnt=cnt+1 WHERE `sitename`=%s"
                            cursor.execute(sql, sitename)
                        else:
                            r = redirecturl.getURL(url)
                            fullurl = r.url
                            imgurl = snapshot.urlpageshot(fullurl, imgname)
                            sql = "INSERT INTO `url_list` (`sitename`, `imgurl`) VALUES (%s,%s)"
                            cursor.execute(sql, (sitename, imgurl))
                finally:
                    connection.commit()
                    # connection.close()
                return jsonify(url=url, notice='scraping')


@app.route('/scraping')
def scraping():
    url = request.args.get('url')
    fullurl = redirecturl.getURL(url).url
    scraper.scraper(fullurl)
    imgurl = 'images/'+ namesplit.make(url) + ".png"
    # make snapshot
    pagespeed = pagespeed_api.curl(fullurl)
    red, orange, green = [], [], []

    pagespeed[1] = sorted(pagespeed[1].items(), key=operator.itemgetter(1))  # dictionary sorting
    for (key, val) in pagespeed[1]:
        if val == 0.0:
            green.append(key)
        elif val < 10:
            orange.append(key)
        else:
            red.append(key)
    return (render_template('page2.html', url=url, pagespeed=pagespeed[0], red=red, orange=orange, green=green, imgurl=imgurl))

@app.route('scrapingend')
def scrapingend():
    return jsonify(url=url, notice='Failed to open URL')

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data) + ')'
            return current_app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)

    return decorated_function


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
