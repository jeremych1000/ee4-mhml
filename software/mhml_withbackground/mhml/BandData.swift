//
//  BandData.swift
//  mhml
//
//  Created by Nathalie Wong on 13/2/2017.
//  Copyright © 2017 Nathalie Wong. All rights reserved.
//


import UIKit
import Alamofire


class BandData: UIViewController, UITextViewDelegate, MSBClientManagerDelegate {
    
    
    var globalCounter = 0
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
    
    var jsonString = ""
    //testing
    var buffer: Int = 0
    
    //MARK: Properties
    
    
    
    @IBOutlet weak var gsrLabel: UILabel!
    @IBOutlet weak var accLabel: UILabel!
    @IBOutlet weak var skinLabel: UILabel!
    @IBOutlet weak var rrLabel: UILabel!
    @IBOutlet weak var sleepLabel: UILabel!
    
    @IBOutlet weak var hrLabel: UILabel!
    @IBOutlet weak var txtOutput: UITextView!
    @IBOutlet weak var startHRSensorButton: UIButton!
    @IBOutlet weak var stopHRSensorButton: UIButton!
    @IBOutlet weak var hrSwitch: UISwitch!
    @IBOutlet weak var skinSwitch: UISwitch!
    @IBOutlet weak var accSwitch: UISwitch!
    
    @IBOutlet weak var gsrSwitch: UISwitch!
    
    @IBOutlet weak var goodbadSwitch: UISwitch!
    
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
        
        // Setup background thread for upload data
        
        /*
         beginBackgroundTask(expirationHandler:)
         let backgroundQueue = DispatchQueue(label: "com.app.queue", attributes: .concurrent)
         DispatchQueue.global().async {
         while true {
         print("dispatched to background queue")
         }
         }
         */
        
        //
        //        //TESTING TESTING TESING
        //        backgroundTask = application.beginBackgroundTaskWithName("MyBackgroundTask") {
        //            // This expirationHandler is called when your task expired
        //            // Cleanup the task here, remove objects from memory, etc
        //
        //            application.endBackgroundTask(self.backgroundTask)
        //            self.backgroundTask = UIBackgroundTaskInvalid
        //        }
        //
        //        // Implement the operation of your task as background task
        //        dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0)) {
        //            // Begin your upload and clean up JSON
        //            // NSURLSession, AlamoFire, etc
        //                print("dispatched to background queue")
        //            // On completion, end your task
        //            application.endBackgroundTask(self.backgroundTask)
        //            self.backgroundTask = UIBackgroundTaskInvalid
        //        }
        
        
        
        
        
        
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
    
    @IBAction func didTapStartHRSensorButton(_ sender: Any) {
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
                
                csv += ",outcome"
                
                let count: Int = timeArrayHR.count
                output("\(count)")
                for i in 0..<count {
                    csv += "\n\(timeArrayHR[i]),\(hrArray[i]),\(rrArray[i]),\(hrQArray[i]),\(gsrArray[i]),\(skinArray[i]),\(accXArray[i]),\(accYArray[i]),\(accZArray[i])"
                    if(goodbadSwitch.isOn){
                        csv+=",1"
                    } else {
                        csv+=",0"
                    }
                    
                }
                
                let dateFormatter = DateFormatter()
                
                dateFormatter.dateFormat = "dd_MM_YY"
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
                    
                    
                    /* Upload Data */
                    /* http://sleepify.zapto,org/ml/upload */
                    
                    let sessionManager = Alamofire.SessionManager.default
                    sessionManager.request("http://sleepify.zapto.org/personal/blank/",method:.get)
                        .responseString { response in
                            if let headerFields = response.response?.allHeaderFields as? [String: String],
                                let URL = response.response?.url {
                                let csrf_token = headerFields["Set-Cookie"]!
                                let cookies = HTTPCookie.cookies(withResponseHeaderFields: headerFields, for: URL)
                                
                                let startIndex = csrf_token.index(csrf_token.startIndex, offsetBy:10)
                                let endIndex = csrf_token.index(csrf_token.startIndex, offsetBy: 73)
                                
                                let v = csrf_token[startIndex...endIndex]
                                
                                let headers: HTTPHeaders = [
                                    "X-CSRFToken": v
                                ]
                                Alamofire.SessionManager.default.session.configuration.httpCookieStorage?.setCookie(cookies.first!)
                                
                                Alamofire.upload(
                                    multipartFormData: { multipartFormData in
                                        multipartFormData.append(fileURL, withName: "file")
                                },
                                    to: "http://sleepify.zapto.org/ml/upload/", headers: headers,
                                    encodingCompletion: { encodingResult in
                                        switch encodingResult {
                                        case .success(let upload, _, _):
                                            upload.responseJSON { response in
                                                debugPrint(response)
                                                self.output("Uploaded")
                                            }
                                        case .failure(let encodingError):
                                            print(encodingError)
                                        }
                                })
                            }
                    }
                    //Session Manager
                    
                }
            }
        }
    }
    
    
    @IBAction func HRlogSwitch(_ sender: UISwitch) {
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
                    
                    
                    
                    self.buffer = self.buffer + 1
                    
                    if self.buffer == 600 {
                        self.buffer = 0
                        self.globalCounter += 1
                        self.output("buffer full")
                        self.output("\(self.globalCounter)")
                        
                        
                        var parameters : Parameters = [
                            "username" : "tszho",
                            "data" : [Parameters]()
                        ]
                        
                        var data = [Parameters]()
                        var datat: Parameters = [:]
                        let count: Int = self.timeArrayHR.count
                        print(count)
                        for i  in 0..<count{
                            
                            datat.updateValue("\(self.timeArrayHR[i])", forKey: "timestamp")
                            datat.updateValue("\(self.hrArray[i])", forKey:  "HR")
                            datat.updateValue("\(self.rrArray[i])", forKey: "RR")
                            datat.updateValue("\(self.hrQArray[i])", forKey: "mode")
                            datat.updateValue("\(self.gsrArray[i])", forKey: "GSR")
                            datat.updateValue("\(self.skinArray[i])", forKey: "SkinT")
                            datat.updateValue("\(self.accXArray[i])", forKey: "AccX")
                            datat.updateValue("\(self.accYArray[i])", forKey: "AccY")
                            datat.updateValue("\(self.accZArray[i])", forKey: "AccZ")
                            datat.updateValue("1", forKey: "outcome")
                            
                            
                            data.append(datat)
                        }
                        
                        parameters["data"] = data
                        
                        print(data)
                        
                        Alamofire.request("http://sleepify.zapto.org/api/raw_data/", method: .post, parameters: parameters, encoding: JSONEncoding.default)
                        
                        self.resetArray()
                        
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
                    self.registerDataGSR()
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
    
    func resetArray(){
        hrQArray.removeAll()
        timeArrayHR.removeAll()
        timeArrayGSR.removeAll()
        timeArraySkin.removeAll()
        timeArrayAcc.removeAll()
        hrArray.removeAll()
        rrArray.removeAll()
        gsrArray.removeAll()
        skinArray.removeAll()
        accXArray.removeAll()
        accYArray.removeAll()
        accZArray.removeAll()
    }
    
    
    func registerDataHR() {
        // Transform to string to save it to array
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "dd/MM/YY HH:mm:ss"
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
        dateFormatter.dateFormat = "dd.MM.YY HH:mm:ss"
        timeStringGSR = dateFormatter.string(from: Date())
        
        timeArrayGSR.append(timeStringGSR as AnyObject)
        gsrString = String(format: "%.3f", tempGSR)
        gsrArray.append(gsrString as  AnyObject)
    }
    
    func registerDataSkin(){
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "dd.MM.YY HH:mm:ss"
        timeStringSkin = dateFormatter.string(from: Date())
        
        timeArraySkin.append(timeStringSkin as AnyObject)
        skinString = String(format: "%.3f", tempSkin)
        skinArray.append(skinString as AnyObject)
    }
    
    func registerDataAcc(){
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "dd.MM.YY HH:mm:ss"
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
    
    
    /*func appendIfDictionary(key:String, value: String){
     if var dict = self.dictionary{
     dict[key] = value;
     self = String(dict);
     }
     }*/
    
    
    
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

