//
//  ViewController.swift
//  820lit
//
//  Created by Stiven Deleur on 1/28/17.
//  Copyright © 2017 Stiven Deleur. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    var ref: FIRDatabaseReference!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        ref = FIRDatabase.database().reference()
        
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

