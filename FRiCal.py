from flask import Flask, request
import urllib
import urllib2
import convert

app = Flask(__name__)

BASE_URL = 'http://urnik.fri.uni-lj.si/allocations'

@app.route('/')
def hello_world():
    return "hello!"

@app.route('/allocations')
def do_convert():
    url = '%s?%s' % (BASE_URL, urllib.urlencode(request.args.to_dict()))
    f = urllib2.urlopen(url)
    ical = convert.convert(f.read())
    return ical


if __name__ == '__main__':
    app.run()
