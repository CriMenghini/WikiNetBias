import argparse

import pickle
from collections import defaultdict

from LoadGraph import LoadGraph
from metrics import Metrics




neighborhood_complete_degree = defaultdict(set)
#neighborhood_complete_degree_ones = {}

count = 0
FOLDER = 'data/wikipedia_all/'
with open(FOLDER + 'idx_adj_lists.txt', 'r') as f:
    for l in f:
        o, i , w_order = l.split('\t')
        neighborhood_complete_degree[o].add(i)
        #neighborhood_complete_degree_ones[o] = 1
        
        if count%10000 == 0:
            print(count)
        count += 1
neighborhood_complete_degree_ = {}
for i,j in neighborhood_complete_degree.items():
    neighborhood_complete_degree_[i] = len(j)
with open('data/wikipedia_all/' +  'general_' + 'neighborhood' + '.p', 'wb') as f:
    pickle.dump(neighborhood_complete_degree_, f)
#with open('data/wikipedia_all/' +  'general_' + 'neighborhood_ones' + '.p', 'wb') as f:
#    pickle.dump(neighborhood_complete_degree_ones, f)