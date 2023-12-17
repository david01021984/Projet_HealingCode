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

    def __init__(self, nom, argent:float, lieu , poche=None):
        self.nom = nom
        self.lieu = lieu
        self.argent = argent
        self.poche = [] if poche is None else poche


    
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
        if patient.etat_de_sante != "Mort":
            patient.maladie = diagnostique.maladie
            patient.etat_de_sante = "Diagnostiqué"
            print(f"{patient.nom}, je vous annonce que vous avez un {diagnostique.maladie}")
        else :
            print(f"Je ne peux pas vous diagnostiquer {patient.nom} vous n'avez pas payer la consult!")
        

    def se_faire_payer(self,patient,montant_consultation = 50):
        prix_a_payer = montant_consultation * (1 - patient.assurance.couverture) if patient.assurance else montant_consultation

        if patient.argent >= prix_a_payer:
            self.argent += prix_a_payer
            patient.argent -= prix_a_payer
            print(f"{patient.nom} a payé sa visite che le docteur {self.nom}")
        else :
            print("Je ne peux pas vous soigner mais il existe des plannings familliaux")
            patient.etat_de_sante = "Mort"
        
        
    def prescrire(self,patient,traitement):
        if patient.etat_de_sante != "Mort":
            patient.poche = traitement
            print(f"Allez à la pharmacie chercher {traitement.nom}")
        else :
            print("Encore désolé mais sans payer ma consultation, je ne peux pas vous donner de prescritpion!")
            print("Allez vous inscrire à la mutuelle ou prenez une autre assurance et revenez!")

    
    def inviter_a_entrer(self,patient,cabinet):
        patient.lieu = self.lieu
        cabinet.personnes.append(patient.nom)
        print(f"Le docteur {self.specialisation} : {self.nom} a invité {patient.nom} à entrer")

    def inviter_a_quitter(self,patient,cabinet):
        patient.lieu = " "
        cabinet.personnes.remove(patient.nom)
        if patient.etat_de_sante == "Mort":
            print(f"Bon courage {patient.nom}!")
        else :
            print(f"Bon rétablissement {patient.nom}!")

class Patient(Personnage):
    Patients = []
    def __init__(self, nom, argent, lieu, poche, maladie = None, etat_de_sante = None, assurance=None):
        #symptomes = None
        super().__init__(nom, argent, lieu, poche)
        self.maladie = "unknown" if maladie is None else maladie
        self.etat_de_sante = "Malade" if etat_de_sante is None else etat_de_sante
        self.assurance = assurance
#       self.symptomes = [] if symptomes is None else symptomes
        Patient.Patients.append(self)
    
    def payerMedoc(self, medoc,pharmacie):
        prix_a_payer = medoc.prix * (1 - self.assurance.couverture) if self.assurance else medoc.prix

        if self.poche != [] and self.argent >= prix_a_payer:
            self.argent -= prix_a_payer
            pharmacie.caisse += prix_a_payer
            pharmacie.traitements_en_stock.remove(medoc)
            self.etat_de_sante = "En traitement"
            print(f"{self.nom} paie {medoc.nom} au prix de {prix_a_payer} à {pharmacie.nom}")
        else : 
            print("Je ne peux pas vous donner de medicaments si vous n'avez pas de quoi payer!")
            print("Allez vous inscrire à la mutuelle ou prenez une autre assurance et revenez!")
            self.etat_de_sante = "Mort"


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
    
class Assurance():
    def __init__(self, nom, couverture):
        self.name = nom
        self.couverture = couverture

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

mutuelle = Assurance("Mutuelle", 0.5)  # 50% couverture avec la mutuelle
dkv = Assurance("Premium DKV", 0.8)  # 80% couverture avec la DKV

antiviraux = Traitement("Antiviraux", 8.7)
sedocar = Traitement("Sedocar",12)
insuline = Traitement("Insuline",6)
antihistaminique = Traitement("Antihistaminiques", 12)
antibiotique = Traitement("Antibiotique", 9.8)
nouveau_traitement_covid = Traitement("COVID",35)

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

marcus = Patient("Marcus",40,chez_Marcus,poche=[])
marcus.assurance = dkv
optimus = Patient("Optimus",200,chez_Optimus,poche=[])
sangoku = Patient("Sangoku",80,chez_sangoku,poche=[])
sangoku.assurance = mutuelle
darthvader = Patient("Vador",140, chez_vador,poche=[])
romulus = Patient("Romulus",240, chez_romulus,poche=[])
remus = Patient("Remus",60, chez_remus,poche=[])

pharma_chez_baba = Pharmacie("Pharmacie chez Baba",["Le Pharmacien (Baba)"],[antiviraux,sedocar,insuline,antihistaminique,antibiotique,nouveau_traitement_covid])


class DisplayManager():
    def __init__(self) -> None:
        pass

    def displaySalleAttente(self):
        dataSA = []

        for patient in Patient.Patients:
            if patient.lieu == salle_attente_Dr_X.nom:
                line = [f"{patient.nom}",f"{patient.maladie}",f"{patient.argent}",f"{patient.poche}",f"{patient.etat_de_sante}"]
                dataSA.append(line)

        tableSA = tabulate(dataSA, headers=["Nom","Maladie","Argent","Prescription","État de Santé"], tablefmt="pipe")

        print("Suivi salle d'attente : \n")
        print(tableSA)
        print("\n")
        time.sleep(2)


    def displayCabinet(self,docteur):
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
        time.sleep(2)


    def displayTraitements(self):
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

        time.sleep(2)


    def displayDiags(self):
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
        time.sleep(2)
        
    def displayPharma(self,pharmacie,dataPharma):  

        for patient in Patient.Patients:
            if patient.lieu == pharmacie.nom and patient.poche != []:
                if patient.poche.prix > patient.argent:
                    solvabilite = "Insolvable"
                    patient.etat_de_sante = "Mort"
                else :
                    solvabilite = "Solvable"
                    patient.etat_de_sante = "Va guérir"
                line = [f"{pharmacie.nom}",f"{pharmacie.caisse}",f"{patient.nom}",f"{patient.argent}",f"{patient.poche.nom}",f"{patient.poche.prix}",f"{solvabilite}",f"{patient.etat_de_sante}"]
                dataPharma.append(line)

        tablePharma = tabulate(dataPharma, headers=["Pharmacie","En caisse","Patient","Solde","Traitement","Prix","Solvabilite","Etat patient"], tablefmt="pipe")

        print("Tableau Pharmacie :\n")
        print(tablePharma) 
        print("\n")
        time.sleep(2)
        return dataPharma

    def displayCimetiere(self):
        dataCim = []

        for patient in Patient.Patients:
            if patient.etat_de_sante == "Mort":
                line = [f"{patient.nom}",f"{patient.etat_de_sante}"]
                dataCim.append(line)
            
        # Créer le tableau avec tabulate
        tableCim = tabulate(dataCim, headers=["Patient","Etat"], tablefmt="pipe")

        # Afficher le tableau
        print("Tableau Cimetière :\n")
        print(tableCim) 
        print("\n")
        time.sleep(2)


display_manager = DisplayManager()
def main():
   
    #on met tous les patients dans la salle d'attente
    marcus.seDeplacer(chez_Marcus,salle_attente_Dr_X)
    optimus.seDeplacer(chez_Optimus,salle_attente_Dr_X)
    sangoku.seDeplacer(chez_sangoku,salle_attente_Dr_X)
    darthvader.seDeplacer(chez_vador,salle_attente_Dr_X)
    romulus.seDeplacer(chez_romulus,salle_attente_Dr_X)
    remus.seDeplacer(chez_remus,salle_attente_Dr_X)
    #print(salle_attente_Dr_X.personnes)

    #MARCUS SCENARIO
    display_manager.displaySalleAttente()
    display_manager.displayCabinet(doc)

    doc.inviter_a_entrer(marcus,cabinet_Dr_X)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    doc.se_faire_payer(marcus,50)
    doc.diagnostiquer(marcus,grippe)
   

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    doc.prescrire(marcus,antiviraux)

    display_manager.displaySalleAttente()

    display_manager.displayCabinet(doc)

    doc.inviter_a_quitter(marcus,cabinet_Dr_X)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    dataPharma_Baba = []
    
    marcus.seDeplacer(cabinet_Dr_X,pharma_chez_baba)

    dataPharma_Baba = display_manager.displayPharma(pharma_chez_baba,dataPharma_Baba)

    marcus.payerMedoc(marcus.poche,pharma_chez_baba)

    dataPharma_Baba = display_manager.displayPharma(pharma_chez_baba,dataPharma_Baba)

    marcus.seDeplacer(pharma_chez_baba,chez_Marcus)

    #OPTIMUS SCENARIO
    
    doc.inviter_a_entrer(optimus,cabinet_Dr_X)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    doc.diagnostiquer(optimus,rhume_foin)
    doc.se_faire_payer(optimus,50)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    doc.prescrire(optimus,antihistaminique)

    display_manager.displaySalleAttente()

    display_manager.displayCabinet(doc)

    doc.inviter_a_quitter(optimus,cabinet_Dr_X)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    optimus.seDeplacer(cabinet_Dr_X,pharma_chez_baba)

    dataPharma_Baba = display_manager.displayPharma(pharma_chez_baba,dataPharma_Baba)

    optimus.payerMedoc(optimus.poche,pharma_chez_baba)

    dataPharma_Baba = display_manager.displayPharma(pharma_chez_baba,dataPharma_Baba)

    optimus.seDeplacer(pharma_chez_baba,chez_Optimus)

    #SANGOKU SCENARIO
    doc.inviter_a_entrer(sangoku,cabinet_Dr_X)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    doc.diagnostiquer(sangoku,hypertension)
    doc.se_faire_payer(sangoku,50)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    doc.prescrire(sangoku,sedocar)

    display_manager.displaySalleAttente()

    display_manager.displayCabinet(doc)

    doc.inviter_a_quitter(sangoku,cabinet_Dr_X)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    sangoku.seDeplacer(cabinet_Dr_X,pharma_chez_baba)

    dataPharma_Baba = display_manager.displayPharma(pharma_chez_baba,dataPharma_Baba)

    sangoku.payerMedoc(sangoku.poche,pharma_chez_baba)

    dataPharma_Baba = display_manager.displayPharma(pharma_chez_baba,dataPharma_Baba)

    sangoku.seDeplacer(pharma_chez_baba,chez_sangoku)

    #DARTHVADER SENARIO
    doc.inviter_a_entrer(darthvader,cabinet_Dr_X)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    doc.diagnostiquer(darthvader,infection_urinaire)
    doc.se_faire_payer(darthvader,60)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    doc.prescrire(darthvader,antibiotique)

    display_manager.displaySalleAttente()

    display_manager.displayCabinet(doc)

    doc.inviter_a_quitter(darthvader,cabinet_Dr_X)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    darthvader.seDeplacer(cabinet_Dr_X,pharma_chez_baba)

    dataPharma_Baba = display_manager.displayPharma(pharma_chez_baba,dataPharma_Baba)

    darthvader.payerMedoc(darthvader.poche,pharma_chez_baba)

    dataPharma_Baba = display_manager.displayPharma(pharma_chez_baba,dataPharma_Baba)

    darthvader.seDeplacer(pharma_chez_baba,chez_vador)

    #ROMULUS SCENARIO 
    
    doc.inviter_a_entrer(romulus,cabinet_Dr_X)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    doc.diagnostiquer(romulus,covid)
    doc.se_faire_payer(romulus,50)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    doc.prescrire(romulus,nouveau_traitement_covid)

    display_manager.displaySalleAttente()

    display_manager.displayCabinet(doc)

    doc.inviter_a_quitter(romulus,cabinet_Dr_X)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    romulus.seDeplacer(cabinet_Dr_X,pharma_chez_baba)

    dataPharma_Baba = display_manager.displayPharma(pharma_chez_baba,dataPharma_Baba)

    romulus.payerMedoc(romulus.poche,pharma_chez_baba)

    dataPharma_Baba = display_manager.displayPharma(pharma_chez_baba,dataPharma_Baba)

    romulus.seDeplacer(pharma_chez_baba,chez_romulus)     

    #REMUS SCENARIO 
    doc.inviter_a_entrer(remus,cabinet_Dr_X)

    display_manager.displayCabinet(doc)
    display_manager.displaySalleAttente()

    doc.diagnostiquer(remus,covid)
    doc.se_faire_payer(remus,50)

    display_manager.displayCabinet(doc)
  #  display_manager.displaySalleAttente()

    doc.prescrire(remus,nouveau_traitement_covid)

  #  display_manager.displaySalleAttente()

    display_manager.displayCabinet(doc)

    doc.inviter_a_quitter(remus,cabinet_Dr_X)

    display_manager.displayCabinet(doc)
   # display_manager.displaySalleAttente()

    remus.seDeplacer(cabinet_Dr_X,pharma_chez_baba)

    dataPharma_Baba = display_manager.displayPharma(pharma_chez_baba,dataPharma_Baba)

    remus.payerMedoc(remus.poche,pharma_chez_baba)

    dataPharma_Baba = display_manager.displayPharma(pharma_chez_baba,dataPharma_Baba)

    remus.seDeplacer(pharma_chez_baba,chez_remus)

    display_manager.displayCimetiere()

    display_manager.displayDiags()

    display_manager.displayTraitements()




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











