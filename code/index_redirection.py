import os
import ast
import time


import time
import ast

FOLDER_WIKI = 'data/wikipedia_all/'


t_start = time.time()
title_id = {}
with open(FOLDER_WIKI + 'id_title.txt', 'r') as f:
    for l in f:
        idx, title = l.split('\t')
        title_id[title.strip()] = idx
print('Dictionary of title and respective ids has been loaded.')
print(time.time() - t_start)

t_start = time.time()
with open(FOLDER_WIKI + 'idx_redirected_to.txt', 'w') as f_write:
    with open(FOLDER_WIKI + 'redirected_to.txt', 'r') as f:
        for l in f:
            idx, adj = l.split('\t')
            idx = idx.strip()
            #print(idx, adj)
            #replace_par = adj.strip().replace('(', '[').replace(')', ']')

            if len(adj) == 0: 
                print('no redirection')
                adj_f = list()
            else: 
                ad = ast.literal_eval(adj)
                adj_f = []
                for h in ad:
                    h = h.strip()
                    try:
                        adj_f.append(title_id[h])
                    except KeyError:
                        if len(h.split('_'))==1:
                            try:
                                adj_f.append(title_id[h.capitalize()])
                            except KeyError:       
                                #print('no article', h, idx)
                                continue
                        elif len(h.split('_'))>1:
                            splits_h = h.replace('_', ' ').strip()
                            splits_h = splits_h.split(' ')
                            splits_h[0] = splits_h[0][0].upper() + splits_h[0][1:]
                            splits_h = '_'.join(splits_h)
                            try:
                                adj_f.append(title_id[splits_h])
                            except KeyError:       
                                #print('no article', splits_h, idx)
                                continue


                        #print('no article', h, idx)
                        continue

                #print(adj_f, len(adj_f), idx)
                if len(adj_f) > 0:   
                    links_id = adj_f[0]
                    if idx == '175731':
                        print ('MERDAAAAAA')
                        print (links_id, adj_f)
                    f_write.write(idx + '\t' + str(links_id) + '\n')
print(time.time() - t_start)
        

"""
if len(replace_par) == 0: 
    ad = list()
    print('None')
else: 
    ad = ast.literal_eval(replace_par)

if len(ad) > 0:
    links_id = ad[0]

    try: links_id = title_id[links_id]
    except KeyError: continue
    f_write.write(idx + '\t' + str(links_id) + '\n')
"""

