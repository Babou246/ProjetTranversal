from app import db, Utilisateur
import csv

# import sqlite3

# # Connexion à la base de données SQLite
# conn = sqlite3.connect('data.sqlite')

# # Création d'un curseur pour exécuter des requêtes
# cursor = conn.cursor()

# # Vider une table spécifique
# table_name = 'user'
# query = f'DELETE FROM {table_name}'
# cursor.execute(query)

# # Valider la transaction et fermer la connexion
# conn.commit()
# conn.close()




def create_import():
    """Generate fake users."""
    with open('MOCK_DATA.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user = Utilisateur(name=row['name'],
                        age=int(row['age']),
                        address=row['address'],
                        phone=row['phone'],
                        email=row['email'])
            db.session.add(user)
        db.session.commit()
    print(f'Added fake users to the database.')

