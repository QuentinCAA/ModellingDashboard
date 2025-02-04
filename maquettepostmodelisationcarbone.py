# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 08:58:22 2025

@author: quent
"""


# ================================
# Table des Matières
# ================================
# Notes de développement             -> juste après la table des Matières
# 1. Initialisation du code          -> environ Ligne 50 (pas possible de créer des liens donc plus facile est controle F)
# 2. Onglet 1 : Accueil              -> environ Ligne 70
# 3. Onglet 2 : Croissance           -> environ Ligne 120
# 4. Onglet 3 : Effets structurels   -> environ Ligne 165
# 5. Onglet 4 : Solutions            -> environ Ligne 255
# 6. Onglet 5 : Target               -> environ Ligne 310
# ================================


# =========================================
# Notes de développement (à remplir à chaque que je ferme le doc)
# =========================================

## À faire
#- [ ] Coeff liées à solutions peuvent jouer sur quantité et sur FE/prix en plus d'avoir de targets en 2030 et en 2035 -> besoin de 4 types de coeff ? (voir avec Paolo)
#- [ ] 

## Fait
#- [x] Création des solutions dans l onglet 3
#- [x] Création de la possibilité de déposer un fichier template de bilan carbone
#- [x] Interface web test pour les targets et l'affichage de graphe et les fonctions d'actualisation ("maquette target dashboard")
#- [x] Modifier target auto après solutions
#- [x] Tenter de déployer le code pour l'envoyer à Paolo (créer github pour pouvoir déployer app)
#- [x] Intégrer la dimension financière
#- [x] Repenser structure pages effets structurels et croissance par rapport présentation Paolo
#- [x] Simplifier les fonctions d'actualisation avec des multiplication de matrices (ou au moins mettre dans des boucles)
#- [x] Simplifier et expliquer le code


## Idées futures
#- Logique à repenser autour des dates (choix à faire, mettre chaquye année ou seulement 2,3 , lesquelles? Via discussion en réu pôle metrics
# + décider de la manière dont on gère croissance et effets structurels / rapport année = décision de groupe ) Via discussion en réu pôle metrics
#- 


# =========================================
#1. Initialisation du code
# =========================================


import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
# Active le mode large pour réduire les marges (à mettre en première commande streamlit du code sinon bug)
st.set_page_config(layout="wide") 
# Onglets principaux
tabs = st.tabs(["Accueil", "Croissance", "Effets structurels", "Solutions", "Target Dashboard"])

#Préparation interaction création solution, target dashboard
if "solutions" not in st.session_state:
    st.session_state["solutions"] = pd.DataFrame(columns=["Nom", "Année"])
if "Nom" not in st.session_state:
    st.session_state["Nom"] = None  # Ou une autre valeur par défaut
    
years = [2025, 2030, 2035]    
# ========================================= 
# Onglet 1 : Accueil
# =========================================

def actualisationémission(data):
    data["Emission"]=data["Quantité"]*data["FE"]
    

def affichergraphe(dataI,data30,data35):
        
        services = [dataI["Emission"][0],data30["Emission"][0],data35["Emission"][0]]
        goods = [dataI["Emission"][1],data30["Emission"][1],data35["Emission"][1]]
        travel = [dataI["Emission"][2],data30["Emission"][2],data35["Emission"][2]]
        commuting = [dataI["Emission"][3],data30["Emission"][3],data35["Emission"][3]]
        event = [dataI["Emission"][4],data30["Emission"][4],data35["Emission"][4]]
        
        categories = np.array([services, goods, travel, commuting, event])
        cumulative = np.cumsum(categories, axis=0)
        
        # Create the stacked area plot for figca2
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.fill_between(years, 0, cumulative[0], label='Services', alpha=0.7)
        ax.fill_between(years, cumulative[0], cumulative[1], label='Goods', alpha=0.7)
        ax.fill_between(years, cumulative[1], cumulative[2], label='Travel', alpha=0.7)
        ax.fill_between(years, cumulative[2], cumulative[3], label='Commuting', alpha=0.7)
        ax.fill_between(years, cumulative[3], cumulative[4], label='Event', alpha=0.7)
        
        # Customize the plot for figca2
        ax.set_title("Carbon Modelling", fontsize=14)
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("kgCO2", fontsize=12)
        ax.set_xticks(years)
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.6)
        
        # Display the plot after the structural effects in Streamlit
        st.pyplot(fig)

with tabs[0]:
    st.title("Accueil : Bienvenue dans l'application qui vous permettra de modéliser vos solutions et vos trajectoires")
    st.write("Bienvenue ! Téléversez vos fichier Excels d'empreinte carbone et de modélisation financière.")
    
    
    col1,col2=st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Téléversez le fichier empreinte", type=["xlsx"])
        if uploaded_file:
            try:
                data = pd.read_excel(uploaded_file)
               
                
                databaseline=data.copy()
                data2030=data.copy()
                data2035=data.copy()
                
                st.success("Fichier téléversé avec succès !")
                
                st.write("Aperçu des données :", databaseline.head())
                fig = px.bar(databaseline, x="Poste", y="Emission", title="Émissions par Poste", labels={"Emission": "Émissions (kgCO2)"})
                st.plotly_chart(fig)
                
            except Exception as e:
                st.error(f"Erreur lors de la lecture du fichier : {e}")
            
    with col2:
        
        uploaded_file2 = st.file_uploader("Téléversez le fichier finance", type=["xlsx"])

        
        if uploaded_file2:
            try:
                data2 = pd.read_excel(uploaded_file2)
                
                databaselineF=data2.copy()
                data2030F=data2.copy()
                data2035F=data2.copy()
                
                st.success("Fichier téléversé avec succès !")
                
                st.write("Aperçu des données :", databaselineF.head())
                fig2 = px.bar(databaselineF, x="Poste", y="Emission", title="Émissions par Poste", labels={"Emission": "Émissions (kgCO2)"})
                st.plotly_chart(fig2)
                
            except Exception as e:
                st.error(f"Erreur lors de la lecture du fichier : {e}")
                
                
# =========================================
# Onglet 2 : Croissance de l'organisation
# =========================================


with tabs[1]:
    
    # 🔹 Initialisation des années
    annees = list(range(2024, 2036))
    
    # 🔹 Stocker chaque budget séparément dans `st.session_state` comme un `st.slider()`
    if "budgets" not in st.session_state:
        st.session_state["budgets"] = {annee: 0.0 for annee in annees}  # 🔹 Dictionnaire au lieu d'un DataFrame
    
    st.title("📊 Saisie des Budgets de l'Organisation (2024 - 2035)")
    
    # 🔹 Interface de saisie (similaire aux `st.slider()`)
    for annee in annees:
        st.session_state["budgets"][annee] = st.number_input(
            f"Budget pour {annee} (€)", 
            min_value=-1000000.0, max_value=1000000.0, 
            value=st.session_state["budgets"][annee], 
            step=0.1
        )
    
    # ✅ Affichage des budgets mis à jour
    st.write("Budgets enregistrés :", st.session_state["budgets"])
    
    col1,col2= st.columns(2)
    
    if uploaded_file:
     
        budget_2024 = st.session_state["budgets"].get(2024, 1)  # Valeur par défaut = 1 pour éviter une division par zéro
        budget_2030 = st.session_state["budgets"].get(2030, 1)
        budget_2035 = st.session_state["budgets"].get(2035, 1)

        data2030["Quantité"] = databaseline["Quantité"] * budget_2030 / budget_2024
        data2035["Quantité"] = databaseline["Quantité"] * budget_2035 / budget_2024
        # data2030["Quantité"]=databaseline["Quantité"]*st.session_state["budgets"][5]/st.session_state["budgets"][0]
        
        with col1:
            st.write("Aperçu des données :", data2030.head())
        with col2:
            st.write("Aperçu des données :", data2035.head())
            
        actualisationémission(data2030)
        actualisationémission(data2035)
        
        with col1:
            st.write("Aperçu des données actualisées:", data2030.head())
            
        with col2:
            st.write("Aperçu des données actualisées:", data2035.head())
        
        affichergraphe(databaseline, data2030, data2035)
    
    #Besoin d'actualiser les données quantité désormais et de créer une fonction actualisation pour emissions
                   
# =========================================
# Onglet 3 : Effets structurels et impacts
# =========================================


with tabs[2]:
    
    # 🔹 Création du DataFrame effet structurels
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
    
    st.title("📊 Tableau des Effets Structurels")
    st.write(effetstructurels.head())
    # Aligenement effets structurels avec EFs sur lesquels ils ont une influence
    # print(effetstructurels["Catégorie"])
    # 🔹 Effets structurels (les colonnes du nouveau tableau)
    # effetstructurels = ["Electricity from the grid", "Aviation", "International maritime transport", "Procurement of goods", "Procurement of services"]
    if uploaded_file:
       # 🔹 Effets structurels (colonnes du tableau interactif)
       effetstructurels1 = [
           "Electricity from the grid", "Aviation", "International maritime transport",
           "Procurement of goods", "Procurement of services"
       ]

       # 🔹 Vérifier si le tableau interactif est déjà stocké dans `st.session_state`
       if "tableau_interactif" not in st.session_state:
           st.session_state["tableau_interactif"] = pd.DataFrame({
               "Nom": databaseline["Poste"],  # Première colonne (identique à `databaseline`)
               **{col: [False] * len(databaseline) for col in effetstructurels1}  # Cases décochées (False par défaut)
           })

       st.title("📊 Tableau Interactif - Effets Structurels")

       # 🔹 Interface interactive avec cases à cocher
       edited_df = st.data_editor(
           st.session_state["tableau_interactif"],
           use_container_width=True,
           hide_index=True,
           num_rows="fixed",
           column_config={col: st.column_config.CheckboxColumn() for col in effetstructurels1}
       )

       # 🔹 Sauvegarde des modifications
       if not edited_df.equals(st.session_state["tableau_interactif"]):
           st.session_state["tableau_interactif"] = edited_df

       # 🔹 Conversion en tableau numérique avec 0 et 1 pour les calculs
       binary_table = st.session_state["tableau_interactif"].copy()  # Copie pour éviter d'écraser les données d'origine

       # ✅ Vérifier les colonnes existantes
       st.write("🔍 Colonnes disponibles dans binary_table :", binary_table.columns.tolist())

       # ✅ Vérifier que chaque colonne de effetstructurels existe bien avant conversion
       for col in effetstructurels:
           if col in binary_table.columns:
               binary_table[col] = binary_table[col].fillna(False).astype(bool).astype(int)
           else:
               st.warning(f"⚠️ Attention : La colonne '{col}' n'existe pas dans binary_table !")

       
       #Actualisation des FEs FI 2030 et 2035 
       binary_table2030=binary_table.copy()
       binary_table2035=binary_table.copy()
       
       # ✅ Extraire correctement les catégories
       categories = effetstructurels["Catégorie"].tolist()

       # ✅ Convertir effetstructurels en dictionnaire pour faciliter l'accès
       effet_dict = dict(zip(effetstructurels["Catégorie"], effetstructurels["Effet Structurel"]))

       # 🔹 Appliquer la multiplication sur chaque colonne de binary_table
       for col in categories:
           if col in binary_table2030.columns:  # Vérifie si la colonne existe
               binary_table2030[col] = binary_table2030[col] * (1-effet_dict[col]/100)**6
               binary_table2035[col] = binary_table2035[col] * (1-effet_dict[col]/100)**11
               
               #On veut désormais pouvoir multiplier les FE par tous ces chiffres et donc 1 devient le chiffre neutre, on remplace donc les 0 par des 1
               
       binary_table2030 = binary_table2030.replace(0, 1)
       binary_table2035 = binary_table2035.replace(0, 1)
       # 🔹 Fusionner `df` avec **toutes** les colonnes de `binary_table`
       data2030 = data2030.merge(binary_table2030, left_on="Poste", right_on="Nom", how="left")
       data2035 = data2035.merge(binary_table2035, left_on="Poste", right_on="Nom", how="left")

       # 🔹 Supprimer la colonne "Nom" qui est un doublon de "Poste"
       data2030.drop(columns=["Nom"], inplace=True)
       data2035.drop(columns=["Nom"], inplace=True)
       
       col1,col2= st.columns(2)
       
       with col2:
           st.write(data2035.head())
       with col1:
           st.write(data2030.head())
    
       
       
       data2030["FE"]=data2030["FE"]*data2030["Electricity from the grid"]*data2030["Aviation"]* data2030["International maritime transport"] * data2030["Procurement of goods"]*data2030["Procurement of services"]
       data2035["FE"]=data2035["FE"]*data2035["Electricity from the grid"]*data2035["Aviation"]* data2035["International maritime transport"] * data2035["Procurement of goods"]*data2035["Procurement of services"]
       affichergraphe(databaseline, data2030, data2035)
       actualisationémission(data2030)
       actualisationémission(data2035)
       st.write("FE et Emissions mises à jour") 
       
       
       with col2:
           st.write(data2035.head())
       with col1:
           st.write(data2030.head())

# =========================================    
# Onglet 4 : Création de solutions
# =========================================


with tabs[3]:
    
    
    st.title("Créer une solution")

    # Étape 1 : Nom de la solution
    solution_name = st.text_input("Nom de la solution :", "")

    # Étape 2 : Choix des années d'implémentation
    st.write("Choisissez les années d'implémentation :")
    implement_2030 = st.checkbox("Implémenter en 2030")
    implement_2035 = st.checkbox("Implémenter en 2035")

    # Étape 3 : Entrée des coefficients
    st.write("Entrez les coefficients pour les 5 éléments :")
    #elements = ["Services", "Goods", "Travel", "Commuting", "Event"]
    
    col1,col2= st.columns(2)
    
    with col1:
        coefficient_services = st.number_input("Coefficient pour services :", value=0.0, step=0.1)
        coefficient_goods = st.number_input("Coefficient pour goods :", value=0.0, step=0.1)
        coefficient_travel = st.number_input("Coefficient pour travel :", value=0.0, step=0.1)
        coefficient_commuting = st.number_input("Coefficient pour commuting :", value=0.0, step=0.1)
        coefficient_event = st.number_input("Coefficient pour event :", value=0.0, step=0.1)
        
    with col2:
        coefficient_servicesF = st.number_input("Coefficient cout pour services :", value=0.0, step=0.1)
        coefficient_goodsF = st.number_input("Coefficient cout pour goods :", value=0.0, step=0.1)
        coefficient_travelF = st.number_input("Coefficient cout pour travel :", value=0.0, step=0.1)
        coefficient_commutingF = st.number_input("Coefficient cout pour commuting :", value=0.0, step=0.1)
        coefficient_eventF = st.number_input("Coefficient cout pour event :", value=0.0, step=0.1)
    target_idea = st.number_input("Si vous avez déjà une première idée de la cible qui sera visée :", value=0.0, step=1.0)
    

    
    # Étape 4 : Sauvegarder la solution
    if st.button("Enregistrer la solution"):
        if not solution_name:
            st.error("Veuillez entrer un nom pour la solution.")
        elif not (implement_2030 or implement_2035):
            st.error("Veuillez sélectionner au moins une année d'implémentation.")
        else:
            # Ajouter les données au DataFrame
            for year in [2030, 2035]:
                if (year == 2030 and implement_2030) or (year == 2035 and implement_2035):
                    
                    # Créer un DataFrame temporaire pour la nouvelle solutio
                    new_row = pd.DataFrame([{"Nom": solution_name, "Année": year, "Coefficient pour services": coefficient_services, 
                                             "Coefficient pour goods": coefficient_goods,"Coefficient pour travel": coefficient_travel, "Coefficient pour commuting": coefficient_commuting, 
                                             "Coefficient pour event": coefficient_event,"Coefficient cout pour services":coefficient_servicesF,"Coefficient cout pour goods":coefficient_goodsF,
                                             "Coefficient cout pour travel":coefficient_travelF, "Coefficient cout pour commuting":coefficient_commutingF,
                                             "Coefficient cout pour event":coefficient_eventF , "Target": target_idea}])
                    
                    # Concaténer au DataFrame existant dans le session_state
                    st.session_state["solutions"] = pd.concat([st.session_state["solutions"], new_row], ignore_index=True)
                        # Ajouter une cible initiale pour chaque combinaison solution/année
                    #st.session_state["Target"][f"{solution_name}_{year}"] = 0.0 #pas sûr que ce soit encore nécessaire, à tester
            st.success(f"Solution '{solution_name}' ajoutée avec succès !")

# =========================================
# Onglet 5 : Interactive Target Dashboard
# =========================================


with tabs[4]:
    st.title("Interactive Target Dashboard")
    
    
    
    st.title("Définir les targets des solutions")

    # Vérifier si des solutions existent
    if not st.session_state["solutions"].empty:
        
        
        solutionsrows,solutionscolumns = st.session_state["solutions"].shape
        st.write("Solutions disponibles :",solutionsrows )
        st.dataframe(st.session_state["solutions"])
       
        for i in range(solutionsrows):
            name = st.session_state["solutions"].iloc[i, 0]
            st.write ("Name:", name)
            
            st.session_state["solutions"].iloc[i, 12]=st.slider(name, min_value=0.0, max_value=100.0, value=0.0, step=1.0)
            
        st.dataframe(st.session_state["solutions"])    
        col1,col2= st.columns(2)
        with col1:
            if uploaded_file:
                for j in range(solutionsrows):
                    if st.session_state["solutions"].iloc[j, 1] == 2030:
                        for k in range (5):
                            data2030["Quantité"][k] = data2030["Quantité"] [k]+ data2030["Quantité"][k]*st.session_state["solutions"].iloc[j,2+k]*st.session_state["solutions"].iloc[j, 12]/100
                            data2030["Emission"][k] = data2030["Emission"] [k]+ data2030["Emission"][k]*st.session_state["solutions"].iloc[j,2+k]*st.session_state["solutions"].iloc[j, 12]/100
                    else : 
                        for l in range (5):
                            data2035["Quantité"][l] = data2035["Quantité"] [l]+ data2035["Quantité"][l]*st.session_state["solutions"].iloc[j,2+l]*st.session_state["solutions"].iloc[j, 12]/100
                            data2035["Emission"][l] = data2035["Emission"] [l]+ data2035["Emission"][l]*st.session_state["solutions"].iloc[j,2+l]*st.session_state["solutions"].iloc[j, 12]/100
                #st.write("data2030", data2030.head())
                #st.write("data2030F", data2030F.head())
                
                st.write("data2030", data2030.head())
                
                services = [databaseline["Emission"][0],data2030["Emission"][0],data2035["Emission"][0]]
                goods = [databaseline["Emission"][1],data2030["Emission"][1],data2035["Emission"][1]]
                travel = [databaseline["Emission"][2],data2030["Emission"][2],data2035["Emission"][2]]
                commuting = [databaseline["Emission"][3],data2030["Emission"][3],data2035["Emission"][3]]
                event = [databaseline["Emission"][4],data2030["Emission"][4],data2035["Emission"][4]]
                
                categoriesca2 = np.array([services, goods, travel, commuting, event])
                cumulativeca2 = np.cumsum(categoriesca2, axis=0)
                
                # Create the stacked area plot for figca2
                figca2, ax = plt.subplots(figsize=(10, 6))
                ax.fill_between(years, 0, cumulativeca2[0], label='Services', alpha=0.7)
                ax.fill_between(years, cumulativeca2[0], cumulativeca2[1], label='Goods', alpha=0.7)
                ax.fill_between(years, cumulativeca2[1], cumulativeca2[2], label='Travel', alpha=0.7)
                ax.fill_between(years, cumulativeca2[2], cumulativeca2[3], label='Commuting', alpha=0.7)
                ax.fill_between(years, cumulativeca2[3], cumulativeca2[4], label='Event', alpha=0.7)
                
                # Customize the plot for figca2
                ax.set_title("Carbon Modelling", fontsize=14)
                ax.set_xlabel("Year", fontsize=12)
                ax.set_ylabel("kgCO2", fontsize=12)
                ax.set_xticks(years)
                ax.legend()
                ax.grid(axis='y', linestyle='--', alpha=0.6)
                
                # Display the plot after the structural effects in Streamlit
                st.pyplot(figca2)
            else: 
                st.warning("Pas de fichiers ca upload")
        
        with col2:
            if uploaded_file2:
                for j in range(solutionsrows):
                    if st.session_state["solutions"].iloc[j, 1] == 2030:
                        for k in range (5):
                            data2030F["Quantité"][k] = data2030F["Quantité"] [k]+ data2030F["Quantité"][k]*st.session_state["solutions"].iloc[j,7+k]*st.session_state["solutions"].iloc[j, 12]/100
                            data2030F["Emission"][k] = data2030F["Emission"] [k]+ data2030F["Emission"][k]*st.session_state["solutions"].iloc[j,7+k]*st.session_state["solutions"].iloc[j, 12]/100
                    else : 
                        for l in range (5):
                            data2035F["Quantité"][l] = data2035F["Quantité"] [l]+ data2035F["Quantité"][l]*st.session_state["solutions"].iloc[j,7+l]*st.session_state["solutions"].iloc[j, 12]/100
                            data2035F["Emission"][l] = data2035F["Emission"] [l]+ data2035F["Emission"][l]*st.session_state["solutions"].iloc[j,7+l]*st.session_state["solutions"].iloc[j, 12]/100
                
                st.write("data2030F", data2030F.head())
                
                
                servicesF = [databaselineF["Emission"][0],data2030F["Emission"][0],data2035F["Emission"][0]]
                goodsF = [databaselineF["Emission"][1],data2030F["Emission"][1],data2035F["Emission"][1]]
                travelF = [databaselineF["Emission"][2],data2030F["Emission"][2],data2035F["Emission"][2]]
                commutingF = [databaselineF["Emission"][3],data2030F["Emission"][3],data2035F["Emission"][3]]
                eventF = [databaselineF["Emission"][4],data2030F["Emission"][4],data2035F["Emission"][4]]
                
                categoriesfi2 = np.array([servicesF, goodsF, travelF, commutingF, eventF])
                cumulativefi2 = np.cumsum(categoriesfi2, axis=0)
                
                # Create the stacked area plot for figca2
                figfi2, ax = plt.subplots(figsize=(10, 6))
                ax.fill_between(years, 0, cumulativefi2[0], label='Services', alpha=0.7)
                ax.fill_between(years, cumulativefi2[0], cumulativefi2[1], label='Goods', alpha=0.7)
                ax.fill_between(years, cumulativefi2[1], cumulativefi2[2], label='Travel', alpha=0.7)
                ax.fill_between(years, cumulativefi2[2], cumulativefi2[3], label='Commuting', alpha=0.7)
                ax.fill_between(years, cumulativefi2[3], cumulativefi2[4], label='Event', alpha=0.7)
                
                # Customize the plot for figca2
                ax.set_title("Finance Modelling", fontsize=14)
                ax.set_xlabel("Year", fontsize=12)
                ax.set_ylabel("kCHF", fontsize=12)
                ax.set_xticks(years)
                ax.legend()
                ax.grid(axis='y', linestyle='--', alpha=0.6)
                
                # Display the plot after the structural effects in Streamlit
                st.pyplot(figfi2)
            else: 
                st.warning("Pas de fichiers fi upload")

    else:
        st.warning("Aucune solution enregistrée.")
        