# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 11:29:09 2025

@author: quent
"""

import streamlit as st
# Active le mode large pour réduire les marges (à mettre en première commande streamlit du code sinon bug)
st.set_page_config(layout="wide")  

import matplotlib.pyplot as plt
import numpy as np



# Data fi
years = [2023, 2027, 2030, 2035]
energyfi = [8, 8, 8, 8]
goodsfi = [2, 2, 2, 2]
financial_supportfi = [10, 10, 10, 10]
servicesfi = [40, 40, 40, 40]
travelsfi = [40, 40, 40, 40]


# Data carbone
years = [2023, 2027, 2030, 2035]
energyca = [3, 3, 3, 3]
goodsca = [1.4, 1.4, 1.4, 1.4]
financial_supportca = [6.5, 6.5, 6.5, 6.5]
servicesca = [37, 37, 37, 37]
travelsca = [33.4, 33.4, 33.4, 33.4]



# Réduire l'espace au-dessus du titre
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1rem;  /* Ajustez ici pour réduire l'espace */
    }
    </style>
""", unsafe_allow_html=True)

# Interface utilisateur Streamlit
st.title("Interactive Target Dashboard")
# Initialiser les variables dans st.session_state si elles n'existent pas encore
if "updatedtravelsca" not in st.session_state:
    st.session_state.updatedtravelsca = [33.4, 33.4, 33.4, 33.4]
if "updatedtravelsfi" not in st.session_state:
    st.session_state.updatedtravelsfi = [40, 40, 40, 40]


#Création des colonnes pour pouvoir mettre curseurs et graphe côte à côte
col1, col2, col3 = st.columns(3)
#col1, col2, col3 = st.columns([1, 2, 1])  
# Largeur relative : 1/2/1, pour faire des colonnes de taille différente

# Curseurs côte à côte
with col1:
    # Sliders pour ajuster les targets
    target1 = st.slider("Plane travel pourcentage reduction by 2030", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
    target2 = st.slider("Plane travel pourcentage reduction by 2035", min_value=0.0, max_value=100.0, value=target1, step=1.0)

with col2:
    target3 = st.slider("Event organisation number reduction", min_value=0.0, max_value=5.0, value=0.0, step=1.0)


    target4 = st.slider("Bank change", min_value=0.0, max_value=1.0, value=0.0, step=1.0)
with col3:
    target5 = st.slider("Energy supplier change", min_value=0.0, max_value=1.0, value=0.0, step=1.0)
# definition facteur financier pour le travel
ftravel = 1

# Fonction pour mettre à jour les données
# def update_data(target1, target2, target3, target4):
#     # Mise à jour des valeurs pour Barplottest
#     updatedtravelsca,updatedtravelsfi = travelsca,travelsfi
#     updatedtravelsca [1] = travelsca[1] *(100-target1/2)/100
#     updatedtravelsca [2] = travelsca[2] *(100-target1)/100
#     updatedtravelsca [3] = travelsca[3] *(100-target2)/100
#     updatedtravelsfi [1] = travelsfi[1] *(100+target1/2*ftravel)/100
#     updatedtravelsfi [2] = travelsfi[2] *(100+target1*ftravel)/100
#     updatedtravelsfi [3] = travelsfi[3] *(100+target2*ftravel)/100
    
    

#     return updatedtravelsca,updatedtravelsfi


def update_data(target1, target2,target3, target4,target5):
    # Création de copies pour éviter les modifications directes
    updatedtravelsca = st.session_state.updatedtravelsca[:]
    updatedtravelsfi = st.session_state.updatedtravelsfi[:]

    ftravel = 1  # Facteur financier (tu peux le garder global si nécessaire)

    # Mise à jour des valeurs
    updatedtravelsca[1] = updatedtravelsca[1] * (100 - target1 / 2) / 100
    updatedtravelsca[2] = updatedtravelsca[2] * (100 - target1) / 100
    updatedtravelsca[3] = updatedtravelsca[3] * (100 - target2) / 100

    updatedtravelsfi[1] = updatedtravelsfi[1] * (100 + target1 / 2 * ftravel) / 100
    updatedtravelsfi[2] = updatedtravelsfi[2] * (100 + target1 * ftravel) / 100
    updatedtravelsfi[3] = updatedtravelsfi[3] * (100 + target2 * ftravel) / 100

    # Enregistrer dans st.session_state pour que ça ne se réinitialise pas
    st.session_state.updatedtravelsca = updatedtravelsca
    st.session_state.updatedtravelsfi = updatedtravelsfi

# Mise à jour des données
# updatedtravelsca,updatedtravelsfi=update_data(target1, target2, target3, target4,target5)
update_data(target1, target2, target3, target4,target5)

assert all(len(lst) == len(years) for lst in [energyfi, goodsfi, financial_supportfi, servicesfi, travelsfi]), "Inconsistent list sizes"
assert all(len(lst) == len(years) for lst in [energyca, goodsca, financial_supportca, servicesca, st.session_state.updatedtravelsca]), "Inconsistent list sizes"

# Prepare data for stacked area plot
categoriesfi = np.array([energyfi, goodsfi, financial_supportfi, servicesfi, travelsfi])
cumulativefi = np.cumsum(categoriesfi, axis=0)


# Prepare data for stacked area plot
categoriesca = np.array([energyca, goodsca, financial_supportca, servicesca, travelsca])
cumulativeca = np.cumsum(categoriesca, axis=0)

# Deux colonnes pour les graphiques
st.subheader("Visualizations")
col1, col2 = st.columns(2)

with col1: 
    
    # Create the stacked area plot
    figfi, ax = plt.subplots(figsize=(10, 6))
    ax.fill_between(years, 0, cumulativefi[0], label='Energy', alpha=0.7)
    ax.fill_between(years, cumulativefi[0], cumulativefi[1], label='Goods', alpha=0.7)
    ax.fill_between(years, cumulativefi[1], cumulativefi[2], label='Financial support', alpha=0.7)
    ax.fill_between(years, cumulativefi[2], cumulativefi[3], label='Services', alpha=0.7)
    ax.fill_between(years, cumulativefi[3], cumulativefi[4], label='Travels', alpha=0.7)
    
    # Customize the plot for figfi
    ax.set_title("Financial Modelling", fontsize=14)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Euros", fontsize=12)
    ax.set_xticks(years)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    
    # Display the plot in Streamlit
    st.pyplot(figfi)

with col2:
    
    # Create the stacked area plot
    figca, ax = plt.subplots(figsize=(10, 6))
    ax.fill_between(years, 0, cumulativeca[0], label='Energy', alpha=0.7)
    ax.fill_between(years, cumulativeca[0], cumulativeca[1], label='Goods', alpha=0.7)
    ax.fill_between(years, cumulativeca[1], cumulativeca[2], label='Financial support', alpha=0.7)
    ax.fill_between(years, cumulativeca[2], cumulativeca[3], label='Services', alpha=0.7)
    ax.fill_between(years, cumulativeca[3], cumulativeca[4], label='Travels', alpha=0.7)
    
    # Customize the plot for figca
    ax.set_title("Carbon Modelling", fontsize=14)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("kgCO2", fontsize=12)
    ax.set_xticks(years)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    
    # Display the plot in Streamlit
    st.pyplot(figca)



