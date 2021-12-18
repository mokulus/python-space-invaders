from alien_grid import AlienGrid
from player import Player
from point import Point
import game_settings


class Game:
    def __init__(self):
        self.alien_grid = AlienGrid(self)
        self.player = Player(self)
        self.bullets = []
        self.explosions = []

    def tick(self):
        self.alien_grid.tick()
        for bullet in self.bullets:
            bullet.tick()
        for explosion in self.explosions:
            explosion.tick()
        self._destroy_bullets()
        self._destroy_explosions()

    def collision(self):
        for bullet in self.bullets[:]:
            for alien in self.alien_grid.aliens():
                if collision(bullet, alien):
                    alien.on_collision(bullet)
                    self.bullets.remove(bullet)

    def drawables(self):
        for alien in self.alien_grid.aliens():
            yield alien
        yield self.player
        for bullet in self.bullets:
            yield bullet
        for explosion in self.explosions:
            yield explosion

    def _destroy_bullets(self):
        for bullet in self.bullets[:]:
            if not inside(
                bullet.position.y,
                bullet.sprite().shape[1],
                game_settings.height(),
            ) or not inside(
                bullet.position.x,
                bullet.sprite().shape[0],
                game_settings.width(),
            ):
                self.bullets.remove(bullet)

    def _destroy_explosions(self):
        for explosion in self.explosions[:]:
            if explosion.frames == 0:
                self.explosions.remove(explosion)


def intersection(a, b):
    minx = max(a.position[0], b.position[0])
    maxx = min(
        a.position[0] + a.sprite().shape[0],
        b.position[0] + b.sprite().shape[0],
    )
    miny = max(a.position[1], b.position[1])
    maxy = min(
        a.position[1] + a.sprite().shape[1],
        b.position[1] + b.sprite().shape[1],
    )
    if minx <= maxx and miny <= maxy:
        return (Point(minx, maxx), Point(miny, maxy))
    else:
        return None


def collision(a, b):
    intersection_rect = intersection(a, b)
    if intersection_rect is None:
        return False
    (minx, maxx), (miny, maxy) = intersection_rect

    def sprite_view(obj):
        return obj.sprite()[
            minx - obj.position[0]: maxx - obj.position[0],
            miny - obj.position[1]: maxy - obj.position[1],
        ]

    if (sprite_view(a) * sprite_view(b)).any():
        return True


def inside(pos, size, max_pos):
    return size <= pos < max_pos - size
