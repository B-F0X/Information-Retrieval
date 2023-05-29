import sys
# Class to safe the term frequency and the positions of the term in the document
class TermDocumentIndex:
    def __init__(self, first_position):
        self.termFrequency = 1
        self.positions = [first_position]

    def add_position(self, position):
        self.termFrequency += 1
        self.positions.append(position)


# Class to safe a token, the Documents it is in and the document frequency
class Index:
    def __init__(self, token, k_gram_size, first_document, first_position):
        self.token = token
        self.k_gram_size = k_gram_size
        self.document_frequency = 1
        self.documents = {first_document: TermDocumentIndex(first_position)}

    def add_position(self, doc_id, position):
        if doc_id in self.documents:
            self.documents[doc_id].add_position(position)
        else:
            self.documents[doc_id] = TermDocumentIndex(position)
            self.document_frequency += 1

    def get_document_list(self):
        return list(self.documents.keys())

    def get_positions_in_document(self, doc_id):
        if doc_id in self.documents:
            return self.documents[doc_id].positions
        else:
            return []


# Class to safe the Indexes of all terms
class PositionalIndex:
    def __init__(self, k_gram_index):
        self.index = {}
        self.k_gram_index = k_gram_index

    def add_position_to_term(self, term, doc_id, position):
        if term in self.index:
            self.index[term].add_position(doc_id, position)
        elif term not in self.index:
            k_gram_size = self.k_gram_index.add_term(term)
            self.index[term] = Index(term, k_gram_size, doc_id, position)

    def get_document_list(self, term):
        if term in self.index:
            return self.index[term].get_document_list()
        else:
            return []

    def get_document_list_spelling_correction(self, term):
        if term in self.index:
            return self.index[term].get_document_list()
        else:
            amount_of_k_grams = len(self.k_gram_index.split_to_k_grams(term))
            k_gram_posting_lists = self.k_gram_index.get_posting_lists(term)
            k_gram_dictionary = {}
            results = []
            for posting_list in k_gram_posting_lists:
                for posting in posting_list:
                    if posting not in k_gram_dictionary:
                        k_gram_dictionary[posting] = 1
                    else:
                        k_gram_dictionary[posting] += 1
            for k_term, value in k_gram_dictionary.items():
                jaccard = value / (amount_of_k_grams + self.index[k_term].k_gram_size - value)
                if jaccard > 0.5:
                    results.append(k_term)

            best_fitting_term = ""
            best_levenshtein_distance = sys.maxsize
            for k_term in results:
                levenshtein_distance = self.levenshtein_distance(k_term, term)
                if levenshtein_distance < best_levenshtein_distance:
                    best_fitting_term = k_term
                    best_levenshtein_distance = levenshtein_distance
            print("Corrected " + term + " to: " + best_fitting_term)

            return self.get_document_list(best_fitting_term)

    def get_positions_in_document(self, term, doc_id):
        if term in self.index:
            return self.index[term].get_positions_in_document(doc_id)
        else:
            return []

    def levenshtein_distance(self, word1, word2):
        """
        Berechnet die Levenshtein-Distanz zwischen zwei Wörtern.
        word1: Das erste Wort.
        word2: Das zweite Wort.
        """
        if len(word1) < len(word2):
            return self.levenshtein_distance(word2, word1)

        if len(word2) == 0:
            return len(word1)

        previous_row = range(len(word2) + 1)
        for i, char1 in enumerate(word1):
            current_row = [i + 1]
            for j, char2 in enumerate(word2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (char1 != char2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]
