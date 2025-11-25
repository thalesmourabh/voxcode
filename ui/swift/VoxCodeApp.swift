// VoxCodeApp.swift
import SwiftUI

@main
struct VoxCodeApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        Settings {
            EmptyView()
        }
    }
}

class AppDelegate: NSObject, NSApplicationDelegate {
    var window: NSWindow!
    var bridge: Bridge!
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Create bridge
        bridge = Bridge()
        
        // Create window
        window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 180, height: 36),
            styleMask: [.borderless],
            backing: .buffered,
            defer: false
        )
        
        // Configure window
        window.isOpaque = false
        window.backgroundColor = .clear
        window.level = .floating
        window.collectionBehavior = [.canJoinAllSpaces, .stationary]
        window.isMovableByWindowBackground = true
        window.hasShadow = false
        
        // Position at bottom center of screen
        if let screen = NSScreen.main {
            let screenFrame = screen.visibleFrame
            let x = (screenFrame.width - 180) / 2 + screenFrame.minX
            let y = screenFrame.minY + 100 // 100px from bottom
            window.setFrameOrigin(NSPoint(x: x, y: y))
        }
        
        // Set content view
        let contentView = ContentView()
            .environmentObject(bridge)
        window.contentView = NSHostingView(rootView: contentView)
        
        // Show window
        window.orderFrontRegardless()
        
        // Keep app running without dock icon
        NSApp.setActivationPolicy(.accessory)
    }
}
