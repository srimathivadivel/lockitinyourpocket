//  ViewModifiers.swift
//  Lock it in Your Pocket
//  Created by Srimathi  Vadivel  on 4/1/24

import SwiftUI
import Foundation
import Combine

struct BubbleTitle: ViewModifier {
    let text: String

    func body(content: Content) -> some View {
        ZStack {
            LinearGradient(gradient: Gradient(colors: [Color(red: 0.1, green: 0.3, blue: 0.6), Color(red: 0.2, green: 0.5, blue: 0.8)]), startPoint: .topLeading, endPoint: .bottomTrailing)
                .mask(
                    Text(text)
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .foregroundColor(.white)
                        .padding()
                        .background(Color.clear)
                        .cornerRadius(25)
                        .shadow(color: Color("BlueAccent").opacity(0.5), radius: 10, x: 0, y: 10)
                )
            Text(text)
                .font(.largeTitle)
                .fontWeight(.bold)
                .foregroundColor(.white)
                .padding()
                .background(Color.clear)
                .cornerRadius(25)
                .shadow(color: Color("BlueAccent").opacity(0.5), radius: 10, x: 0, y: 10)
        }
    }
}

extension View {
    func addCustomNavigationView(title: String) -> some View {
        VStack {
            Text("🔒 \(title)")
                .font(.largeTitle)
                .fontWeight(.bold)
                .foregroundColor(.blue)
                .padding()
                .background(Color(UIColor.systemGray6))
                .cornerRadius(10)
                .padding(.top, 20)
            self
        }
        .navigationTitle("")
        .navigationBarHidden(true)
    }

    func bubbleTitle(text: String) -> some View {
        modifier(BubbleTitle(text: text))
    }
}
