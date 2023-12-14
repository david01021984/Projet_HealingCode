import time
import pygame

class Lieu():
# Lieu: Représente un lieu avec un nom et une liste de personnes présentes
    def __init__(self, nom, personnes = None):
        self.nom = nom
        self.personnes = [] if personnes is None else personnes


class Personnage():
# Personnage: Représente un personnage avec un nom, une quantité d'argent, un lieu actuel, 
# et des objets dans ses mains droite et gauche

    def __init__(self, nom, argent:float, lieu = None, poche=[]):
        self.nom = nom
        self.lieu = lieu
        self.argent = argent
        self.poche = poche
    
    def seDeplacer(self, depart,destination):
        if self.nom in depart:
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
        patient.maladie = diagnostique
        print(f"Je vous annonce que vous avez un {diagnostique}")

    
    def se_faire_payer(self,patient,montant_consultation):
        if patient.argent >= montant_consultation:
            self.argent += montant_consultation
            patient.argent -= montant_consultation
        else :
            print("Je ne peux pas vous soigner mais il existe des plannings familliaux")
        
        
    def prescrire(traitement):
        pass


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
    def __init__(self, nom, personnes=None,traitements_en_stock=[]):
        super().__init__(nom, personnes)
        self.traitements_en_stock = traitements_en_stock
 

class Chat():
    def __init__(self,nom,race):
        self.nom = nom
        self.race = race
        pygame.mixer.init()  # Initialize the mixer
        pygame.mixer.music.load("meow.wav") 

    def miaule(self):
        pygame.mixer.music.play()
        time.sleep(4)
        pygame.mixer.music.stop()

#init    
chat_du_doc = Chat("Xerxès","Sphynx")
chat_du_doc.miaule()

antiviraux = Traitement("Antiviraux", 8.7)
sedocar = Traitement("Sedocar",12)
insuline = Traitement("Insuline",6)
antihistaminique = Traitement("Antihistaminiques", 12)
antibiotique = Traitement("Antibiotique", 9.8)

grippe = Diagnostique("Grippe",antiviraux)
hypertension = Diagnostique("Hypertension",sedocar)
diabete = Diagnostique("Diabète",insuline)
rhume_foin = Diagnostique("Rhume des foins",antihistaminique)
infection_urinaire = Diagnostique("Infection urinaire",antibiotique)

cabinet_doc = Lieu("Cabinet du Docteur X", personnes=["Dr X","Xerxès le Sphynx"])
salle_attente = Lieu("Salle d'attente")

chez_Marcus = Lieu("Maison de Marcus",["Marcus"])
chez_Optimus = Lieu("Maison d'Optimus",["Optimus"])
chez_sangoku = Lieu("Temple de Goku",["SanGoku"])
chez_vador = Lieu("Vaisseau de Darth Vador",["Darth Vador"])
chez_romulus = Lieu("Chez Romulus",["Romulus"])
chez_remus = Lieu("Chez Remus",["Remus"]
                  )
doc = Docteur("Dr X",1000,cabinet_doc,poche=[],specialisation="Généraliste")

marcus = Patient("Marcus",100,chez_Marcus,poche=[])
optimus = Patient("Optimus Prime",200,chez_Optimus,poche=[])
sangoku = Patient("Sangoku",80,chez_sangoku,poche=[])
darthvader = Patient("Darth Vador",140, chez_vador,poche=[])
romulus = Patient("Romulus",240, chez_romulus,poche=[])
remus = Patient("Remus",60, chez_remus,poche=[])

pharma_chez_baba = Pharmacie("Pharmacie chez Baba",["Le Pharmacien (Baba)"])











