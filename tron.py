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

#minor change

class FirstMode(procgame.game.Mode):
  def __init__(self, game):
    super(FirstMode, self).__init__(game=game, priority=5)

  def sw_startButton_active(self, sw):
    print("Start!")
    self.game.lamps.startButton.schedule(schedule=0xff00ff00,cycle_seconds=0, now=True)
    self.game.coils.popB.pulse(50)
    self.game.lamps.shootAgain.pulse(50) # Turn on indefinitely.
    return procgame.game.SwitchStop


class ExampleGame(procgame.game.GameController):
  def __init__(self, machine_type):
    super(ExampleGame, self).__init__(machine_type)
    self.load_config('tron.yaml')

  def reset(self):
    super(ExampleGame, self).reset()
    first_mode = FirstMode(self)
    self.modes.add(first_mode)
    self.enable_flippers(enable=True)

game = ExampleGame(machine_type='sternSAM')
game.reset()
game.run_loop()

