"""Helper function to change AI provider in settings."""

def change_ai_provider():
    """Permite usuário mudar AI provider."""
    from src.config import get_config
    
    print("\n🤖 AI Providers disponíveis:")
    providers = {
        "1": ("whisper-gemini", "FAST Mode - Whisper Local + Gemini (Recomendado) ⚡"),
        "2": ("gemini", "Google Gemini (Rápido, gratuito)"),
        "3": ("openai", "OpenAI (Whisper + GPT, preciso)"),
        "4": ("claude", "Anthropic Claude (Alta qualidade)"),
        "5": ("azure", "Azure OpenAI (Enterprise)")
    }
    
    for key, (name, desc) in providers.items():
        print(f"  {key}. {desc}")
    
    choice = input("\nEscolha o provider (1-5): ").strip()
    
    if choice in providers:
        provider_name, _ = providers[choice]
        get_config().set('ai_provider', provider_name)
        
        # Configure model based on provider
        if provider_name == 'whisper-gemini':
            whisper_models = ["tiny", "base", "small", "medium"]
            print("\n📦 Modelos Whisper (local):")
            for i, model in enumerate(whisper_models, 1):
                sizes = {"tiny": "75MB", "base": "142MB", "small": "466MB", "medium": "1.5GB"}
                print(f"  {i}. {model} ({sizes[model]})")
            whisper_choice = input("\nEscolha o modelo Whisper (1-4, padrão=2): ").strip() or "2"
            if whisper_choice.isdigit() and 1 <= int(whisper_choice) <= len(whisper_models):
                get_config().set('provider_config.whisper_model', whisper_models[int(whisper_choice) - 1])
            
            gemini_models = ["gemini-1.5-flash-latest", "gemini-1.5-pro-latest"]
            print("\n📦 Modelos Gemini (tradução):")
            for i, model in enumerate(gemini_models, 1):
                print(f"  {i}. {model}")
            gemini_choice = input("\nEscolha o modelo Gemini (1-2, padrão=1): ").strip() or "1"
            if gemini_choice.isdigit() and 1 <= int(gemini_choice) <= len(gemini_models):
                get_config().set('provider_config.gemini_model', gemini_models[int(gemini_choice) - 1])
        
        elif provider_name == 'gemini':
            models = ["gemini-1.5-flash-latest", "gemini-1.5-pro-latest", "gemini-2.0-flash-exp"]
            print("\n📦 Modelos Gemini:")
            for i, model in enumerate(models, 1):
                print(f"  {i}. {model}")
            model_choice = input("\nEscolha o modelo (1-3): ").strip()
            if model_choice.isdigit() and 1 <= int(model_choice) <= len(models):
                get_config().set('provider_config.model', models[int(model_choice) - 1])
        
        elif provider_name == 'openai':
            models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"]
            print("\n📦 Modelos OpenAI:")
            for i, model in enumerate(models, 1):
                print(f"  {i}. {model}")
            model_choice = input("\nEscolha o modelo (1-3): ").strip()
            if model_choice.isdigit() and 1 <= int(model_choice) <= len(models):
                get_config().set('provider_config.model', models[int(model_choice) - 1])
            
            # Check for API key
            import os
            if not os.getenv('OPENAI_API_KEY'):
                print("\n⚠️ OPENAI_API_KEY não encontrada no .env")
                print("   Adicione sua chave: OPENAI_API_KEY=sk-...")
        
        elif provider_name == 'claude':
            models = ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"]
            print("\n📦 Modelos Claude:")
            for i, model in enumerate(models, 1):
                print(f"  {i}. {model}")
            model_choice = input("\nEscolha o modelo (1-3): ").strip()
            if model_choice.isdigit() and 1 <= int(model_choice) <= len(models):
                get_config().set('provider_config.model', models[int(model_choice) - 1])
            
            # Check for API keys
            import os
            if not os.getenv('ANTHROPIC_API_KEY'):
                print("\n⚠️ ANTHROPIC_API_KEY não encontrada no .env")
                print("   Adicione sua chave: ANTHROPIC_API_KEY=sk-ant-...")
            if not os.getenv('OPENAI_API_KEY'):
                print("\n⚠️ OPENAI_API_KEY também necessária (para Whisper)")
                print("   Adicione: OPENAI_API_KEY=sk-...")
        
        elif provider_name == 'azure':
            print("\n⚙️ Configuração Azure:")
            endpoint = input("  Endpoint (ex: https://your-resource.openai.azure.com/): ").strip()
            deployment = input("  Deployment name (ex: gpt-4o-mini): ").strip()
            
            get_config().set('provider_config.endpoint', endpoint)
            get_config().set('provider_config.deployment', deployment)
            
            # Check for API key
            import os
            if not os.getenv('AZURE_OPENAI_API_KEY'):
                print("\n⚠️ AZURE_OPENAI_API_KEY não encontrada no .env")
                print("   Adicione sua chave: AZURE_OPENAI_API_KEY=...")
        
        print(f"\n✅ AI Provider alterado para: {provider_name}")
    else:
        print("❌ Opção inválida.")
