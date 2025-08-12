# 🎮 Jogo da Velha com IA Minimax

Um jogo da velha inteligente com três versões diferentes e IA baseada no algoritmo Minimax.

## 📁 Estrutura do Projeto

```
tic-tac-toe-ai/
│
├── game.py               # Servidor web com IA Python + HTML
├── index.html            # Interface visual (HTML + CSS + JS)
├── game_terminal.py      # Versão para terminal (Python)
├── requirements.txt      # Dependências (apenas bibliotecas nativas)
├── README.md            # Este arquivo
├── .vscode/             # Configurações do VS Code
│   ├── extensions.json  # Extensões recomendadas
│   ├── settings.json    # Configurações do workspace
│   └── tasks.json       # Tarefas automatizadas
└── screenshots/         # Capturas de tela (opcional)
```

## 🚀 Como Executar

### Versão Servidor Web com IA Python (Recomendada) 🌟

1. Certifique-se de ter Python 3.6+ instalado
2. Execute: `python game.py`
3. O navegador abrirá automaticamente em `http://localhost:8000`
4. Jogue com a IA Minimax rodando em Python!

### Versão HTML Standalone

1. Abra o arquivo `index.html` diretamente no navegador
2. IA rodará em JavaScript (também funciona offline)

### Versão Terminal (game_terminal.py)

1. Execute: `python game_terminal.py`
2. Jogue no terminal com interface ASCII

## 🧠 Algoritmo Minimax

O jogo utiliza o algoritmo **Minimax** com **poda alfa-beta** para criar uma IA praticamente imbatível:

- **Avaliação de estados**: +10 (IA vence), -10 (jogador vence), 0 (empate)
- **Busca recursiva**: Explora todas as jogadas possíveis
- **Otimização alfa-beta**: Corta ramos desnecessários da árvore de busca
- **Estratégia inicial**: Prioriza cantos e centro no primeiro movimento

## ✨ Características das Versões

### 🌐 Versão Servidor Web (game.py)

- 🎨 Interface moderna com efeito glassmorphism
- 🤖 **IA roda em Python** (mais poderosa e rápida)
- 📡 **API REST** para comunicação frontend-backend
- 🔄 **Fallback automático** para JavaScript se servidor falhar
- 🌐 **Servidor HTTP integrado** com logs detalhados
- 🚀 **Abre automaticamente** no navegador
- 📱 Design responsivo (desktop e mobile)

### 📱 Versão HTML Standalone (index.html)

- 🎨 Interface moderna com efeito glassmorphism
- 📱 Design responsivo (desktop e mobile)
- 🎯 Animações suaves e feedback visual
- 📊 Sistema de estatísticas
- ⚙️ Controles para personalização
- 🔌 **Funciona offline** (sem necessidade de servidor)
- ⚡ IA em JavaScript (rápida e eficiente)

### 🖥️ Versão Terminal (game_terminal.py)

- 🖥️ Interface de texto limpa e intuitiva
- 🎮 Gameplay completo no terminal
- 🔄 Opção de múltiplas partidas
- ✅ Validação robusta de entrada
- 🎯 Tabuleiro ASCII art visual
- ⚡ Execução leve e rápida

## 🎯 Como Jogar

1. **Você é X**, a **IA é O**
2. Faça três símbolos em linha (horizontal, vertical ou diagonal)
3. A IA nunca comete erros - tente empatar ou encontrar uma brecha!

### Controles da Versão Web/HTML

- **Clique nas células** para fazer jogadas
- **Botão "Novo Jogo"** para reiniciar
- **Botão "Quem Começa"** para alternar iniciativa
- **Estatísticas** são salvas durante a sessão

### Controles da Versão Terminal

- **Digite números 1-9** para escolher posições
- **Escolha quem começa** no início da partida
- **Jogue novamente** ao final de cada partida

## 🛠️ Tecnologias Utilizadas

### Frontend

- **HTML5** - Estrutura da página
- **CSS3** - Estilos modernos com glassmorphism
- **JavaScript (ES6+)** - Lógica do jogo e animações
- **Responsive Design** - Compatível com todos os dispositivos

### Backend

- **Python 3.6+** - Servidor e IA
- **http.server** - Servidor HTTP nativo
- **JSON API** - Comunicação assíncrona
- **Threading** - Abertura automática do navegador

### Algoritmo

- **Minimax** com poda alfa-beta
- **Avaliação heurística** de estados
- **Estratégias otimizadas** para primeiro movimento

## 📖 Referências Técnicas

- [Minimax Algorithm - Never Stop Building](https://www.neverstopbuilding.com/blog/minimax)
- [Minimax in Tic-Tac-Toe - GeeksforGeeks](https://www.geeksforgeeks.org/dsa/finding-optimal-move-in-tic-tac-toe-using-minimax-algorithm-in-game-theory/)

## 🎮 Funcionalidades Avançadas

### Comunicação Frontend-Backend (Versão Web)

```javascript
// A IA Python é chamada via API REST
const response = await fetch('/api/move', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ board: tabuleiro }),
});
```

### Algoritmo Minimax (Python)

```python
def minimax(self, tabuleiro, profundidade, eh_maximizando, alfa, beta):
    resultado = self.verificar_vencedor(tabuleiro)

    if resultado == self.ia:
        return 10 - profundidade  # IA vence
    elif resultado == self.jogador_humano:
        return profundidade - 10  # Jogador vence
    elif resultado == 0:
        return 0  # Empate

    # Recursão com poda alfa-beta...
```

### Estratégias da IA

- **Primeira jogada**: Escolhe cantos ou centro aleatoriamente
- **Jogadas seguintes**: Usa Minimax completo
- **Poda alfa-beta**: Otimização que reduz até 90% das avaliações
- **Avaliação por profundidade**: Prefere vitórias rápidas

## 🎯 Vantagens de Cada Versão

| Característica        | Servidor Web    | HTML Standalone | Terminal        |
| --------------------- | --------------- | --------------- | --------------- |
| **Interface Visual**  | ✅ Moderna      | ✅ Moderna      | ❌ ASCII        |
| **IA em Python**      | ✅ Sim          | ❌ JavaScript   | ✅ Sim          |
| **Funciona Offline**  | ❌ Não          | ✅ Sim          | ✅ Sim          |
| **Responsivo**        | ✅ Sim          | ✅ Sim          | ❌ Não          |
| **Animações**         | ✅ Sim          | ✅ Sim          | ❌ Não          |
| **Velocidade IA**     | 🚀 Muito rápida | ⚡ Rápida       | 🚀 Muito rápida |
| **Facilidade de Uso** | 🌟 Excelente    | 🌟 Excelente    | ⭐ Boa          |

## 🔧 Configuração de Desenvolvimento

### Extensões VS Code Recomendadas

- **Live Server** - Servidor local para desenvolvimento
- **Python** - Suporte completo ao Python
- **Prettier** - Formatação automática de código
- **GitLens** - Controle de versão avançado

### Comandos Úteis

```bash
# Executar servidor web
python game.py

# Executar versão terminal
python game_terminal.py

# Verificar sintaxe Python
python -m py_compile game.py

# Executar com logs detalhados
python game.py --verbose
```

## 🎯 Resumo Executivo

Este projeto implementa um **Jogo da Velha com IA Minimax** em **três versões complementares**:

1. **🌐 Servidor Web**: Combina a **interface visual moderna** com a **IA Python mais poderosa**
2. **📱 HTML Standalone**: **Interface visual** que **funciona offline** com IA JavaScript
3. **🖥️ Terminal**: Versão **leve e rápida** para uso via linha de comando

A **IA é praticamente imbatível** em todas as versões, utilizando o algoritmo **Minimax com poda alfa-beta** para garantir **jogadas sempre ótimas**. O projeto demonstra **diferentes arquiteturas** (monolítica, client-side, servidor-cliente) e **tecnologias** (Python, JavaScript, HTML/CSS, HTTP APIs).

**Ideal para**: Aprendizado de algoritmos, demonstrações de IA, projetos acadêmicos, e diversão! 🎮

---

⭐ **Desenvolvido com algoritmo Minimax para máxima inteligência artificial!**
