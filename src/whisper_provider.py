"""
Whisper Local Provider for VoxCode.
Provides fast local transcription using OpenAI Whisper with GPU acceleration.
"""

import os
import torch
import whisper
from typing import Optional

class WhisperLocalProvider:
    """Local Whisper transcription with GPU acceleration."""
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize Whisper model.
        
        Args:
            model_size: Model size (tiny, base, small, medium, large)
        """
        self.model_size = model_size
        
        # Detect device (Metal for Apple Silicon, CUDA for NVIDIA, CPU fallback)
        if torch.backends.mps.is_available():
            self.device = "mps"  # Apple Silicon (M1/M2/M3)
            print(f"✅ Using Metal (Apple Silicon GPU) for Whisper")
        elif torch.cuda.is_available():
            self.device = "cuda"  # NVIDIA GPU
            print(f"✅ Using CUDA (NVIDIA GPU) for Whisper")
        else:
            self.device = "cpu"
            print(f"⚠️ Using CPU for Whisper (slower)")
        
        # Load model
        print(f"📦 Loading Whisper model: {model_size}...")
        self.model = whisper.load_model(model_size, device=self.device)
        print(f"✅ Whisper model loaded successfully")
    
    def transcribe(self, audio_path: str, language: str = "pt") -> str:
        """
        Transcribe audio file.
        
        Args:
            audio_path: Path to audio file
            language: Language code (pt, en, es, etc.)
            
        Returns:
            Transcribed text
        """
        try:
            result = self.model.transcribe(
                audio_path,
                language=language,
                fp16=False,  # Metal doesn't support fp16
                verbose=False
            )
            return result["text"].strip()
        except Exception as e:
            raise Exception(f"Whisper transcription failed: {str(e)}")
    
    def get_name(self) -> str:
        """Return provider name."""
        return f"Whisper Local ({self.model_size}, {self.device.upper()})"


class WhisperGeminiProvider:
    """
    Hybrid provider: Whisper (local transcription) + Gemini (cloud translation).
    FAST mode - best of both worlds.
    """
    
    def __init__(self, whisper_model: str = "base", gemini_model: str = "gemini-1.5-flash-latest"):
        """
        Initialize hybrid provider.
        
        Args:
            whisper_model: Whisper model size
            gemini_model: Gemini model name
        """
        from google import genai
        
        # Initialize Whisper (local)
        self.whisper = WhisperLocalProvider(model_size=whisper_model)
        
        # Initialize Gemini (cloud)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        self.gemini_client = genai.Client(api_key=api_key)
        self.gemini_model = gemini_model
    
    def translate(self, audio_path: str, source_lang: str = "pt", target_lang: str = "en") -> str:
        """
        Transcribe locally with Whisper, then translate with Gemini.
        
        Args:
            audio_path: Path to audio file
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        # Step 1: Transcribe with Whisper (local, fast)
        print(f"🎤 Transcribing with Whisper ({self.whisper.device.upper()})...")
        transcribed_text = self.whisper.transcribe(audio_path, language=source_lang)
        print(f"📝 Transcribed: {transcribed_text[:50]}...")
        
        # Step 2: Translate with Gemini (cloud, accurate)
        print(f"🌍 Translating with Gemini...")
        prompt = f"""Translate the following {source_lang} text to {target_lang}.

Requirements:
- Return ONLY the translation, no explanations
- Output as a SINGLE paragraph (no line breaks)
- Maintain technical terminology
- Use natural, fluent {target_lang}

Text: {transcribed_text}"""
        
        response = self.gemini_client.models.generate_content(
            model=self.gemini_model,
            contents=prompt
        )
        
        translated_text = response.text.strip()
        print(f"✅ Translated: {translated_text[:50]}...")
        
        return translated_text
    
    def get_name(self) -> str:
        """Return provider name."""
        return f"FAST Mode (Whisper {self.whisper.model_size} + Gemini)"
