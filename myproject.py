from flask import Flask, render_template, request, jsonify, current_app, Response
from flask import send_from_directory

import h2checker, scraper, namesplit, operator, pagespeed_api, snapshot,os,redirecturl
from functools import wraps
import pymysql.cursors
# import gevent
# import gevent.monkey
# from gevent.pywsgi import WSGIServer
# gevent.monkey.patch_all()
# import executebash

UPLOAD_FOLDER = '/Users/browsable/PycharmProjects/FEO-backend/web'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='1234',
                             db='feo',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# def event_stream(i):
#     yield 'data: icon%s\n\n' % i
#
# i = 2 #icon number (3~6)
# @app.route('/my_event_source')
# def sse_request():
#     return Response(event_stream(i),mimetype='text/event-stream')

@app.route('/')
def main():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM feo.url_list ORDER BY cnt DESC LIMIT 0,4"
            cursor.execute(sql)
            url_list1 = cursor.fetchall()
            sql = "SELECT * FROM feo.url_list ORDER BY cnt DESC LIMIT 5,4"
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
    sitename = namesplit.make(url)
    if not os.path.isfile("/Users/browsable/PycharmProjects/FEO-backend/web/" + sitename +'.zip'):
        scraper.scraper(fullurl)
    imgurl = 'images/'+ sitename + ".png"
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

@app.route('/web/<path:filename>', methods=['GET', 'POST'])
def getzip(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)

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
