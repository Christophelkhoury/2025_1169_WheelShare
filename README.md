# WheelShare 🚗

WheelShare est une plateforme de covoiturage moderne et intuitive qui permet aux conducteurs et aux passagers de se connecter facilement pour partager des trajets.

## 🌟 Fonctionnalités

- **Inscription et Connexion**
  - Création de compte pour conducteurs et passagers
  - Authentification sécurisée
  - Gestion des profils utilisateurs

- **Pour les Conducteurs**
  - Création de trajets
  - Gestion des réservations
  - Suivi des revenus
  - Communication avec les passagers

- **Pour les Passagers**
  - Recherche de trajets
  - Réservation de places
  - Suivi des réservations
  - Messagerie avec les conducteurs

## 🛠️ Technologies Utilisées

- **Backend**
  - Python 3.12
  - Flask
  - Flask-Session
  - SQLite

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript
  - Font Awesome

## 🚀 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/Christophelkhoury/WheelShare.git
cd WheelShare
```

2. Créez un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurez les variables d'environnement :
```bash
cp .env.example .env
# Modifiez le fichier .env avec vos configurations
```

5. Lancez l'application :
```bash
python main.py
```

## 🔧 Configuration

L'application utilise les variables d'environnement suivantes :
- `SECRET_KEY` : Clé secrète pour la session Flask
- `SESSION_TYPE` : Type de stockage de session (filesystem)

## 📱 Interface Utilisateur

- Design moderne et responsive
- Navigation intuitive
- Thème sombre par défaut
- Animations fluides
- Messages de notification en temps réel

## 🔒 Sécurité

- Authentification sécurisée
- Protection contre les injections SQL
- Gestion des sessions
- Validation des données

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

- Christophe EL Khoury - Développeur Principal

## 🙏 Remerciements

- Tous les contributeurs
- La communauté Flask
- Les utilisateurs qui testent et améliorent l'application
