import pygame

from config import BACKGROUND, DANGER, TEXT, WIDTH
from src.scenes.base import Scene
from src.ui.button import Button


class GameOverScene(Scene):
    def __init__(self, game, won, score, turns):
        super().__init__(game)
        self.won = won
        self.score = score
        self.turns = turns
        self.title_font = pygame.font.SysFont("arial", 54, bold=True)
        self.text_font = pygame.font.SysFont("arial", 24)
        self.buttons = [
            Button((WIDTH // 2 - 130, 420, 260, 56), "Jogar de novo", self.restart),
            Button((WIDTH // 2 - 130, 490, 260, 56), "Menu", self.menu),
        ]

    def restart(self):
        from src.scenes.gameplay import GameScene
        self.game.change_scene(GameScene(self.game))

    def menu(self):
        from src.scenes.menu import MenuScene
        self.game.change_scene(MenuScene(self.game))

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                button.handle_event(event)

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(BACKGROUND)
        title = "Voce venceu!" if self.won else "Fim de jogo"
        title_color = TEXT if self.won else DANGER
        title_surf = self.title_font.render(title, True, title_color)
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, 220)))

        lines = [
            f"Pares encontrados: {self.score}",
            f"Tentativas: {self.turns}",
        ]
        y = 290
        for line in lines:
            surf = self.text_font.render(line, True, TEXT)
            screen.blit(surf, surf.get_rect(center=(WIDTH // 2, y)))
            y += 38

        for button in self.buttons:
            button.draw(screen, self.text_font)
