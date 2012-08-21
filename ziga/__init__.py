# pylint: disable=C0103

from flask import Flask

app = Flask(__name__)

app.config.from_pyfile('settings.py')
app.config.from_envvar('ZIGA_CONF', silent=True)
app.config.from_pyfile('settings_local.py', silent=True)


# redis
from flask.ext.redis import Redis

redis = Redis()
redis.init_app(app)


import ziga.views  # this MUST be the last line!
