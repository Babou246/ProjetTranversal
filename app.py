import math
import random
from bson import ObjectId
from flask import Flask, jsonify, render_template, request, abort, redirect, session, url_for, flash
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
import csv
import pandas as pd
from flask_mail import Mail, Message
from flask_migrate import Migrate
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
import os
from model import *


#------------------------------------

# Configuration de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'diopabubakr79@gmail.com'
app.config['MAIL_PASSWORD'] = 'pxsr locn kckp waqx'
app.config['MAIL_DEFAULT_SENDER'] = ('PREVENTON VHE', 'diopabubakr79@gmail.com')

# Assurez-vous que le dossier de téléchargement existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
migrate = Migrate(app, db)
bcrypt = Bcrypt()
mail = Mail(app)


#------------------------------------
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Utilisateur, user_id)
    

def create_database():
    with app.app_context():
        db.create_all()
        print("Database created successfully.")
##------------------------------------------------------------------------------------------------------------------



@app.route('/changepassword', methods=['POST'])
def changepassword():
    login = request.form['login']
    old_password = request.form['ancien']
    new_password = request.form['new']
    confirm_password = request.form['conf']
    
    user = Utilisateur.query.filter_by(username=login).first()
    if user and bcrypt.check_password_hash(user.password, old_password):
        if new_password == confirm_password:
            user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            db.session.commit()
            flash('Password changed successfully')
        else:
            flash('New passwords do not match')
    else:
        flash('Old password is incorrect')
    return redirect(url_for('login'))

genere=random.randint(14326,6614262)
gname=random.randint(6,66)

@app.route('/dashboard/prevent-vhe/',methods=['GET'])
@login_required
def dashboard():
    patients = Patient.query.order_by(Patient.timestamp.desc()).all()
    return render_template('pages/dashboard.html',current_user=current_user,patients=patients)

#-------------------------------------------------------------------------------------------------------------------

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    print('------------------------------->>>>>>>>>>>',request)
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        insert_data(file_path)
        return render_template('pages/dashboard.html')

def insert_data(file_path):
    # Lire le fichier CSV avec pandas
    data = pd.read_csv(file_path)

    for _, row in data.iterrows():
        current_datetime = datetime.utcnow()
        # Insérer dans MongoDB
        mongo_db.experiment_data.insert_one({
            "temperature": row['Temperature (oC)'],
            "time_hours": row['Time (HOURS)'],
            "time_mins": row['Time (Mins)'],
            "log_reduction": row['Log Reduction'],
            "matrix": row['Matrix'],
            "other_information": row['Other information'],
            "starting_value": row['Starting value'],
            "source": row['Source'],
            "new_data": row['NewData'],
            "experiment_dataset": row['EXPERIMENT_DATASET'],
            "run_number": row['RUN_NUMBER'] if not pd.isna(row['RUN_NUMBER']) else None,
            "exclude_data": row['EXCLUDE_DATA'],
            "upload_datetime": current_datetime
        })
            # Enregistrer le fichier dans la base de données
        """  new_file = User(filename=file.filename, data=file.read())
            db.session.commit() 
            db.session.add(new_file)
            
            # Envoyer des emails aux utilisateurs concernés
            users = User.query.all() """
            #for user in users:
        print("debut des -------------------------")
        #msg = Message('INFO-SANTE', recipients=["babacardiop8@esp.sn","bannabalde@esp.sn","ndeytouboye@esp.sn","mouhamadoumbengue@esp.sn","mariemtidianidia@gmail.com"])
        msg = Message('INFO-SANTE', recipients=["babacardiop8@esp.sn"])
        msg.body = 'C\'est un TEST les enfants '
        mail.send(msg)
        print("fnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        flash('File successfully uploaded and emails sent')
    return redirect(url_for('dashboard'))

######################## AUTH #######################

@app.route('/', methods=['GET', 'POST'])
@app.route('/prevent/vhe/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        utilisateur = Utilisateur.query.filter_by(email=email).first()

        if utilisateur and utilisateur.verify_password(password):
            login_user(utilisateur)
            return redirect(url_for('dashboard'))
        else:
            flash('Identifiants incorrects. Veuillez réessayer.', 'danger')
    return render_template('compte/login.html')


@app.route('/prevent-vhe/sous/inscrire', methods=('GET', 'POST'))
def inscrire():
    regions_senegal = [
    "Dakar", "Diourbel", "Fatick", "Kaffrine", "Kaolack",
    "Kédougou", "Kolda", "Louga", "Matam", "Saint-Louis",
    "Sédhiou", "Tambacounda", "Thiès", "Ziguinchor"
    ]
    region_senegal = Region.query.all()

    # Insérez chaque région dans la table Region
    for region_name in regions_senegal:
        region = Region(nom=region_name)
        #db.session.add(region)

    # Validez les changements dans la base de données
    #db.session.commit()
    if request.method == 'POST':
        print('================================>',request.url)
        prenom = request.form.get('prenom')
        nom = request.form.get('nom')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password == '' and confirm_password == '':
            password = 'P@ssera2024'
            confirm_password='P@ssera2024'
        role_nom = request.form.get('role')
        region_id = request.form.get('region')
        #print(request.form) 

        # Vérifiez que region_id est bien renseigné
        if region_id is None:
            return "Erreur : Vous devez sélectionner une région."

        # Vérifier si l'utilisateur existe déjà par email
        utilisateur_existe = Utilisateur.query.filter_by(email=email).first()
        if utilisateur_existe:
            flash('Cet email est déjà utilisé. Veuillez choisir un autre email.', 'error')
            return redirect(url_for('inscrire'))

        # Vérifier si les mots de passe correspondent
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return redirect(url_for('inscrire'))

        # Vérifier si le rôle spécifié existe dans la base de données
        role = Role.query.filter_by(nom=role_nom).first()
        if not role:
            flash('Le rôle spécifié est invalide.', 'error')
            return redirect(url_for('inscrire'))

        # Créer un nouvel utilisateur avec le rôle correspondant
        nouvel_utilisateur = Utilisateur(
            username=email,  # Utilisation de l'email comme username pour cet exemple
            email=email,
            password=generate_password_hash(password),  # Hasher le mot de passe
            nom=nom,
            prenom=prenom,
            role_id=role.id,
            region_id=region_id
        )
        if nouvel_utilisateur :
            db.session.add(nouvel_utilisateur)
            db.session.commit()
            msg = Message('CREATION COMPTE ALERT VHE', recipients=[nouvel_utilisateur.email])
            msg.body = f"Bonjour M/Mme {nouvel_utilisateur.nom} \nVotre vient d'être crée avec succés avec comme mot de passe par défaut P@ssera2024\n\nMerci de consulter votre le compte sur le lien http://localhost:4000/prevent/vhe/login" 
            #mail.send(msg)
        flash('Inscription réussie. Vous pouvez maintenant vous connecter.', 'success')

    return render_template('compte/inscription.html',region_senegal=region_senegal)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
#####################################################


@app.route('/acceuil')
@login_required
def accueil():
    return render_template('pages/table.html')

####################################################### user

##################### modf
@app.route('/profile/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def profile_modif(id):
    user = Utilisateur.query.get_or_404(id)
    
    if request.method == 'POST':
        prenom = request.form['prenom']
        nom = request.form['nom']
        email = request.form['email']
        new_password = request.form['password']
        
        # Mettre à jour les informations de l'utilisateur
        user.prenom = prenom
        user.nom = nom
        user.email = email
        if new_password:
            user.set_password(new_password)
        
        # Enregistrer les modifications dans la base de données
        db.session.commit()
        
        # Flash message pour notifier l'utilisateur
        flash('Les modifications ont été enregistrées avec succès.', 'success')
        
        # Redirection vers la page de profil
        return redirect(url_for('profile_modif', id=id))
    
    # Si la méthode est GET, afficher simplement le formulaire de modification
    return render_template('profil/user.html', user=user)


@app.route('/user')
@login_required
def user():
    user = Utilisateur.query.get_or_404(current_user.id)
    return render_template('profil/user.html', current_user=current_user,user=user)



def send_email(nom,recipient, csv_filename):
    msg = Message('Données des symptômes du patient', recipients=[recipient])
    msg.body = f'Bonjour Docteur {nom}, veuillez trouver ci-joint les données des symptômes du patient.'
    with app.open_resource(csv_filename) as csv_file:
        msg.attach(csv_filename, 'text/csv', csv_file.read())
    mail.send(msg)

@app.route('/submit-form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        age = request.form.get('age')
        symptoms = request.form.get('symptoms')
        meat_consumption = request.form.get('meatConsumption')
        animal_type = request.form.get('animalType')
        

        # Préparer les données pour le fichier CSV
        print(request.form)  # Print all form data for debugging
        csv_data = [
                ['Nom du Patient', 'Âge', 'Symptômes', 'Consommation de Viande', 'Type d\'Animal'],
                [name, age, symptoms, meat_consumption, animal_type]
        ]


        print('########################>>>',csv_data)
        
        new_patient = Patient(
            user_id=user_id,
            name=name,
            age=age,
            symptoms=symptoms,
            meat_consumption=meat_consumption,
            animal_type=animal_type,
            timestamp=datetime.utcnow()
        )
        db.session.add(new_patient)
        # Enregistrer les données dans un fichier CSV temporaire
        csv_filename = 'symptoms_data.csv'
        with open(csv_filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(csv_data)
        
        # Récupérer tous les utilisateurs ayant le rôle de médecin
        medecins = Utilisateur.query.filter_by(role_id=2).all()
        
        # Envoyer un e-mail aux utilisateurs médecins avec le fichier CSV en pièce jointe
        for medecin in medecins:
            print('################################>>>>',medecin.email)
            #send_email(medecin.nom,medecin.email, csv_filename)
        
        # Supprimer le fichier CSV temporaire après l'envoi des e-mails
        import os
        os.remove(csv_filename)
        db.session.commit()
        flash('Félicitation !!!! Attendez la reaction des medecins')
       
    return redirect(url_for('user'))

#################################################################

from flask import jsonify
@app.route('/api/data')
@login_required
def data():
    query = Utilisateur.query

    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            Utilisateur.username.like(f'%{search}%'),
            Utilisateur.email.like(f'%{search}%')
        ))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            prenom = s[3:]
            if name and prenom not in ['username', 'email', 'nom', 'prenom']:
                name = 'username'
            col = getattr(Utilisateur, name)
            col1 = getattr(Utilisateur, prenom)
            if direction == '-':
                col = col.desc()
                col1 = col1.desc()
            order.append(col,col1)
        if order:
            query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    # execute query and convert results to JSON serializable format
    users = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'nom': user.nom,
            'prenom': user.prenom
            # Add more fields as needed
        }
        for user in query
    ]

    # response
    return jsonify({
        'data': users,
        'total': total,
    })

###################################################################################### CRUD MONGODB 
# Route pour afficher les données
@app.route('/api/vhe')
@login_required
def data_mongodb():
    query = {}

    # search filter
    search = request.args.get('search')
    if search:
        query['$or'] = [
            {'username': {'$regex': search, '$options': 'i'}},
            {'email': {'$regex': search, '$options': 'i'}}
        ]

    total = collection.count_documents(query)

    # sorting
    sort = request.args.get('sort')
    if sort:
        sort_list = []
        for s in sort.split(','):
            direction = pymongo.DESCENDING if s[0] == '-' else pymongo.ASCENDING
            field = s[1:]
            sort_list.append((field, direction))
        collection.create_index(sort_list)

    # pagination
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    cursor = collection.find(query, {'_id': False}).skip(start).limit(length)

    # execute query and convert results to JSON serializable format
    users = list(cursor)

    # response
    return jsonify({
        'vhe': users,
        'total': total,
    })

@app.route('/data-hepat/collects')
@login_required
def data_mongo_db():
    # Paramètres de pagination
    page = int(request.args.get('page', 1))
    per_page =5 # Nombre d'éléments par page

    # Calcul de l'indice de début et de fin pour la pagination
    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    # Récupération des données avec la pagination
    data = list(collection.find({}).skip(start_index).limit(per_page))

    # Compte total des documents pour la pagination
    total = collection.count_documents({})

    # Calcul du nombre total de pages nécessaires
    total_pages = math.ceil(total / per_page)

    return render_template('data/data.html', data=data, page=page, total_pages=total_pages, max=max, min=min)

@app.route('/data-hepat/medecin')
def medecin():
    user = Utilisateur.query.filter_by(role_id=2).all()
    return render_template('pages/medecin.html',user=user)


################################################################################################ FN DE CRUD

@app.route('/api/data/<int:id>', methods=['POST'])
def update(id):
    with app.app_context():
        data = request.get_json()
        if 'id' not in data:
            abort(400)
        user = Utilisateur.query.get(data[id])
        for field in ['username', 'email', 'nom','prenom']:
            if field in data:
                setattr(user, field, data[field])
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    create_database()
    app.run(port=4000, debug=True)