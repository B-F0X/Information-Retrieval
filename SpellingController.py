import re
import copy
from config import *


class SpellingController:
    def __init__(self, index):
        self.positionalIndex = index

    def check_query(self, query):
        # Three for-loops to iterate through the third dimension of the array
        # (this structure is explained in the Tokenizer)
        for and_operand in range(len(query)):
            for or_operand in range(len(query[and_operand])):
                operand = query[and_operand][or_operand]
                if type(operand) is list:
                    for term_number in range(len(operand)):
                        term = operand[term_number]
                        # If the term is not known, and it is not of the format \\x
                        if len(self.positionalIndex.get_document_list(term)) < r_index and not re.match(r'\\[0-9]+', term):
                            # Split the query term into K-Grams and get the posting list for each K-Gram
                            amount_of_k_grams = len(self.positionalIndex.k_gram_index.split_to_k_grams(term))
                            k_gram_posting_lists = self.positionalIndex.k_gram_index.get_posting_lists(term)
                            k_gram_dictionary = {}
                            results = []
                            # Combine the posting lists to one dictionary where the key is a term and the value
                            # describes how often the term appeared in the posting lists
                            for posting_list in k_gram_posting_lists:
                                for posting in posting_list:
                                    if posting not in k_gram_dictionary:
                                        k_gram_dictionary[posting] = 1
                                    else:
                                        k_gram_dictionary[posting] += 1
                            # Calculate the jaccard coefficient for each term in the dictionary
                            # and move it into results if the jaccard coefficient is greater than the jaccard_threshold
                            for k_term, value in k_gram_dictionary.items():
                                jaccard = value / (amount_of_k_grams + self.positionalIndex.index[k_term].k_gram_size - value)
                                if jaccard > jaccard_threshold:
                                    results.append(k_term)

                            # Calculate the levenshtein distance for each term in the results array
                            # and choose the one with the smallest distance to the query string.
                            # If results is empty the wrongly spelled query term remains wrong.
                            #best_fitting_term = ""
                            #best_levenshtein_distance = sys.maxsize
                            best_fitting_terms = []
                            for k_term in results:
                                levenshtein_distance = self.levenshtein_distance(k_term, term)
                                i = 0
                                while i < len(best_fitting_terms) and levenshtein_distance > best_fitting_terms[i][1]:
                                    i += 1
                                best_fitting_terms.insert(i, [k_term, levenshtein_distance])

                            if len(best_fitting_terms) > 0:
                                best_queries = []
                                i = 1
                                for best_fitting_term in best_fitting_terms[:5]:
                                    print("{}. meinten Sie '{}' anstatt '{}'".format(i, best_fitting_term[0], term))
                                    i += 1
                                    copied_query = copy.deepcopy(query)
                                    copied_query[and_operand][or_operand][term_number] = best_fitting_term[0]
                                    best_queries.append(copied_query)
                                return best_queries
                            else:
                                print("Found no correction for '" + term + "'")
        return [query]

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

        return previous_row[-1]
