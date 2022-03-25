import os
import ast
import time


FOLDER_WIKI = 'data/wikipedia_all/'


only_articles_ids = []
with open(FOLDER_WIKI + 'only_articles.txt', 'r') as f:
    for l in f:
        idx = l.split('\t')[0]
        only_articles_ids += [idx]
only_articles_ids = set(only_articles_ids)

t_start = time.time()
title_id = {}
with open(FOLDER_WIKI + 'id_title.txt', 'r') as f:
    for l in f:
        idx, title = l.split('\t')
        if idx in only_articles_ids:
            title_id[title.strip()] = idx
print('Dictionary of title and respective ids has been loaded.')
print(time.time() - t_start)

t_start = time.time()
redirects = {}
with open(FOLDER_WIKI + 'idx_redirected_to.txt', 'r') as f:
    for l in f:
        from_, to_ = l.split('\t')
        from_ = from_.strip()
        to_ = to_.strip()
        redirects[from_] = to_
print('Redirections.')
print(time.time() - t_start)


t_start = time.time()
count=0
with open(FOLDER_WIKI + 'idx_adj_lists.txt', 'w') as f_write:
    with open(FOLDER_WIKI + 'adj_lists.txt', 'r') as f:
        for l in f:
            idx, adj = l.split('\t')
            idx = idx.strip()
            try:
                redirects[idx]
                count += 1
                #print('REDIRECT PAGE: ', idx)
                continue
            except KeyError:  
                #print('EEEXCEPT')
                if len(adj) == 0: 
                    adj_f = list()
                else: 
                    ad = ast.literal_eval(adj)
                    adj_f = []
                    for h in ad:
                        try:
                            adj_f.append(title_id[h])
                        except KeyError:
                            #print('no article')
                            continue
            
                len_ad = len(adj_f)
                #print(len_ad)
                for i_link, link in enumerate(adj_f):
                    link = link#.split('#')[0]
                    if link == '175731':
                        print ('MERDAAAAAA')
                        print (redirects[link])
                    try: 
                        redirects[link]
                        f_write.write(idx + '\t' + str(redirects[link]) + '\t' + str(len_ad - i_link) + '\n')
                    except KeyError: 
                        f_write.write(idx + '\t' + str(link) + '\t' +  str(len_ad - i_link) + '\n') 
                        continue
            count += 1
            if count % 10000 == 0:
                print(count)
                print(idx + '\t' + str(link) + '\t' +  str(len_ad - i_link) + '\n')

print(time.time() - t_start)
