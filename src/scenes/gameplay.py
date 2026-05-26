import pygame

from config import (
    BACKGROUND,
    BOARD_COLS,
    BOARD_ROWS,
    BOTTOM_MARGIN,
    CARD_GAP,
    CARD_H,
    CARD_W,
    HEIGHT,
    LEFT_MARGIN,
    PAIR_COUNT,
    REVEAL_DELAY_MS,
    ROUND_TIME,
    TOP_MARGIN,
    TEXT,
    WIDTH,
)
from src.entities.card import Card
from src.scenes.base import Scene
from src.ui.button import Button
from src.ui.hud import HUD
from src.utils.deck import create_pairs


class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.title_font = pygame.font.SysFont("arial", 30, bold=True)
        self.text_font = pygame.font.SysFont("arial", 22)
        self.small_font = pygame.font.SysFont("arial", 18)
        self.hud = HUD(self.title_font, self.text_font)
        self.back_button = Button((WIDTH - 145, 42, 110, 42), "Menu", self.go_to_menu)
        self.reset()

    def reset(self):
        values = create_pairs(PAIR_COUNT)
        self.cards = []
        idx = 0
        board_width = BOARD_COLS * CARD_W + (BOARD_COLS - 1) * CARD_GAP
        start_x = (WIDTH - board_width) // 2
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                x = start_x + col * (CARD_W + CARD_GAP)
                y = TOP_MARGIN + row * (CARD_H + CARD_GAP)
                self.cards.append(Card((x, y, CARD_W, CARD_H), values[idx]))
                idx += 1

        self.first_card = None
        self.second_card = None
        self.locked = False
        self.turns = 0
        self.score = 0
        self.message = "Clique em duas cartas"
        self.start_ticks = pygame.time.get_ticks()
        self.finish = False
        self.finish_ticks = None

    def go_to_menu(self):
        from src.scenes.menu import MenuScene
        self.game.change_scene(MenuScene(self.game))

    def handle_events(self, events):
        for event in events:
            self.back_button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.locked and not self.finish:
                self.handle_click(event.pos)

    def handle_click(self, pos):
        for card in self.cards:
            if card.contains(pos) and not card.flipped and not card.matched:
                card.flip()
                if self.first_card is None:
                    self.first_card = card
                    self.message = "Escolha a segunda carta"
                else:
                    self.second_card = card
                    self.turns += 1
                    self.locked = True
                    self.message = "Comparando cartas"
                    if self.first_card.value == self.second_card.value:
                        self.first_card.set_matched()
                        self.second_card.set_matched()
                        self.score += 1
                        self.first_card = None
                        self.second_card = None
                        self.locked = False
                        self.message = "Par encontrado!"
                        if self.score == PAIR_COUNT:
                            self.finish = True
                            self.finish_ticks = pygame.time.get_ticks()
                    else:
                        self.hide_after_delay = pygame.time.get_ticks()
                break

    def update(self, dt):
        if self.finish:
            if self.finish_ticks and pygame.time.get_ticks() - self.finish_ticks > 1200:
                from src.scenes.game_over import GameOverScene
                self.game.change_scene(GameOverScene(self.game, True, self.score, self.turns))
            return

        if self.locked and self.first_card and self.second_card and self.first_card.value != self.second_card.value:
            now = pygame.time.get_ticks()
            if now - getattr(self, "hide_after_delay", now) >= REVEAL_DELAY_MS:
                self.first_card.hide()
                self.second_card.hide()
                self.first_card = None
                self.second_card = None
                self.locked = False
                self.message = "Tente novamente"

        elapsed = (pygame.time.get_ticks() - self.start_ticks) // 1000
        if elapsed >= ROUND_TIME:
            from src.scenes.game_over import GameOverScene
            self.game.change_scene(GameOverScene(self.game, False, self.score, self.turns))

    def draw(self, screen):
        screen.fill(BACKGROUND)
        remaining = max(0, ROUND_TIME - ((pygame.time.get_ticks() - self.start_ticks) // 1000))
        self.hud.draw(screen, self.score, self.turns, remaining, self.message)

        for card in self.cards:
            card.draw(screen, self.text_font)

        self.back_button.draw(screen, self.small_font)

        footer = self.small_font.render("Clique nas cartas para formar pares iguais.", True, TEXT)
        screen.blit(footer, (LEFT_MARGIN, HEIGHT - BOTTOM_MARGIN))