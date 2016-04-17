//
//  ApiClass.swift
//  OneBus
//
//  Created by Harry Zheng on 2016-03-25.
//  Copyright © 2016 Harry Zheng. All rights reserved.
//

import Foundation
import Alamofire


public class API_Class{
    
    private var _client: String = ""
    
    public init (){
        self._client = "https://www.yychub.com/onebus"
//        self._client = "http://162.246.156.126:8000"
//        self._client = "http://localhost:5000"
//        self._client = "http://192.168.0.10:5000"
        
    }
    
    private func fetch_url(url: String, values: [String: AnyObject], method: String, completionHandler: (NSDictionary?) -> ()){
        print(values.description)
        if method=="POST"
        {
            Alamofire.request(.POST, url, parameters:values, encoding:ParameterEncoding.JSON)
                .responseJSON{ response in
                    print(response.request)
                    completionHandler(response.result.value as? NSDictionary)
                    
            }
        }
        else if method=="GET"
        {
            debugPrint("POST method required")
        }
    }
    
    public func search_results(search_text: String, lat: String, lng: String, completionHandler: NSDictionary? -> ()){
        let api: String = "/api"
        let url: String = self._client + api
        
        let date = NSDate()
        let calendar = NSCalendar.currentCalendar()
        let components = calendar.components([.Year, .Month, .Day, .Hour, .Minute, .Second], fromDate: date)
        
        let ct = String(components.year) + "-"
                    + String(components.month) + "-"
                    + String(components.day) + "|"
                    + String(components.hour) + ":"
                    + String(components.minute) + ":"
                    + String(components.second)
        
        let values: [String: AnyObject] = ["search_text": search_text,
                                           "home_gps": ["lat": lat, "lng": lng],
                                            "current_time": ct]
        
        fetch_url(url, values: values, method: "POST", completionHandler: completionHandler)
        
    }
    
    public func get_trip_shape(trip_id: String, start_stop: String, end_stop: String, city_code: String, completionHandler: NSDictionary? -> ()){
        let api: String = "/api/route"
        let url: String = self._client + api
        
        let values: [String: AnyObject] = ["trip_id": trip_id,
                                           "start_stop": start_stop,
                                           "end_stop": end_stop,
                                           "city_code": city_code]
        
        fetch_url(url, values: values, method: "POST", completionHandler: completionHandler)
    }
    
    
    
}