import math


class Merger:
    def __init__(self, index):
        self.index = index

    # Standard AND merger
    def and_merge(self, posting_list1, posting_list2):
        answer = []
        i = 0
        j = 0
        while i < len(posting_list1) and j < len(posting_list2):
            if posting_list1[i] == posting_list2[j]:
                answer.append(posting_list1[i])
                i += 1
                j += 1
            elif posting_list1[i] < posting_list2[j]:
                i += 1
            else:
                j += 1
        return answer

    # AND merger with skip-gram indexes
    def and_merge_fast(self, posting_list1, posting_list2):
        answer = []
        i = 0
        j = 0
        i_skip = int(math.sqrt(len(posting_list1)))
        j_skip = int(math.sqrt(len(posting_list2)))
        while i < len(posting_list1) and j < len(posting_list2):
            if posting_list1[i] == posting_list2[j]:
                answer.append(posting_list1[i])
                i += 1
                j += 1
            elif posting_list1[i] < posting_list2[j]:
                if i % i_skip == 0 and i + i_skip < len(posting_list1) and posting_list1[i + i_skip] < posting_list2[j]:
                    i = i + i_skip
                else:
                    i += 1
            else:
                if j % j_skip == 0 and j + j_skip < len(posting_list1) and posting_list2[j + j_skip] < posting_list1[i]:
                    j = j + j_skip
                else:
                    j += 1
        return answer

    # OR merger
    def or_merge(self, posting_list1, posting_list2):
        answer = []
        i = 0
        j = 0
        while i < len(posting_list1) and j < len(posting_list2):
            if posting_list1[i] == posting_list2[j]:
                answer.append(posting_list1[i])
                i += 1
                j += 1
            elif posting_list1[i] < posting_list2[j]:
                answer.append(posting_list1[i])
                i += 1
            else:
                answer.append(posting_list2[j])
                j += 1
        if i == len(posting_list1):
            answer.extend(posting_list2[j:])
        elif j == len(posting_list2):
            answer.extend(posting_list1[i:])
        return answer

        # Standard AND NOT merger
    def and_not_merge(self, posting_list1, posting_list2):
        answer = []
        i = 0
        j = 0
        while i < len(posting_list1) and j < len(posting_list2):
            if posting_list1[i] == posting_list2[j]:
                i += 1
                j += 1
            elif posting_list1[i] > posting_list2[j]:
                j += 1
            else:
                answer.append(posting_list1[i])
                i += 1
        if j == len(posting_list2):
            answer.extend(posting_list1[i:])
        return answer

    def or_not_merge(self, posting_list1, posting_list2, document_count):
        answer = []
        i = 0
        j = 0
        if len(posting_list1) > 0 and len(posting_list2) > 0 and posting_list1[0] <= posting_list2[0]:
            doc_id = 1
            while doc_id < posting_list2[0]:
                answer.append(doc_id)
                doc_id += 1
        while i < len(posting_list1) and j < len(posting_list2):
            if posting_list1[i] == posting_list2[j]:
                answer.append(posting_list1[i])
                i += 1
                j += 1
            elif posting_list1[i] < posting_list2[j]:
                i += 1
            else:
                doc_id = posting_list2[j] + 1
                j += 1
                while j < len(posting_list2) and doc_id < posting_list2[j]:
                    answer.append(doc_id)
                    doc_id += 1

        if i == len(posting_list1):
            # Add all doc_ids after posting_list2[j] except the ones that are in posting_list2
            doc_id = posting_list2[j] + 1
            while doc_id <= document_count:
                if doc_id not in posting_list2:
                    answer.append(doc_id)
                doc_id += 1
        elif j == len(posting_list2):
            # Add all doc_ids after posting_list2[j]
            doc_id = posting_list2[j-1] + 1
            while doc_id <= document_count:
                answer.append(doc_id)
                doc_id += 1
        return answer

    # NOT merger
    def not_merge(self, posting_list1, document_count):
        answer = []
        i = 0
        j = 1
        while j <= document_count:
            if i < len(posting_list1) and posting_list1[i] == j:
                i += 1
                j += 1
            else:
                answer.append(j)
                j += 1
        return answer

    # Positional intersect algorithm to process proximity queries
    def positional_intersect(self, term1, term2, k):
        answer = []
        posting_list1 = self.index.get_document_list(term1)
        posting_list2 = self.index.get_document_list(term2)
        i = 0
        j = 0
        while i < len(posting_list1) and j < len(posting_list2):
            if posting_list1[i] == posting_list2[j]:
                l = []
                positions_term1 = self.index.get_positions_in_document(term1, doc_id=posting_list1[i])
                positions_term2 = self.index.get_positions_in_document(term2, doc_id=posting_list2[j])
                a = 0
                b = 0
                while a < len(positions_term1):
                    while b < len(positions_term2):
                        if abs(positions_term1[a] - positions_term2[b]) <= k:
                            l.append(positions_term2[b])
                        elif positions_term2[b] > positions_term1[a]:
                            break
                        b += 1
                    while len(l) < 0 and abs(l[0] - positions_term1[a]) > k:
                        l.pop(0)
                    if len(l) > 0:
                        answer.append(posting_list1[i])
                        break
                    a += 1
                i += 1
                j += 1
            elif posting_list1[i] < posting_list2[j]:
                i += 1
            else:
                j += 1
        return answer

    # Method to process phrase queries
    def phrase_query(self, phrase):
        answer = []
        documents_with_all_terms = self.index.get_document_list(phrase[0])
        for i in range(1, len(phrase) - 1):
            documents_with_all_terms = self.and_merge_fast(documents_with_all_terms, self.index.get_document_list(phrase[i]))
        for document in documents_with_all_terms:
            position_lists = []
            for term in phrase:
                position_lists.append(self.index.get_positions_in_document(term, document))
            for position_of_first_word_in_document in position_lists[0]:
                if len(phrase) == 2 and position_of_first_word_in_document+1 in position_lists[1]:
                    answer.append(document)
                    break
                if position_of_first_word_in_document+1 in position_lists[1] and \
                        position_of_first_word_in_document+2 in position_lists[2]:
                    answer.append(document)
                    break
        return answer


