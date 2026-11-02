# Associativité des nombres flottants et problème bancaire




## 1. Expérience 1 — Associativité

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


## 2. Expérience 2 — Problème bancaire

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


### Résultats attendus

Le fichier `answer_banking.txt` doit contenir :

```text
Initial balance: 2.718281828459045235360287471352662497757247093699959574966967627724076630353547594571382178525166427
Number of years: 50
Decimal precision: 100 digits
Final balance: 0.019992165836667903219891152066054769364655840492696650225231297366847604012802191130624000000000000
```


## 3. Automatisation avec GitHub Actions
Les résultats des deux expériences sont générés automatiquement par un workflow GitHub Actions défini dans .github/workflows/reproduce.yml.

À chaque push sur une branche du dépôt, le workflow :

1. Récupère le code source.

2. Construit l'image Docker à partir du Dockerfile.

3. Exécute le programme Python dans un conteneur.

4. Génère answer_associativity.txt et answer_banking.txt.

5. Enregistre et pousse les fichiers de résultats dans le dépôt si leur contenu a changé.


## Reproduire les résultats avec Nix

# Lab3 : Comparaison des résultats 

## Matrice de comparaison

| Mesure | Programme 1 : Python original | Programme 2 : Java généré par LLM | Programme 3 : Python généré par LLM |
|---|---:|---:|---:|
| Nombre de tests  | 1 000 | 1 000 000 | 1 000 000 |
| Cas où les résultats sont égaux | 825 | 930 671 | 930 720 |
| Cas où les résultats sont différents | 174 | 69 329 | 69 280 |
| Pourcentage d'égalité | 82,5 % | 93,0671 % | 93,0720 % |
| Graine aléatoire | 152 | 42 | 42 |
| Intervalle des valeurs générées | \([0,1]\) | \([-10^6,10^6)\) | \([-10^6,10^6)\) |
| Type numérique | `float` Python | `double` Java | `float` Python |

