from app.patterns import pattern

SUPPORTED_PATTERNS = [pattern.Deixis, pattern.DeixisJe, pattern.DeixisTu, pattern.Douleur, pattern.Imperatif,
                      pattern.Negation, pattern.Question]


def search_patterns(lemma: str, postag: str) -> list:
    """
    Main entrypoint to the patterns module. Returns a list of all patterns that match a given word
    :param lemma: word in its lemmatized form, with accents
    :param postag: part-of-speech tag of the word, following Perseids format (8 characters)
    :return: List of all patterns that match the word
    """
    movements = [p.name() for p in SUPPORTED_PATTERNS if p.matches(lemma, postag)]
    return movements
