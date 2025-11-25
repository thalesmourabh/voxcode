import SwiftUI
import Foundation
import Combine

enum BridgeState: String {
    case idle, recording, processing, success, error
}

class Bridge: ObservableObject {
    @Published var statusText: String = "Press F8"
    @Published var subTitle: String = ""
    @Published var audioLevels: [CGFloat] = Array(repeating: 3, count: 10)
    @Published var timer: String = "0:00"
    @Published var currentState: BridgeState = .idle
    @Published var isRecording: Bool = false
    @Published var scale: CGFloat = 1.0
    @Published var opacity: Double = 1.0
    
    private var webSocket: URLSessionWebSocketTask?
    private var waveTimer: Timer?
    private var recordingTimer: Timer?
    private var recordingStartTime: Date?
    
    init() {
        connect()
        startIdleAnimation()
    }
    
    private func connect() {
        let url = URL(string: "ws://localhost:8765")!
        webSocket = URLSession(configuration: .default).webSocketTask(with: url)
        webSocket?.resume()
        listen()
    }
    
    private func listen() {
        webSocket?.receive { [weak self] result in
            guard let self = self else { return }
            switch result {
            case .failure(let error):
                print("WebSocket error:", error)
                DispatchQueue.global().asyncAfter(deadline: .now() + 1) {
                    self.connect()
                }
            case .success(let message):
                if case .string(let text) = message,
                   let data = text.data(using: .utf8),
                   let msg = try? JSONDecoder().decode(Message.self, from: data) {
                    self.handle(msg)
                }
                self.listen()
            }
        }
    }
    
    private func handle(_ msg: Message) {
        DispatchQueue.main.async {
            switch msg.action {
            case "show-recording":
                self.showRecording()
            case "show-processing":
                self.showProcessing()
            case "show-success":
                self.showSuccess(text: msg.payload?.text ?? "")
            case "show-error":
                self.showError(message: msg.payload?.message ?? "Error")
            case "hide":
                self.hide()
            case "audio-level":
                if let level = msg.payload?.level {
                    self.updateAudioLevel(level: level)
                }
            default:
                break
            }
        }
    }
    
    private func showRecording() {
        withAnimation(.spring(response: 0.3, dampingFraction: 0.75)) {
            currentState = .recording
            isRecording = true
            statusText = "Listening..."
            scale = 1.0
            opacity = 1.0
        }
        startRecordingWaveform()
        startRecordingTimer()
    }
    
    private func showProcessing() {
        withAnimation(.easeInOut(duration: 0.25)) {
            currentState = .processing
            isRecording = false
            statusText = "Processing..."
        }
        stopRecordingWaveform()
        stopRecordingTimer()
    }
    
    private func showSuccess(text: String) {
        withAnimation(.spring(response: 0.3, dampingFraction: 0.75)) {
            currentState = .success
            isRecording = false
            statusText = "Done!"
        }
        
        // Auto-hide after 2 seconds
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            self.hide()
        }
    }
    
    private func showError(message: String) {
        withAnimation(.spring(response: 0.3, dampingFraction: 0.75)) {
            currentState = .error
            isRecording = false
            statusText = "Error"
        }
        
        // Auto-hide after 3 seconds
        DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
            self.hide()
        }
    }
    
    private func hide() {
        withAnimation(.easeOut(duration: 0.3)) {
            opacity = 0.0
            scale = 0.95
        }
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
            withAnimation {
                self.currentState = .idle
                self.statusText = "Press F8"
                self.subTitle = ""
                self.opacity = 1.0
                self.scale = 1.0
            }
        }
    }
    
    // MARK: - Waveform Animation
    
    private func startIdleAnimation() {
        // Subtle breathing effect when idle
        waveTimer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] _ in
            guard let self = self, !self.isRecording else { return }
            let time = Date().timeIntervalSince1970
            self.audioLevels = (0..<10).map { i in
                3 + CGFloat(sin(time * 2 + Double(i) * 0.5)) * 1.5
            }
        }
    }
    
    private func startRecordingWaveform() {
        waveTimer?.invalidate()
        waveTimer = Timer.scheduledTimer(withTimeInterval: 0.05, repeats: true) { [weak self] _ in
            guard let self = self else { return }
            // Simulate real waveform (will be replaced with actual audio data)
            self.audioLevels = (0..<10).map { _ in
                CGFloat.random(in: 6...20)
            }
        }
    }
    
    private func stopRecordingWaveform() {
        waveTimer?.invalidate()
        startIdleAnimation()
    }
    
    private func updateAudioLevel(level: Double) {
        // Update waveform with real audio data from Python
        let normalizedLevel = CGFloat(level * 40) // Scale to UI
        audioLevels.removeFirst()
        audioLevels.append(max(4, normalizedLevel))
    }
    
    // MARK: - Timer
    
    private func startRecordingTimer() {
        recordingStartTime = Date()
        timer = "0:00"
        recordingTimer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] _ in
            guard let self = self, let startTime = self.recordingStartTime else { return }
            let elapsed = Date().timeIntervalSince(startTime)
            let minutes = Int(elapsed) / 60
            let seconds = Int(elapsed) % 60
            self.timer = String(format: "%d:%02d", minutes, seconds)
        }
    }
    
    private func stopRecordingTimer() {
        recordingTimer?.invalidate()
        recordingTimer = nil
        recordingStartTime = nil
    }
}

// Helper structs for decoding
struct Message: Decodable {
    let action: String
    let payload: Payload?
}

struct Payload: Decodable {
    let auto_stop: Bool?
    let text: String?
    let message: String?
    let level: Double?
}
