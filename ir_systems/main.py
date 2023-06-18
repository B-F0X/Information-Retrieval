import sys
from vec_space_model import *
from config import *
from utility import *


def main():
    # Create the vector space model
    vec_space_model = VectorSpaceModel()

    # Open and read the cisi file
    vec_space_model.open_and_read(collection_file)

    # Print the first 5 results of all the dictionaries
    utility = Utility()
    utility.print_dictionary("Dictionary", vec_space_model.dictionary)
    utility.print_dictionary("term_index_mapping", vec_space_model.term_index_mapping)
    utility.print_dictionary("doc_id_length_mapping", vec_space_model.doc_id_length_mapping)

    # TODO: Evaluate the vector space model
    test_abfragen = [...]  #Ersetzen durch Testabfragen
    erwartete_ergebnisse = [...]  #Ersetzen durch erwarteten Ergebnisse
    bewertungsergebnisse = vec_space_model.evaluate(test_abfragen, erwartete_ergebnisse)
    print(bewertungsergebnisse)

    # TODO: Query the vector space model
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
