import time
from pynput.keyboard import Controller, Key
import pyperclip
from AppKit import NSWorkspace

class SmartTextInjector:
    """
    Sistema inteligente de injeção de texto que detecta o aplicativo ativo
    e injeta o texto traduzido automaticamente.
    """
    
    def __init__(self):
        self.keyboard = Controller()
        self.typing_speed = 0.005  # Delay entre caracteres (5ms)
        
    def get_active_app(self):
        """
        Detecta qual aplicativo está ativo no macOS.
        
        Returns:
            str: Nome do aplicativo ativo
        """
        try:
            workspace = NSWorkspace.sharedWorkspace()
            active_app = workspace.activeApplication()
            app_name = active_app['NSApplicationName']
            return app_name
        except Exception as e:
            print(f"⚠️ Erro ao detectar app ativo: {e}", flush=True)
            return "Unknown"
    
    def inject_text_auto(self, text):
        """
        Injeta texto AUTOMATICAMENTE no aplicativo ativo.
        Usa pynput para simular digitação caractere por caractere.
        NÃO envia a mensagem - apenas coloca o texto no campo.
        
        Args:
            text (str): Texto traduzido para injetar
            
        Returns:
            bool: True se injetou com sucesso, False caso contrário
        """
        if not text or not text.strip():
            print("⚠️ Texto vazio, nada para injetar.", flush=True)
            return False
            
        try:
            # Detecta app ativo
            app_name = self.get_active_app()
            print(f"📱 App ativo detectado: {app_name}", flush=True)
            
            # Aguarda 300ms para garantir que o foco está correto
            time.sleep(0.3)
            
            # Injeta o texto usando pynput (mais confiável que pyautogui)
            print(f"⌨️ Injetando texto: '{text[:50]}...'", flush=True)
            
            # Digita caractere por caractere
            for char in text:
                self.keyboard.type(char)
                time.sleep(self.typing_speed)
            
            # NÃO pressiona Enter - deixa o usuário enviar manualmente
            print(f"✅ Texto injetado em {app_name}! Pressione Enter para enviar.", flush=True)
            return True
            
        except Exception as e:
            print(f"❌ Erro ao injetar texto: {e}", flush=True)
            print(f"📋 Copiando para clipboard como fallback...", flush=True)
            
            # Fallback: copia para clipboard
            try:
                pyperclip.copy(text)
                print(f"✅ Texto copiado para clipboard. Cole com Cmd+V", flush=True)
                return False
            except Exception as e2:
                print(f"❌ Erro ao copiar para clipboard: {e2}", flush=True)
                return False
    
    def inject_with_formatting(self, text, context='general'):
        """
        Injeta texto com formatação específica do contexto.
        
        Args:
            text (str): Texto para injetar
            context (str): Contexto ('code', 'chat', 'email', 'general')
            
        Returns:
            bool: True se injetou com sucesso
        """
        # Para futuras melhorias: adicionar formatação específica
        # por contexto (ex: adicionar markdown para chat, etc.)
        
        if context == 'code':
            # Para código, pode adicionar comentário ou formatação
            formatted_text = f"# {text}"
        elif context == 'email':
            # Para email, pode adicionar saudação
            formatted_text = text
        else:
            formatted_text = text
            
        return self.inject_text_auto(formatted_text)
    
    def set_typing_speed(self, speed):
        """
        Ajusta a velocidade de digitação.
        
        Args:
            speed (float): Delay entre caracteres em segundos
        """
        self.typing_speed = speed
        print(f"⚙️ Velocidade de digitação ajustada para {speed}s", flush=True)
