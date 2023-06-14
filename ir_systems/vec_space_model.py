from retrieval import InitRetrievalSystem  # Abstract class


class VectorSpaceModel(InitRetrievalSystem):
    def __init__(self, tokenized_file):
        self.dictionary = {}

    # TODO: Implement
    # def open_and_read(self):
    # ...

    # TODO: Implement
    # def calc_avg_doc_length(self):
    # ...

    # TODO: Implement
    # def retrieve(self, query):
    # ...

    # TODO: Implement
    # def retrieve_k(self, query, k):
    # ...

    # TODO: Implement
    # def fast_cosine_alg(self):
    # ...