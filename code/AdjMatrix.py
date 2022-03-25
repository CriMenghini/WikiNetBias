from LoadGraph import LoadGraph
from metrics import Metrics

import numpy as np
import pandas as pd

import pickle
from scipy.sparse import diags, vstack, hstack, lil_matrix, csr_matrix
import networkx as nx
import argparse

parser = argparse.ArgumentParser(description='Process graphs.')
parser.add_argument('--topic', type=str, help='topic name')

args = parser.parse_args()

TOPIC = args.topic
graph = LoadGraph(TOPIC, 'data/graphs/')
RESULTS_FOLDER = 'data/results/'


graph = LoadGraph(TOPIC, 'data/graphs/')
metric = Metrics(graph, 'uniform')

node_color = metric.NODE_COLOR

print(node_color['37600900'])

node_id = {n:i for i,n in enumerate(list(metric.S.nodes))}
id_node = {i:n for n,i in node_id.items()}

#with open('data/wikipedia_all/'  + 'general_' + 'neighborhood' + '.p', 'rb') as f_pickle_info:
#    neighborhood_complete_degree = dict(pickle.load(f_pickle_info))


with open('data/wikipedia_all/'  + 'position_len.p', 'rb') as f_pickle_info:
    dict_position_doc = dict(pickle.load(f_pickle_info))
    
with open('data/graphs/info_edges_' + TOPIC + '.p', 'rb') as f_pickle_info:
    info_edges = pickle.load(f_pickle_info)
    
with open(RESULTS_FOLDER + TOPIC + '_' + 'clicks_' + 'neighborhood_super_entrance' + '.p', 'rb') as f:
    neighborhood_super_entrance = pickle.load(f)
    
with open(RESULTS_FOLDER + TOPIC + '_' + 'clicks_' + 'neighborhood_entrance_from_super' + '.p', 'rb') as f:
    neighborhood_entrance_from_super = pickle.load(f)


for k in ['uniform', 'position', 'clicks']:
    if k == 'uniform':
        print(k)
        graph = LoadGraph(TOPIC, 'data/graphs/')
        metric = Metrics(graph, k)

        edges = graph.EDGES
        df_edges = pd.DataFrame(edges, columns=['anchor', 'target', 'uniform',
                                                                'position', 'clicks'])
        df_size = df_edges[['anchor','target', 'position']].groupby(['anchor']).size()

            
        node_color = metric.NODE_COLOR
        node_id = {n:i for i,n in enumerate(list(metric.S.nodes))}
        id_node = {i:n for n,i in node_id.items()}

        # Get nodes
        red = set(set(graph.PARTITIONS['R']).intersection(set(list(metric.S.nodes))))
        blue = set(graph.PARTITIONS['B']).intersection(set(list(metric.S.nodes)))
        # Add edges to supernode
        green = [node_id[n] for n in set(list(metric.S.nodes)).difference(red.union(blue)) if n in metric.S.nodes]

        # Adjacency matrix
        A = nx.adjacency_matrix(metric.S)
        A = A.astype(float)
        # Get sinks
        sinks = np.where(np.array(A.sum(axis=1)) == 0)[0]
        red_id = [node_id[r] for r in red]
        red_sinks = list(set(red_id).intersection(set(list(sinks))))
        blue_id = [node_id[b] for b in blue]
        blue_sinks = list(set(blue_id).intersection(set(list(sinks))))
        green_sink = list(set(green).intersection(set(list(sinks))))
        print('red sinks: ', len(red_sinks), 'blue sinks: ', len(blue_sinks), 'green sinks: ', len(green_sink))
        green_not_sink = list(set(green).difference(set(list(sinks))))

        # not Sinks probabilities to super node
        neig_to_supernodes = {}
        if k == 'uniform':
            for i in green_not_sink:
                diff = df_size[id_node[i]] - np.sum(A[i])
                if diff < 0:
                    neig_to_supernodes[i] = 0
                else:
                    neig_to_supernodes[i] = diff
                #else:
                #    neig_to_supernodes[i] = 1

        # Add rest of Wiki super node
        C = hstack([A, np.zeros((A.shape[0], 1))])
        C = lil_matrix(vstack([C, np.zeros((1,C.shape[1],))]))
        assert len(green_not_sink) == len([neig_to_supernodes[i] for i in green_not_sink])
        C[green_not_sink, -1] = [neig_to_supernodes[i] for i in green_not_sink]
        # Connect sinks with super node
        C[red_sinks, -1] = 1
        C[blue_sinks, -1] = 1
        C[green_sink, -1] = 1

        #Connect super node to itself and green nodes
        beta = info_edges['across_outside']/(info_edges['across_outside'] + info_edges['toward_green'])
        C[-1, green] = (1-beta)/len(green)
        C[-1, -1] = beta


        # Normalize weights
        p = [1/i[0] for i in np.array(C.sum(axis=1))[:]]
        D = diags(p, offsets=0) @ C

        D[red_sinks, -1] = 0
        D[blue_sinks, -1] = 0
        D[green_sink, -1] = 0

        with open('data/adj_matrix/' + TOPIC + '_' + k + '_' + '_adj_matrix.p', 'wb') as f_pickle_info:
            pickle.dump(D, f_pickle_info)
        with open('data/adj_matrix/' + TOPIC + '_' + k + '_' + 'node_id.p', 'wb') as f_pickle_info:
            pickle.dump(node_id, f_pickle_info)
        with open('data/adj_matrix/' + TOPIC + '_' + k + '_' + 'node_color.p', 'wb') as f_pickle_info:
            pickle.dump(node_color, f_pickle_info)

    elif k=='position':
        print(k)
        graph = LoadGraph(TOPIC, 'data/graphs/')
        metric = Metrics(graph, k)

        node_color = metric.NODE_COLOR
        node_id = {n:i for i,n in enumerate(list(metric.S.nodes))}
        id_node = {i:n for n,i in node_id.items()}

        # Get nodes
        red = set(set(graph.PARTITIONS['R']).intersection(set(list(metric.S.nodes))))
        blue = set(graph.PARTITIONS['B']).intersection(set(list(metric.S.nodes)))
        # Add edges to supernode
        green = [node_id[n] for n in set(list(metric.S.nodes)).difference(red.union(blue)) if n in metric.S.nodes]

        # Adjacency matrix
        A = nx.adjacency_matrix(metric.S)
        A = A.astype(float)
        # Get sinks
        sinks = np.where(np.array(A.sum(axis=1)) == 0)[0]
        red_id = [node_id[r] for r in red]
        red_sinks = list(set(red_id).intersection(set(list(sinks))))
        blue_id = [node_id[b] for b in blue]
        blue_sinks = list(set(blue_id).intersection(set(list(sinks))))
        green_sink = list(set(green).intersection(set(list(sinks))))
        print('red sinks: ', len(red_sinks), 'blue sinks: ', len(blue_sinks), 'green sinks: ', len(green_sink))
        green_not_sink = list(set(green).difference(set(list(sinks))))
        red_not_sink = list(set(red_id).difference(set(list(sinks))))
        blue_not_sink = list(set(blue_id).difference(set(list(sinks))))

        neig_to_supernodes = {}
        for i in green_not_sink:
            no_zero = A[i].nonzero()[1]
            positions = list(A[i,no_zero].toarray()[0])
            
            len_adj = dict_position_doc[id_node[i]]
            
            scaled_positions = list(np.tanh([p/len_adj for p in positions]))
            to_super_node = list(np.tanh([i/len_adj for i in range(1,len_adj) if i not in positions]))
            
            sum_to_normalize = np.sum(scaled_positions) + np.sum(to_super_node)
            scaled_final_positon = np.array(scaled_positions)/sum_to_normalize
            scaled_supernode_positon = np.array(to_super_node)/sum_to_normalize
            
            neig_to_supernodes[i] = np.sum(scaled_supernode_positon)
            A[i, no_zero] = scaled_final_positon

        for i in red_not_sink:
            no_zero = A[i].nonzero()[1]
            positions = list(A[i,no_zero].toarray()[0])
            
            len_adj = len(positions)
            
            scaled_positions = list(np.tanh([p/len_adj for p in positions]))
            #to_super_node = list(np.tanh([i/len_adj for i in range(1,len_adj) if i not in positions]))
            
            sum_to_normalize = np.sum(scaled_positions) #+ np.sum(to_super_node)
            scaled_final_positon = np.array(scaled_positions)/sum_to_normalize
            #scaled_supernode_positon = np.array(to_super_node)/sum_to_normalize
            
            #neig_to_supernodes[i] = np.sum(scaled_supernode_positon)
            A[i, no_zero] = scaled_final_positon

        for i in blue_not_sink:
            no_zero = A[i].nonzero()[1]
            positions = list(A[i,no_zero].toarray()[0])
            
            len_adj = len(positions)
            
            scaled_positions = list(np.tanh([p/len_adj for p in positions]))
            #to_super_node = list(np.tanh([i/len_adj for i in range(1,len_adj) if i not in positions]))
            
            sum_to_normalize = np.sum(scaled_positions) #+ np.sum(to_super_node)
            scaled_final_positon = np.array(scaled_positions)/sum_to_normalize
            #scaled_supernode_positon = np.array(to_super_node)/sum_to_normalize
            
            #neig_to_supernodes[i] = np.sum(scaled_supernode_positon)
            A[i, no_zero] = scaled_final_positon
        
        # Add rest of Wiki super node
        C = hstack([A, np.zeros((A.shape[0], 1))])
        C = lil_matrix(vstack([C, np.zeros((1,C.shape[1],))]))
        assert len(green_not_sink) == len([neig_to_supernodes[i] for i in green_not_sink])
        C[green_not_sink, -1] = [neig_to_supernodes[i] for i in green_not_sink]


        # Connect sinks with super node
        C[red_sinks, -1] = 1
        C[blue_sinks, -1] = 1
        C[green_sink, -1] = 1

        #Connect super node to itself and green nodes
        beta = info_edges['across_outside']/(info_edges['across_outside'] + info_edges['toward_green'])
        C[-1, green] = (1-beta)/len(green)
        C[-1, -1] = beta


        # Normalize weights
        p = [1/i[0] for i in np.array(C.sum(axis=1))[:]]
        D = diags(p, offsets=0) @ C

        D[red_sinks, -1] = 0
        D[blue_sinks, -1] = 0
        D[green_sink, -1] = 0

        with open('data/adj_matrix/' + TOPIC + '_' + k + '_' + '_adj_matrix.p', 'wb') as f_pickle_info:
            pickle.dump(D, f_pickle_info)
        with open('data/adj_matrix/' + TOPIC + '_' + k + '_' + 'node_id.p', 'wb') as f_pickle_info:
            pickle.dump(node_id, f_pickle_info)
        with open('data/adj_matrix/' + TOPIC + '_' + k + '_' + 'node_color.p', 'wb') as f_pickle_info:
            pickle.dump(node_color, f_pickle_info)

    elif k=='clicks':
        print(k)
        graph = LoadGraph(TOPIC, 'data/graphs/')
        metric = Metrics(graph, k)    
        node_color = metric.NODE_COLOR
        node_id = {n:i for i,n in enumerate(list(metric.S.nodes))}
        id_node = {i:n for n,i in node_id.items()}

        # Get nodes
        red = set(set(graph.PARTITIONS['R']).intersection(set(list(metric.S.nodes))))
        blue = set(graph.PARTITIONS['B']).intersection(set(list(metric.S.nodes)))
        # Add edges to supernode
        green = [node_id[n] for n in set(list(metric.S.nodes)).difference(red.union(blue)) if n in metric.S.nodes]

        # Adjacency matrix
        A = nx.adjacency_matrix(metric.S)
        A = A.astype(float)
        # Get sinks
        sinks = np.where(np.array(A.sum(axis=1)) == 0)[0]
        red_id = [node_id[r] for r in red]
        red_sinks = list(set(red_id).intersection(set(list(sinks))))
        blue_id = [node_id[b] for b in blue]
        blue_sinks = list(set(blue_id).intersection(set(list(sinks))))
        green_sink = list(set(green).intersection(set(list(sinks))))
        print('red sinks: ', len(red_sinks), 'blue sinks: ', len(blue_sinks), 'green sinks: ', len(green_sink))
        green_not_sink = list(set(green).difference(set(list(sinks))))
        red_not_sink = list(set(red_id).difference(set(list(sinks))))
        blue_not_sink = list(set(blue_id).difference(set(list(sinks))))

        # Sinks probabilities to super node
        neig_to_supernodes = {}
        for i in green_not_sink:
            neig_to_supernodes[i] = neighborhood_super_entrance[id_node[i]]


        # Add rest of Wiki super node
        C = hstack([A, np.zeros((A.shape[0], 1))])
        C = lil_matrix(vstack([C, np.zeros((1,C.shape[1],))]))
        assert len(green_not_sink) == len([neig_to_supernodes[i] for i in green_not_sink])
        C[green_not_sink, -1] = [neig_to_supernodes[i] for i in green_not_sink]


        # Connect sinks with super node
        C[red_sinks, -1] = 1
        C[blue_sinks, -1] = 1
        C[green_sink, -1] = 1

        #Connect super node to itself and green nodes
        beta = info_edges['across_outside']/(info_edges['across_outside'] + info_edges['toward_green'])
        C[-1, green] = (1-beta)/len(green)
        C[-1, -1] = beta


        # Normalize weights
        p = [1/i[0] for i in np.array(C.sum(axis=1))[:]]
        D = diags(p, offsets=0) @ C

        D[red_sinks, -1] = 0
        D[blue_sinks, -1] = 0
        D[green_sink, -1] = 0

        with open('data/adj_matrix/' + TOPIC + '_' + k + '_' + '_adj_matrix.p', 'wb') as f_pickle_info:
            pickle.dump(D, f_pickle_info)
        with open('data/adj_matrix/' + TOPIC + '_' + k + '_' + 'node_id.p', 'wb') as f_pickle_info:
            pickle.dump(node_id, f_pickle_info)
        with open('data/adj_matrix/' + TOPIC + '_' + k + '_' + 'node_color.p', 'wb') as f_pickle_info:
            pickle.dump(node_color, f_pickle_info)

    
   