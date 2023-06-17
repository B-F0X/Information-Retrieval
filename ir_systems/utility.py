class Utility:
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
