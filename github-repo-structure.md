# Architecture GitHub - SmartAquarium

```
smartaquarium/
│
├── .github/
│   ├── workflows/
│   │   ├── ci-backend.yml          # CI/CD pipeline pour le back-end
│   │   ├── ci-frontend.yml         # CI/CD pipeline pour le front-end
│   │   └── docker-build.yml        # Build et push des images Docker
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
│
├── backend/                         # API Python/Flask ou FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # Point d'entrée
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── sensor.py           # Modèle Capteur
│   │   │   ├── measurement.py      # Modèle Mesure
│   │   │   ├── actuator.py         # Modèle Actionneur
│   │   │   └── command_history.py  # Historique des commandes
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── sensors.py          # Endpoints capteurs
│   │   │   ├── measurements.py     # Endpoints mesures
│   │   │   ├── actuators.py        # Endpoints actionneurs
│   │   │   └── commands.py         # Endpoints commandes
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── sensor_service.py   # Logique métier capteurs
│   │   │   ├── measurement_service.py
│   │   │   ├── actuator_service.py
│   │   │   └── alert_service.py    # Gestion des alertes
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py             # Authentification
│   │   │   └── error_handler.py    # Gestion des erreurs
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── validators.py       # Validation données
│   │   │   ├── logger.py           # Logging
│   │   │   └── constants.py        # Constantes
│   │   └── config.py               # Configuration (DB, ports, etc.)
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_sensors.py
│   │   ├── test_measurements.py
│   │   └── test_actuators.py
│   ├── migrations/                 # Migrations SQLAlchemy (Alembic)
│   ├── requirements.txt            # Dépendances Python
│   ├── .env.example                # Variables d'environnement exemple
│   ├── Dockerfile
│   └── README.md
│
├── frontend/                        # Application web (Vue/Angular/Django templates)
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.vue       # Tableau de bord principal
│   │   │   ├── SensorCard.vue      # Affichage capteur
│   │   │   ├── ActuatorControl.vue # Contrôle actionneur
│   │   │   ├── HistoryChart.vue    # Graphique historique
│   │   │   └── AlertPanel.vue      # Panneau alertes
│   │   ├── services/
│   │   │   ├── api.js              # Service API
│   │   │   └── websocket.js        # WebSocket (temps réel)
│   │   ├── styles/
│   │   │   ├── main.css
│   │   │   └── variables.css
│   │   ├── App.vue
│   │   └── main.js
│   ├── Dockerfile
│   ├── package.json
│   └── README.md
│
├── arduino/                         # Code embarqué
│   ├── smartaquarium/
│   │   ├── smartaquarium.ino       # Code principal
│   │   ├── sensors/
│   │   │   ├── temperature.h
│   │   │   ├── water_level.h
│   │   │   └── ph_sensor.h
│   │   ├── actuators/
│   │   │   ├── pump.h
│   │   │   ├── heater.h
│   │   │   └── led.h
│   │   └── config/
│   │       ├── wifi_config.h
│   │       └── server_config.h
│   └── README.md
│
├── database/
│   ├── migrations/
│   │   ├── 001_init_schema.sql
│   │   └── 002_add_indexes.sql
│   ├── seeds/
│   │   └── seed_data.sql
│   ├── schema.sql                  # Schéma complet
│   └── README.md
│
├── docker/
│   ├── docker-compose.yml          # Orchestration services
│   ├── nginx/                       # Proxy inverse (optionnel)
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   └── README.md
│
├── docs/
│   ├── architecture.md             # Vue d'ensemble architecture
│   ├── api-endpoints.md            # Documentation API REST
│   ├── database-schema.md          # Schéma base de données
│   ├── deployment.md               # Guide déploiement Docker
│   ├── setup.md                    # Guide installation
│   └── troubleshooting.md          # Dépannage
│
├── .gitignore
├── .env.example                    # Variables globales exemple
├── docker-compose.yml              # Fichier principal (racine)
├── Dockerfile.backend
├── Dockerfile.frontend
├── README.md                        # README principal du projet
└── CONTRIBUTING.md                 # Guide contribution

```

## 📋 Description des répertoires

### Backend (`backend/`)
- **Structure modulaire** avec séparation responsabilités
- **Models** : Modèles de données (ORM)
- **Routes** : Points d'entrée API
- **Services** : Logique métier
- **Middleware** : Authentification, gestion erreurs
- **Tests** : Suite de tests unitaires

### Frontend (`frontend/`)
- **Components** : Composants Vue/Angular réutilisables
- **Services** : Communication API et WebSocket
- **Public** : Assets statiques
- **Styles** : CSS centralisé

### Arduino (`arduino/`)
- **Modularité** avec headers pour chaque capteur/actionneur
- **Config** : Configuration WiFi et serveur centralisée
- **Facile à tester** sur Wokwi

### Database (`database/`)
- **Migrations** : Versionning du schéma DB
- **Seeds** : Données de test
- **Scripts** : Setup initial

### Docker (`docker/`)
- **docker-compose.yml** : Orchestre backend, frontend, DB
- **Services isolés** pour faciliter le déploiement

### Docs (`docs/`)
- **Documentation complète** pour chaque couche
- **Guide d'installation et déploiement**

## 🚀 Workflow recommandé

1. **Jour 1** : Architecture & MCD
   - Initialiser repo avec cette structure
   - Créer branches : `feature/arduino`, `feature/backend`, `feature/frontend`, `feature/database`

2. **Jour 2-3** : Développement parallèle
   - Arduino envoie données HTTP POST
   - Backend reçoit et stocke en DB
   - Frontend consomme API

3. **Jour 4** : Docker & intégration
   - `docker-compose up` lance tout

4. **Jour 5** : Tests & docs

## 📝 Fichiers importants à créer d'abord

```bash
# Racine du repo
.gitignore
README.md
docker-compose.yml

# Backend
backend/requirements.txt
backend/.env.example
backend/Dockerfile

# Frontend
frontend/package.json
frontend/Dockerfile

# Database
database/schema.sql
```

## 🔄 Communication entre couches

```
Arduino → Backend API (POST /api/measurements)
                ↓
         PostgreSQL (stockage)
                ↓
         Backend (GET /api/sensors, /api/measurements)
                ↓
         Frontend Dashboard
                ↓
         WebSocket (temps réel)
                ↓
         Backend (PUT /api/actuators/:id/state)
                ↓
         Arduino (HTTP GET /api/commands)
```

Besoin de plus de détails sur une partie spécifique? 🎯
