import numpy as np
import pandas as pd


def precision(y_true, y_pred):
    """
        Calculates precision score for a list of relevant documents and the groundtruth.
        
        Parameters
        ----------
        y_true : list
            List of known relevant documents for a given query.
        y_pred : list
            List of retrieved documents.  
        
        Returns
        -------
        Score: float
            Precision = TP / (TP + FP)
    """

    y_true_set = set(y_true)
    y_pred_set = set(y_pred)

    tp = y_pred_set.intersection(y_true_set)
    fp = y_pred_set.difference(y_true_set)

    try:
        return len(tp) / (len(tp) + len(fp))
    except ZeroDivisionError:
        return 0.0


def recall(y_true, y_pred):
    """
        Calculates recall score for a list of relevant documents and the groundtruth.
        
        Parameters
        ----------
        y_true : list
            List of known relevant documents for a given query.
        y_pred : list
            List of retrieved documents.  
        
        Returns
        -------
        Score: float
            Recall = TP / (TP + FN)
    """

    y_true_set = set(y_true)
    y_pred_set = set(y_pred)

    tp = y_pred_set.intersection(y_true_set)
    fn = y_true_set.difference(y_pred_set)

    try:
        return len(tp) / (len(tp) + len(fn))
    except ZeroDivisionError:
        return 0.0


def fscore(y_true, y_pred, beta=1.0):
    """
        Calculates f-measure for a list of relevant documents and the groundtruth.
        
        Parameters
        ----------
        y_true : list
            List of known relevant documents for a given query.
        y_pred : list
            List of retrieved documents.  
        beta : float
            beta parameter weighting precision vs. recall
        
        Returns
        -------
        Score: float
            F-Measure = (1 + beta^2) \cdot \frac{Precision \cdot Recall}{beta^2 \cdot Precision+Recal}
    """

    calculated_precision = precision(y_true, y_pred)
    calculated_recall = recall(y_true, y_pred)

    try:
        return (1 + beta ** 2) * ((calculated_precision * calculated_recall) /
                                  ((beta ** 2 * calculated_precision) + calculated_recall))
    except ZeroDivisionError:
        return 0.0


def precision_recall_fscore(y_true, y_pred, beta=1.0):
    """
        Convenience function, calculating precision, recall and f-measure.
        
        Parameters
        ----------
        y_true : list
            List of known relevant documents for a given query.
        y_pred : list
            List of retrieved documents.  
        beta : float
            beta parameter weighting precision vs. recall
        
        Returns
        -------
        Score: tuple
            (precision, recall, f-measure)
    """

    return precision(y_true, y_pred), recall(y_true, y_pred), fscore(y_true, y_pred, beta)


class RetrievalScorer:
    """
    Retrieval score system. 
    Provides functions like RScore, Average Precision and Mean-Average-Precision. 

    Attributes
    ----------
    retrieval_system : class object
           A Retrieval system. Must implement the abstract class InitRetrievalSystem.
    Methods
    -------
    rPrecision(y_true, query)
        Calculate the RScore.
    aveP(query, groundtruth)
        Calculate the average precision score for a query.
    MAP(queries, groundtruths)
        Calculate the mean average precision for a list of queries.

    """
    def __init__(self, system):
        """
        Initializes a RetrievalScorer class object
        
        Parameters
        ----------
        system : class object
            A retrieval system that implements InitRetrievalSystem.
        """

        self.retrieval_system = system
    
    def rPrecision(self, y_true, query):
        """
        Calculates the precision at R where R denotes the number of all relevant
        documents to a given query.
        
        Parameters
        ----------
        y_true : list
            List of known relevant documents for a given query.
        query : str
            A query.

        Returns
        -------
        Score: float
            R-precision = TP / (TP + FN)
        """

        result = self.retrieval_system.retrieve_k(query, len(y_true))
        y_pred_set = set([res[0] for res in result])
        y_true_set = set(y_true)

        tp = y_pred_set.intersection(y_true_set)

        try:
            return len(tp) / len(y_true_set)
        except ZeroDivisionError:
            return 0.0

    def elevenPointAP(self, query, y_true):
        """
        Calculate the 11-point average precision score.

        Parameters
        ----------
        y_true : list
            List of known relevant documents for a given query.
        query : str
            A query.

        Returns
        -------
        Tuple: (float, list, list)
            (11-point average precision score, recall levels, precision levels).
        """
        #Abrufen Ergebnisse fuer Abfrage
        results = self.retrieve_k(query, len(y_true))

        #Initialisierung von Variablen fuer Berechnung der 11point..
        relevant_results = 0
        precision_levels = []
        recall_levels = np.linspace(0.0, 1.0, 11)  #Festgelegte recalllvl Parameter
        
        #Durchlaufen Ergebnisse
        for i, result in enumerate(results, start=1):
            #Ergebnis in  y_true-Liste ist dann ist es relevant
            if result in y_true:
                relevant_results += 1
                
            precision = relevant_results / i
            recall = relevant_results / len(y_true)
            
            #Wenn aktuelle Abruf gleich oder groesser als das naechste recall lvl ist speichert man die precision
            if recall >= recall_levels[len(precision_levels)]:
                precision_levels.append(precision)

        #Wenn nicht alle relevant realls erreicht, fuellt man restliche preciscion levels mit 0 auf
        while len(precision_levels) < 11:
            precision_levels.append(0.0)

        #Berechnung der 11point...
        average_precision = sum(precision_levels) / 11

        return average_precision, list(recall_levels), precision_levels


    def MAP(self, queries, groundtruths):
        """
        Calculate the mean average precision.

        Parameters
        ----------
        groundtruths : list(list)
            A double nested list. Each entry contains a list of known relevant documents for a given query.
        queries : list(str)
            A list of queries. Each query maps exactly to one groundtruth list in groundtruths.

        Returns
        -------
        Score: float
            MAP = frac{1}{|Q|} \cdot \sum_{q \in Q} AP(q).
        """
        #Liste zur Speicherung der avg precisions fuer jede Abfrage
        average_precisions = []
        
        #Durchlaufen der Abfragen und dazugehoerige groundtruths
        for query, groundtruth in zip(queries, groundtruths):
            #Abrufen der Ergebnisse 
            results = self.retrieve_k(query, len(groundtruth))
            
            #Initialisierung von Var fuer Berechnung der avg precision
            relevant_results = 0
            cumulative_precision = 0
            
            #Durchlaufen der Ergebnisse
            for i, result in enumerate(results, start=1):
                #Ergbeniss ist relevant wenn in groundtruth Liste ist
                if result in groundtruth:
                    relevant_results += 1
                    cumulative_precision += relevant_results / i
                    
            #Berechnung avg precisions fuer Abfrage
            average_precision = cumulative_precision / len(groundtruth) if groundtruth else 0
            average_precisions.append(average_precision)
        
        #Berechnung&Rueckgabe der Mean Average Precision
        return sum(average_precisions) / len(average_precisions)

