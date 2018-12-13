# #!/usr/bin/env python
import requests
import re
#import asyncio

def parse_dict_words(raw_text):
    # break down input and return array of words
    # - input data is raw text file lines like cmu dict
    # ?- or pull data from a source like Wiktionary when given a word list
    # - break data into words
    # - return list of words
    #   - each item in list is [sound, spelling] segments
    #   - phones are already segmented
    #   - try guessing spelling associations starting with one-letter split
    lines = raw_text.split('\n')
    print(len(lines))
    words = []
    counter = 0
    for line in lines:
        if len(line) and re.match(r'[A-Za-z]', line[0]):
            segments = line.split()
            spelling = segments[0]
            # filter out words with punctuation or nonbasic shape
            if re.search(r'[^A-Za-z]', spelling):
                continue
            spelling_cleaned = re.split(r'\(', spelling)[0]
            sounds = [re.split(r'[0-9]', segment)[0] for segment in segments[1:]]
            words.append([spelling_cleaned, sounds])
            counter += 1
        if counter == 20:
            print(words)
        continue
    print(len(words))
    return words

    # NOTE:
    # parsed words raise questions, like what to do about
    #   - AAA read as "triple A"
    #   - words with punctuation (hyphens, apostrophes, ...)
    #   - rare or less interesting words
    #   - personal names
    #   - capitalization

def compare_sound_spelling(word_phones, word_letters):
    # start from sounds and guess mapping letters to sounds
    # - consider place in word and try to assign each letter to one or more sounds
    # - could one sound be silence?
    # - account for digraphs or trigraphs
    # - or try naive scrambled version mapping sounds across the set
    #   - regardless of place?
    #   - for this you need to build and adjust data across words
    return

def open_file(url=""):
    if not url:
        return
    file = requests.get(url)
    return file.text

def start(dict_url=""):
    # get words and score spelling vs sounds
    # - parse data into a long list of words
    # - run each word through the sound-spelling comparison
    # - aggregate sound-spelling comparison data and make calculations
    #   - this step requires multiple comparative steps
    #   - this step also requires taking info from across words
    dict_txt = open_file(url=dict_url)
    if not dict_txt or type(dict_txt) != str:
        return
    words = parse_dict_words(dict_txt)
    return 1.0

if __name__ == '__main__':
    phones_dict_url = "http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b"
    start(phones_dict_url)
