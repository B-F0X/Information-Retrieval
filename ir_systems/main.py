import sys
import matplotlib.pyplot as plt
from vec_space_model import *
from config import *
from utility import *
from retrieval_metrics import *
from evaluation_index import *
from tabulate import tabulate


def main():
    # Create the vector space model
    vec_space_model = VectorSpaceModel()
    retrival_scorer = RetrievalScorer(vec_space_model)
    evaluation_index = EvaluationIndex()

    # Open and read the cisi file
    vec_space_model.open_and_read(collection_file)

    # Print the first 5 results of all the dictionaries
    utility = Utility(vec_space_model, retrival_scorer, evaluation_index)
    utility.print_dictionary("Dictionary", vec_space_model.dictionary)
    utility.print_dictionary("term_index_mapping", vec_space_model.term_index_mapping)
    utility.print_dictionary("doc_id_length_mapping", vec_space_model.doc_id_length_mapping)

    utility.calculate_and_print_MAP()

    utility.calculate_and_print_r_precision()

    utility.calculate_and_print_eleven_point_average_precision()

    utility.calculate_and_print_precision_recall_fscore_at_k([5, 10, 20, 50])

    utility.calculate_and_print_precision_recall_curve([11, 14, 19, 20])

    while True:
        sys.stdout.write('\nGeben Sie die Query ein: ')
        sys.stdout.flush()
        query = input()

        sys.stdout.write('\nGeben Sie den gewünschten Wert für Parameter k ein: ')
        sys.stdout.flush()
        k = input()

        if query in ("#quit", "#q", "#exit", "#e", "#close", "#c") \
                or k in ("#quit", "#q", "#exit", "#e", "#close", "#c"):
            raise SystemExit

        start_time = time.perf_counter()
        results = vec_space_model.retrieve_k(query, int(k))
        elapsed_time = (time.perf_counter() - start_time) * 1e3

        print(results)
        print(f"Zeit zur Abarbeitung der Anfrage: {elapsed_time:.2f} ms\n")

if __name__ == '__main__':
    main()
