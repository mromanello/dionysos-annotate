from app import perseids_search
from app.models import *


class Logic:
    """
    This class contains methods to communicate with the database.
    Mainly adding and deleting entities defined in app.models
    """

    @classmethod
    def add_project(cls, project_attributes):
        project = Project(**project_attributes)
        db.session.add(project)
        # Project needs to be in database to create dependent tables (character)
        db.session.commit()
        try:
            units, speakers = perseids_search.parse_xml_into_units('/home/ahmedj/xml/' + project.file_path)
        except Exception as e:
            # In case There was an error with parsing the file, we have to delete the project before raising the error.
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

    @classmethod
    def get_all_projects(cls):
        return Project.query.all()

    @classmethod
    def delete_project(cls, id):
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

    @classmethod
    def get_project(cls, project_id):
        project = Project.query.get(project_id)
        return project

    @classmethod
    def get_characters(cls, project_id, lang):
        characters = Character.query.filter_by(project_id=project_id, lang=lang).with_entities(Character.id,
                                                                                               Character.name).all()
        return characters

    @classmethod
    def delete_character(cls, character_id):
        character = Character.query.get(character_id)
        db.session.delete(character)
        db.session.commit()
        return

    @classmethod
    def add_character(cls, form):
        character = Character(**form)
        db.session.add(character)
        db.session.commit()
        return

    @classmethod
    def get_accessories(cls, project_id):
        accessories = Accessory.query.filter_by(project_id=project_id).with_entities(Accessory.id,
                                                                                     Accessory.name).all()
        return accessories

    @classmethod
    def delete_accessory(cls, accessory_id):
        accessory = Accessory.query.get(accessory_id)
        db.session.delete(accessory)
        db.session.commit()
        return

    @classmethod
    def add_accessory(cls, form):
        accessory = Accessory(**form)
        db.session.add(accessory)
        db.session.commit()
        return

    @classmethod
    def save_encycleme(cls, form):
        project = Project.query.get(form['project_id'])
        project.encycleme = (form['radioEncycleme'] == 'yes')
        db.session.commit()
        return

    @classmethod
    def save_mechane(cls, form):
        project = Project.query.get(form['project_id'])
        project.mechane = (form['radioMechane'] == 'yes')
        db.session.commit()
        return

    @classmethod
    def save_unit_modifs(cls, form):
        unit = Unit.query.get(form['unit_id'])
        unit.french_text = form['french_text']
        db.session.commit()
        return
