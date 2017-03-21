//
//  ViewController.swift
//  UserLoginAndRegistration
//
//  Created by Sleepify Team
//  Copyright (c) 2017 Sleepify UK Ltd. All rights reserved.
// 
//  This is the logout view controller, at the moment, it only returns to the login page. 
//  In the future, this is be implemented according to the Logout out Django specificaiton. 

import UIKit

class logoutViewController: UIViewController {
    
    //MARK: Outlets
    
    @IBOutlet weak var logoutButton: UIButton!
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
                logoutButton.layer.cornerRadius = 8
    }
    
    //MARK: Action
    
    @IBAction func logoutButtonTapped(_ sender: Any) {
        UserDefaults.standard.set(false,forKey:"isUserLoggedIn");
        UserDefaults.standard.synchronize();
        
        self.performSegue(withIdentifier: "loginView", sender: self);
    }
    
    
    //MARK: Override Function
    
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

    
}

