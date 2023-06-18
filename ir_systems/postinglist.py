class Postinglist:
    def __init__(self, docid: int = None, position: int = None, term: str = None):
        self.postinglist = []
        self.occurrence = 0
        self.seen_docids = set()
        self.positions = {}
        self.term = term

        if docid:
            self.append(docid, position)

    def __len__(self):
        return len(self.postinglist)

    def __getitem__(self, idx):
        return self.postinglist[idx]

    def append(self, docid: int, position: int) -> None:
        try:
            self.positions[docid].append(position)
        except KeyError:
            self.positions[docid] = [position]
            self.occurrence += 1

        if docid in self.seen_docids:
            pass
        else:
            self.postinglist.append(docid)
            self.seen_docids.add(docid)

    def sort_postinglist(self) -> None:
        self.postinglist = sorted(self.postinglist)

    def get_postinglist(self):
        return self.postinglist

    def get_positions_in_document(self, doc_id):
        return self.positions[doc_id]

    def get_document_frequency(self):
        return self.occurrence
