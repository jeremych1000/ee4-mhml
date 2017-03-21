//
//  RegisterPageViewController.swift
//  UserLoginAndRegistration
//
//  Created by Sleepify Team
//  Copyright (c) 2017 Sleepify UK Ltd. All rights reserved.
//
// This is the registration page, where users can create a new acconnt in this view


import UIKit
//import Parse
import Alamofire

class RegisterPageViewController: UIViewController {
    
    //MARK: Outlets

    @IBOutlet weak var userNameTextField: UITextField!
    @IBOutlet weak var userEmailTextField: UITextField!
    @IBOutlet weak var userPasswordTextField: UITextField!
    @IBOutlet weak var userRepeatPassTextField: UITextField!
    @IBOutlet weak var registerButton: UIButton!

    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.hideKeyboardWhenTappedAround()
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    //MARK: Action
    
    
    @IBAction func registerButtonTapped(_ sender: Any) {

    
        let userEmail = userEmailTextField.text;
        let userPassword = userPasswordTextField.text;
        let userRepeatPassword = userRepeatPassTextField.text;
        let userName = userNameTextField.text;
        
        // Check for empty fields
        if((userEmail?.isEmpty)! || (userPassword?.isEmpty)! || (userRepeatPassword?.isEmpty)! || (userName?.isEmpty)!)
        {
            
            // Display alert message 
                print("All fields are required")

       }
        
        //Check if passwords match 
        if(userPassword != userRepeatPassword)
        {
            print("Passwords do not match")
        }
        
        let parameters = [
            "email": userEmailTextField.text!,
            "username" : userName!,
            "password1" : userPassword!,
            "password2" : userRepeatPassword!
            ]
        var statusCode: Int = 0
        
        print("\(parameters)")
        
        let sessionManager = Alamofire.SessionManager.default
        sessionManager.request("http://sleepify.zapto.org/api/csrf/", method: .get)
            .responseString { response in
                if let headerFields = response.response?.allHeaderFields as? [String: String],
                    let URL = response.response?.url {
                    let csrf_token = headerFields["Set-Cookie"]
                    let cookies = HTTPCookie.cookies(withResponseHeaderFields: headerFields, for: URL)
                    
                    let startIndex = csrf_token?.index((csrf_token?.startIndex)!, offsetBy:10)
                    let endIndex = csrf_token?.index((csrf_token?.startIndex)!, offsetBy: 73)
                    
                    let v = (csrf_token?[startIndex!...endIndex!])!
                    
                    print("CSRF_TOKEN: \(v)")
                    
                    let headers: HTTPHeaders = [
                        "X-CSRFToken": v,
                        "Cookie" : ""
                    ]
                    
                    Alamofire.SessionManager.default.session.configuration.httpAdditionalHeaders = headers
                    
                    Alamofire.SessionManager.default.session.configuration.httpCookieStorage?.setCookie(cookies.first!)
                    sessionManager.request(
                        "http://sleepify.zapto.org/api/auth/registration/",
                        method: .post,
                        parameters: parameters,
                        encoding: JSONEncoding.default,
                        headers:headers
                        )   .responseJSON { response in
                            
                            statusCode = (response.response?.statusCode)! //Gets HTTP status code, useful for debugging
                            
                            if let result = (response.result.value){
                                
                                let value = result as! NSDictionary
                                
                                //statusCode Registered sucessful
                                if statusCode == 201 {
                                    print("Response:  \(value)")
                                    //self.valuet = (value.object(forKey: "key") as! String)
                                    //print("TOKEEN: \(self.valuet)")
                                }
                            }
                    }
                }
        }

    }
    
    
    // MARK: Helper function
    

}


