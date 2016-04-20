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
    
    func instanceFromNib(poi_index: Int) -> UIView {
        
        let myannotation = annotationsPOI[poi_index]
        
        let myview = UINib(nibName: "POIView", bundle: nil).instantiateWithOwner(nil, options: nil)[0] as! UIView
        
        let bus_no = myview.viewWithTag(1) as! UILabel
        let depart_time = myview.viewWithTag(2) as! UILabel
        let depart_loc = myview.viewWithTag(3) as! UILabel
        let arrival_time = myview.viewWithTag(4) as! UILabel
        let arrival_loc = myview.viewWithTag(5) as! UILabel
        
        bus_no.text = myannotation.route_id + " " + myannotation.trip_headsign
        depart_time.text = myannotation.start_stop_time
        depart_loc.text = myannotation.start_stop_name
        arrival_time.text = myannotation.end_stop_time
        arrival_loc.text = myannotation.end_stop_name
        
        let widthConstraint = NSLayoutConstraint(item: myview, attribute: .Width, relatedBy: .Equal, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 205)
        myview.addConstraint(widthConstraint)
        
        let heightConstraint = NSLayoutConstraint(item: myview, attribute: .Height, relatedBy: .Equal, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 55)
        myview.addConstraint(heightConstraint)
        
        return myview
    }
    
    func instanceFromUIWebView(poi_index: Int) -> UIView {
        
        let myannotation = annotationsPOI[poi_index]
        
        let myview = UIWebView()

        var htmlString: String = ""
        
        htmlString = "<html><head>"
        htmlString = htmlString + "<style type='text/css'>"
        htmlString = htmlString + "p {font-size:10pt;font-family:Arial, Helvetica, sans-serif;}"
        htmlString = htmlString + "</style>"
        htmlString = htmlString + "</head>"
        
        htmlString = htmlString + "<body leftmargin='0' topmargin='0' rightmargin='0' bottommargin='0'>"
        htmlString = htmlString + "<p>"
        htmlString = htmlString + "<b>Bus No.: " + myannotation.route_id + " - " + myannotation.trip_headsign + "</b><br>"
        htmlString = htmlString + "<b>" + myannotation.start_stop_time + "</b> from " + myannotation.start_stop_name + "<br>"
        htmlString = htmlString + "<b>" + myannotation.end_stop_time + "</b> arrive at " + myannotation.end_stop_name + "<br>"
        htmlString = htmlString + "</p>"
        htmlString = htmlString + "</body>"
        htmlString = htmlString + "</html>"
        
        myview.loadHTMLString(htmlString, baseURL: nil)
    
        
        let widthConstraint = NSLayoutConstraint(item: myview, attribute: .Width, relatedBy: .Equal, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 200)
        myview.addConstraint(widthConstraint)
        
        let heightConstraint = NSLayoutConstraint(item: myview, attribute: .Height, relatedBy: .Equal, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 100)
        myview.addConstraint(heightConstraint)
        
        return myview
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
    
    func mapView(mapView: MKMapView, rendererForOverlay overlay: MKOverlay) -> MKOverlayRenderer! {
        if overlay is MKPolyline {
            let polylineRenderer = MKPolylineRenderer(overlay: overlay)
            polylineRenderer.strokeColor = UIColor.blueColor()
            polylineRenderer.alpha = 0.5
            polylineRenderer.lineWidth = 5
            return polylineRenderer
        }
    
        return nil
    }
    
    func mapView(mapView: MKMapView!, annotationView view: MKAnnotationView!,
                 calloutAccessoryControlTapped control: UIControl!) {
        
        if control == view.rightCalloutAccessoryView {
            print("Right")
        }
        else if control == view.leftCalloutAccessoryView   {
            print("Left")
        }
        
    }
    

    func mapView(mapView: MKMapView, didSelectAnnotationView view: MKAnnotationView){
        
        if(view.annotation?.isKindOfClass(MKUserLocation) == true){
            return
        }
        
        let index = find_index_of_annoation(view.annotation!, annotation_arrays: self.annotationsPOI)
        
        self.show_bus_route_by_index(index)
        
        let table_index = NSIndexPath(forRow: index, inSection: 0)
        self.poiTable.selectRowAtIndexPath(table_index, animated: true, scrollPosition: UITableViewScrollPosition.Middle)
        
        zoom_on_two_location(CLLocationCoordinate2D(latitude: Double(self.lat)!, longitude: Double(self.lng)!), location2: (view.annotation?.coordinate)!)
        
        
    }
    
    func mapView(mapView: MKMapView, viewForAnnotation annotation: MKAnnotation) -> MKAnnotationView? {
        
        if let annotation = annotation as? POI {
            let identifier = "pin"
            var view: MKPinAnnotationView
//            if let dequeuedView = mapView.dequeueReusableAnnotationViewWithIdentifier(identifier)
//                as? MKPinAnnotationView { // 2
//                    dequeuedView.annotation = annotation
//                    view = dequeuedView
//            } else {
//                 3
            view = MKPinAnnotationView(annotation: annotation, reuseIdentifier: identifier)
            view.canShowCallout = true
            view.calloutOffset = CGPoint(x: -5, y: 5)
            
//            let bus_button = BusUIButton(type: .DetailDisclosure)
//            bus_button.poi_index = annotation.index
//            bus_button.addTarget(self, action: #selector(ViewController.busRouteButtonClicked(_:)), forControlEvents: UIControlEvents.TouchUpInside)
//            
//            view.rightCalloutAccessoryView = bus_button as UIView
            
            
//            let yelp_button = YelpUIButton(type: .ContactAdd)
//            yelp_button.urlString = annotation.yelp_url
//            yelp_button.addTarget(self, action: #selector(ViewController.yelpButtonClicked(_:)), forControlEvents: UIControlEvents.TouchUpInside)
            
//            view.leftCalloutAccessoryView = yelp_button as UIView
            

        let myview = instanceFromUIWebView(annotation.index)
        view.detailCalloutAccessoryView = myview
            
            
//            let myview = instanceFromNib(annotation.index)
//            
//            view.detailCalloutAccessoryView = myview
            
            
//            }
        
            
            return view
        }
        return nil
    }
    
    
    func busRouteButtonClicked(sender:BusUIButton){
        
        show_bus_route_by_index(sender.poi_index!)
    }
    
    func show_bus_route_by_index(index: Int){
        
        // remove existing bus routes
        let overlaysToRemove = mapView.overlays
        mapView.removeOverlays(overlaysToRemove)
        
        if(index == -1){
            return
        }
        
        if(self.annotationsPOI[index].bus_shape==""){
            
            self.api.get_trip_shape(self.annotationsPOI[index].trip_id, start_stop: self.annotationsPOI[index].start_stop, end_stop: self.annotationsPOI[index].end_stop, city_code: self.annotationsPOI[index].city_code)
            {response in
                if(response != nil){
                    if(response!["success"]! as! Int==1){
                        print(response!["message"])
                        let raw_shape = response!["results"] as! String
                        self.annotationsPOI[index].bus_shape = raw_shape
                        
                        var locations: [CLLocationCoordinate2D] = decodePolyline(raw_shape)!
                        
                        let polyline = MKPolyline(coordinates: &locations, count: locations.count)
                        self.mapView.addOverlay(polyline)
                        //                                self.centerOnUser()
                    }
                    else{
                        print(response!["message"])
                    }
                }
                else{
                    print("nil")
                }
            }
        }
        else{
            let raw_shape = self.annotationsPOI[index].bus_shape as String!
            
            var locations: [CLLocationCoordinate2D] = decodePolyline(raw_shape)!
            
            let polyline = MKPolyline(coordinates: &locations, count: locations.count)
            self.mapView.addOverlay(polyline)
            
        }
        
    }
    
    func yelpButtonClicked(sender:YelpUIButton){
        // open button url in safari
        UIApplication.sharedApplication().openURL(NSURL(string: sender.urlString!)!)
    }
    
    func centerOnUser(){
        
        let center = CLLocationCoordinate2D(latitude: Double(self.lat)!, longitude: Double(self.lng)!)
        
        let region = MKCoordinateRegion(center: center, span: MKCoordinateSpan(latitudeDelta: 0.03, longitudeDelta: 0.03))
        
        self.mapView.setRegion(region, animated: true)
    }
    
    func zoom_on_two_location(location1: CLLocationCoordinate2D, location2: CLLocationCoordinate2D){
        
        let center = CLLocationCoordinate2D(latitude: (location1.latitude + location2.latitude)/2,
                                            longitude:(location1.longitude + location2.longitude)/2)
        
        let region = MKCoordinateRegion(center: center,
                                        span: MKCoordinateSpan(latitudeDelta: fabs(location1.latitude - location2.latitude)*2,
                                            longitudeDelta: fabs(location1.longitude - location2.longitude)*2))
        self.mapView.setRegion(region, animated: true)
        
    }
}