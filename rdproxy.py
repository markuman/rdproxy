from bottle import route, run, hook, request, abort, redirect, response
import requests
import redis
import os
import logging

# init stuff
logging.basicConfig()
logger = logging.getLogger('rdproxy')

REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
REDIS_DB = os.environ.get('REDIS_DB') or 0
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

# init database connection
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, charset="utf-8", decode_responses=True)

try:
    r.ping()
    RDPROXY_PORT = r.get('RDPROXY:PORT') or 8000
    RDPROXY_HOST = r.get('RDPROXY:HOST') or 'localhost'
    RDPROXY_DEBUG = r.get('RDPROXY:DEBUG') or False
except:
    logger.error("cannot connect to redis")
    exit(0)


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
        response.headers['Content-Type'] = ret.headers["Content-Type"]
        return ret.content

    else:
        abort(404, "Route not found")

if __name__ == '__main__':
    run(host=RDPROXY_HOST, port=RDPROXY_PORT, debug=RDPROXY_DEBUG)