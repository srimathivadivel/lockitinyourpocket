//  ContentView.swift
//  Lock it in Your Pocket
//  Created by Srimathi Vadivel on 4/1/24

import SwiftUI
import Combine

struct ContentView: View {
    @StateObject private var vm = ViewModel()

    var body: some View {
        NavigationView {
            ZStack {
                Color(UIColor.systemCyan).edgesIgnoringSafeArea(.all) // Background color for the entire app
                
                VStack {
                    bubbleTitle(text: "🔒 Lock it in Your Pocket")
                        .padding(.top, 10)
                        .padding(.bottom, 10)

                    Form {
                        Section(header: Text("Options").font(.headline)) {
                            Toggle(isOn: $vm.containsSymbols) {
                                Label("Symbols", systemImage: "textformat")
                            }
                            Toggle(isOn: $vm.containsUppercase) {
                                Label("Uppercase", systemImage: "textformat.size")
                            }
                            Stepper("Character count \(vm.length)", value: $vm.length, in: 6...18)

                            Button(action: {
                                vm.createPassword()
                            }) {
                                Label("Generate Password", systemImage: "key.fill")
                                    .padding()
                                    .background(Color.blue)
                                    .foregroundColor(.white)
                                    .cornerRadius(8)
                            }
                        }

                        Section(header: Text("Generated Passwords").font(.headline)) {
                            List(vm.passwords) { password in
                                HStack {
                                    Text(password.password)
                                        .font(.body)
                                        .padding()
                                        .background(Color(UIColor.systemGray5))
                                        .cornerRadius(8)
                                        .textSelection(.enabled)
                                    Spacer()
                                    Image(systemName: "lock.fill")
                                        .foregroundColor(password.strengthColor)
                                    Button(action: {
                                        UIPasteboard.general.string = password.password
                                    }) {
                                        Image(systemName: "doc.on.doc")
                                            .foregroundColor(.blue)
                                    }
                                    .buttonStyle(BorderlessButtonStyle())
                                    .padding(.leading, 5)
                                }
                            }
                        }
                    }
                    .background(Color.blue)
                    .navigationTitle("")
                    .navigationBarHidden(true)
                }
            }
        }
    }

    @ViewBuilder
    func bubbleTitle(text: String) -> some View {
        Text(text)
            .fontWeight(.bold)
            .foregroundColor(.white)
            .padding()
            .background(
                LinearGradient(gradient: Gradient(colors: [Color(red: 0.1, green: 0.3, blue: 0.6), Color(red: 0.2, green: 0.5, blue: 0.8)]), startPoint: .topLeading, endPoint: .bottomTrailing)
            )
            .cornerRadius(25)
            .shadow(color: Color.blue.opacity(0.5), radius: 10, x: 0, y: 10)
            .font(.largeTitle)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

