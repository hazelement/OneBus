from __future__ import print_function
import datetime
import sys
import traceback

from app import app
from flask import render_template, request, jsonify

from Database import backend


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api_port():
    post_data = request.get_json()
    print(post_data, file=sys.stderr)

    home = post_data['home_gps']
    home_lat = home['lat']  # it has gps data
    home_lng = home['lng']

    txtSearch = post_data['search_text']
    current_time = datetime.datetime.now()
    ctime = str(current_time.year) + "-" + str(current_time.month) + "-" + str(current_time.day) + "|" + str(current_time.hour) + ":" +str(current_time.minute) + ":" + str(current_time.second)

    try:
        result = backend.get_destinations(home_lat, home_lng, txtSearch, ctime) # yyyy-mm-dd|hh:mm:ss
    except Exception, e:
        exc_info = sys.exc_info()
        

        traceback.print_exception(*exc_info)
        print(str(e))
        result={}
        result['results']={}

        
    return jsonify(**result)
