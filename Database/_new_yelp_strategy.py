

class Point():
	def __init__(self, lat, lng):
		self.lat = lat
		self.lng = lng

class Rectangle():
    def __init__(self, p1, p2):
        self.p_nw = self._upate_p_nw(p1, p2)
        self.p_se = self._upate_p_se(p1, p2)

    def _update_p_nw(self, p1, p2):
        return Point( min(p1.lat, p2.lat), max(p1.lng, p2.lng) )

    def _upate_p_se(self, p1, p2):
        return Point( max(p1.lat, p2.lat), min(p1.lng, p2.lng) )

    def update_rec(self, p):
        self.p_nw = self._upate_p_sw(self.p_nw, p)
        self.p_se = self._upate_p_se(self.p_se, p)

    def calc_area(self):
        lat_side = abs(self.p_nw.lat - self.p_se.lat)
        lng_side = abs(self.p_nw.lng - self.p_se.lng)

        return lat_side * lng_side




# make this a function and thread out for each trip, use a thread pool maybe

stops_array_of_a_trip = []
area_threashold = 0.001

for i in range(0, len(stops_array_of_a_trip)):
    rec = Rectangle(stops_array_of_a_trip[i], stops_array_of_a_trip[i+1])
    for j in range(i+2, len(stops_array_of_a_trip)):
        if(rec.calc_area() > 0.001): # if rectange from stop i to stop j is greater than an area, do yelp search on this area
            i=j+1  # set i to start new search from j + 1
            get_yelp(rec)  # threadout to get yelp result
        else:
            rec.update_rec(stops_array_of_a_trip[j])    # update rectange area from stop i to stop j


# thread join here


# note this new strategy will still need to use the cross calc to find istance bwetween stops and target locations,
            # this is the only method to link targets with there stops thus generate bus route data



# another idea:
# from all the stop locations, generate arrays of rectangles based on size criteria and use these rectangles
# to seach on yelp


# method 1 to generate rectangle arrays:
# find nw corner and ne corner of the stops and create a huge rectangle to enclose all stops
# slice the big rectanges into small rectangesl and tag ones with stop inside then, these tag rectanges will then
# be used to do yelp search

# method 2:
# search on online solutions, there might be something similar, create mesh gride from lat lng points etc
# numpy or matplot etc

# method 3:
# this might be the slowest one and not necessary will work
#  search from on stop to another and take thsese stops once a rectangle is formed