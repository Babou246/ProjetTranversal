from flask import Flask, render_template, request, abort, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import csv
from flask_mail import Mail, Message
import os


#------------------------------------

app = Flask(__name__)
app.secret_key = 'codesecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dt.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configuration de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'diopabubakr79@gmail.com'
app.config['MAIL_PASSWORD'] = 'pxsr locn kckp waqx'
app.config['MAIL_DEFAULT_SENDER'] = ('PREVENTON VHE', 'diopabubakr79@gmail.com')

db = SQLAlchemy(app)
mail = Mail(app)


#------------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.Integer, index=True)
    address = db.Column(db.String(256))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))

class Medecin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
   


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'address': self.address,
            'phone': self.phone,
            'email': self.email
        }
    

def create_database():
    with app.app_context():
        db.create_all()
        print("Database created successfully.")
        

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            # Enregistrer le fichier dans la base de données
           """  new_file = User(filename=file.filename, data=file.read())
            db.session.commit() 
            db.session.add(new_file)
            
            # Envoyer des emails aux utilisateurs concernés
            users = User.query.all() """
            #for user in users:
        print("debut des -------------------------")
        msg = Message('INFO-XIBAR', recipients=["babacardiop8@esp.sn"])
        msg.body = 'Bonjour M DIOP les fichiers sont disponibles: {}'.format(file.filename)
        mail.send(msg)
        print("fnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        flash('File successfully uploaded and emails sent')
    return redirect(url_for('index'))



@app.route('/')
def index():
    return render_template('pages/dashboard.html')

@app.route('/cal')
def cal():
    return render_template('pages/cal.html')


@app.route('/index')
def accueil():
    return render_template('pages/table.html')




@app.route('/user')
def user():
    return render_template('pages/users.html')

@app.route('/home')
def home():
    with app.app_context():
        with open('MOCK_DATA.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User(name=row['name'],
                            age=int(row['age']),
                            address=row['address'],
                            phone=row['phone'],
                            email=row['email'])
                db.session.add(user)
            db.session.commit()

        print(f'Added fake  to the database.')
    return redirect(url_for('index'))


@app.route('/api/data')
def data():
    with app.app_context():
        query = User.query

        # search filter
        search = request.args.get('search')

        print('====>', request.args)
        if search:
            query = query.filter(db.or_(
                User.name.like(f'%{search}%'),
                User.email.like(f'%{search}%')
            ))
        total = query.count()

        # sorting
        sort = request.args.get('sort')
        if sort:
            order = []
            for s in sort.split(','):
                direction = s[0]
                name = s[1:]
                if name not in ['name', 'age', 'email']:
                    name = 'name'
                col = getattr(User, name)
                if direction == '-':
                    col = col.desc()
                order.append(col)
            if order:
                query = query.order_by(*order)

        # pagination
        start = request.args.get('start', type=int, default=-1)
        length = request.args.get('length', type=int, default=-1)
        if start != -1 and length != -1:
            query = query.offset(start).limit(length)

        # response
        return {
            'data': [user.to_dict() for user in query],
            'total': total,
        }


@app.route('/api/data/<int:id>', methods=['POST'])
def update(id):
    with app.app_context():
        data = request.get_json()
        if 'id' not in data:
            abort(400)
        user = User.query.get(data['id'])
        for field in ['name', 'age', 'address', 'phone', 'email']:
            if field in data:
                setattr(user, field, data[field])
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    create_database()
    app.run(port=4000, debug=True)