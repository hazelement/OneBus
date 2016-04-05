//
//  yelpUIButton.swift
//  OneBus
//
//  Created by Harry Zheng on 2016-04-04.
//  Copyright © 2016 Harry Zheng. All rights reserved.
//

import Foundation
import UIKit

class YelpUIButton: UIButton {
    var urlString: String?
}

func buttonClicked(sender:YelpUIButton)
{
    UIApplication.sharedApplication().openURL(NSURL(string: sender.urlString!)!)
//    if(sender.tag == 5){
//        
//        var abc = "argOne" //Do something for tag 5
//    }
//    println("hello")
}