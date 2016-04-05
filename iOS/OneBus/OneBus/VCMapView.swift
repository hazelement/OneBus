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
    
//    func createDetailView(address: String, review_count: Int, raing_img_url: String, yelp_url: String) -> UIView{
//    func createDetailView() -> UIView{
//        var myview: UIView = UIView()
//        myview.loadFromNibNamed("ViewPOI.xib")  // looks like this file is not loaded properly
//        
//        
//        return myview
//        
//    }
    
    
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
                
                let poi = annotation as POI
                
//                let detailView = UIWebView()
//                
                var htmlString: String = ""
//                htmlString = htmlString + "<b><font size = \"3\">" + poi.title! + "</font></b><br>"
                htmlString = htmlString + "<img src=\"" + poi.ratings_img_url + "\"><br>"
                htmlString = htmlString + "Number of Reviews: " + String(poi.review_count) + "<br>"
                htmlString = htmlString + poi.address
                htmlString = htmlString + "<br><a href=\"" + poi.yelp_url + "\" target=\"_blank\">" + "<img src=\"yelp_review_btn_light.png\"></a>" // todo this yelp image is not working
                
                print(htmlString)
                

                
//                detailView.loadHTMLString(htmlString, baseURL: nil)
//                detailView.frame = CGRectMake(0, 0, 200, 200)
//                
//                let widthConstraint = NSLayoutConstraint(item: detailView, attribute: .Width, relatedBy: .Equal, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 200)
//                detailView.addConstraint(widthConstraint)
//
//                let heightConstraint = NSLayoutConstraint(item: detailView, attribute: .Height, relatedBy: .Equal, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 200)
//                detailView.addConstraint(heightConstraint)
//
//                detailView.scrollView.scrollEnabled = false
//                
//                
//                view.detailCalloutAccessoryView = detailView
                
                
                let myview = POIView.instanceFromNib(poi.address, no_review: poi.review_count, yelp_url: poi.yelp_url)
                
                let widthConstraint = NSLayoutConstraint(item: myview, attribute: .Width, relatedBy: .Equal, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 280)
                myview.addConstraint(widthConstraint)
                
                let heightConstraint = NSLayoutConstraint(item: myview, attribute: .Height, relatedBy: .Equal, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 90)
                myview.addConstraint(heightConstraint)
                
                view.detailCalloutAccessoryView = myview
                
                view.canShowCallout = true
                
            }
        
            
            return view
        }
        return nil
    }
}