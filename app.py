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
    tokensFile, simbolTable, errors = JL.tokenizer(data['program'])
    return jsonify({'simbolTable': simbolTable, 'tokensFile': tokensFile, 'errors': errors})

if __name__ == '__main__':
    app.run()
