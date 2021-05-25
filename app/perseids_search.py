import xml.etree.ElementTree as ET

import pandas as pd

from app.patterns import search,pattern


def read_perseids_xml_into_df(filename):
    xml = ET.parse(filename)
    root = xml.getroot()
    dicts = []
    for sentence in root.iter('sentence'):
        sentence_num = sentence.attrib['id']
        speaker = sentence.attrib['speaker']
        for word in sentence.iter('word'):
            if 'insertion_id' not in word.attrib:
                word.attrib['speaker'] = speaker
                word.attrib['sentence_id'] = int(sentence_num)
                dicts.append(word.attrib)
    return pd.DataFrame(dicts)


def get_characters(words):
    return list(words.speaker.unique())


def shift_series(series, start):
    new_series = pd.Series(start, index=series.index)
    new_series[1:] = series.iloc[:-1]
    return new_series


def get_new_units(words):
    unit_delimiter = words.apply(lambda r: pattern.UnitDelimiter.matches(r['lemma'], r['postag']), axis=1) |\
                     words.apply(lambda r: pattern.Punctuation.matches(r['lemma'], r['postag']), axis=1)
    return shift_series(unit_delimiter, start=True)


def get_unit_id(words):
    unit_delimiter = get_new_units(words)
    unit_ids = range(1, unit_delimiter.sum() + 1)
    starts = unit_delimiter[unit_delimiter].index
    ends = list(starts[1:] - 1) + [unit_delimiter.index[-1]]
    starts = list(starts)
    res = pd.Series(0, index=unit_delimiter.index)
    for index, (start, end) in enumerate(zip(starts, ends)):
        res.loc[start:end] = unit_ids[index]
    return res


def get_words_with_punc_after(words):
    punctuation = words.apply(lambda r: pattern.Punctuation.matches(r['lemma'], r['postag']), axis=1)
    punc_after = pd.Series(False, index=punctuation.index)
    punc_after[:-1] = punctuation[1:]  # shift left
    return punc_after


def group_words_into_units(words):
    def apply_group_by_unit(df):
        mouvements_in_unit = []

        # unique in unit
        cite = df.iloc[0]['cite']
        sentence_id = int(df.iloc[0]['sentence_id'])
        speaker = df.iloc[0]['speaker']

        current_line = cite
        text = ''
        mouvements = []

        for _, row in df.iterrows():
            if current_line != row['cite']:
                text += '\n'
                current_line = row['cite']

            text += row['form']
            if not row['punc_after']:
                text += ' '

            mouvements += row['mouvements']

        if not mouvements:
            mouvements += ['Affirmation']
        res = {
            'cite': cite,
            'sentence_num': sentence_id,
            'speaker': speaker,
            'mouvements': '-'.join(list(set(mouvements))),
            'text': text
        }
        return res

    return words.groupby('unit_id').apply(apply_group_by_unit)


def parse_xml_into_units(filename):
    words = read_perseids_xml_into_df(filename)

    words['mouvements'] = words.apply(lambda x: search.search_patterns(x['lemma'], x['postag']), axis=1)

    words['unit_id'] = get_unit_id(words)

    words['punc_after'] = get_words_with_punc_after(words)

    return group_words_into_units(words), get_characters(words)
