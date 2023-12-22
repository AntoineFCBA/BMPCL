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
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"<
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"   
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
    d6 = df[6]
    
    #thickness
    epai = ep_etalon - d1 - d3
    epai = [round(val, 2) for val in epai]
    # formule pour calculer largeur
    larg = larg_etalon - d2 - d5
    larg = [round(val, 2) for val in larg]
    
    fleche = abs(d2)
    tuil = abs(d3)
    fl_face = abs(d6)
    gauch = abs(d4)
    new_column = []

    #verification
    i=0
    for n in epai:
        if ((ep_nom-5) < epai[i] < (ep_nom + 5)) and ((larg_nom-5) < larg[i] < (larg_nom + 5)):
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
                d5[i]   = np.nan
                d6[i]   = np.nan
                lt[i]   = np.nan
                fleche[i] = lt[i]
                tuil[i] = d4[i]
        i=i+1
        
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
        
    df.insert(7, "epaisseur", epai, True)
    df.insert(8, "largeur", larg, True)
    df.insert(9, "verif", Test2, True)
    df.insert(10,"tuilage",tuil,True)
    df.insert(11,"fleche",fleche,True)
    df.insert(12,"gauchissement",gauch,True)
    df.insert(13, "Fleche de face",fl_face,True)
    
    df['gauchissement'] = np.where(df['gauchissement'] < 25, df['gauchissement'], np.nan)
    #condition = (df['gauchissement'] <= df[['tuilage', 'Fleche de face']].max(axis=1))
   # df.loc[condition, ['tuilage', 'Fleche de face']] = np.nan
    
    df["Fleche de face"] = df.groupby('verif')["Fleche de face"].transform(lambda x: x.max() - x.min())
    df["tuilage"] = df.groupby('verif')['tuilage'].transform('max')
    df["fleche"] = df.groupby('verif')['fleche'].transform('max')
    df["gauchissement"] = df.groupby('verif')['gauchissement'].transform('max')

    ddf = df.dropna()
    ddf.reset_index(drop = True)
#     moyennes_df = moyennes_df.iloc[:, :-2]
    ddf.to_csv('num_'+filename, sep=';', decimal=',',header=True, index=False, index_label=None)
    moyennes_df = df.groupby('verif').mean()
    moyennes_df.columns = ['t(s)', 'CH5(mm)', 'CH7(mm)', 'CH8(mm)', 'CH9(mm)','CH10(mm)','CH11(mm)','epaisseur(mm)','largeur(mm)',"tuilage (mm)","fleche(mm)","gauchissement(mm)","Fleche de face"]
    moyennes_df.to_csv('moyennes_'+filename, sep=';', decimal=',', header=True, index=True)
    print('Terminé')
    print('')
    
def open_last_file():
    original_filename = TB0.get("1.0", "end-1c")
    if original_filename:
        filename, extension = os.path.splitext(os.path.basename(original_filename))
        processed_filename = f'num_{filename}{extension}'
        os.startfile(processed_filename)
        
        
def fusionner_fichiers_selectionnes(fichiers, fichier_sortie):
    # Ouvrir le fichier de sortie en mode écriture
    with open(fichier_sortie, 'w') as fusion_file:
        # Écrire l'en-tête dans le fichier de sortie
        header = "verif\tt(s)\tCH5(mm)\tCH7(mm)\tCH8(mm)\tCH9(mm)\tCH10(mm)\tCH11(mm)\tepaisseur(mm)\tlargeur(mm)\ttuilage (mm)\tfleche(mm)\tgauchissement(mm)\tFleche de face\n"
        fusion_file.write(header)

        # Parcourir chaque fichier sélectionné
        for fichier in fichiers:
            # Vérifier si le fichier n'est pas vide
            if os.path.getsize(fichier) > 0:
                # Lire la deuxième ligne du fichier
                deuxieme_ligne = open(fichier, 'r').readlines()[1].strip()

                # Écrire la deuxième ligne dans le fichier de sortie
                fusion_file.write(deuxieme_ligne + '\n')
            else:
                print(f"Attention: Le fichier {fichier} est vide.")

    print(f"Fusion terminée. Les lignes deux de chaque fichier ont été ajoutées à {fichier_sortie}")

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
