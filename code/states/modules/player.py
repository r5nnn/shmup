"""Places and blits player, handles user input and collision."""
import pygame.sprite
from .spritesheet import Spritesheet


class Player(pygame.sprite.Sprite):
    def __init__(self, game, stage, sprite_dir, x, y, speed):
        super().__init__()
        self.game = game
        self.stage = stage
        self.basespeed = speed
        self.speed = self.basespeed
        self.spritesheet = Spritesheet(sprite_dir)
        self.player = [[self.spritesheet.parse_sprite('player-sheet ' + i + ' 0.png'), self.spritesheet.parse_sprite('player-sheet ' + i + ' 1.png')] for i
                       in ['idle', 'down', 'left', 'right', 'up']]
        self.modifier_key = 0
        self.player_state = 0
        self.rect = self.player[self.player_state][self.modifier_key].get_rect(center=(x, y))
        self.key_list = []
        self.key_opposite = {
            pygame.K_DOWN: pygame.K_UP,
            pygame.K_UP: pygame.K_DOWN,
            pygame.K_LEFT: pygame.K_RIGHT,
            pygame.K_RIGHT: pygame.K_LEFT
        }
        self.key_speed = {
            pygame.K_UP: -self.speed,
            pygame.K_DOWN: self.speed,
            pygame.K_LEFT: -self.speed,
            pygame.K_RIGHT: self.speed,
        }

    def update(self):
        self.dx, self.dy, self.player_state, self.modifier_key = 0, 0, 0, 0
        for key in self.key_list:
            if key == pygame.K_UP:
                self.dy = -self.speed
                self.player_state = 4
            elif key == pygame.K_DOWN:
                self.dy = self.speed
                self.player_state = 1
            elif key == pygame.K_LEFT:
                self.dx = -self.speed
                self.player_state = 2
            elif key == pygame.K_RIGHT:
                self.dx = self.speed
                self.player_state = 3
        if pygame.K_LSHIFT in self.key_list:
            self.dx /= 2
            self.dy /= 2
            self.modifier_key = 1
        self.rect.move_ip(self.dx, self.dy)

    def render(self, surface):
        self.rect.clamp_ip(surface.get_rect())
        surface.blit(self.player[self.player_state][self.modifier_key], self.rect)

    def on_keydown(self, event) -> None:
        self.key_list.append(event.key) if event.key not in self.key_list else None

    def on_keyup(self, event) -> None:
        self.key_list.remove(event.key) if event.key in self.key_list else None

    def on_exit(self) -> None:
        self.key_list.clear()