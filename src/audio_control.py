# This class handles all audio for Markov Music.
# Its functions can be called by both ChordSelection and Playback.

from common.clock import *
from common.core import *
from common.audio import *
from common.mixer import *
from common.synth import *
from building_block import *
import random

class AudioController(object):
    def __init__(self, channel=0, patch=(0,1)):
        super(AudioController, self).__init__()
        self.channel = channel
        self.patch = patch

        # Set up synth.
        self.audio = Audio(2)
        self.synth = Synth("data/FluidR3_GM.sf2")
        self.bpm = 96
        self.tempo_map = SimpleTempoMap(self.bpm)
        self.sched = AudioScheduler(self.tempo_map)
        self.synth.program(self.channel, self.patch[0], self.patch[1])
        self.audio.set_generator(self.sched)
        self.sched.set_generator(self.synth)
        self.tick_duration = 60./self.bpm / kTicksPerQuarter

        self.time_chords = []

        # Keep track of current preview cmds.
        self.previews = []

        # Set up ability to modulate.
        self.transpose_steps = 0

    def transpose(self, steps):
        self.transpose_steps += steps

    def get_current_chord(self):
        now = self.sched.get_tick()
        prev_chord = None
        for time_chord in self.time_chords:
            if now < time_chord[0]:
                return prev_chord
            prev_chord = time_chord[1]
        return prev_chord


    def play_phrase(self, phrase):
        self.play_progression(phrase.get_chords())

    def play_progression(self, chords):
        now = self.sched.get_tick()
        now = now - (now % kTicksPerQuarter) + kTicksPerQuarter
        for chord_idx in range(len(chords)):
            chord = chords[chord_idx]
            time = now + chord_idx * 4 * kTicksPerQuarter
            self.time_chords.append((time,chord))
            self.sched.post_at_tick(time, self.play_scheduled_chord, chord)

    def play_preview(self, chords):
        self.clear_previous_previews()
        now = self.sched.get_tick()
        now = now - (now % kTicksPerQuarter) + kTicksPerQuarter
        for chord_idx in range(len(chords)):
            chord = chords[chord_idx]
            time = now + chord_idx * kTicksPerQuarter
            self.previews.append(self.sched.post_at_tick(time, self.play_scheduled_chord, chord))

    def clear_previous_previews(self):
        for preview_cmd in self.previews:
            self.sched.remove(preview_cmd)
        self.previews = []

    def touch_down_block_handler(self, x_block, y_block, num_x_blocks=10):
        chord = self.get_current_chord()
        melody_notes = chord.get_possible_melody_notes()
        base_index = int(x_block * float(len(melody_notes))/num_x_blocks)
        lower = max(0, base_index - 1)
        upper = min(len(melody_notes) - 1, base_index + 1)
        possible_notes = melody_notes[lower:upper + 1]
        note = random.choice(possible_notes)
        
        divider = y_block + 1
        now = self.sched.get_tick()
        time = now - (now % (kTicksPerQuarter / divider)) + (kTicksPerQuarter / divider)
        self.sched.post_at_tick(time,self.play_scheduled_note, (note, kTicksPerQuarter * self.tick_duration / divider))

    def play_scheduled_note(self,tick, note_duration_tuple):
        note = note_duration_tuple[0]
        duration = note_duration_tuple[1]
        self.play_note(note, duration=duration, synth_settings = (0, 5))

    def play_scheduled_chord(self, tick, chord):
        self.play_chord(chord, .9)

    def play_chord(self, chord, duration=1):
        notes = chord.get_notes()
        print notes
        for note in notes:
            self.play_note(note, duration=duration)

    def set_exact_transpose(self, transpose_steps):
        self.transpose_steps = transpose_steps

    def play_note(self, pitch, velocity=100, duration=1, synth_settings = (0,1)):
        pitch = pitch + self.transpose_steps
        now = self.sched.get_tick()
        self.synth.program(self.channel,synth_settings[0],synth_settings[1])
        self.synth.noteon(self.channel, pitch, velocity)
        self.sched.post_at_tick(now + int(duration * kTicksPerQuarter),
                                self.note_off, pitch)
        self.synth.program(self.channel,self.patch[0],self.patch[1])

    def note_off(self, tick, pitch):
        self.synth.noteoff(self.channel, pitch)

    def on_update(self):
        self.audio.on_update()
