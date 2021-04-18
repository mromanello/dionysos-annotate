greek_names = [f"nom_perso{i}" for i in range(5)]
french_names = [f"nom_perso_fr{i}" for i in range(5)]


def get_greek_characters_names(lang):
    if lang == "french":
        return french_names
    elif lang == "greek":
        return greek_names


def delete_character(character, lang):
    if lang == 'greek':
        greek_names.remove(character)
    elif lang == 'french':
        french_names.remove(character)
    return


def add_character(character, lang):
    if lang == 'greek':
        greek_names.append(character)
    elif lang == 'french':
        french_names.append(character)
    return
