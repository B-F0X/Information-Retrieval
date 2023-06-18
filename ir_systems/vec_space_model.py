from retrieval import InitRetrievalSystem  # Abstract class
from tokenizer import *
from termIndex import *
from postinglist import *
from config import *
import time
import numpy as np


class VectorSpaceModel(InitRetrievalSystem):
    def __init__(self):
        self.dictionary = {}
        self.term_index_mapping = {}
        self.doc_id_length_mapping = {}
        self.average_doc_len = 0.0

        self.tokenizer = Tokenizer()

    def open_and_read(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            num_lines = len(lines)

            print(f"Öffne Datei {file_path}")
            print(f"Datei enthält {num_lines} Zeilen.")

            start_time = time.perf_counter()
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

                    # Mapping zwischen doc_id und Länge des Abstracts
                    self.doc_id_length_mapping[doc_id] = len(abstract)

                    for token in abstract:

                        # If there is no term index for the given token in the dictionary
                        # create a new term index and add it
                        try:
                            term_index = self.term_index_mapping[token]
                        except KeyError:
                            term_index = TermIndex(token)
                            self.term_index_mapping[token] = term_index

                        # Add doc_id + position for that term_index to the existing posting list
                        # Increment occurrence counter
                        # If there is no posting list for that term; create a new one
                        try:
                            self.dictionary[term_index].append(doc_id, i)
                            term_index.occurence += 1
                        except KeyError:
                            self.dictionary[term_index] = Postinglist(doc_id, i, token)

                i += 1

            elapsed_time_indexing = (time.perf_counter() - start_time) * 1e3
            start_time = time.perf_counter()

            # Sort posting lists
            for key, val in self.dictionary.items():
                val.sort_postinglist()

            elapsed_time_sorting = (time.perf_counter() - start_time) * 1e3

            self.calc_avg_doc_length()

            # Print some file statistics
            print("\nEinlesen und Indexierung beendet.")
            print(f"Zeit für Einlesen und Indexierung: {elapsed_time_indexing:.2f} ms")
            print(f"Zeit fürs Sortieren der Postinglisten: {elapsed_time_sorting:.2f} ms\n")

    def calc_avg_doc_length(self):
        average_length = 0
        for doc_id, doc_length in self.doc_id_length_mapping.items():
            average_length += doc_length
        self.average_doc_len = average_length / len(self.doc_id_length_mapping.items())

    # TODO: Implement for real (I do not think we need it)
    def retrieve(self, query):
        return 0

    def retrieve_k(self, query, k):
        query_terms = self.tokenizer.tokenize(query)
        return self.fast_cosine_scores(query_terms, k)

    def fast_cosine_alg(self, posting_list_obj, doc_id, query_freq):
        term_doc_freq = len(posting_list_obj.positions[doc_id])
        len_doc = self.doc_id_length_mapping[doc_id]
        number_of_docs = len(self.doc_id_length_mapping)
        d_f_t = posting_list_obj.occurrence
        score = query_freq * (term_doc_freq / (term_doc_freq + (config_k * (len_doc / self.average_doc_len)))
                              * np.log((number_of_docs / d_f_t)))
        return 0

    def fast_cosine_scores(self, query_terms, k):
        number_of_documents = len(self.doc_id_length_mapping.keys())
        scores = {}
        # for each query term t
        for query_term in query_terms:
            # do fetch posting list for t
            try:
                query_term_posting_list = self.dictionary[self.term_index_mapping[query_term]]
            except KeyError:
                print("Term {} is not known. It will be ignored in the query.".format(query_term))
                continue
            document_frequency = query_term_posting_list.get_document_frequency()
            # for each pair(d, tf(t,d)) in postinglist
            for doc_id in query_term_posting_list.get_postinglist():
                term_frequency = len(query_term_posting_list.get_positions_in_document(doc_id))
                # do Scored[d] += w(t,d)
                try:
                    scores[doc_id] += self.calculate_weight_of_term_in_document(
                        doc_id, term_frequency, number_of_documents, document_frequency, k)
                except KeyError:
                    scores[doc_id] = self.calculate_weight_of_term_in_document(
                        doc_id, term_frequency, number_of_documents, document_frequency, k)
        # for each d
        for doc_id in scores.keys():
            # do Scored[d] = Scored[d] / Length[d]
            scores[doc_id] = scores[doc_id] / self.doc_id_length_mapping[doc_id]
        sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
        # return components of Scores[]
        return list(sorted_scores.keys())

    def calculate_weight_of_term_in_document(self, doc_id, term_frequency, number_of_documents, document_frequency, k):
        return term_frequency / \
               (term_frequency + k * (self.doc_id_length_mapping[doc_id] /
                                      self.average_doc_len)) * np.log(number_of_documents/document_frequency)



