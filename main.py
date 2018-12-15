# #!/usr/bin/env python
import requests
import re

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
    words = []
    for line in lines:
        if len(line) and re.match(r'[A-Za-z]', line[0]):
            segments = line.split()
            spelling = segments[0]
            # filter out words with punctuation or nonbasic shape
            if re.search(r'[^A-Za-z]', spelling):
                continue
            spelling_cleaned = re.split(r'\(', spelling)[0]
            sounds = [re.split(r'[0-9]', segment)[0] for segment in segments[1:]]
            words.append((spelling_cleaned, sounds))
    return words

    # NOTE: filter for "real" words
    # parsed words raise questions, like what to do about
    #   - AAA read as "triple A"
    #   - words with punctuation (hyphens, apostrophes, ...)
    #   - rare or less interesting words
    #   - personal names
    #   - capitalization

def compare_sound_spelling(words_letters_vs_phones, sensitivity=0.1):
    """Compare distance between orthography and phonology in a set of words

    inputs:
        words_letters_vs_phones = [word_0, ... word_n]
        # where each word = ('spelling', ('phone_0', ... 'phone_n'))

        0.0 <= sensitivity <= 1.0
        # used to find letter variant likelihood

    count shape:    {
                        'phone': {          # each found phone
                            'letter': 1,    # count each letter occurrence in every word containing phone
                            ...
                        },
                        ...
                    }
    # then use mapped counts and sensitivity to guess associating letters to each phone

    # TODO: add considering di- and trigraphs during count map

    return =>       0.0 <= distance_value <= 1.0
    """
    # start from sounds and guess mapping letters to sounds
    # - consider place in word and try to assign each letter to one or more sounds
    # - could one sound be silence?
    # - account for digraphs or trigraphs
    # - or try naive scrambled version mapping sounds across the set
    #   - regardless of place?
    #   - for this you need to build and adjust data across words
    letters_present_per_sound = {}

    # TODO: understand and experiment with sensitivity
    sensitivity # clamp 0.0 <= s <= 1.0

    # NOTE: building letters per sound
    # - figure out which letters are present in words that have a sound
    # - assumes that certain sounds will emerge
    #
    # mock example:
    # - input: 'CAT', 'SAD', 'ADD', 'AFTER', 'RAN', 'PASS', 'AS'
    # - expected: associate the sound "/æ/" with the letter "A"
    # - input: 'QUILT', 'CALL', 'CAT', 'CORE', 'KEEP', 'SACK', 'PLACATE', 'SICKER', 'UNIQUE'
    # - expected: associate the sound "/k/" with the letters "C", "K", ("Q(U)"?)
    #
    # uncertainties & issues:
    # - aren't you assuming that letter-sound cooccurrences are noise apart from letter-phone correspondences?
    #   - nonrandom: 'U' after 'Q' (? or expect this as a digraph)
    #   - nonrandom: 'E' is in so many spellings; '/ə/' is such a common phoneme
    # - how does this handle very common sounds?
    #   - think about all of the possible variants for "/ə/"
    # - how does this handle rare letters or rare sounds?
    #   - including less common sounds like EN "/ʒ/" or even "/θ/"
    #   - including rare letter-sound cooccurrences like "zh" for
    # - should we figure Zipf's before tying sounds to letters?
    # - are you able to map both ways, from letters->sounds and sounds->letters?
    #   - GK iotacism leaves one sound -> many letters
    #   - EN vowel shift leave multiple sounds <- per letter
    for word_data in words_letters_vs_phones:
        letters = word_data[0]
        sounds = word_data[1]
        for sound in sounds:
            if sound not in letters_present_per_sound:
                letters_present_per_sound[sound] = {}
            for letter in letters:
                if letter in letters_present_per_sound[sound]:
                    letters_present_per_sound[sound][letter] += 1
                else:
                    letters_present_per_sound[sound][letter] = 1

    # TODO: split finding letter options away from finding polygraphs
    # - map possible di- and trigraphs while iterating through individual words
    # - determine letter variants per sound after all words traversed

    # sort letters per sound by frequency and choose the most common candidates depending on sensitivity
    letter_guesses_per_phone = {}
    for sound in letters_present_per_sound:
        sorted_letters = sorted(letters_present_per_sound[sound].items(), key=lambda k: k[1])

        # sorted letters contain letter count tuple pairs [('letter', n), ...]

        # default guess is the most common letter
        letter_guesses_per_phone[sound] = [sorted_letters[0][0]]
        highest_letter_count = sorted_letters[0][1]

        # variant guesses based on sensitivity
        for letter_and_count in sorted_letters[1:]:
            letter = letter_and_count[0]
            tally = letter_and_count[1]
            if tally >= highest_letter_count - (sensitivity * highest_letter_count):
                letter_guesses_per_phone[sound].append(letter)
            else:
                # letters are sorted by frequency - end loop once reach first nonvariant
                break
        continue

    # count variants per letter and propose an average distance
    average_distance = 0.0
    variants_total = 0
    # determine average number of letters per sound
    for variants in letter_guesses_per_phone.values():
        variants_total += len(variants)     # calc above during prev loop?
    average_variants = variants_total / len(letter_guesses_per_phone.keys())

    print(average_variants)
    return average_variants

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
    words_spellings_sounds = parse_dict_words(dict_txt)
    print(words_spellings_sounds[:5])
    distance = compare_sound_spelling(words_spellings_sounds)
    return distance

if __name__ == '__main__':
    phones_dict_url = "http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b"
    start(phones_dict_url)
