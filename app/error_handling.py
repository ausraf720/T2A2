
from flask import jsonify
from werkzeug.exceptions import BadRequest, Unauthorized
from marshmallow.exceptions import ValidationError

#\***************************************************************************\

#Error handling function for when inputs are missing or json is malformed
def error_handler(blueprint):
    @blueprint.errorhandler(KeyError)
    def key_error(e):
        return jsonify({'error': f'The field {e} is required'}), 400

    @blueprint.errorhandler(BadRequest)
    def default_error(e):
        return jsonify({'error': e.description}), 400

    @blueprint.errorhandler(ValidationError)
    def validation_error(e):
        return jsonify(e.messages), 400
    
    @blueprint.errorhandler(Unauthorized)
    def unauthorized_error(e):
        return jsonify({'error': e.description}), 401

#\***************************************************************************\