# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 10:45:36 2025

@author: quent
"""

# ================================
# Table des Matières
# ================================
# Notes de développement             -> juste après la table des Matières
# 1. Initialisation du code          -> environ Ligne 45 (pas possible de créer des liens donc plus facile est controle F)
# 2. Onglet 1 : Accueil              -> environ Ligne 65
# 3. Onglet 2 : Croissance           -> environ Ligne 95
# 4. Onglet 3 : Effets structurels   -> environ Ligne 165
# 5. Onglet 4 : Solutions            -> environ Ligne 255
# 6. Onglet 5 : Target               -> environ Ligne 310
# ================================


# =========================================
# Notes de développement (à remplir à chaque que je ferme le doc)
# =========================================

## À faire
#- [ ] Tenter de déployer le code pour l'envoyer à Paolo (créer github pour pouvoir déployer app)
#- [ ] Intégrer la dimension financière A faire avant mercredi

## Fait
#- [x] Création des solutions dans l onglet 3
#- [x] Création de la possibilité de déposer un fichier template de bilan carbone
#- [x] Interface web test pour les targets et l'affichage de graphe et les fonctions d'actualisation ("maquette target dashboard")
#- [x] Modifier target auto après solutions

## Idées futures
#- Logique à repenser autour des dates (choix à faire, mettre chaquye année ou seulement 2,3 , lesquelles? Via discussion en réu pôle metrics
# + décider de la manière dont on gère croissance et effets structurels / rapport année = décision de groupe ) Via discussion en réu pôle metrics
#- Simplifier les fonctions d'actualisation avec des multiplication de matrices (ou au moins mettre dans des boucles) (est-ce qu'on a des contraintes de temps/ d'efficacité du code ?) pas prioritaire



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

if "solutions" not in st.session_state:
    st.session_state["solutions"] = pd.DataFrame(columns=["Nom", "Année"])
#if "Target" not in st.session_state:
    #st.session_state["Target"] = {}
if "Nom" not in st.session_state:
    st.session_state["Nom"] = None  # Ou une valeur par défaut
    
    
# ========================================= 
# Onglet 1 : Accueil
# =========================================


with tabs[0]:
    st.title("Accueil : Téléverser un fichier Excel")
    st.write("Bienvenue ! Téléversez votre fichier Excel avec le template défini pour commencer.")
    uploaded_file = st.file_uploader("Téléversez un fichier Excel", type=["xlsx"])
    # Étape 1 : Créer un DataFrame vide
    columns = ["Poste", "Quantité", "FE", "Emission"]
    databc = pd.DataFrame(columns=columns)

    if uploaded_file:
        try:
            data = pd.read_excel(uploaded_file)
            databc=data
            
            st.success("Fichier téléversé avec succès !")
            st.write("Aperçu des données :", data.head())
            
            st.write("Transfert 1 réussi? :", databc.head())
            fig = px.bar(databc, x="Poste", y="Emission", title="Émissions par Poste", labels={"Emission": "Émissions (kgCO2)"})
            st.plotly_chart(fig)
            
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {e}")
    
# =========================================
# Onglet 2 : Croissance de l'organisation
# =========================================


with tabs[1]:
    print(databc)
    st.write("test transfert des datas importées vers deuxième onglet:", databc.head())
    # Ajouter une interaction : Filtrer par seuil d'émission
    #st.sidebar.title("Filtrage")
    #emission_threshold = st.sidebar.slider("Afficher les postes avec des émissions supérieures à :", 
                                           #min_value=0, max_value=int(df["Emission"].max()), value=500)
    
    #filtered_df = df[df["Emission"] > emission_threshold]
    #st.write(f"Postes avec des émissions supérieures à {emission_threshold} :")
    #st.dataframe(filtered_df)
    #st.title("Définir la croissance de l'organisation")
    
    col1,col2=st.columns(2)
    
    with col1:
        growth_rate_2030 = st.slider("Taux de croissance d'ici 2030 (%)", min_value=-50, max_value=50, value=0, step=1)
        st.write(f"Croissance 2030 définie à **{growth_rate_2030}%**.")
        
    with col2:
        growth_rate_2035 = st.slider("Taux de croissance entre 2030 et 2035 (%)", min_value=-50, max_value=50, value=0, step=1)
        st.write(f"Croissance 2035 définie à **{growth_rate_2035}%**.")
    if uploaded_file:
        data2030=databc.copy()
        data2035=databc.copy()
        
        data2030["Quantité"]=data2030["Quantité"]*(1+growth_rate_2030/100)
        data2030["Emission"]=data2030["Emission"]*(1+growth_rate_2030/100)
        data2035["Quantité"]=data2035["Quantité"]*(1+growth_rate_2030/100)
        data2035["Emission"]=data2035["Emission"]*(1+growth_rate_2030/100)
        #st.write("Croissance appliquée à 2030 :", data2030.head())
        
        data2035["Quantité"]=data2035["Quantité"]*(1+growth_rate_2035/100)
        data2035["Emission"]=data2035["Emission"]*(1+growth_rate_2035/100)
        #st.write("Croissance appliquée à 2035 :", data2035.head())
        
        services = [databc["Emission"][0],data2030["Emission"][0],data2035["Emission"][0]]
        goods = [databc["Emission"][1],data2030["Emission"][1],data2035["Emission"][1]]
        travel = [databc["Emission"][2],data2030["Emission"][2],data2035["Emission"][2]]
        commuting = [databc["Emission"][3],data2030["Emission"][3],data2035["Emission"][3]]
        event = [databc["Emission"][4],data2030["Emission"][4],data2035["Emission"][4]]
        
        years = [2025, 2030, 2035]
        
        categoriesca1 = np.array([services, goods, travel, commuting, event])
        cumulativeca1 = np.cumsum(categoriesca1, axis=0)
        
        # Create the stacked area plot
        figca1, ax = plt.subplots(figsize=(10, 6))
        ax.fill_between(years, 0, cumulativeca1[0], label='Services', alpha=0.7)
        ax.fill_between(years, cumulativeca1[0], cumulativeca1[1], label='Goods', alpha=0.7)
        ax.fill_between(years, cumulativeca1[1], cumulativeca1[2], label='Travel', alpha=0.7)
        ax.fill_between(years, cumulativeca1[2], cumulativeca1[3], label='Commuting', alpha=0.7)
        ax.fill_between(years, cumulativeca1[3], cumulativeca1[4], label='Event', alpha=0.7)
        
        # Customize the plot for figca
        ax.set_title("Carbon Modelling", fontsize=14)
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("kgCO2", fontsize=12)
        ax.set_xticks(years)
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.6)
        
        # Display the plot in Streamlit
        st.pyplot(figca1)
        
                    
# =========================================
# Onglet 3 : Effets structurels et impacts
# =========================================


with tabs[2]:
    
    col1,col2= st.columns(2)
    
    st.title("Effets structurels et impacts")
    with col1:

    
        structural_effect_services_2030 = st.slider("Effet structurel services 2030(%)", min_value=-50, max_value=50, value=0, step=1)
    
        structural_effect_goods_2030 = st.slider("Effet structurel goods 2030(%)", min_value=-50, max_value=50, value=0, step=1)
    
        structural_effect_travel_2030 = st.slider("Effet structurel travel 2030(%)", min_value=-50, max_value=50, value=0, step=1)
    
        structural_effect_commuting_2030 = st.slider("Effet structurel commuting 2030(%)", min_value=-50, max_value=50, value=0, step=1)
    
        structural_effect_event_2030 = st.slider("Effet structurel event 2030(%)", min_value=-50, max_value=50, value=0, step=1)
    
    
    with col2:
        structural_effect_services_2035 = st.slider("Effet structurel services 2035(%)", min_value=-50, max_value=50, value=0, step=1)
        structural_effect_goods_2035 = st.slider("Effet structurel goods 2035(%)", min_value=-50, max_value=50, value=0, step=1)
        structural_effect_travel_2035 = st.slider("Effet structurel travel 2035(%)", min_value=-50, max_value=50, value=0, step=1)
        structural_effect_commuting_2035 = st.slider("Effet structurel commuting 2035(%)", min_value=-50, max_value=50, value=0, step=1)
        structural_effect_event_2035 = st.slider("Effet structurel event 2035(%)", min_value=-50, max_value=50, value=0, step=1)
        
    # Mise à jour des FEs et des Emissions en fonction des effets structurels
    if uploaded_file:
        data2030["FE"][0]=data2030["FE"][0]*(1+structural_effect_services_2030/100)
        data2030["Emission"][0]=data2030["Emission"][0]*(1+structural_effect_services_2030/100)
        
        data2035["FE"][0]=data2035["FE"][0]*(1+structural_effect_services_2035/100)
        data2035["Emission"][0]=data2035["Emission"][0]*(1+structural_effect_services_2035/100)
        
        data2030["FE"][1]=data2030["FE"][1]*(1+structural_effect_goods_2030/100)
        data2030["Emission"][1]=data2030["Emission"][1]*(1+structural_effect_goods_2030/100)
        
        data2035["FE"][1]=data2035["FE"][1]*(1+structural_effect_goods_2035/100)
        data2035["Emission"][1]=data2035["Emission"][1]*(1+structural_effect_goods_2035/100)
        
        data2030["FE"][2]=data2030["FE"][2]*(1+structural_effect_travel_2030/100)
        data2030["Emission"][2]=data2030["Emission"][2]*(1+structural_effect_travel_2030/100)
        
        data2035["FE"][2]=data2035["FE"][2]*(1+structural_effect_travel_2035/100)
        data2035["Emission"][2]=data2035["Emission"][2]*(1+structural_effect_travel_2035/100)
        
        data2030["FE"][3]=data2030["FE"][3]*(1+structural_effect_commuting_2030/100)
        data2030["Emission"][3]=data2030["Emission"][3]*(1+structural_effect_commuting_2030/100)
        
        data2035["FE"][3]=data2035["FE"][2]*(1+structural_effect_commuting_2035/100)
        data2035["Emission"][3]=data2035["Emission"][3]*(1+structural_effect_commuting_2035/100)
        
        data2030["FE"][4]=data2030["FE"][4]*(1+structural_effect_event_2030/100)
        data2030["Emission"][4]=data2030["Emission"][4]*(1+structural_effect_event_2030/100)
        
        data2035["FE"][4]=data2035["FE"][4]*(1+structural_effect_event_2035/100)
        data2035["Emission"][4]=data2035["Emission"][4]*(1+structural_effect_event_2035/100)
        
        services = [databc["Emission"][0],data2030["Emission"][0],data2035["Emission"][0]]
        goods = [databc["Emission"][1],data2030["Emission"][1],data2035["Emission"][1]]
        travel = [databc["Emission"][2],data2030["Emission"][2],data2035["Emission"][2]]
        commuting = [databc["Emission"][3],data2030["Emission"][3],data2035["Emission"][3]]
        event = [databc["Emission"][4],data2030["Emission"][4],data2035["Emission"][4]]
        
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
    elements = ["Services", "Goods", "Travel", "Commuting", "Event"]
    
    coefficient_services = st.number_input("Coefficient pour services :", value=0.0, step=0.1)
    coefficient_goods = st.number_input("Coefficient pour goods :", value=0.0, step=0.1)
    coefficient_travel = st.number_input("Coefficient pour travel :", value=0.0, step=0.1)
    coefficient_commuting = st.number_input("Coefficient pour commuting :", value=0.0, step=0.1)
    coefficient_event = st.number_input("Coefficient pour event :", value=0.0, step=0.1)
    target_idea = st.number_input("Si vous avez déjà une première idée de la cible qui sera visée :", value=0.0, step=1.0)
    
    # Ajouter une cible initiale pour chaque combinaison solution/année
    #st.session_state["Target"][f"{solution_name}"] = 0
    
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
                                             "Coefficient pour event": coefficient_event, "Target": target_idea}])
                    
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
        #st.write("Keys in targets:", st.session_state["Target"].keys())
        
        solutionsrows,solutionscolumns = st.session_state["solutions"].shape
        st.write("Solutions disponibles :",solutionsrows )
        st.dataframe(st.session_state["solutions"])
        # Accéder aux données brutes
        # solutions_df = st.session_state["solutions"]
        # st.write("Les données brutes :", solutions_df)
        # st.write("Test 1", st.session_state["solutions"].iloc[0, 1])
        # st.write("Test 2", solutions_df.iloc[0, 3])
        # st.write("Définissez les cibles pour chaque solution et année :")
        
        for i in range(solutionsrows):
            name = st.session_state["solutions"].iloc[i, 0]
            st.write ("Name:", name)
            
            st.session_state["solutions"].iloc[i, 7]=st.slider(name, min_value=0.0, max_value=100.0, value=0.0, step=1.0)
            
        st.dataframe(st.session_state["solutions"])    
        
        if uploaded_file:
            for j in range(solutionsrows):
                if st.session_state["solutions"].iloc[j, 1] == 2030:
                    for k in range (5):
                        data2030["Quantité"][k] = data2030["Quantité"] [k]+ data2030["Quantité"][k]*st.session_state["solutions"].iloc[j,2+k]*st.session_state["solutions"].iloc[j, 7]/100
                        data2030["Emission"][k] = data2030["Emission"] [k]+ data2030["Emission"][k]*st.session_state["solutions"].iloc[j,2+k]*st.session_state["solutions"].iloc[j, 7]/100
                else : 
                    for l in range (5):
                        data2035["Quantité"][l] = data2035["Quantité"] [l]+ data2035["Quantité"][l]*st.session_state["solutions"].iloc[j,2+l]*st.session_state["solutions"].iloc[j, 7]/100
                        data2035["Emission"][l] = data2035["Emission"] [l]+ data2035["Emission"][l]*st.session_state["solutions"].iloc[j,2+l]*st.session_state["solutions"].iloc[j, 7]/100
            st.write("data2030", data2030.head())
            st.write("data2030", data2035.head())
            
            
            services = [databc["Emission"][0],data2030["Emission"][0],data2035["Emission"][0]]
            goods = [databc["Emission"][1],data2030["Emission"][1],data2035["Emission"][1]]
            travel = [databc["Emission"][2],data2030["Emission"][2],data2035["Emission"][2]]
            commuting = [databc["Emission"][3],data2030["Emission"][3],data2035["Emission"][3]]
            event = [databc["Emission"][4],data2030["Emission"][4],data2035["Emission"][4]]
            
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
            st.warning("Pas de fichiers upload")
        #target_idea = st.number_input(st.session_state["Nom"], value=0.0, step=1.0)
        #st.write("Target")
        # Générer un curseur pour chaque combinaison solution/année
        #for key, target in st.session_state["Target"].items():
            #solution_name, year = key.rsplit("_", 1) = si on veut ajouter l'année au slider, pour plus tard car pour l'instant ça bug 
            #+ jsp s'il vaut mieux définir l'année dans cet onglet ou dans le précédent à déterminer
            #year = int(year)
            #st.session_state["Target"][key] = st.slider(
                #f"Target pour '{solution_name}' :", min_value=0.0, max_value=100.0, value=float(target))

        #st.write("Cibles définies :")
        #st.json(st.session_state["Target"])
        
        # Récupérer une solution spécifique
        #selected_solution = st.selectbox(
            #"Sélectionnez une solution à modifier :",
            #st.session_state["solutions"]["Nom"].unique())
        
        # if selected_solution:
        #     # Filtrer le DataFrame pour la solution sélectionnée
        #     solution_data = st.session_state["solutions"][
        #         st.session_state["solutions"]["Nom"] == selected_solution
        #     ]
        
        #     # Afficher les données actuelles
        #     st.write(f"Données pour la solution '{selected_solution}':")
        #     st.dataframe(solution_data)
        
        #     # Modifier une valeur spécifique (exemple : coefficient)
        #     new_coefficient = st.number_input(
        #         f"Modifier le coefficient pour '{selected_solution}':",
        #         value=float(solution_data["Coefficient"].iloc[0]),  # Première valeur
        #         step=0.1
        #     )
        
        #     # Appliquer la modification au DataFrame dans session_state
        #     st.session_state["solutions"].loc[
        #         st.session_state["solutions"]["Nom"] == selected_solution, "Coefficient"
        #     ] = new_coefficient
        
        # # Afficher les données modifiées
        # st.write("Données mises à jour :")
        # st.dataframe(st.session_state["solutions"])
        
        # # Récupérer les noms des solutions disponibles
        # solution_names = st.session_state["solutions"]["Nom"].unique()
        
        # # Sélectionner une solution
        # selected_solution = st.selectbox("Choisissez une solution :", solution_names)

    else:
        st.warning("Aucune solution enregistrée.")