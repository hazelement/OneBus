//
//  VCTableView.swift
//  OneBus
//
//  Created by Harry Zheng on 2016-04-12.
//  Copyright © 2016 Harry Zheng. All rights reserved.
//

import Foundation
import UIKit

extension ViewController{
    
    
    func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        // 1
        return 1
    }
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // 2
        return annotationsPOI.count
    }
    
    func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath){
        
        self.mapView.selectAnnotation(self.annotationsPOI[indexPath.row], animated: true)
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        // 3
        
        let cell = tableView.dequeueReusableCellWithIdentifier("CustomizeTableCellUnit", forIndexPath: indexPath) as! CustomizeTableCell

        
//        let cell = tableView.dequeueReusableCellWithIdentifier("poiCell", forIndexPath: indexPath) as UITableViewCell
        
//        cell.textLabel!.text = annotationsPOI[indexPath.row].title
        
        cell.name.text = annotationsPOI[indexPath.row].title
        cell.no_reviews.text = String(annotationsPOI[indexPath.row].review_count) + " of reviews from yelp"
        cell.review_image.downloadedFrom(link: annotationsPOI[indexPath.row].ratings_img_url, contentMode: UIViewContentMode.ScaleAspectFill)
        cell.yelp_button.urlString = annotationsPOI[indexPath.row].yelp_url
        return cell
    }
    
    
    
    func toggle_table(loading: Bool){
        
        
//        if(loading == false){
        if(self.btnHideList.table_is_hidden == true){ // show table
            
            showPOITable("Hide List")
            
        }
        else if(self.btnHideList.table_is_hidden == false) { // hide table
            
            hidePOITable("Show List")
        }
//            }
//        } else {  // hide table with loading label
//            self.btnHideList.table_is_hidden = true
//            self.btnHideList.setTitle("Loading...", forState: .Normal)
//            hidePOITable(true)
//        }
    }
    
    func showPOITable(label: String){
        if(self.btnHideList.table_is_hidden == true){
            self.btnHideList.hidden=false
            self.btnHideList.table_is_hidden = false
            self.btnHideList.setTitle(label, forState: .Normal)
            
            UIView.animateWithDuration(ANIMATION_DURATION, delay: ANIMATION_DELAY, options: [.CurveEaseOut], animations: {
                
                self.tableBottomLocation.constant -= self.poiTable.frame.size.height
                
                self.view.layoutIfNeeded()
                }, completion: { finished in
                    print("Table show")
            })
        }
    }
    
    func initHidePOITable(){
        self.tableBottomLocation.constant += self.poiTable.frame.size.height
        self.btnHideList.hidden=true
        self.btnHideList.table_is_hidden=true
        self.view.layoutIfNeeded()
    }
    
    func hidePOITable(label: String){
        self.btnHideList.setTitle(label, forState: .Normal)
        self.btnHideList.hidden=false
        if(self.btnHideList.table_is_hidden == false){
            
            self.btnHideList.table_is_hidden = true
            
            
            UIView.animateWithDuration(ANIMATION_DURATION, delay: ANIMATION_DELAY, options: [.CurveEaseOut], animations: {
                
                self.tableBottomLocation.constant += self.poiTable.frame.size.height
                self.view.layoutIfNeeded()
                
                }, completion: { finished in
                    print("Table hide")
            })
        }
    }
    
    
    
}
