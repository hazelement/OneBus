//
//  ViewController.swift
//  OneBus
//
//  Created by Harry Zheng on 2016-03-25.
//  Copyright © 2016 Harry Zheng. All rights reserved.
//

import UIKit
import MapKit
import CoreLocation

class ViewController: UIViewController, CLLocationManagerDelegate, UISearchBarDelegate, MKMapViewDelegate {

    @IBOutlet weak var searchBar: UISearchBar!
    @IBOutlet weak var mapView: MKMapView!
    
    var locationManager: CLLocationManager!
    var api = API_Class()
    
    var lat: String = "51.0454027"
    var lng: String = "-114.05651890000001"
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        self.searchBar.showsScopeBar = true
        self.searchBar.delegate = self
        
        self.locationManager = CLLocationManager()
        self.locationManager.desiredAccuracy = kCLLocationAccuracyBest
        self.locationManager.delegate = self
        
        let status = CLLocationManager.authorizationStatus()
        if status == .NotDetermined || status == .Denied || status == .AuthorizedWhenInUse {
            // present an alert indicating location authorization required
            // and offer to take the user to Settings for the app via
            // UIApplication -openUrl: and UIApplicationOpenSettingsURLString
            self.locationManager.requestAlwaysAuthorization()
            self.locationManager.requestWhenInUseAuthorization()
        }
        self.locationManager.startUpdatingLocation()
        self.locationManager.startUpdatingHeading()
        
        self.mapView.showsUserLocation = true
        self.mapView.delegate = self
        self.mapView.mapType = MKMapType(rawValue: 0)!
        self.mapView.userTrackingMode = MKUserTrackingMode(rawValue: 1)!

    }
    
    func searchBarSearchButtonClicked( search_bar: UISearchBar){
        let search_txt = search_bar.text!

        api.search_results(search_txt, lat: self.lat, lng: self.lng)
            {response in
                if(response != nil){
                    if(response!["success"]! as! Int==1){
                        print(response!["message"])
    //                    self.performSegueWithIdentifier("login_success",sender: self)
                        self.parseResult(response!["results"] as! NSDictionary)
                    }
                    else{
                        print(response!["message"])
                    }
                }
                else{
                    print("nil")
                }

        }

        
        self.searchBar.endEditing(true)
    }
    
    func parseResult(result: NSDictionary){
        
        for (key, value) in result {
            print("Property: \"\(key as! String)\"")
        }
    }
    

    func locationManager(manager: CLLocationManager, didUpdateLocations locations: [CLLocation]){
        let locValue:CLLocationCoordinate2D = manager.location!.coordinate
        self.lat = String(locValue.latitude)
        self.lng = String(locValue.longitude)
        
        print("locations = \(locValue.latitude) \(locValue.longitude)")
    }
    
//    func mapView(mapView: MKMapView, viewForAnnotation annotation: MKAnnotation) -> MKAnnotationView? {
//        func mapView(mapView: MKMapView, viewForAnnotation annotation: MKAnnotation) -> MKAnnotationView? {
//            if (annotation is MKUserLocation) {
//                return nil
//            }
//            
//            if (annotation.isKindOfClass(CustomAnnotation)) {
//                let customAnnotation = annotation as? CustomAnnotation
//                mapView.translatesAutoresizingMaskIntoConstraints = false
//                var annotationView = mapView.dequeueReusableAnnotationViewWithIdentifier("CustomAnnotation") as MKAnnotationView!
//                
//                if (annotationView == nil) {
//                    annotationView = customAnnotation?.annotationView()
//                } else {
//                    annotationView.annotation = annotation;
//                }
//                
//                self.addBounceAnimationToView(annotationView)
//                return annotationView
//            } else {
//                return nil
//            }
//        }

    
    
    func centerMapOnLocation(location: CLLocation) {
        let regionRadius: CLLocationDistance = 1000
        let coordinateRegion = MKCoordinateRegionMakeWithDistance(location.coordinate,
            regionRadius * 2.0, regionRadius * 2.0)
        mapView.setRegion(coordinateRegion, animated: true)
    }
    
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

