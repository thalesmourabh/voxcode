import os
import threading
import time
from dotenv import load_dotenv
from pynput import keyboard

from src.audio_capture import AudioCapture
from src.processor import AudioProcessor
from src.text_injector import SmartTextInjector
# Removed Tkinter RecorderWindow import
from ui.electron_bridge import ElectronBridge
from src.config import get_config

# Load environment variables
load_dotenv()

class VoxCodeApp:
    """
    Aplicação principal do VoxCode.
    Integra captura de áudio, processamento, UI e injeção de texto.
    """
    
    def __init__(self):
        # Load config
        self.config = get_config()
        
        # Componentes principais
        self.audio_capture = AudioCapture()
        self.processor = AudioProcessor()
        self.injector = SmartTextInjector()
        # UI bridge to Electron
        self.bridge = ElectronBridge()
        
        # Estado
        self.is_recording = False
    
    def start_recording(self):
        """Inicia gravação ao pressionar hotkey."""
        if self.is_recording:
            return  # Já está gravando
        
        self.is_recording = True
        
        # Mostra UI via Electron bridge
        self.bridge.show_recording(auto_stop=True)
        
        # Inicia gravação com detecção automática
        self.audio_capture.start_recording_with_auto_stop(
            on_auto_stop=self.on_recording_stopped,
            ui_callback=self.on_ui_update
        )
    
    def on_recording_stopped(self, audio_path):
        """
        Callback chamado quando gravação para automaticamente.
        
        Args:
            audio_path: Caminho do arquivo de áudio gravado
        """
        self.is_recording = False
        
        # Atualiza UI para processamento
        self.bridge.show_processing()
        
        # Processa em thread separada para não travar UI
        threading.Thread(
            target=self.process_and_inject,
            args=(audio_path,),
            daemon=True
        ).start()
    
    def process_and_inject(self, audio_path):
        """
        Processa áudio e injeta texto automaticamente.
        
        Args:
            audio_path: Caminho do arquivo de áudio
        """
        try:
            # 1. Transcrever e Traduzir com Gemini
            translated_text = self.processor.process(audio_path)
            print(f"✅ Traduzido: {translated_text}", flush=True)
            
            if not translated_text or not translated_text.strip():
                raise ValueError("Texto traduzido está vazio")
            
            # 2. Injetar texto automaticamente
            success = self.injector.inject_text_auto(translated_text)
            
            # 3. Mostrar sucesso na UI
            self.bridge.show_success(translated_text)
                
        except Exception as e:
            print(f"❌ Erro: {e}", flush=True)
            self.bridge.show_error(str(e))
            
        finally:
            # Limpeza do arquivo temporário
            if audio_path and os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except:
                    pass
    
    def on_ui_update(self, event, data=None):
        """
        Callback para atualizar UI durante gravação.
        
        Args:
            event: Tipo de evento ('recording_started', 'duration_update', etc.)
            data: Dados do evento
        """
        if event == 'duration_update':
            # Could send duration updates via bridge if needed
            pass
    
    def run(self):
        """Inicia a aplicação."""
        hotkey = self.config.get('hotkey', 'f8')
        print(f"🚀 VoxCode está rodando. Pressione {hotkey.upper()} para iniciar gravação.", flush=True)
        print("💡 O sistema detectará automaticamente quando você parar de falar.", flush=True)
        print(f"⚙️  Para alterar configurações, execute: python3 settings.py", flush=True)
        
        # Configurar listener de teclado
        def on_press(key):
            # Parse hotkey config
            hotkey_lower = hotkey.lower()
            
            # Simple key (f1-f12)
            if hasattr(key, 'name') and key.name == hotkey_lower:
                if not self.is_recording:
                    self.start_recording()
        
        # Inicia listener em thread separada
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        
        # Mantém programa rodando (UI já está em thread separada)
        try:
            # Loop infinito para manter o programa vivo
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n👋 Encerrando VoxCode...", flush=True)
            listener.stop()

def main():
    """Entry point da aplicação."""
    app = VoxCodeApp()
    app.run()

if __name__ == "__main__":
    main()
