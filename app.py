# app.py
from flask import Flask, redirect, render_template, request, url_for

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
            a = float(request.form["a"])
            b = float(request.form["b"])
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


if __name__ == "__main__":
    app.run(debug=True)