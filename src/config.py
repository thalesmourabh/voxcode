import json
import os
from pathlib import Path

class Config:
    """Gerenciador de configurações do VoxCode."""
    
    DEFAULT_CONFIG = {
        "hotkey": "f8",  # Padrão: F8
        "language_from": "pt",  # Português
        "language_to": "en",  # Inglês
        "ai_provider": "gemini",  # Simple mode - Gemini does everything
        "provider_config": {
            "model": "gemini-2.5-flash"
        },
        "auto_detect_language": False,
        "silence_threshold": 0.01,
        "silence_duration": 1.5,
        "min_recording_time": 2.0,
        "ui": {
            "theme": "dark",
            "position": "bottom-center",
            "opacity": 0.95,
            "show_waveform": True,
            "window_width": 320,
            "window_height": 70  # Increased for Wispr Flow style
        }
    }
    
    def __init__(self):
        self.config_dir = Path.home() / ".voxcode"
        self.config_file = self.config_dir / "config.json"
        self.config = self.load()
    
    def load(self):
        """Carrega configurações do arquivo ou cria com defaults."""
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge com defaults (caso novas configs sejam adicionadas)
                    return {**self.DEFAULT_CONFIG, **loaded}
            except Exception as e:
                print(f"⚠️ Erro ao carregar config: {e}. Usando defaults.")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Primeira execução - criar arquivo
            self.save(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def save(self, config=None):
        """Salva configurações no arquivo."""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"❌ Erro ao salvar config: {e}")
    
    def get(self, key, default=None):
        """Obtém valor de configuração."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, default)
            if value is None:
                return default
        return value
    
    def set(self, key, value):
        """Define valor de configuração."""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save()
    
    def reset(self):
        """Reseta para configurações padrão."""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()

# Singleton
_config_instance = None

def get_config():
    """Retorna instância singleton de Config."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
