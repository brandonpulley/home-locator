from flask import request, jsonify
from server import app


from tools.home_finder import get_home_location

@app.route('/query', methods=['POST'])
def pquery():

    visits = request.json.get('visits')

    return jsonify(get_home_location(visits))
