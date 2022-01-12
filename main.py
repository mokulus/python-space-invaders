import pygame
import sys
import numpy as np
import game_settings
import game


pygame.init()
screen_size = (game_settings.width(), game_settings.height())
canvas_size = screen_size
screen = pygame.display.set_mode(
    screen_size, flags=pygame.SCALED  # | pygame.RESIZABLE
)
canvas = pygame.Surface(canvas_size)
clock = pygame.time.Clock()

game = game.Game()


def draw_sprite(surfarr, position, sprite):
    img = sprite * 255
    y = canvas_size[1] - position.y - sprite.shape[1]
    x = position.x
    arr[x : x + img.shape[0], y : y + img.shape[1], :] |= img[..., np.newaxis]


running = True

while running:
    shoot = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.exit()
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            shoot = True

    pressed = pygame.key.get_pressed()

    screen.fill((0, 0, 0))
    canvas.fill((0, 0, 0))
    arr = pygame.surfarray.array3d(canvas)
    ticks = pygame.time.get_ticks()
    if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
        game.player.move_left()
    if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
        game.player.move_right()
    if shoot:
        game.player.shoot()
    game.tick()
    game.collision()
    for obj in game.game_objects():
        draw_sprite(arr, obj.position(), obj.sprite())
    pygame.surfarray.blit_array(canvas, arr)
    scaled_canvas = pygame.transform.scale(canvas, screen_size)
    screen.blit(scaled_canvas, (0, 0))
    pygame.display.update()
    clock.tick(60)
