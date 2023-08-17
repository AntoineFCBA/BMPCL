"""
Created on Tue Jun 13 15:56:11 2023

@author: haratono
"""

import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os
import pandas as pd
import numpy as np
    
############################## WINDOW ##############################
root = tk.Tk()
root.title('BMPCL')
root.geometry('800x350+20+20')
root.resizable(0, 0)

   
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
    
        
    #model
    ep_etalon = TB1.get(1.0, "end-1c") 
    ep_etalon = float(ep_etalon)
    larg_etalon= TB2.get(1.0, "end-1c")  
    larg_etalon = float(larg_etalon)

    #nominal
    ep_nom = TB3.get(1.0, "end-1c")  
    ep_nom = float(ep_nom)
    larg_nom = TB4.get(1.0, "end-1c") 
    larg_nom = float(larg_nom)
    
    #extract every column from dataframe
    lt = df[0]
    d1 = df[1]
    d2 = df[2]
    d3 = df[3]
    d4 = df[4]
    
    #Epaisseur
    epai = ep_etalon - d1 - d4
    # formule pour calculer largeur
    larg = larg_etalon - d2 - d3
    
    fleche = abs(d3)
    tuil = abs(d4)
    
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

    df.insert(5, "epaisseur", epai, True)
    df.insert(6, "largeur", larg, True)
    df.insert(7, "verif", Test2, True)
    df.insert(8,"tuilage",tuil,True)
    df.insert(9,"fleche",fleche,True)
    df.insert(10, "Epaisseur moyenne", m_epai, True)
    df.insert(11, "Largeur moyenne", m_larg, True)

    #df.dropna(thresh=10)
    ddf = df.dropna()
    ddf.reset_index(drop = True)
    
     
    # df["Epaisseur moyenne"].loc[1:len(df)] = None
    # df["Largeur moyenne"].loc[1:len(df)] = None

    ddf.columns = ['t(s)', 'CH5(mm)', 'CH6(mm)', 'CH7(mm)', 'CH8(mm)', 'epaisseur(mm)','largeur(mm)','numero Erpouvette',"tuilage (mm)","fleche(mm)","Epaisseur moyenne (mm)","Largeur moyenne (mm)"]
    
    ddf.to_csv('num_'+filename, sep=';', decimal=',',header=True, index=False, index_label=None)
    print('Terminé')
    print('')
   
############################## LABEL ##############################
L0 = tk.Label(root, text="Chemin du fichier : ").place(x=20, y=20)
L1 = tk.Label(root, text="Epaisseur de l'étalon (mm) : ").place(x=20, y=60)
L2 = tk.Label(root, text="Largeur de l'étalon (mm) : ").place(x=20, y=100)
L3 = tk.Label(root, text="Epaisseur nominale (mm) : ").place(x=20, y=140)
L4 = tk.Label(root, text="Largeur nominale (mm) : ").place(x=20, y=180)

# ================================== choisir ==================================
file_button = tk.Button(root, text='Fichier',
                    bg='red', fg='white', command=fichier)
file_button.place(x=380, y=260)
# ================================== repertoire ==================================
file_button = tk.Button(root, text='Répertoire',
                    bg='green', fg='white', command=rep)
file_button.place(x=180, y=260)

############################## TEXT BOX ##############################
TB0 = tk.Text(root, height=1, width=60)
TB0.place(x=190, y=20)
TB1 = tk.Text(root, height=1, width=30)
TB1.place(x=190, y=60)
TB2= tk.Text(root, height=1, width=30)
TB2.place(x=190, y=100)
TB3 = tk.Text(root, height=1, width=30)
TB3.place(x=190, y=140)
TB4 = tk.Text(root, height=1, width=30)
TB4.place(x=190, y=180)

#insert
TB1.insert('end', 78.25)
TB2.insert('end', 110.49) 
TB3.insert('end', 41)
TB4.insert('end', 107)

    


root.mainloop()
