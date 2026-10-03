# app.py
import math

from flask import Flask, jsonify, redirect, render_template, request, url_for

from models import Calculatrice

app = Flask(__name__)

# Une seule calculatrice partagée par toute l'application
calc = Calculatrice()

OPERATIONS = {
    "addition": "Addition",
    "soustraction": "Soustraction",
    "multiplication": "Multiplication",
    "division": "Division",
}


def _lire_nombre(texte):
    """Convertit une saisie de formulaire en nombre fini (int si entier)."""
    valeur = float(texte)
    if not math.isfinite(valeur):
        raise ValueError("Nombre non fini.")
    if valeur.is_integer() and abs(valeur) < 1e15:
        return int(valeur)
    return valeur


# ---------------------------------------------------------------------------
# Pages web
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculer", methods=["GET", "POST"])
def calculer():
    resultat = None
    erreur = None

    if request.method == "POST":
        operation = request.form.get("operation", "")
        try:
            a = _lire_nombre(request.form["a"])
            b = _lire_nombre(request.form["b"])
            if operation not in OPERATIONS:
                raise ValueError("Opération inconnue.")
            resultat = getattr(calc, operation)(a, b)
        except ZeroDivisionError as e:
            erreur = str(e)
        except (ValueError, KeyError):
            erreur = "Saisissez deux nombres valides et choisissez une opération."

    return render_template(
        "calculer.html",
        operations=OPERATIONS,
        resultat=resultat,
        erreur=erreur,
    )


@app.route("/historique")
def historique():
    return render_template("historique.html", historique=calc.get_historique())


@app.route("/historique/effacer", methods=["POST"])
def effacer_historique():
    calc.effacer_historique()
    return redirect(url_for("historique"))


# ---------------------------------------------------------------------------
# API REST (JSON)
# ---------------------------------------------------------------------------
def _est_nombre(valeur):
    """Vrai pour un int ou un float fini (booléens, NaN et infini exclus)."""
    return (
        isinstance(valeur, (int, float))
        and not isinstance(valeur, bool)
        and math.isfinite(valeur)
    )


@app.route("/api/v1/calculer", methods=["POST"])
def api_calculer():
    donnees = request.get_json(silent=True)

    if not isinstance(donnees, dict):
        return jsonify(erreur="Le corps de la requête doit être un objet JSON."), 400

    manquants = [c for c in ("a", "b", "operation") if c not in donnees]
    if manquants:
        return jsonify(erreur=f"Champs manquants : {', '.join(manquants)}."), 400

    a, b, operation = donnees["a"], donnees["b"], donnees["operation"]

    if not (_est_nombre(a) and _est_nombre(b)):
        return jsonify(erreur="'a' et 'b' doivent être des nombres."), 400

    if operation not in OPERATIONS:
        return jsonify(
            erreur=f"Opération inconnue. Valeurs possibles : {', '.join(OPERATIONS)}."
        ), 400

    try:
        resultat = getattr(calc, operation)(a, b)
    except ZeroDivisionError as e:
        return jsonify(erreur=str(e)), 400

    # 201 : une nouvelle entrée a été créée dans l'historique
    return jsonify(a=a, b=b, operation=operation, resultat=resultat), 201


@app.route("/api/v1/historique", methods=["GET"])
def api_historique():
    historique = calc.get_historique()
    return jsonify(total=len(historique), historique=historique), 200


if __name__ == "__main__":
    app.run(debug=True)