import os
import pickle
import pandas as pd
from collections import defaultdict

class LoadGraph(object):
    def __init__(self, topic, file_edges):
        self.t = topic
        self.FILE_EDGES = file_edges

        # Get edges
        with open(self.FILE_EDGES  + 'edges_' + self.t + '.p', 'rb') as f_pickle_info:
            edges = pickle.load(f_pickle_info)
        self.EDGES = list(edges)
        print('Edges loaded.')
        # Get partitions
        self.get_list_pol_partition()
        print('Red and blue partitions.')
        # Final partitions
        self.complementary_partition()
        print('All nodes partitioned.')

    def load_edges(self, kind='uniform'):
        """Return set of edges unweighted
        """

        df_edges = pd.DataFrame(self.EDGES, columns=['anchor', 'target', 'uniform',
                                                         'position', 'clicks'])
        
        if kind == 'uniform' or kind == 'occurrences':
            occ_edges = df_edges.groupby(['anchor','target']).size().reset_index(name='occ')
            occ_edges['unif'] = [1]*len(occ_edges)
            if kind == 'uniform':
                EDGES =  list(occ_edges[['anchor', 'target', 'unif']].itertuples(index=False, name=None))
            else:
                EDGES =  list(occ_edges[['anchor', 'target', 'occ']].itertuples(index=False, name=None))
        elif kind == 'position':
            df_pos = df_edges[['anchor','target', 'position']].groupby(['anchor','target']).agg(max).reset_index()
            EDGES = list(df_pos.itertuples(index=False, name=None))
        elif kind == 'clicks':
            df_click = df_edges[['anchor','target', 'clicks']].groupby(['anchor','target']).agg(sum).reset_index()
            EDGES = list(df_click.itertuples(index=False, name=None))
        
        del df_edges
        return EDGES

    def get_list_pol_partition(self):
        """ For polarized partitions we get the list of nodes
        """
        
        self.PARTITIONS = defaultdict(set)
        for s in ['R', 'B']:
            with open('data/partitions/' + self.t + '_' + s + '.txt', 'r') as f:
                for l in f:
                    idx = l.split('\t')[1].strip()
                    self.PARTITIONS[s].add(idx) 

         

    def complementary_partition(self):
        """ The nodes that belong both to red and blue are assigned to green
        """
        
        overlapping = set(self.PARTITIONS['R']).intersection(set(self.PARTITIONS['B']))

        print('OVERMERDAPPING: ', overlapping)
    
        for o in overlapping:
            self.PARTITIONS['R'].remove(o)
            self.PARTITIONS['B'].remove(o)
            self.PARTITIONS['G'].add(o)
        
        union_topic = set(self.PARTITIONS['R']).union(set(self.PARTITIONS['B']))
        for o, i, w, w1, w2 in self.EDGES:
            if o not in union_topic:
                self.PARTITIONS['G'].add(o)

            if i not in union_topic:
                self.PARTITIONS['G'].add(i)


    