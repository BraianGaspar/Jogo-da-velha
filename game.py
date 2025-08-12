#!/usr/bin/env python3
"""
Jogo da Velha com IA Minimax - Servidor Web
Serve o arquivo HTML e processa as jogadas da IA via API REST
"""

import json
import math
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
import webbrowser
import threading
import time

class JogoDaVelhaIA:
    """Classe para lógica do jogo da velha com IA Minimax"""
    
    def __init__(self):
        self.jogador_humano = 1
        self.ia = -1
        
    def verificar_vencedor(self, tabuleiro):
        """Verifica se há um vencedor ou empate"""
        combinacoes = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # linhas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # colunas
            [0, 4, 8], [2, 4, 6]              # diagonais
        ]
        
        for combinacao in combinacoes:
            if (tabuleiro[combinacao[0]] == tabuleiro[combinacao[1]] == 
                tabuleiro[combinacao[2]] != 0):
                return tabuleiro[combinacao[0]]
        
        # Verifica empate
        if 0 not in tabuleiro:
            return 0  # empate
        
        return None  # jogo continua
    
    def minimax(self, tabuleiro, profundidade, eh_maximizando, alfa=float('-inf'), beta=float('inf')):
        """Algoritmo Minimax com poda alfa-beta"""
        resultado = self.verificar_vencedor(tabuleiro)
        
        # Casos base
        if resultado == self.ia:
            return 10 - profundidade
        elif resultado == self.jogador_humano:
            return profundidade - 10
        elif resultado == 0:
            return 0
        
        if eh_maximizando:
            melhor_valor = float('-inf')
            for i in range(9):
                if tabuleiro[i] == 0:
                    tabuleiro[i] = self.ia
                    valor = self.minimax(tabuleiro, profundidade + 1, False, alfa, beta)
                    tabuleiro[i] = 0
                    melhor_valor = max(melhor_valor, valor)
                    alfa = max(alfa, valor)
                    if beta <= alfa:
                        break
            return melhor_valor
        else:
            melhor_valor = float('inf')
            for i in range(9):
                if tabuleiro[i] == 0:
                    tabuleiro[i] = self.jogador_humano
                    valor = self.minimax(tabuleiro, profundidade + 1, True, alfa, beta)
                    tabuleiro[i] = 0
                    melhor_valor = min(melhor_valor, valor)
                    beta = min(beta, valor)
                    if beta <= alfa:
                        break
            return melhor_valor
    
    def melhor_movimento(self, tabuleiro):
        """Encontra o melhor movimento para a IA"""
        # Primeira jogada estratégica
        if all(cell == 0 for cell in tabuleiro):
            estrategicos = [0, 2, 4, 6, 8]  # Cantos e centro
            return random.choice(estrategicos)
        
        melhor_valor = float('-inf')
        melhor_movimento = 0
        
        for i in range(9):
            if tabuleiro[i] == 0:
                tabuleiro_copia = tabuleiro.copy()
                tabuleiro_copia[i] = self.ia
                valor = self.minimax(tabuleiro_copia, 0, False)
                
                if valor > melhor_valor:
                    melhor_valor = valor
                    melhor_movimento = i
        
        return melhor_movimento

class GameRequestHandler(BaseHTTPRequestHandler):
    """Handler para requisições HTTP do jogo"""
    
    def __init__(self, *args, **kwargs):
        self.ia_jogo = JogoDaVelhaIA()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            self.serve_html()
        elif parsed_path.path == '/favicon.ico':
            self.send_error(404)
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/move':
            self.handle_ai_move()
        else:
            self.send_error(404)
    
    def serve_html(self):
        """Serve o arquivo HTML principal"""
        try:
            with open('index.html', 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            # Adiciona JavaScript para comunicação com o servidor Python
            api_js = """
            <script>
            // Substituir a função melhorMovimento original por uma que chama a API Python
            JogoDaVelha.prototype.melhorMovimento = async function() {
                try {
                    const response = await fetch('/api/move', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            board: this.tabuleiro
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error('Erro na API');
                    }
                    
                    const data = await response.json();
                    return data.move;
                } catch (error) {
                    console.error('Erro ao comunicar com a IA Python:', error);
                    // Fallback para a IA JavaScript original
                    return this.melhorMovimentoFallback();
                }
            };
            
            // Backup da IA JavaScript original
            JogoDaVelha.prototype.melhorMovimentoFallback = function() {
                let melhorValor = -Infinity;
                let melhorMovimento = 0;

                if (this.tabuleiro.every(cell => cell === 0)) {
                    const estrategicos = [0, 2, 4, 6, 8];
                    return estrategicos[Math.floor(Math.random() * estrategicos.length)];
                }

                for (let i = 0; i < 9; i++) {
                    if (this.tabuleiro[i] === 0) {
                        this.tabuleiro[i] = this.ia;
                        const valor = this.minimax(0, false, -Infinity, Infinity);
                        this.tabuleiro[i] = 0;

                        if (valor > melhorValor) {
                            melhorValor = valor;
                            melhorMovimento = i;
                        }
                    }
                }

                return melhorMovimento;
            };
            
            // Modificar a jogada da IA para ser assíncrona
            JogoDaVelha.prototype.jogadaIA = async function() {
                if (!this.jogoAtivo) return;

                const melhorJogada = await this.melhorMovimento();
                this.tabuleiro[melhorJogada] = this.ia;
                this.atualizarCelula(melhorJogada, 'O', 'o');

                const resultado = this.verificarVencedor();
                if (resultado !== null) {
                    this.finalizarJogo(resultado);
                } else {
                    this.atualizarStatus('Sua vez! Clique em uma casa para jogar.');
                }
            };
            </script>
            """
            
            # Insere o JavaScript antes do fechamento do body
            html_content = html_content.replace('</body>', f'{api_js}</body>')
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-length', len(html_content.encode('utf-8')))
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except FileNotFoundError:
            self.send_error(404, "Arquivo index.html não encontrado")
        except Exception as e:
            self.send_error(500, f"Erro interno: {str(e)}")
    
    def handle_ai_move(self):
        """Processa movimento da IA via API"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            tabuleiro = data.get('board', [0] * 9)
            
            # Converte o tabuleiro JavaScript para formato Python
            # JavaScript: X=1, O=-1 -> Python: X=1, O=-1 (já está correto)
            melhor_movimento = self.ia_jogo.melhor_movimento(tabuleiro)
            
            response_data = {
                'move': melhor_movimento,
                'success': True
            }
            
            response_json = json.dumps(response_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-length', len(response_json.encode('utf-8')))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response_json.encode('utf-8'))
            
        except Exception as e:
            error_response = json.dumps({
                'error': str(e),
                'success': False
            })
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-length', len(error_response.encode('utf-8')))
            self.end_headers()
            self.wfile.write(error_response.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Customiza as mensagens de log"""
        print(f"🌐 {self.address_string()} - {format % args}")

def open_browser(port):
    """Abre o navegador após um delay"""
    time.sleep(1.5)  # Aguarda o servidor inicializar
    url = f"http://localhost:{port}"
    print(f"🚀 Abrindo {url} no navegador...")
    webbrowser.open(url)

def main():
    """Função principal"""
    PORT = 8000
    
    # Verifica se o arquivo index.html existe
    if not os.path.exists('index.html'):
        print("❌ Erro: Arquivo 'index.html' não encontrado!")
        print("📝 Certifique-se de que o arquivo index.html está na mesma pasta que este script.")
        return
    
    # Configura o servidor
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, GameRequestHandler)
    
    print("🎮 === JOGO DA VELHA - SERVIDOR WEB ===")
    print(f"🌐 Servidor rodando em: http://localhost:{PORT}")
    print("🤖 IA Minimax integrada via Python!")
    print("⚡ Pressione Ctrl+C para parar o servidor")
    print("-" * 50)
    
    # Abre o navegador em uma thread separada
    browser_thread = threading.Thread(target=open_browser, args=(PORT,))
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
        httpd.server_close()
        print("👋 Obrigado por jogar!")

if __name__ == "__main__":
    main()