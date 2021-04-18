from app.models import *


def add_project(project_attributes):
    full_project_attributes = dict(project_attributes)
    if full_project_attributes['greek_name'] == '':
        full_project_attributes['greek_name'] = None
    full_project_attributes['encycleme'] = False
    full_project_attributes['mechane'] = False
    project = Project(**full_project_attributes)
    db.session.add(project)
    db.session.commit()
    return


def get_all_projects():
    return Project.query.all()


def delete_project(id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()
    return
