# LITRevu

## Description
LITRevu est un MVP de plateforme de demande et publication de critiques de livres et d’articles, développé avec Django 5.2.

## Prérequis
- Python 3.10+  
- virtualenv ou venv  
- (facultatif) Git  

## Installation

1. **Cloner le dépôt**
   ```bash
   git clone <https://github.com/r3n3gat/projet8_LITRevu>
   cd projet8_LITRevu/litrevu
    ```

2. **Créer et activer l’environnement virtuel**
     ```bash
    python3 -m venv ../env
    source ../env/bin/activate    # macOS / Linux
    .\env\Scripts\Activate.ps1    # Windows PowerShell
      ```

3. **Installer les dépendances**
    ```bash
   pip install -r ../requirements.txt
   ```

4. **Appliquer les migrations**
    ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Charger des données de test (fixtures)**
        Si vous fournissez un fixtures/initial_data.json, lancez :
    ```bash
   python manage.py loaddata fixtures
   ```
   Sinon creez un compte superuser :
    ```bash
   python manage.py createsuperuser
     ```
6. **Lancer le serveur de développement**
    ```bash
   python manage.py runserver

   ```

## Accès

- **Site** : http://127.0.0.1:8000/  
- **Admin** : http://127.0.0.1:8000/admin/  

---

## Utilisation

- **Inscription / Connexion**  
  - `/accounts/signup/`  
  - `/accounts/login/`  
- **CRUD Tickets**  
  - `/reviews/`  
- **CRUD Reviews**  
  - via les liens depuis chaque ticket  
- **Suivi d’utilisateurs**  
  - `/reviews/follows/`  
- **Fil d’actualité**  
  - `/reviews/`  

---

## Tests

Pour exécuter la suite de tests unitaires :

```bash
python manage.py test
   ```
---

## Contenu du dépôt
```bash
projet8_LITRevu/
├── docs/                  # wireframes, cahier des charges…
├── env/                   # venv (ignoré par .gitignore)
├── litrevu/               # dossier racine du projet Django
│   ├── accounts/          # app gestion de l’authentification et profils
│   ├── core/              # app pages statiques (home, about…)
│   └── litrevu            # package racine du projet 
│   ├── reviews/           # app Tickets & Reviews (fonctionnalités principales)
│   └── scripts/           # scripts utilitaires (ex. nettoyage de fixtures)
│   └── static             # fichiers statiques communs (CSS, images…)
│   └── templates          # templates globaux (layout, includes partagés)
│   └── manage.py          # point d’entrée CLI Django
├── fixtures/              # (facultatif) jeux de données
├── db.sqlite3             # base SQLite avec données de test
├── README.md              # ce fichier de documentation
├── requirements.txt       # liste des dépendances pip
└── .gitignore             # fichiers/dossiers ignorés par Git

   ```

## Pages principales

Accueil / Fil d’actualité : http://127.0.0.1:8000/reviews/

Vos posts (tickets & critiques) : http://127.0.0.1:8000/reviews/posts/

Suivis : http://127.0.0.1:8000/reviews/follows/

Profil utilisateur : http://127.0.0.1:8000/accounts/profile/

Inscription : http://127.0.0.1:8000/accounts/signup/

Connexion : http://127.0.0.1:8000/accounts/login/

## Compte de démonstration

Nom d’utilisateur : stevi

Mot de passe : 123azerty321


## Export de la veille au format PDF
Si votre veille est en Markdown (docs/veille.md) :

```bash
    cd docs
pandoc veille.md -o veille.pdf
   ```

## Publication sur GitHub
Initialiser (si nécessaire) :
```bash
    git add .
git commit -m "Version finale : documentation, fixtures et veille PDF"
git push -u origin main

   ```
Vérifier : Que env/, db.sqlite3 (ou autres fichiers sensibles) sont bien dans .gitignore.

```bash
   ```
## Ajouter et publier 
```bash
    git add .
git commit -m "Version finale : documentation, fixtures et veille PDF"
git push -u origin main

   ```

```bash
   ```