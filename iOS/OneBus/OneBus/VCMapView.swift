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
    
    
    
    func mapView(mapView: MKMapView, didAddAnnotationViews views: [MKAnnotationView]) {
        for myview in views {
            let endFrame: CGRect = myview.frame
            myview.frame = CGRectOffset(endFrame, 0, -500)
            
//            UIView.animateWithDuration(0.5, delay: 0.5, options: UIViewAnimationOptions.TransitionNone, animations: { () -> Void in myview.frame = endFrame }, completion: { (finished: Bool) in
//            })
            UIView.animateWithDuration(0.5, animations: { () -> Void in myview.frame = endFrame })
            
        }
    }
    
    
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
                
                let detailView = UIWebView()
                let poi = annotation as POI
                
                var htmlString: String = "<html><body><p>"
                htmlString = htmlString + "<b><font size = \"3\">" + poi.title! + "</font></b><br>"
//                htmlString = htmlString + "<img src=\"" + poi.ratings_img_url + "\"><br>"
                htmlString = htmlString + "Number of Reviews: " + String(poi.review_count) + "<br>"
                htmlString = htmlString + poi.address
                //            htmlString = htmlString + "<br><a href=\"" + poi.yelp_url + "\" target=\"_blank\">" + "<img src=\"yelp_rewview_btn_light.png\"></a>"
                
                htmlString = htmlString + "</p></body></html>"
                
                print(htmlString)
                
                detailView.loadHTMLString(htmlString, baseURL: nil)
                view.detailCalloutAccessoryView = detailView
                
//                view.translatesAutoresizingMaskIntoConstraints = true
                
                
                
                
                
//                view.rightCalloutAccessoryView = UIButton(type: UIButtonType.DetailDisclosure) as UIView
            }
        
            
            return view
        }
        return nil
    }
}