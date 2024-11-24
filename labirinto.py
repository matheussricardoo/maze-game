import pygame
import random
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Labirinto")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
CINZA = (100, 100, 100)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
AZUL = (0, 100, 255)
ROXO = (147, 0, 211)
DOURADO = (255, 215, 0)

class Idioma:
    def __init__(self):
        self.atual = "pt"  # Começa em português
        self.textos = {
            "pt": {
                "titulo": "LABIRINTO",
                "subtitulo": "Escolha a dificuldade",
                "facil": "Fácil",
                "medio": "Médio",
                "dificil": "Difícil",
                "controles": "Controles:",
                "mover": "Use as setas para Mover",
                "voltar": "ESC : Voltar ao Menu",
                "reiniciar": "R : Reiniciar após morte",
                "objetivo": "Objetivo:",
                "objetivo_desc": "Chegue ao portal roxo",
                "aviso": "sem tocar nas paredes!",
                "pressione_tecla": "Pressione qualquer tecla para começar!",
                "voce_venceu": "VOCÊ VENCEU!",
                "tempo": "Tempo: {} segundos",
                "proximo": "Pressione ENTER para próximo nível",
                "menu": "ESC para menu principal",
                "game_over": "GAME OVER",
                "reiniciar_r": "R para Reiniciar",
                "menu_esc": "ESC para Menu"
            },
            "en": {
                "titulo": "MAZE",
                "subtitulo": "Choose difficulty",
                "facil": "Easy",
                "medio": "Medium",
                "dificil": "Hard",
                "controles": "Controls:",
                "mover": "Use arrow keys to Move",
                "voltar": "ESC : Back to Menu",
                "reiniciar": "R : Restart after death",
                "objetivo": "Objective:",
                "objetivo_desc": "Reach the purple portal",
                "aviso": "without touching the walls!",
                "pressione_tecla": "Press any key to start!",
                "voce_venceu": "YOU WIN!",
                "tempo": "Time: {} seconds",
                "proximo": "Press ENTER for next level",
                "menu": "ESC for main menu",
                "game_over": "GAME OVER",
                "reiniciar_r": "R to Restart",
                "menu_esc": "ESC for Menu"
            }
        }
    
    def trocar(self):
        self.atual = "en" if self.atual == "pt" else "pt"
    
    def get(self, chave):
        return self.textos[self.atual][chave]

# Crie uma instância global do idioma
idioma = Idioma()

class Botao:
    def __init__(self, x, y, largura, altura, texto, cor, callback=None):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.cor_hover = tuple(min(c + 30, 255) for c in cor)
        self.fonte = pygame.font.Font(None, 36)
        self.callback = callback

    def executar(self):
        if self.callback:
            self.callback()

    def desenhar(self, tela):
        cor = self.cor_hover if self.rect.collidepoint(pygame.mouse.get_pos()) else self.cor
        pygame.draw.rect(tela, cor, self.rect, border_radius=12)
        pygame.draw.rect(tela, BRANCO, self.rect, 3, border_radius=12)
        
        texto_surface = self.fonte.render(self.texto, True, BRANCO)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        tela.blit(texto_surface, texto_rect)
        
    def clicado(self, pos):
        return self.rect.collidepoint(pos)

class Jogador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 5
        self.tamanho = 20
        self.vivo = True
        self.rastro = []
        
    def mover(self, teclas, obstaculos):
        if not self.vivo:
            return
            
        novo_x = self.x
        novo_y = self.y
        
        if teclas[pygame.K_LEFT]:
            novo_x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            novo_x += self.velocidade
        if teclas[pygame.K_UP]:
            novo_y -= self.velocidade
        if teclas[pygame.K_DOWN]:
            novo_y += self.velocidade
            
        for obstaculo in obstaculos:
            if obstaculo.colide_com(novo_x, novo_y, self.tamanho):
                self.morrer()
                return
                
        self.rastro.append((self.x, self.y))
        if len(self.rastro) > 10:
            self.rastro.pop(0)
                
        self.x = max(0, min(LARGURA - self.tamanho, novo_x))
        self.y = max(0, min(ALTURA - self.tamanho, novo_y))
    
    def morrer(self):
        self.vivo = False
            
    def desenhar(self, tela):
        # Desenha rastro
        for i, (x, y) in enumerate(self.rastro):
            alpha = i / len(self.rastro) * 255
            s = pygame.Surface((self.tamanho, self.tamanho))
            s.set_alpha(alpha)
            s.fill(AZUL)
            tela.blit(s, (x, y))
        
        # Desenha jogador
        cor = VERDE if self.vivo else VERMELHO
        pygame.draw.rect(tela, cor, (self.x, self.y, self.tamanho, self.tamanho))
        # Brilho
        pygame.draw.rect(tela, BRANCO, (self.x, self.y, self.tamanho, self.tamanho), 2)

class Objetivo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tamanho = 30
        self.pulso = 0
        self.particulas = []
        
    def atualizar(self):
        self.pulso = (self.pulso + 0.1) % (2 * math.pi)
        
        # Atualiza partículas
        if random.random() < 0.2:
            angulo = random.uniform(0, 2 * math.pi)
            velocidade = random.uniform(1, 3)
            self.particulas.append({
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angulo) * velocidade,
                'vy': math.sin(angulo) * velocidade,
                'vida': 1.0
            })
            
        for p in self.particulas[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vida'] -= 0.02
            if p['vida'] <= 0:
                self.particulas.remove(p)
        
    def desenhar(self, tela):
        # Desenha partículas
        for p in self.particulas:
            raio = int(5 * p['vida'])
            alpha = int(255 * p['vida'])
            s = pygame.Surface((raio*2, raio*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*DOURADO, alpha), (raio, raio), raio)
            tela.blit(s, (p['x']-raio, p['y']-raio))
        
        # Desenha portal
        tamanho = self.tamanho + math.sin(self.pulso) * 5
        
        # Círculos concêntricos com gradiente
        for i in range(3):
            t = tamanho * (1 - i*0.2)
            cor = tuple(c * (1 - i*0.2) for c in ROXO)
            pygame.draw.circle(tela, cor, (self.x, self.y), t)
        
        # Brilho central
        pygame.draw.circle(tela, BRANCO, (self.x, self.y), tamanho * 0.3)

def menu_principal():
    botoes = [
        Botao(LARGURA//2 - 100, 200, 200, 50, idioma.get("facil"), VERDE),
        Botao(LARGURA//2 - 100, 300, 200, 50, idioma.get("medio"), AMARELO),
        Botao(LARGURA//2 - 100, 400, 200, 50, idioma.get("dificil"), VERMELHO),
        # Botão de idioma no canto superior direito
        Botao(LARGURA - 100, 10, 90, 30, "EN/PT", AZUL, idioma.trocar)
    ]
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, botao in enumerate(botoes):
                    if botao.clicado(evento.pos):
                        if i == 3:  # Botão de idioma
                            botao.executar()
                            # Atualiza os textos dos botões após trocar o idioma
                            botoes[0].texto = idioma.get("facil")
                            botoes[1].texto = idioma.get("medio")
                            botoes[2].texto = idioma.get("dificil")
                        else:
                            return i + 1
                        
        tela.fill(PRETO)
        
        # Título
        fonte_titulo = pygame.font.Font(None, 74)
        titulo = fonte_titulo.render(idioma.get("titulo"), True, BRANCO)
        tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 50))
        
        # Subtítulo
        fonte_sub = pygame.font.Font(None, 36)
        subtitulo = fonte_sub.render(idioma.get("subtitulo"), True, BRANCO)
        tela.blit(subtitulo, (LARGURA//2 - subtitulo.get_width()//2, 120))
        
        # Botões
        for botao in botoes:
            texto = botao.texto() if callable(botao.texto) else botao.texto
            botao.texto = texto  # Atualiza o texto do botão
            botao.desenhar(tela)
        
        # Instruções
        fonte_instrucoes = pygame.font.Font(None, 28)
        instrucoes = [
            idioma.get("controles"),
            idioma.get("mover"),
            idioma.get("voltar"),
            idioma.get("reiniciar"),
            "",
            idioma.get("objetivo"),
            idioma.get("objetivo_desc"),
            idioma.get("aviso")
        ]
        
        y = 480
        for linha in instrucoes:
            texto = fonte_instrucoes.render(linha, True, BRANCO)
            tela.blit(texto, (LARGURA//2 - texto.get_width()//2, y))
            y += 25
            
        pygame.display.flip()

def gerar_labirinto(nivel):
    obstaculos = []
    TAMANHO_CELULA = 40 - nivel * 5  # Células menores em níveis mais difíceis
    LARGURA_PAREDE = TAMANHO_CELULA // 3
    
    # Calcula número de células
    colunas = LARGURA // TAMANHO_CELULA
    linhas = ALTURA // TAMANHO_CELULA
    
    # Cria grade
    grade = [[1 for _ in range(colunas)] for _ in range(linhas)]
    
    def criar_caminho(x, y):
        grade[y][x] = 0
        direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(direcoes)
        
        for dx, dy in direcoes:
            novo_x, novo_y = x + dx*2, y + dy*2
            if (0 <= novo_x < colunas and 0 <= novo_y < linhas and 
                grade[novo_y][novo_x] == 1):
                grade[y + dy][x + dx] = 0
                criar_caminho(novo_x, novo_y)
    
    # Gera o labirinto começando do centro
    criar_caminho(1, 1)
    
    # Converte a grade em obstáculos
    for y in range(linhas):
        for x in range(colunas):
            if grade[y][x] == 1:
                px = x * TAMANHO_CELULA
                py = y * TAMANHO_CELULA
                
                # Adiciona parede com efeito de gradiente
                class ParedeComGradiente:
                    def __init__(self, x, y, largura, altura):
                        self.x = x
                        self.y = y
                        self.largura = largura
                        self.altura = altura
                        
                    def colide_com(self, x, y, tamanho):
                        return (x < self.x + self.largura and 
                                x + tamanho > self.x and 
                                y < self.y + self.altura and 
                                y + tamanho > self.y)
                    
                    def desenhar(self, tela):
                        # Desenha parede com gradiente
                        base_cor = (80, 80, 100)
                        pygame.draw.rect(tela, base_cor, 
                                       (self.x, self.y, self.largura, self.altura))
                        
                        # Adiciona brilho na borda superior
                        brilho = pygame.Surface((self.largura, 5))
                        for i in range(5):
                            alpha = 255 - (i * 50)
                            brilho.fill((200, 200, 220))
                            brilho.set_alpha(alpha)
                            tela.blit(brilho, (self.x, self.y + i))
                
                obstaculos.append(ParedeComGradiente(px, py, TAMANHO_CELULA, TAMANHO_CELULA))
    
    # Garante que o caminho inicial e final estejam livres
    obstaculos = [obs for obs in obstaculos if not (
        obs.colide_com(40, 40, 20) or  # Área inicial
        obs.colide_com(LARGURA-80, ALTURA-80, 40)  # Área do objetivo
    )]
    
    return obstaculos

def jogar(nivel):
    jogador = Jogador(40, 40)
    objetivo = Objetivo(LARGURA-60, ALTURA-60)
    obstaculos = gerar_labirinto(nivel)
    
    # Mostra instruções iniciais
    tela.fill(PRETO)
    fonte = pygame.font.Font(None, 48)
    texto = fonte.render(idioma.get("pressione_tecla"), True, BRANCO)
    tela.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2))
    pygame.display.flip()
    
    # Espera tecla
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                esperando = False
    
    tempo_inicio = pygame.time.get_ticks()
    rodando = True
    clock = pygame.time.Clock()
    
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r and not jogador.vivo:
                    return True
                elif evento.key == pygame.K_ESCAPE:
                    return False
        
        teclas = pygame.key.get_pressed()
        jogador.mover(teclas, obstaculos)
        objetivo.atualizar()
        
        if jogador.vivo and (abs(jogador.x - objetivo.x) < 20 and 
            abs(jogador.y - objetivo.y) < 20):
            # Tela de vitória
            tela.fill(PRETO)
            tempo_final = (pygame.time.get_ticks() - tempo_inicio) / 1000
            
            mensagens = [
                idioma.get("voce_venceu"),
                idioma.get("tempo").format(f"{tempo_final:.1f}"),
                "",
                idioma.get("proximo"),
                idioma.get("menu")
            ]
            
            y = ALTURA//2 - len(mensagens)*30
            for msg in mensagens:
                texto = fonte.render(msg, True, VERDE if idioma.get("voce_venceu") in msg else BRANCO)
                tela.blit(texto, (LARGURA//2 - texto.get_width()//2, y))
                y += 60
                
            pygame.display.flip()
            
            # Espera decisão do jogador
            esperando = True
            while esperando:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        return False
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_RETURN:
                            return True
                        if ev.key == pygame.K_ESCAPE:
                            return False
            
            return True
        
        # Desenha
        tela.fill(PRETO)
        for obstaculo in obstaculos:
            obstaculo.desenhar(tela)
        objetivo.desenhar(tela)
        jogador.desenhar(tela)
        
        if not jogador.vivo:
            fonte = pygame.font.Font(None, 48)
            mensagens = [
                idioma.get("game_over"),
                idioma.get("reiniciar_r"),
                idioma.get("menu_esc")
            ]
            y = ALTURA//2 - len(mensagens)*30
            for msg in mensagens:
                texto = fonte.render(msg, True, VERMELHO if idioma.get("game_over") in msg else BRANCO)
                tela.blit(texto, (LARGURA//2 - texto.get_width()//2, y))
                y += 60
            
        pygame.display.flip()
        clock.tick(60)

def main():
    while True:
        nivel = menu_principal()
        if nivel is None:
            break
            
        while jogar(nivel):
            pass  # Continua jogando até perder ou sair
            
    pygame.quit()

if __name__ == "__main__":
    main() 