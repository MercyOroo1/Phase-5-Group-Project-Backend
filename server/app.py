from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db






app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///property.db'

migrate = Migrate(app = app, db= db)
db.init_app(app)
@app.route('/')
def home():
    return "Welcome to the Home Page!"




app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Galaxy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050,debug=True)