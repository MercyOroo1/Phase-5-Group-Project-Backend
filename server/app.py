from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db
from routes.auth import auth_bp,bcrypt, jwt



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///property.db'

app.config['SECRET_KEY']= "We are winners"

app.register_blueprint(auth_bp)
bcrypt.init_app(app)
jwt.init_app(app)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



migrate = Migrate(app = app, db= db)
db.init_app(app)
@app.route('/')
def home():
    return "Welcome to the Home Page!"





if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050,debug=True)
