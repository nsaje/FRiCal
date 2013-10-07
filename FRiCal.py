from flask import Flask, request, make_response, render_template
import urllib2
import convert
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

BASE_URL = 'http://urnik.fri.uni-lj.si'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/allocations', defaults={'path': ''})
@app.route('/<path:path>/allocations')
def do_convert(path):
    url = BASE_URL + request.full_path
    logging.debug(url)

    f = urllib2.urlopen(url)
    ical = convert.convert(f.read())

    resp = make_response(ical)
    resp.headers['Content-type'] = 'text/calendar; charset=utf-8'
    resp.headers['Content-Disposition'] = 'inline; filename=calendar.ics'

    return resp

if __name__ == '__main__':
    app.run()
