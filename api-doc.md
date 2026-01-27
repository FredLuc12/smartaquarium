# 🐠 Tuto – Comment utiliser l’API SmartAquarium 

Ce document explique **comment consommer l’API** SmartAquarium 

- côté **Arduino/ESP32** (pour envoyer les mesures et lire les ordres), 
- côté **Frontend** (pour afficher les données et piloter les actionneurs). 

---

## 🌍 1. Infos générales 

### URL de base

```text
http://localhost:8000
```  

Sur le réseau / serveur :  

```text
http://<IP_ou_nom_serveur>:8000
```  

Toutes les requêtes utilisent :  

```text
Content-Type: application/json
```  

La doc interactive de l’API est dispo ici :  

```text
http://<IP_ou_nom_serveur>:8000/docs
```  

---

## 🤖 2. Arduino / ESP32 – Intégration  

### 2.1 Rôle de l’Arduino  

L’Arduino :  

- lit les capteurs physiques (température, pH, etc.),  
- envoie les valeurs au backend via `POST /api/mesures`,  
- lit l’état des actionneurs via `GET /api/actionneurs/{id}` pour savoir s’il doit allumer/éteindre un relais.  

L’intelligence (seuils, alertes, historique) est gérée par le backend, pas dans l’Arduino.  

### 2.2 Pré‑requis côté Arduino  

Plaque : ESP32 / ESP8266 ou Arduino + module WiFi.  

Bibliothèques typiques :  

- `WiFi.h`  
- `HTTPClient.h`  
- `ArduinoJson` (recommandé pour gérer le JSON).  

Connaître :  

- l’URL de l’API,  
- l’ID des capteurs (`capteur_id`) et actionneurs (`actionneur_id`) créés dans la base.  

### 2.3 Connexion WiFi  

```cpp
#include <WiFi.h>

const char* WIFI_SSID = "TON_WIFI";
const char* WIFI_PASSWORD = "TON_MDP";

void connectToWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}
```  

À appeler dans `setup()`.  

### 2.4 Envoyer une mesure à l’API  

Endpoint utilisé :  

```text
POST /api/mesures
```  

Corps JSON attendu :  

```json
{
  "capteur_id": 1,
  "valeur": 25.3
}
```  

Exemple de fonction :  

```cpp
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* API_URL = "http://192.168.1.100:8000"; // IP du backend

void sendTemperature(float value) {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(String(API_URL) + "/api/mesures");
  http.addHeader("Content-Type", "application/json");

  DynamicJsonDocument doc(256);
  doc["capteur_id"] = 1;      // ID du capteur de température
  doc["valeur"] = value;

  String payload;
  serializeJson(doc, payload);

  int code = http.POST(payload);

  // Optionnel: vérifier le code (200/201 = OK)
  // String resp = http.getString();

  http.end();
}
```  

Tu appelles cette fonction périodiquement, par exemple toutes les 60 secondes.  

### 2.5 Récupérer l’état d’un actionneur  

Endpoint utilisé :  

```text
GET /api/actionneurs/{id}
```  

Réponse JSON (simplifiée) :  

```json
{
  "id": 1,
  "nom": "Pompe filtration",
  "type": "pompe",
  "etat": true,
  "derniere_mise_a_jour": "2026-01-27T14:31:00"
}
```  

Exemple de fonction :  

```cpp
void syncPumpFromApi() {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(String(API_URL) + "/api/actionneurs/1"); // 1 = ID de la pompe

  int code = http.GET();
  if (code == 200) {
    DynamicJsonDocument doc(512);
    deserializeJson(doc, http.getString());

    bool etat = doc["etat"]; // true = ON, false = OFF
    digitalWrite(12, etat ? HIGH : LOW); // 12 = pin de la pompe
  }

  http.end();
}
```  

### 2.6 Boucle Arduino typique  

```cpp
unsigned long lastMeasure = 0;
unsigned long lastSync = 0;

void loop() {
  unsigned long now = millis();

  // Envoyer une mesure toutes les 60s
  if (now - lastMeasure > 60000) {
    float temp = readTemperatureSensor(); // ta fonction de lecture
    sendTemperature(temp);
    lastMeasure = now;
  }

  // Vérifier les ordres toutes les 30s
  if (now - lastSync > 30000) {
    syncPumpFromApi();
    lastSync = now;
  }
}
```  

---

## 🖥️ 3. Frontend – Intégration  

### 3.1 Rôle du frontend  

Le frontend :  

- lit les données via l’API pour afficher :  
  - la liste des capteurs,  
  - la dernière valeur de chaque capteur,  
  - les alertes actives,  
  - l’état des actionneurs.  
- envoie les actions utilisateur :  
  - changement d’état d’un actionneur (ON/OFF),  
  - acquittement / résolution d’alertes.  

Le frontend ne parle jamais directement à l’Arduino, seulement à l’API.  

### 3.2 Pré‑requis  

- Application React (ou autre framework JS).  
- Lib HTTP : `fetch` natif ou `axios`.  

Exemple ci‑dessous avec Axios.  

### 3.3 Client HTTP  

Installation :  

```bash
npm install axios
```  

Client :  

```js
// api/client.js
import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000", // à adapter
  headers: { "Content-Type": "application/json" },
});
```  

### 3.4 Récupérer les capteurs  

Endpoint :  

```text
GET /api/capteurs
```  

```js
// api/capteurs.js
import { api } from "./client";

export async function getCapteurs() {
  const res = await api.get("/api/capteurs");
  return res.data;
}
```  

Utilisation dans un composant :  

```js
import { useEffect, useState } from "react";
import { getCapteurs } from "./api/capteurs";

function CapteursList() {
  const [capteurs, setCapteurs] = useState([]);

  useEffect(() => {
    getCapteurs().then(setCapteurs).catch(console.error);
  }, []);

  return (
    <ul>
      {capteurs.map((c) => (
        <li key={c.id}>
          {c.nom} ({c.type}) – {c.localisation}
        </li>
      ))}
    </ul>
  );
}
```  

### 3.5 Afficher la dernière mesure d’un capteur  

Endpoint :  

```text
GET /api/mesures/capteur/{id}/latest
```  

```js
// api/mesures.js
import { api } from "./client";

export async function getLastMeasure(capteurId) {
  const res = await api.get(`/api/mesures/capteur/${capteurId}/latest`);
  return res.data;
}
```  

Dans une carte de capteur :  

```js
import { useEffect, useState } from "react";
import { getLastMeasure } from "./api/mesures";

function CapteurCard({ capteur }) {
  const [last, setLast] = useState(null);

  useEffect(() => {
    getLastMeasure(capteur.id)
      .then(setLast)
      .catch(() => setLast(null));
  }, [capteur.id]);

  return (
    <div>
      <h3>{capteur.nom}</h3>
      {last ? (
        <p>
          {last.valeur} {capteur.unite}
        </p>
      ) : (
        <p>Aucune mesure</p>
      )}
    </div>
  );
}
```  

### 3.6 Récupérer les alertes actives  

Endpoint :  

```text
GET /api/alertes/active
```  

```js
// api/alertes.js
import { api } from "./client";

export async function getActiveAlerts() {
  const res = await api.get("/api/alertes/active");
  return res.data;
}
```  

Badge dans un header :  

```js
import { useEffect, useState } from "react";
import { getActiveAlerts } from "./api/alertes";

function AlertsBadge() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const load = () => getActiveAlerts().then(setAlerts).catch(console.error);
    load();
    const id = setInterval(load, 10000); // refresh toutes les 10s
    return () => clearInterval(id);
  }, []);

  if (alerts.length === 0) return null;

  return <span>{alerts.length} alertes</span>;
}
```  

### 3.7 Contrôler un actionneur  

Option simple :  

```text
PUT /api/actionneurs/{id}
