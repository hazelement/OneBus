from django.shortcuts import render
from django.http import HttpResponse
from GTFSDatabase import backend
import json
# Create your views here.
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import sys, traceback
import logging

# import pdb
# pdb.set_trace()

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'OneBus/index.html')

def route_port(request):
    try:
        post_data = json.loads(request.body)
        trip_id = post_data['trip_id']
        start_stop = post_data['start_stop']  # it has gps data
        end_stop = post_data['end_stop']
        city_code = post_data['city_code']

        # print(trip_id, start_stop, end_stop, lat, lng)

    except:
        result={}
        result['results']={}
        result['success']=0
        result['message']='posting data error'

        return HttpResponse(json.dumps(result), content_type="application/json")

    result={}
    result['results'] = backend.get_shape_gps(city_code, trip_id, start_stop, end_stop)
    result['success'] = 1
    result['message'] = 'success'

    return HttpResponse(json.dumps(result), content_type="application/json")


def api_port(request):
    print("here")

    try:
        post_data = json.loads(request.body)
        print(post_data)

        home = post_data['home_gps']
        home_lat = home['lat']  # it has gps data
        home_lng = home['lng']
        txtSearch = post_data['search_text']
        ctime = post_data['current_time']
        #
        # current_time = datetime.datetime.now()
        # ctime = str(current_time.year) + "-" + str(current_time.month) + "-" + str(current_time.day) + "|" + str(current_time.hour) + ":" +str(current_time.minute) + ":" + str(current_time.second)
    except Exception, e:
        print(e)
        result={}
        result['results']={}
        result['success']=0
        result['message']='posting data error'

        return HttpResponse(json.dumps(result), content_type="application/json")

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

    return HttpResponse(json.dumps(result), content_type="application/json")