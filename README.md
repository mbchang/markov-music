# markov-music

Action required: create directory 'data' in 'src' and add the FluidSynth sf2 file to it.

To run app, in the src directory, run "python main.py." Right now, clicking will make a note sound, and pressing any key will toggle between chord selection and playback modes (right now the only visual feedback to changing modes is that the red circle will appear and disappear...)

MarkovMusicWidget is the main entry point for the app. It creates display objects, audio_control, and passes them to ChordSelection and Playback. MarkovMusicWidget is in either cs or p mode, and passes along user input events to either ChordSelection or Playback appropriatey.

ChordSelection owns all high level logic and control while the app is in cs mode. It handles click events, queries the Graphs, and sends commands to BlockBuilder, AudioController, and ChordSelectionDisplay.

Playback is the analogous structure to ChordSelection, but for p mode.

There is a single AudioController that is shared by both modes. It controls all sound-producing aspects of the app, which for now is just producing notes. It uses the synth.

A Graph has two methods:
    get_choices(): returns list of next possible chord objects from current state
    make_choice(chord): passes in a chord object and advances the graph object based on that particular choice.

BlockBuilder is a reusable class that facilitates composing blocks together, and can handle adding blocks, removing blocks (to support "undo"), and returning the final composed block.

BuildingBlock and its children, Chord and Phrase, are classes used to encapsulate information about a given chord or phrase, such as its notes, inversion, etc.

Chord objects have the notes that the chord has. You can call get_notes() to get the notes of that particular chord.

Interface
    - Major: 'I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii0'
    - Minor: 'i', 'ii0', 'III+', 'iv', 'v', 'VI', 'vii0'
    - Inversions: 'XR', 'X6', 'X64'
    - Format: '<Roman_Numeral>_[0,*,+]_[R,6,64,7]'
        Example: 'ii_0_64' == 'ii diminished 64'
