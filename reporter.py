from flask import Flask
from flask import render_template
import extract_site

app = Flask(__name__)


@app.route('/')
def result():
    data_set = extract_site.get_data_comparison_site()
    return render_template("report.html",data_set=data_set)

if __name__ == '__main__':
    app.run()
