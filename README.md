# Générateur de Cahiers des Charges

## 📋 Description

Ce projet Python permet de générer automatiquement des cahiers des charges (CDC) pour vos projets. Il propose deux modes d'utilisation :
- **Mode CLI** : Interface en ligne de commande pour collecter les informations projet
- **Mode GUI** : Interface graphique avec PySide6 pour une expérience utilisateur améliorée

Le projet utilise le pattern **Builder** pour construire progressivement les objets Project et peut communiquer avec un webhook distant pour traiter les données collectées.

## 🚀 Fonctionnalités

- **Structure de données complète** : Collecte d'informations détaillées sur le projet (meta, contexte, objectifs, cibles, périmètre, livrables, contraintes, timeline, gouvernance, budget, critères d'acceptation, risques)
- **Pattern Builder** : Architecture propre et maintenable pour construire les objets Project
- **Affichage formaté** : Méthode `describe()` pour visualiser toutes les informations du projet
- **Sérialisation JSON** : Méthode `to_dict()` pour convertir facilement les données en JSON
- **Interface CLI** : Collection interactive d'informations via terminal
- **Interface GUI** : Interface moderne avec PySide6 (en développement)
- **Communication webhook** : Envoi des données structurées à un webhook distant
- **Authentification sécurisée** : Via clé API
- **Configuration via variables d'environnement**

## 📦 Prérequis

- Python 3.7+
- pip (gestionnaire de paquets Python)

## 🔧 Installation

1. Clonez le dépôt :
```bash
git clone <url-du-repo>
cd cdc_generator
```

2. Créez un environnement virtuel (recommandé) :
```bash
python -m venv .venv
```

3. Activez l'environnement virtuel :
   - Windows (PowerShell) :
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
   - Windows (CMD) :
   ```cmd
   .venv\Scripts\activate.bat
   ```
   - Linux/Mac :
   ```bash
   source .venv/bin/activate
   ```

4. Installez les dépendances :
```bash
# Pour le mode CLI uniquement
pip install requests python-dotenv

# Pour le mode GUI (interface PySide6)
pip install requests python-dotenv PySide6
```

## ⚙️ Configuration

1. Créez un fichier `.env` à la racine du projet :
```bash
N8N_WEBHOOK_URL=https://votre-webhook-url.com
API-KEY-CDC=votre_cle_api_ici
```

2. Remplacez les valeurs par vos informations de webhook.

## 🎯 Utilisation

### Mode CLI (Interface en ligne de commande)

```bash
python main.py
```

Le script vous guidera à travers une série de questions pour collecter toutes les informations nécessaires au cahier des charges.

### Mode GUI (Interface graphique)

```bash
python main_test.py
```

Lance l'interface graphique PySide6 avec navigation par pages.

### Structure du projet

```
cdc_generator/
│
├── main.py                     # Point d'entrée CLI
├── main_test.py                # Point d'entrée GUI (PySide6)
├── models/                     # Modèles de données et builders
│   ├── __init__.py
│   ├── Project.py              # Classe Project avec describe() et to_dict()
│   ├── projectBuilder.py       # Pattern Builder (abstrait et concret)
│   └── projectBuilderDirector.py  # Director pour orchestrer la construction
├── pages/                      # Pages de l'interface GUI
│   ├── __init__.py
│   ├── meta_page.py
│   ├── context_page.py
│   └── objectives_page.py
├── utils/                      # Fonctions utilitaires
│   ├── __init__.py
│   └── utils.py
├── .env                        # Variables d'environnement (non versionné)
├── .gitignore                  # Fichiers à ignorer par Git
└── README.md                   # Documentation
```

## 📝 Exemple d'utilisation

### Utilisation de la classe Project

```python
from models.projectBuilder import ConcreteProjectBuilder
from models.projectBuilderDirector import ProjectBuilderDirector

# Initialiser le builder et le director
director = ProjectBuilderDirector(ConcreteProjectBuilder())

# Construire les métadonnées
project = director.construct_meta({
    "client_name": "Client XYZ",
    "project_name": "Application Mobile",
    "entreprise_name": "Entreprise ABC",
    "author": "Votre Nom",
    "version": "1.0",
    "created_at": "2025-12-20"
})

# Construire le contexte
project = director.construct_context({
    "trigger": "Besoin d'une application mobile",
    "current_state": "Aucune solution existante",
    "stakes": ["Augmenter la visibilité", "Améliorer l'expérience client"]
})

# Construire les objectifs
project = director.construct_objectives([
    "Développer une application mobile iOS et Android",
    "Intégrer un système de paiement sécurisé"
])

# Afficher le projet
project.describe()

# Convertir en JSON pour envoi
import requests
response = requests.post(
    webhook_url,
    json=project.to_dict(),
    headers={"API-KEY-CDC": api_key}
)
```

### Accéder au projet en cours de construction

```python
# Récupérer le projet avant le build final
current_project = director._builder.get_project()
print(current_project.to_dict())
```

## 🔐 Sécurité

- ⚠️ **Important** : Ne jamais committer le fichier `.env` contenant vos clés API
- Le fichier `.env` est déjà ajouté au `.gitignore` pour éviter tout commit accidentel
- Gardez vos clés API confidentielles

## 🛠️ Développement

### Architecture - Pattern Builder

Le projet utilise le **pattern Builder** pour construire progressivement les objets `Project` :

- `Project` : Classe de données contenant tous les attributs du cahier des charges
- `ProjectBuilder` : Interface abstraite définissant les méthodes de construction
- `ConcreteProjectBuilder` : Implémentation concrète du builder
- `ProjectBuilderDirector` : Orchestre la construction avec des méthodes de haut niveau

### Méthodes de la classe Project

#### `describe()`
Affiche une description complète et formatée du projet dans la console avec tous les détails structurés par sections.

```python
project.describe()
```

#### `to_dict()`
Convertit l'objet Project en dictionnaire Python pour la sérialisation JSON.

```python
project_dict = project.to_dict()
# Peut être utilisé directement avec requests.post(json=project_dict)
```

### Méthodes du ConcreteProjectBuilder

#### `get_project()`
Retourne l'instance actuelle du projet en cours de construction sans finaliser le build.

```python
current_project = builder.get_project()
```

#### `build()`
Finalise et retourne le projet construit.

```python
final_project = builder.build()
```

### Ajout de nouveaux modèles

Ajoutez vos classes de modèles dans le dossier `models/` :

```python
# models/nouvelle_entite.py
class NouvelleEntite:
    def __init__(self, titre, description):
        self.titre = titre
        self.description = description
```

### Ajout de fonctions utilitaires

Ajoutez vos fonctions utilitaires dans le dossier `utils/` :

```python
# utils/helpers.py
def formater_donnees(data):
    # Votre logique ici
    return formatted_data
```

### Ajout de nouvelles pages GUI

Pour ajouter une page à l'interface PySide6 :

1. Créez un fichier dans `pages/` (ex: `new_page.py`)
2. Implémentez les méthodes `get_data()` et `set_data()`
3. Ajoutez la page dans `main_test.py`

```python
# pages/new_page.py
from PySide6.QtWidgets import QWidget, QVBoxLayout

class NewPage(QWidget):
    def __init__(self):
        super().__init__()
        # Votre UI ici
    
    def get_data(self):
        # Retourner les données du formulaire
        return {}
    
    def set_data(self, data):
        # Charger les données dans le formulaire
        pass
```

## 📋 Dépendances

- `requests` : Pour les requêtes HTTP vers le webhook
- `python-dotenv` : Pour gérer les variables d'environnement
- `PySide6` : Pour l'interface graphique (optionnel, mode GUI uniquement)

## ⚡ Méthodes du ProjectBuilderDirector

Chaque méthode `construct_*()` prend un dictionnaire ou une liste en paramètre et met à jour le projet :

- `construct_meta(meta: dict)` : Métadonnées du projet
- `construct_context(context: dict)` : Contexte et enjeux
- `construct_objectives(objectives: list)` : Liste des objectifs
- `construct_targets(targets: dict)` : Cibles primaires, secondaires et parcours utilisateur
- `construct_scope(scope: dict)` : Périmètre (inclus, exclus)
- `construct_deliverables(deliverables: list)` : Liste des livrables
- `construct_constraints(constraints: dict)` : Contraintes du projet
- `construct_timeline(timeline: list)` : Planning et jalons
- `construct_governance(governance: dict)` : Gouvernance et contacts
- `construct_budget(budget: dict)` : Budget et arbitrages
- `construct_acceptance(acceptance: dict)` : Critères d'acceptation
- `construct_risks(risks: list)` : Liste des risques

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Forker le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commiter vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Pousser vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## 📞 Support

Pour toute question ou problème, n'hésitez pas à ouvrir une issue sur le dépôt GitHub.

---

**Note** : Ce projet est en développement actif. Les fonctionnalités et l'API peuvent évoluer.