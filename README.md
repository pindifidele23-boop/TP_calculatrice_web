# Calculatrice web (Flask)

Application web de calcul développée avec Flask et Jinja2. Elle s'appuie sur une classe
`Calculatrice` en programmation orientée objet, qui garde l'historique des opérations.
Elle propose des pages web et une API REST au format JSON.

## Fonctionnalités

- Opérations : addition, soustraction, multiplication, division (division par zéro refusée).
- Pages web avec un gabarit parent Jinja2 partagé (`base.html`).
- Historique des calculs, affiché avec une boucle `{% for %}`.
- API REST : `POST /api/v1/calculer` et `GET /api/v1/historique`.

## Structure du projet

```
TP_calculatrice_web/
├── app.py                 # Serveur Flask : pages web et API
├── models.py              # Classe Calculatrice (historique privé _historique)
├── requirements.txt
├── README.md
└── templates/
    ├── base.html          # Gabarit parent (navigation, CSS)
    ├── index.html
    ├── calculer.html
    └── historique.html
```

## Installation

Prérequis : Python 3.10 ou plus récent.

```bash
python -m venv .venv
source .venv/Scripts/activate     # Git Bash sous Windows
# .venv\Scripts\activate          # PowerShell / cmd
pip install -r requirements.txt
```

## Lancement

```bash
python app.py
```

Ouvrir ensuite http://127.0.0.1:5000. Le serveur s'arrête avec `Ctrl+C`.

## Pages web

| URL | Rôle |
|---|---|
| `/` | Accueil |
| `/calculer` | Formulaire de calcul (deux nombres et une opération) |
| `/historique` | Liste des calculs effectués |

## API REST

### `POST /api/v1/calculer`

Effectue un calcul et l'ajoute à l'historique.

Requête (`Content-Type: application/json`) :

```json
{ "a": 10, "b": 5, "operation": "addition" }
```

Opérations acceptées : `addition`, `soustraction`, `multiplication`, `division`.

Réponse `201 Created` :

```json
{ "a": 10, "b": 5, "operation": "addition", "resultat": 15 }
```

Réponse `400 Bad Request` (exemple) :

```json
{ "erreur": "Division par zéro impossible." }
```

### `GET /api/v1/historique`

Réponse `200 OK` :

```json
{ "total": 1, "historique": ["10 + 5 = 15"] }
```

### Codes de statut

| Code | Signification |
|---|---|
| 200 | Lecture réussie (historique) |
| 201 | Calcul effectué et enregistré |
| 400 | Requête invalide : JSON absent ou mal formé, champ manquant, valeur non numérique, opération inconnue, division par zéro |

### Exemple avec curl

```bash
curl -X POST http://127.0.0.1:5000/api/v1/calculer \
     -H "Content-Type: application/json" \
     -d '{"a": 10, "b": 5, "operation": "multiplication"}'
```

## Limites connues

- L'historique est conservé en mémoire : il est partagé entre tous les visiteurs et
  disparaît au redémarrage du serveur.
- Le serveur lancé avec `debug=True` est prévu pour le développement uniquement.
