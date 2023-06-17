import re

class Tokenizer:
    def __init__(self):
        pass

    # Methode zum Aufteilen von Text in Wörter
    def tokenize(self, text):
        """
        Diese Methode nimmt einen Text als Eingabe, konvertiert ihn in Kleinbuchstaben,
        entfernt Sonderzeichen und Unterstriche und gibt eine Liste von Wörtern zurück.
        """
        text = text.lower()
        text = re.sub(r'[^\w\s\']|_', '', text)
        text = re.sub(r"\s'|'\s", ' ', text)
        return text.split()

    # (information OR data) AND analysis AND NOT retrieval AND Information \10 retrieval AND "library of congress"
    def tokenizeQuery(self, text):
        """
        This method tokenizes queries in the following way:
        Input query: (NOT tErM1 term2&- OR   term3) AND NOT term4 AND term5 \3 term6
        Output array:
        1st 2nd 3rd dimension
        [
            ['LEADING_NOT',
                ['term1', 'term2'],
            'OR',
                ['term3']
            ],
            ['AND_NOT',
                ['term4']
            ],
            [
                ['term5', '\\3', 'term6']
            ]
        ]
        1st dimension of the array are the operands that will be combined by an AND operation
        2nd dimension are the NOT and OR operations
        3rd dimension are the terms.
            One term in the 3rd dimension: Index list of this term can be read out of the index directly.
            Two terms with a \\x inbetween in the 3rd dimension: Index list needs to be processed with the positional intersect method
            Multiple terms in the 3rd dimension: Index list needs to be processed with the phrase query method
        """
        text = re.sub(r'["()]', '', text)
        tokens = text.split("AND")
        for i in range(len(tokens)):
            subquery = tokens[i]
            subquery = subquery.strip()
            subtokens = subquery.split()
            if len(subtokens) > 1:
                    a = 0
                    new_subtokens = []
                    while a < len(subtokens):
                        while subtokens[a] == "NOT" or subtokens[a] == "OR":
                            if subtokens[a + 1] == "NOT":
                                new_subtokens.append("OR_NOT")
                                a += 2
                            elif subtokens[a] == "NOT" and "OR" not in subtokens:
                                new_subtokens.append("AND_NOT")
                                a += 1
                            elif subtokens[a] == "NOT" and len(subtokens) > 2:
                                new_subtokens.append("LEADING_NOT")
                                a += 1
                            else:
                                new_subtokens.append(subtokens[a])
                                a += 1

                        # Find range of tokens (beginning and end)
                        b = a
                        while b < len(subtokens) and subtokens[b] != "NOT" and subtokens[b] != "OR":
                            b += 1
                        connected = []

                        # Normalize all tokens in range
                        for j in range(a, b):
                            subtokens[j] = subtokens[j].lower()
                            subtokens[j] = re.sub(r'[^\w\s\'\\]|_', '', subtokens[j])
                            subtokens[j] = re.sub(r"\s'|'\s", ' ', subtokens[j])
                            connected.append(subtokens[j])

                        new_subtokens.append(connected)
                        a = b
                    subtokens = new_subtokens
            else:
                subtokens[0] = subtokens[0].lower()
                subtokens[0] = re.sub(r'[^\w\s\']|_', '', subtokens[0])
                subtokens[0] = re.sub(r"\s'|'\s", ' ', subtokens[0])
                subtokens = [subtokens]
            tokens[i] = subtokens
        return tokens


    # Methode zum Aufteilen des Inhalts einer Datei in Wörter
    def tokenize_file(self, file_path):
        """
        Diese Methode nimmt den Pfad zu einer Datei als Eingabe, öffnet die Datei und liest ihren Inhalt.
        Der Inhalt wird dann an die `tokenize`-Methode übergeben, um ihn in Wörter aufzuteilen.
        Das Ergebnis, eine Liste von Wörtern, wird zurückgegeben.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return self.tokenize(content)