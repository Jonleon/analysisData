import os

baseDir = os.path.abspath(os.path.dirname(__file__))
print(baseDir)

class Config(object):
    test = "test"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lajdflajdsfafsd'
    dataStore = 'C:\temp\\'

    #sql config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(baseDir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
