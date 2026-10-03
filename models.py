# models.py

class Calculatrice:
    """Calculatrice simple avec historique des opérations."""

    def __init__(self):
        self._historique = []  # liste privée (convention : préfixe _)

    # ---------- Opérations ----------
    def addition(self, a, b):
        resultat = a + b
        self._enregistrer(f"{a} + {b} = {resultat}")
        return resultat

    def soustraction(self, a, b):
        resultat = a - b
        self._enregistrer(f"{a} - {b} = {resultat}")
        return resultat

    def multiplication(self, a, b):
        resultat = a * b
        self._enregistrer(f"{a} * {b} = {resultat}")
        return resultat

    def division(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Division par zéro impossible.")
        resultat = a / b
        self._enregistrer(f"{a} / {b} = {resultat}")
        return resultat

    # ---------- Historique ----------
    def _enregistrer(self, operation):
        """Méthode interne : ajoute une entrée à l'historique."""
        self._historique.append(operation)

    def get_historique(self):
        """Retourne une copie pour protéger la liste interne."""
        return list(self._historique)

    def effacer_historique(self):
        self._historique.clear()