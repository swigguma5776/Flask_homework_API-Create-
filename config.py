import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

# Giving access to project to any OS 
# Allowing outside files/folders to be added from base directory 

class Config():
    """
    Set Config variables for the flask app. Using Environments variables 
    where available otherwise. create the config variable if not done already
    """

    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY') or "No Secret Key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or "sqlite:///" + os.path.join(basedir, 'app.db')
    SQLACHEMY_TRACK_MODIFICATIONS = False