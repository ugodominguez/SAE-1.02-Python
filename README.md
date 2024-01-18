# SAE-1.02-Python

### Exemple de plateau
```python
{
'nb_lignes': 20,
'nb_colonnes': 30, 
'nb_joueurs': 5, 
'nb_fantomes': 5, 
'cases': [
          [case, case, case, ...],
          [case, case, case, ...],
          ],
'joueurs': {'A': (1, 2), 'B': (1, 22)},
'fantomes': {'a': (7, 5), 'b': (10, 1), 'c': (10, 12)}
}
```

### Exemple de case
```python
{
'mur': False,
'objet': '&',
'pacmans_presents': {'A','B'},
'fantomes_presents': {'a','b','c'}
}
```

### Exemple de joueur
```python
{
'couleur': 'A',
'nom': 'tom',
'nb_points': 53, 
'nb_faux_mvt': 2,  
'pos_pacman': (12,27), 
'pos_fantome': (2,14), 
'objets': {const.GLOUTON: 3, const.IMMOBILITE: 0, const.PASSEMURAILLE: 1}
}
```

### Lancer le jeu
```bash
python3 affichage.py&
python3 ia_tom.py --equipe Tom&
python3 ia_classique.py --equipe J2&
python3 ia_classique.py --equipe J3&
python3 ia_classique.py --equipe J4&
```

```bash
py .\affichage.py
py .\ia_tom.py --equipe Tom
py .\ia_classique.py --equipe J2
py .\ia_classique.py --equipe J3
py .\ia_classique.py --equipe J4
```
