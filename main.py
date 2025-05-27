import pygame
import sys
import random

# Inicialização
pygame.init()
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stone Reigns")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (100, 200, 100)
RED = (200, 100, 100)

font = pygame.font.SysFont(None, 28)
large_font = pygame.font.SysFont(None, 48)

# Carregar imagens
fundo_img = pygame.image.load("cenario.png")
fundo_img = pygame.transform.scale(fundo_img, (WIDTH, HEIGHT))

personagem_img = pygame.image.load("personagem.png")
personagem_img = pygame.transform.scale(personagem_img, (300, 400))

# Barras de status e história
status = {
    "Ciência": 50,
    "Recursos": 50,
    "População": 50,
    "Energia": 50
}

historia = {
    "capitulo": 1,
    "progresso": 0,
    "objetivo": "Estabelecer uma vila segura",
    "inimigos": ["Clã dos Olhos Vermelhos", "Tropas de Obsidian"],
    "aliados": []
}

fase_1 = [
    {
        "contexto": "Ao acordar, você encontra outros despertos, mas assustados. A noite se aproxima e o frio é intenso.",
        "pergunta": "Ensinar a criar fogo com atrito?",
        "sim": {"Ciência": +5, "Recursos": -2, "Energia": +5},
        "nao": {"População": -3},
        "explicacao": "Você esfregou madeira seca até criar brasas. O fogo aquece o grupo e afasta predadores."
    },
    {
        "contexto": "Uma grande pedra bloqueia o caminho para um vale fértil. Seus companheiros desistem.",
        "pergunta": "Construir alavanca para mover a pedra?",
        "sim": {"Recursos": -3, "População": +5},
        "nao": {"População": -4},
        "explicacao": "Com uma vara longa e uma rocha como fulcro, a pedra foi movida! O vale agora é seu."
    },
    {
        "contexto": "A água do rio está contaminada. Doenças começam a se espalhar.",
        "pergunta": "Filtrar água com areia e carvão?",
        "sim": {"Ciência": +4, "População": +3},
        "nao": {"População": -5},
        "explicacao": "Você criou um sistema de filtragem que remove impurezas, salvando muitos doentes."
    }
]

fase_2 = [
    {
        "contexto": "O Clã dos Olhos Vermelhos ataca com armas primitivas. Você precisa de uma vantagem.",
        "pergunta": "Construir baterias para armas elétricas rudimentares?",
        "sim": {"Energia": +7, "Recursos": -3, "Ciência": +5},
        "nao": {"Energia": -4},
        "explicacao": "Os limões com placas de metal criam choques que assustam os invasores!"
    },
    {
        "contexto": "As doenças continuam a se espalhar. Um aldeão sugere usar plantas medicinais.",
        "pergunta": "Investigar propriedades medicinais das plantas?",
        "sim": {"Ciência": +6, "População": +5, "Recursos": -4},
        "nao": {"População": -7},
        "explicacao": "Você descobriu antibióticos naturais! A saúde da vila melhora drasticamente."
    }
]

class Card:
    def __init__(self, data):
        self.pergunta = data["pergunta"]
        self.sim = data["sim"]
        self.nao = data["nao"]
        self.explicacao = data.get("explicacao", "")
        self.contexto = data.get("contexto", "")

    def draw(self, surface):
        card_rect = pygame.Rect(150, 480, 780, 200)
        pygame.draw.rect(surface, (230, 230, 230), card_rect, border_radius=12)

        contexto_lines = [self.contexto[i:i + 70] for i in range(0, len(self.contexto), 70)]
        for i, line in enumerate(contexto_lines):
            text = font.render(line, True, BLACK)
            surface.blit(text, (card_rect.x + 20, card_rect.y + 20 + i * 20))

        text = font.render(self.pergunta, True, BLACK)
        surface.blit(text, (card_rect.x + 20, card_rect.y + 20 + len(contexto_lines) * 20 + 10))

        sim_text = font.render("[D] Sim", True, GREEN)
        nao_text = font.render("[A] Não", True, RED)
        surface.blit(sim_text, (card_rect.x + 20, card_rect.y + 140))
        surface.blit(nao_text, (card_rect.x + 650, card_rect.y + 140))

    def aplicar_decisao(self, escolha):
        efeitos = self.sim if escolha == "sim" else self.nao
        for chave, valor in efeitos.items():
            status[chave] = max(0, min(100, status[chave] + valor))
        historia["progresso"] += 1
        return self.explicacao

def desenhar_barras():
    x = 50
    for nome, valor in status.items():
        pygame.draw.rect(screen, BLACK, (x, 50, 150, 20))
        pygame.draw.rect(screen, GREEN, (x, 50, 150 * (valor / 100), 20))
        label = font.render(f"{nome}: {valor}", True, BLACK)
        screen.blit(label, (x, 25))
        x += 180

    cap_text = font.render(f"Capítulo {historia['capitulo']}: {historia['objetivo']}", True, BLACK)
    screen.blit(cap_text, (50, 80))

def escolher_fase():
    media = sum(status.values()) / len(status)
    return fase_1 if media < 65 else fase_2

def escolher_nova_carta(cartas, ultima_pergunta):
    nova = random.choice(cartas)
    while ultima_pergunta and nova["pergunta"] == ultima_pergunta.pergunta:
        nova = random.choice(cartas)
    return Card(nova)

def atualizar_historia():
    media = sum(status.values()) / len(status)
    if media < 40:
        historia.update({
            "capitulo": 1,
            "objetivo": "Sobreviver aos primeiros dias",
            "inimigos": ["Fome", "Frio", "Animais selvagens"],
            "aliados": []
        })
    elif media < 65:
        historia.update({
            "capitulo": 2,
            "objetivo": "Estabelecer uma vila segura",
            "inimigos": ["Clã dos Olhos Vermelhos"],
            "aliados": ["Caçadores despertos"]
        })
    else:
        historia.update({
            "capitulo": 3,
            "objetivo": "Reconstruir a civilização",
            "inimigos": ["Tropas de Obsidian"],
            "aliados": ["Vila da Primavera", "Sábio do Vale"]
        })

def verificar_eventos():
    if status["Ciência"] >= 70 and "Laboratório" not in historia["aliados"]:
        historia["aliados"].append("Laboratório")
        carta_especial = {
            "contexto": "Você construiu um laboratório primitivo! Os aldeões trazem materiais curiosos.",
            "pergunta": "Estudar os materiais para novas invenções?",
            "sim": {"Ciência": +10, "Recursos": -5},
            "nao": {"População": +5},
            "explicacao": "Você descobriu como purificar metais! A Idade do Bronze começa."
        }
        return Card(carta_especial)
    return None

def menu_inicial():
    screen.fill(WHITE)
    titulo = large_font.render("Stone Reigns", True, BLACK)
    subtitulo = font.render("O Renascimento Científico", True, BLACK)
    instrucao = font.render("Pressione ENTER para começar", True, BLACK)

    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(subtitulo, (WIDTH // 2 - subtitulo.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(instrucao, (WIDTH // 2 - instrucao.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperando = False

def fim_de_jogo():
    screen.fill(WHITE)
    if any(valor == 0 for valor in status.values()):
        mensagem = "Sua vila não sobreviveu... A humanidade permanece na idade das trevas."
    else:
        mensagem = "Você liderou o renascimento científico! A civilização floresce novamente."

    fim = large_font.render("Fim de jogo!", True, RED)
    msg = font.render(mensagem, True, BLACK)
    instrucao = font.render("Pressione R para reiniciar ou ESC para sair", True, BLACK)

    screen.blit(fim, (WIDTH // 2 - fim.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(instrucao, (WIDTH // 2 - instrucao.get_width() // 2, HEIGHT // 2 + 20))

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
                    historia.update({
                        "capitulo": 1,
                        "progresso": 0,
                        "objetivo": "Sobreviver aos primeiros dias",
                        "inimigos": ["Fome", "Frio", "Animais selvagens"],
                        "aliados": []
                    })
                    esperando = False
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Início do jogo
menu_inicial()
rodando = True
cartas = escolher_fase()
ultima_pergunta = None
carta_atual = escolher_nova_carta(cartas, ultima_pergunta)
ultima_pergunta = carta_atual
explicacao_atual = ""

while rodando:
    screen.blit(fundo_img, (0, 0))
    personagem_rect = personagem_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(personagem_img, personagem_rect)

    desenhar_barras()

    evento_especial = verificar_eventos()
    if evento_especial:
        carta_atual = evento_especial

    carta_atual.draw(screen)

    if explicacao_atual:
        explic_text = font.render(explicacao_atual, True, BLACK)
        screen.blit(explic_text, (WIDTH // 2 - explic_text.get_width() // 2, 690))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_d:
                explicacao_atual = carta_atual.aplicar_decisao("sim")
                cartas = escolher_fase()
                carta_atual = escolher_nova_carta(cartas, ultima_pergunta)
                ultima_pergunta = carta_atual
            elif evento.key == pygame.K_a:
                explicacao_atual = carta_atual.aplicar_decisao("nao")
                cartas = escolher_fase()
                carta_atual = escolher_nova_carta(cartas, ultima_pergunta)
                ultima_pergunta = carta_atual

    atualizar_historia()

    if any(valor == 0 or valor == 100 for valor in status.values()):
        fim_de_jogo()
        cartas = escolher_fase()
        carta_atual = escolher_nova_carta(cartas, None)
        ultima_pergunta = carta_atual
        explicacao_atual = ""

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
