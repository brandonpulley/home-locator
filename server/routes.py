from flask import request, jsonify
from server import app


@app.route('/query', methods=['POST'])
def pquery():

    payload = {'hey': 'ho'}

    return jsonify(payload)

