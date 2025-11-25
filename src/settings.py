#!/usr/bin/env python3
"""
VoxCode Settings Manager
Permite ao usuário customizar hotkey, idiomas, modelo, e UI.
"""

import sys
from src.config import get_config

def print_menu():
    """Exibe menu de configurações."""
    print("\n" + "="*50)
    print("⚙️  VoxCode - Configurações")
    print("="*50)
    
    config = get_config()
    
    print("\n📋 Configurações Atuais:")
    print(f"  1. Hotkey: {config.get('hotkey').upper()}")
    print(f"  2. Idioma de origem: {config.get('language_from')}")
    print(f"  3. Idioma de destino: {config.get('language_to')}")
    print(f"  4. AI Provider: {config.get('ai_provider')}")
    print(f"  5. Modelo: {config.get('provider_config', {}).get('model', 'N/A')}")
    print(f"  6. Auto-detectar idioma: {config.get('auto_detect_language')}")
    print(f"  7. UI - Largura: {config.get('ui.window_width')}px")
    print(f"  8. UI - Altura: {config.get('ui.window_height')}px")
    print(f"  9. UI - Opacidade: {config.get('ui.opacity')}")
    print(f"  10. Mostrar waveform: {config.get('ui.show_waveform')}")
    print("\n  0. Resetar para padrões")
    print("  q. Sair")
    print("\n" + "="*50)

def change_hotkey():
    """Permite usuário mudar hotkey."""
    print("\n🔑 Atalhos disponíveis:")
    print("  - F1 até F12")
    print("  - cmd+shift+space (macOS)")
    print("  - ctrl+shift+space (Windows/Linux)")
    print("  - alt+space")
    
    hotkey = input("\nDigite o novo atalho (ex: f9, cmd+shift+space): ").strip().lower()
    
    # Validação básica
    valid_keys = [f"f{i}" for i in range(1, 13)] + [
        "cmd+shift+space", "ctrl+shift+space", "alt+space",
        "cmd+space", "ctrl+space"
    ]
    
    if hotkey in valid_keys:
        get_config().set('hotkey', hotkey)
        print(f"✅ Hotkey alterado para: {hotkey.upper()}")
    else:
        print(f"❌ Atalho inválido. Use um dos sugeridos.")

def change_language():
    """Permite usuário mudar idiomas."""
    print("\n🌍 Idiomas disponíveis:")
    languages = {
        "pt": "Português",
        "es": "Espanhol",
        "fr": "Francês",
        "de": "Alemão",
        "it": "Italiano",
        "ja": "Japonês",
        "zh": "Chinês",
        "en": "Inglês"
    }
    
    for code, name in languages.items():
        print(f"  {code} - {name}")
    
    lang_from = input("\nIdioma de origem (ex: pt): ").strip().lower()
    lang_to = input("Idioma de destino (ex: en): ").strip().lower()
    
    if lang_from in languages and lang_to in languages:
        get_config().set('language_from', lang_from)
        get_config().set('language_to', lang_to)
        print(f"✅ Idiomas: {languages[lang_from]} → {languages[lang_to]}")
    else:
        print("❌ Código de idioma inválido.")

def change_ui_size():
    """Permite usuário mudar tamanho da UI."""
    print("\n📐 Tamanho da janela:")
    print("  Presets:")
    print("  1. Compacto (240x45)")
    print("  2. Médio (280x50) [atual]")
    print("  3. Grande (320x60)")
    print("  4. Custom")
    
    choice = input("\nEscolha (1-4): ").strip()
    
    presets = {
        "1": (240, 45),
        "2": (280, 50),
        "3": (320, 60)
    }
    
    if choice in presets:
        width, height = presets[choice]
        get_config().set('ui.window_width', width)
        get_config().set('ui.window_height', height)
        print(f"✅ Tamanho alterado para: {width}x{height}px")
    elif choice == "4":
        try:
            width = int(input("Largura (px): "))
            height = int(input("Altura (px): "))
            get_config().set('ui.window_width', width)
            get_config().set('ui.window_height', height)
            print(f"✅ Tamanho alterado para: {width}x{height}px")
        except ValueError:
            print("❌ Valores inválidos.")

def main():
    """Loop principal do menu."""
    while True:
        print_menu()
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == '1':
            change_hotkey()
        elif choice == '2' or choice == '3':
            change_language()
        elif choice == '4':
            from provider_settings import change_ai_provider
            change_ai_provider()
        elif choice == '5':
            # Model selection (now handled by provider selection)
            print("💡 Use opção 4 para alterar provider e modelo")
        elif choice == '6':
            auto = input("Auto-detectar idioma? (s/n): ").strip().lower()
            get_config().set('auto_detect_language', auto == 's')
            print(f"✅ Auto-detecção: {'Ativada' if auto == 's' else 'Desativada'}")
        elif choice == '7' or choice == '8':
            change_ui_size()
        elif choice == '9':
            try:
                opacity = float(input("Opacidade (0.5 - 1.0): "))
                if 0.5 <= opacity <= 1.0:
                    get_config().set('ui.opacity', opacity)
                    print(f"✅ Opacidade alterada para: {opacity}")
                else:
                    print("❌ Valor deve estar entre 0.5 e 1.0")
            except ValueError:
                print("❌ Valor inválido.")
        elif choice == '10':
            show = input("Mostrar waveform? (s/n): ").strip().lower()
            get_config().set('ui.show_waveform', show == 's')
            print(f"✅ Waveform: {'Visível' if show == 's' else 'Oculto'}")
        elif choice == '0':
            confirm = input("⚠️ Resetar todas configurações? (s/n): ").strip().lower()
            if confirm == 's':
                get_config().reset()
                print("✅ Configurações resetadas para padrão.")
        elif choice.lower() == 'q':
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida.")

if __name__ == "__main__":
    main()
