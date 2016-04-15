from __future__ import print_function
import datetime
import sys
import traceback

from app import app
from flask import render_template, request, jsonify, redirect


from Database import backend


# @app.before_request
# def before_request():
#     if request.url.startswith('http://'):
#         print("redirect to https")
#         url = request.url.replace('http://', 'https://', 1)
#         code = 301
#         return redirect(url, code=code)


@app.route('/onebus', methods=['GET', 'POST'])
def onebus_index():
    return render_template('onebus/index.html')

# todo add loading bar on html
# todo add list panel on html
# todo check this api works
@app.route('/api/route', methods=['POST'])
def route_port():
    try:
        post_data = request.get_json()
        print(post_data, file=sys.stderr)

        trip_id = post_data['trip_id']
        start_stop = post_data['start_stop']  # it has gps data
        end_stop = post_data['end_stop']
        lat = post_data['lat']
        lng = post_data['lng']

        # print(trip_id, start_stop, end_stop, lat, lng)

    except:
        result={}
        result['results']={}
        result['success']=0
        result['message']='posting data error'

        return jsonify(**result)

    result={}
    result['result'] = backend.get_shape_gps(lat, lng, trip_id, start_stop, end_stop)
    result['success'] = 1
    result['message'] = 'success'

    return jsonify(**result)


@app.route('/api', methods=['POST'])
def api_port():

    try:
        post_data = request.get_json()
        print(post_data, file=sys.stderr)

        home = post_data['home_gps']
        home_lat = home['lat']  # it has gps data
        home_lng = home['lng']
        txtSearch = post_data['search_text']
        ctime = post_data['current_time']
        #
        # current_time = datetime.datetime.now()
        # ctime = str(current_time.year) + "-" + str(current_time.month) + "-" + str(current_time.day) + "|" + str(current_time.hour) + ":" +str(current_time.minute) + ":" + str(current_time.second)
    except:
        result={}
        result['results']={}
        result['success']=0
        result['message']='posting data error'

        return jsonify(**result)

    try:
        result = backend.get_destinations(home_lat, home_lng, txtSearch, ctime) # yyyy-mm-dd|hh:mm:ss
        result['success'] = 1
        result['message'] = 'success'
    except Exception, e:
        exc_info = sys.exc_info()
        

        traceback.print_exception(*exc_info)
        print(str(e))
        result={}
        result['results']={}
        result['success']=0
        result['message']=str(exc_info)

        
    return jsonify(**result)
