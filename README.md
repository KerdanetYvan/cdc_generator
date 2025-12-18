# Générateur de Cahiers des Charges

## 📋 Description

Ce projet Python permet de générer automatiquement des cahiers des charges (CDC) en communiquant avec un webhook distant. Il facilite la création et la gestion de spécifications techniques pour vos projets.

## 🚀 Fonctionnalités

- Communication avec un webhook pour générer des cahiers des charges
- Authentification sécurisée via clé API
- Support de l'envoi de données structurées au format JSON
- Configuration via variables d'environnement

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
pip install requests python-dotenv
```

## ⚙️ Configuration

1. Créez un fichier `.env` à la racine du projet :
```bash
API-KEY-CDC=votre_cle_api_ici
```

2. Remplacez `votre_cle_api_ici` par votre clé API fournie par le service de webhook.

## 🎯 Utilisation

### Exécution basique

```bash
python main.py
```

### Structure du projet

```
cdc_generator/
│
├── main.py              # Point d'entrée principal
├── models/              # Modèles de données
│   └── __init__.py
├── utils/               # Fonctions utilitaires
│   └── __init__.py
├── .env                 # Variables d'environnement (non versionné)
├── .gitignore          # Fichiers à ignorer par Git
└── README.md           # Documentation
```

## 📝 Exemple d'utilisation

Le script `main.py` envoie une requête POST au webhook avec les données suivantes :

```python
json = {
    "id": "1234",  # Identifiant du projet
}
```

Vous pouvez modifier ces données selon vos besoins pour générer différents types de cahiers des charges.

## 🔐 Sécurité

- ⚠️ **Important** : Ne jamais committer le fichier `.env` contenant vos clés API
- Le fichier `.env` est déjà ajouté au `.gitignore` pour éviter tout commit accidentel
- Gardez vos clés API confidentielles

## 🛠️ Développement

### Ajout de nouveaux modèles

Ajoutez vos classes de modèles dans le dossier `models/` :

```python
# models/cahier_charges.py
class CahierCharges:
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

## 📋 Dépendances

- `requests` : Pour les requêtes HTTP
- `python-dotenv` : Pour gérer les variables d'environnement

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