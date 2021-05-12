import abc
import re

from greek_accentuation.characters import base


class Pattern(abc.ABC, metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def name(cls) -> str:
        pass

    @classmethod
    @abc.abstractmethod
    def matches(cls, lemma: str, postag: str) -> bool:
        return False


class Deixis(Pattern):
    @classmethod
    def name(cls) -> str:
        return "Deixis"

    @classmethod
    def matches(cls, lemma: str, postag: str) -> bool:
        return bool(re.fullmatch(r'(τοδε)|(ουτος)|(εκεινος)|(οδε)', base_form(lemma)))


class DeixisJe(Pattern):
    @classmethod
    def name(cls) -> str:
        return "Deixis_Je"

    @classmethod
    def matches(cls, lemma: str, postag: str) -> bool:
        return bool(re.fullmatch(r'εγω', base_form(lemma)))


class DeixisTu(Pattern):
    @classmethod
    def name(cls) -> str:
        return "Deixis_Tu"

    @classmethod
    def matches(cls, lemma: str, postag: str) -> bool:
        return bool(re.fullmatch(r'συ', base_form(lemma))) or \
               bool(re.fullmatch(r'ὦ', lemma)) or \
               bool(re.fullmatch(r'\S{7}v\S', postag))


class Negation(Pattern):
    @classmethod
    def name(cls) -> str:
        return "Négation"

    @classmethod
    def matches(cls, lemma: str, postag: str) -> bool:
        return bool(re.fullmatch(r'(ου)|(ουδε)|(ουκετι)|(ουτε)|(μη)|(μηδε)|(μητε)|(μηκετι)', base_form(lemma))) or \
               bool(re.fullmatch(r'(οὐδείς)|(μηδείς)', lemma))


class Douleur(Pattern):
    @classmethod
    def name(cls) -> str:
        return "Douleur"

    @classmethod
    def matches(cls, lemma: str, postag: str) -> bool:
        return bool(re.fullmatch(r'i\S{8}', postag)) and \
               not bool(re.fullmatch(r'ὦ', lemma))


class Imperatif(Pattern):
    @classmethod
    def name(cls) -> str:
        return "Impératif"

    @classmethod
    def matches(cls, lemma: str, postag: str) -> bool:
        return bool(re.fullmatch(r'v2\S{2}m\S{4}', postag))


class Question(Pattern):
    @classmethod
    def name(cls) -> str:
        return "Question"

    @classmethod
    def matches(cls, lemma: str, postag: str) -> bool:
        return bool(re.fullmatch(r';', lemma))


class Punctuation(Pattern):

    @classmethod
    def name(cls) -> str:
        pass

    @classmethod
    def matches(cls, lemma: str, postag: str) -> bool:
        return bool(re.fullmatch(r'u--------', postag))


class UnitDelimiter(Pattern):

    @classmethod
    def name(cls) -> str:
        pass

    @classmethod
    def matches(cls, lemma: str, postag: str) -> bool:
        return bool(re.fullmatch(r",|\.|;|·", lemma))


def base_form(word: str) -> str:
    return ''.join([base(c) for c in word])
