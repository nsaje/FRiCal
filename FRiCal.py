from flask import Flask, request, make_response, render_template
import urllib2
import convert

app = Flask(__name__)

BASE_URL = 'http://urnik.fri.uni-lj.si'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/allocations')
def do_convert():
    url = BASE_URL + request.full_path
    f = urllib2.urlopen(url)
    ical = convert.convert(f.read())

    resp = make_response(ical)
    resp.headers['Content-type'] = 'text/calendar; charset=utf-8'
    resp.headers['Content-Disposition'] = 'inline; filename=calendar.ics'

    return resp

if __name__ == '__main__':
    app.run()
