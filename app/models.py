from app import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(1000), unique=True)
    greek_name = db.Column(db.String(120), index=True, unique=True)
    french_name = db.Column(db.String(120), index=True, unique=True)
    encycleme = db.Column(db.Boolean)
    mechane = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Project {self.french_name}>'



