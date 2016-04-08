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
    
    func instanceFromNib(address: String, no_review: Int, yelp_url: String, ratings_img_url: String) -> UIView {
        let myview = UINib(nibName: "POIView", bundle: nil).instantiateWithOwner(nil, options: nil)[0] as! UIView
        let address_label = myview.viewWithTag(2) as! UILabel
        let review_count = myview.viewWithTag(1) as! UILabel
        let yelp_button = myview.viewWithTag(4) as! YelpUIButton
        let rating_image = myview.viewWithTag(3) as! UIImageView
        
        rating_image.downloadedFrom(link: ratings_img_url, contentMode: UIViewContentMode.ScaleAspectFill)
        
        yelp_button.urlString = yelp_url
        yelp_button.addTarget(self, action: #selector(ViewController.yelpButtonClicked(_:)), forControlEvents: UIControlEvents.TouchUpInside)
        
        address_label.text = address
        review_count.text = String(no_review)
        
        return myview
    }
    
    func yelpButtonClicked(sender:YelpUIButton){
        // open button url in safari
        UIApplication.sharedApplication().openURL(NSURL(string: sender.urlString!)!)
    }
    
    func mapView(mapView: MKMapView, didAddAnnotationViews views: [MKAnnotationView]) {
        for myview in views {
            let endFrame: CGRect = myview.frame
            myview.frame = CGRectOffset(endFrame, 0, -500)
            
//            UIView.animateWithDuration(0.5, delay: 0.5, options: UIViewAnimationOptions.TransitionNone, animations: { () -> Void in myview.frame = endFrame }, completion: { (finished: Bool) in
//            })
            UIView.animateWithDuration(0.5, animations: { () -> Void in myview.frame = endFrame })
            
        }
    }
    

    
    
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
                
                let myview = instanceFromNib(poi.address,
                                            no_review: poi.review_count,
                                            yelp_url: poi.yelp_url,
                                            ratings_img_url: poi.ratings_img_url)
                
                let widthConstraint = NSLayoutConstraint(item: myview, attribute: .Width, relatedBy: .Equal, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 250)
                myview.addConstraint(widthConstraint)
                
                let heightConstraint = NSLayoutConstraint(item: myview, attribute: .Height, relatedBy: .Equal, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 100)
                myview.addConstraint(heightConstraint)
                
                view.detailCalloutAccessoryView = myview
                
                view.canShowCallout = true
                
            }
        
            
            return view
        }
        return nil
    }
}