import os
import gzip
import pickle
import argparse
from collections import defaultdict


parser = argparse.ArgumentParser(description='Process graphs.')
parser.add_argument('--lang', type=str, help='topic name')

args = parser.parse_args()

lang = args.lang
folder = 'data/dumps/clickstreams/'
list_files = [f for f in os.listdir(folder) if f.startswith('clickstream-{}wiki'.format(lang))]

data_files = [folder+f for f in list_files]
print(data_files[0])
title_id = {}
with open('data/wikipedia_all/' + 'id_title.txt', 'r') as f:
    for l in f:
        idx, title = l.split('\t')
        
        title_id[title.strip()] = idx
print('Dictionary of title and respective ids has been loaded.')


clickstream_dictionary = defaultdict(int)
entrance_dictionary = defaultdict(int)
#monthly_click = {}
monthly_entrance = {}

for raw_click in data_files:
    print(raw_click)
    date = '_'.join(raw_click.split('.')[0].split('-')[-2:])
    #monthly_click[date] = {}
    monthly_entrance[date] = {}
    with gzip.open(raw_click,'rt') as f:
        for line in f:
            title_out, title_in, kind, clicks = line.split('\t')
            # decode titles
            try:
                #if kind == 'internal':
                out = title_id[title_out]#.lower()]       
                in_ = title_id[title_in.strip()]#.lower()]
                clickstream_dictionary[(out, in_)] += int(clicks.strip())
                #monthly_click[date][(out, in_)] = int(clicks.strip())
            except KeyError:
                try:
                    #if kind=='external':
                    in_ = title_id[title_in.strip()]#.lower()]
                    entrance_dictionary[in_] += int(clicks.strip())
                    monthly_entrance[date][in_] = int(clicks.strip())
                except:
                    continue
                continue

    #with open('data/wikipedia_all/' + lang + '_' + str(date) + '_monthly_click' + '.p', 'wb') as f:
    #    pickle.dump(monthly_click, f)
with open('data/wikipedia_all/' + lang + '_clickstreams' + '.p', 'wb') as f:
    pickle.dump(clickstream_dictionary, f)

with open('data/wikipedia_all/' + lang + '_enter_external' + '.p', 'wb') as f:
    pickle.dump(entrance_dictionary, f)

with open('data/wikipedia_all/' + lang + '_monthly_entrance' + '.p', 'wb') as f:
    pickle.dump(monthly_entrance, f)

