import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib

# Charger les données depuis le fichier CSV
df = pd.read_csv('uploads/HEVTimes_Data.csv')

# Vérifier les noms de colonnes actuels dans le DataFrame
print(df.columns)

# Sélectionner les colonnes pertinentes pour le clustering
features = ['temperature', 'time_hours', 'time_mins', 'log_reduction',
            'starting_value', 'source', 'new_data', 'run_number', 'exclude_data']

# Vérifier la présence des colonnes dans le DataFrame
missing_columns = [col for col in features if col not in df.columns]
if missing_columns:
    raise ValueError(f"Les colonnes suivantes sont manquantes dans le DataFrame : {missing_columns}")

# Exclure les lignes avec des valeurs manquantes uniquement dans les colonnes spécifiées
df = df.dropna(subset=features)

# Normalisation des données
X = df[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Réduction de dimension avec PCA
pca = PCA(n_components=3)  # Réduire à 3 composants principaux
X_pca = pca.fit_transform(X_scaled)

# Initialiser et entraîner le modèle K-Means sur les données réduites
kmeans = KMeans(n_clusters=3)  # Spécifier le nombre de clusters
kmeans.fit(X_pca)

# Ajouter les prédictions de clusters au DataFrame original
df['cluster'] = kmeans.labels_

# Enregistrer le modèle K-Means pour une utilisation ultérieure
joblib.dump(kmeans, 'kmeans_model.pkl')
