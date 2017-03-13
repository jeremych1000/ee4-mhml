//
//  ForgotViewController.swift
//  mhml
//
//  Created by Tszho on 11/03/2017.
//  Copyright © 2017 Nathalie Wong. All rights reserved.
//

import Foundation
import Alamofire
//import SwiftyJSON

class ForgotViewController: UIViewController {
    
    
    @IBOutlet weak var ResetButton: UIButton!
    @IBOutlet weak var userEmailTextField: UITextField!
    
    var token = ""
    var v = ""
    var valuet:String? = ""
    var field_error:String? = ""

    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        self.hideKeyboardWhenTappedAround()
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    //MARK: Action
    
    
    @IBAction func didResetpress(_ sender: Any) {
        print("Reset User")
        resetuser()
    }
    
    
    
    
    // MARK: Function
    

    func resetuser() {
        print("\(userEmailTextField.text!)")
        
        let parameters = [
            "email": userEmailTextField.text!,
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
                    
                    self.v = (csrf_token?[startIndex!...endIndex!])!
                    
                    print("CSRF_TOKEN: \(self.v)")
                    
                    let headers: HTTPHeaders = [
                        "X-CSRFToken": self.v,
                        "Cookie" : ""
                    ]
                    
                    Alamofire.SessionManager.default.session.configuration.httpAdditionalHeaders = headers
                    
                    Alamofire.SessionManager.default.session.configuration.httpCookieStorage?.setCookie(cookies.first!)
                    sessionManager.request(
                        "http://sleepify.zapto.org/api/auth/password/reset/",
                        method: .post,
                        parameters: parameters,
                        encoding: JSONEncoding.default,
                        headers:headers
                        )   .responseJSON { response in
                            
                            statusCode = (response.response?.statusCode)! //Gets HTTP status code, useful for debugging
                            
                            if let result = (response.result.value){
                                
                                let value = result as! NSDictionary
                                
                                
                                print("statuscode: \(statusCode)")
                                if statusCode == 200 {
                                    print("Response:  \(value)")
                                    self.valuet = (value.object(forKey: "key") as! String)
                                    print("TOKEEN: \(self.valuet)")
                                }
                            }
                    }
                }
        }
    }
    
    
    
    
    
    


    
}
