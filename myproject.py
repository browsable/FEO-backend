import os

from flask import Flask,render_template,request,jsonify,current_app,redirect,url_for,flash
from flask import send_from_directory
from werkzeug.utils import secure_filename
from curlchecker import curl
import h2checker,scraper
from functools import wraps
UPLOAD_FOLDER = 'templates/web'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def main():
    url = request.args.get('url')
    if(url==None or ""):
        return render_template('index.html')
    else:
        h2scheck = h2checker.checkH2S(url)
        if(h2scheck==3):
            return jsonify(url=url, notice='This domain supports HTTP/2')
        elif (h2checker.checkH2(url) == 2):
            return jsonify(url=url, notice='Failed to open URL')
        else:
            return jsonify(url=url, notice='scraping')

@app.route('/scraping')
def scraping():
    url = request.args.get('url')
    pagespeed = curl("http://www.naver.com")
    #scraper.scraper(url)
    return render_template('scraping.html',url=url,pagespeed=pagespeed)

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