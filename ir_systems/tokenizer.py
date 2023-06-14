import re

class Tokenizer:
    def __init__(self):
        pass

    # Methode zum Aufteilen von Text in Wörter
    def tokenize(self, text):
        """
        Diese Methode nimmt einen Text als Eingabe, konvertiert ihn in Kleinbuchstaben,
        entfernt Sonderzeichen und Unterstriche und gibt eine Liste von Wörtern zurück.
        """
        text = text.lower()
        text = re.sub(r'[^\w\s\']|_', '', text)
        text = re.sub(r"\s'|'\s", ' ', text)
        return text.split()