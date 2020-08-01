"""This script takes a Chinese text document and creates a list of words in the
document. The words definitions, pinyin and word frequency is added
You can choose to ignore words for import that are above a certain frequency,
or below a certain level on the HSK or TOCFL test
Matthew Delaney 2020"""

import sys
from operator import itemgetter
import os
import logging

folder = os.path.dirname(__file__)
libfolder = os.path.join(folder, '_vendor')
sys.path.insert(0, libfolder)
jieba_dict_large = os.path.join(folder, 'materials/dicts/jieba_dict_large.txt')
hsk_1_6_simp_file = os.path.join(folder, 'materials/HSK_materials/HSK_1-6_simp.txt')
hsk_1_6_trad_file = os.path.join(folder, 'materials/HSK_materials/HSK_1-6_trad.txt')
tocfl_1_5_simp_file = os.path.join(folder, 'materials/TOCFL_materials/TOCFL_1-5_simp.txt')
tocfl_1_5_trad_file = os.path.join(folder, 'materials/TOCFL_materials/TOCFL_1-5_trad.txt')

import jieba
import jieba.posseg
import more_itertools
import wordfreq

from .materials.cc_cedict_materials import cc_cedict_parser

def segment_NLP(text):
    """ Segments newline separated zh input using Jieba NLP, returns a list of
    lists with the words as their first entries """
    word_list = []
    for line in text:
        word_list += jieba.lcut(line, cut_all=False) #accurate mode
    word_list = more_itertools.unique_everseen(word_list)#mimic set uniqueness in list,
                                                        #maintains ordering
    return [[el] for el in word_list] #each word will be its own list with
    #definition and pinyin added as items to the word

def add_pinyin_and_definition(word_list, zh_dict, include_surname_tag):
    """Adds pinyin and definition from zh_dict to entries in hanzi_set. Adds
    english definition as a list of items"""
    #TODO figure out tags vs def
    for word in word_list:
        english_translation_list = []
        if word[0] in zh_dict:
            attrib_list = zh_dict[word[0]]
            for index, attrib in enumerate(attrib_list):
                if index == 0:
                    pass
                elif index == 1: #pinyin
                    word.append(attrib.lower())
                else: #english
                    if 'surname' in attrib:
                        pass
                    else:
                        english_translation_list.append(attrib)
            word.append(english_translation_list)
    word_list = [word for word in word_list if len(word) > 2] #removes all
    #words that where not found in the dictionary
    return word_list

def filter_by_freq(word_list, lower_freq_bound, upper_freq_bound):
    """Filters words based on their relative frequency and adds frequency info
    to the wordlist"""
    filtered_word_list = []
    for word in word_list:
        freq = wordfreq.zipf_frequency(word[0], 'zh', wordlist='large', minimum=0.0)
        if lower_freq_bound <= freq <= upper_freq_bound:
            filtered_word_list.append(word)
    return filtered_word_list

def add_freq(word_list, add_freq_to_output):
    """ Adds frequencies to output """
    if not add_freq_to_output:
        return word_list
    for word in word_list:
        freq = wordfreq.zipf_frequency(word[0], 'zh', wordlist='large',
                minimum=0.0)
        word.append(freq)

    return word_list

def add_parts_of_speech(word_list, add_parts_of_speech):
    if not add_parts_of_speech:
        return word_list
    for word in word_list:
        pos = jieba.posseg.lcut(word[0]) #returns a pair type
        tag = process_part_of_speech(str(pos[0]).split('/')[1])
        word.append(tag)
    return word_list

def process_part_of_speech(pos):
    """Jieba tags parts of speech, this changes their tag into something
    readable for the user. It is not exhaustive, jieba's own docs are not
    exhaustive and the parts of speech part has no translation"""
    pos_dict = {
            'Ag': 'adj morpheme', 'a': 'adj', 'ad': 'adv/adj', 'an': 'adj/noun', 'b':
            'classifier of type', 'c': 'conj', 'dg': 'adv morpheme', 'd': 'adv', 'e': 'exclamation',
            'f': 'direction word', 'g': 'morpheme', 'h': 'prefix', 'i':
            'chengyu', 'j': 'simple morpheme', 'k': 'suffix', 'l': 'idiom', 'm': 'numeral',
            'Ng': 'noun morpheme', 'n': 'noun', 'nr': 'name', 'ns': 'place name',
            'nt': 'time noun', 'nz': 'descriptive noun', 'o': 'onomatopoeia',
            'p': 'preposition', 'q': 'measure word', 'r': 'pronoun', 's':
            'place word', 'tg': 'time morpheme', 't': 'time', 'u': 'auxiliary',
            'vg': 'verb morpheme', 'v': 'verb', 'vd': 'adv/verb', 'vn': 'a name verb',
            'w': 'punctuation', 'x': 'pronumeral', 'y': 'modal verb', 'z': 'descriptive word',
            'un': 'unknown'
            }
    if pos in pos_dict:
        return pos_dict[pos]
    
    return 'unknown'

def remove_hsk_vocab(word_list, hsk_level, simp_or_trad):
    """Filters HSK vocab"""
    hsk_dict = {}
    hsk_removed_list = []
    if simp_or_trad == 'trad':
        with open(hsk_1_6_trad_file, 'r') as h:
            for line in h:
                liness = line.split()
                hsk_dict[liness[0]] = liness[1]
    else:
        with open(hsk_1_6_simp_file, 'r') as h:
            for line in h:
                liness = line.split()
                hsk_dict[liness[0]] = liness[1]
    for word in word_list:
        hanzi = word[0]
        if hanzi in hsk_dict and int(hsk_dict[hanzi]) <= hsk_level:
            pass
        else:
            hsk_removed_list.append(word)
    return hsk_removed_list

def remove_tocfl_vocab(word_list, tocfl_level, simp_or_trad):
    """filters TOCFL vocab"""
    tocfl_dict = {}
    tocfl_removed_list = []
    if simp_or_trad == 'trad':
        with open(tocfl_1_5_trad_file, 'r') as h:
            for line in h:
                liness = line.split()
                tocfl_dict[liness[0]] = liness[1]
    else:
        with open(tocfl_1_5_simp_file, 'r') as h:
            for line in h:
                liness = line.split()
                tocfl_dict[liness[0]] = liness[1]
    for word in word_list:
        hanzi = word[0]
        if hanzi in tocfl_dict and int(tocfl_dict[hanzi]) <= tocfl_level:
            pass
        else:
            tocfl_removed_list.append(word)
    return tocfl_removed_list

def sort_by_freq(word_list, ascending, freq_sort):
    if not freq_sort:
        return word_list
    return sorted(word_list, key=itemgetter(1), reverse=ascending)

def save_generated_list(word_list, location):
    #deprecated
    with open(location + '.txt', 'w+') as g:
        for word in word_list:
            for part in word:
                if isinstance(part, list):
                    for elem in part:
                        g.write(str(elem)+'; ')
                    g.write('\t')
                else:
                    g.write(str(part)+'\t')
            g.write('\n')

def analyse(zh_input, freq_sort, add_freq_to_output, hsk_level, tocfl_level,
        simp_or_trad, add_speech_parts, upper_freq_bound, lower_freq_bound,
        deck_name, include_surname_tag):
    """Parses text and applies filters"""
    cc_cedict_parser.QUIET = True
    zh_dict = cc_cedict_parser.parse_dict(simp_or_trad)
    jieba.setLogLevel(logging.ERROR)
    jieba.initialize()
    jieba.set_dictionary(jieba_dict_large)

    word_list = segment_NLP(zh_input)
    word_list = filter_by_freq(word_list, lower_freq_bound, upper_freq_bound)
    word_list = remove_hsk_vocab(word_list, hsk_level, simp_or_trad)
    word_list = remove_tocfl_vocab(word_list, tocfl_level, simp_or_trad)
    word_list = add_pinyin_and_definition(word_list, zh_dict,
            include_surname_tag)
    word_list = add_parts_of_speech(word_list, add_speech_parts)
    word_list = word_list.add_freq(word_list)
    word_list = sort_by_freq(word_list, 0, freq_sort)

    return word_list
