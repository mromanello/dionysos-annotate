from flask import render_template, request, redirect, jsonify

import json
from app import app
from app.logic import Logic


@app.route('/')
@app.route('/index')
def index():
    """
       Render the Home page, containing all projects
    """
    return render_template("index.html", page_title='', projects=Logic.get_all_projects())


@app.route('/project')
def project():
    """
        Render a specific project page.
        Handles GET request in the form /project?id=#id, where #id is the project id
        in the Database
    """
    project_id = int(request.args['id'])
    project = Logic.get_project(project_id)
    speakers = Logic.get_characters(project_id, lang='greek')
    french_speakers = Logic.get_characters(project_id, lang='french')
    return render_template("project.html", page_title=project.french_name, project=project,
                           greek_characters=speakers, french_characters=french_speakers)


@app.route('/deleteProject')
def delete_project():
    """
        Delete a specific project.
        Handles GET request in the form /deleteProject?id=#id, where #id is the project id
        in the Database.
    """
    Logic.delete_project(int(request.args['id']))
    return redirect(request.referrer)


@app.route('/addProject', methods=['POST'])
def add_project():
    """
        Creates a new project in the database.
        Handles POST requests where the fields of the form are like the following:

    """
    Logic.add_project(request.form)
    return redirect(request.referrer)


@app.route('/addLocalProject', methods=['POST'])
def add_local_project():
    """
        Creates a new project in the database.
        Handles POST requests where the fields of the form are like the following:

    """
    if request.files:
        uploaded_json_file = request.files['json_file_upload']
        json_data = json.loads(uploaded_json_file.read())
        project_metadata = json_data['metadata']
        text_units = json_data['ContenuSource']
        grk_characters = project_metadata['greek_characters']
        fr_characters = project_metadata['french_characters']
        project_attributes = {
            "greek_name": project_metadata['greek_name'],
            "french_name": project_metadata['french_name'],
            "file_path": project_metadata['file_path'],
            "encycleme": project_metadata['encycleme'],
            "mechane": project_metadata['mechane']
        }
        Logic.add_project_from_json(project_attributes, grk_characters, fr_characters, text_units)
    return redirect(request.referrer)


@app.route('/deleteCharacter')
def delete_character():
    Logic.delete_character(request.args['id'])
    return redirect(request.referrer)


@app.route('/addCharacter', methods=['POST'])
def add_character():
    Logic.add_character(request.form)
    return redirect(request.referrer)


@app.route('/addAccessory', methods=['POST'])
def add_accessory():
    Logic.add_accessory(request.form)
    return redirect(request.referrer)


@app.route('/deleteAccessory')
def delete_accessory():
    Logic.delete_accessory(request.args['id'])
    return redirect(request.referrer)


@app.route('/saveEncycleme', methods=['POST'])
def save_encycleme():
    Logic.save_encycleme(request.form)
    return redirect(request.referrer)


@app.route('/saveMechane', methods=['POST'])
def save_mechane():
    Logic.save_mechane(request.form)
    return redirect(request.referrer)


@app.route('/saveUnitModifs', methods=['POST'])
def save_unit_modifs():
    request_dict = dict([(u['name'], u['value']) for u in request.json])
    Logic.save_unit_modifs(request_dict)
    # method doesn't redirect page, Javascript will update the corresponding unit
    return request_dict


@app.route('/projectJson')
def get_project_json():
    json_dict = Logic.get_project_json(request.args['id'])
    return jsonify(json_dict)


@app.route('/unitsJson')
def get_units_as_json():
    project_id = int(request.args['id'])
    project = Logic.get_project(project_id)
    # This format is required for the DataTable library Ajax fetching
    return jsonify({'data': [unit.as_dict() for unit in project.units]})
