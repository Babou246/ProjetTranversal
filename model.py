import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from itsdangerous import Serializer
from werkzeug.security import generate_password_hash, check_password_hash
import pandas
from pymongo import MongoClient
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:passer@localhost/projetransversal'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

mongo_uri = "mongodb://localhost:27017"
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client['projetransversal']
collection = mongo_db['experiment_data']

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f'<Role {self.nom}>'
class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100),nullable=False)

# Modèle Utilisateur avec référence à Role
class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False) 
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('utilisateurs', lazy=True))
    active = db.Column(db.Boolean, default=True)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    region = db.relationship('Region', backref=db.backref('utilisateurs', lazy=True))
    session_token = db.Column(db.String(36), unique=True, nullable=True) 
    suivi_par = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=True)
    check = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return f'<Utilisateur {self.username}>'
    def verify_password(self, password):
        return check_password_hash(self.password, password)
    def is_active(self):
        return self.active
    def get_id(self):
        return str(self.id)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_session_token(self):
        return str(uuid.uuid4())
    
    @property
    def can_follow_doctor(self):
        return self.role_id == 1 
    
    @property
    def is_authenticated(self):
        # Utilisateur toujours authentifié si l'objet existe
        return True

    @property
    def is_anonymous(self):
        return False
    

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    fever = db.Column(db.String(3), nullable=False)
    fatigue = db.Column(db.String(3), nullable=False)
    muscle_aches = db.Column(db.String(3), nullable=False)
    headache = db.Column(db.String(3), nullable=False)
    vomiting = db.Column(db.String(3), nullable=False)
    diarrhea = db.Column(db.String(3), nullable=False)
    meat_consumption = db.Column(db.String(3), nullable=False)
    animal_type = db.Column(db.String(100), nullable=True)
    additional_info = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)  # Assuming dataset is binary data
    uploaded_by = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    read = db.Column(db.Boolean, default=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    utilisateur = db.relationship('Utilisateur', backref=db.backref('notifications', lazy=True))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
