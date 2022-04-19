import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Giving access to project to any OS 
# Allowing outside files/folders to be added from base directory 

class Config():
    """
    Set Config variables for the flask app. Using Environments variables 
    where available otherwise. create the config variable if not done already
    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or "No Secret Key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///" + os.path.join(basedir, 'app.db')
    SQLACHEMY_TRACK_MODIFICATIONS = False