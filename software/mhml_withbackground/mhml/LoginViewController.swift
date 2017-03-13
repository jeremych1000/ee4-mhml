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



extension UIViewController {
    func hideKeyboardWhenTappedAround() {
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(UIViewController.dismissKeyboard))
        view.addGestureRecognizer(tap)
    }
    
    func dismissKeyboard() {
        view.endEditing(true)
    }
}

public class SharedLogin {
    static let shareInstance = SharedLogin()
    var usernameString = String()
    var userTokenString = String()
}


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
    

    @IBAction func loginButtonTapped(_ sender: AnyObject) {
        
        let userPassword = userPasswordTextField.text;
        let userName = userNameTextField.text;
        
        //let userEmailStored = UserDefaults.standard.string(forKey: "userEmail");
        
        //let userPasswordStored = UserDefaults.standard.string(forKey: "userPassword");
        
        
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
            //"email" : userEmailTextField.text!,
            "password": userPasswordTextField.text! //password
        ]
        var statusCode: Int = 0
        
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
                                if statusCode == 200 {
                                    print("Response:  \(value)")
                                    self.valuet = (value.object(forKey: "key") as! String)
                                    print("TOKEEN: \(self.valuet)")
                                }
                
                                
                                /*
                                let authManager = Alamofire.SessionManager.default
                                
                                authManager.session.configuration.httpAdditionalHeaders = [
                                    "X-CSRFToken" : self.v,
                                    "Authorization": "Token \(self.valuet)",
                                    "HTTP_AUTHORIZATION": "Token \(self.valuet)",
                                    "Token": (self.valuet),
                                    "Content-Type": "text/json"
                                ]
                                
                                let sessionManagernew = Alamofire.SessionManager.default
                                
                                print("CSRFT: \(self.v)")

                                Alamofire.SessionManager.default.session.configuration.httpCookieStorage?.setCookie(cookies.first!)
                                
                                sessionManagernew.request(
                                    "http://sleepify.zapto.org/api/make_coffee/",
                                    method: .get)
                                    //headers: headersnew)
                                    .responseData { response in
                                        debugPrint("All Response info: \(response)")
                                        
                                        if let datanew = response.result.value, let return_string = String(data: datanew, encoding: .utf8){
                                            
                                            print("return \(return_string)")
                                        } else {
                                            print("no tea pot")
                                        }
                                        
                                        
                                } */

                                
                            }
                            
                            
                            if statusCode == 200{
                                print("token valid")
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
