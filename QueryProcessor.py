import copy
import random
import sys
from Tokenizer import *
from Merger import *
from SpellingController import *


class QueryProcessor:

    def __init__(self, index, document_count):
        self.index = index
        self.tokenizer = Tokenizer()  # Tokenizerobjekt zum Aufteilen von Text in Wörter
        self.merger = Merger(index)
        self.document_count = document_count
        self.spelling_controller = SpellingController(index)

    # Verarbeitet eine boolesche Anfrage in Normalform und gibt die entsprechenden Suchergebnisse zurück
    # (NOT "term1 term2" OR NOT term3 \4 term5) AND NOT term4 \3 term5 AND "term1 term3 term4" AND term4
    # (NOT the OR NOT a \20 the OR a b c OR d) AND NOT read write AND (the OR a) AND the
    def process_query(self, query):
        """
        In the following the query_tokens array as well as the index_lists dictionary will be important data structures.
        query_tokens is the array of operands which has the structure explained in the Tokenizer Class.
        index_lists is a dictionary of the processed index lists.
        For example, at the beginning the structures will look like this:
        query_tokens: [['NOT', ['term1'], 'OR', ['term2', 'term3']], ['NOT', ['term4', '\\3', 'term5']]]
        index_lists: {}
        After the first loop they will look like this:
        query_tokens: [['NOT', ['term1'], 'OR', ['#&0.1']], ['NOT', ['#&0.2']]]
        index_lists: {'#&0.1': [docID1, DocID2, ...], '#&0.2': [docID1, DocID2, ...]}
        After the second loop they will look like this:
        query_tokens: [['#&0.3'], ['#&0.4']]
        index_lists: {'#&0.1': [docID1, DocID2, ...], '#&0.2': [docID1, DocID2, ...],
                      '#&0.3': [docID1, DocID2, ...], '#&0.4': [docID3, DocID4, ...]}
        After that the tokens in the query_tokens list will get sorted by the size of the according index list in the
        index_lists dictionary.
        In the last step the index lists can be AND-Merged starting with the smallest two.
        """
        # tokenize the query and get array of operands
        query_tokens = self.tokenizer.tokenizeQuery(query)
        query_tokens = self.spelling_controller.check_query(query_tokens)
        index_lists = {}
        # resolve the proximity and phrase queries
        for query_part in query_tokens:
            for i in range(len(query_part)):
                r = re.compile(r'\\[0-9]+')
                filtered_part = list(filter(r.match, query_part[i]))
                if type(query_part[i]) is list and len(filtered_part) > 0:
                    result = self.merger.positional_intersect(query_part[i][0], query_part[i][2], int(query_part[i][1].replace("\\", "")))
                    result_id = "#&" + str(random.random())
                    index_lists[result_id] = result
                    query_part[i] = result_id
                elif type(query_part[i]) is list and len(query_part[i]) > 1:
                    result = self.merger.phrase_query(query_part[i])
                    result_id = "#&" + str(random.random())
                    index_lists[result_id] = result
                    query_part[i] = result_id

        # Resolve first the NOT and then the OR expressions in each query part.
        # If there are still terms in the query part after that,
        # then put the according index list in the index_lists array and put a reference in the query_tokens array
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

            if type(query_part[0]) is list:
                result = self.index.get_document_list(query_part[0][0])
                result_id = "#&" + str(random.random())
                index_lists[result_id] = result
                query_tokens[i][0] = result_id

        # Sort the remaining index_lists references in the query_tokens by their index list size
        sorted_query = []
        copied_query_tokens = copy.deepcopy(query_tokens)
        while len(copied_query_tokens) > 0:
            shortest = sys.maxsize
            shortest_index = 0
            for i in range(len(copied_query_tokens)):
                token = copied_query_tokens[i][0]
                if len(index_lists[token]) < shortest:
                    if len(index_lists[token]) == 0:
                        return []  # If one of the index_lists is [] we can instantly return [].
                    shortest = len(index_lists[token])
                    shortest_index = i
            sorted_query.append(copied_query_tokens[shortest_index][0])
            copied_query_tokens.pop(shortest_index)

        # AND-Merge the index lists starting with the smallest
        while len(sorted_query) != 1:
            result = self.merger.and_merge_fast(index_lists[sorted_query[0]], index_lists[sorted_query[1]])
            result_id = "#&" + str(random.random())
            index_lists[result_id] = result
            sorted_query[0] = result_id
            sorted_query.pop(1)

        return index_lists[sorted_query[0]]
