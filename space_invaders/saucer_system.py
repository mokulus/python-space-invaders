"""
Provides :class:`SaucerSystem`, :class:`Saucer`, :class:`SaucerExplosion`
"""
from space_invaders import assets, game_object, player_bullet, system, util
from space_invaders.explosion import Explosion
from space_invaders.point import Point


class SaucerExplosion(Explosion):
    """
    Represents the exploding saucer. Spawn a score information explosion when
    it ends.
    """

    def __init__(self, game, position, color):
        self._game = game
        super().__init__(position, assets.saucer_explosion(), color, 16)

    def tick(self):
        super().tick()
        if self._frames == 0:
            score = self._game.settings.saucer_score()
            self._game.add_score(score)
            sprite = util.text_to_sprite(f"{score:3}")
            obj = Explosion(self._position, sprite, self.color, 60)
            self._game.spawn(obj)


class Saucer(game_object.GameObject):
    """
    Saucer that spawns above aliens and has score based on number of shots
    fired by the player.
    """

    def __init__(self, game):
        super().__init__()
        self.color = (255, 0, 0)
        self._game = game
        y = 208
        if game.player.shots_fired() % 2 == 0:
            self._position = Point(0, y)
            self._velocity = Point(2, 0)
        else:
            self._position = Point(
                self._game.settings.width() - self.sprite().shape[0] - 1, y
            )
            self._velocity = Point(-2, 0)

    def position(self):
        return self._position

    def sprite(self):
        return assets.saucer()

    def tick(self):
        if self._game.ticks() % 3 == 0:
            self._position += self._velocity
        if (
            not 0
            <= self._position.x
            < self._game.settings.width() - self.sprite().shape[0]
        ):
            self.alive = False

    def on_collision(self, other):
        if isinstance(other, player_bullet.PlayerBullet):
            obj = SaucerExplosion(self._game, self._position, self.color)
            self._game.spawn(obj)
            self.alive = False


class SaucerSystem(system.System):
    """
    `System` that manages `Saucer` spawns.
    """

    def __init__(self, game):
        self._game = game
        self._ticks = 0
        self._saucer = None

    def tick(self):
        if self._game.player.dying():
            return
        if self._saucer is None or not self._saucer.alive:
            self._ticks += 1
            if self._ticks == self._game.settings.saucer_period():
                self._ticks = 0
                self._saucer = Saucer(self._game)
                self._game.spawn(self._saucer)
