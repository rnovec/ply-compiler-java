from flask import Flask, jsonify, json, request
from flask_cors import CORS
from lexer import tokenizer, create_set

app = Flask(__name__)
CORS(app)


@app.route('/tokenize', methods=['POST'])
def tokenize():
    # data = request.form['program'] # for 'multipart/form-data'
    data = request.get_json(force=False, silent=False, cache=True)
    tokens = tokenizer(data['program'])
    tokens = create_set(tokens)
    return jsonify({'tokens': tokens})


if __name__ == '__main__':
    app.run()
