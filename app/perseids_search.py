import xml.etree.ElementTree as ET

import pandas as pd

from app.patterns import search,pattern


def read_perseids_xml_into_df(filename):
    """
        Parses an XML file in Perseids format to a pandas Dataframe
    :param filename: location of file
    :return:
    """
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
    """
    :param words: pandas Dataframe which should contain the column 'speaker'
    :return: list(str)
    """
    return list(words.speaker.unique())


def shift_series(series, start):
    """
        Helper function, shifts a Pandas series By 1 position to the left,
        with the last element taking the value start
    :param series:  Pd.Series to shift
    :param start: default element to give to the last element
    :return: Pd.Series
    """
    new_series = pd.Series(start, index=series.index)
    new_series[1:] = series.iloc[:-1]
    return new_series


def get_new_units(words):
    """
    Finds positions where a new unit starts.
    This is defined as words coming after a word satisfying the UnitDelimiter Pattern or a Punctuation pattern.
    :param words: Pd.DataFrame, should contain columns 'lemma' and 'postag'
    :return: Pd.Series with True in positions where a new unit starts
    """
    unit_delimiter = words.apply(lambda r: pattern.UnitDelimiter.matches(r['lemma'], r['postag']), axis=1) |\
                     words.apply(lambda r: pattern.Punctuation.matches(r['lemma'], r['postag']), axis=1)
    return shift_series(unit_delimiter, start=True)


def get_unit_id(words):
    """
    Gives to each word in the DataFrame the unit number it belongs to.
    :param words: Pd.DataFrame, should contain columns 'lemma' and 'postag'
    :return: Pd.Series
    """
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
    """
    Find words with punctuation after them.
    :param words: Pd.DataFrame, should contain columns 'lemma' and 'postag'
    :return: Pd.Series
    """
    punctuation = words.apply(lambda r: pattern.Punctuation.matches(r['lemma'], r['postag']), axis=1)
    punc_after = pd.Series(False, index=punctuation.index)
    punc_after[:-1] = punctuation[1:]  # shift left
    return punc_after


def group_words_into_units(words):
    """
    This function groups the words DataFrame into a Dataframe with Units.
    :param words: Pd.DataFrame
    :return: Pd.DataFrame
    """
    def apply_group_by_unit(df):
        """
        Apply used in GroupBy of the words DataFrame
        :param df: Pd.DataFrame
        :return: Pd.DataFrame
        """

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
    """
    This function does all the required steps in order to Parse an XML file into dataframes that will
    be stored in the Database
    :param filename: Path to the XML file
    :return: Pd.DataFrame (unit DataFrame), list(str): list of characters in play
    """
    # Parse XML
    words = read_perseids_xml_into_df(filename)
    # Detect Mouvements
    words['mouvements'] = words.apply(lambda x: search.search_patterns(x['lemma'], x['postag']), axis=1)
    # Add Unit ids
    words['unit_id'] = get_unit_id(words)
    # Detectes words with punctuation after them, useful for rendering unit text
    words['punc_after'] = get_words_with_punc_after(words)

    return group_words_into_units(words), get_characters(words)
