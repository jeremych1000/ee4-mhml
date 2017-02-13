//
//  ViewController.swift
//  BSwiftHeartRate
//
//  Created by Mark Thistle on 2/18/16.
//  Copyright © 2016 NewThistle, LLC. All rights reserved.
//

import UIKit

class ViewController: UIViewController, MSBClientManagerDelegate, UITextViewDelegate {
    
    @IBOutlet weak var txtOutput: UITextView!
    @IBOutlet weak var hrLabel: UILabel!
    @IBOutlet weak var startHRSensorButton: UIButton!
    var client: MSBClient?
    fileprivate var clientManager = MSBClientManager.shared()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        // Setup View
        markSampleReady(false)
        self.txtOutput.delegate = self
        var insets = txtOutput!.textContainerInset
        insets.top = 20
        insets.bottom = 60
        txtOutput.textContainerInset = insets
        
        // Setup Band
        clientManager?.delegate = self
        if let band = clientManager?.attachedClients().first as! MSBClient? {
            self.client = band
            clientManager?.connect(client)
            output("Please wait. Connecting to Band <\(client!.name)>")
        } else {
            output("Failed! No Bands attached.")
            return
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


    @IBAction func didTapStartHRSensorButton(_ sender: AnyObject) {
        markSampleReady(false)
        if let client = self.client {
            if client.sensorManager.heartRateUserConsent() == MSBUserConsent.granted {
                startHeartRateUpdates()
            } else {
                output("Requesting user consent for accessing HeartRate...")
                //client.sensorManager.requestHRUserConsent( completion: { (userConsent: Bool, error: Error?) -> Void in
               
                
                client.sensorManager.requestHRUserConsent(completion: { (userConsent: Bool, error: Error?) in
                    if userConsent {
                        self.startHeartRateUpdates()
                    } else {
                        self.sampleDidCompleteWithOutput("User consent declined.")
                    }
                })
                
                    //if userConsent {
                    //    self.startHeartRateUpdates()
                    //} else {
                    //    self.sampleDidCompleteWithOutput("User consent declined.")
                    //}
                //})
            }
        }
    }

    
    func startHeartRateUpdates() {
        output("Starting Heart Rate updates...")
        if let client = self.client {
            do {
                try client.sensorManager.startHeartRateUpdates(to: nil, withHandler: {(heartRateData: MSBSensorHeartRateData?, error: Error?) in
                    
                    self.hrLabel.text = NSString(format: "Heart Rate: %3u %@",
                                                 heartRateData!.heartRate,
                                                 heartRateData!.quality == MSBSensorHeartRateQuality.acquiring ? "Acquiring" : "Locked") as String})
                self.perform(#selector(ViewController.stopHeartRateUpdates), with: nil, afterDelay: 60)
            } catch let error as NSError {
                output("startHeartRateUpdatesToQueue failed: \(error.description)")
            }
        } else {
            output("Client not connected, can not start heart rate updates")
        }
    }
    
    func stopHeartRateUpdates() {
        if let client = self.client {
            do {
                try client.sensorManager.stopHeartRateUpdatesErrorRef()
            } catch let error as NSError {
                output("stopHeartRateUpdatesErrorRef failed: \(error.description)")
            }
            sampleDidCompleteWithOutput("Heart Rate updates stopped...")
        }
    }
    
    // MARK - Helper methods
    func sampleDidCompleteWithOutput(_ output: String) {
        self.output(output)
        markSampleReady(true)
    }
    
    func markSampleReady(_ ready: Bool) {
        self.startHRSensorButton.isEnabled = ready
        self.startHRSensorButton.alpha = ready ? 1.0 : 0.2
    }
    
    func output(_ message: String) {
        self.txtOutput.text = String("\(self.txtOutput.text)\n\(message)")
        self.txtOutput.layoutIfNeeded()
        if (self.txtOutput.text.lengthOfBytes(using: String.Encoding.utf8) > 0) {
            self.txtOutput.scrollRangeToVisible(NSRange.init(location: self.txtOutput.text.lengthOfBytes(using: String.Encoding.utf8) - 1, length: 1))
        }
    }
    
    // MARK - UITextViewDelegate
    func textViewShouldBeginEditing(_ textView: UITextView) -> Bool {
        return false
    }
    
    // MARK - MSBClientManagerDelegate
    func clientManager(_ clientManager: MSBClientManager!, clientDidConnect client: MSBClient!) {
        markSampleReady(true)
        output("Band <\(client.name)>connected.")
    }
    
    func clientManager(_ clientManager: MSBClientManager!, clientDidDisconnect client: MSBClient!) {
        markSampleReady(false)
        output(")Band <\(client.name)>disconnected.")
    }
    
    //func clientManager(_ clientManager: MSBClientManager!, client: MSBClient!, didFailToConnectWithError error: NSError!) {
    //    output("Failed to connect to Band <\(client.name)>.")
    //    output(error.description)
    //}
    
    func clientManager(_ clientManager: MSBClientManager!, client: MSBClient!, didFailToConnectWithError error: Error!) {
        output("Failed to connect to Band <\(client.name)>.")
        output((error! as NSError).description)
        //output(error.description)
    }

}

