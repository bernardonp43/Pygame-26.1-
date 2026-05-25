import pygame

from config import CARD_BORDER, CARD_FRONT, CARD_MATCH


class Card:
    def __init__(self, rect, value):
        self.rect = pygame.Rect(rect)
        self.value = value
        self.flipped = False
        self.matched = False

    def contains(self, pos):
        return self.rect.collidepoint(pos)

    def flip(self):
        if not self.matched:
            self.flipped = True

    def hide(self):
        if not self.matched:
            self.flipped = False

    def set_matched(self):
        self.matched = True
        self.flipped = True

    def draw(self, screen, font):
        if self.matched:
            color = CARD_MATCH
        elif self.flipped:
            color = CARD_FRONT
        else:
            color = None

        if color is None:
            pygame.draw.rect(screen, (54, 71, 122), self.rect, border_radius=14)
            inner = self.rect.inflate(-10, -10)
            pygame.draw.rect(screen, (76, 98, 170), inner, border_radius=12)
        else:
            pygame.draw.rect(screen, color, self.rect, border_radius=14)
            inner = self.rect.inflate(-10, -10)
            pygame.draw.rect(screen, (255, 255, 255), inner, width=2, border_radius=12)
            if self.flipped or self.matched:
                label = font.render(str(self.value), True, (25, 34, 52))
                label_rect = label.get_rect(center=self.rect.center)
                screen.blit(label, label_rect)

        pygame.draw.rect(screen, CARD_BORDER, self.rect, width=2, border_radius=14)