# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:26:30 2025

@author: quent
"""

import streamlit as st
import pandas as pd

effetstructurels = pd.DataFrame({
    "Catégorie": [
        "Electricity from the grid", 
        "Aviation", 
        "International maritime transport", 
        "Procurement of goods", 
        "Procurement of services"
    ],
    "Effet Structurel": [1.13, 2.0, 2.0, 3.43, 2.32]  # 🔹 Valeurs associées
})
print(effetstructurels["Effet Structurel"][0])
effetstructurels = [
    "Electricity from the grid", "Aviation", "International maritime transport",
    "Procurement of goods", "Procurement of services"
]

import pandas as pd

# 🔹 Création du DataFrame basé sur l'image fournie
binary_table = pd.DataFrame({
    "Nom": ["Services", "Goods", "Travel", "Commuting", "Event"],
    "Electricity from the grid": [1, 0, 0, 0, 0],
    "Aviation": [0, 0, 0, 1, 0],
    "International maritime transport": [0, 0, 0, 0, 0],
    "Procurement of goods": [0, 0, 0, 0, 0],
    "Procurement of services": [0, 0, 0, 0, 0]
})


df = pd.DataFrame({
    "Poste": ["Services", "Goods", "Travel", "Commuting", "Event"],
    "Quantité": [200, 100, 160, 4000, 6],
    "FE": [6, 11, 30, 0.1, 50],
    "Emission": [1200, 1100, 4800, 400, 300]
})

# 🔹 Vérification : Aligner les noms des catégories pour éviter les erreurs
categories = effetstructurels["Catégorie"].tolist()  # Liste des catégories d'effets structurels

# 🔹 Conversion en dictionnaire pour un accès rapide
effet_dict = dict(zip(effetstructurels["Catégorie"], effetstructurels["Effet Structurel"]))

# 🔹 Multiplication : Chaque colonne de binary_table * valeur correspondante dans effetstructurels
for col in categories:
    if col in binary_table.columns:  # Vérifie si la colonne existe dans binary_table
        binary_table[col] = binary_table[col] * effet_dict[col]  # Applique la multiplication

# 🔹 Affichage du DataFrame modifié
print(binary_table)

#df["FE"]=df["FE"]*binary_table["Electricity from the grid"]*effetstructurels["Effet Structurel"][1]

# # 🔹 Vérifier l'alignement des noms (Poste vs Nom)
# df = df.merge(binary_table[["Nom", "Electricity from the grid"]], left_on="Poste", right_on="Nom", how="left")

# 🔹 Fusionner `df` avec **toutes** les colonnes de `binary_table`
df = df.merge(binary_table, left_on="Poste", right_on="Nom", how="left")

# 🔹 Supprimer la colonne "Nom" qui est un doublon de "Poste"
df.drop(columns=["Nom"], inplace=True)


# 🔹 Multiplier la colonne "FE" par "Electricity from the grid"
df["FE x Electricity"] = df["FE"] * df["Electricity from the grid"]

print(df.head())