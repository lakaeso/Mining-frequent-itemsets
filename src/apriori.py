import itertools as it
from typing import List, Set


class Apriori:
    """Class which generates frequent itemsets with apriori algorithm based on given list of transactions."""

    def __init__(self, support_threshold: int):
        """Inits Apriori class instance, takes in ```support_threshold``` parameter."""
        self.support_threshold = support_threshold
        self.frequent_itemsets = []

    def _generate_candidates(self, L):
        """Generates candidates based on list of itemsets ```L```."""
        list_of_sets = list()
        combinations = list(it.combinations(L, 2))

        for (p, q) in combinations:
            c = p.union(q)
            if len(c) == len(p) + 1 and len(c) == len(q) + 1:
                list_of_sets.append(c)

        unique_sets = [set(s) for s in {frozenset(s) for s in list_of_sets}]

        return unique_sets

    def _generate_large_singleton_itemsets(self, transactions):
        """Generates singleton itemsets which satisfy ```>= support_threshold``` property.
        Used in a first step of the algorithm."""
        # init counter
        items_counter = {}

        # count all
        for i, transaction in enumerate(transactions):
            for item in transaction:
                if item in items_counter:
                    items_counter[item] += 1
                else:
                    items_counter[item] = 1
        
        # filter by counter
        L = [{item} for (item, count) in items_counter.items() if count >= self.support_threshold]

        # return L
        return L

    def fit(self, transactions: List[Set[str]]):
        """Fits Apriori class with data and generates frequent itemsets."""
        L = self._generate_large_singleton_itemsets(transactions)
        if len(L) > 0:
            self.frequent_itemsets.extend(L)
        k = 2

        while len(L) > 0:
            candidates = self._generate_candidates(L)
            counts = [0] * len(candidates)

            # count appearances in transactions
            for i, transaction in enumerate(transactions):
                for j, candidate in enumerate(candidates):
                    if candidate <= transaction:
                        counts[j] += 1
            
            # filter by support threshold
            L = [candidates[i] for i in range(len(candidates)) if counts[i] >= self.support_threshold]
            
            # save frequent itemsets
            if len(L) > 0:
                self.frequent_itemsets.extend(L)
            
            # increment k
            k += 1

    def get_frequent_itemsets(self):
        """Returns frequent itemsets."""
        return self.frequent_itemsets