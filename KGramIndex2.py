class KGramIndex:
    def __init__(self):
        self.documents = {}   # Dictionary zur Speicherung von Dokumenten
        self.kgram_index = {} # Dictionary zur Speicherung des K-Gramm-Indexes

    def add_document(self, doc_id, tokens):
        """
        Fügt ein Dokument und seine zugehörigen Tokens dem Index hinzu.
        doc_id: Die eindeutige Kennung des Dokuments.
        tokens: Eine Liste von Tokens, die im Dokument vorkommen.
        """
        self.documents[doc_id] = tokens

    def generate_kgram_index(self, k):
        """
        Erstellt den K-Gramm-Index aus den Tokens der Dokumente.
        k: Die Länge der K-Gramme, die erstellt werden sollen.
        """
        for doc_id, tokens in self.documents.items():
            for token in tokens:
                for i in range(len(token) - k + 1):
                    kgram = token[i:i+k]
                    if kgram not in self.kgram_index:
                        self.kgram_index[kgram] = set()
                    self.kgram_index[kgram].add(token)

    def jaccard_similarity(self, set1, set2):
        """
        Berechnet die Jaccard-Ähnlichkeit zwischen zwei Mengen.
        set1: Die erste Menge.
        set2: Die zweite Menge.
        """
        intersection = set1 & set2
        union = set1 | set2
        return len(intersection) / len(union) if len(union) != 0 else 0