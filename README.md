# Reproductibilité et variabilité
Travail réalisé par Jason EL KHOURY en 5INFO.
Ce dépôt regroupe tous le travail réalisé lors des TP1,2 et 3 en REP. 

## Hiérarchie du dépôt

```
.
│
├── .github/
|     ├── experiments.yml           # Workflow GitHub Actions du lab #3
|     ├── reproduce.yml             # Workflow GitHub Actions du lab #1            
├── llm/                            # Programmes générés par les LLM (lab #2)
│   ├── L1/
│   │   ├── AssociativityTest.py    # Programme d'associativité généré en Python
│   │   ├── answer_associativity_llm.txt # résultat généré par le programme
│   │   └── LLM_associativity.md    # Prompt et informations sur la génération
│   │
│   └── L2/
│       ├── AssociativityTest.java  # Programme d'associativité généré en Java
│       ├── AssociativityTest.class # Fichier compilé
│       ├── BankingLLM.java         # Programme de banking généré en Java
│       ├── BankingLLM.class        # Fichier compilé
│       ├── answer_associativity_llm.txt # résultat généré par le programme
│       ├── answer_banking_llm.txt # résultat généré par le programme de banking
│       ├── Dockerfile.llm          # Environnement Docker pour les programmes Java
│       ├── LLM_associativity.md    # Prompt et informations sur la génération
│       └── LLM_banking.md          # Prompt et informations sur la génération
│
├── part3.1/                        # Exploration par paramètres à l'exécution
│   └── runtime_parameters.py       # Variation du nombre de répétitions
|    └── answer_associativity_runtime_parameters.txt 
│
├── part3.2/                        # Exploration via une interface en ligne de commande
│   ├── cli.py                      # Programme configurable avec des arguments CLI
│   └── answer_associativity_cli.txt
│
├── part3.3/                        # Génération automatique avec des templates
│   ├── generate.py                 # Génération et exécution des variantes
│   └── generated/                  # Programmes générés automatiquement
│       ├── AssociativityAddFloat32.java
│       ├── AssociativityAddFloat64.java
│       ├── DistributivityFloat32.java
│       ├── DistributivityFloat64.java
│       ├── associativity_add_float32.py
│       ├── associativity_add_float64.py
│       ├── distributivity_float32.py
│       └── distributivity_float64.py
│
├── part3.4/                        # Variation de l'environnement d'exécution
│   ├── cpython.txt                 # Résultats avec CPython
│   └── pypy.txt                    # Résultats avec PyPy
│
├── part6/                          # Exécution automatisée des configurations
│   ├── build_docker_images.py      # Construction des images Docker
│   ├── run_experiments.py          # Exécution des configurations échantillonnées
│   ├── generated/                  # Programmes générés pour les expériences
│   └── results.csv                 # Résultats des expériences
│
├── part7/                          # Reproductibilité avec GitHub Actions
│   └── results.csv                 # Résultats fusionnés des différents runners
│
├── part8/                          # Analyse et expériences de causalité
│   ├── results_analysis.ipynb      # Analyse des résultats et recommandations
│   ├── interval_causality.uvl      # Modèle de variabilité pour l'expérience sur l'intervalle
│   ├── interval_causality.csv      # Configurations de l'expérience sur l'intervalle
│   ├── interval_causality_results.csv # Résultats de l'expérience sur l'intervalle
│   ├── generated_interval_causality/ # Programmes générés pour tester l'effet de l'intervalle
│   ├── numeric_precision_causality.uvl # Modèle de variabilité pour la précision numérique
│   ├── numeric_precision_causality_results.csv # Résultats de l'expérience sur la précision
│   └── generated_numeric_precision/ # Programmes générés pour tester l'effet de la précision
│
├── configs/                        # Configurations incluses dans l'échantillonnage
│   ├── program1.csvconf            # Configuration du programme initial
│   ├── program2.csvconf            # Configuration du programme LLM en L2
│   ├── program3.csvconf            # Configuration du programme LLM en L1
│   └── sample.csv                  # Échantillon de configurations généré pour la partie 6
│
├── fm/
│   └── experiment.uvl              # Feature model principal des facteurs de variabilité
│
│
├── tp1.py                          # Programme initial écrit à la main (lab #1)
├── answer_associativity.txt       # Résultats du programme d'associativité initial
├── answer_banking.txt             # Résultats du programme de banking
├── Dockerfile                      # Définition de l'environnement Docker principal
├── property_template.py.jinja      # Template Python pour générer les variantes
├── property_template.java.jinja    # Template Java pour générer les variantes
├── sample.py                       # Génération reproductible d'un échantillon de configurations
├── shell.nix                       # Environnement Nix du lab #1
├── nixpkgs-pin.nix                 # Version de nixpkgs utilisée pour figer l'environnement
├── README.md                       # Présentation du projet et instructions de reproduction
└── LICENSE                         # Licence du projet
```

## Reproduction des résultats

Cette section présente les commandes nécessaires pour reproduire les résultats obtenus au cours des différentes parties du TP.

### 1. Préparation de l'environnement

Commencer par créer un environnement virtuel Python et installer les bibliothèques utilisées :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas seaborn flamapy==2.6.0 Jinja2 numpy
```

### 2. Programmes du TP1 et programmes générés par un LLM

Pour exécuter le programme principal du TP1 ([`tp1.py`](tp1.py)) ainsi que les programmes générés par le LLM (dans le dossier [`llm`](llm/)), il suffit de lancer les commandes suivantes :

```bash
python3 tp1.py
python3 llm/L1/AssociativityTest.py

cd llm/L2
javac AssociativityTest.java
java AssociativityTest

javac BankingLLM.java
java BankingLLM
```

### 3. Variation du nombre de répétitions

Le script [`runtime_parameters.py`](part3.1/runtime_parameters.py) permet d'étudier l'influence du nombre de répétitions sur le résultat.
Pour observer la variation des résultats en fonction du nombre de répétitions, exécuter :

```bash
python3 part3.1/runtime_parameters.py
```
Les résultats seront affichés dans le fichier [`answer_associativity_runtime_parameters.txt`](part3.1/answer_associativity_runtime_parameters.txt)

### 4. Exécution avec des paramètres en ligne de commande

Pour étudier la variation des résultats en fonction des différents paramètres configurables en ligne de commande, exécuter :

```bash
python3 part3.2/cli.py --repetitions [REPETITIONS] --seed [SEED] --min-value [MIN_VALUE] --max-value [MAX_VALUE]
```

Les valeurs entre crochets sont à remplacer par les valeurs souhaitées.

### 5. Génération des programmes avec Jinja2

La génération des programmes Python et Java permettant de tester l'associativité et la distributivité avec des nombres en précision 32 bits et 64 bits repose sur les templates Jinja2.

Pour générer ces programmes, exécuter :

```bash
python3 part3.3/generate.py
```

Les programmes générés sont disponibles dans le dossier [`part3.3/generated`](part3.3/generated/).

### 6. Génération et exécution des configurations (parties 6 et 7)

Le feature model principal, utilisé pour générer les différentes configurations des parties 6 et 7, est disponible dans [`fm/experiment.uvl`](fm/experiment.uvl).

Pour effectuer le sampling à partir de ce feature model et générer 30 configurations, exécuter :

```bash
python3 sample.py fm/experiment.uvl --size 30 --seed 1 -o configs/sample.csv
```

Avant d'exécuter les configurations, il faut construire les images Docker qui permettront de lancer chaque programme dans son environnement d'exécution :

```bash
python3 part6/build_docker_images.py
```

Une fois les images construites et les configurations générées, on peut lancer les expériences avec :

```bash
python3 part6/run_experiments.py \
    --sample configs/sample.csv \
    --generated-dir part6/generated \
    --results part6/results.csv
```

Les programmes correspondant aux différentes configurations sont générés dans [`part6/generated`](part6/generated/). Les résultats, qui associent chaque configuration à ses différents paramètres et au pourcentage obtenu, sont enregistrés dans [`part6/results.csv`](part6/results.csv).

Chaque configuration est exécutée trois fois afin de vérifier la stabilité des résultats pour une même configuration.

Le workflow GitHub Actions défini dans [`.github/workflows/experiments.yml`](.github/workflows/experiments.yml) reproduit cette expérience sur deux architectures CPU : `ubuntu-24.04` et `ubuntu-24.04-arm`.

Les résultats obtenus sont regroupés dans [`part7/results.csv`](part7/results.csv).

Pour consulter l'analyse de ces résultats, voir le notebook [`part8/results_analysis.ipynb`](part8/results_analysis.ipynb).

### 7. Étude de la causalité : précision numérique et intervalle (partie 8)

Dans cette partie, deux nouveaux feature models ont été créés afin d'étudier séparément l'effet causal de la précision numérique et celui de l'intervalle sur les résultats. Chaque feature model permet de faire varier uniquement le facteur étudié, en maintenant les autres paramètres constants.

**Étude de l'effet de la précision numérique**

Générer les configurations à partir du feature model [`numeric_precision_causality.uvl`](part8/numeric_precision_causality.uvl) :

```bash
python3 sample.py part8/numeric_precision_causality.uvl --size 30 --seed 1 -o part8/numeric_precision_causality.csv
```

Puis exécuter les expériences :

```bash
python3 part6/run_experiments.py \
    --sample part8/numeric_precision_causality.csv \
    --generated-dir part8/generated_numeric_precision \
    --results part8/numeric_precision_causality_results.csv
```

**Étude de l'effet de l'intervalle**

Générer les configurations à partir du feature model [`interval_causality.uvl`](part8/interval_causality.uvl) :

```bash
python3 sample.py part8/interval_causality.uvl --size 30 --seed 1 -o part8/interval_causality.csv
```

Puis exécuter les expériences :

```bash
python3 part6/run_experiments.py \
    --sample part8/interval_causality.csv \
    --generated-dir part8/generated_interval_causality \
    --results part8/interval_causality_results.csv
```

Les résultats de ces deux études sont enregistrés respectivement dans [`numeric_precision_causality_results.csv`](part8/numeric_precision_causality_results.csv) et [`interval_causality_results.csv`](part8/interval_causality_results.csv). Leur analyse est également disponible dans le notebook [`results_analysis.ipynb`](part8/results_analysis.ipynb).
