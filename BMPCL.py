# -*- coding: utf-8 -*-


#from datetime import *
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from statistics import pstdev
import openpyxl

############################## WINDOW ##############################
root = Toplevel() 
root.title('BMPCL')
root.geometry('800x227+20+20')
root.resizable(0, 0)

############################## FUNCTION ##############################
#================================== directory ==================================
def rep(): #directory
    print('----------------')
    full_path = filedialog.askdirectory() #path of the folder
    os.chdir(full_path)
    print("Répertoire actuel : " + full_path)
    print('')

def fichier():
    print('----------------')
    
    full_path = filedialog.askopenfilename() #path of the file
    print("Chemin : " + full_path )
    filename = os.path.basename(full_path)
    TB0.insert('end', full_path)
    
    df = pd.read_csv(full_path, delimiter="\t", header=None, engine='python') #read output file
    
    de = TB1.get(1.0, "end-1c")
    de = float(de)
    dl = TB2.get(1.0, "end-1c") 
    dl = float(dl)

    lt = df[0]
    d1 = df[1]
    d2 = df[2]
    d3 = df[3]
    d4 = df[4]
    
    epai = de-(d1+d2)
    larg = dl-(d4+d3)
    
    epai_m = sum(epai)
    epai_m = epai_m/len(epai)
    
    larg_m = sum(larg)
    larg_m=larg_m/len(larg)
   
    
    sigm1 = pstdev(epai)
    sigm2 = pstdev(larg)
    
    flèche = d2
    
    tuilage = d4
    

    df.insert(5,"epaisseur",epai,True)
    df.insert(6,"largeur",larg,True)
   
    df.insert(7,"flèche",flèche,True)
    df.insert(8,"tuilage",tuilage,True)
# =============================================================================
#     
    #df["epaisseur moyenne"].loc[1:len(df)]=None
    #df["largeur moyenne"].loc[1:len(df)]=Nones
# =============================================================================

    
    df.columns = ['t(s)','d1(mm)','d2(mm)','d3(mm)','d4(mm)','epaisseur(mm)','largeur(mm)','flèche','tuilage',]
    df.to_csv('num_'+filename,sep=';',decimal=',',header=True,index=False,index_label=None)
    print('Terminé')
    df.to_csv  
    
     
############################## import-logo ##############################

photo = PhotoImage(file="Capture.png")
canvas = Canvas(root, width = 800, height = 227)
canvas.create_image(632,150, anchor=SW, image=photo)


############################## LABEL ##############################
L0 = tk.Label(root,text = "Chemin du fichier : ").place(x = 20,y = 20)
L1 = tk.Label(root,text = "Largeur de l'étalon (mm) : ").place(x = 20,y = 60)
L2 = tk.Label(root,text = "Epaisseur de l'étalon (mm) : ").place(x = 20,y = 100)

############################## BUTTON ##############################
#================================== choisir ==================================
file_button = tk.Button(root, text='Choisir fichier', bg='brown',fg='white',command=fichier)
file_button.place(x=80, y=200)
#================================== repertoire ==================================
file_button = tk.Button(root, text='Répertoire', bg='green',fg='white',command=rep)
file_button.place(x=5, y=200)

def ouvrir():
    # Ouvrir une boîte de dialogue pour sélectionner un fichier
    file_path = filedialog.askopenfilename()
    if file_path != '':
        os.startfile(file_path)  # Ouvrir le fichier avec le programme par défaut
        
file_buton = tk.Button(root, text = 'Ouvrir', bg = 'blue',fg ="white",command=ouvrir)
file_buton.place(x=180, y=200)        

############################## TEXT BOX ##############################
TB0 = tk.Text(root,height=1,width=50)
TB0.place(x=190, y=20)
TB1 = tk.Text(root,height=1,width=30)
TB1.place(x=190, y=60)
TB2 = tk.Text(root,height=1,width=30)
TB2.place(x=190, y=100)

TB1.insert('end', 200)
TB2.insert('end', 200)

canvas.pack()
root.mainloop()