# Dossier Technique - WheelShare

## 1. Architecture Système

### 1.1 Vue d'ensemble
```
WheelShare/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/
│   │   ├── components/
│   │   └── pages/
│   └── models/
├── main.py
├── requirements.txt
└── .env
```

### 1.2 Technologies Utilisées
- **Backend**: Python 3.12, Flask
- **Base de données**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Sécurité**: Flask-Session, Werkzeug
- **Dépendances**: Voir requirements.txt

## 2. Structure de la Base de Données

### 2.1 Schéma de la Base de Données
```sql
-- Utilisateurs
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trajets
CREATE TABLE trips (
    id INTEGER PRIMARY KEY,
    driver_id INTEGER,
    from_location TEXT NOT NULL,
    to_location TEXT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    price_per_seat REAL NOT NULL,
    available_seats INTEGER NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (driver_id) REFERENCES users(id)
);

-- Réservations
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY,
    trip_id INTEGER,
    user_id INTEGER,
    seats INTEGER NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 3. API Endpoints

### 3.1 Authentification
- `POST /register` - Inscription utilisateur
- `POST /login` - Connexion
- `GET /logout` - Déconnexion

### 3.2 Trajets
- `GET /trips` - Liste des trajets
- `GET /trip/<id>` - Détails d'un trajet
- `POST /trips/new` - Création d'un trajet
- `POST /trip/<id>/cancel` - Annulation d'un trajet

### 3.3 Réservations
- `GET /bookings` - Liste des réservations
- `POST /trip/<id>/book` - Création d'une réservation
- `POST /booking/<id>/cancel` - Annulation d'une réservation

## 4. Sécurité

### 4.1 Authentification
- Hachage des mots de passe avec Werkzeug
- Sessions sécurisées avec Flask-Session
- Protection CSRF

### 4.2 Validation des Données
- Validation des entrées utilisateur
- Protection contre les injections SQL
- Sanitization des données

## 5. Performance

### 5.1 Optimisations
- Mise en cache des sessions
- Indexation de la base de données
- Optimisation des requêtes SQL

### 5.2 Monitoring
- Logs d'erreurs
- Métriques de performance
- Suivi des sessions

## 6. Déploiement

### 6.1 Prérequis
- Python 3.12+
- pip
- virtualenv

### 6.2 Installation
```bash
# Création de l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installation des dépendances
pip install -r requirements.txt

# Configuration
cp .env.example .env
# Éditer .env avec les configurations

# Lancement
python main.py
```

## 7. Maintenance

### 7.1 Sauvegarde
- Sauvegarde quotidienne de la base de données
- Versioning du code
- Documentation des changements

### 7.2 Mises à Jour
- Procédure de mise à jour
- Tests de compatibilité
- Plan de rollback

## 8. Tests

### 8.1 Tests Unitaires
- Tests des modèles
- Tests des routes
- Tests des utilitaires

### 8.2 Tests d'Intégration
- Tests des workflows
- Tests de performance
- Tests de sécurité 