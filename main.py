import argparse
import os

import numpy as np
import pygame

from space_invaders.game import Game


def make_parser():
    parser = argparse.ArgumentParser(
        description="Play space invaders.", allow_abbrev=False
    )
    parser.add_argument(
        "--cheats", dest="cheats", action="store_true", help="Enable cheats."
    )
    return parser


def main():
    pygame.init()
    parser = make_parser()
    args = parser.parse_args()
    game = Game(args.cheats)
    game.load_menu()
    screen_size = (game.settings.width(), game.settings.height())
    screen = pygame.display.set_mode(
        screen_size, flags=pygame.SCALED | pygame.RESIZABLE
    )
    clock = pygame.time.Clock()

    def draw_sprite(surfarr, position, sprite, color):
        img = sprite[..., np.newaxis] * np.array(color, dtype=np.uint8)
        y = screen_size[1] - position.y - sprite.shape[1]
        x = position.x
        sx = img.shape[0]
        sy = img.shape[1]
        arr[x : x + sx, y : y + sy, :] |= img

    running = True

    while running:
        shoot = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.exit()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot = True

        pressed = pygame.key.get_pressed()

        screen.fill((0, 0, 0))
        arr = pygame.surfarray.array3d(screen)
        if pressed[pygame.K_RETURN]:
            game.play()
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            if game.player:
                game.player.move_left()
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            if game.player:
                game.player.move_right()
        if (
            shoot
            or pressed[pygame.K_SPACE]
            and game.settings.infinite_bullets()
        ):
            if game.player:
                game.player.shoot()
        game.tick()
        for obj in game.game_objects():
            draw_sprite(arr, obj.position(), obj.sprite(), obj.color)
        pygame.surfarray.blit_array(screen, arr)
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
