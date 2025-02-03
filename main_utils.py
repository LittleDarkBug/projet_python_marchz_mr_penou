from core.classes.Admin import Admin
from core.classes.Client import Client
from core.classes.EspaceMarche import EspaceMarche
from core.classes.FactureVente import FactureVente
from core.classes.Fournisseur import Fournisseur
from core.classes.Marchand import Marchand
from core.classes.Produit import Produit
from core.classes.Utilisateur import Utilisateur
from core.enums.TypeUniteEnum import TypeUniteEnum
from core.services.AuthService import AuthManager
from demos.achat_client import demo_achats
from demos.historiques import demo_historique
from demos.optimisation_recherche import demo_optimisation_recherche
from demos.espace_marche import demo_espace_marche
import time
from demos.marchands_produits import demo_creation_marche_et_marchands
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from datetime import datetime
from core.enums.ModaliteVenteEnum import ModaliteVenteEnum
from core.classes.LigneVente import LigneVente

console = Console()

class Session:
    def __init__(self):
        self.utilisateur_connecte = False
        self.utilisateur_auth = None
        self.role_utilisateur = None

    def se_connecter(self):
        """Permet à l'utilisateur de se connecter."""
        if self.utilisateur_connecte:
            print("[bold red]Vous êtes déjà connecté.[/bold red]")
            return
        
        username = console.input("[cyan]Entrez votre nom d'utilisateur: [/cyan]")
        password = console.input("[cyan]Entrez votre mot de passe: [/cyan]")
        
        auth_manager = AuthManager()
        self.utilisateur_auth = auth_manager.authenticate_user(username, password)
        
        if self.utilisateur_auth:
            self.utilisateur_connecte = True
            self.role_utilisateur = self.utilisateur_auth.__class__.__name__.lower()  # Identifie le rôle par le nom de la classe
            print(f"[green]Connexion réussie en tant que {self.role_utilisateur.capitalize()}.[/green]")
            self.gerer_menu_specifique()
        else:
            print("[bold red]Nom d'utilisateur ou mot de passe incorrect.[/bold red]")

    def afficher_menu_principal(self):
        """Affiche le menu principal après connexion selon le rôle."""
        if self.role_utilisateur == "admin":
            print(Panel("[bold cyan]Menu Admin[/bold cyan]", title="Menu Admin", subtitle="Sélectionnez une option"))
            print("[yellow]1.[/] Gérer les utilisateurs")
            print("[yellow]2.[/] Gérer les marchés")
            print("[yellow]3.[/] Se déconnecter")
        elif self.role_utilisateur == "marchand":
            print(Panel("[bold cyan]Menu Marchand[/bold cyan]", title="Menu Marchand", subtitle="Sélectionnez une option"))
            print("[yellow]1.[/] Gérer les stock de produits")
            print("[yellow]2.[/] Gérer les ventes")
            print("[yellow]3.[/] Statistiques et Rapports")
            print("[yellow]4.[/] Gérer les fournisseurs")
            print("[yellow]5.[/] Se déconnecter")
        elif self.role_utilisateur == "client":
            print(Panel("[bold cyan]Menu Client[/bold cyan]", title="Menu Client", subtitle="Sélectionnez une option"))
            print("[yellow]1.[/] Gérer les démonstrations")
            print("[yellow]2.[/] Autres actions client")
            print("[yellow]3.[/] Se déconnecter")

    def gerer_menu_specifique(self):
        """Gère les actions spécifiques à chaque rôle."""
        if self.role_utilisateur == "admin":
            while True:
                print(Panel("[bold cyan]Gestion Administrative[/bold cyan]"))
                print("[yellow]1.[/] Gérer les utilisateurs")
                print("[yellow]2.[/] Gérer les marchés")
                print("[yellow]3.[/] Retour au menu principal")
                
                choix = console.input("[magenta]Veuillez choisir une option (1-3): [/magenta]")
                if choix == "1":
                    self.gerer_utilisateurs()
                elif choix == "2":
                    self.gerer_marches()
                elif choix == "3":
                    print("[bold red]Déconnexion...[/bold red]")
                    self.utilisateur_connecte = False
                    self.role_utilisateur = None
                    self.utilisateur_auth = None
                    break
                else:
                    print("[bold red]Choix invalide.[/bold red]")
                    
        elif self.role_utilisateur == "marchand":
            while True:
                print(Panel("[bold cyan]Actions Marchand[/bold cyan]"))
                print("[yellow]1.[/] Gérer mes produits")
                print("[yellow]2.[/] Gérer les ventes")
                print("[yellow]3.[/] Statistiques et Rapports")
                print("[yellow]4.[/] Gérer les fournisseurs")
                print("[yellow]5.[/] Se déconnecter")
                
                choix = console.input("[magenta]Veuillez choisir une option (1-5): [/magenta]")
                if choix == "1":
                    self.gerer_produits()
                elif choix == "2":
                    self.gerer_ventes()
                elif choix == "3":
                    self.afficher_statistiques()
                elif choix == "4":
                    self.gerer_fournisseurs()
                elif choix == "5":
                    print("[bold red]Déconnexion...[/bold red]")
                    self.utilisateur_connecte = False
                    self.role_utilisateur = None
                    self.utilisateur_auth = None
                    break
                else:
                    print("[bold red]Choix invalide.[/bold red]")
                    
        elif self.role_utilisateur == "client":
            self.gerer_menu_client()

    def gerer_menu_client(self):
        """Gestion du menu client."""
        while True:
            print(Panel("[bold cyan]Actions Client[/bold cyan]"))
            print("[yellow]1.[/] Voir mon panier")
            print("[yellow]2.[/] Voir mes Factures")
            print("[yellow]3.[/] Rechercher des produits et ajout éventuel au panier")
            print("[yellow]4.[/] Enregistrer un achat")
            print("[yellow]5.[/] Retour au menu principal")
            
            choix = self.input_securise("[magenta]Veuillez choisir une option (1-5): [/magenta]")
            
            if choix == "1":
                self.voir_panier()
            elif choix == "2":
                self.voir_factures()
            elif choix == "3":
                self.rechercher_produits()
            elif choix == "4":
                self.enregistrer_achat()
            elif choix == "5":
                break
            else:
                print("[bold red]Option invalide.[/bold red]")

    def voir_panier(self):
        """Affiche le contenu du panier actuel."""
        if not hasattr(self.utilisateur_auth, 'panier'):
            self.utilisateur_auth.panier = {}
        
        if not self.utilisateur_auth.panier:
            print("[yellow]Votre panier est vide.[/yellow]")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Produit", style="cyan")
        table.add_column("Quantité", style="yellow")
        table.add_column("Prix unitaire", style="green")
        table.add_column("Total", style="red")
        
        total_panier = 0
        for produit, quantite in self.utilisateur_auth.panier.items():
            prix_total = produit.prix_vente * quantite
            total_panier += prix_total
            table.add_row(
                produit.libelle,
                str(quantite),
                f"{produit.prix_vente:.2f} FCFA",
                f"{prix_total:.2f} FCFA"
            )
        
        console.print(table)
        print(f"[bold green]Total du panier: {total_panier:.2f} FCFA[/bold green]")

    def voir_factures(self):
        """Affiche l'historique des factures du client."""
        factures = self.utilisateur_auth.liste_achats
        
        if not factures:
            print("[yellow]Vous n'avez pas encore effectué d'achats.[/yellow]")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Date", style="cyan")
        table.add_column("N° Facture", style="yellow")
        table.add_column("Produits", style="green")
        table.add_column("Total", style="red")
        
        for facture in factures:
            produits_str = ", ".join([f"{ligne.produit.libelle} (x{ligne.quantite})" for ligne in facture.lignes])
            table.add_row(
                facture.date_vente.strftime('%d/%m/%Y %H:%M'),
                facture.numero_vente,
                produits_str,
                f"{facture.prix_total:.2f} FCFA"
            )
        
        console.print(table)

    def rechercher_produits(self):
        """Recherche des produits et permet de les ajouter au panier."""
        mot_cle = self.input_securise("[cyan]Entrez un mot-clé pour la recherche: [/cyan]")
        
        # Récupérer tous les marchands
        marchands = Marchand.objects()
        produits_trouves = []
        
        # Rechercher dans les produits de chaque marchand
        for marchand in marchands:
            produits_marchand = marchand.rechercher_produit(mot_cle)
            for produit in produits_marchand:
                produits_trouves.append((produit, marchand))
        
        if not produits_trouves:
            print("[yellow]Aucun produit trouvé.[/yellow]")
            return
        
        # Afficher les résultats
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("N°", style="cyan")
        table.add_column("Produit", style="yellow")
        table.add_column("Prix", style="green")
        table.add_column("Stock", style="blue")
        table.add_column("Marchand", style="magenta")
        
        for i, (produit, marchand) in enumerate(produits_trouves, 1):
            table.add_row(
                str(i),
                produit.libelle,
                f"{produit.prix_vente:.2f} FCFA",
                str(produit.quantite),
                marchand.nom
            )
        
        console.print(table)
        
        # Proposer d'ajouter au panier
        choix = self.input_securise("[cyan]Entrez le numéro du produit à ajouter au panier (0 pour annuler): [/cyan]")
        if choix == "0":
            return
        
        try:
            index = int(choix) - 1
            if 0 <= index < len(produits_trouves):
                produit, _ = produits_trouves[index]
                quantite = self.input_nombre(
                    "[cyan]Quantité désirée: [/cyan]",
                    min_val=1,
                    max_val=produit.quantite
                )
                
                if not hasattr(self.utilisateur_auth, 'panier'):
                    self.utilisateur_auth.panier = {}
                
                if produit in self.utilisateur_auth.panier:
                    self.utilisateur_auth.panier[produit] += quantite
                else:
                    self.utilisateur_auth.panier[produit] = quantite
                
                print("[bold green]Produit ajouté au panier![/bold green]")
            else:
                print("[bold red]Numéro invalide.[/bold red]")
        except ValueError:
            print("[bold red]Veuillez entrer un numéro valide.[/bold red]")

    def enregistrer_achat(self):
        """Enregistre l'achat à partir du panier."""
        if not hasattr(self.utilisateur_auth, 'panier') or not self.utilisateur_auth.panier:
            print("[yellow]Votre panier est vide.[/yellow]")
            return
        
        # Vérifier les stocks
        for produit, quantite in self.utilisateur_auth.panier.items():
            if produit.quantite < quantite:
                print(f"[bold red]Stock insuffisant pour {produit.libelle} (disponible: {produit.quantite})[/bold red]")
                return
        
        # Créer les lignes de vente
        lignes_vente = []
        total_prix = 0
        
        for produit, quantite in self.utilisateur_auth.panier.items():
            prix_total_ligne = quantite * produit.prix_vente
            ligne = LigneVente(
                quantite=quantite,
                prix_total_ligne=prix_total_ligne,
                produit=produit
            )
            ligne.save()
            lignes_vente.append(ligne)
            total_prix += prix_total_ligne
            
            # Mettre à jour le stock
            produit.quantite -= quantite
            produit.save()
        
        # Créer la facture
        numero_vente = f"V{int(time.time())}"
        facture = FactureVente(
            prix_total=total_prix,
            numero_vente=numero_vente,
            date_vente=datetime.now(),
            modalite=ModaliteVenteEnum.EN_LIGNE.value,
            lignes=lignes_vente,
            acheteur=self.utilisateur_auth
        )
        facture.save()
        
        # Ajouter la facture à l'historique du client
        self.utilisateur_auth.add_achat(facture)
        self.utilisateur_auth.save()
        
        # Vider le panier
        self.utilisateur_auth.panier = {}
        
        print("[bold green]Achat enregistré avec succès![/bold green]")
        print(f"[cyan]Numéro de facture: {numero_vente}[/cyan]")

    def afficher_menu_demos(self):
        """Affiche le menu des démonstrations disponibles."""
        print(Panel("[bold cyan]Menu des Démonstrations[/bold cyan]", title="Menu des Démonstrations", subtitle="Sélectionnez une démonstration"))
        print("[yellow]1.[/] Démonstration : Placement des marchands")
        print("[yellow]2.[/] Démonstration : Création de marché, marchands, ajouts et retraits de produits.")
        print("[yellow]3.[/] Démonstration : Optimisation de l'achat pour un client")
        print("[yellow]4.[/] Démonstration : Achat client")
        print("[yellow]5.[/] Démonstration : Historique des achats par marchand")
        print("[yellow]6.[/] Retour au menu principal")
        choix = console.input("[magenta]Veuillez choisir une option (1-6): [/magenta]")
        return choix

    def gerer_menu_demos(self):
        """Gère le menu des démonstrations et exécute la démonstration choisie."""
        while True:
            choix = self.afficher_menu_demos()
            if choix == "1":
                demo_espace_marche()  # Appel de la démonstration
                time.sleep(5)
            elif choix == "2":
                demo_creation_marche_et_marchands()
                time.sleep(5)
            elif choix == "3":
                demo_optimisation_recherche()
                time.sleep(5)
            elif choix == "4":
                demo_achats()
                time.sleep(5)
                break
            elif choix == "5":
                demo_historique()
                time.sleep(5)
                break
            elif choix == "6":
                print("[bold cyan]Retour au menu principal.[/bold cyan]")
                break
            else:
                print("[bold red]Choix invalide. Veuillez choisir une option entre 1 et 5.[/bold red]")
    
    def fermer(self): 
        """Ferme le programme définitivement."""
        print("[bold red]Fermeture du programme.[/bold red]")
        exit()

    def valider_telephone(self, telephone: str) -> bool:
        """Valide le format du numéro de téléphone."""
        import re
        pattern = r'^\+?[0-9]{8,}$'
        return bool(re.match(pattern, telephone))

    def valider_champs_obligatoires(self, data: dict) -> bool:
        """Vérifie que tous les champs obligatoires sont remplis."""
        return all(data[field].strip() for field in ['nom', 'prenom', 'telephone', 'adresse', 'username', 'password'])

    @staticmethod
    def input_securise(message: str, obligatoire: bool = True, validation_func=None) -> str:
        """Gère la saisie sécurisée avec validation."""
        while True:
            valeur = console.input(message).strip()
            if not valeur and obligatoire:
                print("[bold red]Ce champ est obligatoire.[/bold red]")
                continue
            if validation_func and valeur:
                if not validation_func(valeur):
                    print("[bold red]Format invalide.[/bold red]")
                    continue
            return valeur

    def input_nombre(self, message: str, min_val: int = None, max_val: int = None) -> int:
        """Gère la saisie sécurisée d'un nombre."""
        while True:
            try:
                valeur = int(console.input(message))
                if min_val is not None and valeur < min_val:
                    print(f"[bold red]La valeur doit être supérieure ou égale à {min_val}.[/bold red]")
                    continue
                if max_val is not None and valeur > max_val:
                    print(f"[bold red]La valeur doit être inférieure ou égale à {max_val}.[/bold red]")
                    continue
                return valeur
            except ValueError:
                print("[bold red]Veuillez entrer un nombre valide.[/bold red]")

    def collecter_donnees_utilisateur(self) -> dict:
        """Collecte et valide les données utilisateur."""
        user_data = {
            "nom": self.input_securise("[cyan]Nom: [/cyan]"),
            "prenom": self.input_securise("[cyan]Prénom: [/cyan]"),
            "telephone": self.input_securise("[cyan]Téléphone: [/cyan]", validation_func=self.valider_telephone),
            "adresse": self.input_securise("[cyan]Adresse: [/cyan]"),
            "username": self.input_securise("[cyan]Nom d'utilisateur: [/cyan]"),
            "password": self.input_securise("[cyan]Mot de passe: [/cyan]")
        }
        return user_data

    def gerer_utilisateurs(self):
        """Interface de gestion des utilisateurs pour l'admin."""
        while True:
            print(Panel("[bold cyan]Gestion des Utilisateurs[/bold cyan]"))
            print("[yellow]1.[/] Créer un utilisateur")
            print("[yellow]2.[/] Supprimer un utilisateur")
            print("[yellow]3.[/] Modifier un utilisateur")
            print("[yellow]4.[/] Lister les utilisateurs")
            print("[yellow]5.[/] Retour")
            
            choix = self.input_securise("[magenta]Veuillez choisir une option (1-5): [/magenta]")
            
            if choix == "1":
                try:
                    user_data = self.collecter_donnees_utilisateur()
                    
                    while True:
                        role = self.input_securise("[cyan]Rôle (admin/marchand/client): [/cyan]").lower()
                        if role in ["admin", "marchand", "client"]:
                            break
                        print("[bold red]Rôle invalide. Veuillez choisir parmi: admin, marchand, client[/bold red]")
                    
                    if role == "marchand":
                        while True:
                            type_marchand = self.input_securise("[cyan]Type de marchand (GROSSISTE/DETAILLANT/MIXTE): [/cyan]").upper()
                            if type_marchand in ["GROSSISTE", "DETAILLANT", "MIXTE"]:
                                user_data["type_marchand"] = type_marchand
                                break
                            print("[bold red]Type invalide. Veuillez choisir parmi: GROSSISTE, DETAILLANT, MIXTE[/bold red]")
                    
                    if role == "admin":
                        Admin(**user_data).save()
                    elif role == "marchand":
                        Marchand(**user_data).save()
                    elif role == "client":
                        Client(**user_data).save()
                    print("[bold green]Utilisateur créé avec succès![/bold green]")
                    
                except Exception as e:
                    print(f"[bold red]Erreur lors de la création: {str(e)}[/bold red]")
                    
            elif choix == "2":
                username = self.input_securise("[cyan]Nom d'utilisateur à supprimer: [/cyan]")
                user = Utilisateur.find_one({"username": username})
                if user:
                    confirmation = self.input_securise("[red]Êtes-vous sûr de vouloir supprimer cet utilisateur? (oui/non): [/red]").lower()
                    if confirmation == "oui":
                        user.delete()
                        print("[bold green]Utilisateur supprimé avec succès![/bold green]")
                    else:
                        print("[yellow]Suppression annulée.[/yellow]")
                else:
                    print("[bold red]Utilisateur non trouvé.[/bold red]")
                    
            elif choix == "3":
                username = self.input_securise("[cyan]Nom d'utilisateur à modifier: [/cyan]")
                user = Utilisateur.find_one({"username": username})
                if user:
                    print("[cyan]Laissez vide pour ne pas modifier[/cyan]")
                    user.nom = self.input_securise("[cyan]Nouveau nom: [/cyan]", obligatoire=False) or user.nom
                    user.prenom = self.input_securise("[cyan]Nouveau prénom: [/cyan]", obligatoire=False) or user.prenom
                    
                    nouveau_tel = self.input_securise("[cyan]Nouveau téléphone: [/cyan]", obligatoire=False, validation_func=self.valider_telephone)
                    if nouveau_tel:
                        user.telephone = nouveau_tel
                    
                    user.adresse = self.input_securise("[cyan]Nouvelle adresse: [/cyan]", obligatoire=False) or user.adresse
                    
                    try:
                        user.save()
                        print("[bold green]Utilisateur modifié avec succès![/bold green]")
                    except Exception as e:
                        print(f"[bold red]Erreur lors de la modification: {str(e)}[/bold red]")
                else:
                    print("[bold red]Utilisateur non trouvé.[/bold red]")
                    
            elif choix == "4":
                users = Utilisateur.objects()
                if users:
                    for user in users:
                        print(f"[cyan]{user}[/cyan]")
                else:
                    print("[yellow]Aucun utilisateur trouvé.[/yellow]")
                    
            elif choix == "5":
                break
            else:
                print("[bold red]Option invalide.[/bold red]")

    def gerer_marches(self):
        """Interface de gestion des marchés pour l'admin."""
        while True:
            print(Panel("[bold cyan]Gestion des Marchés[/bold cyan]"))
            print("[yellow]1.[/] Créer un marché")
            print("[yellow]2.[/] Supprimer un marché")
            print("[yellow]3.[/] Assigner un marchand")
            print("[yellow]4.[/] Retirer un marchand")
            print("[yellow]5.[/] Lister les marchés")
            print("[yellow]6.[/] Retour")
            
            choix = self.input_securise("[magenta]Veuillez choisir une option (1-6): [/magenta]")
            
            if choix == "1":
                nom = self.input_securise("[cyan]Nom du marché: [/cyan]")
                taille_x = self.input_nombre("[cyan]Taille X: [/cyan]", min_val=1, max_val=10000)
                taille_y = self.input_nombre("[cyan]Taille Y: [/cyan]", min_val=1, max_val=10000)
                
                try:
                    marche = EspaceMarche(nom=nom, taille=(taille_x, taille_y))
                    marche.save()
                    print("[bold green]Marché créé avec succès![/bold green]")
                except Exception as e:
                    print(f"[bold red]Erreur lors de la création: {str(e)}[/bold red]")
                    
            elif choix == "2":
                nom = self.input_securise("[cyan]Nom du marché à supprimer: [/cyan]")
                marche = EspaceMarche.objects(nom=nom).first()
                if marche:
                    confirmation = self.input_securise("[red]Êtes-vous sûr de vouloir supprimer ce marché? (oui/non): [/red]").lower()
                    if confirmation == "oui":
                        marche.delete()
                        print("[bold green]Marché supprimé avec succès![/bold green]")
                    else:
                        print("[yellow]Suppression annulée.[/yellow]")
                else:
                    print("[bold red]Marché non trouvé.[/bold red]")
                    
            elif choix == "3":
                nom_marche = self.input_securise("[cyan]Nom du marché: [/cyan]")
                username_marchand = self.input_securise("[cyan]Nom d'utilisateur du marchand: [/cyan]")
                
                marche = EspaceMarche.objects(nom=nom_marche).first()
                marchand = Marchand.find_one({"username": username_marchand})
                
                if marche and marchand:
                    try:
                        x = self.input_nombre("[cyan]Position X: [/cyan]", min_val=0, max_val=marche.taille[0]-1)
                        y = self.input_nombre("[cyan]Position Y: [/cyan]", min_val=0, max_val=marche.taille[1]-1)
                        marche.ajouter_marchand(marchand, x, y)
                        print("[bold green]Marchand assigné avec succès![/bold green]")
                    except ValueError as e:
                        print(f"[bold red]Erreur: {str(e)}[/bold red]")
                else:
                    print("[bold red]Marché ou marchand non trouvé.[/bold red]")
                    
            elif choix == "4":
                nom_marche = self.input_securise("[cyan]Nom du marché: [/cyan]")
                username_marchand = self.input_securise("[cyan]Nom d'utilisateur du marchand: [/cyan]")
                
                marche = EspaceMarche.objects(nom=nom_marche).first()
                marchand = Marchand.find_one({"username": username_marchand})
                
                if marche and marchand:
                    try:
                        marche.retirer_marchand(marchand)
                        print("[bold green]Marchand retiré avec succès![/bold green]")
                    except ValueError as e:
                        print(f"[bold red]Erreur: {str(e)}[/bold red]")
                else:
                    print("[bold red]Marché ou marchand non trouvé.[/bold red]")
                    
            elif choix == "5":
                marches = EspaceMarche.objects()
                if marches:
                    for marche in marches:
                        print(f"[cyan]{marche}[/cyan]")
                else:
                    print("[yellow]Aucun marché trouvé.[/yellow]")
                    
            elif choix == "6":
                break
            else:
                print("[bold red]Option invalide.[/bold red]")

    def gerer_produits(self):
        """Gestion des produits pour le marchand."""
        while True:
            print(Panel("[bold cyan]Gestion des Produits[/bold cyan]"))
            print("[yellow]1.[/] Ajouter un produit")
            print("[yellow]2.[/] Modifier un produit")
            print("[yellow]3.[/] Supprimer un produit")
            print("[yellow]4.[/] Lister mes produits")
            print("[yellow]5.[/] Retour")
            
            choix = self.input_securise("[magenta]Veuillez choisir une option (1-5): [/magenta]")
            
            if choix == "1":
                try:
                    libelle = self.input_securise("[cyan]Libellé du produit: [/cyan]")
                    prix_achat = float(self.input_securise("[cyan]Prix d'achat: [/cyan]"))
                    prix_vente = float(self.input_securise("[cyan]Prix de vente: [/cyan]"))
                    description = self.input_securise("[cyan]Description: [/cyan]")
                    quantite = int(self.input_securise("[cyan]Quantité: [/cyan]"))
                    
                    # Sélection du type d'unité
                    print("Types d'unités disponibles:")
                    for type_unite in TypeUniteEnum:
                        print(f"- {type_unite.name}")
                    type_unite = self.input_securise("[cyan]Type d'unité: [/cyan]").upper()
                    
                    # Sélection du fournisseur
                    fournisseurs = Fournisseur.objects()
                    if fournisseurs:
                        print("Fournisseurs disponibles:")
                        for f in fournisseurs:
                            print(f"- {f.nom} (ID: {f.id})")
                        fournisseur_id = self.input_securise("[cyan]ID du fournisseur: [/cyan]")
                        fournisseur = Fournisseur.find_by_id(fournisseur_id)
                    else:
                        print("[yellow]Aucun fournisseur disponible.[/yellow]")
                        fournisseur = None
                    
                    produit = Produit(
                        libelle=libelle,
                        prix_achat=prix_achat,
                        prix_vente=prix_vente,
                        description=description,
                        type_unite=type_unite,
                        quantite=quantite,
                        fournisseur=fournisseur
                    )
                    produit.save()
                    
                    # Ajouter le produit au marchand
                    marchand = self.utilisateur_auth
                    marchand.ajouter_produit(produit)
                    print("[bold green]Produit ajouté avec succès![/bold green]")
                    
                except Exception as e:
                    print(f"[bold red]Erreur lors de l'ajout: {str(e)}[/bold red]")
                    
            elif choix == "2":
                try:
                    produits = self.utilisateur_auth.produits
                    if not produits:
                        print("[yellow]Vous n'avez aucun produit.[/yellow]")
                        continue
                    
                    print("Vos produits:")
                    for i, p in enumerate(produits, 1):
                        print(f"[cyan]{i}. {p.libelle}[/cyan]")
                    
                    index = int(self.input_securise("[cyan]Numéro du produit à modifier: [/cyan]")) - 1
                    if 0 <= index < len(produits):
                        produit = produits[index]
                        print("[cyan]Laissez vide pour ne pas modifier[/cyan]")
                        
                        nouveau_libelle = self.input_securise("[cyan]Nouveau libellé: [/cyan]", obligatoire=False)
                        if nouveau_libelle:
                            produit.libelle = nouveau_libelle
                            
                        nouveau_prix_achat = self.input_securise("[cyan]Nouveau prix d'achat: [/cyan]", obligatoire=False)
                        if nouveau_prix_achat:
                            produit.prix_achat = float(nouveau_prix_achat)
                            
                        nouveau_prix_vente = self.input_securise("[cyan]Nouveau prix de vente: [/cyan]", obligatoire=False)
                        if nouveau_prix_vente:
                            produit.prix_vente = float(nouveau_prix_vente)
                            
                        nouvelle_quantite = self.input_securise("[cyan]Nouvelle quantité: [/cyan]", obligatoire=False)
                        if nouvelle_quantite:
                            produit.quantite = int(nouvelle_quantite)
                        
                        produit.save()
                        print("[bold green]Produit modifié avec succès![/bold green]")
                    else:
                        print("[bold red]Index invalide.[/bold red]")
                    
                except Exception as e:
                    print(f"[bold red]Erreur lors de la modification: {str(e)}[/bold red]")
                    
            elif choix == "3":
                try:
                    produits = self.utilisateur_auth.produits
                    if not produits:
                        print("[yellow]Vous n'avez aucun produit.[/yellow]")
                        continue
                    
                    print("Vos produits:")
                    for i, p in enumerate(produits, 1):
                        print(f"[cyan]{i}. {p.libelle}[/cyan]")
                    
                    index = int(self.input_securise("[cyan]Numéro du produit à supprimer: [/cyan]")) - 1
                    if 0 <= index < len(produits):
                        produit = produits[index]
                        confirmation = self.input_securise("[red]Êtes-vous sûr de vouloir supprimer ce produit? (oui/non): [/red]").lower()
                        if confirmation == "oui":
                            self.utilisateur_auth.retirer_produit(produit)
                            produit.delete()
                            print("[bold green]Produit supprimé avec succès![/bold green]")
                        else:
                            print("[yellow]Suppression annulée.[/yellow]")
                    else:
                        print("[bold red]Index invalide.[/bold red]")
                    
                except Exception as e:
                    print(f"[bold red]Erreur lors de la suppression: {str(e)}[/bold red]")
                    
            elif choix == "4":
                produits = self.utilisateur_auth.produits
                if produits:
                    table = Table(show_header=True, header_style="bold magenta")
                    table.add_column("Libellé", style="cyan")
                    table.add_column("Prix Vente", style="green")
                    table.add_column("Quantité", style="yellow")
                    table.add_column("Fournisseur", style="blue")
                    
                    for p in produits:
                        table.add_row(
                            p.libelle,
                            f"{p.prix_vente:.2f} FCFA",
                            str(p.quantite),
                            p.fournisseur.nom if p.fournisseur else "N/A"
                        )
                    console.print(table)
                else:
                    print("[yellow]Vous n'avez aucun produit.[/yellow]")
                    
            elif choix == "5":
                break
            else:
                print("[bold red]Option invalide.[/bold red]")

    def gerer_ventes(self):
        """Gestion des ventes pour le marchand."""
        while True:
            print(Panel("[bold cyan]Gestion des Ventes[/bold cyan]"))
            print("[yellow]1.[/] Voir les ventes")
            print("[yellow]2.[/] Retour")
            
            choix = self.input_securise("[magenta]Veuillez choisir une option (1-2): [/magenta]")
            
            if choix == "1":
                # Récupérer les IDs des produits du marchand
                produits_marchand = set(produit.id for produit in self.utilisateur_auth.produits)
                
                # Récupérer toutes les factures
                all_ventes = FactureVente.objects()
                
                # Filtrer les factures qui contiennent au moins un produit du marchand
                ventes_marchand = [
                    vente for vente in all_ventes
                    if any(
                        ligne.produit.id in produits_marchand
                        for ligne in vente.lignes
                    )
                ]
                
                if ventes_marchand:
                    table = Table(show_header=True, header_style="bold magenta")
                    table.add_column("Date", style="cyan")
                    table.add_column("N° Vente", style="yellow")
                    table.add_column("Produit", style="green")
                    table.add_column("Quantité", style="blue")
                    table.add_column("Prix Total", style="red")
                    
                    for vente in ventes_marchand:
                        # Pour chaque facture, ne montrer que les lignes concernant les produits du marchand
                        lignes_marchand = [
                            ligne for ligne in vente.lignes
                            if ligne.produit.id in produits_marchand
                        ]
                        
                        for ligne in lignes_marchand:
                            table.add_row(
                                vente.date_vente.strftime('%d/%m/%Y %H:%M'),
                                vente.numero_vente,
                                ligne.produit.libelle,
                                str(ligne.quantite),
                                f"{ligne.prix_total_ligne:.2f} FCFA"
                            )
                    console.print(table)
                else:
                    print("[yellow]Aucune vente trouvée pour vos produits.[/yellow]")
                    
            elif choix == "2":
                break
            else:
                print("[bold red]Option invalide.[/bold red]")

    def afficher_statistiques(self):
        """Affiche les statistiques pour le marchand."""
        while True:
            print(Panel("[bold cyan]Statistiques[/bold cyan]"))
            print("[yellow]1.[/] Statistiques des ventes")
            print("[yellow]2.[/] Statistiques des produits")
            print("[yellow]3.[/] Retour")
            
            choix = self.input_securise("[magenta]Veuillez choisir une option (1-3): [/magenta]")
            
            if choix == "1":
                self.afficher_statistiques_ventes()
            elif choix == "2":
                self.afficher_statistiques_produits()
            elif choix == "3":
                break
            else:
                print("[bold red]Option invalide.[/bold red]")

    def afficher_statistiques_ventes(self):
        """Affiche les statistiques détaillées des ventes."""
        # Récupérer les IDs des produits du marchand
        produits_marchand = set(produit.id for produit in self.utilisateur_auth.produits)
        
        # Récupérer toutes les factures concernant les produits du marchand
        ventes_marchand = [
            vente for vente in FactureVente.objects()
            if any(ligne.produit.id in produits_marchand for ligne in vente.lignes)
        ]

        if not ventes_marchand:
            print("[yellow]Aucune vente trouvée.[/yellow]")
            return

        # Calculer les statistiques
        total_ventes = 0
        total_quantite = 0
        ventes_par_produit = {}
        
        for vente in ventes_marchand:
            for ligne in vente.lignes:
                if ligne.produit.id in produits_marchand:
                    total_ventes += ligne.prix_total_ligne
                    total_quantite += ligne.quantite
                    
                    if ligne.produit.libelle not in ventes_par_produit:
                        ventes_par_produit[ligne.produit.libelle] = {
                            'quantite': 0,
                            'montant': 0
                        }
                    ventes_par_produit[ligne.produit.libelle]['quantite'] += ligne.quantite
                    ventes_par_produit[ligne.produit.libelle]['montant'] += ligne.prix_total_ligne

        # Afficher les statistiques générales
        print(Panel("[bold cyan]Statistiques Générales des Ventes[/bold cyan]"))
        print(f"[green]Chiffre d'affaires total: {total_ventes:.2f} FCFA[/green]")
        print(f"[green]Nombre total d'articles vendus: {total_quantite}[/green]")
        print(f"[green]Nombre total de transactions: {len(ventes_marchand)}[/green]")
        
        # Afficher les statistiques par produit
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Produit", style="cyan")
        table.add_column("Quantité Vendue", style="yellow", justify="right")
        table.add_column("Montant Total", style="green", justify="right")
        table.add_column("% du CA", style="red", justify="right")

        for produit, stats in ventes_par_produit.items():
            pourcentage = (stats['montant'] / total_ventes * 100) if total_ventes > 0 else 0
            table.add_row(
                produit,
                str(stats['quantite']),
                f"{stats['montant']:.2f} FCFA",
                f"{pourcentage:.1f}%"
            )

        console.print(table)

    def afficher_statistiques_produits(self):
        """Affiche les statistiques sur l'état des stocks."""
        produits = self.utilisateur_auth.produits
        
        if not produits:
            print("[yellow]Aucun produit en stock.[/yellow]")
            return

        # Calculer les statistiques
        valeur_stock = sum(p.prix_vente * p.quantite for p in produits)
        cout_stock = sum(p.prix_achat * p.quantite for p in produits)
        marge_potentielle = valeur_stock - cout_stock

        # Afficher les statistiques générales
        print(Panel("[bold cyan]Statistiques des Stocks[/bold cyan]"))
        print(f"[green]Valeur totale du stock (prix de vente): {valeur_stock:.2f} FCFA[/green]")
        print(f"[green]Coût total du stock (prix d'achat): {cout_stock:.2f} FCFA[/green]")
        print(f"[green]Marge potentielle: {marge_potentielle:.2f} FCFA[/green]")

        # Tableau détaillé des produits
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Produit", style="cyan")
        table.add_column("Stock", style="yellow", justify="right")
        table.add_column("Valeur Stock", style="green", justify="right")
        table.add_column("Marge Unit.", style="red", justify="right")

        for produit in produits:
            marge_unitaire = produit.prix_vente - produit.prix_achat
            valeur_stock_produit = produit.prix_vente * produit.quantite
            
            table.add_row(
                produit.libelle,
                str(produit.quantite),
                f"{valeur_stock_produit:.2f} FCFA",
                f"{marge_unitaire:.2f} FCFA"
            )

        console.print(table)

    def gerer_fournisseurs(self):
        """Gestion des fournisseurs pour le marchand."""
        while True:
            print(Panel("[bold cyan]Gestion des Fournisseurs[/bold cyan]"))
            print("[yellow]1.[/] Ajouter un fournisseur")
            print("[yellow]2.[/] Lister les fournisseurs")
            print("[yellow]3.[/] Retour")
            
            choix = self.input_securise("[magenta]Veuillez choisir une option (1-3): [/magenta]")
            
            if choix == "1":
                try:
                    nom = self.input_securise("[cyan]Nom du fournisseur: [/cyan]")
                    telephone = self.input_securise("[cyan]Téléphone: [/cyan]", validation_func=self.valider_telephone)
                    email = self.input_securise("[cyan]Email: [/cyan]")
                    adresse = self.input_securise("[cyan]Adresse: [/cyan]")
                    
                    fournisseur = Fournisseur(
                        nom=nom,
                        telephone=telephone,
                        email=email,
                        adresse=adresse
                    )
                    fournisseur.save()
                    print("[bold green]Fournisseur ajouté avec succès![/bold green]")
                    
                except Exception as e:
                    print(f"[bold red]Erreur lors de l'ajout: {str(e)}[/bold red]")
                    
            elif choix == "2":
                fournisseurs = Fournisseur.objects()
                if fournisseurs:
                    for f in fournisseurs:
                        print(f"[cyan]{f.nom} (ID: {f.id})[/cyan]")
                else:
                    print("[yellow]Aucun fournisseur trouvé.[/yellow]")
                    
            elif choix == "3":
                break
            else:
                print("[bold red]Option invalide.[/bold red]")

def afficher_menu():
    """Affiche le menu principal stylisé pour MrPlenou."""
    banner = Text(
        """
    ___ ___  ____       ____  _        ___  ____    ___   __ __ 
    |   |   ||    \     |    \| |      /  _]|    \  /   \ |  |  |
    | _   _ ||  D  )    |  o  ) |     /  [_ |  _  ||     ||  |  |
    |  \_/  ||    /     |   _/| |___ |    _]|  |  ||  O  ||  |  |
    |   |   ||    \     |  |  |     ||   [_ |  |  ||     ||  :  |
    |   |   ||  .  \    |  |  |     ||     ||  |  ||     ||     |
    |___|___||__|\_|    |__|  |_____||_____||__|__| \___/  \__,_|
        """, 
        justify="center", 
        style="bold cyan"
    )

    console.print(banner)
    console.print(Panel("[bold yellow]Bienvenue sur MrPlenou[/bold yellow]", expand=False, style="blue"))

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Option", justify="center", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")

    table.add_row("1", "Demos")
    table.add_row("2", "Se connecter")
    table.add_row("3", "Analyse des données")
    table.add_row("4", "Fermer")

    console.print(table)
    
    choix = console.input("[bold white]Veuillez choisir une option (1-4) : [/bold white]")
    return choix


