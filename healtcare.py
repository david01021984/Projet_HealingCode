import time
import pygame
import threading
from tabulate import tabulate


class Lieu():
# Lieu: Représente un lieu avec un nom et une liste de personnes présentes
    def __init__(self, nom, personnes = None):
        self.nom = nom
        self.personnes = [] if personnes is None else personnes


class Personnage():
# Personnage: Représente un personnage avec un nom, une quantité d'argent, un lieu actuel, 
# et des objets dans ses mains droite et gauche

    def __init__(self, nom, argent:float, lieu , poche=[]):
        self.nom = nom
        self.lieu = lieu
        self.argent = argent
        self.poche = poche
    
    def seDeplacer(self, depart,destination):
        if self.nom in depart.personnes:
            depart.personnes.remove(self.nom)
        self.lieu = destination.nom
        if self.nom not in destination.personnes:
            destination.personnes.append(self.nom)
        print(f"{self.nom} se déplace...")
        time.sleep(1.5)
        print(f"{self.nom} est arrivé à {destination.nom}")
    

class Docteur(Personnage):
    def __init__(self, nom, argent, lieu, poche, specialisation):
        super().__init__(nom, argent, lieu, poche)
        self.specialisation = specialisation

    def diagnostiquer(self, patient, diagnostique):
        patient.maladie = diagnostique.maladie
        patient.etat_de_sante = "Diagnostiqué"
        print(f"{patient.nom}, je vous annonce que vous avez un {diagnostique.maladie}")
        

    def se_faire_payer(self,patient,montant_consultation=50):
        if patient.argent >= montant_consultation:
            self.argent += montant_consultation
            patient.argent -= montant_consultation
            print(f"{patient.nom} a payé sa visite che le docteur {self.nom}")
        else :
            print("Je ne peux pas vous soigner mais il existe des plannings familliaux")
        
        
    def prescrire(self,patient,traitement):
        patient.poche = traitement
        print(f"Allez à la pharmacie chercher {traitement.nom}")

    
    def inviter_a_entrer(self,patient,cabinet):
        patient.lieu = self.lieu
        cabinet.personnes.append(patient.nom)
        print(f"Le docteur {self.specialisation} : {self.nom} a invité {patient.nom} à entrer")

    def inviter_a_quitter(self,patient,cabinet):
        patient.lieu = " "
        cabinet.personnes.remove(patient.nom)
        print(f"Bon rétablissement {patient.nom}!")

class Patient(Personnage):
    Patients = []
    def __init__(self, nom, argent, lieu, poche, maladie = "unknown", etat_de_sante = "Malade"):
        super().__init__(nom, argent, lieu, poche)
        self.maladie = maladie
        self.etat_de_sante = etat_de_sante
        Patient.Patients.append(self)
    
    def payerMedoc(self, medoc,pharmacie):
        self.argent -= medoc.prix
        pharmacie.caisse += medoc.prix
        self.etat_de_sante = "En traitement"
        print(f"{self.nom} paie {medoc.nom} au prix de {medoc.prix} à {pharmacie.nom}")

    

class Traitement():
    Traitements = []
    def __init__(self, nom, prix):
        self.nom = nom
        self.prix = prix 
        Traitement.Traitements.append(self)

    def __str__(self): 
        return self.nom
    
    def __repr__(self):
        return self.nom
    

class Diagnostique():
    Diagnostiques = []
    def __init__(self,maladie,traitement):
        self.maladie = maladie
        self.traitement = traitement
        Diagnostique.Diagnostiques.append(self)

    def __str__(self): 
            return self.nom
    
    def __repr__(self):
            return self.nom

class Lieu():
# Lieu: Représente un lieu avec un nom et une liste de personnes présentes
    def __init__(self, nom, personnes = None):
        self.nom = nom
        self.personnes = [] if personnes is None else personnes

class Pharmacie(Lieu):
    def __init__(self, nom, personnes=None,traitements_en_stock=[],caisse=500):
        super().__init__(nom, personnes)
        self.traitements_en_stock = traitements_en_stock
        self.caisse = caisse

class Chat():
    def __init__(self,nom,race):
        self.nom = nom
        self.race = race
        pygame.mixer.init()  # Initialize the mixer
        pygame.mixer.music.load("meow.wav") 


    def miaule(self):
    #while not stop_flag.is_set():
        pygame.mixer.music.play(loops=20)
        time.sleep(4)
        #pygame.mixer.music.stop()


#init    
chat_du_doc = Chat("Xerxès","Sphynx")
#chat_du_doc.miaule()

antiviraux = Traitement("Antiviraux", 8.7)
sedocar = Traitement("Sedocar",12)
insuline = Traitement("Insuline",6)
antihistaminique = Traitement("Antihistaminiques", 12)
antibiotique = Traitement("Antibiotique", 9.8)
nouveau_traitement_covid = Traitement("COVID",15)

grippe = Diagnostique("Grippe",antiviraux)
hypertension = Diagnostique("Hypertension",sedocar)
diabete = Diagnostique("Diabète",insuline)
rhume_foin = Diagnostique("Rhume des foins",antihistaminique)
infection_urinaire = Diagnostique("Infection urinaire",antibiotique)
covid = Diagnostique("Covid SARS",nouveau_traitement_covid)

cabinet_Dr_X = Lieu("Cabinet du Docteur X", personnes=["Dr X","Xerxès le Sphynx"])
salle_attente_Dr_X = Lieu("Salle d'attente")

chez_Marcus = Lieu("Maison de Marcus",["Marcus"])
chez_Optimus = Lieu("Maison d'Optimus",["Optimus"])
chez_sangoku = Lieu("Temple de Goku",["SanGoku"])
chez_vador = Lieu("Vaisseau de Darth Vador",["Darth Vador"])
chez_romulus = Lieu("Chez Romulus",["Romulus"])
chez_remus = Lieu("Chez Remus",["Remus"])

doc = Docteur("Dr X",1000,cabinet_Dr_X,poche=[],specialisation="Généraliste")

marcus = Patient("Marcus",100,chez_Marcus,poche=[])
optimus = Patient("Optimus",200,chez_Optimus,poche=[])
sangoku = Patient("Sangoku",80,chez_sangoku,poche=[])
darthvader = Patient("Vador",140, chez_vador,poche=[])
romulus = Patient("Romulus",240, chez_romulus,poche=[])
remus = Patient("Remus",60, chez_remus,poche=[])

pharma_chez_baba = Pharmacie("Pharmacie chez Baba",["Le Pharmacien (Baba)"],[antiviraux,sedocar,insuline,antihistaminique,antibiotique,nouveau_traitement_covid])


def displaySalleAttente():
    dataSA = []

    for patient in Patient.Patients:
        if patient.lieu == salle_attente_Dr_X.nom:
            line = [f"{patient.nom}",f"{patient.maladie}",f"{patient.argent}",f"{patient.poche}",f"{patient.etat_de_sante}"]
            dataSA.append(line)

    tableSA = tabulate(dataSA, headers=["Nom","Maladie","Argent","Prescription","État de Santé"], tablefmt="pipe")

    print("Suivi salle d'attente : \n")
    print(tableSA)
    print("\n")


def displayCabinet(docteur):
    dataCabinet = []
    for patient in Patient.Patients:
        patient_in = " "
        patient_out = " " 
        if patient.lieu == docteur.lieu: 
            patient_in = patient.nom
        if patient.poche != [] and patient.lieu != docteur.lieu: 
            patient_out = patient.nom
            patient_in = " "
        line = [f"{docteur.nom}",f"{docteur.argent}",f"{docteur.lieu.personnes}",f"{patient.maladie}",f"{patient_in}",f"{patient_out}"]
        dataCabinet.append(line)

    tableCabinet = tabulate(dataCabinet, headers=["Nom","Argent","Cabinet","Diagnostique","patient IN","Patient OUT"], tablefmt="pipe")

    print("Suivi Cabinet : \n")
    print(tableCabinet)
    print("\n")


def displayTraitements():
    dataTrait = []
    
    for traitement in Traitement.Traitements:
        line = [f"{traitement.nom}",f"{traitement.prix}"]
        dataTrait.append(line)
        
    # Créer le tableau avec tabulate
    tableTrait = tabulate(dataTrait, headers=["Nom du traitement","Prix"], tablefmt="pipe")

    # Afficher le tableau
    print("Tableau des Traitements : \n")
    print(tableTrait) 
    print("\n")


def displayDiags():
    dataDiags = []
    
    for diagnostique in Diagnostique.Diagnostiques:
        line = [f"{diagnostique.maladie}",f"{diagnostique.traitement}"]
        dataDiags.append(line)
        
    # Créer le tableau avec tabulate
    tableDiags = tabulate(dataDiags, headers=["Maladie","Traitement"], tablefmt="pipe")

    # Afficher le tableau
    print("Tableau des diagnostiques :\n")
    print(tableDiags) 
    print("\n")
    
def displayPharma(pharmacie,dataPharma):  
        # Créer le tableau avec tabulate
    for patient in Patient.Patients:
        if patient.lieu == pharmacie.nom :
            if patient.poche.prix > patient.argent:
                solvabilite = "Insolvable"
                patient.etat_de_sante = "Va mourir"
            else :
                solvabilite = "Solvable"
                patient.etat_de_sante = "Va guérir"
            line = [f"{pharmacie.nom}",f"{pharmacie.caisse}",f"{patient.nom}",f"{patient.argent}",f"{patient.poche.nom}",f"{patient.poche.prix}",f"{solvabilite}",f"{patient.etat_de_sante}"]
            dataPharma.append(line)

    tablePharma = tabulate(dataPharma, headers=["Pharmacie","En caisse","Patient","Solde","Traitement","Prix","Solvable","Etat patient"], tablefmt="pipe")

    # Afficher le tableau
    print("Tableau des diagnostiques :\n")
    print(tablePharma) 
    print("\n")
    return dataPharma


def main():
    #try:
    # Code principal
    #print(pharma_chez_baba.traitements_en_stock)
    #print(cabinet_Dr_X.personnes)
    #on met tous les patients dans la salle d'attente
    marcus.seDeplacer(chez_Marcus,salle_attente_Dr_X)
    optimus.seDeplacer(chez_Optimus,salle_attente_Dr_X)
    sangoku.seDeplacer(chez_sangoku,salle_attente_Dr_X)
    darthvader.seDeplacer(chez_vador,salle_attente_Dr_X)
    romulus.seDeplacer(chez_romulus,salle_attente_Dr_X)
    remus.seDeplacer(chez_remus,salle_attente_Dr_X)
    #print(salle_attente_Dr_X.personnes)
    
    displaySalleAttente()

    displayCabinet(doc)
    #displayDiags()
    #displayTraitements()
    #finally:
        # Définir le drapeau pour demander au thread de travail de s'arrêter
        #stop_flag.set()

    doc.inviter_a_entrer(marcus,cabinet_Dr_X)

    displayCabinet(doc)
    displaySalleAttente()

    doc.diagnostiquer(marcus,grippe)
    doc.se_faire_payer(marcus)

    displayCabinet(doc)
    displaySalleAttente()

    doc.prescrire(marcus,antiviraux)

    displaySalleAttente()

    displayCabinet(doc)

    doc.inviter_a_quitter(marcus,cabinet_Dr_X)

    displayCabinet(doc)
    displaySalleAttente()

    dataPharma_Baba = []
    marcus.seDeplacer(cabinet_Dr_X,pharma_chez_baba)

    displayPharma(pharma_chez_baba,dataPharma_Baba)

    marcus.payerMedoc(marcus.poche,pharma_chez_baba)

    dataPharma_Baba = displayPharma(pharma_chez_baba,dataPharma_Baba)

    marcus.seDeplacer(pharma_chez_baba,chez_Marcus)

    doc.inviter_a_entrer(optimus,cabinet_Dr_X)

    displayCabinet(doc)
    displaySalleAttente()

    doc.diagnostiquer(optimus,rhume_foin)
    doc.se_faire_payer(optimus)

    displayCabinet(doc)
    displaySalleAttente()

    doc.prescrire(optimus,antihistaminique)

    displaySalleAttente()

    displayCabinet(doc)

    doc.inviter_a_quitter(optimus,cabinet_Dr_X)

    displayCabinet(doc)
    displaySalleAttente()

    optimus.seDeplacer(cabinet_Dr_X,pharma_chez_baba)

    dataPharma_Baba = displayPharma(pharma_chez_baba,dataPharma_Baba)

    optimus.payerMedoc(optimus.poche,pharma_chez_baba)

    dataPharma_Baba = displayPharma(pharma_chez_baba,dataPharma_Baba)

    optimus.seDeplacer(pharma_chez_baba,chez_Optimus)







    










# Créer un drapeau partagé entre le thread principal et le thread de travail
stop_flag = threading.Event()

# Créez un thread pour la fonction chat_du_doc.miaule() and play_sound
sound_thread = threading.Thread(target=chat_du_doc.miaule())

# Lancez le thread pour jouer le son en parallèle
sound_thread.start()

# Exécutez votre fonction main() en même temps
main()

# Attendez que le thread de son se termine avant de quitter complètement le programme
sound_thread.join()











