import pygame

from config import ACCENT, ACCENT_2, PANEL, SHADOW, TEXT


class Button:
    def __init__(self, rect, text, action, width=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.hovered = False
        self.width = width

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

    def draw(self, screen, font):
        shadow = self.rect.move(4, 5)
        pygame.draw.rect(screen, SHADOW, shadow, border_radius=14)
        color = ACCENT_2 if self.hovered else ACCENT
        pygame.draw.rect(screen, color, self.rect, border_radius=14)
        pygame.draw.rect(screen, PANEL, self.rect, width=2, border_radius=14)
        text_surf = font.render(self.text, True, TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
