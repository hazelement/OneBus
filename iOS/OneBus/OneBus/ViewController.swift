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



class ViewController: UIViewController, CLLocationManagerDelegate, UISearchBarDelegate, MKMapViewDelegate, UITableViewDelegate, UITableViewDataSource {

    
    
    @IBOutlet weak var btnHideList: HideListButton!
   
    @IBOutlet weak var btnCenter: UIButton!
    
    @IBOutlet weak var searchBar: UISearchBar!
    
    @IBOutlet weak var mapView: MKMapView!
    
    @IBOutlet weak var poiTable: UITableView!
    @IBOutlet weak var tableBottomLocation: NSLayoutConstraint!
    
    let ANIMATION_DURATION = 0.2
    let ANIMATION_DELAY = 0.0
    
    var locationManager: CLLocationManager!
    var first_time_open = true
    
    var api = API_Class()
    
    var annotationsPOI: Array = [POI]()
    
    var lat: String = "51.0454027"
    var lng: String = "-114.05651890000001"
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        
        self.poiTable.dataSource = self
        self.poiTable.delegate = self
//        self.poiTable.registerClass(UITableViewCell.self, forCellReuseIdentifier: "cell")
        self.poiTable.registerNib(UINib(nibName: "CustomizeTableCell", bundle: nil), forCellReuseIdentifier: "CustomizeTableCellUnit")
        self.hidePOITable(false)
        
        self.annotationsPOI = [POI]()
        self.api = API_Class()
        
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
    
    
    @IBAction func btnHideListClicked(sender: AnyObject) {
        toggle_table(false)
    }
    
    
    func searchBarSearchButtonClicked( search_bar: UISearchBar){
        
        // refresh data and annotaions
        let annotationsToRemove = self.mapView.annotations.filter { $0 !== self.mapView.userLocation }
        self.mapView.removeAnnotations( annotationsToRemove )
        let overlaysToRemove = mapView.overlays
        mapView.removeOverlays(overlaysToRemove)
        self.annotationsPOI = [POI]()
        
        let search_txt = search_bar.text!
        
        // if is not first time, need to hide table first
        if(self.first_time_open == false){
//            self.hidePOITable(true)
            self.toggle_table(true)
        } else {
            
        }
        
//        SwiftSpinner.show("Looking around ...")
        api.search_results(search_txt, lat: self.lat, lng: self.lng)
            {response in
                if(response != nil){
                    if(response!["success"]! as! Int==1){
                        print(response!["message"])
                        self.collectResults(response!["results"] as! NSDictionary)
                        
                        self.mapView.addAnnotations(self.annotationsPOI)
                    }
                    else{
                        print(response!["message"])
                    }
                }
                else{
                    print("nil")
                    let alertController = UIAlertController(title: "Server Error", message:
                        "Oops, our server are being lazy. We are getting it to work.", preferredStyle: UIAlertControllerStyle.Alert)
                    alertController.addAction(UIAlertAction(title: "Dismiss", style: UIAlertActionStyle.Default,handler: nil))
                    
                    self.presentViewController(alertController, animated: true, completion: nil)
                }
//                SwiftSpinner.hide()
                
                self.poiTable.reloadData()
//                self.showPOITable()
                self.toggle_table(false)
                self.centerOnUser()
                self.first_time_open=false
        }

        
        self.searchBar.endEditing(true)
    }
    
    func collectResults(result: NSDictionary){
        
        for (key, value) in result {
            
            let detail = value as! NSDictionary
            
            let lat = detail["lat"] as! Double
            let lng = detail["lng"] as! Double
            
            let myLocation = CLLocationCoordinate2DMake(lat, lng)
            
            let poi = POI(index: annotationsPOI.count,
                          destName: extractString(detail["dest_name"]),
                          address: extractString(detail["address"]),
                          image_url: extractString(detail["image_url"]),
                          yelp_url: extractString(detail["yelp_url"]),
                          review_count: detail["review_count"] as! Int,
                          ratings_img_url: extractString(detail["ratings_img"]),
                          coordinate: myLocation,
                          start_stop: detail["start_stop"] as! Int,
                          end_stop: detail["end_stop"] as! Int,
                          trip_id: detail["trip_id"] as! Int,
                          route_id: detail["route_id"] as! Int)
            
            annotationsPOI.append(poi)
            
            print("Property: \"\(key as! String)\"")
        }

    }
    
    
    @IBAction func btnCenterClicked(sender: UIButton) {
        
        centerOnUser()

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
        self.mapView.setRegion(coordinateRegion, animated: true)
    }
    
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

