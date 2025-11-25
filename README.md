# 🎙️ VoxCode

<div align="center">

![VoxCode Logo](assets/VoxCodeLogo.png)

**Speak Portuguese. Code in English. Save Tokens.**
*Fale em Português. Code em Inglês. Economize Tokens.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![SwiftUI](https://img.shields.io/badge/SwiftUI-macOS-orange.svg)](https://developer.apple.com/xcode/swiftui/)

[English](#english) | [Português](#português)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### What is VoxCode?
VoxCode is a powerful productivity tool designed for developers who are native Portuguese speakers but work in English-centric environments. It allows you to speak naturally in Portuguese, instantly translates your voice to fluent technical English, and injects the text directly into your IDE, terminal, or AI chat (ChatGPT, Claude, Gemini).

### 🚀 Why VoxCode?

#### 1. The Language Barrier
Many developers think in their native language but need to code and document in English. Switching contexts mentally consumes energy. VoxCode bridges this gap, letting you express complex ideas in your native tongue while producing professional English output.

#### 2. The Token Economy 💰 (Killer Feature)
LLMs (Large Language Models) like GPT-4 and Claude process English much more efficiently than other languages. English prompts use significantly fewer tokens for the same semantic meaning.

**By translating your Portuguese prompts to English, VoxCode saves you ~30-40% on API costs and generation time.**

#### 📊 Token Comparison Example

**Scenario**: Asking for a React component.

| Language | Prompt | Token Count | Cost Impact |
|----------|--------|-------------|-------------|
| **Portuguese** | "Crie um componente React funcional usando hooks para gerenciar um formulário de login com validação de email e senha." | **~28 tokens** | 🔴 Higher |
| **English** | "Create a functional React component using hooks to manage a login form with email and password validation." | **~19 tokens** | 🟢 **~32% Savings** |

**Scenario**: Explaining a bug.

| Language | Prompt | Token Count | Cost Impact |
|----------|--------|-------------|-------------|
| **Portuguese** | "O código está quebrando quando o usuário tenta enviar o formulário vazio, retornando um erro de referência nula no console." | **~32 tokens** | 🔴 Higher |
| **English** | "The code breaks when submitting an empty form, returning a null reference error in the console." | **~21 tokens** | 🟢 **~34% Savings** |

### ✨ Key Features
- **Real-time Voice-to-Text**: Press `F8` and speak.
- **Instant Translation**: Uses Google Gemini 2.5 Flash (Free Tier) for fast, accurate technical translation.
- **Universal Injection**: Works in VSCode, Cursor, Terminal, Slack, Discord, etc.
- **Minimalist UI**: Unobtrusive "pill" design with real-time audio waveform.
- **Privacy Focused**: Local audio processing options available.

### 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/voxcode.git
   cd voxcode
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   Create a `.env` file:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Build the macOS App**
   ```bash
   ./build.sh
   ```

5. **Run**
   ```bash
   python3 main.py
   open build/VoxCode.app
   ```

---

<a name="português"></a>
## 🇧🇷 Português

### O que é o VoxCode?
O VoxCode é uma ferramenta de produtividade essencial para desenvolvedores brasileiros. Ele permite que você fale naturalmente em português, traduz instantaneamente sua fala para um inglês técnico fluente e injeta o texto diretamente na sua IDE, terminal ou chat de IA.

### 🚀 Por que usar o VoxCode?

#### 1. Quebre a Barreira do Idioma
Muitos devs pensam em português mas precisam codar em inglês. O VoxCode elimina o atrito mental de tradução, permitindo que você expresse ideias complexas rapidamente em sua língua nativa.

#### 2. A Economia de Tokens 💰 (Diferencial)
LLMs (como GPT-4 e Claude) são otimizados para inglês. Prompts em inglês consomem significativamente menos tokens para expressar a mesma ideia, resultando em respostas mais rápidas e baratas.

**Ao traduzir seus prompts para inglês, o VoxCode economiza ~30-40% em custos de API e tempo de geração.**

#### 📊 Comparativo de Tokens

**Cenário**: Pedindo um componente React.

| Idioma | Prompt | Tokens | Impacto no Custo |
|--------|--------|--------|------------------|
| **Português** | "Crie um componente React funcional usando hooks para gerenciar um formulário de login com validação de email e senha." | **~28 tokens** | 🔴 Maior |
| **Inglês** | "Create a functional React component using hooks to manage a login form with email and password validation." | **~19 tokens** | 🟢 **~32% Economia** |

**Cenário**: Explicando um bug.

| Idioma | Prompt | Tokens | Impacto no Custo |
|--------|--------|--------|------------------|
| **Português** | "O código está quebrando quando o usuário tenta enviar o formulário vazio, retornando um erro de referência nula no console." | **~32 tokens** | 🔴 Maior |
| **Inglês** | "The code breaks when submitting an empty form, returning a null reference error in the console." | **~21 tokens** | 🟢 **~34% Economia** |

### ✨ Funcionalidades
- **Voz para Texto em Tempo Real**: Pressione `F8` e fale.
- **Tradução Instantânea**: Usa Google Gemini 2.5 Flash (Gratuito) para tradução técnica precisa.
- **Injeção Universal**: Funciona no VSCode, Cursor, Terminal, Slack, Discord, etc.
- **UI Minimalista**: Design "pílula" discreto com visualização de onda sonora.
- **Foco em Privacidade**: Opções de processamento local.

### 🛠️ Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seuusuario/voxcode.git
   cd voxcode
   ```

2. **Instale as dependências Python**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o Ambiente**
   Crie um arquivo `.env`:
   ```bash
   GEMINI_API_KEY=sua_chave_api_aqui
   ```

4. **Compile o App macOS**
   ```bash
   ./build.sh
   ```

5. **Execute**
   ```bash
   python3 main.py
   open build/VoxCode.app
   ```

---

<div align="center">
Built with ❤️ by VoxCode Team and AUTOMAXIS
</div>
