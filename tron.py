# MIT License
# 
# Copyright (c) 2013 Steven Kowal
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import procgame.game
import pinproc
import trough
import attract

class FirstMode(procgame.game.Mode):
    def __init__(self, game):
        super(FirstMode, self).__init__(game=game, priority=5)

    def sw_startButton_active(self, sw):
        self.game.lamps.startButton.schedule(schedule=0xff00ff00,cycle_seconds=0, now=True)
        self.game.coils.popB.pulse(50)
        self.game.lamps.shootAgain.pulse(50) # Turn on indefinitely.
        return procgame.game.SwitchStop


class BaseGameMode(procgame.game.Mode):
    def __init__(self, game):
        super(BaseGameMode, self).__init__(game=game, priority=1)
        pass

    def mode_started(self):
        self.game.trough.changed_handlers.append(self.trough_changed)

    def mode_stopped(self):
        self.game.trough.changed_handlers.remove(self.trough_changed)

    def trough_changed(self):
        if self.game.trough.is_full():
            self.game.end_ball()

    def sw_videoGameEject_active_for_1s(self, sw):
		self.game.coils.flasherVideoGame.pulsed_patter(50,50,250,True)
		self.game.coils.videoGameEject.pulse()

    def sw_popL_active_for_200ms(self, sw):
        self.game.coils.popL.pulse()
        self.game.lamps.popL.pulse(50)

    def sw_popR_active_for_200ms(self, sw):
        self.game.coils.popR.pulse()
        self.game.lamps.popR.pulse(50)

    def sw_popB_active_for_200ms(self, sw):
        self.game.coils.popB.pulse()
        self.game.lamps.popB.pulse(50)


class TronGame(procgame.game.BasicGame):

    trough = None
    basic_game_mode = None

    def __init__(self):
        super(TronGame, self).__init__(pinproc.MachineTypeSternSAM)
        self.load_config('tron.yaml')
        self.trough = trough.Trough(game=self)
        self.base_game_mode = BaseGameMode(game=self)
        self.attract_mode = attract.Attract(game=self)
        self.reset()

    def reset(self):
        super(TronGame, self).reset()
        self.modes.add(self.trough)
        self.modes.add(self.attract_mode)

    def start_ball(self):
        super(TronGame, self).start_ball()

    def game_started(self):
        self.log("GAME STARTED")
        super(TronGame, self).game_started()
        # don't start_ball here

    def ball_starting(self):
        self.log("BALL STARTING")
        super(TronGame, self).ball_starting()
        # TODO: Frist Check for ball in shooter lane
        # TODO: Next, puslse trough until ball shows up in the
        # shooter lane
       
        # Eject a ball into the shooter lane.
        self.coils.trough.pulse()

        self.enable_flippers(True)
        self.modes.add(self.base_game_mode)

    def ball_ended(self):
        """Called by end_ball(), which is itslef called by base_game_mode.trough_changed """
        self.log("BALL ENDED")
        self.modes.remove(self.base_game_mode)
        self.enable_flippers(False)
        super(TronGame, self).ball_ended()

    def game_ended(self):
        self.log("GAME_ENDED")
        super(TronGame, self).game_ended()
        self.modes.remove(self.base_game_mode)
        self.modes.add(self.attract_mode)

## main:
def main():
    game = None
    try:
        game = TronGame()
        game.run_loop()
    finally:
        del game

if __name__ == '__main__':
    main()

