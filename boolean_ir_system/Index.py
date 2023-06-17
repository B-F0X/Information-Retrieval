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
    def __init__(self, term, k_gram_size, first_document, first_position):
        self.term = term
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

    def get_positions_in_document(self, term, doc_id):
        if term in self.index:
            return self.index[term].get_positions_in_document(doc_id)
        else:
            return []
