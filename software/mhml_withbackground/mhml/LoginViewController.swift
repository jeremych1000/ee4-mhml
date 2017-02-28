//
//  LoginViewController.swift
//  UserLoginAndRegistration
//
//  Created by Sergey Kargopolov on 2015-01-13.
//  Copyright (c) 2015 Sergey Kargopolov. All rights reserved.
//

import UIKit
import Alamofire
//import SwiftyJSON

class LoginViewController: UIViewController {
    
    var token = ""

    @IBOutlet weak var userNameTextField: UITextField!
    @IBOutlet weak var userPasswordTextField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    @IBAction func loginButtonTapped(_ sender: AnyObject) {
        
        //let userEmail = userNameTextField.text;
        let userPassword = userPasswordTextField.text;
        let userName = userNameTextField.text;
        
        let userEmailStored = UserDefaults.standard.string(forKey: "userEmail");
        
        let userPasswordStored = UserDefaults.standard.string(forKey: "userPassword");
        
        //let userNameStored = U
        
        //print("\(userEmail)");
        print("\(userPassword)");
        print("\(userEmailStored)")
        
        
        
        if ( (userPassword?.isEmpty)! || (userName?.isEmpty)!){
            print("fields are empty")
            
        } else {
            logIn()
            print("Logged in")
            if token != nil {
                print("token valid")
                self.performSegue(withIdentifier: "showMain", sender: self);
            }
        }
    }
    
    // MARK: Function
    
    /**
     Function that logs the user in and stores the session token for later use
     **/
    func logIn() {
        print("\(userNameTextField.text!)")
        
        let parameters = [
            "username": userNameTextField.text!,
            //"email" : userEmailTextField.text!,
            "password": userPasswordTextField.text! //password
        ]
        var statusCode: Int = 0
        
        Alamofire.request("http://sleepify.zapto.org/api/auth/login/",method: .post, parameters: parameters, encoding: JSONEncoding.default)
            .responseJSON { response in
                
                statusCode = (response.response?.statusCode)! //Gets HTTP status code, useful for debugging
                if let value = response.result.value {
                    //Handle the results as JSON
                    //let post = JSON(value)
                    
                    //if let key = post["session_id"].string {
                    //At this point the user should have authenticated, store the session id and use it as you wish
                   // self.token = value as! String
                    print("TOKEN:  \(value)")
                } else {
                    print("error detected")
                }
            }
        //}
    }
    
    
    
    



    
    
    
    
    
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */


}
