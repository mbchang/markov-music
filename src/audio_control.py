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
        self.note_gfx = None

        self.time_chords = []
        self.setting = "selection"

        # Keep track of current preview cmds.
        self.previews = []

        self.piano_velocity = 100
        rhythm0 = [960,960]
        rhythm1 = [240,360,240,240,360,240,240]
        rhythm2 = [720,720,480]
        rhythm3 = [320,320,160,320,320,320,160]
        rhythm4 = [480, 960, 480]
        rhythm5 = [120,240,240,240,240,360,240,240]
        self.rhythm_counter = 0
        self.rhythms = [rhythm0,rhythm1,rhythm2,rhythm3,rhythm4,rhythm5]

        # Set up ability to modulate.
        self.transpose_steps = 60  # C Major

    def set_click_gfx(self, function):
        self.click_gfx = function

    def set_note_gfx(self, function):
        self.note_gfx = function

    def get_rhythm_text(self):
        if self.setting == "rhythm":
            return str(self.rhythm_counter)
        else:
            return "<none>"

    def transpose(self, steps):
        self.transpose_steps += steps

    def get_current_chord(self):
        now = self.sched.get_tick()
        prev_chord = Chord()
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
            self.sched.post_at_tick(time, self.play_scheduled_chord_line, chord)

    def play_preview(self, chords):
        self.clear_previous_previews()
        now = self.sched.get_tick()
        now = now - (now % kTicksPerQuarter) + kTicksPerQuarter
        for chord_idx in range(len(chords)):
            chord = chords[chord_idx]
            time = now + chord_idx * kTicksPerQuarter
            self.previews.append(self.sched.post_at_tick(time, self.play_scheduled_chord_line, chord))

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
        self.click_gfx()
        self.play_note(note, duration=duration, synth_settings = (0, 5))

    def play_scheduled_bass_note(self, tick, note_duration_tuple):
        note = note_duration_tuple[0]
        duration = note_duration_tuple[1]
        self.play_note(note, duration=duration, synth_settings = (0, 1))


    def play_scheduled_chord_line(self, tick, chord):
        self.piano_velocity = 100

        if self.setting == "selection":
            self.play_chord(chord, kTicksPerQuarter * self.tick_duration * 0.9)
        if self.setting == "basic":
            self.note_gfx()
            self.play_chord(chord, kTicksPerQuarter * self.tick_duration * 4)
        if self.setting == "arpeggiator":
            self.play_arpeg_chord(chord)
        if self.setting == "rhythm":
            self.piano_velocity = 75
            rhythm = self.rhythms[self.rhythm_counter]
            self.play_rhythm_chord(chord,rhythm)

    def play_scheduled_chord(self, tick, chord_duration):
        self.play_chord(*chord_duration)
        self.note_gfx()



    def play_rhythm_chord(self, chord, rhythm):
        time = self.sched.get_tick()
        for note_duration in rhythm:
            self.sched.post_at_tick(time,self.play_scheduled_chord, (chord,note_duration * self.tick_duration*0.95))
            time += note_duration



    def play_arpeg_chord(self, chord):
        time = self.sched.get_tick()
        for i in range(4):
            self.note_gfx()
            note = chord.get_bottom() - 12
            self.sched.post_at_tick(time,self.play_scheduled_bass_note, (note, kTicksPerQuarter * self.tick_duration / 4))
            time += kTicksPerQuarter/4
            note = chord.get_middle() - 12
            self.sched.post_at_tick(time,self.play_scheduled_bass_note, (note, kTicksPerQuarter * self.tick_duration / 4))
            time += kTicksPerQuarter/4
            note = chord.get_top() - 12
            self.sched.post_at_tick(time,self.play_scheduled_bass_note, (note, kTicksPerQuarter * self.tick_duration / 4))
            time += kTicksPerQuarter/4
            note = chord.get_bottom()
            self.sched.post_at_tick(time,self.play_scheduled_bass_note, (note, kTicksPerQuarter * self.tick_duration / 4))
            time += kTicksPerQuarter/4

    def clear_sounds(self):
        self.sched.clear()

    def set_setting(self, setting):
        self.setting = setting

    def toggle_setting(self, setting):
        if setting == "rhythm":
            self.setting = setting
            self.rhythm_counter = self.rhythm_counter+1 % len(self.rhythms)
        else:
            self.rhythm_counter = 0
            if self.setting == setting:
                self.setting = "basic"
            else:
                self.setting = setting

    def play_chord(self, chord, duration=1):
        notes = chord.get_expanded_notes()
        for note in notes:
            self.play_note(note, duration=duration)

    def set_exact_transpose(self, transpose_steps):
        self.transpose_steps = transpose_steps

    def play_note(self, pitch, velocity=100, duration=1, synth_settings = (0,1)):
        pitch = pitch + self.transpose_steps
        now = self.sched.get_tick()
        self.synth.program(self.channel,synth_settings[0],synth_settings[1])
        self.synth.noteon(self.channel, pitch, self.piano_velocity)
        self.sched.post_at_tick(now + int(duration * kTicksPerQuarter),
                                self.note_off, pitch)
        self.synth.program(self.channel,self.patch[0],self.patch[1])

    def note_off(self, tick, pitch):
        self.synth.noteoff(self.channel, pitch)

    def on_update(self):
        self.audio.on_update()
