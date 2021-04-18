from flask import render_template, jsonify, request

from app import app, db_access, logic


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", page_title='Acceuil', projects=logic.get_all_projects())


@app.route('/deleteChar', methods=['POST'])
def delete_char():
    db_access.delete_character(request.json['character'], request.json['language'])
    return jsonify(success=True)


@app.route('/addChar', methods=['POST'])
def add_char():
    db_access.add_character(request.json['character'], request.json['language'])
    return jsonify(success=True)


@app.route('/getChars')
def get_chars():
    lang = request.args['language']
    characters = db_access.get_greek_characters_names(lang)
    return jsonify({'characters': characters})


@app.route('/deleteProject')
def delete_project():
    logic.delete_project(int(request.args['id']))
    return index()


@app.route('/addProject', methods=['POST'])
def add_project():
    logic.add_project(request.form)
    return index()
    