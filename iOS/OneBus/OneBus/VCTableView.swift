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
    
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        // 3
        let cell = tableView.dequeueReusableCellWithIdentifier("poiCell", forIndexPath: indexPath) as UITableViewCell
        
        cell.textLabel!.text = annotationsPOI[indexPath.row].title
        return cell
    }
    
    func showPOITable(){
        UIView.animateWithDuration(ANIMATION_DURATION, delay: ANIMATION_DELAY, options: [.CurveEaseOut], animations: {
            
            self.tableBottomLocation.constant -= self.poiTable.frame.size.height
            
            self.view.layoutIfNeeded()
            }, completion: { finished in
                print("Table show")
        })
    }
    
    func hidePOITable(animated: Bool){
        if(animated){
            UIView.animateWithDuration(ANIMATION_DURATION, delay: ANIMATION_DELAY, options: [.CurveEaseOut], animations: {
                
                self.tableBottomLocation.constant += self.poiTable.frame.size.height
                self.view.layoutIfNeeded()
                
                }, completion: { finished in
                    print("Table hide")
            })
        } else {
            
            self.tableBottomLocation.constant += self.poiTable.frame.size.height
            self.view.layoutIfNeeded()
        }
        
    }
    
    
    
}
