//
//  ViewController.swift
//  UserLoginAndRegistration
//
//  Created by Sergey Kargopolov on 2015-01-08.
//  Copyright (c) 2015 Sergey Kargopolov. All rights reserved.
//

import UIKit

class logoutViewController: UIViewController {
    
    @IBOutlet weak var logoutButton: UIButton!
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
                logoutButton.layer.cornerRadius = 8
        
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    override func viewDidAppear(_ animated: Bool)
    {
        
        let isUserLoggedIn = UserDefaults.standard.bool(forKey: "isUserLoggedIn");
        
        if(!isUserLoggedIn)
        {
   //         self.performSegue(withIdentifier: "loginView", sender: self);
        }
        
        
    }
    
    
    @IBAction func logoutButtonTapped(_ sender: Any) {
        UserDefaults.standard.set(false,forKey:"isUserLoggedIn");
        UserDefaults.standard.synchronize();
        
        self.performSegue(withIdentifier: "loginView", sender: self);
        
        
    }
    
    
    
    
}

