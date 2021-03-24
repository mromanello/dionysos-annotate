from flask import render_template, jsonify, request

from app import app, db_access


@app.route('/')
@app.route('/index')
def index():
    return render_template("tmp.html", col_names=['a', 'b', 'b'])


@app.route('/deleteChar', methods=['POST'])
def delete_char():
    db_access.delete_character(request.json['character'])
    return jsonify(success=True)


@app.route('/addChar', methods=['POST'])
def add_char():
    db_access.add_character(request.json['character'])
    return jsonify(success=True)


@app.route('/getChars')
def get_chars():
    lang = request.args['language']
    characters = db_access.get_greek_characters_names(lang)
    return jsonify({'characters': characters})
