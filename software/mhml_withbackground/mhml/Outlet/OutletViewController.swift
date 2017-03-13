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

class OutletViewController: UIViewController {
    
    var outletAccessoryName: String!
    var isOutletServiceFound:Bool = false
    var isAlertVisible:Bool = false
    var isViewAppeared = true
    var activityTimer = Timer()
    var outletInstance:Outlet = Outlet.sharedInstance
    
    override func viewDidLoad() {
        super.viewDidLoad()
        disableOutletControls()
        outletInstance.delegate = self
    }
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        stopActivityAnimation()
        isViewAppeared = false
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        print("viewWillAppear")
        isViewAppeared = true
    }


    @IBOutlet weak var outletTitle: UILabel!
    @IBOutlet weak var outletStateSegmentedControl: UISegmentedControl!
    @IBOutlet weak var outletInUseValue: UILabel!
    
    @IBAction func outletStateChanged(_ sender: UISegmentedControl) {
        outletStateSegmentedControl.isEnabled = false        
        if outletInstance.isAccessoryConnected() {
            print("\(outletAccessoryName) is reachable")
            if outletStateSegmentedControl.selectedSegmentIndex == 0 {

            }
            else  {
            }
            outletInstance.writeToPowerState(outletStateSegmentedControl.selectedSegmentIndex)
        }
        else {
            print("\(outletAccessoryName) is not reachable")
            clearOutlet()
        }

    }
    
    
    func addNewAccessory(_ accessory: HMAccessory?) {
        if let accessory = accessory {
            self.startActivityAnimation("Connecting")
            outletAccessoryName = accessory.name
            outletInstance.selectedAccessory(accessory)
            outletInstance.discoverServicesAndCharacteristics()
        }
    }
    
    func clearOutlet() {
        outletAccessoryName = nil
        outletTitle.textColor = UIColor(red: 170.0/255.0, green: 171.0/255.0, blue: 175.0/255.0, alpha: 1.0)
        outletTitle.text = "Device Name"
        outletInUseValue.text = "-"
        isOutletServiceFound = false
        disableOutletControls()        
    }
    
    func enableOutletControls() {
        outletStateSegmentedControl.isEnabled = true
    }
    
    func disableOutletControls() {
        self.stopActivityAnimation()
        outletStateSegmentedControl.isEnabled = false
    }
    
    func startActivityAnimation(_ message: String) {
        // 20 seconds timeout
        let delayInSeconds = 20.0
        activityTimer = Timer.scheduledTimer(timeInterval: delayInSeconds, target: self, selector: #selector(OutletViewController.processingTimeout), userInfo: nil, repeats: false)
    }
    
    func stopActivityAnimation() {
        stopTimer()
    }
    
    func processingTimeout() {
        self.stopActivityAnimation()
        self.showAlert("Time out!. Please Select Device again")
    }
    
    func stopTimer() {
        activityTimer.invalidate()
    }
    
    func showAlert(_ message: String) {
        if isViewAppeared {
        }
    }
    
    // MARK: - Navigation
    
    // In a storyboard-based application, you will often want to do a little preparation before navigation
    /*override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "scan" {
            let navigationController = segue.destination as! UINavigationController
            let scanVC = navigationController.topViewController as! SelectAccessoryTableViewController
            scanVC.delegate = self
            scanVC.logMessages = self.logMessages
        }
        else if segue.identifier == "log" {
            let logVC = segue.destination as! LogTableViewController
            logVC.logMessages = self.logMessages
        }
    }*/
    
}



extension OutletViewController: OutletProtocol {
    
    func didReceiveState(_ value: Int) {
        print("didReceiveState \(value)")
        if value == 0 {
        }
        else  {
        }
        enableOutletControls()
        stopActivityAnimation()
        outletStateSegmentedControl.selectedSegmentIndex = value
    }
    
    func didReceiveInUse(_ value: Int) {
        print("didReceiveInUse \(value)")
        if value == 0 {
            outletInUseValue.text = "NO"
        }
        else  {
            outletInUseValue.text = "YES"
        }
    }
    
    func didStateChanged(_ state: Int) {
        print("didStateChanged \(state)")
        if state == 0 {
        }
        else  {
        }
        outletStateSegmentedControl.isEnabled = true
        self.stopActivityAnimation()
    }
    
    func didFoundServiceAndCharacteristics(_ isAllFound: Bool) {
        print("didFoundServiceAndCharacteristics: \(isAllFound)")
        if isAllFound == true {
            outletTitle.textColor = UIColor.black
            outletTitle.text = outletAccessoryName
            isOutletServiceFound = true
            outletInstance.readValues()
        }
        else {
            clearOutlet()
            showAlert("Accessory is not Outlet")
        }
    }
    
    func didReceiveLogMessage(_ message: String) {
        print("didReceiveLogMessage: \(message)")
    }
    
    func didReceiveErrorMessage(_ message: String) {
        print("didReceiveErrorMessage: \(message)")
        self.showAlert(message)
        clearOutlet()
    }
    
    func didReceiveAccessoryReachabilityUpdate(_ accessory:HMAccessory!) {
        print("didReceiveAccessoryReachabilityUpdate: \(accessory)")
        addNewAccessory(accessory)
    }

}

/*
 extension OutletViewController: SelectAccessaryDelegate {
    func selectedAccessary(_ accessary: HMAccessory!) {
        print("selectedAccessary \(accessary.name)")
        self.logMessages.addLogText("selectedAccessary: \(accessary.name)")
        clearOutlet()
        //this delegate is called before viewWillAppear() therefore setting this flag here
        //otherwise Alert box will not appear
        isViewAppeared = true
        addNewAccessory(accessary)
    }
}
*/
