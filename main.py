import sys
import operator
from QueryProcessor import *
from Collection import *


def print_docs(documents):
    print("\nDie ersten 3 Dokumente:\n")
    count = 0
    for doc in documents:
        if count >= 3:
            break
        print("ID:", doc.doc_id)
        print("Abstract:", doc.abstract)
        print("-----------------------")
        count += 1


def print_index(index):
    print("\nDie ersten 3 Indices\n")
    count = 0
    for term, indexes in index.index.items():
        if count >= 3:
            break
        print("Term:", term)
        print("Documents:", indexes.get_document_list())
        print("-----------------------")
        count += 1


def print_dictionary(dictionary):
    sorted_dict = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    print("\nTop 5 häufigste Wörter:\n")
    for i in range(5):
        if i >= len(sorted_dict):
            break
        word, count = sorted_dict[i]
        print("Wort:", word)
        print("Anzahl:", count)
        print("-----------------------")


def main():
    # Nutzung der Collection-Klasse
    file_path = "cisi/CISI.ALL"
    collection = Collection(file_path)
    collection.open_and_read()

    # Ausgabe der eingelesenen Dokumente
    print_docs(collection.documents)
    print_index(collection.index)
    print_dictionary(collection.dictionary)
    # Initialisierung des Suchanfragenverarbeiters
    query_processor = QueryProcessor(collection.index, collection.get_document_count())

    # Loop für die Verarbeitung von Suchanfragen
    # Output muss geflushed werden, da die Reihenfolge der Prints sonst nicht deterministisch ist
    while True:
        sys.stdout.write('Geben Sie Ihre Suchanfrage ein: ')
        sys.stdout.flush()
        query = input()
        result = query_processor.process_query(query)
        print(result)
        print('\n')


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
