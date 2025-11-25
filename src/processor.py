"""
Audio processor for VoxCode.
Handles audio transcription and translation using configurable AI providers.
"""

import os
from src.ai_providers import get_provider
from src.config import get_config

class AudioProcessor:
    """
    Processa áudio e traduz usando provider de IA configurado.
    """
    
    def __init__(self):
        """Inicializa o processador com provider configurado."""
        config = get_config()
        
        # Get provider settings
        provider_name = config.get('ai_provider', 'gemini')
        provider_config = config.get('provider_config', {})
        
        # Initialize provider
        try:
            self.provider = get_provider(provider_name, **provider_config)
            print(f"✅ AI Provider: {self.provider.get_name()}")
        except Exception as e:
            print(f"⚠️ Error initializing {provider_name}: {e}")
            print(f"⚠️ Falling back to Gemini")
            self.provider = get_provider('gemini')
    
    def process(self, audio_path: str) -> str:
        """
        Processa arquivo de áudio e retorna tradução.
        
        Args:
            audio_path: Caminho do arquivo de áudio
            
        Returns:
            Texto traduzido
        """
        config = get_config()
        source_lang = config.get('language_from', 'pt')
        target_lang = config.get('language_to', 'en')
        
        try:
            translated_text = self.provider.translate(
                audio_path=audio_path,
                source_lang=source_lang,
                target_lang=target_lang
            )
            return translated_text
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")
