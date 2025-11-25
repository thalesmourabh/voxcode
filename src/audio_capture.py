import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import os
import time
import threading

class AudioCapture:
    """
    Captura de áudio com detecção automática de silêncio.
    Para a gravação automaticamente quando detecta pausa na fala.
    """
    
    def __init__(self, samplerate=16000, channels=1):
        self.samplerate = samplerate
        self.channels = channels
        self.recording = []
        self.stream = None
        self.is_recording = False
        
        # Configurações de detecção de silêncio
        self.silence_threshold = 0.01  # Threshold de amplitude para silêncio
        self.silence_duration = 1.5    # Segundos de silêncio para parar
        self.min_recording_time = 2.0  # Mínimo de gravação (evita paradas prematuras)
        
        # Callbacks
        self.on_auto_stop_callback = None
        self.ui_callback = None
        
        # Controle de silêncio
        self.silence_start_time = None
        self.recording_start_time = None
        
    def start_recording_with_auto_stop(self, on_auto_stop=None, ui_callback=None):
        """
        Inicia gravação com detecção automática de pausa.
        
        Args:
            on_auto_stop: Callback chamado quando parar automaticamente (recebe audio_path)
            ui_callback: Callback para atualizar UI (recebe evento, dados)
        """
        self.on_auto_stop_callback = on_auto_stop
        self.ui_callback = ui_callback
        
        self.recording = []
        self.is_recording = True
        self.silence_start_time = None
        self.recording_start_time = time.time()
        
        # Inicia stream de áudio
        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            callback=self._audio_callback
        )
        self.stream.start()
        
        # Notifica UI
        if self.ui_callback:
            self.ui_callback('recording_started')
        
        print("🎤 Gravação iniciada com detecção automática de pausa...", flush=True)
        
        # Inicia thread de monitoramento de silêncio
        self.monitor_thread = threading.Thread(target=self._monitor_silence)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def _audio_callback(self, indata, frames, time_info, status):
        """Callback chamado para cada chunk de áudio capturado."""
        if status:
            print(f"⚠️ Status do áudio: {status}", flush=True)
        
        if self.is_recording:
            self.recording.append(indata.copy())
    
    def _is_silent(self):
        """
        Verifica se o último chunk de áudio é silêncio.
        
        Returns:
            bool: True se for silêncio
        """
        if not self.recording:
            return True
        
        # Pega o último chunk
        last_chunk = self.recording[-1]
        
        # Calcula RMS (Root Mean Square) do áudio
        rms = np.sqrt(np.mean(last_chunk**2))
        
        return rms < self.silence_threshold
    
    def _monitor_silence(self):
        """
        Monitora o áudio continuamente e para quando detecta silêncio prolongado.
        Roda em thread separada.
        """
        while self.is_recording:
            time.sleep(0.1)  # Verifica a cada 100ms
            
            if not self.recording:
                continue
            
            # Verifica se está em silêncio
            if self._is_silent():
                if self.silence_start_time is None:
                    self.silence_start_time = time.time()
                else:
                    # Calcula quanto tempo está em silêncio
                    silence_elapsed = time.time() - self.silence_start_time
                    
                    # Verifica se passou do threshold de silêncio
                    if silence_elapsed >= self.silence_duration:
                        # Garante que gravou o mínimo necessário
                        recording_elapsed = time.time() - self.recording_start_time
                        
                        if recording_elapsed >= self.min_recording_time:
                            print(f"🛑 Silêncio detectado ({silence_elapsed:.1f}s). Parando automaticamente...", flush=True)
                            self._auto_stop()
                            break
            else:
                # Reset do contador de silêncio se detectar som
                self.silence_start_time = None
                
                # Atualiza UI com duração
                if self.ui_callback:
                    duration = time.time() - self.recording_start_time
                    self.ui_callback('duration_update', int(duration))
    
    def _auto_stop(self):
        """Para a gravação automaticamente e chama o callback."""
        audio_path = self.stop_recording()
        
        if self.on_auto_stop_callback and audio_path:
            self.on_auto_stop_callback(audio_path)
    
    def stop_recording(self):
        """
        Para a gravação manualmente e salva o arquivo.
        
        Returns:
            str: Caminho do arquivo de áudio salvo
        """
        self.is_recording = False
        
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        # Concatena todos os chunks gravados
        if not self.recording:
            print("⚠️ Nenhum áudio foi gravado.", flush=True)
            return None
        
        audio_data = np.concatenate(self.recording, axis=0)
        
        # Salva em arquivo temporário
        fd, path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        
        sf.write(path, audio_data, self.samplerate)
        
        duration = len(audio_data) / self.samplerate
        print(f"💾 Áudio salvo: {duration:.1f}s em {path}", flush=True)
        
        # Notifica UI
        if self.ui_callback:
            self.ui_callback('recording_stopped', path)
        
        return path
    
    def set_silence_threshold(self, threshold):
        """Ajusta o threshold de detecção de silêncio."""
        self.silence_threshold = threshold
        print(f"⚙️ Threshold de silêncio ajustado para {threshold}", flush=True)
    
    def set_silence_duration(self, duration):
        """Ajusta a duração de silêncio necessária para parar."""
        self.silence_duration = duration
        print(f"⚙️ Duração de silêncio ajustada para {duration}s", flush=True)
