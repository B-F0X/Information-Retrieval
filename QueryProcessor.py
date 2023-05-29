import copy
import random
import sys
from Tokenizer import *
from Merger import *


class QueryProcessor:

    def __init__(self, index, document_count):
        self.index = index
        self.tokenizer = Tokenizer()  # Tokenizerobjekt zum Aufteilen von Text in Wörter
        self.merger = Merger(index)
        self.document_count = document_count

    def tokenize(self, text):
        """
        Teilt eine Suchanfrage in Wörter auf.
        text: Die Suchanfrage als Text.
        """
        return self.tokenizer.tokenize(text)

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

        return previous_row[-1]  # Der letzte Wert in der letzten Zeile ist die Levenshtein-Distanz

    def correct_spelling(self, word, k, r, J):
        """
        Korrigiert die Rechtschreibung eines Worts basierend auf dem Index.
        word: Das zu korrigierende Wort.
        k: Die Länge der K-Gramme für die Suche im Index.
        r: Die minimale Anzahl von Dokumenten, in denen das Wort vorkommen muss, um als korrekt zu gelten.
        J: Der Schwellenwert für die Jaccard-Ähnlichkeit zwischen K-Grammen, um Kandidaten zu ermitteln.
        """
        if len([doc_id for doc_id, tokens in self.index.documents.items() if word in tokens]) >= r:
            return word

        kgrams_word = set(word[i:i + k] for i in range(len(word) - k + 1))
        candidates = {token for kgram in kgrams_word for token in self.index.kgram_index.get(kgram, [])}
        candidates = {candidate for candidate in candidates if self.index.jaccard_similarity(kgrams_word, set(
            candidate[i:i + k] for i in range(len(candidate) - k + 1))) >= J}
        candidates = sorted(candidates, key=lambda candidate: self.levenshtein_distance(word, candidate))

        if candidates:
            return candidates[0]

        return word

    # Verarbeitet eine boolesche Anfrage in Normalform und gibt die entsprechenden Suchergebnisse zurück
    # (NOT "term1 term2" OR NOT term3 \4 term5) AND NOT term4 \3 term5 AND "term1 term3 term4" AND term4
    # (NOT the OR NOT a \20 the OR a b c OR d) AND NOT read write AND (the OR a) AND the
    def process_query(self, query):
        query_tokens = self.tokenizer.tokenizeQuery(query)
        #results = set(self._get_posting_ids(query_tokens[0]))
        #print(results)
        #results = self.merger.phrase_query(query_tokens[0])
        index_lists = {}
        for query_part in query_tokens:
            for i in range(len(query_part)):
                r = re.compile(r'\\[0-9]+')
                filtered_part = list(filter(r.match, query_part[i]))
                if type(query_part[i]) is list and len(filtered_part) > 0:
                    result = self.merger.positional_intersect(query_part[i][0], query_part[i][2], 3)
                    result_id = "#&" + str(random.random())
                    index_lists[result_id] = result
                    query_part[i] = result_id
                elif type(query_part[i]) is list and len(query_part[i]) > 1:
                    result = self.merger.phrase_query(query_part[i])
                    result_id = "#&" + str(random.random())
                    index_lists[result_id] = result
                    query_part[i] = result_id

        for i in range(len(query_tokens)):
            query_part = query_tokens[i]
            while "NOT" in query_part:
                or_pos = query_part.index("NOT")
                if type(query_part[or_pos + 1]) is list:
                    position_list = self.index.get_document_list(query_part[or_pos + 1][0])
                else:
                    position_list = index_lists[query_part[or_pos + 1]]
                result = self.merger.not_merge(position_list, self.document_count)
                result_id = "#&" + str(random.random())
                index_lists[result_id] = result
                query_tokens[i][or_pos] = result_id
                query_tokens[i].pop(or_pos + 1)

            while "OR" in query_part:
                or_pos = query_part.index("OR")
                first_operand = query_part[or_pos - 1]
                second_operand = query_part[or_pos + 1]
                if type(first_operand) is list:
                    position_list_first_operand = self.index.get_document_list(first_operand[0])
                else:
                    position_list_first_operand = index_lists[first_operand]
                if type(second_operand) is list:
                    position_list_second_operand = self.index.get_document_list(second_operand[0])
                else:
                    position_list_second_operand = index_lists[second_operand]
                result = self.merger.or_merge(position_list_first_operand, position_list_second_operand)
                result_id = "#&" + str(random.random())
                index_lists[result_id] = result
                query_tokens[i][or_pos] = result_id
                query_tokens[i].pop(or_pos + 1)
                query_tokens[i].pop(or_pos - 1)

            if not re.match(r'(#&).*', query_part[0]):
                result = self.index.get_document_list(query_part[0])
                result_id = "#&" + str(random.random())
                index_lists[result_id] = result
                query_tokens[i][0] = result_id

        sorted_query = []
        copied_query_tokens = copy.deepcopy(query_tokens)
        while len(copied_query_tokens) > 0:
            shortest = sys.maxsize
            shortest_index = 0
            for i in range(len(copied_query_tokens)):
                token = copied_query_tokens[i][0]
                if len(index_lists[token]) < shortest:
                    if len(index_lists[token]) == 0:
                        return []  # If one of the index_lists is [] than we can instantly return [].
                    shortest = len(index_lists[token])
                    shortest_index = i
            sorted_query.append(copied_query_tokens[shortest_index][0])
            copied_query_tokens.pop(shortest_index)

        while len(sorted_query) != 1:
            result = self.merger.and_merge_fast(index_lists[sorted_query[0]], index_lists[sorted_query[1]])
            result_id = "#&" + str(random.random())
            index_lists[result_id] = result
            sorted_query[0] = result_id
            sorted_query.pop(1)

        return index_lists[sorted_query[0]]

    # Parst die boolesche Anfrage in Normalform und gibt die Liste der Tokens zurück
    def _parse_query(self, query):
        query = query.replace('(', ' ( ')
        query = query.replace(')', ' ) ')
        query_tokens = query.split()
        return query_tokens

    # Gibt die Liste der Dokument-IDs zurück, die mit dem angegebenen Begriff verknüpft sind
    def _get_posting_ids(self, term):
        if term in self.index:
            return self.index[term].get_document_list()
        else:
            return []

    # Verarbeitet eine komplexe boolesche Anfrage in Normalform und gibt die entsprechenden Suchergebnisse zurück
    def _process_complex_query(self, query):
        query_tokens = self._parse_query(query)
        results = set(self._get_posting_ids(query_tokens[0]))
        start_index = 1
        step_size = 2

        for i in range(start_index, len(query_tokens), step_size):
            operator = query_tokens[i]
            #print("C-Operator: ", operator)
            operand = query_tokens[i + 1]
            #print("C-Operand: ", operand)

            if operator == 'AND':
                results &= set(self._get_posting_ids(operand))
            elif operator == 'OR':
                results |= set(self._get_posting_ids(operand))
            elif operator == 'NOT':
                results -= set(self._get_posting_ids(operand))

        return results