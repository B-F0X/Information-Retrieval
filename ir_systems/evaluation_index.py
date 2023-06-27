from config import *


class EvaluationIndex:
    def __init__(self):
        self.queries = {}
        self.relevant_documents = {}
        self.extract_queries(query_file)
        self.extract_relevant_documents(relevant_documents_file)

    def extract_queries(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            num_lines = len(lines)

            print(f"Öffne Datei {file_path}")
            print(f"Datei enthält {num_lines} Zeilen.")

            i = 0
            while i < num_lines:
                if lines[i].startswith(".I"):
                    # Hole Dokumenten-ID aus der Zeile (letztes Zeichen)
                    query_id = int(lines[i].split()[-1])
                    i += 1

                    while not lines[i].startswith(".W"):
                        i += 1

                    # Zur nächsten Zeile nach einem ".W" (Beginn eines Abstract)
                    i += 1

                    abstract = ""

                    # Füge alle Zeilen bis zur Referenzsektion (.X) dem Abstract hinzu
                    while i < num_lines and not lines[i].startswith(".I"):
                        abstract += lines[i]
                        i += 1

                    # Mapping zwischen doc_id und Länge des Abstracts
                    self.queries[query_id] = abstract.strip()

    def extract_relevant_documents(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            num_lines = len(lines)

            print(f"Öffne Datei {file_path}")
            print(f"Datei enthält {num_lines} Zeilen.")

            i = 0
            query_index = 1
            while i < num_lines:
                relevant_documents_for_query = []
                while i < num_lines and lines[i].strip().startswith(str(query_index)):
                    current_line = lines[i].strip()
                    current_line = current_line[current_line.index(" "):].strip()
                    relevant_documents_for_query.append(int(current_line[:current_line.index("\t")]))
                    i += 1
                self.relevant_documents[query_index] = relevant_documents_for_query
                query_index += 1
