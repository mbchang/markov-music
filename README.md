# markov-music

Graph Object has two methods
    get_choices(): returns list of next possible chord objects from current state
    make_choice(chord): passes in a chord object and advances the graph object based on that particular choice.

Chord objects have the notes that the chord has. You can call get_notes() to get the notes of that particular chord

Interface 
    - Major: 'I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii0'
    - Minor: 'i', 'ii0', 'III+', 'iv', 'v', 'VI', 'vii0'
    - Inversions: 'XR', 'X6', 'X64'
