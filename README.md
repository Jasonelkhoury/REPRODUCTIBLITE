# Associativité des nombres flottants et problème bancaire

## 1. Description

Ce projet contient deux expériences réalisées en Python 3 :

- **Expérience 1 — Associativité :** mesurer la proportion de cas où \((x+y)+z = x+(y+z)\) pour des nombres flottants générés aléatoirement.
- **Expérience 2 — Problème bancaire :** calculer le solde final après 50 ans en utilisant le type `Decimal` pour limiter les erreurs d'arrondi.

Les résultats de chaque expérience sont enregistrés dans un fichier texte.


## 2. Exécution

Depuis le répertoire contenant `tp1.py`, exécuter :

```bash
python3 tp1.py
```

Le programme crée ou remplace les fichiers suivants dans le répertoire de travail courant :

- `answer_associativity.txt`
- `answer_banking.txt`


## 5. Expérience 1 — Associativité

### Choix expérimentaux

| Paramètre | Valeur |
|---|---|
| Langage | Python 3 |
| Type numérique | `float` |
| Nombre de tests annoncé | 1 000 |
| Valeurs minimales et maximales | 0 et 1 |
| Générateur | `random.uniform(0, 1)` |
| Graine aléatoire | `152` |


### Résultats attendus

Le fichier `answer_associativity.txt` doit contenir :

```text
Number of tests: 1000
Equal results: 825
Different results: 174
Percentage of equality: 82.500000%
```


## 6. Expérience 2 — Problème bancaire

### Choix expérimentaux

| Paramètre | Valeur |
|---|---|
| Langage | Python 3 |
| Type numérique | `Decimal` |
| Solde initial | \(e\), calculé avec `Decimal(1).exp()` |
| Durée | 50 ans |
| Frais annuels | 1 € |
| Frais de retrait final | 1 € |
| Précision décimale | 100 chiffres significatifs |

Le solde initial est calculé à partir de l'exponentielle de 1 :

### Résultats attendus

Le fichier `answer_banking.txt` doit contenir :

```text
Initial balance: 2.718281828459045235360287471352662497757247093699959574966967627724076630353547594571382178525166427
Number of years: 50
Decimal precision: 100 digits
Final balance: 0.019992165836667903219891152066054769364655840492696650225231297366847604012802191130624000000000000
```


## 7. Reproductibilité

Pour reproduire les expériences :

1. Cloner ou télécharger le dépôt.
2. Vérifier que Python 3 est installé.
3. Exécuter `python3 tp1.py`.
4. Comparer les fichiers générés avec les résultats attendus présentés dans ce README.

Pour l'expérience sur l'associativité, la graine aléatoire doit rester fixée à `152` et les paramètres de génération doivent être conservés.

Pour l'expérience bancaire, les paramètres, l'ordre des opérations et la précision doivent rester identiques.



