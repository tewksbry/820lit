//
//  ViewController.swift
//  820lit
//
//  Created by Stiven Deleur on 1/28/17.
//  Copyright © 2017 Stiven Deleur. All rights reserved.
//

import UIKit
import FirebaseDatabase

class ViewController: UIViewController, UIPickerViewDataSource, UIPickerViewDelegate, HSBColorPickerDelegate {

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
    @IBOutlet weak var colorPicker: HSBColorPicker!
    @IBOutlet weak var colorDisplayView: UIView!
    
    var patterns = ["Single Color", "Rainbow", "Random", "Random Bright", "Grayscale", "USC", "Mood Lighting"]
    var displayTypes = ["Fill", "Middle Out", "Middle Out Fill", "Strobe", "Cycle", "Middle Out White"]
    
//    func updateViews() {
//        if patternPicker.selectedRow(inComponent: 0) != 0{
//            rSlider.alpha = 0
//            gSlider.alpha = 0
//            bSlider.alpha = 0
//            wSlider.alpha = 0
//            colorPicker.alpha = 0
//            colorDisplayView.alpha = 0
//        }else{
//            rSlider.alpha = 1
//            gSlider.alpha = 1
//            bSlider.alpha = 1
//            wSlider.alpha = 1
//            colorPicker.alpha = 1
//            colorDisplayView.alpha = 1
//        }
//        
//    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        colorPicker.delegate = self
        ref = FIRDatabase.database().reference()
        refHandle = ref.observe(FIRDataEventType.value, with: { (snapshot) in
            let postDict = snapshot.value as? [String : AnyObject] ?? [:]
            print(postDict)
//            if self.lockUI{ return}
            self.patternPicker.selectRow(postDict["PatternID"] as! Int, inComponent: 0, animated: true)
            self.displayPicker.selectRow(postDict["DisplayID"] as! Int, inComponent: 0, animated: true)
            self.onSwitch.setOn(postDict["on"] as! Int == 1, animated: true)
            self.rSlider.setValue(Float(postDict["R"] as! Int), animated: true)
            self.gSlider.setValue(Float(postDict["G"] as! Int), animated: true)
            self.bSlider.setValue(Float(postDict["B"] as! Int), animated: true)
            self.wSlider.setValue(Float(postDict["W"] as! Int), animated: true)
            self.brightnessSlider.setValue(Float(postDict["brightness"] as! Int), animated: true)
            self.cycleSpeedSlider.setValue(Float(postDict["cycleSpeed"] as! Int), animated: true)
            self.fadeSlider.setValue(postDict["fade"] as! Float, animated: true)
            self.cutoffSlider.setValue(postDict["cutoff"] as! Float, animated: true)
            self.dimCenterSwitch.setOn(postDict["dimcenter"] as! Int == 1, animated: true)
            self.brightEdgesSwitch.setOn(postDict["brightedges"] as! Int == 1, animated: true)
            
            self.colorDisplayView.backgroundColor = UIColor.init(colorLiteralRed: Float(postDict["R"] as! Int)/255, green: Float(postDict["G"] as! Int)/255, blue: Float(postDict["B"] as! Int)/255, alpha: 1)
//            self.updateViews()
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
    

    
    func HSBColorColorPickerTouched(sender:HSBColorPicker, color:UIColor, point:CGPoint, state:UIGestureRecognizerState){
        var r: CGFloat = 0, g: CGFloat = 0, b: CGFloat = 0, a: CGFloat = 0
        color.getRed(&r, green: &g, blue: &b, alpha: &a)
        ref.updateChildValues(["R": Int(r*255)])
        ref.updateChildValues(["G": Int(g*255)])
        ref.updateChildValues(["B": Int(b*255)])
        ref.updateChildValues(["W": 0])
        
    }
    
}

