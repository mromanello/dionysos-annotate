greek_names = [f"nom_perso{i}" for i in range(10)]
french_names = [f"nom_perso_fr{i}" for i in range(10)]


def get_greek_characters_names(lang):
    if lang == "french":
        return french_names
    elif lang == "greek":
        return greek_names


def delete_character(character):
    greek_names.remove(character)
    return


def add_character(character):
    greek_names.append(character)
    return
