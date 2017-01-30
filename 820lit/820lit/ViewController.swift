//
//  ViewController.swift
//  820lit
//
//  Created by Stiven Deleur on 1/28/17.
//  Copyright © 2017 Stiven Deleur. All rights reserved.
//

import UIKit
import FirebaseDatabase

class ViewController: UIViewController, UIPickerViewDataSource, UIPickerViewDelegate {

    var ref: FIRDatabaseReference!
    var refHandle: UInt!
    
    @IBOutlet weak var patternPicker: UIPickerView!
    @IBOutlet weak var displayPicker: UIPickerView!
    @IBOutlet weak var onSwitch: UISwitch!
    @IBOutlet weak var rSlider: UISlider!
    @IBOutlet weak var gSlider: UISlider!
    @IBOutlet weak var bSlider: UISlider!
    @IBOutlet weak var wSlider: UISlider!
    @IBOutlet weak var brightnessSlider: UISlider!
    @IBOutlet weak var cycleSpeedSlider: UISlider!
    @IBOutlet weak var fadeSlider: UISlider!
    @IBOutlet weak var cutoffSlider: UISlider!
    @IBOutlet weak var dimCenterSwitch: UISwitch!
    @IBOutlet weak var brightEdgesSwitch: UISwitch!
    var lockUI = false

    var patterns = ["Single Color", "Rainbow", "Random", "Random Bright", "Grayscale", "USC", "Mood Lighting"]
    var displayTypes = ["Fill", "Middle Out", "Middle Out Fill", "Strobe", "Cycle", "Middle Out White"]
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        ref = FIRDatabase.database().reference()
        refHandle = ref.observe(FIRDataEventType.value, with: { (snapshot) in
            let postDict = snapshot.value as? [String : AnyObject] ?? [:]
            if self.lockUI{ return}
            self.patternPicker.selectRow(postDict["PatternID"] as! Int, inComponent: 0, animated: true)
            self.displayPicker.selectRow(postDict["DisplayID"] as! Int, inComponent: 0, animated: true)
            self.onSwitch.setOn(postDict["on"] as! Int == 1, animated: true)
            if Int(self.rSlider.value) != postDict["R"] as! Int{
                self.rSlider.setValue(postDict["R"] as! Float, animated: true)
            }
            if Int(self.gSlider.value) != postDict["G"] as! Int{
                self.gSlider.setValue(postDict["G"] as! Float, animated: true)
            }
            if Int(self.bSlider.value) != postDict["B"] as! Int{
                self.bSlider.setValue(postDict["B"] as! Float, animated: true)
            }
            if Int(self.wSlider.value) != postDict["W"] as! Int{
                self.wSlider.setValue(postDict["W"] as! Float, animated: true)
            }
            if Int(self.brightnessSlider.value) != postDict["brightness"] as! Int{
                self.brightnessSlider.setValue(postDict["brightness"] as! Float, animated: true)
            }
            if Int(self.cycleSpeedSlider.value) != postDict["cycleSpeed"] as! Int{
                self.cycleSpeedSlider.setValue(postDict["cycleSpeed"] as! Float, animated: true)
            }
            if self.fadeSlider.value != postDict["fade"] as! Float{
                self.fadeSlider.setValue(postDict["fade"] as! Float, animated: true)
            }
            if self.cutoffSlider.value != postDict["cutoff"] as! Float{
                self.cutoffSlider.setValue(postDict["cutoff"] as! Float, animated: true)
            }
            self.dimCenterSwitch.setOn(postDict["dimcenter"] as! Int == 1, animated: true)
            self.brightEdgesSwitch.setOn(postDict["brightedges"] as! Int == 1, animated: true)
        })
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        if pickerView == patternPicker{
            return 7
        }else if pickerView == displayPicker{
            return 6
        }
        return 0
    }
    
    func pickerView(_ pickerView: UIPickerView, titleForRow row: Int, forComponent component: Int) -> String? {
        if pickerView == patternPicker{
            return patterns[row]
        }else if pickerView == displayPicker{
            return displayTypes[row]
        }
        return "BLANK"
    }
    
    func pickerView(_ pickerView: UIPickerView,
                    didSelectRow row: Int,
                    inComponent component: Int){
        if pickerView == patternPicker{
            ref.updateChildValues(["PatternID": row])
        }else if pickerView == displayPicker{
            ref.updateChildValues(["DisplayID": row])
        }
    }
    
    @IBAction func switchChanged(_ sender: UISwitch) {
        switch sender {
        case onSwitch:
            ref.updateChildValues(["on": sender.isOn ? 1 : 0])
            break
        case dimCenterSwitch:
            ref.updateChildValues(["dimcenter": sender.isOn ? 1 : 0])
            break
        case brightEdgesSwitch:
            ref.updateChildValues(["brightedges": sender.isOn ? 1 : 0])
            break
        default: break
        }

    }

    
    @IBAction func sliderChanged(_ sender: UISlider) {
        lockUI = true
        switch sender {
        case rSlider:
            ref.updateChildValues(["R": Int(sender.value)])
            break
        case gSlider:
            ref.updateChildValues(["G": Int(sender.value)])
            break
        case bSlider:
            ref.updateChildValues(["B": Int(sender.value)])
            break
        case wSlider:
            ref.updateChildValues(["W": Int(sender.value)])
            break
        case brightnessSlider:
            ref.updateChildValues(["brightness": Int(sender.value)])
            break
        case cycleSpeedSlider:
            ref.updateChildValues(["cycleSpeed": Int(sender.value)])
            break
        case fadeSlider:
            ref.updateChildValues(["fade": sender.value])
            break
        case cutoffSlider:
            ref.updateChildValues(["cutoff": sender.value])
            break
        default: break
        }
    }
    
    
    
    @IBAction func changesEnded(_ sender: UISlider) {
        lockUI = false
    }
    
}

