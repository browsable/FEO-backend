from flask import Flask, render_template
import h2checker
app = Flask(__name__)

@app.route('/')
def main():
    url = 'h2perf.com'
    # h2 support checking
    support = h2checker.checkH2(url)
    support += h2checker.checkH2S(url)
    return "<h1>%support</h1>"

@app.route('/feo/')
@app.route('/feo/<name>')
def feo(name=None):
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)