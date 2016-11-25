# This class handles all audio for Markov Music.
# Its functions can be called by both ChordSelection and Playback.

from common.clock import *
from common.core import *
from common.audio import *
from common.mixer import *
from common.synth import *
from building_block import *

class AudioController(object):
    def __init__(self, channel=0, patch=(0,1)):
        super(AudioController, self).__init__()
        self.channel = channel
        self.patch = patch

        # Set up synth.
        self.audio = Audio(2)
        self.synth = Synth("data/FluidR3_GM.sf2")
        self.tempo_map = SimpleTempoMap(96)
        self.sched = AudioScheduler(self.tempo_map)
        self.synth.program(self.channel, self.patch[0], self.patch[1])
        self.audio.set_generator(self.sched)
        self.sched.set_generator(self.synth)

        # Set up ability to modulate.
        self.transpose_steps = 0

    def transpose(self, steps):
        self.transpose_steps += steps

    def play_phrase(self, phrase):
        self.play_progression(phrase.get_chords())

    def play_progression(self, chords):
        now = self.sched.get_tick()
        now = now - (now % kTicksPerQuarter) + kTicksPerQuarter
        for chord_idx in range(len(chords)):
            chord = chords[chord_idx]
            time = now + chord_idx * kTicksPerQuarter
            self.sched.post_at_tick(time, self.play_scheduled_chord, chord)

    def play_scheduled_chord(self, tick, chord):
        self.play_chord(chord, .9)

    def play_chord(self, chord, duration=1):
        notes = chord.get_notes()
        for note in notes:
            self.play_note(note, duration=duration)

    def set_exact_transpose(self, transpose_steps):
        self.transpose_steps = transpose_steps

    def play_note(self, pitch, velocity=100, duration=1):
        pitch = pitch + self.transpose_steps
        now = self.sched.get_tick()
        self.synth.noteon(self.channel, pitch, velocity)
        self.sched.post_at_tick(now + int(duration * kTicksPerQuarter),
                                self.note_off, pitch)

    def note_off(self, tick, pitch):
        self.synth.noteoff(self.channel, pitch)

    def on_update(self):
        self.audio.on_update()
