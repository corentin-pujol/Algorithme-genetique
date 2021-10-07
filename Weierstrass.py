# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 17:44:39 2021

@author: coco8
"""
import random
import math as m
import csv
#import time

cr = csv.reader(open("temperature_sample.csv","r")) #Lecture du fichier csv

my_sample = {} #Dictionnaire afin de récupérer les températures en fonction de l'instant i

i = 0
for row in cr: #boucle sur les lignes du fichier
    if(i!=0):
        liste = row[0].split(';') #séparation des i et des t(i)
        my_sample[float(liste[0])] = float(liste[1]) #ajout des éléments dans le dictionnaire
    else:
        i = 1
        
#print(my_sample)
    
class Combinaison:
    #une classe pour gérer les combinaisons a, b, c
    combi_count=0 #variable de classe
    def __init__(self, a, b, c): #Constructeur
        self.a=a #variables d'instances
        self.b=b
        self.c=c
        Combinaison.combi_count+=1
    def __str__(self):
        return f"({self.a}, {self.b}, {self.c})"


def Weierstrass_function(a, b, c, i): #Calcul de la température t(i) par la formule de Weierstrass
    t = 0
    for n in range(c+1):
        t += a**n * m.cos(b**n * m.pi * i)
    return t
#print(Weierstrass_function(0.18284959268435685, 15, 10, 1.933)) 
    
def Moyenne_des_ecarts(a, b, c): #Moyenne des écarts des températures avec l'échantillon analysé sur la planète plus le résultat est proche de zéro plus la combinaison a, b, c est proche de la solution
    m = 0
    for key, value in my_sample.items():
         m += abs(value - Weierstrass_function(a, b, c, key))
    return m/len(my_sample)

#print(Moyenne_des_ecarts(0.2, 15, 8)) 
    
def Population_initiale(): #création de la population initiale de 100 combinaisons possibles
    my_population = {}
    for i in range(100):
        a=round(random.random(),2)
        b=random.randint(1,20)
        c=random.randint(1,20)
        my_population[Combinaison(a, b, c)] = Moyenne_des_ecarts(a, b, c)
    return my_population

#my_population = Population_initiale()

def Croisement(I1, I2):
    new_a = round(float(random.choice([str(I1.a),str(I2.a)])),9)
    new_b = int(random.choice([str(I1.b),str(I2.b)]))
    if(new_a == I1.a and new_b == I1.b):
        new_c = I2.c
    elif(new_a == I2.a and new_b == I2.b):
        new_c = I1.c
    else:
        new_c = int(random.choice([str(I1.c),str(I2.c)]))
    new_I = Combinaison(new_a, new_b, new_c)
    return new_I
    
    
def Mutation(my_population):
    cpt = 0
    new_population = {}
    liste_cle = []
    for k, v in sorted(my_population.items(), key=lambda x: x[1]):
        if(cpt<20): #on garde 20% des meilleurs éléments (les meilleurs éléments sont ceux qui ont la moyenne des ecarts de temperatures la plus proche de 0)
            new_population[k] = v
            liste_cle.append(k)
            cpt += 1
    
    #Nous allons maintenant effectuer des croisements entre les meilleurs éléments afin de recréer une nouvelle population de 100 individus
    while(len(new_population)<100):
        r1 = random.randint(0,19)
        r2 = random.randint(0,19)
        while(r1==r2):
            r2 = random.randint(0,19)
        I1 = liste_cle[r1]
        I2 = liste_cle[r2]
        I_enfant = Croisement(I1, I2)
        new_population[I_enfant] = Moyenne_des_ecarts(I_enfant.a, I_enfant.b, I_enfant.c)
    return new_population

def Mutation2(my_population):
    cpt = 0
    new_population = {}
    liste_cle = []
    for k, v in sorted(my_population.items(), key=lambda x: x[1]):
        if(cpt<20): #on garde 20% des meilleurs éléments (les meilleurs éléments sont ceux qui ont la moyenne des ecarts de temperatures la plus proche de 0)
            new_population[k] = v
            liste_cle.append(k)
            cpt += 1
    
    #Nous allons maintenant effectuer des croisements entre les meilleurs éléments afin de recréer une nouvelle population de 100 individus
    while(len(new_population)<100):
        I_enfant = Combinaison(round(random.random(),2), random.randint(1,20), random.randint(1,20))
        new_population[I_enfant] = Moyenne_des_ecarts(I_enfant.a, I_enfant.b, I_enfant.c)
    return new_population

def Mutation3(my_population):
    cpt = 0
    new_population = {}
    liste_cle = []
    liste_cle_enfant_mutation = []
    for k, v in sorted(my_population.items(), key=lambda x: x[1]):
        if(cpt<20): #on garde 20% des meilleurs éléments (les meilleurs éléments sont ceux qui ont la moyenne des ecarts de temperatures la plus proche de 0)
            new_population[k] = v
            liste_cle.append(k)
            cpt += 1
    
    #Nous allons maintenant effectuer des croisements entre les meilleurs éléments afin de recréer une nouvelle population de 100 individus
    while(len(new_population)<100):
        r1 = random.randint(0,19)
        r2 = random.randint(0,19)
        I1 = liste_cle[r1]
        I2 = liste_cle[r2]
        I_enfant = Croisement(I1, I2)
        liste_cle_enfant_mutation.append(I_enfant)
        new_population[I_enfant] = Moyenne_des_ecarts(I_enfant.a, I_enfant.b, I_enfant.c)
    cpt=0
    i = 79
    while(cpt<10):
        n1 = random.randint(0,i) #on choisit l'index d'un enfant parmi les 80 nouveaux qui auront un paramètre ayant muté
        cpt+=1
        i = i - 1
        n2 = random.randint(0,2) #On prend au hasard un parametre à muter aleatoirement sur une dizaine d'enfant 
        del new_population[liste_cle_enfant_mutation[n1]]
        if(n2==0):
            I_enfant = Combinaison(round(random.random(),2), liste_cle_enfant_mutation[n1].b, liste_cle_enfant_mutation[n1].c )
            new_population[I_enfant] = Moyenne_des_ecarts(I_enfant.a, I_enfant.b, I_enfant.c)
        elif(n2==1):
            I_enfant = Combinaison(liste_cle_enfant_mutation[n1].a, random.randint(1,20), liste_cle_enfant_mutation[n1].c )
            new_population[I_enfant] = Moyenne_des_ecarts(I_enfant.a, I_enfant.b, I_enfant.c)
        else:
            I_enfant = Combinaison(liste_cle_enfant_mutation[n1].a, liste_cle_enfant_mutation[n1].b, random.randint(1,20))
            new_population[I_enfant] = Moyenne_des_ecarts(I_enfant.a, I_enfant.b, I_enfant.c)
        liste_cle_enfant_mutation.remove(liste_cle_enfant_mutation[n1])
    return new_population
    
def Algorithme_Genetique():
    my_population = Population_initiale()
    #n = int(input("Veuillez rentrer un nombre d'itération (au moins superieur à 10) : "))
    for i in range(200):
        my_population = Mutation3(my_population)
        cle = min(my_population, key=my_population.get)
        print("Combinaison :", cle)
    for k, v in sorted(my_population.items(), key=lambda x: x[1]):
        return k

Combi_gagnante = Algorithme_Genetique()
print(str(Combi_gagnante))
print(Moyenne_des_ecarts(Combi_gagnante.a, Combi_gagnante.b, Combi_gagnante.c)) 
"""
somme_temps=0
for i in range(100):
    start_time = time.time()
    Algorithme_Genetique()
    somme_temps = somme_temps + (time.time() - start_time)
moyenne_temps = somme_temps/100
print("\n\nMoyenne temps d'exécution :", moyenne_temps, "secondes")
"""       
        