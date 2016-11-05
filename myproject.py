from flask import Flask, render_template, request, jsonify, current_app, redirect, url_for
import h2checker, scraper, namesplit
from functools import wraps
import pymysql.cursors

app = Flask(__name__)
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
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
        h2scheck = h2checker.checkH2S(url)
        if (h2checker.checkH2(url) == 2):
            return jsonify(url=url, notice='Failed to open URL')
        else:
            try:
                sitename = namesplit.make(url)

                with connection.cursor() as cursor:
                    sql = "INSERT INTO url_list (sitename) VALUES (%s) ON DUPLICATE KEY UPDATE cnt=cnt+1"
                    cursor.execute(sql, sitename)
            finally:
                connection.commit()
                # connection.close()

            if (h2scheck == 3):
                return jsonify(url=url, notice='This domain supports HTTP/2')
            else:
                return jsonify(url=url, notice='scraping')


@app.route('/scraping')
def scraping():
    url = request.args.get('url')
    # scraper.scraper(url)
    return render_template('scraping.html', url=url)


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
