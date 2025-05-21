import pygame
import sys
import random

# Inicialização
pygame.init()
WIDTH, HEIGHT = 900, 650  # Tela um pouco maior
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stone Reigns: O Renascimento Científico")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)
DARK_GRAY = (100, 100, 100)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
BLUE = (52, 152, 219)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)

# Fontes
try:
    title_font = pygame.font.Font("assets/fonts/OpenSans-Bold.ttf", 48)
    large_font = pygame.font.Font("assets/fonts/OpenSans-Regular.ttf", 36)
    font = pygame.font.Font("assets/fonts/OpenSans-Regular.ttf", 24)
    small_font = pygame.font.Font("assets/fonts/OpenSans-Light.ttf", 18)
except:
    title_font = pygame.font.SysFont("arial", 48, bold=True)
    large_font = pygame.font.SysFont("arial", 36)
    font = pygame.font.SysFont("arial", 24)
    small_font = pygame.font.SysFont("arial", 18)

# Efeitos sonoros
try:
    click_sound = pygame.mixer.Sound("assets/sounds/click.wav")
    success_sound = pygame.mixer.Sound("assets/sounds/success.wav")
    failure_sound = pygame.mixer.Sound("assets/sounds/failure.wav")
    has_audio = True
except:
    has_audio = False

# Imagens de fundo
try:
    bg_images = {
        1: pygame.image.load("assets/images/bg1.jpg").convert(),
        2: pygame.image.load("assets/images/bg2.jpg").convert(),
        3: pygame.image.load("assets/images/bg3.jpg").convert()
    }
    for i in bg_images:
        bg_images[i] = pygame.transform.scale(bg_images[i], (WIDTH, HEIGHT))
    has_images = True
except:
    has_images = False

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
    "objetivo": "Sobreviver aos primeiros dias",
    "inimigos": ["Fome", "Frio", "Animais selvagens"],
    "aliados": [],
    "eventos": []
}

fase_1 = [
    {
        "contexto": "Ao acordar, você encontra outros despertos, mas assustados. A noite se aproxima e o frio é intenso.",
        "pergunta": "Ensinar a criar fogo com atrito?",
        "sim": {"Ciência": +5, "Recursos": -2, "Energia": +5},
        "nao": {"População": -3},
        "explicacao": "Você esfregou madeira seca até criar brasas. O fogo aquece o grupo e afasta predadores.",
        "imagem": "fire" if has_images else None
    },
    {
        "contexto": "Uma grande pedra bloqueia o caminho para um vale fértil. Seus companheiros desistem.",
        "pergunta": "Construir alavanca para mover a pedra?",
        "sim": {"Recursos": -3, "População": +5},
        "nao": {"População": -4},
        "explicacao": "Com uma vara longe e uma rocha como fulcro, a pedra foi movida! O vale agora é seu.",
        "imagem": "lever" if has_images else None
    },
    {
        "contexto": "A água do rio está contaminada. Doenças começam a se espalhar.",
        "pergunta": "Filtrar água com areia e carvão?",
        "sim": {"Ciência": +4, "População": +3},
        "nao": {"População": -5},
        "explicacao": "Você criou um sistema de filtragem que remove impurezas, salvando muitos doentes.",
        "imagem": "water" if has_images else None
    }
]

fase_2 = [
    {
        "contexto": "O Clã dos Olhos Vermelhos ataca com armas primitivas. Você precisa de uma vantagem.",
        "pergunta": "Construir baterias para armas elétricas rudimentares?",
        "sim": {"Energia": +7, "Recursos": -3, "Ciência": +5},
        "nao": {"Energia": -4},
        "explicacao": "Os limões com placas de metal criam choques que assustam os invasores!",
        "imagem": "battery" if has_images else None
    },
    {
        "contexto": "As doenças continuam a se espalhar. Um aldeão sugere usar plantas medicinais.",
        "pergunta": "Investigar propriedades medicinais das plantas?",
        "sim": {"Ciência": +6, "População": +5, "Recursos": -4},
        "nao": {"População": -7},
        "explicacao": "Você descobriu antibióticos naturais! A saúde da vila melhora drasticamente.",
        "imagem": "medicine" if has_images else None
    }
]

fase_3 = [
    {
        "contexto": "Uma tempestade solar ameaça destruir seus equipamentos eletrônicos primitivos.",
        "pergunta": "Construir um para-raios e gaiola de Faraday?",
        "sim": {"Ciência": +8, "Recursos": -6, "Energia": +5},
        "nao": {"Energia": -10, "Ciência": -5},
        "explicacao": "Você protegeu seus dispositivos! A vila agora tem proteção contra tempestades.",
        "imagem": "lightning" if has_images else None
    },
    {
        "contexto": "Os alimentos básicos estão escassos. Um aldeão sugere agricultura científica.",
        "pergunta": "Implementar sistema de rotação de culturas?",
        "sim": {"População": +8, "Recursos": +5, "Ciência": +3},
        "nao": {"População": -7, "Recursos": -5},
        "explicacao": "Sua colheita triplicou! A fome foi erradicada na vila.",
        "imagem": "farm" if has_images else None
    }
]

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Card:
    def __init__(self, data):
        self.pergunta = data["pergunta"]
        self.sim = data["sim"]
        self.nao = data["nao"]
        self.explicacao = data.get("explicacao", "")
        self.contexto = data.get("contexto", "")
        self.imagem = data.get("imagem", None)
        
    def draw(self, surface):
        # Fundo do card
        pygame.draw.rect(surface, GRAY, (50, 150, WIDTH-100, 350), border_radius=15)
        pygame.draw.rect(surface, DARK_GRAY, (50, 150, WIDTH-100, 350), 2, border_radius=15)
        
        # Contexto narrativo
        if self.contexto:
            y_offset = 170
            for line in self._wrap_text(self.contexto, 80):
                text = small_font.render(line, True, BLACK)
                surface.blit(text, (70, y_offset))
                y_offset += 25
                
            # Linha divisória
            pygame.draw.line(surface, DARK_GRAY, (70, y_offset+10), (WIDTH-70, y_offset+10), 2)
            y_offset += 30
        
        # Pergunta
        for line in self._wrap_text(self.pergunta, 60):
            text = font.render(line, True, BLACK)
            surface.blit(text, (70, y_offset))
            y_offset += 30
        
        # Botões (agora desenhados separadamente)
        
    def _wrap_text(self, text, max_len):
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            if len(' '.join(current_line + [word])) <= max_len:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines

    def aplicar_decisao(self, escolha):
        efeitos = self.sim if escolha == "sim" else self.nao
        for chave, valor in efeitos.items():
            status[chave] = max(0, min(100, status[chave] + valor))
        historia["progresso"] += 1
        return self.explicacao

def desenhar_barras():
    x = 50
    bar_height = 25
    for i, (nome, valor) in enumerate(status.items()):
        # Barra de fundo
        pygame.draw.rect(screen, DARK_GRAY, (x, 80, 180, bar_height), border_radius=5)
        
        # Barra de progresso
        color = BLUE if i == 0 else GREEN if i == 1 else YELLOW if i == 2 else PURPLE
        pygame.draw.rect(screen, color, (x, 80, 180 * (valor / 100), bar_height), border_radius=5)
        
        # Borda
        pygame.draw.rect(screen, BLACK, (x, 80, 180, bar_height), 2, border_radius=5)
        
        # Texto
        label = small_font.render(f"{nome}: {valor}", True, BLACK)
        screen.blit(label, (x + 5, 80 + (bar_height - label.get_height()) // 2))
        x += 190

def desenhar_info_historia():
    # Capítulo e objetivo
    cap_text = font.render(f"Capítulo {historia['capitulo']}: {historia['objetivo']}", True, BLACK)
    screen.blit(cap_text, (50, 120))
    
    # Inimigos e aliados (em uma barra lateral)
    pygame.draw.rect(screen, (240, 240, 240), (WIDTH-250, 50, 200, HEIGHT-100), border_radius=10)
    pygame.draw.rect(screen, DARK_GRAY, (WIDTH-250, 50, 200, HEIGHT-100), 2, border_radius=10)
    
    title = small_font.render("Situação Atual", True, BLACK)
    screen.blit(title, (WIDTH-240, 60))
    
    # Inimigos
    enemy_title = small_font.render("Desafios:", True, RED)
    screen.blit(enemy_title, (WIDTH-240, 90))
    
    y_offset = 120
    for enemy in historia["inimigos"]:
        enemy_text = small_font.render(f"- {enemy}", True, BLACK)
        screen.blit(enemy_text, (WIDTH-230, y_offset))
        y_offset += 25
    
    # Aliados
    ally_title = small_font.render("Aliados:", True, GREEN)
    screen.blit(ally_title, (WIDTH-240, y_offset + 10))
    y_offset += 40
    
    for ally in historia["aliados"]:
        ally_text = small_font.render(f"- {ally}", True, BLACK)
        screen.blit(ally_text, (WIDTH-230, y_offset))
        y_offset += 25
    
    # Eventos importantes
    if historia["eventos"]:
        event_title = small_font.render("Marcos:", True, BLUE)
        screen.blit(event_title, (WIDTH-240, y_offset + 10))
        y_offset += 40
        
        for event in historia["eventos"][-3:]:  # Mostra apenas os 3 últimos
            event_text = small_font.render(f"- {event}", True, BLACK)
            screen.blit(event_text, (WIDTH-230, y_offset))
            y_offset += 25

def escolher_fase():
    media = sum(status.values()) / len(status)
    if media < 40:
        return fase_1
    elif media < 70:
        return fase_2
    else:
        return fase_3

def escolher_nova_carta(cartas, ultima_pergunta):
    nova = random.choice(cartas)
    while ultima_pergunta and nova["pergunta"] == ultima_pergunta.pergunta and len(cartas) > 1:
        nova = random.choice(cartas)
    return Card(nova)

def atualizar_historia():
    media = sum(status.values()) / len(status)
    
    if media < 40:
        new_chapter = 1
        objetivo = "Sobreviver aos primeiros dias"
        inimigos = ["Fome", "Frio", "Animais selvagens"]
        aliados = []
    elif media < 70:
        new_chapter = 2
        objetivo = "Estabelecer uma vila segura"
        inimigos = ["Clã dos Olhos Vermelhos"]
        aliados = ["Caçadores despertos"]
    else:
        new_chapter = 3
        objetivo = "Reconstruir a civilização"
        inimigos = ["Tropas de Obsidian"]
        aliados = ["Vila da Primavera", "Sábio do Vale"]
    
    if historia["capitulo"] != new_chapter:
        historia["eventos"].append(f"Capítulo {new_chapter} alcançado!")
        if has_audio:
            success_sound.play()
    
    historia.update({
        "capitulo": new_chapter,
        "objetivo": objetivo,
        "inimigos": inimigos,
        "aliados": aliados
    })

def verificar_eventos():
    # Evento do Laboratório
    if status["Ciência"] >= 70 and "Laboratório" not in historia["aliados"]:
        historia["aliados"].append("Laboratório")
        historia["eventos"].append("Laboratório construído!")
        carta_especial = {
            "contexto": "Você construiu um laboratório primitivo! Os aldeões trazem materiais curiosos.",
            "pergunta": "Estudar os materiais para novas invenções?",
            "sim": {"Ciência": +10, "Recursos": -5},
            "nao": {"População": +5},
            "explicacao": "Você descobriu como purificar metais! A Idade do Bronze começa."
        }
        if has_audio:
            success_sound.play()
        return Card(carta_especial)
    
    # Evento da Universidade
    if historia["capitulo"] == 3 and "Universidade" not in historia["aliados"] and status["Ciência"] >= 80:
        historia["aliados"].append("Universidade")
        historia["eventos"].append("Universidade fundada!")
        carta_especial = {
            "contexto": "Seus conhecimentos atraíram sábios de outras vilas. Eles propõem uma escola.",
            "pergunta": "Fundar uma universidade primitiva?",
            "sim": {"Ciência": +15, "População": +10, "Recursos": -10},
            "nao": {"Ciência": -5, "População": +3},
            "explicacao": "A Universidade de Petra se torna centro do conhecimento! Novas gerações de cientistas florescem."
        }
        if has_audio:
            success_sound.play()
        return Card(carta_especial)
    
    return None

def menu_inicial():
    while True:
        if has_images:
            screen.blit(bg_images[1], (0, 0))
        else:
            screen.fill(BLUE)
            
        # Título
        title = title_font.render("STONE REIGNS", True, WHITE)
        subtitle = large_font.render("O Renascimento Científico", True, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2 - 40))
        
        # Instrução
        instruction = font.render("Pressione ENTER para começar", True, WHITE)
        screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//2 + 50))
        
        # Créditos
        credits = small_font.render("Use a ciência para reconstruir a civilização em um mundo pós-apocalíptico", True, WHITE)
        screen.blit(credits, (WIDTH//2 - credits.get_width()//2, HEIGHT - 50))
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                if has_audio:
                    click_sound.play()
                return

def tela_explicacao(explicacao):
    screen.fill(WHITE)
    
    # Título
    title = large_font.render("Resultado", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    # Explicação
    y_offset = 180
    for line in Card._wrap_text(None, explicacao, 80):
        text = font.render(line, True, BLACK)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, y_offset))
        y_offset += 30
    
    # Botão de continuar
    continue_btn = Button(WIDTH//2 - 100, HEIGHT - 100, 200, 50, "Continuar", GREEN, (46, 184, 113))
    continue_btn.draw(screen)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        mouse_pos = pygame.mouse.get_pos()
        continue_btn.check_hover(mouse_pos)
        continue_btn.draw(screen)
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if continue_btn.is_clicked(mouse_pos, evento):
                if has_audio:
                    click_sound.play()
                waiting = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                if has_audio:
                    click_sound.play()
                waiting = False

def fim_de_jogo():
    if any(valor == 0 for valor in status.values()):
        title = "Fracasso"
        message = "Sua vila não sobreviveu... A humanidade permanece na idade das trevas."
        color = RED
    else:
        title = "Vitória!"
        message = "Você liderou o renascimento científico! A civilização floresce novamente."
        color = GREEN
    
    while True:
        if has_images:
            screen.blit(bg_images[3 if title == "Vitória!" else 2], (0, 0))
        else:
            screen.fill(BLACK if title == "Fracasso" else BLUE)
            
        # Título
        title_text = title_font.render(title, True, color)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 100))
        
        # Mensagem
        y_offset = HEIGHT//2 - 30
        for line in Card._wrap_text(None, message, 70):
            text = large_font.render(line, True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, y_offset))
            y_offset += 40
        
        # Instruções
        instruction = font.render("Pressione R para reiniciar ou ESC para sair", True, WHITE)
        screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT - 100))
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    if has_audio:
                        click_sound.play()
                    # Reiniciar valores
                    for chave in status:
                        status[chave] = 50
                    historia.update({
                        "capitulo": 1,
                        "progresso": 0,
                        "objetivo": "Sobreviver aos primeiros dias",
                        "inimigos": ["Fome", "Frio", "Animais selvagens"],
                        "aliados": [],
                        "eventos": []
                    })
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Inicialização do jogo
menu_inicial()

# Configuração inicial
cartas = escolher_fase()
ultima_pergunta = None
carta_atual = escolher_nova_carta(cartas, ultima_pergunta)
ultima_pergunta = carta_atual
explicacao_atual = ""

# Botões
sim_btn = Button(150, 450, 200, 60, "Sim (D)", GREEN, (46, 184, 113))
nao_btn = Button(550, 450, 200, 60, "Não (A)", RED, (231, 86, 70))

# Loop principal
running = True
while running:
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Verificar hover nos botões
        sim_btn.check_hover(mouse_pos)
        nao_btn.check_hover(mouse_pos)
        
        # Cliques do mouse
        if sim_btn.is_clicked(mouse_pos, evento):
            if has_audio:
                click_sound.play()
            explicacao_atual = carta_atual.aplicar_decisao("sim")
            cartas = escolher_fase()
            carta_atual = escolher_nova_carta(cartas, ultima_pergunta)
            ultima_pergunta = carta_atual
            
        if nao_btn.is_clicked(mouse_pos, evento):
            if has_audio:
                click_sound.play()
            explicacao_atual = carta_atual.aplicar_decisao("nao")
            cartas = escolher_fase()
            carta_atual = escolher_nova_carta(cartas, ultima_pergunta)
            ultima_pergunta = carta_atual
        
        # Teclado
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_d:
                if has_audio:
                    click_sound.play()
                explicacao_atual = carta_atual.aplicar_decisao("sim")
                cartas = escolher_fase()
                carta_atual = escolher_nova_carta(cartas, ultima_pergunta)
                ultima_pergunta = carta_atual
            elif evento.key == pygame.K_a:
                if has_audio:
                    click_sound.play()
                explicacao_atual = carta_atual.aplicar_decisao("nao")
                cartas = escolher_fase()
                carta_atual = escolher_nova_carta(cartas, ultima_pergunta)
                ultima_pergunta = carta_atual
    
    # Atualização
    atualizar_historia()
    evento_especial = verificar_eventos()
    if evento_especial:
        carta_atual = evento_especial
    
    # Renderização
    if has_images:
        screen.blit(bg_images[historia["capitulo"]], (0, 0))
    else:
        screen.fill(WHITE)
    
    # Desenhar elementos da UI
    desenhar_barras()
    desenhar_info_historia()
    
    # Desenhar card atual
    carta_atual.draw(screen)
    
    # Desenhar botões
    sim_btn.draw(screen)
    nao_btn.draw(screen)
    
    # Explicação (se houver)
    if explicacao_atual:
        tela_explicacao(explicacao_atual)
        explicacao_atual = ""
    
    # Verificar condições de fim de jogo
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