import pygame

from config import PANEL, TEXT


class HUD:
    def __init__(self, title_font, text_font):
        self.title_font = title_font
        self.text_font = text_font

    def draw_panel(self, screen):
        panel = pygame.Rect(25, 18, screen.get_width() - 50, 110)
        pygame.draw.rect(screen, PANEL, panel, border_radius=18)
        pygame.draw.rect(screen, (50, 66, 98), panel, width=2, border_radius=18)

    def draw(self, screen, score, turns, time_left, message=""):
        self.draw_panel(screen)

        title = self.title_font.render("Desafio das Cartas", True, TEXT)
        screen.blit(title, (45, 32))

        info = f"Pares: {score}   Tentativas: {turns}   Tempo: {time_left:02d}s"
        info_surf = self.text_font.render(info, True, TEXT)
        screen.blit(info_surf, (45, 74))

        if message:
            msg = self.text_font.render(message, True, TEXT)
            screen.blit(msg, (45, 96))