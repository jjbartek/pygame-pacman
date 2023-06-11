from stages.menu_stage import MenuStage
from stages.stage import Stages


class PauseMenuStage(MenuStage):
    CONTINUE_BUTTON = "CONTINUE"
    QUIT_BUTTON = "QUIT"

    def __init__(self):
        super().__init__()

    def _add_buttons(self):
        self._add_button(self.CONTINUE_BUTTON, self._continue_clicked)
        self._add_button(self.QUIT_BUTTON, self._quit_clicked)

    def _continue_clicked(self):
        self.notify(Stages.GAME)

    def _quit_clicked(self):
        self.notify(Stages.QUIT)
