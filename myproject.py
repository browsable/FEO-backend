from flask import Flask,render_template,request,jsonify,current_app,redirect,url_for
import h2checker,scraper
from functools import wraps
app = Flask(__name__)

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
    #scraper.scraper(url)
    return render_template('scraping.html',url=url)


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