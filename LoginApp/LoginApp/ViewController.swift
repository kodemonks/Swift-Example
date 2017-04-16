//
//  ViewController.swift
//  LoginApp
//
//  Created by Avinash Raghunathan on 15/02/17.
//  Copyright © 2017 Unknown Yet. All rights reserved.
//

import UIKit
import FBSDKCoreKit
import FBSDKLoginKit




class ViewController: UIViewController {

    @IBOutlet weak var fbData: UILabel!
    
    
    @IBOutlet weak var fbImages: UIImageView!
    
    var dict : NSDictionary!

    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let loginButton = FBSDKLoginButton()
        
        view.addSubview(loginButton)
        
        loginButton.frame = CGRect(x: 16, y: 50, width: view.frame.width-32 , height: 50)
        
        // Do any additional setup after loading the view, typically from a nib.
        
    
        
        if((FBSDKAccessToken.current()) != nil){
            FBSDKGraphRequest(graphPath: "me", parameters: ["fields": "id, name, first_name, last_name, picture.type(large), email"]).start(completionHandler: { (connection, result, error) -> Void in
                if (error == nil){
                    self.dict = result as! NSDictionary
                    print(self.dict)
                    NSLog(((self.dict.object(forKey: "picture") as AnyObject).object(forKey: "data") as AnyObject).object(forKey: "url") as! String)
                }
            })
        }
        
    
        
//        let name = self.dict.value(forKey: "name")
//        let url = self.dict.value(forKey: "picture")
//        
//        let data = NSData(contentsOf:url! as! URL)
//        
//        // It is the best way to manage nil issue.
//        if (data?.length)! > 0 {
//            fbImages.image = UIImage(data:data! as Data)
//        } else {
//            // In this when data is nil or empty then we can assign a placeholder image
//            fbImages.image = UIImage(named: "placeholder.png")
//        }
//        
//        fbData.text=name as! String?
        
        
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

