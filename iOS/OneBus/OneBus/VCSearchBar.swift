//
//  VCSearchBar.swift
//  OneBus
//
//  Created by Harry Zheng on 2016-04-19.
//  Copyright © 2016 Harry Zheng. All rights reserved.
//

import Foundation
import UIKit

extension ViewController {

    func searchBarTextDidBeginEditing(searchBar: UISearchBar!){
        
        searchBar.setShowsCancelButton(true, animated: true)
    }

    func searchBarTextDidEndEditing(searchBar: UISearchBar!){
        searchBar.setShowsCancelButton(false, animated: true)
    }
    
    func searchBarCancelButtonClicked(searchBar: UISearchBar){
        searchBar.resignFirstResponder()
    }

}