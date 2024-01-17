# coding: utf-8
"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module client_joueur.py
        Ce module contient le programme principal d'un joueur
        il s'occupe des communications avec le serveur
            - envois des ordres
            - recupération de l'état du jeu
        la fonction mon_IA est celle qui contient la stratégie de
        jeu du joueur.

"""
import argparse
import random
import client
import const
import plateau
import case
import joueur

prec='X'

def mon_IA(ma_couleur, carac_jeu, plan, les_joueurs):
    """ Cette fonction permet de calculer les deux actions du joueur de couleur ma_couleur
        en fonction de l'état du jeu décrit par les paramètres. 
        Le premier caractère est parmi XSNOE X indique pas de peinture et les autres
        caractères indique la direction où peindre (Nord, Sud, Est ou Ouest)
        Le deuxième caractère est parmi SNOE indiquant la direction où se déplacer.

    Args:
        ma_couleur (str): un caractère en majuscule indiquant la couleur du jeur
        carac_jeu (str): une chaine de caractères contenant les caractéristiques
                                   de la partie séparées par des ;
             duree_act;duree_tot;reserve_init;duree_obj;penalite;bonus_touche;bonus_rechar;bonus_objet           
        plan (str): le plan du plateau comme comme indiqué dans le sujet
        les_joueurs (str): le liste des joueurs avec leur caractéristique (1 joueur par ligne)
        couleur;reserve;nb_cases_peintes;objet;duree_objet;ligne;colonne;nom_complet
    
    Returns:
        str: une chaine de deux caractères en majuscules indiquant la direction de peinture
            et la direction de déplacement
    """

    # decodage des informations provenant du serveur
    joueurs = {}

    for ligne in les_joueurs.split('\n'):
        lejoueur = joueur.joueur_from_str(ligne)
        joueurs[joueur.get_couleur(lejoueur)] = lejoueur

    le_plateau = plateau.Plateau(plan)


    def get_analyse(pos):
        directions = plateau.directions_possibles(le_plateau, pos)
        res = dict()

        for card in directions:
            res[card] = plateau.analyse_plateau(le_plateau, pos, card, plateau.get_nb_lignes(le_plateau))

        return res
    

    def suivre_ou_fuir(glouton):
        """va vers le pacman le plus proche s'il n'a pas de glouton
        s'il en a un, le fantome va fuir

        Args:
            glouton (bool): si le pacman est glouton

        Returns:
            str: la direction à prendre
        """

        pos_fantome = joueur.get_pos_fantome(joueurs[ma_couleur])
        analyse = get_analyse(pos_fantome)

        func = max if glouton else min
        direction_pacman = func(analyse, key = lambda direct: analyse[direct]["pacmans"])

        return random.choice("NOSE") if direction_pacman is None else direction_pacman
    

    def prendre_objets():

        pos_pacman = joueur.get_pos_pacman(joueurs[ma_couleur])
        analyse = get_analyse(pos_pacman)

        direction_pacman = min(analyse, key = lambda direct: analyse[direct]["objets"])

        return random.choice("NOSE") if direction_pacman is None else direction_pacman
    

    # IA complètement aléatoire
    dir_p = plateau.deplacement(le_plateau,joueur.get_pos_pacman(joueurs[ma_couleur]),joueurs[ma_couleur])
    dir_f = suivre_ou_fuir(False)

    #plateau.analyse_plateau(le_plateau, )

    return dir_p + dir_f


if __name__=="__main__":
    parser = argparse.ArgumentParser()  
    parser.add_argument("--equipe", dest="nom_equipe", help="nom de l'équipe", type=str, default='Non fournie')
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)
    
    args = parser.parse_args()
    le_client=client.ClientCyber()
    le_client.creer_socket(args.serveur,args.port)
    le_client.enregistrement(args.nom_equipe,"joueur")
    ok=True
    while ok:
        ok,id_joueur,le_jeu=le_client.prochaine_commande()
        if ok:
            carac_jeu,le_plateau,les_joueurs=le_jeu.split("--------------------\n")
            actions_joueur=mon_IA(id_joueur,carac_jeu,le_plateau,les_joueurs[:-1])
            le_client.envoyer_commande_client(actions_joueur)
            # le_client.afficher_msg("sa reponse  envoyée "+str(id_joueur)+args.nom_equipe)
    le_client.afficher_msg("terminé")

