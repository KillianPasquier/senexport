#!/usr/bin/env python
# coding: utf-8

# # J'importe la librairie pandas pour le traitement de fichier csv

# In[1]:


import pandas as pd
from tkinter import * 
from tkinter import messagebox


# # J'importe le fichier excel sous le nom de variable "df"

# In[2]:


df = pd.read_csv("fortransformation.csv")


# # Je supprime les colonnes inutiles 

# In[3]:


df.drop(["Class", "Method Name", "Comment", "Sample Status", "Element Type", "Mass", "Analysis Condition", "Conc.[1]", "Conc.[2]", "Conc.[3]", "Conc.[4]", "Conc.[5]", "Conc.[6]", "Conc.[7]", "Conc.[8]", "Conc.[9]", "Conc.[10]", "Conc.[11]", "Conc.[12]", "Conc.[13]", "Conc.[14]", "Conc.[15]", "Conc.[16]", "Conc.[17]", "Conc.[18]", "Conc.[19]", "Conc.[20]", "Conc.[SD]", "Conc.[RSD]", "Status", "QAQC1", "QAQC2", "QAQC Status1", "QAQC Status2", "Intensity[1]", "Intensity[2]", "Intensity[3]", "Intensity[4]", "Intensity[5]", "Intensity[6]", "Intensity[7]", "Intensity[8]", "Intensity[9]", "Intensity[10]", "Intensity[11]", "Intensity[12]", "Intensity[13]", "Intensity[14]", "Intensity[15]", "Intensity[16]", "Intensity[17]", "Intensity[18]", "Intensity[19]", "Intensity[20]", "Intensity[RSD]", "Intensity[Ave.]", "Intensity[SD]"], axis = 1, inplace=True)


# # Je renomme les colonnes "Sample Name" et "Date/Time" en "TECNumEchantillon" et "TANDateAnalyse"

# In[4]:


df.rename(columns={"Sample Name":"TECNUMEchantillon", "Date/Time":"TANDateAnalyse"}, inplace=True )


# # J'ajoute la colonne "TANModeOperatoire et lui donne la valeur "P705.317" pour toutes les lignes

# In[5]:


df["TANModeOperatoire"]="P705.317"


# # J'ajoute une colonne "TANResultatLD" et lui donne pas de valeur, puisque c'est une colonne vide dans l'export ICP-MS

# In[6]:


df["TANResultatLD"]=""


# # Pour formater comme il faut les unités, je vais créer un dictionnaire "unites_lims" qui met en relation les unités du fichier brut avec les unités utilisées dans le LIMS, puis créer une nouvelle colonne "TANResultatUnite" qui contiendra les unités LIMS

# In[7]:


unites_lims={"mg/L":"mg/l", "ug/L":"\N{MICRO SIGN}""g/l"}


# In[8]:


df["TANResultatUnite"]=df["Unit"].map(unites_lims)


# # Pour charger les ID des paramètres en fonction de la colonne "Element", je crée un dictionnaire "analytes_idlims" qui mets en relation la colonne "Element" et les ID du LIMS, puis crée une colonne "TPAParametre_ID" qui contiendra les ID LIMS

# In[9]:


analytes_idlims={"Ag":"Par0040", "Al":"Par0031", "As":"Par0041", "Ba":"Par0050", "Ca":"Par0074", "Cd":"Par0072", "Co":"Par0097", "Cr":"Par0093", "Cu":"Par0100", "Fe":"Par0146", "K":"Par0245", "Mg":"Par0179", "Mn":"Par0183", "Mo":"Par0203", "Na":"Par0271", "Ni":"Par0208", "Pb":"Par0244", "Se":"Par0267", "Sn":"Par0136", "Sr":"Par0275", "Ti":"Par0298", "U":"Par0310", "V":"Par0311", "Zn":"Par0314"}


# In[10]:


df["TPAParametre_ID"]=df["Element"].map(analytes_idlims)


# # Pour charger les LQ en fonction de la colonne "Element", je crée un dictionnaire "analytes_lqlims" qui mets en relation la colonne "Element" et les LQ du LIMS, puis crée une colonne "TANResultatLQ" qui contiendra les LQ LIMS

# In[11]:


analytes_lqlims={"Ag":"0.050", "Al":"10.0", "As":"0.500", "Ba":"0.500", "Ca":"0.100", "Cd":"0.050", "Co":"0.100", "Cr":"0.500", "Cu":"1.00", "Fe":"5.00", "K":"1.00", "Mg":"0.100", "Mn":"0.500", "Mo":"0.500", "Na":"1.00", "Ni":"0.500", "Pb":"0.500", "Se":"5.00", "Sn":"0.500", "Sr":"1.00", "Ti":"1.00", "U":"0.100", "V":"0.100", "Zn":"5.00"}


# In[12]:


df["TANResultatLQ"]=df["Element"].map(analytes_lqlims)


# # Pour les résultats, je vais créer une colonne de fonction "TANResultat" qui affichera "<" et la valeur de la LQ si c'est le cas

# In[13]:


df["pluspetitque"]= "<"


# In[14]:


df["Conc.[Ave.]"]=df["Conc.[Ave.]"].astype(str)
df["TANResultatLQ"]=df["TANResultatLQ"].astype(str)
df["pluspetitque"]=df["pluspetitque"].astype(str)


# In[15]:


df.loc[df["Conc.[Ave.]"]<df["TANResultatLQ"], "TANResultat"] = df["pluspetitque"]+df["TANResultatLQ"]
df.loc[df["Conc.[Ave.]"]>df["TANResultatLQ"], "TANResultat"] = df["Conc.[Ave.]"]


# # Je remets de l'ordre dans mes colonnes en supprimant les colonnes dont je n'ai plus besoin pour l'export et en les réordonnant dans le bon ordre

# In[16]:


df.drop(["Element", "Unit", "Conc.[Ave.]", "pluspetitque"], axis=1, inplace=True)
df["TANDateAnalyse"]=df["TANDateAnalyse"].astype(str)


# In[17]:


df=df.reindex(columns=["TECNUMEchantillon", "TPAParametre_ID", "TANResultat", "TANResultatUnite", "TANResultatLD", "TANResultatLQ", "TANModeOperatoire", "TANDateAnalyse"])


# In[18]:


df


# # Je termine en enregistrant le dataframe ("df") sous un fichier csv

# In[19]:


df.to_csv("finalfile.csv", index=False)
messagebox.showinfo("Information", "Opération terminée !")


# In[ ]:




