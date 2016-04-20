//
//  POI.swift
//  OneBus
//
//  Created by Harry Zheng on 2016-03-26.
//  Copyright © 2016 Harry Zheng. All rights reserved.
//

import Foundation
import MapKit

class POI: NSObject, MKAnnotation {
    var title: String? {
        return self.destName
    }
    var subtitle: String? {
        return "Bus no.: " + self.route_id
//        return self.address
    }
    
    let index: Int
    
    let destName: String
    let address: String
    let image_url: String
    let yelp_url: String
    let review_count: Int
    let ratings_img_url: String
    
    let start_stop: String
    let start_stop_time: String
    let start_stop_name: String
    
    let end_stop: String
    let end_stop_time: String
    let end_stop_name: String
    
    let trip_id: String
    let trip_headsign: String
    let route_id: String
    var bus_shape: String

    let coordinate: CLLocationCoordinate2D
    let city_code: String
    
    
    
    init(index: Int,
         destName: String,
         address: String,
         image_url: String,
         yelp_url: String,
         review_count: Int,
         ratings_img_url: String,
         
         start_stop: Int,
         start_stop_time: Int,
         start_stop_name: String,
         
         end_stop: Int,
         end_stop_time: Int,
         end_stop_name: String,
         
         trip_id: Int,
         trip_headsign: String,
         route_id: Int,
         
         coordinate: CLLocationCoordinate2D,
         city_code: String) {
        
        self.index = index
        
        self.destName = destName
        self.address = address
        self.image_url = image_url
        self.yelp_url = yelp_url
        self.review_count = review_count
        self.ratings_img_url = ratings_img_url
        
        self.start_stop = String(start_stop)
        self.start_stop_time = convert_time_int_to_string(start_stop_time)
        self.start_stop_name = start_stop_name
        
        self.end_stop = String(end_stop)
        self.end_stop_time = convert_time_int_to_string(end_stop_time)
        self.end_stop_name = end_stop_name
        
        self.trip_id = String(trip_id)
        self.trip_headsign = trip_headsign
        self.route_id = String(route_id)
        self.bus_shape = ""
        
        self.coordinate = coordinate
        self.city_code = city_code
        
        super.init()
    }
    

}