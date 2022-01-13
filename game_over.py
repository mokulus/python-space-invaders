from text_animation import TextAnimation


class GameOver(TextAnimation):
    def __init__(self, game):
        super().__init__(game, 200, "GAME OVER", 30)

    def tick(self):
        super().tick()

        if self.done_once():
            self._game.reset()
