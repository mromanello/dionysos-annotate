import urllib.request

from app import perseids_search
from app.models import *


class Logic:
    """
    This class contains methods to communicate with the database.
    Mainly adding and deleting entities defined in app.models
    Most of the methods here are straightforward. Comments added where things may be unclear.
    """

    @classmethod
    def add_project(cls, project_attributes):
        project = Project(**project_attributes)
        db.session.add(project)
        db.session.commit()  # Project needs to be in database to create dependent tables (character)

        try:
            # Here the filename can be a URL or an absolute path to a file.
            local_filename, headers = urllib.request.urlretrieve(project.file_path)
            units, speakers = perseids_search.parse_xml_into_units(local_filename)
        except Exception as e:
            # In case There was an error with parsing the file, we have to delete the project before raising the error.
            db.session.delete(project)
            db.session.commit()
            raise e

        for speaker_name in speakers:
            character = Character(name=speaker_name, project_id=project.id, lang='greek')
            db.session.add(character)

        for index, unit_dict in enumerate(units):
            unit = Unit(**unit_dict, unit_num=index + 1, project_id=project.id)
            db.session.add(unit)

        db.session.commit()
        return

    @classmethod
    def get_all_projects(cls):
        """
        Returns all Projects in the database
        :return: List(models.Project)
        """
        return Project.query.all()

    @classmethod
    def delete_project(cls, id):
        """
        deletes projects with given id.
        Implements CASCADING delete
        :param id: int, id of project in database
        :return: None
        """
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
        """
        get Project with given id in the database
        :param project_id: int
        :return: models.Project instance
        """
        project = Project.query.get(project_id)
        return project

    @classmethod
    def get_characters(cls, project_id, lang):
        """
        Get character names in the database for the given project_id and language('greek'/'french')
        :param project_id: int
        :param lang: 'greek' or 'french'
        :return: List(models.Character)
        """
        characters = Character.query.filter_by(project_id=project_id, lang=lang).with_entities(Character.id,
                                                                                               Character.name).all()
        return characters

    @classmethod
    def delete_character(cls, character_id):
        """
        Delete Character with given id in database
        :param character_id: int
        :return: None
        """
        character = Character.query.get(character_id)
        db.session.delete(character)
        db.session.commit()
        return

    @classmethod
    def add_character(cls, form):
        """
        Add new Character from database
        :param form: Dict giving the attributes of character.
        :return: None
        """
        character = Character(**form)
        db.session.add(character)
        db.session.commit()
        return

    @classmethod
    def get_accessories(cls, project_id):
        """
        Get all accessory names for the given project
        :param project_id:  int
        :return: List(models.Accessory)
        """
        accessories = Accessory.query.filter_by(project_id=project_id).with_entities(Accessory.id,
                                                                                     Accessory.name).all()
        return accessories

    @classmethod
    def delete_accessory(cls, accessory_id):
        """
        Delete an accessory given by its id in the database
        :param accessory_id: int
        :return: None
        """
        accessory = Accessory.query.get(accessory_id)
        db.session.delete(accessory)
        db.session.commit()
        return

    @classmethod
    def add_accessory(cls, form):
        """
        Add an accessory to project. project_id should be in form
        :param form: Dict representing the accessory attributes
        :return: None
        """
        accessory = Accessory(**form)
        db.session.add(accessory)
        db.session.commit()
        return

    @classmethod
    def save_encycleme(cls, form):
        """
        Save changes to 'encycleme' field of project.
        :param form: dict sent by request.
        :return:
        """
        project = Project.query.get(form['project_id'])
        # This is bad, form logic should be seperate from DB logic.
        project.encycleme = (form['radioEncycleme'] == 'yes')
        db.session.commit()
        return

    @classmethod
    def save_mechane(cls, form):
        """
        Save changes to 'mechane' field of project.
        :param form: dict sent by request.
        :return:
        """
        project = Project.query.get(form['project_id'])
        project.mechane = (form['radioMechane'] == 'yes')
        db.session.commit()
        return

    @classmethod
    def save_unit_modifs(cls, form):
        """
        Save unit french_text translation to Database
        :param form: Dict containing the unit_id as well as the french_text to save.
        :return:
        """
        unit = Unit.query.get(form['unit_id'])
        unit.french_text = form['french_text']
        db.session.commit()
        return

    @classmethod
    def get_project_json(cls, project_id):
        """
        Generates JSON to be downloaded by app.
        format is :
            {'metadata': {'greek_characters': list(str),
                     'french_characters': list(str),
                      'accessories': list(str),
                      'encycleme': Boolean,
                      'mechane': Boolean},
            'ContenuSource': [{'unit_id':int , 'sentence_id':int ,
                                'cite': str, 'speaker': str,
                                'text': str, 'french_text': str,
                                'mouvements': list(str)}]
            }
        :param project_id: int
        :return: Dict
        """
        project = Project.query.get(project_id)
        greek_characters = cls.get_characters(project_id, lang='greek')
        french_characters = cls.get_characters(project_id, lang='french')
        project_json = {'metadata': {'greek_characters': [gc[1] for gc in greek_characters],
                                     'french_characters': [fc[1] for fc in french_characters],
                                     'accessories': [acc.name for acc in project.accessories],
                                     'encycleme': project.encycleme,
                                     'mechane': project.mechane},
                        'ContenuSource': [{'unit_id': unit.unit_num, 'sentence_id': unit.sentence_num,
                                           'cite': unit.cite, 'speaker': unit.speaker,
                                           'text': unit.text, 'french_text': unit.french_text,
                                           'mouvements': unit.mouvements.split('-')} for unit in project.units]}
        return project_json
