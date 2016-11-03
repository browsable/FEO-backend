from flask import Flask, render_template, request, jsonify, current_app, redirect, url_for
import h2checker, scraper
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
    url = request.args.get('url')

    if (url == None or ""):
        return render_template('index.html')
    else:
        h2scheck = h2checker.checkH2S(url)
        if(h2checker.checkH2(url) == 2):
            return jsonify(url=url, notice='Failed to open URL')
        else:
            try:
                try:
                    split = str(url).split('.')
                    print(split[0])
                    if (len(split) == 1):
                        sitename = split[0]
                    elif (len(split) == 2):
                        sitename = split[0]
                    else:
                        sitename = split[1]
                except Exception:
                    sitename = split[1]
                    print("url error: " + url)
                print(sitename)
                with connection.cursor() as cursor:
                    sql = "INSERT INTO url_list (sitename) VALUES (%s) ON DUPLICATE KEY UPDATE cnt=cnt+1"
                    cursor.execute(sql,sitename)

            finally:
                connection.commit()
                #connection.close()

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
