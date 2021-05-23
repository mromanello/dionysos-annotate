from app import db

"""
This module contains Database Table definitions, following SQLALCHEMY Syntax.
"""


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.Text, unique=True)
    greek_name = db.Column(db.Text, default='')
    french_name = db.Column(db.Text)
    encycleme = db.Column(db.Boolean, default=False)
    mechane = db.Column(db.Boolean, default=False)
    characters = db.relationship('Character', backref='project')
    accessories = db.relationship('Accessory', backref='project')
    units = db.relationship('Unit', backref='project')


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    name = db.Column(db.Text)
    lang = db.Column(db.Enum('greek', 'french'))


class Accessory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    name = db.Column(db.Text)


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    text = db.Column(db.Text)
    french_text = db.Column(db.Text, default='')
    speaker = db.Column(db.Text)
    mouvements = db.Column(db.Text)
    cite = db.Column(db.Text)
    sentence_num = db.Column(db.Integer)
    unit_num = db.Column(db.Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
