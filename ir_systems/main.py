import sys

def main():
    # Nutzung der Collection-Klasse
    #file_path = collection_file
    #collection = Collection(file_path)

    # Messe die benötigte Zeit zum Aufbauen des Index
    #start_time = time.perf_counter()
    #collection.open_and_read()
    #elapsed_time = (time.perf_counter() - start_time) * 1e3
    #print(f"Zeit zum Aufbau des Index: {elapsed_time:.2f} ms")

    # Ausgabe der eingelesenen Dokumente
    #print_docs(collection.documents)
    #print_index(collection.index)
    #print_dictionary(collection.dictionary)

    # Initialisierung des Suchanfragenverarbeiters
    #query_processor = QueryProcessor(collection.index, collection.get_document_count())

    # Loop für die Verarbeitung von Suchanfragen
    # Output muss geflushed werden, da die Reihenfolge der Prints sonst nicht deterministisch ist
    while True:
        sys.stdout.write('\nGeben Sie Ihre Suchanfrage ein: ')
        sys.stdout.flush()
        query = input()

        if query in ("#quit", "#q", "#exit", "#e", "#close", "#c"):
            raise SystemExit

        #start_time = time.perf_counter()
        #results = query_processor.process_query(query)
        #elapsed_time = (time.perf_counter() - start_time) * 1e3

        #print(results)
        #print(f"Zeit zur Abarbeitung der Anfrage: {elapsed_time:.2f} ms\n")


if __name__ == '__main__':
    main()