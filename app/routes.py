from flask import render_template, request, redirect

from app import app, logic


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", page_title='Acceuil', projects=logic.get_all_projects())


@app.route('/project')
def project():
    id = int(request.args['id'])
    project = logic.get_project(id)
    speakers = logic.get_characters(id, lang='greek')
    french_speakers = logic.get_characters(id, lang='french')
    return render_template("project.html", page_title=project.french_name, project=project,
                           greek_characters=speakers, french_characters=french_speakers)


@app.route('/deleteProject')
def delete_project():
    logic.delete_project(int(request.args['id']))
    return redirect(request.referrer)


@app.route('/addProject', methods=['POST'])
def add_project():
    logic.add_project(request.form)
    return redirect(request.referrer)


@app.route('/deleteCharacter')
def delete_character():
    logic.delete_character(request.args['id'])
    return redirect(request.referrer)


@app.route('/addCharacter', methods=['POST'])
def add_character():
    logic.add_character(request.form)
    return redirect(request.referrer)


@app.route('/addAccessory', methods=['POST'])
def add_accessory():
    logic.add_accessory(request.form)
    return redirect(request.referrer)


@app.route('/deleteAccessory')
def delete_accessory():
    logic.delete_accessory(request.args['id'])
    return redirect(request.referrer)


@app.route('/saveEncycleme', methods=['POST'])
def save_encycleme():
    logic.save_encycleme(request.form)
    return redirect(request.referrer)


@app.route('/saveMechane', methods=['POST'])
def save_mechane():
    logic.save_mechane(request.form)
    return redirect(request.referrer)


@app.route('/saveUnitModifs', methods=['POST'])
def save_unit_modifs():
    logic.save_unit_modifs(request.form)
    return redirect(request.referrer + "#" + f'unit{request.form["unit_id"]}')
