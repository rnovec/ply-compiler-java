from flask import Flask, jsonify, json, request
from flask_cors import CORS
from lexer import JavaLexer
from parse import JavaParser
import re

app = Flask(__name__)
CORS(app)


@app.route('/compile', methods=['POST'])
def compile():
    # data = request.form['program'] # for 'multipart/form-data'
    data = request.get_json(force=False, silent=False, cache=True)
    program = data['program']
    JL = JavaLexer()
    JP = JavaParser()
    tokensFile, simbolTable = JL.tokenizer(program)
    errors, names = JP.compile(program)
    for t in simbolTable:
        if re.match(r'ID', t['type']):
            try:
                t['vartype'] = names[t['value']]['vartype']
            except Exception as err:
                print(err)
            
    return jsonify({'simbolTable': simbolTable, 'tokensFile': tokensFile, 'errors': errors})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
