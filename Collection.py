from Tokenizer import *
from Document import *
from Index import *
from KGramIndex import *

class Collection:
    def __init__(self, file_path):
        self.file_path = file_path
        self.documents = []
        self.tokenizer = Tokenizer()
        self.k_gram_index = KGramIndex(2)
        self.index = PositionalIndex(self.k_gram_index)
        self.dictionary = {}

    def update_index(self, doc_id, abstract):
        for i in range(len(abstract)):
            term = abstract[i]
            self.index.add_position_to_term(term, doc_id, i)

    def update_dictionary(self, abstract):
        for term in abstract:
            if term in self.dictionary:
                self.dictionary[term] += 1
            else:
                self.dictionary[term] = 1

    def open_and_read(self):
        with open(self.file_path, "r") as file:
            lines = file.readlines()
            num_lines = len(lines)

            i = 0
            while i < num_lines:
                if lines[i].startswith(".I"):
                    # Hole Dokumenten-ID aus der Zeile (letztes Zeichen)
                    doc_id = int(lines[i].split()[-1])
                    i += 1

                    while not lines[i].startswith(".W"):
                        i += 1

                    # Zur nächsten Zeile nach einem ".W" (Beginn eines Abstract)
                    i += 1

                    abstract = ""

                    # Füge alle Zeilen bis zur Referenzsektion (.X) dem Abstract hinzu
                    while not lines[i].startswith(".X"):
                        abstract += lines[i]
                        i += 1

                    # Packe den Abstract in den Tokenizer (ohne führende und nachfolgende Leerzeichen)
                    abstract = self.tokenizer.tokenize(abstract.strip())

                    document = Document(doc_id, abstract)
                    self.documents.append(document)

                    # Index und Dictionary aktualisieren
                    self.update_index(doc_id, abstract)
                    self.update_dictionary(abstract)

                i += 1

            print("Dokumente eingelesen:", len(self.documents))

    def get_document_count(self):
        return len(self.documents)