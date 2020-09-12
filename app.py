from flask import Flask, jsonify, json, request
from flask_cors import CORS
from lexer import JavaLexer

app = Flask(__name__)
CORS(app)


@app.route('/tokenize', methods=['POST'])
def tokenize():
    # data = request.form['program'] # for 'multipart/form-data'
    data = request.get_json(force=False, silent=False, cache=True)
    JL = JavaLexer()
    JL.build()
    tokens = JL.tokenizer(data['program'])
    tokens = JL.create_set(tokens)
    return jsonify({'tokens': tokens})


if __name__ == '__main__':
    app.run()
