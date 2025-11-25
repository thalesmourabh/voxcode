"""
AI Provider abstraction layer for VoxCode.
Supports multiple AI providers: Gemini, OpenAI, Claude, Azure, etc.
"""

from abc import ABC, abstractmethod
import os
from typing import Optional

class AIProvider(ABC):
    """Base class for AI translation providers."""
    
    @abstractmethod
    def translate(self, audio_path: str, source_lang: str = "pt", target_lang: str = "en") -> str:
        """
        Translate audio to text in target language.
        
        Args:
            audio_path: Path to audio file
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return provider name."""
        pass


class GeminiProvider(AIProvider):
    """Google Gemini AI provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-flash-latest"):
        from google import genai
        from google.genai import types
        
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model = model
    
    def translate(self, audio_path: str, source_lang: str = "pt", target_lang: str = "en") -> str:
        """Translate using Gemini."""
        from google.genai import types
        
        # Upload audio with explicit mime type
        with open(audio_path, 'rb') as f:
            audio_file = self.client.files.upload(
                file=f,
                config=types.UploadFileConfig(mime_type="audio/wav")
            )
        
        # Prepare prompt
        prompt = f"""You are a professional translator specializing in technical and programming content.

Task: Transcribe the audio in {source_lang} and translate it to {target_lang}.

Requirements:
1. Return ONLY the translated text, nothing else
2. Output as a SINGLE paragraph (no line breaks)
3. Maintain proper punctuation and grammar
4. Preserve technical terms accurately
5. Use natural, fluent {target_lang}

Audio to translate:"""
        
        # Generate translation
        response = self.client.models.generate_content(
            model=self.model,
            contents=[prompt, audio_file]
        )
        
        return response.text.strip()
    
    def get_name(self) -> str:
        return f"Google Gemini ({self.model})"


class OpenAIProvider(AIProvider):
    """OpenAI Whisper + GPT provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
    
    def translate(self, audio_path: str, source_lang: str = "pt", target_lang: str = "en") -> str:
        """Translate using Whisper + GPT."""
        
        # Step 1: Transcribe with Whisper
        with open(audio_path, 'rb') as f:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language=source_lang
            )
        
        transcribed_text = transcription.text
        
        # Step 2: Translate with GPT
        prompt = f"""Translate the following {source_lang} text to {target_lang}.

Requirements:
- Return ONLY the translation, no explanations
- Output as a SINGLE paragraph (no line breaks)
- Maintain technical terminology
- Use natural, fluent {target_lang}

Text: {transcribed_text}"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
    
    def get_name(self) -> str:
        return f"OpenAI (Whisper + {self.model})"


class ClaudeProvider(AIProvider):
    """Anthropic Claude provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
    
    def translate(self, audio_path: str, source_lang: str = "pt", target_lang: str = "en") -> str:
        """
        Translate using Claude.
        Note: Claude doesn't support audio directly, so we use Whisper for transcription first.
        """
        
        # Use OpenAI Whisper for transcription (requires OPENAI_API_KEY)
        try:
            from openai import OpenAI
            openai_key = os.getenv("OPENAI_API_KEY")
            if not openai_key:
                raise ValueError("OPENAI_API_KEY required for audio transcription with Claude")
            
            openai_client = OpenAI(api_key=openai_key)
            with open(audio_path, 'rb') as f:
                transcription = openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    language=source_lang
                )
            transcribed_text = transcription.text
        except ImportError:
            raise ImportError("openai package required for Claude audio support. Run: pip install openai")
        
        # Translate with Claude
        prompt = f"""Translate the following {source_lang} text to {target_lang}.

Requirements:
- Return ONLY the translation, no explanations
- Output as a SINGLE paragraph (no line breaks)
- Maintain technical terminology
- Use natural, fluent {target_lang}

Text: {transcribed_text}"""
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text.strip()
    
    def get_name(self) -> str:
        return f"Anthropic Claude ({self.model})"


class AzureProvider(AIProvider):
    """Azure OpenAI provider."""
    
    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, 
                 deployment: str = "gpt-4o-mini"):
        try:
            from openai import AzureOpenAI
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
        
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        
        if not self.api_key or not self.endpoint:
            raise ValueError("AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT required")
        
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version="2024-02-01",
            azure_endpoint=self.endpoint
        )
        self.deployment = deployment
    
    def translate(self, audio_path: str, source_lang: str = "pt", target_lang: str = "en") -> str:
        """Translate using Azure OpenAI."""
        
        # Transcribe with Whisper
        with open(audio_path, 'rb') as f:
            transcription = self.client.audio.transcriptions.create(
                model="whisper",
                file=f,
                language=source_lang
            )
        
        transcribed_text = transcription.text
        
        # Translate with GPT
        prompt = f"""Translate the following {source_lang} text to {target_lang}.

Requirements:
- Return ONLY the translation, no explanations
- Output as a SINGLE paragraph (no line breaks)
- Maintain technical terminology
- Use natural, fluent {target_lang}

Text: {transcribed_text}"""
        
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
    
    def get_name(self) -> str:
        return f"Azure OpenAI ({self.deployment})"


# Provider factory
def get_provider(provider_name: str, **kwargs) -> AIProvider:
    """
    Factory function to get AI provider instance.
    
    Args:
        provider_name: Name of provider ('gemini', 'openai', 'claude', 'azure', 'whisper-gemini')
        **kwargs: Provider-specific arguments
        
    Returns:
        AIProvider instance
    """
    # Import whisper provider here to avoid import errors if not installed
    try:
        from src.whisper_provider import WhisperGeminiProvider
        whisper_available = True
    except ImportError:
        whisper_available = False
    
    providers = {
        'gemini': GeminiProvider,
        'openai': OpenAIProvider,
        'claude': ClaudeProvider,
        'azure': AzureProvider
    }
    
    if whisper_available:
        providers['whisper-gemini'] = WhisperGeminiProvider
    
    provider_class = providers.get(provider_name.lower())
    if not provider_class:
        available = list(providers.keys())
        raise ValueError(f"Unknown provider: {provider_name}. Available: {available}")
    
    return provider_class(**kwargs)
