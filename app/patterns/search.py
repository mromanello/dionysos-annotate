from app.patterns import pattern

SUPPORTED_PATTERNS = [pattern.Deixis, pattern.DeixisJe, pattern.DeixisTu, pattern.Douleur, pattern.Imperatif,
                      pattern.Negation, pattern.Question]


def search_patterns(lemma: str, postag: str) -> list:
    movements = [p.name() for p in SUPPORTED_PATTERNS if p.matches(lemma, postag)]
    return movements
