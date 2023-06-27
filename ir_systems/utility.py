import matplotlib.pyplot as plt
from tabulate import tabulate
from retrieval_metrics import *


class Utility:

    def __init__(self, vec_space_model, retrival_scorer, evaluation_index):
        self.vec_space_model = vec_space_model
        self.retrival_scorer = retrival_scorer
        self.evaluation_index = evaluation_index
    def __main__(self):
        pass

    def print_dictionary(self, dictionary_name, dictionary):
        # Get the keys and values from the dictionary
        keys = list(dictionary.keys())
        values = list(dictionary.values())

        # Determine the number of items to display (maximum 5)
        num_items = min(5, len(keys))

        # Print the length of the dictionary
        print(f"Length of {dictionary_name}: {len(dictionary)}")

        # Print the table header
        print("------------------------------------------------")

        # Print the first 5 key-value pairs
        for i in range(num_items):
            key = keys[i]
            value = values[i]
            print(f"| {key} | {value} |")

        # Print the table footer
        print("------------------------------------------------\n")

    def calculate_retrievals(self):
        retrievals = {}
        for key in self.evaluation_index.queries.keys():
            retrievals[key] = self.vec_space_model.retrieve(self.evaluation_index.queries[key])
        return retrievals

    def calculate_and_print_MAP(self):
        print("MAP:")
        print(self.retrival_scorer.MAP(list(self.evaluation_index.queries.values()),
                                  list(self.evaluation_index.relevant_documents.values())))

    def calculate_and_print_r_precision(self):
        print("\nR-Precision:")
        categories = []
        values = []
        for key in self.evaluation_index.queries.keys():
            relevant_documents = self.evaluation_index.relevant_documents[key]
            categories.append(str(key))
            values.append(str(self.retrival_scorer.rPrecision(relevant_documents, self.evaluation_index.queries[key])))
        print(tabulate([values], categories, tablefmt='fancy_grid'))

    def calculate_and_print_precision_recall_fscore_at_k(self, k_values):
        retrievals = self.calculate_retrievals()
        for k in k_values:
            at_k_categories = ['@{}:'.format(k)]
            precision_at_k_values = ['Precision']
            recall_at_k_values = ['Recall']
            fscore_at_k_values = ['F-Score']

            for key in self.evaluation_index.queries.keys():
                relevant_documents = self.evaluation_index.relevant_documents[key]
                at_k_categories.append(key)
                precision_at_k_values.append(str(precision(relevant_documents, retrievals[key][:k])))
                recall_at_k_values.append(str(recall(relevant_documents, retrievals[key][:k])))
                fscore_at_k_values.append(str(fscore(relevant_documents, retrievals[key][:k])))

            data = [precision_at_k_values, recall_at_k_values, fscore_at_k_values]
            print(tabulate(data, at_k_categories, tablefmt='fancy_grid'))

    def calculate_and_print_precision_recall_curve(self, curve_query_ids):
        for curve_query_id in curve_query_ids:
            self.retrival_scorer.eleven_point_precision_recall_curve(self.evaluation_index.queries[curve_query_id],
                                          self.evaluation_index.relevant_documents[curve_query_id])

    def calculate_and_print_eleven_point_average_precision(self):
        print("\nEleven point average precision:")
        categories = []
        values = []
        for key in self.evaluation_index.queries.keys():
            relevant_documents = self.evaluation_index.relevant_documents[key]
            categories.append(str(key))
            values.append(str(self.retrival_scorer.elevenPointAP(self.evaluation_index.queries[key], relevant_documents)[0]))
        print(tabulate([values], categories, tablefmt='fancy_grid'))
