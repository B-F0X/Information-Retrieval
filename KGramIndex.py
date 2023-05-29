class KGramIndex:
    def __init__(self, k):
        self.k_gram_index = {}
        self.k = k

    def split_to_k_grams(self, term):
        k_grams = []
        for i in range(len(term) - self.k + 1):
            k_grams.append(term[i:i + self.k])
        return k_grams

    def add_term(self, term):
        k_grams = self.split_to_k_grams(term)
        for k_gram in k_grams:
            if k_gram in self.k_gram_index and term not in self.k_gram_index[k_gram]:
                self.k_gram_index[k_gram].append(term)
            elif k_gram not in self.k_gram_index:
                self.k_gram_index[k_gram] = [term]
        return len(k_grams)

    def get_posting_lists(self, term):
        k_grams = self.split_to_k_grams(term)
        result = []
        for k_gram in k_grams:
            if k_gram in self.k_gram_index:
                result.append(self.k_gram_index[k_gram])
        return result
