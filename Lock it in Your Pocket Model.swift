//  Lock it in Your Pocket Model.swift
//  Lock it in Your Pocket
//  Created by Srimathi  Vadivel  on 4/1/24


import Foundation
import SwiftUI

struct Password: Identifiable, Codable {
    var id = UUID()
    var password: String
    var containsSymbols: Bool
    var containsUppercase: Bool
    
    var strength: Int {
        var strength = 0
        
        if containsSymbols {
            strength += 1
        }
        
        if containsUppercase {
            strength += 1
        }
        
        if password.count > 12 {
            strength += 1
        } else if password.count < 8 {
            strength -= 1
        }
        
        return strength
    }
    
    var strengthColor: Color {
        switch strength {
        case 1: return .red
        case 2: return .yellow
        case 3: return .green
        default: return .gray
        }
    }
}
