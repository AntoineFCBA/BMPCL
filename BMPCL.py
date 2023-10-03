# -*- coding: utf-8 -*-

import customtkinter
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os
import pandas as pd
import numpy as np

    
############################## WINDOW ##############################
root = customtkinter.CTk()
root.title('BMPCL')
root.geometry('800x350+20+20')
root.resizable(0, 0)

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"<
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"   
############################## FUNCTION ##############################

#================================== directory ==================================
def rep():
    print('----------------')
    full_path = filedialog.askdirectory()
    
    #declare directory
    os.chdir(full_path)
    print("Répertoire actuel : " + full_path)
    print('')

def fichier():
    print('----------------')
    full_path = filedialog.askopenfilename()
    print("Chemin : " + full_path)
    #extract directory of the raw file and insert in the first text box
    filename = os.path.basename(full_path)
    TB0.delete("1.0","end")
    TB0.insert('end', full_path)

    #read raw csv file
    df = pd.read_csv(full_path, delimiter=",", header=None)
    
        
    #Demande à l'utilisateur de rentrer dim etalon
    ep_etalon = TB1.get(1.0, "end-1c") 
    ep_etalon = float(ep_etalon)
    larg_etalon= TB2.get(1.0, "end-1c")  
    larg_etalon = float(larg_etalon)

    #nominal
    ep_nom = TB3.get(1.0, "end-1c")  
    ep_nom = float(ep_nom)
    larg_nom = TB4.get(1.0, "end-1c") 
    larg_nom = float(larg_nom)
    
    #extraction des donnée brut dans le dataframe
    lt = df[0]
    d1 = df[1]
    d2 = df[2]
    d3 = df[3]
    d4 = df[4]
    d5 = df[5]

    #thickness
    epai = ep_etalon - d1 - d3
    epai = [round(val, 2) for val in epai]
    # formule pour calculer largeur
    larg = larg_etalon - d2 - d5
    larg = [round(val, 2) for val in larg]
    
    fleche = abs(d1)
    tuil = abs(d3)
    gauch = abs(d4)
    new_column = []

    #verification
    i=0
    for n in epai:
        if ((ep_nom-15) < epai[i] < (ep_nom + 15)) and ((larg_nom-15) < larg[i] < (larg_nom + 15)):
                new_column.insert(i,100)
                epai[i] = epai[i]
                larg[i] = larg[i]
        else:
                new_column.insert(i,0)
                epai[i] = np.nan
                larg[i] = np.nan
                d1[i]   = np.nan
                d2[i]   = np.nan
                d3[i]   = np.nan
                d4[i]   = np.nan
                lt[i]   = np.nan
                fleche[i] = lt[i]
                tuil[i] = d4[i]
        i=i+1
        
    #read plank file
    df2 = pd.read_csv("planche.csv", delimiter=";", header=None, skiprows=1)
    planche = df2[0]
    
    i1=0
    i2=1
    i3=2

    cc = 0

    Number=1
    Test2=[]


    if new_column[0] == 0 :
        Test2.insert(cc, 0)
    else:
        Test2.insert(cc, planche[Number-1])
        
    cc=cc+1


    for n in range(len(new_column)-2):
        if new_column[i1] == 0 and new_column[i2] == 0 and new_column[i3] == 0:
            Test2.insert(cc, 0)
        elif new_column[i1] == 100 and new_column[i2] == 100 and new_column[i3] == 100:
            Test2.insert(cc, planche[Number-1])
        elif new_column[i1] == 0 and new_column[i2] == 100 and new_column[i3] == 100:
            Test2.insert(cc, planche[Number-1])
        elif new_column[i1] == 100 and new_column[i2] == 100 and new_column[i3] == 0:
            Test2.insert(cc, planche[Number-1])
        elif new_column[i1] == 0 and new_column[i2] == 0 and new_column[i3] == 100:
            Test2.insert(cc, 0)
            Number = Number + 1
        elif new_column[i1] == 100 and new_column[i2] == 0 and new_column[i3] == 100:
            Test2.insert(cc, 0)
            Number = Number + 1
        else:
            Test2.insert(cc, 0)
        cc=cc+1
        i1=i1+1
        i2=i2+1
        i3=i3+1

    if new_column[-1] == 0 and new_column[-2]==0:
        Test2.insert(cc, 0)
    elif new_column[-1] == 100 and new_column[-2]==0:
        Test2.insert(cc, 0)
    elif new_column[-1] == 0 and new_column[-2]==100:
        Number=Number+1
        Test2.insert(cc, planche[Number-1])
    else:
        Test2.insert(cc, planche[Number-1])
        
        
    i = 0  
    for n in Test2 : 
        if n == 0 :
            Test2[i] = np.nan
            
            
        i = i+1 
    
    
    m_epai = np.nanmean(epai) if len(epai)>0 else np.nan
    m_larg = np.nanmean(larg) if len(larg)>0 else np.nan
            
    # m_epai = sum(epai)/len(epai)
    # m_larg = sum(larg)/len(larg)

    df.insert(6, "epaisseur", epai, True)
    df.insert(7, "largeur", larg, True)
    df.insert(8, "verif", Test2, True)
    df.insert(9,"tuilage",tuil,True)
    df.insert(10,"fleche",fleche,True)
    df.insert(11,"gauchissement",gauch,True)
    df.insert(12, "Epaisseur moyenne", m_epai, True)
    df.insert(13, "Largeur moyenne", m_larg, True)

    #df.dropna(thresh=10)
    ddf = df.dropna()
    ddf.reset_index(drop = True)
    
    # df["Epaisseur moyenne"].loc[1:len(df)] = Noned
    # df["Largeur moyenne"].loc[1:len(df)] = None

    ddf.columns = ['t(s)', 'CH5(mm)', 'CH6(mm)', 'CH7(mm)', 'CH8(mm)','CH9(mm)','epaisseur(mm)','largeur(mm)','numero Eprouvette',"tuilage (mm)","fleche(mm)","gauchissement(mm)","Epaisseur moyenne (mm)","Largeur moyenne (mm)"]
    ddf.to_csv('num_'+filename, sep=';', decimal=',',header=True, index=False, index_label=None)
    print('Terminé')
    print('')
    
def open_last_file():
    original_filename = TB0.get("1.0", "end-1c")
    if original_filename:
        filename, extension = os.path.splitext(os.path.basename(original_filename))
        processed_filename = f'num_{filename}{extension}'
        os.startfile(processed_filename)
        
def fusionner_fichiers_selectionnes(fichiers, fichier_sortie):
    # Créer un DataFrame vide pour stocker les données fusionnées
    fusion_df = pd.DataFrame()

    # Compteur pour le numéro de fichier
    num_fichier = 1

    # En-têtes (initialisés à None)
    en_tetes = []

    # Parcourir chaque fichier sélectionné
    for fichier in fichiers:
        # Lire uniquement la dernière ligne du fichier
        with open(fichier, "r") as file:
            last_line = file.readlines()[-1].strip().split(";")

        # Créer un DataFrame à partir de la dernière ligne du fichier
        df = pd.DataFrame([last_line])

        # Ajouter une colonne "Id" avec le numéro de fichier
        df.insert(0, "Id", num_fichier)

        # Arrondir les valeurs à deux décimales
        df = df.round(2)

        # Ajouter les données du fichier à fusion_df
        fusion_df = pd.concat([fusion_df, df], axis=0, ignore_index=True)

        # Incrémenter le compteur de fichier
        num_fichier += 1

        # Lire les en-têtes du fichier une seule fois (lors du premier fichier)
        if not en_tetes:
            with open(fichier, "r") as file:
                en_tetes = file.readline().strip().split(";")

    # Renommer la colonne "temps" en "Id"
    fusion_df = fusion_df.rename(columns={"temps": "Id"})

    # Ajouter les en-têtes d'origine au début du DataFrame fusionné
    fusion_df = pd.concat([pd.DataFrame([en_tetes]), fusion_df], ignore_index=True)

    # Écrire le DataFrame fusionné dans un fichier de sortie
    fusion_df.to_csv(fichier_sortie, sep=';', decimal=',', header=False, index=False)




def selectionner_et_fusionner():
    fichiers = filedialog.askopenfilenames(filetypes=[("CSV Files", "*.csv")])
    if fichiers:
        fichier_sortie = "fusion.csv"
        fusionner_fichiers_selectionnes(fichiers, fichier_sortie)
          
############################## LABEL ##############################
L0 =customtkinter.CTkLabel(root, text="Chemin du fichier : ").place(x=20, y=20)
L1 = customtkinter.CTkLabel(root, text="Epaisseur de l'étalon (mm) : ").place(x=20, y=60)
L2 = customtkinter.CTkLabel(root, text="Largeur de l'étalon (mm) : ").place(x=20, y=100)
L3 = customtkinter.CTkLabel(root, text="Epaisseur nominale (mm) : ").place(x=20, y=140)
L4 = customtkinter.CTkLabel(root, text="Largeur nominale (mm) : ").place(x=20, y=180)

# ================================== choisir ==================================
file_button = customtkinter.CTkButton(root, text='Fichier', command=fichier)
file_button.place(x=260, y=240)
# ================================== repertoire ==================================
file_button =  customtkinter.CTkButton(root, text='Répertoire',command=rep)
file_button.place(x=60, y=240)
# ================================== full screen ==================================
fullscreen_button = customtkinter.CTkButton(root, text='Ouvrir', command=open_last_file,bg_color='red',fg_color='red')
fullscreen_button.place(x=260, y=280)
# ================================== full screen ==================================
fusion_button = customtkinter.CTkButton(root, text='Sélectionner et Fusionner', command=selectionner_et_fusionner)
fusion_button.place(x=460, y=240)
############################## TEXT BOX ##############################
TB0 = customtkinter.CTkTextbox(root, height=1, width=600)
TB0.place(x=190, y=20)
TB1 = customtkinter.CTkTextbox(root, height=1, width=300)
TB1.place(x=190, y=60)
TB2= customtkinter.CTkTextbox(root, height=1, width=300)
TB2.place(x=190, y=100)
TB3 = customtkinter.CTkTextbox(root, height=1, width=300)
TB3.place(x=190, y=140)
TB4 = customtkinter.CTkTextbox(root, height=1, width=300)
TB4.place(x=190, y=180)

#insert
TB1.insert('end', 49.65)
TB2.insert('end', 150) 
TB3.insert('end', 53)
TB4.insert('end', 153)


root.mainloop()

