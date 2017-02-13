//
//  ViewController.swift
//  BSwiftHeartRate
//
//  Created by Mark Thistle on 2/18/16.
//  Copyright © 2016 NewThistle, LLC. All rights reserved.
//

import UIKit

class ViewController: UIViewController, MSBClientManagerDelegate, UITextViewDelegate {
    
    var tempHR: Double = 0.0
    var tempRR: Double = 0.0
    var tempGSR: Double = 0.0
    var tempSkin: Double = 0.0
    var tempX: Double = 0.0
    var tempY: Double = 0.0
    var tempZ: Double = 0.0
    var tempHRQ: String = ""
    var timeStringHR = ""
    var timeStringGSR = ""
    var timeStringSkin = ""
    var timeStringAcc = ""
    var hrString = ""
    var hrQString = ""
    var rrString = ""
    var gsrString = ""
    var skinString = ""
    var accXString = ""
    var accYString = ""
    var accZString = ""
    var timeArrayHR = [AnyObject]()
    var timeArrayGSR = [AnyObject]()
    var timeArraySkin = [AnyObject]()
    var timeArrayAcc = [AnyObject]()

    var hrArray = [AnyObject]()
    var rrArray = [AnyObject]()
    var hrQArray = [AnyObject]()
    var gsrArray = [AnyObject]()
    var skinArray = [AnyObject]()
    var accXArray = [AnyObject]()
    var accYArray = [AnyObject]()
    var accZArray = [AnyObject]()
    var hrSwitchT: Int = 1
    var skinSwitchT: Int = 1
    var gsrSwitchT: Int = 1
    var accSwitchT: Int = 1

    
    //MARK: Properties
    
    @IBOutlet weak var txtOutput: UITextView!
    @IBOutlet weak var hrLabel: UILabel!
    @IBOutlet weak var rrLabel: UILabel!
    @IBOutlet weak var accLabel: UILabel!
    @IBOutlet weak var startHRSensorButton: UIButton!
    @IBOutlet weak var stopHRSensorButton: UIButton!
    @IBOutlet weak var gsrLabel: UILabel!
    @IBOutlet weak var skinLabel: UILabel!
    @IBOutlet weak var hrSwitch: UISwitch!
    @IBOutlet weak var skinSwitch: UISwitch!
    @IBOutlet weak var gsrSwitch: UISwitch!
    @IBOutlet weak var accSwitch: UISwitch!
    



    
    var client: MSBClient!
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
        if let band = clientManager?.attachedClients().first as! MSBClient! {
            self.client = band
            clientManager?.connect(client)
            output("Please wait... \nConnecting to Band \(client.name!)")
        } else {
            output("Failed! No Bands attached.")
            return
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    
    //MARK: Action

    @IBAction func didTapStartHRSensorButton(_ sender: AnyObject) {
        markSampleReady(false)
        if let client = self.client {
            if client.sensorManager.heartRateUserConsent() == MSBUserConsent.granted {
                
                initializeSensorVariables()
                
                let dateFormatter = DateFormatter()
                dateFormatter.dateFormat = "dd.MM.YY HH:mm:ss"
                output("The records started at:")
                output(dateFormatter.string(from: Date()))
                
                
                startHeartRateUpdates()
                startRRIntervalUpdates()
                startAccUpdates()
                startGsrUpdates()
                startSkinUpdates()
                
                
            } else {
                output("Requesting user consent for accessing HeartRate...")
                client.sensorManager.requestHRUserConsent(completion: { (userConsent: Bool, error: Error?) in
                    if userConsent {
                        self.startHeartRateUpdates()
                        self.startRRIntervalUpdates()
                        self.startAccUpdates()
                        self.startGsrUpdates()
                        self.startSkinUpdates()
                    } else {
                        self.sampleDidCompleteWithOutput("User consent declined.")
                    }
                })

            }
        }
    }

    @IBAction func didTapStopHRSensorButton(_ sender: Any) {
        if let client = self.client{
            if client.sensorManager.heartRateUserConsent() == MSBUserConsent.granted{
                stopHeartRateUpdates()
                stopRRIntervalUpdates()
                stopAccUpdates()
                stopGsrUpdates()
                stopSkinUpdates()
                
                var csv: String = "Time"
                
                if(hrSwitchT == 1){
                    //LogHR()
                    csv += ",HR,RR,Mode"
                    output("LogHR saved")
                }else {
                    output("LogHR NOT saved")
                }
                
                if(gsrSwitchT == 1){
                    //LogGSR()
                    csv += ",GSR"
                    output("LogGSR saved")
                }else {
                    output("LogGSR NOT saved")
                }
                
                if(skinSwitchT == 1){
                    //LogSkin()
                    csv += ",SkinT"
                    output("LogSkin saved")
                } else {
                    output("LogSkin NOT saved")
                }
                
                if(accSwitchT == 1){
                    //LogAcc()
                    csv += ",AccX,AccY,AccZ"
                    output("LogAcc saved")
                } else {
                    output("LogAcc NOT saved")
                }
                
                
                let count: Int = timeArrayHR.count
                output("\(count)")
                for i in 0..<count {
                    csv += "\n\(timeArrayHR[i]),\(hrArray[i]),\(rrArray[i]),\(hrQArray[i]),\(gsrArray[i]),\(skinArray[i]),\(accXArray[i]),\(accYArray[i]),\(accZArray[i])"
                }
                
                let dateFormatter = DateFormatter()
                
                dateFormatter.dateFormat = "dd.MM.YY"
                let fileName = "MSBand2_ALL_data_\(dateFormatter.string(from: Date()))"
                
                //let fileName = "MSBand2_ALL_data_"
 
                let docDirectory = try? FileManager.default.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: true)
                
                if let fileURL = docDirectory?.appendingPathComponent(fileName).appendingPathExtension("csv"){
                    
                    // Write to the file
                    do {
                        try csv.write(to: fileURL, atomically: true, encoding: String.Encoding.utf8)
                    } catch let error as NSError {
                        output("Error \(error.localizedDescription) while writing to file \(csv)")
                    }
                }
                
                
            }
        }
    }
    
    
    @IBAction func HRLogSwitch(_ sender: UISwitch) {
        if hrSwitch.isOn{
            hrSwitchT = 1
            output("Log HR data: ON")
        } else {
            hrSwitchT = 0
            output("Log HR data: OFF")
        }
    }
    
    @IBAction func SkinLogSwitch(_ sender: UISwitch) {
        if skinSwitch.isOn{
            skinSwitchT = 1
            output("Log Skin Temp data: ON")
        } else {
            skinSwitchT = 0
            output("Log Skin Temp data: OFF")
        }
    }
    
    
    @IBAction func GsrLogSwitch(_ sender: UISwitch) {
        if gsrSwitch.isOn{
            gsrSwitchT = 1
            output("Log Gsr data: ON")
        }else{
            gsrSwitchT = 0
            output("Log Gsr data: OFF")
        }
    }
    
    @IBAction func AccLogSwitch(_ sender: UISwitch) {
        if accSwitch.isOn{
            accSwitchT = 1
            output("Log Acc data: ON")
        }else {
            accSwitchT = 0
            output("Log Acc data: OFF")
        }
    }
    
    
    
    //MARK: Function
    
    func startHeartRateUpdates() {
        output("[START] Starting Heart Rate updates")
        if let client = self.client {
            do {
                try client.sensorManager.startHeartRateUpdates(to: nil, withHandler: {(heartRateData: MSBSensorHeartRateData?, error: Error?) in
                    
                    self.hrLabel.text = NSString(format: "Heart Rate: %3u %@",
                                                 heartRateData!.heartRate,
                                                 heartRateData!.quality == MSBSensorHeartRateQuality.acquiring ? "Acquiring" : "Locked") as String;
                
                    self.tempHR = Double(heartRateData!.heartRate)
                    
                    if (heartRateData!.quality == MSBSensorHeartRateQuality.acquiring){
                        self.tempHRQ = "Acquiring"
                    }else{
                        self.tempHRQ = "Locked"
                    }
                    })

        
            } catch let error as NSError {
                output("startHeartRateUpdatesToQueue failed: \(error.description)")
            }
        } else {
            output("Client not connected, can not start heart rate updates")
        }
    }
    
    func stopHeartRateUpdates() {
        output("[ACTION] Stopping Heart Rate ...")
        if let client = self.client {
            do {
                try client.sensorManager.stopHeartRateUpdatesErrorRef()
            } catch let error as NSError {
                output("stopHeartRateUpdatesErrorRef failed: \(error.description)")
            }
            sampleDidCompleteWithOutput("[STOP] Heart Rate updates stopped")
        }
    }
    
    func startRRIntervalUpdates(){
        output("[START] Starting RR Interval updates")
        if let client = self.client{
            do{
                try client.sensorManager.startRRIntervalUpdates(to: nil, withHandler: {(rrData: MSBSensorRRIntervalData?, error: Error?) in
                    
                    self.rrLabel.text = NSString(format: "RR Interval: %.2f second",
                                                 rrData!.interval) as String;
                    self.tempRR = Double(rrData!.interval)
                    self.registerDataHR()
                    self.registerDataAcc()
                    self.registerDataGSR()
                    self.registerDataSkin()
                
                    })
            } catch let error as NSError {
                output("startRRUpdatesToQueue failed: \(error.description)")
            }
        } else {
            output("Client not connect, can not start RR updates")
        }
    }
    
    func stopRRIntervalUpdates(){
        output("[ACTION] Stopping RR Interval...")
        if let client = self.client{
            do{
                try client.sensorManager.stopRRIntervalUpdatesErrorRef()
            } catch let error as NSError {
                output("stopRRUpdatesErrorRef failed: \(error.description)")
            }
            sampleDidCompleteWithOutput("[STOP] RR updates stopped")
        }
    }
    
    func startAccUpdates(){
        output("[START] Starting Acc updates")
        if let client = self.client {
            do{
                try client.sensorManager.startAccelerometerUpdates(to: nil, withHandler: {(accData: MSBSensorAccelerometerData?, error : Error?)in
                    
                    self.accLabel.text = NSString(format: "Acc:  X = %5.2f, Y = %5.2f, Z = %5.2f (g)",
                                                 accData!.x,
                                                 accData!.y,
                                                 accData!.z) as String;
                    self.tempX = Double(accData!.x)
                    self.tempY = Double(accData!.y)
                    self.tempZ = Double(accData!.z)
                    //self.registerDataAcc()
                })
            } catch let error as NSError {
                output("startAccUpdatesToQueue failed: \(error.description)")
            }
        }else{
            output("Client not connect, can not start Acc updates")
        }
    }
    
    func stopAccUpdates(){
        output("[ACTION] Stopping Acc")
        if let client = self.client{
            do{
                try client.sensorManager.stopAccelerometerUpdatesErrorRef()
            }   catch let error as NSError {
                output("stopAccUpdatesError Ref failed: \(error.description)")
            }
            sampleDidCompleteWithOutput("[STOP] Acc updates stopped")
        }
    }
    
    func startGsrUpdates(){
        output("[START] Starting Gsr updates")
        if let client = self.client {
            do{
                try client.sensorManager.startGSRUpdates(to: nil, withHandler: {(gsrData:
                    MSBSensorGSRData?, error: Error?)in
                    
                    self.gsrLabel.text = NSString(format: "Gsr: %8u kOhm", gsrData!.resistance) as String;
                    self.tempGSR = Double(gsrData!.resistance)
                    //self.registerDataGSR()
                })
            } catch let error as NSError {
                output("startGsrUpdatesToQueue failed: \(error.description)")
            }
        } else {
            output("Client not connect, can not start Gsr Updates")
        }
    }
    
    func stopGsrUpdates(){
        output("[ACTION] Stopping Gsr...")
        if let client = self.client{
            do{
                try client.sensorManager.stopGSRUpdatesErrorRef()
            } catch let error as NSError {
                output("stopGsrUpdatesError Ref failed: \(error.description)")
            }
            sampleDidCompleteWithOutput("[STOP] Gsr updates stopped")
        }
    }
    
    func startSkinUpdates(){
        output("[START] Starting Skin updates")
        if let client = self.client{
            do{
                try client.sensorManager.startSkinTempUpdates(to: nil, withHandler: {(skinData:
                    MSBSensorSkinTemperatureData?, error: Error?)in
                    self.skinLabel.text = NSString(format: "Skin temp: %.3f degree C", skinData!.temperature) as String;
                    self.tempSkin = Double(skinData!.temperature)
                    //self.output("one \n")
                    //self.registerDataSkin()
                })
            } catch let error as NSError {
                output("stopSkinUpdatesToQueue failed: \(error.description)")
            }
        }else {
            output("Client not connect, can not start Skin Temp Updates")
        }
    }
    
    func stopSkinUpdates(){
        output("[ACTION] Stopping Skin Temp...")
        if let client = self.client{
            do{
                try client.sensorManager.stopSkinTempUpdatesErrorRef()
            } catch let error as NSError {
                output("stopSkinUpdatesError Ref failed: \(error.description)")
            }
            sampleDidCompleteWithOutput("[STOP] Skin Temp updates stopped")
        }
    }
    
    func initializeSensorVariables() {
        timeStringHR = String()
        timeStringAcc = String()
        timeStringGSR = String()
        timeStringSkin = String()
        
        hrString = String()
        hrQString = String()
        rrString = String()
        gsrString = String()
        skinString = String()
        accXString = String()
        accYString = String()
        accZString = String()
        hrQArray = [Any]() as [AnyObject]
        timeArrayHR = [Any]() as [AnyObject]
        timeArrayGSR = [Any]() as [AnyObject]
        timeArraySkin = [Any]() as [AnyObject]
        timeArrayAcc = [Any]() as [AnyObject]
        
        
        hrArray = [Any]() as [AnyObject]
        rrArray = [Any]() as [AnyObject]
        gsrArray = [Any]() as [AnyObject]
        skinArray = [Any]() as [AnyObject]
        accXArray = [Any]() as [AnyObject]
        accYArray = [Any]() as [AnyObject]
        accZArray = [Any]() as [AnyObject]
        tempHR = 0
        tempRR = 0
        tempGSR = 0
        tempSkin = 0
        tempX = 0
        tempY = 0
        tempZ = 0
        //tempCounter = 0
        //frequencyGSR = 0
    }
    
    
    func registerDataHR() {
        // Transform to string to save it to array
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "dd/MM/YY HH:mm:ss.SSS"
        timeStringHR = dateFormatter.string(from: Date())
        
        hrString = String(format: "%3f", tempHR)
        rrString = String(format: "%3f", tempRR)
        hrQString = tempHRQ
    
        // Add to array
        timeArrayHR.append(timeStringHR as AnyObject)
        
        rrArray.append(rrString as AnyObject)
        hrArray.append(hrString as AnyObject)
        hrQArray.append(hrQString as AnyObject)
    }
    
    func registerDataGSR(){
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "dd.MM.YY HH:mm:ss.SSS"
        timeStringGSR = dateFormatter.string(from: Date())
        
        timeArrayGSR.append(timeStringGSR as AnyObject)
        gsrString = String(format: "%.3f", tempGSR)
        gsrArray.append(gsrString as  AnyObject)
    }
    
    func registerDataSkin(){
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "dd.MM.YY HH:mm:ss.SSS"
        timeStringSkin = dateFormatter.string(from: Date())
        
        timeArraySkin.append(timeStringSkin as AnyObject)
        skinString = String(format: "%.3f", tempSkin)
        skinArray.append(skinString as AnyObject)
    }
    
    func registerDataAcc(){
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "dd.MM.YY HH:mm:ss.SSS"
        timeStringAcc = dateFormatter.string(from: Date())
        
        timeArrayAcc.append(timeStringAcc as AnyObject)
        accXString = String(format: "%.3f", tempX)
        accYString = String(format: "%.3f", tempY)
        accZString = String(format: "%.3f", tempZ)
        
        accXArray.append(accXString as AnyObject)
        accYArray.append(accYString as AnyObject)
        accZArray.append(accZString as AnyObject)
    }
    
    func LogHR(){
        var csv: String = "Time,HR,RR,Mode"
        let count: Int = timeArrayHR.count
        output("\(count)")
        for i in 0..<count {
            csv += "\n\(timeArrayHR[i]),\(hrArray[i]),\(rrArray[i]),\(hrQArray[i])"
        }
        
        let dateFormatter = DateFormatter()
        
        dateFormatter.dateFormat = "dd/MM/YY HH:mm:ss"
        let fileName = "MSBand2_HR_data_\(dateFormatter.string(from: Date()))"
        
        let docDirectory = try? FileManager.default.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: true)
        
        if let fileURL = docDirectory?.appendingPathComponent(fileName).appendingPathExtension("csv"){
            
            // Write to the file
            do {
                try csv.write(to: fileURL, atomically: true, encoding: String.Encoding.utf8)
            } catch let error as NSError {
                output("Error \(error.localizedDescription) while writing to file \(csv)")
            }
        }
    }
    
    func LogGSR(){
        var csv: String = "Time,GSR"
        let count: Int = timeArrayGSR.count
        output("\(count)")
        for i in 0..<count {
            csv += "\n\(timeArrayGSR[i]),\(gsrArray[i])"
        }
        
        let dateFormatter = DateFormatter()
        
        dateFormatter.dateFormat = "dd/MM/YY HH:mm:ss"
        let fileName = "MSBand2_GSR_data_\(dateFormatter.string(from: Date()))"
        
        let docDirectory = try? FileManager.default.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: true)
        
        if let fileURL = docDirectory?.appendingPathComponent(fileName).appendingPathExtension("csv"){
            
            // Write to the file
            do {
                try csv.write(to: fileURL, atomically: true, encoding: String.Encoding.utf8)
            } catch let error as NSError {
                output("Error \(error.localizedDescription) while writing to file \(csv)")
            }
        }
    }
    
    
    func LogSkin(){
        var csv: String = "Time,Skin Temperature"
        let count: Int = timeArraySkin.count
        output("\(count)")
        for i in 0..<count {
            csv += "\n\(timeArraySkin[i]),\(skinArray[i])"
        }
        
        let dateFormatter = DateFormatter()
        
        dateFormatter.dateFormat = "dd/MM/YY HH:mm:ss"
        let fileName = "MSBand2_SkinTemp_data_\(dateFormatter.string(from: Date()))"
        
        let docDirectory = try? FileManager.default.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: true)
        
        if let fileURL = docDirectory?.appendingPathComponent(fileName).appendingPathExtension("csv"){
            
            // Write to the file
            do {
                try csv.write(to: fileURL, atomically: true, encoding: String.Encoding.utf8)
            } catch let error as NSError {
                output("Error \(error.localizedDescription) while writing to file \(csv)")
            }
        }
    }
    
    func LogAcc(){
        var csv: String = "Time, X, Y, Z"
        let count: Int = timeArrayAcc.count
        output("\(count)")
        for i in 0..<count {
            csv += "\n\(timeArrayAcc[i]),\(accXArray[i]),\(accYArray[i]), \(accZArray[i])"
        }
        
        let dateFormatter = DateFormatter()
        
        dateFormatter.dateFormat = "dd/MM/YY HH:mm:ss"
        let fileName = "MSBand2_Acc_data_\(dateFormatter.string(from: Date()))"
        
        let docDirectory = try? FileManager.default.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: true)
        
        if let fileURL = docDirectory?.appendingPathComponent(fileName).appendingPathExtension("csv"){
            
            // Write to the file
            do {
                try csv.write(to: fileURL, atomically: true, encoding: String.Encoding.utf8)
            } catch let error as NSError {
                output("Error \(error.localizedDescription) while writing to file \(csv)")
            }
        }
    }
    
    
    
    // MARK: Helper methods
    func sampleDidCompleteWithOutput(_ output: String) {
        self.output(output)
        markSampleReady(true)
    }
    
    func markSampleReady(_ ready: Bool) {
        self.startHRSensorButton.isEnabled = ready
        self.startHRSensorButton.alpha = ready ? 1.0 : 0.2
        self.stopHRSensorButton.isEnabled = !ready
        self.stopHRSensorButton.alpha = ready ? 0.2 : 1.0
    }
    
    func output(_ message: String) {
        self.txtOutput.text = String("\(self.txtOutput.text!)\n\(message)")
        self.txtOutput.layoutIfNeeded()
        if (self.txtOutput.text.lengthOfBytes(using: String.Encoding.utf8) > 0) {
            self.txtOutput.scrollRangeToVisible(NSRange.init(location: self.txtOutput.text.lengthOfBytes(using: String.Encoding.utf8) - 1, length: 1))
        }
    }
    
    // MARK: UITextViewDelegate
    func textViewShouldBeginEditing(_ textView: UITextView) -> Bool {
        return false
    }
    
    // MARK: MSBClientManagerDelegate
    func clientManager(_ clientManager: MSBClientManager?, clientDidConnect client: MSBClient!) {
        markSampleReady(true)
        output("Band \(client.name!) connected.")
    }
    
    func clientManager(_ clientManager: MSBClientManager?, clientDidDisconnect client: MSBClient!) {
        markSampleReady(false)
        output(")Band \(client.name!) disconnected.")
    }
    
    func clientManager(_ clientManager: MSBClientManager?, client: MSBClient!, didFailToConnectWithError error: Error!) {
        output("Failed to connect to Band \(client.name!).")
        output((error! as NSError).description)
    }

}

