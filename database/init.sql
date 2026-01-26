-- Création des tables pour SmartAquarium

-- Table des capteurs
CREATE TABLE IF NOT EXISTS capteurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    unite VARCHAR(20) NOT NULL,
    localisation VARCHAR(100)
);

-- Table des actionneurs
CREATE TABLE IF NOT EXISTS actionneurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    etat BOOLEAN NOT NULL DEFAULT FALSE,
    derniere_mise_a_jour TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Table des mesures
CREATE TABLE IF NOT EXISTS mesures (
    id SERIAL PRIMARY KEY,
    capteur_id INTEGER NOT NULL REFERENCES capteurs(id) ON DELETE CASCADE,
    valeur DOUBLE PRECISION NOT NULL,
    horodatage TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- Table de l'historique des commandes
CREATE TABLE IF NOT EXISTS historique_commandes (
    id SERIAL PRIMARY KEY,
    actionneur_id INTEGER NOT NULL REFERENCES actionneurs(id) ON DELETE CASCADE,
    commande VARCHAR(10) NOT NULL,               -- 'ON' / 'OFF' par exemple
    source VARCHAR(50) NOT NULL,                 -- 'front', 'auto', etc.
    horodatage TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- Index utiles
CREATE INDEX IF NOT EXISTS idx_mesures_capteur_id ON mesures(capteur_id);
CREATE INDEX IF NOT EXISTS idx_mesures_horodatage ON mesures(horodatage);
CREATE INDEX IF NOT EXISTS idx_hist_cmd_actionneur_id ON historique_commandes(actionneur_id);
CREATE INDEX IF NOT EXISTS idx_hist_cmd_horodatage ON historique_commandes(horodatage);
