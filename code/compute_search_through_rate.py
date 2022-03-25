import argparse

import pickle
from collections import defaultdict

from LoadGraph import LoadGraph
from metrics import Metrics


parser = argparse.ArgumentParser(description='Process graphs.')
parser.add_argument('--topic', type=str, help='topic name')

args = parser.parse_args()

TOPIC = args.topic
RESULTS_FOLDER = 'data/results/'

graph = LoadGraph(TOPIC, 'data/graphs/')
metric = Metrics(graph, 'clicks')
G = metric.S

with open('data/wikipedia_all/'  + 'en_enter_external.p', 'rb') as f_pickle_info:
    en_enter_external = dict(pickle.load(f_pickle_info))

with open('data/wikipedia_all/'  + 'en_clickstreams.p', 'rb') as f_pickle_info:
    clickstream_dictionary = dict(pickle.load(f_pickle_info))
    
node_color = metric.NODE_COLOR
    
neighborhood_super_entrance = defaultdict(int)
neighborhood_entrance_from_super = defaultdict(int)

for i,j in clickstream_dictionary.items():
    try:
        node_color[i[0]]
        try:
            node_color[i[1]]
        except KeyError:
            if node_color[i[0]]=='G':
                neighborhood_super_entrance[i[0]] += j   
    except KeyError:
        try:
            node_color[i[1]]
            if node_color[i[1]]=='G':
                neighborhood_entrance_from_super[i[1]] += j   
        except KeyError:
            continue
print('Neigh done')

exit_node = defaultdict(int)
for n in G.nodes():
    for i,j in G.out_edges(n):
        if G[n][j]['weight']>10:
            exit_node[n] += G[n][j]['weight']
        else:
            exit_node[n] += 0
            
        if node_color[n] == 'G':
            exit_node[n] += neighborhood_super_entrance[n]
print('Exit done')
total_entrance_node = defaultdict(int)
for n in G.nodes():
    try:
        total_entrance_node[n] = en_enter_external[n]
    except KeyError:
        total_entrance_node[n] = 0
print('Total entrance done')
entrance_node = defaultdict(int)
for n in G.nodes():
    for i,j in G.in_edges(n):
        if G[i][n]['weight']>10:
            entrance_node[n] += G[i][n]['weight']
        else:
            entrance_node[n] += 0
            
        if node_color[n] == 'G':
            entrance_node[n] += neighborhood_entrance_from_super[n]
print('Entrance internal done')
search_rate = {}
for n in G.nodes():
    if total_entrance_node[n]+entrance_node[n]!=0:
        rate = total_entrance_node[n]/(total_entrance_node[n]+entrance_node[n])
        if 0 < rate < 1:
            search_rate[n] = rate
        elif rate >= 1:
            search_rate[n] = 1
        else:
            search_rate[n] = 0
    else:
        search_rate[n] = 0
print('Search done')
click_through = {}
for n in G.nodes():
    if total_entrance_node[n]+entrance_node[n]!=0:
        click = exit_node[n]/(total_entrance_node[n]+entrance_node[n])
        if 0 < click < 1:
            click_through[n] = click
        elif click >= 1:
            click_through[n] = 1
        else:
            click_through[n] = 0
    else:
        click_through[n] = 0
print('Click done')
with open(RESULTS_FOLDER + TOPIC + '_' + 'clicks_' + 'neighborhood_super_entrance' + '.p', 'wb') as f:
    pickle.dump(neighborhood_super_entrance, f)
with open(RESULTS_FOLDER + TOPIC + '_' + 'clicks_' + 'neighborhood_entrance_from_super' + '.p', 'wb') as f:
    pickle.dump(neighborhood_entrance_from_super, f)
with open(RESULTS_FOLDER + TOPIC + '_' + 'clicks_' + 'exit_node' + '.p', 'wb') as f:
    pickle.dump(exit_node, f)
with open(RESULTS_FOLDER + TOPIC + '_' + 'clicks_' + 'total_entrance_node' + '.p', 'wb') as f:
    pickle.dump(total_entrance_node, f)
with open(RESULTS_FOLDER + TOPIC + '_' + 'clicks_' + 'entrance_node' + '.p', 'wb') as f:
    pickle.dump(entrance_node, f)   
with open(RESULTS_FOLDER + TOPIC + '_' + 'clicks_' + 'search_rate' + '.p', 'wb') as f:
    pickle.dump(search_rate, f) 
with open(RESULTS_FOLDER + TOPIC + '_' + 'clicks_' + 'click_through' + '.p', 'wb') as f:
    pickle.dump(click_through, f) 