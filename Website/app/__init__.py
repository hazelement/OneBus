
from flask import Flask
# from flask_googlemaps import GoogleMaps


app = Flask(__name__)

# cache = Cache(config={'CACHE_TYPE': 'redis'})
#
# with app.app_context():
#     cache.clear()
#
#
# app.config.from_object('config')
app.config.from_object('config')

# GoogleMaps(app)


from app import views


