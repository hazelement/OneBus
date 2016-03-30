//
//  util.swift
//  OneBus
//
//  Created by Harry Zheng on 2016-03-29.
//  Copyright © 2016 Harry Zheng. All rights reserved.
//

import Foundation


func extractString(value : AnyObject?) -> String {
    if value is NSNull {
        return ""
    } else {
        return (value as! String)
    }
}