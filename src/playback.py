''' Contains high level control and logic for the app while in playback mode.
This includes controlling audio and graphical elements. '''

from kivy.clock import Clock as kivyClock

class Playback(object):
    def __init__(self, audio_control, display):
        super(Playback, self).__init__()
        self.audio_control = audio_control
        self.display = display

        self.active = False
        self.phrase = None

    def set_song(self, phrase):
        self.phrase = phrase

    def activate(self):
        self.active = True
        print 'playback activate'
        self.display.activate()

    def inactivate(self):
        self.active = False
        print 'playback inactivate'
        self.display.inactivate()

    def play(self):
        self.audio_control.play_phrase(self.phrase)

    def on_update(self):
        dt = kivyClock.frametime
        self.display.on_update(dt)
        self.audio_control.on_update()
