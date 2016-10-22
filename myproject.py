from flask import Flask,jsonify,render_template,request,redirect,url_for
import h2checker,scraper

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/feo', methods=['POST'])
def feo():
    url = request.form['url']
    h2scheck = h2checker.checkH2S(url);

    if(h2scheck==3):
        notice = 'This domain supports HTTP/2'
        return render_template('h2check.html', url=url, notice=notice)
    elif(h2checker.checkH2(url)==2):
        notice = 'Failed to open URL'
        return render_template('h2check.html', url=url, notice=notice)
    else:
        #return redirect(url_for('scraping',url=url))
        #scraper.scrap(url)
        return 'scraping'

@app.route('/scraping')
def scraping():
    url = request.args.get('url')
    return render_template('scraping.html',url=url)

if __name__ == '__main__':
    app.run(host='0.0.0.0')