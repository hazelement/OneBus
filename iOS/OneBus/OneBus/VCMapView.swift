//
//  VCMapView.swift
//  OneBus
//
//  Created by Harry Zheng on 2016-03-26.
//  Copyright © 2016 Harry Zheng. All rights reserved.
//

import Foundation
import MapKit

extension ViewController {
    
    // 1
    func mapView(mapView: MKMapView!, viewForAnnotation annotation: MKAnnotation!) -> MKAnnotationView! {
        
        if let annotation = annotation as? POI {
            let identifier = "pin"
            var view: MKPinAnnotationView
            if let dequeuedView = mapView.dequeueReusableAnnotationViewWithIdentifier(identifier)
                as? MKPinAnnotationView { // 2
                    dequeuedView.annotation = annotation
                    view = dequeuedView
            } else {
                // 3
                view = MKPinAnnotationView(annotation: annotation, reuseIdentifier: identifier)
                view.canShowCallout = true
                view.calloutOffset = CGPoint(x: -5, y: 5)
                view.rightCalloutAccessoryView = UIButton(type: UIButtonType.DetailDisclosure) as UIView
            }
            
            let myView = UIWebView()
            let poi = annotation as POI
            
            var htmlString: String = "<b><font size = \"3\">"
            htmlString = htmlString + poi.title! + "</font></b><br>"
            htmlString = htmlString + "<img src=\"" + poi.ratings_img_url + "\"><br>"
            htmlString = htmlString + "Number of Reviews: " + String(poi.review_count) + "<br>"
            htmlString = htmlString + poi.address
            htmlString = htmlString + "<br><a href=\"" + poi.yelp_url + "\" target=\"_blank\">" + "<img src=\"yelp_rewview_btn_light.png\"></a>"
            
            print(htmlString)
                
            myView.loadHTMLString(htmlString, baseURL: nil)
//
//
//            let poi = annotation as POI
////            view.image = UIImage(named:poi.ratings_img_url)
//            view.detailCalloutAccessoryView = UIImage(named: poi.ratings_img_url)
            view.detailCalloutAccessoryView = myView as UIView
            
            return view
        }
        return nil
    }
}