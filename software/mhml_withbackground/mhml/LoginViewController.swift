//
//  LoginViewController.swift
//  UserLoginAndRegistration
//
//  Created by Sleepify Team
//  Copyright (c) 2017 Sleepify UK Ltd. All rights reserved.
//
//  This is the LoginViewController, it provides classes and methods for user to login.
//  It also handles feedback from the server to see if the login is valid. 
//

import UIKit
import Alamofire
//import SwiftyJSON


//Declare extension to hide keyboard when user tap outside of the keyboard.
extension UIViewController {
    func hideKeyboardWhenTappedAround() {
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(UIViewController.dismissKeyboard))
        view.addGestureRecognizer(tap)
    }
    
    func dismissKeyboard() {
        view.endEditing(true)
    }
}

//Declare publice class to share variables
public class SharedLogin {
    static let shareInstance = SharedLogin()
    var usernameString = String()
    var userTokenString = String()
    var userdeviceTokenString = String()
}

//Actual class for LoginViewController
class LoginViewController: UIViewController {
    
    var token = ""
    var v = ""
    var valuet:String? = ""
    var field_error:String? = ""
    var donedone = 0

    @IBOutlet weak var userNameTextField: UITextField!
    @IBOutlet weak var userPasswordTextField: UITextField!
    
    @IBOutlet weak var returnlabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        self.hideKeyboardWhenTappedAround()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    // MARK: Action
    @IBAction func loginButtonTapped(_ sender: AnyObject) {
        
        let userPassword = userPasswordTextField.text;
        let userName = userNameTextField.text;
    
        if ( (userPassword?.isEmpty)! || (userName?.isEmpty)!){
            print("fields are empty")
            returnlabel.text = "Fields are empty"
            
        } else {
            SharedLogin.shareInstance.usernameString = userName!  // set share instance value here
            logIn()
            
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
            "password": userPasswordTextField.text! //password
        ]
        var statusCode: Int = 0
        
        
        //Start a Alamofire Session
        let sessionManager = Alamofire.SessionManager.default
        sessionManager.request("http://sleepify.zapto.org/api/csrf/", method: .get)
            .responseString { response in
                if let headerFields = response.response?.allHeaderFields as? [String: String],
                    let URL = response.response?.url {
                    let csrf_token = headerFields["Set-Cookie"]
                    let cookies = HTTPCookie.cookies(withResponseHeaderFields: headerFields, for: URL)
                    
                    let startIndex = csrf_token?.index((csrf_token?.startIndex)!, offsetBy:10)
                    let endIndex = csrf_token?.index((csrf_token?.startIndex)!, offsetBy: 73)
                    
                    self.v = (csrf_token?[startIndex!...endIndex!])!
                    
                    print("v: \(self.v)")
                    
                    SharedLogin.shareInstance.userTokenString = self.v
                    
                    //Create headers for packets
                    let headers: HTTPHeaders = [
                        "X-CSRFToken": self.v,
                        "Cookie" : ""
                    ]
                 
                    Alamofire.SessionManager.default.session.configuration.httpAdditionalHeaders = headers
                    
                    Alamofire.SessionManager.default.session.configuration.httpCookieStorage?.setCookie(cookies.first!)
                    sessionManager.request(
                        "http://sleepify.zapto.org/api/auth/login/",
                        method: .post,
                        parameters: parameters,
                        encoding: JSONEncoding.default,
                        headers:headers
                        ).responseJSON { response in
                            
                            statusCode = (response.response?.statusCode)! //Gets HTTP status code, useful for debugging
                            
                            if let result = (response.result.value){
                                
                                let value = result as! NSDictionary
                                
                                
                                print("statuscode: \(statusCode)")
                                
                                //StatusCode = 200, meaning login successful
                                if statusCode == 200 {
                                    print("Response:  \(value)")
                                    self.valuet = (value.object(forKey: "key") as! String)
                                    //print("TOKEEN: \(self.valuet)")
                                }

                                
                            }

                            if statusCode == 200{
                                print("token valid")
                                
                                
                                let packets: Parameters = [
                                    "usernmae" : self.userNameTextField.text!,
                                    "token" : SharedLogin.shareInstance.userdeviceTokenString
                                ]
                                
                                print("Data: \(packets)")
                                
                                sessionManager.request(
                                    "http://sleepify.zapto.org/api/pushy_token/",
                                    method: .post,
                                    parameters: packets,
                                    encoding: JSONEncoding.default,
                                    headers: headers
                                    ).responseJSON { response in
                                        
                                        statusCode = (response.response?.statusCode)!
                                        
                                        if let result = (response.result.value){
                                            let value = result as! NSDictionary
                                            print("result: \(value)")
                                        }
                                }
                                
                                //If login sucessfully, move into the next view
                                self.performSegue(withIdentifier: "showMain", sender: self);
                            } else {
                                print("token is not valid, error detected")
                                self.returnlabel.text = "Invalid User name or password"
                            }
                        }
                    
                }
                

        }

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
