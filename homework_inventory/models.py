from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime 

# Adding Flask Security Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Importing Secrets Module 
import secrets 

# Import for Login Manager
from flask_login import UserMixin

# Import for Flask Login
from flask_login import LoginManager

# Import for Flask Marshmallow
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Make sure to add in UserMixin to User Class
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = False,)
    last_name = db.Column(db.String(150), nullable = False,)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    turbine = db.relationship('Turbine', backref = 'owner', lazy = True)

    def __init__(self, first_name, last_name, email, id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash 

    def __repr__(self):
        return f"User {self.email} has been added to the database."

class Turbine(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision = 10, scale = 2))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    number_of_blades = db.Column(db.String(20))
    rotor_position = db.Column(db.String(100))
    wind_direction = db.Column(db.String(100))
    generator = db.Column(db.String(100))
    blade_material = db.Column(db.String(100), nullable = True)
    wind_energy_converted = db.Column(db.String(100))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)


    def __init__(self, name, description, price, dimensions, weight, number_of_blades,
    rotor_position, wind_direction, generator, blade_material, wind_energy_converted, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.dimensions = dimensions
        self.weight = weight
        self.number_of_blades = number_of_blades
        self.rotor_position = rotor_position
        self.wind_direction = wind_direction
        self.generator = generator
        self.blade_material = blade_material
        self.wind_energy_converted = wind_energy_converted
        self.user_token = user_token

    def __repr__(self):
        return f"The following Turbine has been added: {self.name}"

    def set_id(self):
        return (secrets.token_urlsafe())


# Creating API Schema via Marshmallow Object

class TurbineSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'price', 'dimensions', 'weight', 'number_of_blades',
        'rotor_position', 'wind_direction', 'generator', 'blade_material', 'wind_energy_converted']

turbine_schema = TurbineSchema()
turbines_schema = TurbineSchema(many = True)
