from stages.menu_stage import MenuStage
from stages.stage import Stages


class StartMenuStage(MenuStage):
    START_BUTTON = "START"
    QUIT_BUTTON = "QUIT"

    def __init__(self):
        super().__init__()

    def _add_buttons(self):
        self._add_button(self.START_BUTTON, self._start_game_clicked)
        self._add_button(self.QUIT_BUTTON, self._quit_clicked)

    def _start_game_clicked(self):
        self.notify(Stages.GAME)

    def _quit_clicked(self):
        self.notify(Stages.QUIT)
