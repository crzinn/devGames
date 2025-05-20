import pygame
import sys
import random

# Inicialização
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stone Reigns")
clock = pygame.time.Clock()

# Sons
##pygame.mixer.init()
#click_sound = pygame.mixer.Sound(pygame.mixer.Sound(file=None))  # Substitua por um arquivo real se quiser
#background_music = pygame.mixer.Sound(pygame.mixer.Sound(file=None))  # Substitua por um arquivo real se quiser
# pygame.mixer.Sound.play(background_music, loops=-1)  # Descomente ao usar um arquivo válido

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (100, 200, 100)
RED = (200, 100, 100)

font = pygame.font.SysFont(None, 28)
large_font = pygame.font.SysFont(None, 48)

# Barras de status
status = {
    "Ciência": 50,
    "Recursos": 50,
    "População": 50,
    "Energia": 50
}

fase_1 = [
    {"pergunta": "Criar fogo com atrito?", "sim": {"Ciência": +5, "Recursos": -2, "Energia": +5}, "nao": {"População": -3}, "explicacao": "Você criou fogo com fricção, usando calor gerado pelo atrito."},
    {"pergunta": "Construir alavanca para mover pedra?", "sim": {"Recursos": -3, "População": +5}, "nao": {"População": -4}, "explicacao": "Você usou uma alavanca, aplicando a Lei de Arquimedes."},
    {"pergunta": "Filtrar água com areia e carvão?", "sim": {"Ciência": +4, "População": +3}, "nao": {"População": -5}, "explicacao": "Você usou filtração com carvão ativado, removendo impurezas da água."},
    {"pergunta": "Criar tinta natural para registrar descobertas?", "sim": {"Ciência": +5, "Recursos": -2}, "nao": {"Ciência": -3}, "explicacao": "Você extraiu pigmentos naturais de frutas e plantas para criar tinta."}
]

fase_2 = [
    {"pergunta": "Construir bateria com cobre e limão?", "sim": {"Energia": +7, "Recursos": -3, "Ciência": +5}, "nao": {"Energia": -4}, "explicacao": "Você criou uma célula galvânica com ácido cítrico e metais condutores."},
    {"pergunta": "Produzir sabão com gordura animal?", "sim": {"População": +5, "Recursos": -4}, "nao": {"População": -6}, "explicacao": "Você fez sabão por saponificação, misturando gordura e cinzas."},
    {"pergunta": "Fazer vidro com areia e calor intenso?", "sim": {"Ciência": +6, "Recursos": -5}, "nao": {"Ciência": -3}, "explicacao": "Você derreteu areia rica em sílica para formar vidro."},
    {"pergunta": "Consertar rádio para comunicação?", "sim": {"Energia": -4, "Ciência": +7, "População": +3}, "nao": {"População": -5}, "explicacao": "Você reconectou circuitos para restaurar ondas de rádio."}
]

class Card:
    def __init__(self, data):
        self.pergunta = data["pergunta"]
        self.sim = data["sim"]
        self.nao = data["nao"]
        self.explicacao = data.get("explicacao", "")

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, (150, 200, 500, 200))
        text = font.render(self.pergunta, True, BLACK)
        surface.blit(text, (160, 250))
        sim_text = font.render("[D] Sim", True, GREEN)
        nao_text = font.render("[A] Não", True, RED)
        surface.blit(sim_text, (160, 330))
        surface.blit(nao_text, (600, 330))

    def aplicar_decisao(self, escolha):
        # pygame.mixer.Sound.play(click_sound)
        efeitos = self.sim if escolha == "sim" else self.nao
        for chave, valor in efeitos.items():
            status[chave] = max(0, min(100, status[chave] + valor))
        return self.explicacao

# Função para desenhar barras
def desenhar_barras():
    x = 50
    for nome, valor in status.items():
        pygame.draw.rect(screen, BLACK, (x, 50, 150, 20))
        pygame.draw.rect(screen, GREEN, (x, 50, 150 * (valor / 100), 20))
        label = font.render(f"{nome}: {valor}", True, BLACK)
        screen.blit(label, (x, 25))
        x += 180

# Escolher fase com base na média dos status
def escolher_fase():
    media = sum(status.values()) / len(status)
    return fase_1 if media < 65 else fase_2

# Menu inicial
def menu_inicial():
    screen.fill(WHITE)
    titulo = large_font.render("Stone Reigns", True, BLACK)
    instrucao = font.render("Pressione ENTER para começar", True, BLACK)
    screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, HEIGHT//2 - 60))
    screen.blit(instrucao, (WIDTH//2 - instrucao.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperando = False

# Fim de jogo
def fim_de_jogo():
    screen.fill(WHITE)
    fim = large_font.render("Fim de jogo!", True, RED)
    instrucao = font.render("Pressione R para reiniciar ou ESC para sair", True, BLACK)
    screen.blit(fim, (WIDTH//2 - fim.get_width()//2, HEIGHT//2 - 60))
    screen.blit(instrucao, (WIDTH//2 - instrucao.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    for chave in status:
                        status[chave] = 50
                    esperando = False
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Início
menu_inicial()
rodando = True
cartas = escolher_fase()
carta_atual = Card(random.choice(cartas))
explicacao_atual = ""

while rodando:
    screen.fill(WHITE)
    desenhar_barras()
    carta_atual.draw(screen)
    if explicacao_atual:
        explic_text = font.render(explicacao_atual, True, BLACK)
        screen.blit(explic_text, (WIDTH//2 - explic_text.get_width()//2, 420))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_d:
                explicacao_atual = carta_atual.aplicar_decisao("sim")
                cartas = escolher_fase()
                carta_atual = Card(random.choice(cartas))
            elif evento.key == pygame.K_a:
                explicacao_atual = carta_atual.aplicar_decisao("nao")
                cartas = escolher_fase()
                carta_atual = Card(random.choice(cartas))

    if any(valor == 0 or valor == 100 for valor in status.values()):
        fim_de_jogo()
        cartas = escolher_fase()
        carta_atual = Card(random.choice(cartas))
        explicacao_atual = ""

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
