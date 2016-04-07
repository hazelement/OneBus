//
//  ViewController.swift
//  OneBus
//
//  Created by Harry Zheng on 2016-03-25.
//  Copyright © 2016 Harry Zheng. All rights reserved.
//


// todo add pin drop annimation
// todo add html support in detailCalloutAccessoryView
// todo add bus route display


import UIKit
import MapKit
import CoreLocation


extension UIView {
    func loadFromNibNamed(nibNamed: String, bundle : NSBundle? = nil) -> UIView? {
        return UINib(
            nibName: nibNamed,
            bundle: bundle
            ).instantiateWithOwner(nil, options: nil)[0] as? UIView
    }
}



class ViewController: UIViewController, CLLocationManagerDelegate, UISearchBarDelegate, MKMapViewDelegate, UIWebViewDelegate {

    @IBOutlet weak var searchBar: UISearchBar!
    @IBOutlet weak var mapView: MKMapView!
    
//    @IBOutlet weak var webView: UIWebView!
//    var webView: UIWebView!
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
        
//        self.webView.delegate = self

    }
    
    func searchBarSearchButtonClicked( search_bar: UISearchBar){
        let annotationsToRemove = self.mapView.annotations.filter { $0 !== self.mapView.userLocation }
        self.mapView.removeAnnotations( annotationsToRemove )
        let search_txt = search_bar.text!

        SwiftSpinner.show("Looking around ...")
        api.search_results(search_txt, lat: self.lat, lng: self.lng)
            {response in
                if(response != nil){
                    if(response!["success"]! as! Int==1){
                        print(response!["message"])
                        self.plotResult(response!["results"] as! NSDictionary)
                    }
                    else{
                        print(response!["message"])
                    }
                }
                else{
                    print("nil")
                }
                SwiftSpinner.hide()
        }

        
        self.searchBar.endEditing(true)
    }
    
    func plotResult(result: NSDictionary){
        
        for (key, value) in result {
            
            let detail = value as! NSDictionary
            
            let lat = detail["lat"] as! Double
            let lng = detail["lng"] as! Double
            
            let myLocation = CLLocationCoordinate2DMake(lat, lng)
            
            let poi = POI(destName: extractString(detail["dest_name"]), address: extractString(detail["address"]), image_url: extractString(detail["image_url"]), yelp_url: extractString(detail["yelp_url"]), review_count: detail["review_count"] as! Int, ratings_img_url: extractString(detail["ratings_img"]), coordinate: myLocation)
            
//            usleep(useconds_t(500)) // todo drop down pins one after another like maps on iphone
            self.mapView.addAnnotation(poi)
            
            print("Property: \"\(key as! String)\"")
        }

    }
    

    func locationManager(manager: CLLocationManager, didUpdateLocations locations: [CLLocation]){
        let locValue:CLLocationCoordinate2D = manager.location!.coordinate
        self.lat = String(locValue.latitude)
        self.lng = String(locValue.longitude)
        
        print("locations = \(locValue.latitude) \(locValue.longitude)")
    }
    


    
    
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

