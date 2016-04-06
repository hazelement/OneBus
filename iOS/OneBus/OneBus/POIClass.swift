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
        return self.address
    }
    
    let destName: String
    let address: String
    let image_url: String
    let yelp_url: String
    let review_count: Int
    let ratings_img_url: String

    let coordinate: CLLocationCoordinate2D
    
    init(destName: String, address: String, image_url: String, yelp_url: String, review_count: Int, ratings_img_url: String, coordinate: CLLocationCoordinate2D) {
        
        self.destName = destName
        self.address = address
        self.image_url = image_url
        self.yelp_url = yelp_url
        self.review_count = review_count
        self.ratings_img_url = ratings_img_url
        
        self.coordinate = coordinate
        
        super.init()
    }
    

}