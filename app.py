from flask import Flask, jsonify, json, request
from flask_cors import CORS
from lexer import tokenizer
from lexer import tokens
import re

app = Flask(__name__)
CORS(app)


@app.route('/tokenize', methods=['POST'])
def tokenize():
    # data = request.form['program'] # for 'multipart/form-data'
    data = request.get_json(force=False, silent=False, cache=True)
    L = tokenizer(data['program'])
    seen = set()
    new_l = []
    counters = {}
    for t in tokens:
        counters[t] = 0
    for d in L:
        if d['value'] not in seen or re.match(r'LXERR', d['type']):
            seen.add(d['value'])
            new_l.append(d)
    
    for token in new_l:
        if not re.match(r'LXERR', token['type']):
            counters[token['type']] += 1
            token['type'] = token['type'] + str(counters[token['type']])
    return jsonify({'tokens': new_l})


if __name__ == '__main__':
    app.run()
