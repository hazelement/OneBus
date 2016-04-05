//
//  POIView2.swift
//  OneBus
//
//  Created by Harry Zheng on 2016-04-03.
//  Copyright © 2016 Harry Zheng. All rights reserved.
//

import UIKit


// this one is working!!!!
class POIView: UIView {

    /*
    // Only override drawRect: if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    override func drawRect(rect: CGRect) {
        // Drawing code
    }
    */
    class func instanceFromNib(address: String, no_review: Int, yelp_url: String) -> UIView {
        let myview = UINib(nibName: "POIView", bundle: nil).instantiateWithOwner(nil, options: nil)[0] as! UIView
//        return UINib(nibName: "POIView", bundle: nil).instantiateWithOwner(nil, options: nil)[0] as! UIView
        let address_label = myview.viewWithTag(2) as! UILabel
        let review_count = myview.viewWithTag(1) as! UILabel
        let yelp_button = myview.viewWithTag(4) as! YelpUIButton
        yelp_button.urlString = yelp_url
        
        
        address_label.text = address
        review_count.text = String(no_review)
        
        return myview
    }
}

//    @IBOutlet var myView: UIView!

////    var address: String
////    var no_of_review: Int
//
//class func instanceFromNib() -> UIView {
//    return UINib(nibName: "POIView", bundle: nil).instantiateWithOwner(nil, options: nil)[0] as! UIView
//}

//
//    init(address: String, no_of_review: Int) {
//        self.address = address
//        self.no_of_review = no_of_review
//        super.init(frame: CGRect(x: 0, y: 0, width: 100, height: 100))
//
//        NSBundle.mainBundle().loadNibNamed("POIView", owner: self, options: nil)
//        self.addSubview(self.view)
//    }
//
//
//    required init(coder aDecoder:NSCoder){
//        self.address = ""
//        self.no_of_review = 0
//        super.init(coder: aDecoder)!
//
//    }

