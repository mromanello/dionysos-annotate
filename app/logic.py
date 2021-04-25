from app import perseids_search
from app.models import *


def add_project(project_attributes):
    project = Project(**project_attributes)
    db.session.add(project)
    db.session.commit()

    try:
        units, speakers = perseids_search.parse_xml_into_units('/home/ahmedj/xml/' + project.file_path)
    except Exception as e:
        db.session.delete(project)
        db.session.commit()
        raise e

    for speaker_name in speakers:
        character = Character(name=speaker_name, project_id=project.id, lang='greek')
        db.session.add(character)

    for unit_dict in units:
        unit = Unit(**unit_dict, project_id=project.id)
        db.session.add(unit)

    db.session.commit()
    return


def get_all_projects():
    return Project.query.all()


def delete_project(id):
    project = Project.query.get(id)
    # delete children
    children = project.characters + project.accessories + project.units
    for child in children:
        child.query.delete()
    # delete project
    db.session.delete(project)
    # commit
    db.session.commit()
    return


def get_project(project_id):
    project = Project.query.get(project_id)
    return project


def get_characters(project_id, lang):
    characters = Character.query.filter_by(project_id=project_id, lang=lang).with_entities(Character.id,
                                                                                           Character.name).all()
    return characters


def delete_character(id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    return


def add_character(form):
    character = Character(**form)
    db.session.add(character)
    db.session.commit()
    return


def get_accessories(project_id):
    accessories = Accessory.query.filter_by(project_id=project_id).with_entities(Accessory.id,
                                                                                 Accessory.name).all()
    return accessories


def delete_accessory(id):
    accessory = Accessory.query.get(id)
    db.session.delete(accessory)
    db.session.commit()
    return


def add_accessory(form):
    accessory = Accessory(**form)
    db.session.add(accessory)
    db.session.commit()
    return


def save_encycleme(form):
    project = Project.query.get(form['project_id'])
    project.encycleme = (form['radioEncycleme'] == 'yes')
    db.session.commit()
    return


def save_mechane(form):
    project = Project.query.get(form['project_id'])
    project.mechane = (form['radioMechane'] == 'yes')
    db.session.commit()
    return


def save_unit_modifs(form):
    unit = Unit.query.get(form['unit_id'])
    print(form['french_text'])
    unit.french_text = form['french_text']
    db.session.commit()
    return
