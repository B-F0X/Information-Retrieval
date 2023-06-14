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
            self.occurrence += 1
        except KeyError:
            self.positions[docid] = [position]
            self.occurrence += 1

        if docid in self.seen_docids:
            pass
        else:
            self.postinglist.append(docid)
            self.seen_docids.add(docid)

    def get_sorted_postinglist(self) -> None:
        self.postinglist = sorted(self.postinglist)