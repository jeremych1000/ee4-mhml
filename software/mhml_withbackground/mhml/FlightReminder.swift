//
//  FlightReminder.swift
//  mhml
//
//  Created by Nathalie Wong on 9/2/2017.
//  Copyright © 2017 Nathalie Wong. All rights reserved.
//
//  Secondary features

import UIKit
import EventKit

class FlightReminder: UIViewController {
    

    @IBOutlet weak var reminderText: UITextField!

    @IBOutlet weak var myDatePicker: UIDatePicker!
  
    
    @IBOutlet weak var setRe: UIButton!
    
    
    let appDelegate = UIApplication.shared.delegate
        as! AppDelegate
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        setRe.layer.cornerRadius = 8
        self.myDatePicker.setValue(UIColor.white, forKey: "textColor")
        // Do any additional setup after loading the view.
    }
    

    @IBAction func setReminder(_ sender: Any) {
    
    if appDelegate.eventStore == nil {
    appDelegate.eventStore = EKEventStore()
    
    appDelegate.eventStore?.requestAccess(
    to: EKEntityType.reminder, completion: {(granted, error) in
    if !granted {
    print("Access to store not granted")
    print(error?.localizedDescription)
    } else {
    print("Access granted")
    }
    })
    }
    
    if (appDelegate.eventStore != nil) {
    self.createReminder()
    }
    }
    
    func createReminder() {
        
        let reminder = EKReminder(eventStore: appDelegate.eventStore!)
        
        reminder.title = reminderText.text!
        reminder.calendar =
            appDelegate.eventStore!.defaultCalendarForNewReminders()
        let date = myDatePicker.date
        let alarm = EKAlarm(absoluteDate: date)
        
        reminder.addAlarm(alarm)
        
        do {
            try appDelegate.eventStore?.save(reminder,
                                             commit: true)
        } catch let error {
            print("Reminder failed with error \(error.localizedDescription)")
        }
    }
    
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        reminderText.endEditing(true)
    }
    
}
