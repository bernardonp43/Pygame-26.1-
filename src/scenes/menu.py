import pygame
from src.scenes.gameplay import GameScene
from config import BACKGROUND, PANEL, TEXT, ACCENT, SHADOW, WIDTH, HEIGHT


class MenuScene:
    def __init__(self, game):
        self.game = game

        self.title_font = pygame.font.SysFont("arial", 58, bold=True)
        self.body_font = pygame.font.SysFont("arial", 24)
        self.button_font = pygame.font.SysFont("arial", 30, bold=True)

        self.start_rect = pygame.Rect(0, 0, 260, 58)
        self.exit_rect = pygame.Rect(0, 0, 260, 58)

        self.start_rect.center = (WIDTH // 2, 460)
        self.exit_rect.center = (WIDTH // 2, 535)

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current = ""

        for word in words:
            test = f"{current} {word}".strip()
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word

        if current:
            lines.append(current)

        return lines

    def draw_button(self, screen, rect, label, hover=False):
        shadow_rect = rect.move(0, 6)
        pygame.draw.rect(screen, SHADOW, shadow_rect, border_radius=14)
        pygame.draw.rect(screen, ACCENT if hover else PANEL, rect, border_radius=14)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=14)

        text_surf = self.button_font.render(label, True, TEXT)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.game.change_scene(GameScene(self.game))
                elif event.key == pygame.K_ESCAPE:
                    self.game.running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.start_rect.collidepoint(event.pos):
                    self.game.change_scene(GameScene(self.game))
                elif self.exit_rect.collidepoint(event.pos):
                    self.game.running = False

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(BACKGROUND)

        panel_rect = pygame.Rect(0, 0, 760, 520)
        panel_rect.center = (WIDTH // 2, HEIGHT // 2 - 10)
        pygame.draw.rect(screen, PANEL, panel_rect, border_radius=22)

        title_surf = self.title_font.render("Desafio das Cartas", True, TEXT)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 150))
        screen.blit(title_surf, title_rect)

        subtitle = "Encontre todos os pares antes do tempo acabar."
        subtitle_surf = self.body_font.render(subtitle, True, TEXT)
        subtitle_rect = subtitle_surf.get_rect(center=(WIDTH // 2, 215))
        screen.blit(subtitle_surf, subtitle_rect)

        instructions = [
            "Clique em duas cartas para descobrir o par.",
            "Se as cartas forem iguais, elas ficam abertas.",
            "Se não forem, elas viram de novo em um instante.",
        ]

        y = 255
        for line in instructions:
            line_surf = self.body_font.render(line, True, TEXT)
            line_rect = line_surf.get_rect(center=(WIDTH // 2, y))
            screen.blit(line_surf, line_rect)
            y += 34

        mouse_pos = pygame.mouse.get_pos()
        self.draw_button(screen, self.start_rect, "Jogar", self.start_rect.collidepoint(mouse_pos))
        self.draw_button(screen, self.exit_rect, "Sair", self.exit_rect.collidepoint(mouse_pos))