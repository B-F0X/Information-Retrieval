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

    # Methode zum Aufteilen des Inhalts einer Datei in Wörter
    def tokenize_file(self, file_path):
        """
        Diese Methode nimmt den Pfad zu einer Datei als Eingabe, öffnet die Datei und liest ihren Inhalt.
        Der Inhalt wird dann an die `tokenize`-Methode übergeben, um ihn in Wörter aufzuteilen.
        Das Ergebnis, eine Liste von Wörtern, wird zurückgegeben.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return self.tokenize(content)