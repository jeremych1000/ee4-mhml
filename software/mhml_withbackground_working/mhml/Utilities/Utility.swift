/*
* Copyright (c) 2015, Nordic Semiconductor
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
*
* 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
*
* 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the
* documentation and/or other materials provided with the distribution.
*
* 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this
* software without specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
* LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
* HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
* LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
* ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
* USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

import UIKit
import HomeKit

open class Utility {
    
    //For showing Processing Message with activity indicator
    fileprivate var processingMessageView = UIView()
    fileprivate var processingActivityIndicator = UIActivityIndicatorView()
    fileprivate var processingSuperView:UIView?
    
    //For Showing Empty Table Message
    fileprivate var emptyTableMessageView = UIView()
    fileprivate var emptyTableSuperView : UITableView?
    
    fileprivate var emptyRoomsTableMessageView = UIView()
    fileprivate var emptyRoomsTableMessageSuperView : UITableView?
    
    fileprivate var emptyAccessoriesTableMessageView = UIView()
    fileprivate var emptyAccessoriesTableMessageSuperView : UITableView?
    
    fileprivate var isAlertVisible = false
    
    open class var sharedInstance : Utility {
        struct staticUtility {
            static let instance:Utility = Utility()
        }
        return staticUtility.instance
    }
    
    //Messages to show for empty table view
    open let NO_HOME_FOUND_IN_SELECT_DEVICE = "There is no home. Please add Home from Settings."
    open let NO_ACCESSORY_IN_PRIMARY_HOME = "There is no accessory in Primary Home. Please add accessory from Settings or change Primay Home from Settings."
    open let NO_HOME_FOUND_IN_SETTINGS = "There is no home. Please add Home by tapping [+] on navigation bar."
    open let NO_ROOM_FOUND_IN_HOME_SETTINGS = "Please add Room by tapping on [+]."
    open let NO_ACCESSORIES_FOUND_IN_HOME_SETTINGS = "Please add Accessory by tapping on [+]."
    open let NO_ROOM_FOUND_IN_ACCESSORY_CONFIG = "No Room is found in this Home. Please add one from ROOMS in Configure Home page."
    open let NO_ACCESSORY_FOUND_IN_ROOM_CONFIG = "No Accessory is found in this room. Please add one from ACCESSORIES in Configure Home page."
    open let NO_ACCESSORY_FOUND_IN_ADD_ACCESSORY = "No Accessory to add. Please makes sure the accessory is in range."

    open func displayEmptyTableMessage(_ tableView:UITableView, msg:String) {
        let viewWidth:CGFloat = 200
        let viewHeight:CGFloat = 150
        self.emptyTableSuperView = tableView
        removeEmptyTableMessage()
        
        let emptyTableMessageLabel = UILabel(frame: CGRect(x: 10, y: 10, width: viewWidth - 20, height: viewHeight - 20))
        emptyTableMessageLabel.text = msg
        emptyTableMessageLabel.textColor = UIColor.white
        emptyTableMessageLabel.font = UIFont(name: "HelveticaNeue", size: 16.0)
        emptyTableMessageLabel.lineBreakMode = .byWordWrapping
        emptyTableMessageLabel.numberOfLines = 0
        
        emptyTableMessageView = UIView(frame: CGRect(x: tableView.frame.midX - 100, y: tableView.frame.midY - 150 , width: viewWidth, height: viewHeight))
        emptyTableMessageView.layer.cornerRadius = 15
        //emptyTableMessageView.backgroundColor = UIColor(white: 0, alpha: 0.5)
        emptyTableMessageView.backgroundColor = UIColor.lightGray
        
        emptyTableMessageView.addSubview(emptyTableMessageLabel)
        
        tableView.addSubview(emptyTableMessageView)
        tableView.separatorStyle = .none
        tableView.isScrollEnabled = false
    }
    
    open func displayEmptyTableMessageAtTop(_ tableView:UITableView, msg:String) {
        let viewWidth:CGFloat = 200
        let viewHeight:CGFloat = 150
        self.emptyTableSuperView = tableView
        removeEmptyTableMessage()
        
        let emptyTableMessageLabel = UILabel(frame: CGRect(x: 10, y: 10, width: viewWidth - 20, height: viewHeight - 20))
        emptyTableMessageLabel.text = msg
        emptyTableMessageLabel.textColor = UIColor.white
        emptyTableMessageLabel.font = UIFont(name: "HelveticaNeue", size: 16.0)
        emptyTableMessageLabel.lineBreakMode = .byWordWrapping
        emptyTableMessageLabel.numberOfLines = 0
        
        emptyTableMessageView = UIView(frame: CGRect(x: tableView.frame.midX - 100, y: 30 , width: viewWidth, height: viewHeight))
        emptyTableMessageView.layer.cornerRadius = 15
        //emptyTableMessageView.backgroundColor = UIColor(white: 0, alpha: 0.5)
        emptyTableMessageView.backgroundColor = UIColor.lightGray
        
        emptyTableMessageView.addSubview(emptyTableMessageLabel)
        
        tableView.addSubview(emptyTableMessageView)
        tableView.separatorStyle = .none
        tableView.isScrollEnabled = false
    }
    
    open func removeEmptyTableMessage() {
        if let emptyTableSuperView = emptyTableSuperView {
            emptyTableMessageView.removeFromSuperview()
            emptyTableSuperView.separatorStyle = .singleLine
            emptyTableSuperView.isScrollEnabled = true
        }
    }
    
    open func displayEmptyRoomsTableMessage(_ tableView:UITableView, msg:String, width:Int, height:Int) {
        let viewWidth:CGFloat = CGFloat(width)
        let viewHeight:CGFloat = CGFloat(height)
        self.emptyRoomsTableMessageSuperView = tableView
        removeEmptyRoomsTableMessage()
        
        let emptyTableMessageLabel = UILabel(frame: CGRect(x: 10, y: 10, width: viewWidth - 20, height: viewHeight - 20))
        emptyTableMessageLabel.text = msg
        emptyTableMessageLabel.textColor = UIColor.white
        emptyTableMessageLabel.font = UIFont(name: "HelveticaNeue", size: 14.0)
        emptyTableMessageLabel.lineBreakMode = .byWordWrapping
        emptyTableMessageLabel.numberOfLines = 0
        
        emptyRoomsTableMessageView = UIView(frame: CGRect(x: tableView.frame.midX - 100, y: tableView.frame.midY - 30 , width: viewWidth, height: viewHeight))
        emptyRoomsTableMessageView.layer.cornerRadius = 15
        //emptyRoomsTableMessageView.backgroundColor = UIColor(white: 0.5, alpha: 0.5)
        emptyRoomsTableMessageView.backgroundColor = UIColor.lightGray
        
        emptyRoomsTableMessageView.addSubview(emptyTableMessageLabel)
        
        tableView.addSubview(emptyRoomsTableMessageView)
        tableView.separatorStyle = .none
        tableView.isScrollEnabled = false
    }
    
    open func displayEmptyAccessoriesTableMessage(_ tableView:UITableView, msg:String, width:Int, height:Int) {
        let viewWidth:CGFloat = CGFloat(width)
        let viewHeight:CGFloat = CGFloat(height)
        self.emptyAccessoriesTableMessageSuperView = tableView
        removeEmptyAccessoriesTableMessage()
        
        let emptyTableMessageLabel = UILabel(frame: CGRect(x: 10, y: 10, width: viewWidth - 20, height: viewHeight - 20))
        emptyTableMessageLabel.text = msg
        emptyTableMessageLabel.textColor = UIColor.white
        emptyTableMessageLabel.font = UIFont(name: "HelveticaNeue", size: 14.0)
        emptyTableMessageLabel.lineBreakMode = .byWordWrapping
        emptyTableMessageLabel.numberOfLines = 0
        
        emptyAccessoriesTableMessageView = UIView(frame: CGRect(x: tableView.frame.midX - 100, y: 20 , width: viewWidth, height: viewHeight))
        emptyAccessoriesTableMessageView.layer.cornerRadius = 15
        //emptyAccessoriesTableMessageView.backgroundColor = UIColor(white: 0.5, alpha: 0.5)
        emptyAccessoriesTableMessageView.backgroundColor = UIColor.lightGray
        
        emptyAccessoriesTableMessageView.addSubview(emptyTableMessageLabel)
        
        tableView.addSubview(emptyAccessoriesTableMessageView)
        tableView.separatorStyle = .none
        tableView.isScrollEnabled = false
    }
    
    open func removeEmptyRoomsTableMessage() {
        if let emptyRoomsTableMessageSuperView = emptyRoomsTableMessageSuperView {
            emptyRoomsTableMessageView.removeFromSuperview()
            emptyRoomsTableMessageSuperView.separatorStyle = .singleLine
            emptyRoomsTableMessageSuperView.isScrollEnabled = true
            
        }
    }
    
    open func removeEmptyAccessoriesTableMessage() {
        if let emptyAccessoriesTableMessageSuperView = emptyAccessoriesTableMessageSuperView {
            emptyAccessoriesTableMessageView.removeFromSuperview()
            emptyAccessoriesTableMessageSuperView.separatorStyle = .singleLine
            emptyAccessoriesTableMessageSuperView.isScrollEnabled = true
        }
    }
    
    open func displayActivityIndicator(_ view:UIView, msg:String) {
        self.processingSuperView = view
        removeActivityIndicator()
        
        let processingMessageLabel = UILabel(frame: CGRect(x: 5, y: 50, width: 110, height: 50))
        processingMessageLabel.text = msg
        processingMessageLabel.textColor = UIColor.white
        processingMessageLabel.font = UIFont(name: "HelveticaNeue", size: 16.0)
        processingMessageLabel.textAlignment = NSTextAlignment.center
        
        processingActivityIndicator = UIActivityIndicatorView(activityIndicatorStyle: UIActivityIndicatorViewStyle.whiteLarge)
        processingActivityIndicator.frame = CGRect(x: 35, y: 10, width: 50, height: 50)
        processingActivityIndicator.startAnimating()
        
        processingMessageView = UIView(frame: CGRect(x: view.frame.midX - 70, y: view.frame.midY - 150 , width: 120, height: 100))
        processingMessageView.layer.cornerRadius = 15
        processingMessageView.backgroundColor = UIColor(white: 0, alpha: 0.5)
        processingMessageView.addSubview(processingActivityIndicator)
        processingMessageView.addSubview(processingMessageLabel)
        
        view.addSubview(processingMessageView)
    }
    
    open func displayActivityIndicator(_ view:UIView, msg:String, xOffset:Int, yOffset:Int) {
        self.processingSuperView = view
        removeActivityIndicator()
        
        let processingMessageLabel = UILabel(frame: CGRect(x: 5, y: 50, width: 110, height: 50))
        processingMessageLabel.text = msg
        processingMessageLabel.textColor = UIColor.white
        processingMessageLabel.font = UIFont(name: "HelveticaNeue", size: 16.0)
        processingMessageLabel.textAlignment = NSTextAlignment.center
        
        processingActivityIndicator = UIActivityIndicatorView(activityIndicatorStyle: UIActivityIndicatorViewStyle.whiteLarge)
        processingActivityIndicator.frame = CGRect(x: 35, y: 10, width: 50, height: 50)
        processingActivityIndicator.startAnimating()
        
        processingMessageView = UIView(frame: CGRect(x: view.frame.midX + CGFloat(xOffset), y: view.frame.midY + CGFloat(yOffset) , width: 120, height: 100))
        processingMessageView.layer.cornerRadius = 15
        processingMessageView.backgroundColor = UIColor(white: 0, alpha: 0.5)
        processingMessageView.addSubview(processingActivityIndicator)
        processingMessageView.addSubview(processingMessageLabel)
        
        view.addSubview(processingMessageView)
    }

    
    open func removeActivityIndicator() {
        if processingSuperView != nil {
            processingMessageView.removeFromSuperview()
        }
    }
    
    open func showAlert(_ viewController: UIViewController, title: String!, message:String!) {
        let alert = UIAlertController(title: title, message: message, preferredStyle: UIAlertControllerStyle.alert)
        alert.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.default, handler: { action -> Void in
            //Do some stuff
            print("OK pressed")
            self.isAlertVisible = false
        }))
        
        if isAlertVisible == false {
            isAlertVisible = true
            viewController.present(alert, animated: true, completion: nil)
        }
    }
    
    open func getAccessoryCategoryImage(_ category: String) -> UIImage! {
        switch (category) {
            case HMAccessoryCategoryTypeLightbulb:
                return UIImage(named: "CategoryLightbulb")
            case HMAccessoryCategoryTypeDoorLock:
                return UIImage(named: "CategoryLock")
            case HMAccessoryCategoryTypeGarageDoorOpener:
                return UIImage(named: "CategoryGarageDoor")
            case HMAccessoryCategoryTypeSwitch:
                return UIImage(named: "CategorySwitch")
            case HMAccessoryCategoryTypeOutlet:
                return UIImage(named: "CategoryOutlet")
            case HMAccessoryCategoryTypeFan:
                return UIImage(named: "CategoryFan")
                
            default: return UIImage(named: "CategoryNotSupported")
        }
    }
    
}
