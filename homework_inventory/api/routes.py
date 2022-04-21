from flask import Blueprint, request, jsonify
from flask_login import current_user
from homework_inventory.helpers import token_required
from homework_inventory.models import db, User, Turbine, turbine_schema, turbines_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some': 'value'}

# Create Turbine Endpoint
@api.route('/turbines', methods = ['POST'])
@token_required
def create_turbine(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    number_of_blades = request.json['number_of_blades']
    rotor_position = request.json['rotor_position']
    wind_direction = request.json['wind_direction']
    generator = request.json['generator']
    blade_material = request.json['blade_material']
    wind_energy_converted = request.json['wind_energy_converted']
    user_token = current_user_token.token 

    print(f"BIG TESTER: {current_user_token.token}")
 
    turbine = Turbine(name, description, price, dimensions, weight, number_of_blades, rotor_position,
    wind_direction, generator, blade_material, wind_energy_converted, user_token=user_token)

    db.session.add(turbine)
    db.session.commit()

    response = turbine_schema.dump(turbine)
    return jsonify(response)

# Retrieve Turbine Endpoints
@api.route('/turbines', methods = ['GET'])
@token_required
def get_turbines(current_user_token):
    owner = current_user_token.token
    turbines = Turbine.query.filter_by(user_token = owner).all()
    response = turbines_schema.dump(turbines)
    return jsonify(response)

# Retrieve One Turbine Endpoint
@api.route('/turbines/<id>', methods = ['GET'])
@token_required
def get_turbine(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        turbine = Turbine.query.get(id)
        response = turbine_schema.dump(turbine)
        return jsonify(response)
    else: 
        return jsonify({'message': 'Valid Token Rquired'}), 401 

# Update Turbine Endpoint
@api.route('/turbines/<id>', methods = ['POST', 'PUT'])
@token_required
def update_turbine(current_user_token, id):
    turbine = Turbine.query.get(id)

    turbine.name = request.json['name']
    turbine.description = request.json['description']
    turbine.price = request.json['price']
    turbine.dimensions = request.json['dimensions']
    turbine.weight = request.json['weight']
    turbine.number_of_blades = request.json['number_of_blades']
    turbine.rotor_position = request.json['rotor_position']
    turbine.wind_direction = request.json['wind_direction']
    turbine.generator = request.json['generator']
    turbine.blade_material = request.json['blade_material']
    turbine.wind_energy_converted = request.json['wind_energy_converted']
    turbine.user_token = current_user_token.token 

    db.session.commit()
    response = turbine_schema.dump(turbine)
    return jsonify(response)

# Delete Turbine Endpone
@api.route('/turbines/<id>', methods = ['DELETE'])
@token_required
def delete_turbine(current_user_token, id):
    turbine = Turbine.query.get(id)
    db.session.delete(turbine)
    db.session.commit()
    response = turbine_schema.dump(turbine)
    return jsonify(response)