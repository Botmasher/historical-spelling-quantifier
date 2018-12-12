# #!/usr/bin/env python

def parse_words(data):
    # break down input and return array of words
    # - input data is raw text file lines like cmu dict
    # ?- or pull data from a source like Wiktionary when given a word list
    # - break data into words
    # - return list of words
    #   - each item in list is [sound, spelling] segments
    #   - phones are already segmented
    #   - try guessing spelling associations starting with one-letter split
    return []

def compare_sound_spelling(word_phones, word_letters):
    # start from sounds and guess mapping letters to sounds
    # - consider place in word and try to assign each letter to one or more sounds
    # - could one sound be silence?
    # - account for digraphs or trigraphs
    # - or try naive scrambled version mapping sounds across the set
    #   - regardless of place?
    #   - for this you need to build and adjust data across words

def start():
    # get words and score spelling vs sounds
    # - parse data into a long list of words
    # - run each word through the sound-spelling comparison
    # - aggregate sound-spelling comparison data and make calculations
    #   - this step requires multiple comparative steps
    #   - this step also requires taking info from across words
    return 1.0

if __name__ == '__main__':
    start()
