# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 11:19:13 2025

@author: quent
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Données de base pour les graphiques
Barplottest = {
    "x": ["Category A", "Category B", "Category C"],
    "y": [10, 20, 30],
    "name": "Impact Example"
}

LinePlottest = {
    "x": ["January", "February", "March"],
    "y": [100, 150, 120],
    "name": "Financial Trend"
}

# Fonction pour mettre à jour les données
def update_data(target1, target2):
    # Mise à jour des valeurs pour Barplottest
    updated_bar_y = [value * target1 for value in Barplottest["y"]]
    updated_bar = {
        "x": Barplottest["x"],
        "y": updated_bar_y,
        "name": Barplottest["name"]
    }

    # Mise à jour des valeurs pour LinePlottest
    updated_line_y = [value * target2 for value in LinePlottest["y"]]
    updated_line = {
        "x": LinePlottest["x"],
        "y": updated_line_y,
        "name": LinePlottest["name"]
    }

    return updated_bar, updated_line

# Interface utilisateur Streamlit
st.title("Interactive Impact Dashboard")

# Sliders pour ajuster les targets
target1 = st.slider("Adjust Target 1", min_value=0.0, max_value=5.0, value=1.0, step=0.1)
target2 = st.slider("Adjust Target 2", min_value=0.0, max_value=5.0, value=1.0, step=0.1)

# Mise à jour des données
updated_bar, updated_line = update_data(target1, target2)

# Affichage du graphique Bar Plot
st.subheader("Updated Bar Plot")
fig_bar, ax_bar = plt.subplots()
ax_bar.bar(updated_bar["x"], updated_bar["y"], color="blue", alpha=0.7)
ax_bar.set_title(updated_bar["name"])
ax_bar.set_ylabel("Values")
ax_bar.set_xlabel("Categories")
st.pyplot(fig_bar)

# Affichage du graphique Line Plot
st.subheader("Updated Line Plot")
fig_line, ax_line = plt.subplots()
ax_line.plot(updated_line["x"], updated_line["y"], marker="o", linestyle="-", color="green")
ax_line.set_title(updated_line["name"])
ax_line.set_ylabel("Values")
ax_line.set_xlabel("Time")
st.pyplot(fig_line)