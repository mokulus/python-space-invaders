import os

import numpy as np
import pygame

from game import Game


def main():
    pygame.init()
    game = Game()
    screen_size = (game.settings.width(), game.settings.height())
    canvas_size = screen_size
    screen = pygame.display.set_mode(
        screen_size, flags=pygame.SCALED  # | pygame.RESIZABLE
    )
    canvas = pygame.Surface(canvas_size)
    clock = pygame.time.Clock()

    def draw_sprite(surfarr, position, sprite):
        img = sprite * 255
        y = canvas_size[1] - position.y - sprite.shape[1]
        x = position.x
        sx = img.shape[0]
        sy = img.shape[1]
        arr[x: x + sx, y: y + sy, :] |= img[..., np.newaxis]

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
        if pressed[pygame.K_RETURN]:
            game.play()
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            if game.player:
                game.player.move_left()
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            if game.player:
                game.player.move_right()
        if shoot:
            if game.player:
                game.player.shoot()
        game.tick()
        for obj in game.game_objects():
            draw_sprite(arr, obj.position(), obj.sprite())
        pygame.surfarray.blit_array(canvas, arr)
        scaled_canvas = pygame.transform.scale(canvas, screen_size)
        screen.blit(scaled_canvas, (0, 0))
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
