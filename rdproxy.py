from bottle import route, run, hook, request, abort, redirect
import requests
import redis
import os

# no config, just environment variables
REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
REDIS_DB = os.environ.get('REDIS_DB') or 0
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
RDPROXY_PORT = os.environ.get('RDPROXY_PORT') or 8000
RDPROXY_DEBUG = os.environ.get('RDPROXY_DEBUG') or False


r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, charset="utf-8", decode_responses=True)

# FUCK rfc3986
@hook('before_request')
def strip_path():
    path = request.environ['PATH_INFO']
    if len(path) > 1:
        if path[1:].find('/') < 0:
            redirect(request.environ['PATH_INFO'] + "/")

@route('/')
def index():
    abort(404, "No Route")

@route('/<uri>/')
@route('/<uri>/<opt:re:.+>')
def rdproxy(uri = None, opt = None):
    uri = uri or ""
    opt = opt or ""
    url = r.get(uri)

    if url:
        ret = requests.get(url + "/" + opt)
        return ret.content

    else:
        abort(404, "Route not found")

if __name__ == '__main__':
    run(host='localhost', port=RDPROXY_PORT, debug=RDPROXY_DEBUG)