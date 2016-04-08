//
//  util.swift
//  OneBus
//
//  Created by Harry Zheng on 2016-03-29.
//  Copyright © 2016 Harry Zheng. All rights reserved.
//

import Foundation
import UIKit

func extractString(value : AnyObject?) -> String {
    if value is NSNull {
        return ""
    } else {
        return (value as! String)
    }
}


extension UIImageView {
    func downloadedFrom(link link:String, contentMode mode: UIViewContentMode) {
        guard
            let url = NSURL(string: link)
            else {return}
        contentMode = mode
        NSURLSession.sharedSession().dataTaskWithURL(url, completionHandler: { (data, response, error) -> Void in
            guard
                let httpURLResponse = response as? NSHTTPURLResponse where httpURLResponse.statusCode == 200,
                let mimeType = response?.MIMEType where mimeType.hasPrefix("image"),
                let data = data where error == nil,
                let image = UIImage(data: data)
                else { return }
            dispatch_async(dispatch_get_main_queue()) { () -> Void in
                self.image = image
            }
        }).resume()
    }
}