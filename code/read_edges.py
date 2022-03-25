import time
import pickle
import argparse




parser = argparse.ArgumentParser(description='Process graphs.')
parser.add_argument('--topic', type=str, help='topic name')

args = parser.parse_args()

FOLDER = 'data/wikipedia_all/'
FOLDER_PART = 'data/partitions/'
FOLDER_WIKI = 'data/wikipedia_all/'
FOLDER_GRAPHS = 'data/graphs/'
TOPIC = args.topic 

SIDES = ['R', 'B']#+ '.txt'

ids = set()
for s in SIDES:
    with open(FOLDER_PART + TOPIC + '_' + s + '.txt', 'r') as f:
        for l in f:
            el = l.split('\t')[1].strip()
            ids.add(el)


print('37600898' in ids)

# 'en' stays for the language
with open(FOLDER_WIKI  + 'en_clickstreams.p', 'rb') as f_pickle_info:
    clickstreams = dict(pickle.load(f_pickle_info))


green = set()
toward_green = 0
outside_green = 0
across_outside = 0
w_toward_green = 0
w_outside_green = 0
w_across_outside = 0


s = time.time()
count = 0
with open(FOLDER + 'idx_adj_lists.txt', 'r') as f:
    for l in f:
        o, i, w1 = l.split('\t')
        #o = o.strip()
        i = i.strip()
        
        if (o in ids) and (i not in ids):
            green.add(i)
        if (i in ids) and (o not in ids):
            green.add(o)
            
        
        if count % 10000 == 0:
            print(count)
        count += 1
    print(time.time()-s)
    print(len(green), len(ids.union(green)))


    

count = 0
edges = set()
total = ids.union(green)

with open(FOLDER + 'idx_adj_lists.txt', 'r') as f:
    for l in f:
        o, i , w_order = l.split('\t')
        i = i.strip()
        o = o.strip()

        w = int(w_order.strip())
        
        if (o in total) and (i in total):
            try:
                w_click = int(clickstreams[(o,i)])
                edges.add((o,i, 1, w, w_click))
            except:
                edges.add((o,i, 1, w, 10))
        elif (o in green) and (i not in total) :
            outside_green += 1
            try:
                w_click = int(clickstreams[(o,i)])
                w_outside_green += w_click
            except:
                w_outside_green += 0
        elif (i in green) and (o not in total) :
            toward_green += 1
            try:
                w_click = int(clickstreams[(o,i)])
                w_toward_green += w_click
            except:
                w_toward_green += 0
        elif (i not in total) and (o not in total) :
            across_outside += 1
            try:
                w_click = int(clickstreams[(o,i)])
                w_across_outside += w_click
            except:
                w_across_outside += 0

        if count % 10000 == 0:
            print(count)
        count += 1

    print(len(edges), toward_green, outside_green, across_outside)


with open('data/graphs/edges_' + TOPIC + '.p', 'wb') as f_pickle_edges:
    pickle.dump(edges, f_pickle_edges)

dict_info = {'toward_green':toward_green,
            'outside_green':outside_green,
            'across_outside':across_outside, 
            'w_toward_green':w_toward_green,
            'w_outside_green':w_outside_green,
            'w_across_outside':w_across_outside}

with open('data/graphs/info_edges_' + TOPIC + '.p', 'wb') as f_pickle_info:
    pickle.dump(dict_info, f_pickle_info)
