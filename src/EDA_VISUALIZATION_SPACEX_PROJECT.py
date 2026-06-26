# pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns

#First, let's read the SpaceX dataset into a Pandas dataframe and print its summary
from js import fetch
import io

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
resp = await fetch(URL)
dataset_part_2_csv = io.BytesIO((await resp.arrayBuffer()).to_py())
df=pd.read_csv(dataset_part_2_csv)
df.head(5)

#First, let's try to see how the FlightNumber (indicating the continuous launch attempts.) and Payload variables would affect the launch outcome.
sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()

#TASK 1: Visualize the relationship between Flight Number and Launch Site

## Plot a scatter point chart with x axis to be Flight Number and y axis to be the launch site, and hue to be the class value
sns.catplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df, aspect = 3)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Launch site",fontsize=20)
plt.show()

#TASK 2: Visualize the relationship between Payload Mass and Launch Site
# Plot a scatter point chart with x axis to be Pay Load Mass (kg) and y axis to be the launch site, and hue to be the class value

sns.catplot(y="LaunchSite", x="PayloadMass", hue="Class", data=df, aspect = 3)
plt.xlabel("Pay Load Mass (Kg)",fontsize=20)
plt.ylabel("Launch site",fontsize=20)
plt.show()

#TASK 3: Visualize the relationship between success rate of each orbit type
# use groupby method on Orbit column and get the mean of Class column
# 1. Calculer le taux de réussite moyen (mean de Class) pour chaque type d'orbite
# On réinitialise l'index (.reset_index()) pour transformer le résultat en DataFrame propre pour Seaborn
df_orbit_success = df.groupby('Orbit')['Class'].mean().reset_index()

# Multiplier par 100 pour obtenir un pourcentage (optionnel mais plus parlant graphiquement)
df_orbit_success['SuccessRate'] = df_orbit_success['Class'] * 100

# Tri des données par taux de réussite décroissant pour une meilleure lisibilité du graphique
df_orbit_success = df_orbit_success.sort_values(by='SuccessRate', ascending=False)

# 2. Création du graphique à barres (Barplot) avec Seaborn
plt.figure(figsize=(10, 6))
sns.barplot(
    x='Orbit',
    y='SuccessRate',
    data=df_orbit_success,
    palette='Blues_r'  # Dégradé de bleu (du plus foncé au plus clair)
)

# 3. Personnalisation des axes et du titre
plt.title("Taux de réussite des lancements selon le type d'Orbite", fontsize=16, fontweight='bold', pad=15)
plt.xlabel("Type d'Orbite", fontsize=12)
plt.ylabel("Taux de réussite (%)", fontsize=12)
plt.ylim(0, 105)  # Fixer la limite de l'axe Y à 100%

# Ajouter des étiquettes de données textuelles au-dessus de chaque barre
for index, row in enumerate(df_orbit_success.itertuples()):
    plt.text(
        index,
        row.SuccessRate + 1,
        f"{row.SuccessRate:.1f}%",
        color='black',
        ha="center",
        fontsize=10
    )

plt.tight_layout()
plt.show()

#TASK 4: Visualize the relationship between FlightNumber and Orbit type
# Plot a scatter point chart with x axis to be FlightNumber and y axis to be the Orbit, and hue to be the class value
plt.figure(figsize=(10, 6))
sns.catplot(y="Orbit", x="FlightNumber", hue="Class", data=df, aspect = 2)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Orbit Type",fontsize=20)
plt.show()

#TASK 5: Visualize the relationship between Payload Mass and Orbit type
# Plot a scatter point chart with x axis to be Payload Mass and y axis to be the Orbit, and hue to be the class value

plt.figure(figsize=(10, 6))
sns.catplot(y="Orbit", x="PayloadMass", hue="Class", data=df, aspect = 2)
plt.xlabel("Pay Load Mass (in Kg)",fontsize=20)
plt.ylabel("Orbit Type",fontsize=20)
plt.show()

#TASK 6: Visualize the launch success yearly trend

# A function to Extract years from the date
year=[]
def Extract_year():
    for i in df["Date"]:
        year.append(i.split("-")[0])
    return year
Extract_year()
df['Date'] = year
df.head()

# Plot a line chart with x axis to be the extracted year and y axis to be the success rate

# 2. Calculer le taux de réussite moyen par année
# On regroupe par 'Year' et on calcule la moyenne de la colonne 'Class'
df_yearly_success = df.groupby('Date')['Class'].mean().reset_index()

# Conversion en pourcentage pour l'affichage graphique
df_yearly_success['SuccessRate'] = df_yearly_success['Class'] * 100

# 3. Création du graphique linéaire (Line Chart) avec Seaborn
plt.figure(figsize=(10, 6))
sns.lineplot(
    x='Date',
    y='SuccessRate',
    data=df_yearly_success,
    marker='o',         # Ajoute des points sur chaque année
    linewidth=2.5,
    color='#1f77b4'     # Bleu standard et lisible
)

# 4. Personnalisation esthétique du graphique
plt.title("Évolution annuelle du taux de réussite des lancements", fontsize=16, fontweight='bold', pad=15)
plt.xlabel("Année", fontsize=12)
plt.ylabel("Taux de réussite (%)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)  # Ajout d'une grille pour mieux lire les valeurs
plt.ylim(-5, 105)                          # Ajustement des limites de l'axe Y

# Facultatif : Ajouter la valeur textuelle exacte au-dessus de chaque point
for row in df_yearly_success.itertuples():
    plt.text(
        row.Date,
        row.SuccessRate + 3,
        f"{row.SuccessRate:.0f}%",
        ha='center',
        fontsize=9,
        fontweight='bold'
    )

plt.tight_layout()
plt.show()


#Features Engineering

features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()

#TASK 7: Create dummy variables to categorical columns

# Use get_dummies() function on the categorical columns
# 1. Sélection des colonnes catégorielles à encoder
categorical_cols = ['Orbit', 'LaunchSite', 'LandingPad', 'Serial']

# 2. Application de pd.get_dummies pour créer les variables indicatrices (One-Hot Encoding)
# On passe l'ensemble du DataFrame 'features' mais en spécifiant uniquement les colonnes textuelles dans 'columns'
features_one_hot = pd.get_dummies(features, columns=categorical_cols)

# 3. Affichage d'un aperçu du nouveau DataFrame
print("Aperçu des premières lignes après One-Hot Encoding :")
print(features_one_hot.head())

#TASK 8: Cast all numeric columns to float64
# Conversion de l'ensemble du DataFrame en float64
features_one_hot = features_one_hot.astype('float64')

# Vérification du nombre total de colonnes générées
print(f"\nNombre total de caractéristiques (features) après encodage : {features_one_hot.shape[1]}")

features_one_hot.to_csv('dataset_part_3.csv', index=False)