class TermIndex:
    def __init__(self, term: str):
        self.term = term
        self.occurence = 1

    def __hash__(self):
        return hash(self.term)
