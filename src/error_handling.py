
from flask import jsonify
from werkzeug.exceptions import BadRequest, Unauthorized
from marshmallow.exceptions import ValidationError

#\***************************************************************************\

#Error handling function for when inputs are missing or json is malformed
def error_handler(blueprint):

    #When required input in json is missing
    @blueprint.errorhandler(KeyError)
    def key_error(e):
        return jsonify({'error': f'The field {e} is required'}), 400

    #When the input cannot be understood due to bad syntax
    @blueprint.errorhandler(BadRequest)
    def default_error(e):
        return jsonify({'error': e.description}), 400

    #When the input has data of wrong type
    @blueprint.errorhandler(ValidationError)
    def validation_error(e):
        return jsonify(e.messages), 400
    
    #When JWT token not provided or incorrect for a given user
    @blueprint.errorhandler(Unauthorized)
    def unauthorized_error(e):
        return jsonify({'error': e.description}), 401
    
    #Custom 404 error handler for pages that don't exist,
    # for routes using <int:id>
    @blueprint.errorhandler(404)
    def not_found_error(e):
        return jsonify({'error': e.description}), 404

#\***************************************************************************\