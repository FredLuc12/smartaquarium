-- =====================================================
-- Initialisation de la base SmartAquarium
-- =====================================================

-- ======================
-- Table des capteurs
-- ======================
CREATE TABLE IF NOT EXISTS capteurs (
    id INTEGER PRIMARY KEY,                  -- ❌ Plus de SERIAL, ID manuel
    nom VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    unite VARCHAR(20),
    localisation VARCHAR(100),
    seuil_min DOUBLE PRECISION,
    seuil_max DOUBLE PRECISION,
    actif BOOLEAN NOT NULL DEFAULT TRUE
);

-- ======================
-- Table des actionneurs
-- ======================
CREATE TABLE IF NOT EXISTS actionneurs (
    id INTEGER PRIMARY KEY,                  -- ❌ Plus de SERIAL, ID manuel
    nom VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    etat BOOLEAN NOT NULL DEFAULT FALSE,
    derniere_mise_a_jour TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- ======================
-- Table des mesures
-- ======================
CREATE TABLE IF NOT EXISTS mesures (
    id SERIAL PRIMARY KEY,                   -- ✅ Ici on garde SERIAL (pas de conflit)
    capteur_id INTEGER NOT NULL,
    valeur DOUBLE PRECISION NOT NULL,
    horodatage TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_mesures_capteur
        FOREIGN KEY (capteur_id)
        REFERENCES capteurs(id)
        ON DELETE CASCADE
);

-- ======================
-- Table historique des commandes
-- ======================
CREATE TABLE IF NOT EXISTS historique_commandes (
    id SERIAL PRIMARY KEY,                   -- ✅ Ici on garde SERIAL
    actionneur_id INTEGER NOT NULL,
    commande VARCHAR(10) NOT NULL,
    source VARCHAR(50) NOT NULL,
    horodatage TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_hist_cmd_actionneur
        FOREIGN KEY (actionneur_id)
        REFERENCES actionneurs(id)
        ON DELETE CASCADE
);

-- ======================
-- Table des alertes
-- ======================
CREATE TABLE IF NOT EXISTS alertes (
    id SERIAL PRIMARY KEY,                   -- ✅ Ici on garde SERIAL
    capteur_id INTEGER NOT NULL,
    niveau VARCHAR(20) NOT NULL CHECK (niveau IN ('warning', 'critical')),
    message VARCHAR(255) NOT NULL,
    horodatage TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    acquitte_par INTEGER,
    acquitte_le TIMESTAMP WITHOUT TIME ZONE,
    resolue BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_alertes_capteur
        FOREIGN KEY (capteur_id)
        REFERENCES capteurs(id)
        ON DELETE CASCADE
);

-- ======================
-- Index (perfs)
-- ======================
CREATE INDEX IF NOT EXISTS idx_mesures_capteur_id ON mesures(capteur_id);
CREATE INDEX IF NOT EXISTS idx_mesures_horodatage ON mesures(horodatage);
CREATE INDEX IF NOT EXISTS idx_hist_cmd_actionneur_id ON historique_commandes(actionneur_id);
CREATE INDEX IF NOT EXISTS idx_hist_cmd_horodatage ON historique_commandes(horodatage);
CREATE INDEX IF NOT EXISTS idx_alertes_capteur_id ON alertes(capteur_id);
CREATE INDEX IF NOT EXISTS idx_alertes_niveau ON alertes(niveau);

-- ======================
-- Données initiales (IDs manuels définis par Arduino)
-- ======================
INSERT INTO capteurs (id, nom, type, unite, localisation, seuil_min, seuil_max, actif) VALUES
    (1, 'HC-SR04 Distance', 'distance', 'cm', 'Capteur de niveau d''eau', 5.0, 30.0, TRUE),
    (2, 'Potentiomètre pH', 'ph', 'pH', 'Mesure du pH de l''eau', 6.5, 7.5, TRUE),
    (3, 'Photosensor Luminosité', 'luminosite', 'lux', 'Capteur de luminosité ambiante', 100.0, 800.0, TRUE)
ON CONFLICT (id) DO NOTHING;

INSERT INTO actionneurs (id, nom, type, etat) VALUES
    (1, 'Pompe de filtration', 'pompe', FALSE),
    (2, 'LED Principal', 'led', FALSE),
    (3, 'Distributeur nourriture', 'nourrisseur', FALSE)
ON CONFLICT (id) DO NOTHING;

-- Message de succès
DO $$
BEGIN
    RAISE NOTICE '✅ Base de données SmartAquarium initialisée avec 3 capteurs et 3 actionneurs';
END $$;
