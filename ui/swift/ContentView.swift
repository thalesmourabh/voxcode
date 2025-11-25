import SwiftUI

struct ContentView: View {
    @EnvironmentObject var bridge: Bridge
    
    var body: some View {
        HStack(spacing: 10) {
            // Waveform (sempre visível quando gravando)
            if bridge.isRecording {
                RealWaveformView(audioLevels: bridge.audioLevels)
                    .frame(width: 50, height: 24)
                    .transition(.scale.combined(with: .opacity))
            }
            
            // Status text
            Text(bridge.statusText)
                .font(.system(size: 12, weight: .medium, design: .rounded))
                .foregroundColor(.white)
            
            // Timer (quando gravando)
            if bridge.isRecording {
                Text(bridge.timer)
                    .font(.system(size: 10, weight: .medium, design: .monospaced))
                    .foregroundColor(.white.opacity(0.6))
            }
        }
        .padding(.horizontal, 14)
        .padding(.vertical, 8)
        .background(
            ZStack {
                // Fundo preto com leve transparência
                Color.black.opacity(0.85)
                
                // Borda sutil
                RoundedRectangle(cornerRadius: 20)
                    .stroke(Color.white.opacity(0.15), lineWidth: 0.5)
            }
        )
        .background(VisualEffectView(material: .hudWindow, blendingMode: .behindWindow))
        .clipShape(Capsule())
        .shadow(color: Color.black.opacity(0.4), radius: 8, x: 0, y: 4)
        .frame(width: 180, height: 36)
        .scaleEffect(bridge.scale)
        .opacity(bridge.opacity)
        .animation(.spring(response: 0.3, dampingFraction: 0.75), value: bridge.scale)
        .animation(.easeInOut(duration: 0.25), value: bridge.opacity)
        .background(WindowAccessor())
    }
}

// Waveform minimalista
struct RealWaveformView: View {
    let audioLevels: [CGFloat]
    
    var body: some View {
        HStack(spacing: 2) {
            ForEach(audioLevels.indices, id: \.self) { i in
                Capsule()
                    .fill(Color.white.opacity(0.9))
                    .frame(width: 2, height: max(3, audioLevels[i]))
                    .animation(.spring(response: 0.12, dampingFraction: 0.65), value: audioLevels[i])
            }
        }
    }
}

// Native Blur Effect
struct VisualEffectView: NSViewRepresentable {
    let material: NSVisualEffectView.Material
    let blendingMode: NSVisualEffectView.BlendingMode
    
    func makeNSView(context: Context) -> NSVisualEffectView {
        let visualEffectView = NSVisualEffectView()
        visualEffectView.material = material
        visualEffectView.blendingMode = blendingMode
        visualEffectView.state = .active
        return visualEffectView
    }
    
    func updateNSView(_ nsView: NSVisualEffectView, context: Context) {
        nsView.material = material
        nsView.blendingMode = blendingMode
    }
}

// Window Accessor
struct WindowAccessor: NSViewRepresentable {
    func makeNSView(context: Context) -> NSView {
        let view = NSView()
        DispatchQueue.main.async {
            if let window = view.window {
                window.isOpaque = false
                window.backgroundColor = .clear
                window.hasShadow = false
                window.styleMask = [.borderless]
                window.isMovableByWindowBackground = true
                window.level = .floating
            }
        }
        return view
    }
    
    func updateNSView(_ nsView: NSView, context: Context) {}
}
