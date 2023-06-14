import sys
from tokenizer import *
from config import *

def main():
    # TODO: Create the vector space model

    # TODO: Evaluate the vector space model

    # TODO: Query the vector space model
    while True:
        sys.stdout.write('\nGeben Sie die Query ein: ')
        sys.stdout.flush()
        query = input()

        sys.stdout.write('\nGeben Sie den gewünschten Wert für Parameter k ein: ')
        sys.stdout.flush()
        k = input()

        if query or k in ("#quit", "#q", "#exit", "#e", "#close", "#c"):
            raise SystemExit

        # start_time = time.perf_counter()
        # TODO: Retrieve_k for given query and given K
        # elapsed_time = (time.perf_counter() - start_time) * 1e3

        # TODO: Print results and elapsed time
        # print(results)
        # print(f"Zeit zur Abarbeitung der Anfrage: {elapsed_time:.2f} ms\n")


if __name__ == '__main__':
    main()
