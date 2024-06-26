from hashlib import sha1
import hashlib
import random
import sys
from faker import Faker
from model import db, Utilisateur,app



with app.app_context():
    # Your Flask-specific code here
    nom = ['diop', 'sylla', 'fall', 'coly', 'sané', 'balde', 'mbengue', 'sarr', 'mar', 'keita', 'preira', 'ndoye']
    prenom = ['babou', 'modou', 'ndeytou', 'banna', 'marem', 'sophy', 'aly', 'penda', 'haby', 'soumba', 'demba', 'abdoulaye']
    faker = Faker()
    n =1000
    # Example code using Flask extensions or database operations
    password = "passera"
    hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
    for i in range(n):

        user = Utilisateur(
            username=faker.name(),
            email=faker.email(),
            password=hashed_password,
            nom=random.choice(nom),
            prenom=random.choice(prenom),
            role_id=random.randint(1, 2),
            region_id=random.randint(1, 14)
        )
        db.session.add(user)

    db.session.commit()
    print(f'Added {n} fake users to the database.')