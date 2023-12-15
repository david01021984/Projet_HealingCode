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
    
    def payerArticle(self, article):
        self.argent -= article.prix
        print(f"{self.nom} paie {article.nom} au prix de {article.prix}")

class Docteur(Personnage):
    def __init__(self, nom, argent, lieu, poche, specialisation):
        super().__init__(nom, argent, lieu, poche)
        self.specialisation = specialisation

    def diagnostiquer(self, patient, diagnostique):
        patient.maladie = diagnostique.maladie
        print(f"Je vous annonce que vous avez un {diagnostique}")
        return patient.maladie

    
    def se_faire_payer(self,patient,montant_consultation=50):
        if patient.argent >= montant_consultation:
            self.argent += montant_consultation
            patient.argent -= montant_consultation
        else :
            print("Je ne peux pas vous soigner mais il existe des plannings familliaux")
        
        
    def prescrire(self,patient,diagnostique):
        prescription = diagnostique.traitement
        return prescription
    

class Patient(Personnage):
    Patients = []
    def __init__(self, nom, argent, lieu, poche, maladie = "unknown", etat_de_sante = "Malade"):
        super().__init__(nom, argent, lieu, poche)
        self.maladie = maladie
        self.etat_de_sante = etat_de_sante
        Patient.Patients.append(self)
    

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
        line = [f"{patient.nom}",f"{patient.maladie}",f"{patient.argent}",f"{patient.poche}",f"{patient.etat_de_sante}"]
        dataSA.append(line)

    tableSA = tabulate(dataSA, headers=["Nom","Maladie","Argent","Poche","État de Santé"], tablefmt="pipe")

    print("Suivi salle d'attente : \n")
    print(tableSA)
    print("\n")

def displayCabinet(docteur):
    patient_in = " "
    patient_out = " " 
    dataCabinet = []
    for patient in Patient.Patients:
        if patient.maladie != "unknown" : patient_out = patient.nom
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
    
def displayPharma(pharmacie):
    dataPharma = []
        # Créer le tableau avec tabulate
    for patient in Patient.Patients:
        if patient.argent >= patient
        line = [f"{pharmacie.nom}",f"{pharmacie.caisse}",f"{patient.nom}",f"{patient.argent}",]
        dataPharma.append(line)

    tablePharma = tabulate(dataPharma, headers=["Pharmacie","En caisse","Patient","Solde","Solvable"], tablefmt="pipe")

    # Afficher le tableau
    print("Tableau des diagnostiques :\n")
    print(tablePharma) 
    print("\n")


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
    displayDiags()
    #displayTraitements()
    #finally:
        # Définir le drapeau pour demander au thread de travail de s'arrêter
        #stop_flag.set()





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











