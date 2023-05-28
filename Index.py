class TermDocumentIndex:
    def __init__(self, first_position):
        self.termFrequency = 1
        self.positions = [first_position]

    def add_position(self, position):
        self.termFrequency += 1
        self.positions.append(position)


class Index:
    def __init__(self, token, first_document, first_position):
        self.token = token
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


class PositionalIndex:
    def __init__(self):
        self.index = {}

    def add_position_to_term(self, term, doc_id, position):
        if term in self.index:
            self.index[term].add_position(doc_id, position)
        elif term not in self.index:
            self.index[term] = Index(term, doc_id, position)

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
