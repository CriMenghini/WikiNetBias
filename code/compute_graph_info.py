import argparse

import pickle
import numpy as np
import pandas as pd
from collections import defaultdict

from metrics import Metrics
from LoadGraph import LoadGraph


parser = argparse.ArgumentParser(description='Process graphs.')
parser.add_argument('--topic', type=str, help='topic name')

args = parser.parse_args()

TOPIC = args.topic
RESULTS_FOLDER = 'data/results/'

graph = LoadGraph(TOPIC, 'data/graphs/')


kind = 'uniform'
metric = Metrics(graph, kind)

G = metric.S
line = [TOPIC, kind, len(G.nodes), len(graph.PARTITIONS['R']), len(graph.PARTITIONS['B']), len(graph.PARTITIONS['G']),
        len(G.edges), len(metric.EDGES_DISTR['RR']), len(metric.EDGES_DISTR['RB']), len(metric.EDGES_DISTR['RG']),
        len(metric.EDGES_DISTR['BR']), len(metric.EDGES_DISTR['BB']), len(metric.EDGES_DISTR['BG']), 
        len(metric.EDGES_DISTR['GR']), len(metric.EDGES_DISTR['GB']), len(metric.EDGES_DISTR['GG']),
        round(metric.OVERALL_DENSITY, 6), round(metric.PARTITIONS_DENSITY['R'], 6), round(metric.PARTITIONS_DENSITY['B'], 6),
        round(metric.PARTITIONS_DENSITY['G'], 6), round(metric.MODULARITY, 6), 
        len(metric.EDGES_DISTR['RR']) + len(metric.EDGES_DISTR['BR']) + len(metric.EDGES_DISTR['GR']),
        len(metric.EDGES_DISTR['RR']) + len(metric.EDGES_DISTR['RB']) + len(metric.EDGES_DISTR['RG']),
        len(metric.EDGES_DISTR['RB']) + len(metric.EDGES_DISTR['BB']) + len(metric.EDGES_DISTR['GB']),
        len(metric.EDGES_DISTR['BR']) + len(metric.EDGES_DISTR['BB']) + len(metric.EDGES_DISTR['BG'])]
reshaped_line = np.array(line).reshape(1, len(line))

    
node_centrality = defaultdict(int)
for n in G.nodes:
    for i,j in G.in_edges(n):
        node_centrality[n] += G[i][n]['weight']
        
within_same_color_centrality = {}
for n in G.nodes():
    r = 0
    b = 0
    for k,j in G.in_edges(n):
        if metric.NODE_COLOR[k] == 'R':
            r += G[k][n]['weight']
        elif metric.NODE_COLOR[k] == 'B':
            b += G[k][n]['weight']
    within_same_color_centrality[n] = {'r': r,
                                    'b': b}

color_neighbour = {}
for n in G.nodes:
    r = 0
    b = 0
    for k in G[n]:
        if metric.NODE_COLOR[k] == 'R':
            r += G[n][k]['weight']
        elif metric.NODE_COLOR[k] == 'B':
            b += G[n][k]['weight']
    color_neighbour[n] = {'r': r,
                         'b': b}
    
color_neighbour_prob = {}
for n in G.nodes:
    r = 0
    b = 0
    sum_deg = 0
    for k in G[n]:
        if metric.NODE_COLOR[k] == 'R':
            r += G[n][k]['weight']
            #sum_deg += G[n][k]['weight']
        elif metric.NODE_COLOR[k] == 'B':
            b += G[n][k]['weight']
            #sum_deg += G[n][k]['weight']
        sum_deg += G[n][k]['weight']
    if sum_deg >= 1:
        color_neighbour_prob[n] = {'r': r/sum_deg,
                                   'b': b/sum_deg}
    else:
        color_neighbour_prob[n] = {'r': 0,
                                   'b': 0}
        
with open(RESULTS_FOLDER + TOPIC + '_' + kind + '_node_centrality' + '.p', 'wb') as f:
    pickle.dump(node_centrality, f)
with open(RESULTS_FOLDER + TOPIC + '_' + kind + '_within_same_color_centrality' + '.p', 'wb') as f:
    pickle.dump(within_same_color_centrality, f)
with open(RESULTS_FOLDER + TOPIC + '_' + kind + '_color_neighbour' + '.p', 'wb') as f:
    pickle.dump(color_neighbour, f)
with open(RESULTS_FOLDER + TOPIC + '_' + kind + '_color_neighbour_prob' + '.p', 'wb') as f:
    pickle.dump(color_neighbour_prob, f)



df_info = pd.DataFrame(reshaped_line, columns=['topic', 'kind',
                                       'V', 'R', 'B', 'G',
                                      'E', 'ERR', 'ERB', 'ERG', 'EBR', 'EBB', 'EBG', 'EGR', 'EGB', 'EGG',
                                      'D_all', 'D_R', 'D_B', 'D_G', 
                                      'RB_modularity', 
                                      'indeg_R', 'oudeg_R', 'indeg_B', 'ourdeg_B'])


for topic, kind in [(TOPIC, 'occurrences'), (TOPIC, 'position'), (TOPIC, 'clicks')]:
    print(topic, kind)
    metric = Metrics(graph, kind)
    G = metric.S
    line = [TOPIC, kind, len(G.nodes), len(graph.PARTITIONS['R']), len(graph.PARTITIONS['B']), len(graph.PARTITIONS['G']),
        len(G.edges), len(metric.EDGES_DISTR['RR']), len(metric.EDGES_DISTR['RB']), len(metric.EDGES_DISTR['RG']),
        len(metric.EDGES_DISTR['BR']), len(metric.EDGES_DISTR['BB']), len(metric.EDGES_DISTR['BG']), 
        len(metric.EDGES_DISTR['GR']), len(metric.EDGES_DISTR['GB']), len(metric.EDGES_DISTR['GG']),
        round(metric.OVERALL_DENSITY, 6), round(metric.PARTITIONS_DENSITY['R'], 6), round(metric.PARTITIONS_DENSITY['B'], 6),
        round(metric.PARTITIONS_DENSITY['G'], 6), round(metric.MODULARITY, 6), 
        len(metric.EDGES_DISTR['RR']) + len(metric.EDGES_DISTR['BR']) + len(metric.EDGES_DISTR['GR']),
        len(metric.EDGES_DISTR['RR']) + len(metric.EDGES_DISTR['RB']) + len(metric.EDGES_DISTR['RG']),
        len(metric.EDGES_DISTR['RB']) + len(metric.EDGES_DISTR['BB']) + len(metric.EDGES_DISTR['GB']),
        len(metric.EDGES_DISTR['BR']) + len(metric.EDGES_DISTR['BB']) + len(metric.EDGES_DISTR['BG'])]
    reshaped_line = np.array(line).reshape(1, len(line))
    
    df_info = df_info.append(pd.DataFrame(reshaped_line, columns=['topic', 'kind',
                                       'V', 'R', 'B', 'G',
                                      'E', 'ERR', 'ERB', 'ERG', 'EBR', 'EBB', 'EBG', 'EGR', 'EGB', 'EGG',
                                      'D_all', 'D_R', 'D_B', 'D_G', 
                                      'RB_modularity', 
                                      'indeg_R', 'oudeg_R', 'indeg_B', 'ourdeg_B']), 
                                      ignore_index=True)


    node_centrality = defaultdict(int)
    for n in G.nodes:
        for i,j in G.in_edges(n):
            node_centrality[n] += G[i][n]['weight']
            
    within_same_color_centrality = {}
    for n in G.nodes():
        r = 0
        b = 0
        for k,j in G.in_edges(n):
            if metric.NODE_COLOR[k] == 'R':
                r += G[k][n]['weight']
            elif metric.NODE_COLOR[k] == 'B':
                b += G[k][n]['weight']
        within_same_color_centrality[n] = {'r': r,
                                        'b': b}

    color_neighbour = {}
    for n in G.nodes:
        r = 0
        b = 0
        for k in G[n]:
            if metric.NODE_COLOR[k] == 'R':
                r += G[n][k]['weight']
            elif metric.NODE_COLOR[k] == 'B':
                b += G[n][k]['weight']
        color_neighbour[n] = {'r': r,
                            'b': b}
        
    color_neighbour_prob = {}
    for n in G.nodes:
        r = 0
        b = 0
        sum_deg = 0
        for k in G[n]:
            if metric.NODE_COLOR[k] == 'R':
                r += G[n][k]['weight']
                #sum_deg += G[n][k]['weight']
            elif metric.NODE_COLOR[k] == 'B':
                b += G[n][k]['weight']
                #sum_deg += G[n][k]['weight']
            sum_deg += G[n][k]['weight']
        if sum_deg >= 1:
            color_neighbour_prob[n] = {'r': r/sum_deg,
                                    'b': b/sum_deg}
        else:
            color_neighbour_prob[n] = {'r': 0,
                                    'b': 0}
            
    with open(RESULTS_FOLDER + TOPIC + '_' + kind + '_node_centrality' + '.p', 'wb') as f:
        pickle.dump(node_centrality, f)
    with open(RESULTS_FOLDER + TOPIC + '_' + kind + '_within_same_color_centrality' + '.p', 'wb') as f:
        pickle.dump(within_same_color_centrality, f)
    with open(RESULTS_FOLDER + TOPIC + '_' + kind + '_color_neighbour' + '.p', 'wb') as f:
        pickle.dump(color_neighbour, f)
    with open(RESULTS_FOLDER + TOPIC + '_' + kind + '_color_neighbour_prob' + '.p', 'wb') as f:
        pickle.dump(color_neighbour_prob, f)
        

df_info.to_csv(RESULTS_FOLDER + TOPIC + '_info.tsv', sep='\t', index=None)