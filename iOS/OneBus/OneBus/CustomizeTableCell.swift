//
//  CustomizeTableCell.swift
//  OneBus
//
//  Created by Harry Zheng on 2016-04-13.
//  Copyright © 2016 Harry Zheng. All rights reserved.
//

import UIKit

class CustomizeTableCell: UITableViewCell {

    @IBOutlet weak var yelp_button: YelpUIButton!
    @IBOutlet weak var name: UILabel!
    @IBOutlet weak var no_reviews: UILabel!
    @IBOutlet weak var review_image: UIImageView!
    
    @IBAction func yelpButtonClicked(sender: YelpUIButton) {
        UIApplication.sharedApplication().openURL(NSURL(string: sender.urlString!)!)

    }
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
