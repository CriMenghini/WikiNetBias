import os 
import ast
import time
import argparse

parser = argparse.ArgumentParser(description='Process graphs.')
parser.add_argument('--topic', type=str, help='topic name')

args = parser.parse_args()


FOLDER_PART = 'data/partitions/'
FOLDER_WIKI = 'data/wikipedia_all/'
FOLDER_GRAPHS = 'data/graphs/'
TOPIC = args.topic 

SIDES = ['R', 'B']#+ '.txt'

#ids = []
#for s in SIDES:
#    with open(FOLDER_PART + TOPIC + '_' + s + '.txt', 'r') as f:
#        for l in f:
#            el = l.split('\t')[1].strip()
#            ids.append(el)

#ids = set(ids)

t_start = time.time()
count = 1
with open(FOLDER_GRAPHS +  TOPIC + '.txt', 'w') as f_write:
    with open(FOLDER_WIKI + 'idx_adj_lists.txt', 'r') as f:
        for l in f:
            idx, adj = l.split('\t')
            replace_par = adj.strip().replace('(', '[').replace(')', ']')
            
            if len(replace_par) == 0: ad = set(list())
            else: ad = set(ast.literal_eval(replace_par))

            #constraint = idx in ids

            for link in ad:
                #if constraint:
                f_write.write(idx + '\t' + link + '\n')
                
                #if link in ids:
                #    f_write.write(idx + '\t' + link + '\n')
            
            if count%100000 == 0:
                print(count)
            count += 1


print('EXECUTION TIME: ', time.time() - t_start)